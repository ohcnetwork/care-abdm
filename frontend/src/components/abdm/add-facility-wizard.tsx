import {
  type CareFacilityDraft,
  blankFacilityDraft,
  toCreateBody,
  validateDraft,
} from "@/components/abdm/care-facility-draft";
import CareFacilityForm from "@/components/abdm/care-facility-form";
import FieldHelp from "@/components/abdm/field-help";
import HfrOnboardingWizard from "@/components/abdm/hfr-onboarding-wizard";
import { errorMessage } from "@/components/abdm/nhpr-shared";
import {
  RegistryFinder,
  RegistryRecord,
} from "@/components/abdm/registry-card";
import PluginComponent from "@/components/common/plugin-component";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Skeleton } from "@/components/ui/skeleton";
import { useTranslation } from "@/hooks/use-translation";
import careApi, {
  type AbdmCreateFacilityResponse,
  type AbdmFacilityPrefill,
  type AbdmHfrState,
  type CareGovtOrganization,
  type CareGovtOrganizationParent,
  type FacilityBridgeActionResponse,
} from "@/lib/careApi";
import { mutate, query } from "@/lib/request";
import { cn } from "@/lib/utils";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  ArrowRight,
  Building2,
  CheckCircle2,
  CircleDashed,
  ClipboardList,
  Hospital,
  Link2,
  Loader2,
  Search,
} from "lucide-react";
import { navigate, useQueryParams } from "raviger";
import { useEffect, useMemo, useState } from "react";

/**
 * "Add a facility" (ADR-016), at /abdm/facilities/new. Entered from the ABDM admin dashboard or from
 * an organization's facilities page (the host `AddFacilitySheet` override), which adds
 * `?organization=<id>` so the geo picker starts at that organization.
 *
 * 1 wizard, 3 ways in, chosen on the first step:
 * - linked:   the facility is already in the Health Facility Registry. Find it, pick it, and the
 *             Care form comes prefilled from the record. Create in Care and link in 1 call.
 * - register: the facility is new to the registry. Create it in Care first (the resumable state
 *             lives on the facility), then run the 5 HFR steps here, then register the services.
 * - care:     Care only. The core fields, nothing sent to ABDM.
 *
 * The URL carries `mode`, `facility` (once created) and `step`, so a refresh or a closed tab
 * resumes where the person was. Layout is append-only: the step list stays put, panels replace
 * below it.
 */

type Mode = "linked" | "register" | "care";
type Step = "choose" | "find" | "details" | "registry" | "services" | "done";
type Params = {
  mode?: Mode;
  facility?: string;
  step?: Step;
  organization?: string;
};

const STEPS: Record<Mode, Step[]> = {
  linked: ["choose", "find", "details", "services", "done"],
  register: ["choose", "details", "registry", "services", "done"],
  care: ["choose", "details", "done"],
};

const HIP_NAME_RE = /^[A-Za-z0-9 ]{1,15}$/;

function chainFromDetail(org: CareGovtOrganization): CareGovtOrganization[] {
  // The detail carries its parents nested; every parent has children by definition.
  const chain: CareGovtOrganization[] = [];
  let parent: CareGovtOrganizationParent | Record<string, never> | undefined =
    org.parent;
  while (parent && "id" in parent && parent.id) {
    chain.unshift({
      id: parent.id,
      name: parent.name ?? "",
      org_type: parent.org_type ?? "govt",
      level_cache: parent.level_cache ?? 0,
      has_children: true,
      metadata: parent.metadata,
    });
    parent = parent.parent;
  }
  chain.push(org);
  return chain;
}

function serverFieldErrors(error: unknown): Record<string, string> {
  const cause = (error as { cause?: { errors?: unknown } })?.cause;
  const list = cause?.errors;
  if (!Array.isArray(list)) return {};
  const out: Record<string, string> = {};
  for (const item of list) {
    const loc = (item as { loc?: unknown[] }).loc;
    const msg = (item as { msg?: string }).msg;
    if (Array.isArray(loc) && loc.length && typeof msg === "string")
      out[String(loc[0])] = msg;
  }
  return out;
}

function ModeCard({
  icon,
  title,
  body,
  onClick,
  primary,
}: {
  icon: React.ReactNode;
  title: string;
  body: string;
  onClick: () => void;
  primary?: boolean;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        "hover:bg-accent grid gap-2 rounded-lg border p-4 text-left transition-colors",
        primary && "border-primary",
      )}
    >
      <span className="text-muted-foreground flex items-center gap-2 text-sm font-medium">
        {icon}
        {title}
      </span>
      <span className="text-sm">{body}</span>
    </button>
  );
}

export default function AddFacilityWizard() {
  const { t } = useTranslation();
  const qc = useQueryClient();
  const [params, setParams] = useQueryParams<Params>();
  const mode: Mode | undefined = params.mode;
  const facilityId = params.facility;
  const organizationId = params.organization;
  // Every URL write keeps the organization context.
  const setWizardParams = (next: Omit<Params, "organization">) =>
    setParams(
      organizationId ? { ...next, organization: organizationId } : next,
    );
  const steps = mode ? STEPS[mode] : STEPS.linked;

  // The step follows the URL once a facility exists; before that, it follows local progress.
  const [localStep, setLocalStep] = useState<Step>("choose");
  const step: Step = facilityId ? (params.step ?? "services") : localStep;
  const go = (next: Step) => {
    if (facilityId) setWizardParams({ ...params, step: next });
    else setLocalStep(next);
  };
  const choose = (next: Mode) => {
    setWizardParams({ mode: next });
    setLocalStep(next === "linked" ? "find" : "details");
  };
  const restart = () => {
    setWizardParams({});
    setLocalStep("choose");
  };

  const [picked, setPicked] = useState<AbdmFacilityPrefill | null>(null);
  const [draft, setDraft] = useState<CareFacilityDraft>(blankFacilityDraft);
  const [hipName, setHipName] = useState("");
  // True after the person pressed the create button. The form shows the errors only then.
  const [attempted, setAttempted] = useState(false);
  const [serverErrors, setServerErrors] = useState<Record<string, string>>({});
  const [actionError, setActionError] = useState<string>();

  const navOrg = useQuery<CareGovtOrganization>({
    queryKey: ["abdm", "govt-organization", organizationId],
    queryFn: query(careApi.govtOrganization, {
      pathParams: { organizationId: organizationId ?? "" },
      silent: true,
    }),
    enabled: Boolean(organizationId),
    retry: false,
  });

  const prefill = useMutation<AbdmFacilityPrefill, unknown, string>({
    mutationFn: (registryId) =>
      query(careApi.hfrPrefill, {
        queryParams: { facility_id: registryId },
        silent: true,
      })({ signal: new AbortController().signal }),
    onMutate: () => setActionError(undefined),
    onSuccess: (data) => {
      setPicked(data);
      setDraft((d) => ({
        ...d,
        name: data.care.name || d.name,
        address: data.care.address || d.address,
        pincode: data.care.pincode ? String(data.care.pincode) : d.pincode,
        latitude:
          data.care.latitude !== null ? String(data.care.latitude) : d.latitude,
        longitude:
          data.care.longitude !== null
            ? String(data.care.longitude)
            : d.longitude,
        facility_type: data.care.facility_type || d.facility_type,
      }));
      setHipName(data.hipName);
      go("details");
    },
    onError: (e) => setActionError(errorMessage(e, t("abdm_hfr_not_found"))),
  });

  const create = useMutation<AbdmCreateFacilityResponse, unknown, void>({
    mutationFn: () =>
      mutate(careApi.createFacility, { silent: true })({
        care: toCreateBody(draft),
        registry_id:
          mode === "linked" ? picked?.registry.facilityId : undefined,
        hip_name: mode === "care" ? undefined : hipName.trim() || undefined,
        organization: organizationId,
      }),
    onMutate: () => {
      setActionError(undefined);
      setServerErrors({});
    },
    onSuccess: (data) => {
      qc.invalidateQueries({ queryKey: ["abdm", "admin", "overview"] });
      setWizardParams({
        mode,
        facility: data.facility.id,
        step:
          mode === "register"
            ? "registry"
            : mode === "care"
              ? "done"
              : "services",
      });
    },
    onError: (e) => {
      const fields = serverFieldErrors(e);
      setServerErrors(fields);
      setActionError(
        Object.keys(fields).length
          ? t("abdm_form_fix_fields")
          : errorMessage(e, t("abdm_create_failed")),
      );
    },
  });

  const facilityState = useQuery<AbdmHfrState>({
    queryKey: ["abdm", "facility", facilityId, "hfr"],
    queryFn: query(careApi.hfrOnboarding, {
      pathParams: { facilityId: facilityId ?? "" },
      silent: true,
    }),
    enabled: Boolean(facilityId),
    retry: false,
  });
  const services = useMutation<FacilityBridgeActionResponse, unknown, void>({
    mutationFn: () =>
      mutate(careApi.registerHrpService, {
        pathParams: { facilityId: facilityId ?? "" },
        silent: true,
      })({}),
    onMutate: () => setActionError(undefined),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["abdm", "facility", facilityId] });
    },
    onError: (e) =>
      setActionError(errorMessage(e, t("abdm_hrp_register_failed"))),
  });

  const errors = useMemo(() => validateDraft(draft, t), [draft, t]);
  const hipNameInvalid = Boolean(hipName) && !HIP_NAME_RE.test(hipName);
  const canCreate =
    Object.keys(errors).length === 0 &&
    !hipNameInvalid &&
    (mode === "care" || Boolean(hipName.trim()));

  const geoInitial = useMemo<CareGovtOrganization[] | undefined>(() => {
    if (picked?.geo.state) {
      return picked.geo.district
        ? [picked.geo.state, picked.geo.district]
        : [picked.geo.state];
    }
    return navOrg.data && navOrg.data.org_type === "govt"
      ? chainFromDetail(navOrg.data)
      : undefined;
  }, [picked, navOrg.data]);

  const prefilledFields = useMemo(() => {
    const set = new Set<keyof CareFacilityDraft>();
    if (!picked) return set;
    if (picked.care.name) set.add("name");
    if (picked.care.address) set.add("address");
    if (picked.care.pincode) set.add("pincode");
    if (picked.care.latitude !== null) set.add("latitude");
    if (picked.care.longitude !== null) set.add("longitude");
    if (picked.care.facility_type) set.add("facility_type");
    return set;
  }, [picked]);

  useEffect(() => {
    // A resumed register-mode wizard with a submitted registry step moves on to services.
    if (
      facilityId &&
      mode === "register" &&
      step === "registry" &&
      facilityState.data?.config.facility_id
    )
      setWizardParams({ ...params, step: "services" });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [facilityState.data?.config.facility_id]);

  const config = facilityState.data?.config;
  const stepIndex = steps.indexOf(step);
  const stepTitle = (s: Step) => t(`abdm_add_step_${s}`);
  const busy = create.isPending || prefill.isPending || services.isPending;

  return (
    <PluginComponent>
      <div className="mx-auto grid max-w-4xl gap-4 p-4 md:p-6">
        <div className="flex flex-wrap items-center gap-3">
          <Hospital className="text-muted-foreground size-5" />
          <h1 className="text-lg font-semibold">{t("abdm_add_facility")}</h1>
          {navOrg.data && (
            <span className="text-muted-foreground text-sm">
              {navOrg.data.name}
            </span>
          )}
          {organizationId ? (
            <Button
              type="button"
              variant="ghost"
              size="sm"
              className="ml-auto"
              onClick={() =>
                navigate(`/organization/${organizationId}/facilities`)
              }
            >
              {t("abdm_add_back_to_list")}
            </Button>
          ) : (
            /* Full page load on purpose: a client-side move between /admin and an app route
               crashes the host's PinPageDialog (hooks order). */
            <a
              href="/admin/abdm"
              className="text-primary ml-auto text-sm underline-offset-4 hover:underline"
            >
              {t("abdm_add_back_to_admin")}
            </a>
          )}
        </div>
        <p className="text-muted-foreground text-sm">{t("abdm_add_intro")}</p>

        <ol
          className="grid gap-1 text-sm"
          style={{
            gridTemplateColumns: `repeat(${steps.length}, minmax(0, 1fr))`,
          }}
        >
          {steps.map((s, i) => {
            const done = i < stepIndex || step === "done";
            return (
              <li
                key={s}
                className={cn(
                  "flex items-center gap-2 rounded-md border px-2 py-1.5",
                  step === s && "border-primary",
                )}
              >
                {done ? (
                  <CheckCircle2 className="size-4 shrink-0 text-green-600" />
                ) : (
                  <CircleDashed className="text-muted-foreground size-4 shrink-0" />
                )}
                <span className="truncate">
                  {i + 1}. {stepTitle(s)}
                </span>
              </li>
            );
          })}
        </ol>

        {actionError && (
          <Alert variant="destructive">
            <AlertDescription>{actionError}</AlertDescription>
          </Alert>
        )}

        {step === "choose" && (
          <Card>
            <CardHeader>
              <CardTitle>{t("abdm_add_choose_title")}</CardTitle>
              <CardDescription>{t("abdm_add_choose_help")}</CardDescription>
            </CardHeader>
            <CardContent className="grid gap-3 md:grid-cols-3">
              <ModeCard
                primary
                icon={<Search className="size-4" />}
                title={t("abdm_add_mode_linked")}
                body={t("abdm_add_mode_linked_help")}
                onClick={() => choose("linked")}
              />
              <ModeCard
                icon={<ClipboardList className="size-4" />}
                title={t("abdm_add_mode_register")}
                body={t("abdm_add_mode_register_help")}
                onClick={() => choose("register")}
              />
              <ModeCard
                icon={<Building2 className="size-4" />}
                title={t("abdm_add_mode_care")}
                body={t("abdm_add_mode_care_help")}
                onClick={() => choose("care")}
              />
            </CardContent>
          </Card>
        )}

        {step === "find" && mode === "linked" && (
          <Card>
            <CardHeader>
              <CardTitle>{t("abdm_add_find_title")}</CardTitle>
              <CardDescription>{t("abdm_add_find_help")}</CardDescription>
            </CardHeader>
            <CardContent>
              <RegistryFinder
                idPrefix="abdm-add"
                busy={busy}
                pickLabel={t("abdm_add_pick")}
                lookup={async (id) => {
                  const result = await query(careApi.hfrSearchForCreate, {
                    queryParams: { facility_id: id },
                    silent: true,
                  })({ signal: new AbortController().signal });
                  const record = result.facilities[0];
                  if (!record) throw new Error(t("abdm_hfr_not_found"));
                  return record;
                }}
                search={({ name, state, ownership }) =>
                  query(careApi.hfrSearchForCreate, {
                    queryParams: { name, state, ownership },
                    silent: true,
                  })({ signal: new AbortController().signal })
                }
                onPick={(record) => prefill.mutate(record.facilityId)}
              />
            </CardContent>
            <CardFooter className="border-t">
              <Button type="button" variant="ghost" size="sm" onClick={restart}>
                {t("abdm_back")}
              </Button>
            </CardFooter>
          </Card>
        )}

        {step === "details" && mode && (
          <Card>
            <CardHeader>
              <CardTitle>{t("abdm_add_details_title")}</CardTitle>
              <CardDescription>
                {mode === "linked"
                  ? t("abdm_add_details_help_linked")
                  : t("abdm_add_details_help")}
              </CardDescription>
            </CardHeader>
            <CardContent className="grid gap-5">
              {picked && mode === "linked" && (
                <RegistryRecord
                  record={picked.registry}
                  action={
                    picked.alreadyLinked ? (
                      <Alert variant="warning">
                        <AlertDescription>
                          {t("abdm_add_already_linked", {
                            name: picked.alreadyLinked.name,
                          })}{" "}
                          <a
                            className="underline"
                            href={`/facility/${picked.alreadyLinked.id}/abdm/setup`}
                          >
                            {t("abdm_open_setup")}
                          </a>
                        </AlertDescription>
                      </Alert>
                    ) : (
                      <Badge variant="info" size="sm">
                        <Link2 className="size-3" /> {t("abdm_add_will_link")}
                      </Badge>
                    )
                  }
                />
              )}
              <CareFacilityForm
                draft={draft}
                onChange={(next) => setDraft((d) => ({ ...d, ...next }))}
                errors={attempted ? errors : {}}
                serverErrors={serverErrors}
                geoInitial={geoInitial}
                disabled={busy}
                prefilled={prefilledFields}
              />
              {mode !== "care" && (
                <div className="grid gap-1.5 md:max-w-sm">
                  <div className="flex min-h-5 items-center gap-1.5">
                    <Label htmlFor="add-hip-name">{t("abdm_hip_name")}</Label>
                    <FieldHelp
                      title={t("abdm_facility_help_hip_name_title")}
                      what={t("abdm_facility_help_hip_name_what")}
                      how={t("abdm_facility_help_hip_name_how")}
                      example={t("abdm_facility_help_hip_name_example")}
                    />
                    <span className="text-muted-foreground ml-auto w-12 text-right font-mono text-xs tabular-nums">
                      {hipName.length}/15
                    </span>
                  </div>
                  <Input
                    id="add-hip-name"
                    value={hipName}
                    maxLength={15}
                    disabled={busy}
                    onChange={(e) => setHipName(e.target.value)}
                  />
                  <span
                    className={cn(
                      "text-xs",
                      hipNameInvalid
                        ? "text-destructive"
                        : "text-muted-foreground",
                    )}
                  >
                    {hipNameInvalid
                      ? t("abdm_hip_name_invalid")
                      : t("abdm_hip_name_help")}
                  </span>
                </div>
              )}
            </CardContent>
            <CardFooter className="flex flex-wrap items-center gap-3 border-t">
              <Button
                type="button"
                variant="ghost"
                size="sm"
                disabled={busy}
                onClick={() => {
                  if (mode === "linked") go("find");
                  else restart();
                }}
              >
                {t("abdm_back")}
              </Button>
              <Button
                type="button"
                size="sm"
                className="ml-auto"
                disabled={
                  busy ||
                  Boolean(picked?.alreadyLinked) ||
                  (attempted && !canCreate)
                }
                onClick={() => {
                  setAttempted(true);
                  if (canCreate) create.mutate();
                }}
              >
                {create.isPending ? (
                  <Loader2 className="size-4 animate-spin" />
                ) : (
                  <Building2 className="size-4" />
                )}
                {mode === "linked"
                  ? t("abdm_add_create_and_link")
                  : t("abdm_add_create")}
              </Button>
            </CardFooter>
          </Card>
        )}

        {step === "registry" && facilityId && (
          <Card>
            <CardHeader>
              <CardTitle>{t("abdm_add_registry_title")}</CardTitle>
              <CardDescription>{t("abdm_add_registry_help")}</CardDescription>
            </CardHeader>
            <CardContent>
              <HfrOnboardingWizard
                facilityId={facilityId}
                embedded
                onSubmitted={() =>
                  setWizardParams({ ...params, step: "services" })
                }
              />
            </CardContent>
            <CardFooter className="border-t">
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="ml-auto"
                onClick={() => setWizardParams({ ...params, step: "done" })}
              >
                {t("abdm_add_finish_later")}
              </Button>
            </CardFooter>
          </Card>
        )}

        {step === "services" && facilityId && (
          <Card>
            <CardHeader>
              <CardTitle>{t("abdm_add_services_title")}</CardTitle>
              <CardDescription>{t("abdm_add_services_help")}</CardDescription>
            </CardHeader>
            <CardContent className="grid gap-4">
              {facilityState.isLoading && (
                <Skeleton className="h-24 w-full rounded-md" />
              )}
              {config && (
                <>
                  {config.facility_id ? (
                    <RegistryRecord
                      record={{
                        ...(config.hfr ?? {}),
                        facilityId: config.facility_id,
                        facilityName: config.facility_name,
                      }}
                    />
                  ) : (
                    <Alert variant="warning">
                      <AlertDescription>
                        {t("abdm_add_services_not_linked")}
                      </AlertDescription>
                    </Alert>
                  )}
                  <dl className="grid gap-2 text-sm sm:grid-cols-2">
                    <div className="grid gap-0.5">
                      <dt className="text-muted-foreground text-xs">
                        {t("abdm_hip_name")}
                      </dt>
                      <dd>{config.hip_name || "—"}</dd>
                    </div>
                    <div className="grid gap-0.5">
                      <dt className="text-muted-foreground text-xs">
                        {t("abdm_hip_id_issued")}
                      </dt>
                      <dd className="font-mono">
                        {config.hip_id || t("abdm_hip_id_pending")}
                      </dd>
                    </div>
                    <div className="grid gap-0.5">
                      <dt className="text-muted-foreground text-xs">
                        {t("abdm_hrp_registered_at")}
                      </dt>
                      <dd>
                        {config.hrp_registered_at
                          ? new Date(config.hrp_registered_at).toLocaleString()
                          : t("abdm_not_recorded")}
                      </dd>
                    </div>
                  </dl>
                  {config.last_error && (
                    <Alert variant="warning">
                      <AlertDescription>{config.last_error}</AlertDescription>
                    </Alert>
                  )}
                </>
              )}
            </CardContent>
            <CardFooter className="flex flex-wrap items-center gap-3 border-t">
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={() => setWizardParams({ ...params, step: "done" })}
              >
                {t("abdm_add_skip")}
              </Button>
              <div className="ml-auto flex items-center gap-2">
                <Button
                  type="button"
                  size="sm"
                  variant={config?.hrp_registered_at ? "outline" : "default"}
                  disabled={busy || !config?.facility_id || !config?.hip_name}
                  onClick={() => services.mutate()}
                >
                  {services.isPending && (
                    <Loader2 className="size-4 animate-spin" />
                  )}
                  {t("abdm_register_hrp_service")}
                </Button>
                {config?.hrp_registered_at && (
                  <Button
                    type="button"
                    size="sm"
                    onClick={() => setWizardParams({ ...params, step: "done" })}
                  >
                    {t("abdm_add_continue")} <ArrowRight className="size-4" />
                  </Button>
                )}
              </div>
            </CardFooter>
          </Card>
        )}

        {step === "done" && facilityId && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle2 className="size-5 text-green-600" />
                {t("abdm_add_done_title")}
              </CardTitle>
              <CardDescription>
                {mode === "care"
                  ? t("abdm_add_done_help_care")
                  : t("abdm_add_done_help")}
              </CardDescription>
            </CardHeader>
            <CardContent className="grid gap-2 text-sm">
              {config && (
                <ul className="grid gap-1">
                  <li className="flex items-center gap-2">
                    <CheckCircle2 className="size-4 text-green-600" />
                    {t("abdm_add_done_created")}
                  </li>
                  <li className="flex items-center gap-2">
                    {config.facility_id ? (
                      <CheckCircle2 className="size-4 text-green-600" />
                    ) : (
                      <CircleDashed className="text-muted-foreground size-4" />
                    )}
                    {config.facility_id
                      ? t("abdm_add_done_linked", { id: config.facility_id })
                      : t("abdm_add_done_not_linked")}
                  </li>
                  {mode !== "care" && (
                    <li className="flex items-center gap-2">
                      {config.hip_id ? (
                        <CheckCircle2 className="size-4 text-green-600" />
                      ) : (
                        <CircleDashed className="text-muted-foreground size-4" />
                      )}
                      {config.hip_id
                        ? t("abdm_add_done_services", { id: config.hip_id })
                        : t("abdm_add_done_no_services")}
                    </li>
                  )}
                </ul>
              )}
            </CardContent>
            <CardFooter className="flex flex-wrap gap-2 border-t">
              <Button
                type="button"
                size="sm"
                onClick={() => navigate(`/facility/${facilityId}`)}
              >
                {t("abdm_add_open_facility")}
              </Button>
              {mode !== "care" && (
                <Button
                  type="button"
                  size="sm"
                  variant="outline"
                  onClick={() => navigate(`/facility/${facilityId}/abdm/setup`)}
                >
                  {t("abdm_open_setup")}
                </Button>
              )}
              <Button
                type="button"
                size="sm"
                variant="ghost"
                className="ml-auto"
                onClick={() => {
                  restart();
                  setPicked(null);
                  setDraft(blankFacilityDraft);
                  setHipName("");
                  setAttempted(false);
                }}
              >
                {t("abdm_add_another")}
              </Button>
            </CardFooter>
          </Card>
        )}
      </div>
    </PluginComponent>
  );
}
