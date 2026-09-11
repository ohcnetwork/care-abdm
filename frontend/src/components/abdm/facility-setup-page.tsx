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
  type AbdmFacilityConfig,
  type FacilityBridgeActionResponse,
} from "@/lib/careApi";
import { mutate, query } from "@/lib/request";
import { cn } from "@/lib/utils";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  ArrowLeft,
  CheckCircle2,
  CircleDashed,
  Hospital,
  Link2,
  Server,
} from "lucide-react";
import { Link } from "raviger";
import { useEffect, useMemo, useState } from "react";

/**
 * Dedicated page for the ADR-007 facility setup form, mounted by the host
 * router at /facility/:facilityId/abdm/setup (manifest `routes`, merged in
 * care_fe/src/Routers/AppRouter.tsx:104-115).
 *
 * WHY A PAGE AND NOT A DIALOG
 * ---------------------------
 * The FacilityHomeActions slot renders inside the host's "Configurations"
 * dropdown (care_fe/src/components/Facility/FacilityHome.tsx:253-257). Every
 * portal of this plug mounts into `PluginComponent`, which keeps the design
 * tokens (see components/common/plugin-component.tsx). Inside that dropdown
 * the container has a transformed ancestor, so `position: fixed` anchors to
 * the dropdown popup and not to the viewport. A dialog opened from that slot
 * can therefore never centre itself, and it unmounts when the dropdown
 * closes. The slot now only links here.
 */

const blankConfig: AbdmFacilityConfig = {
  hip_id: "",
  bridge_id: "",
  service_id: "",
  facility_id: "",
  facility_name: "",
  hip_name: "",
  x_hip_id_source: "hip_id",
  bridge_url: "",
};

type TextField = keyof Pick<
  AbdmFacilityConfig,
  | "hip_id"
  | "bridge_id"
  | "service_id"
  | "facility_id"
  | "facility_name"
  | "hip_name"
  | "bridge_url"
>;

const X_HIP_ID_SOURCES = [
  { value: "hip_id", labelKey: "abdm_hip_id" },
  { value: "bridge_id", labelKey: "abdm_bridge_id" },
  { value: "service_id", labelKey: "abdm_service_id" },
] as const;

function errorMessage(error: unknown, fallback: string) {
  if (error && typeof error === "object" && "cause" in error) {
    const cause = (error as { cause?: Record<string, unknown> }).cause;
    const value = cause?.errors ?? cause?.message;
    if (typeof value === "string") return value;
  }
  return fallback;
}

function Field({
  name,
  label,
  hint,
  placeholder,
  config,
  onChange,
}: {
  name: TextField;
  label: string;
  hint?: string;
  placeholder?: string;
  config: AbdmFacilityConfig;
  onChange: (next: Partial<AbdmFacilityConfig>) => void;
}) {
  return (
    <div className="grid gap-1.5">
      <Label htmlFor={`abdm-${name}`}>{label}</Label>
      <Input
        id={`abdm-${name}`}
        value={config[name] ?? ""}
        placeholder={placeholder}
        autoComplete="off"
        spellCheck={false}
        onChange={(e) => onChange({ [name]: e.target.value })}
      />
      {hint && <p className="text-muted-foreground text-xs">{hint}</p>}
    </div>
  );
}

/** Shows when an ABDM registration call last succeeded. */
function RegistrationStatus({
  label,
  timestamp,
  notRecorded,
}: {
  label: string;
  timestamp?: string;
  notRecorded: string;
}) {
  const done = Boolean(timestamp);
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 text-xs",
        done ? "text-green-800" : "text-muted-foreground",
      )}
    >
      {done ? (
        <CheckCircle2 className="size-3.5" />
      ) : (
        <CircleDashed className="size-3.5" />
      )}
      {label}: {timestamp ? new Date(timestamp).toLocaleString() : notRecorded}
    </span>
  );
}

export default function AbdmFacilitySetupPage({
  facilityId,
}: {
  facilityId: string;
}) {
  const { t } = useTranslation();
  const qc = useQueryClient();
  const [config, setConfig] = useState<AbdmFacilityConfig>(blankConfig);
  const [actionError, setActionError] = useState<string>();

  const facility = useQuery({
    queryKey: ["abdm", "host-facility", facilityId],
    queryFn: query(careApi.hostFacility, {
      pathParams: { facilityId },
      silent: true,
    }),
    retry: false,
  });
  const gateway = useQuery({
    queryKey: ["abdm", "gateway-status"],
    queryFn: query(careApi.gatewayStatus, { silent: true }),
    retry: false,
  });
  const settings = useQuery<AbdmFacilityConfig>({
    queryKey: ["abdm", "facility", facilityId],
    queryFn: query(careApi.facilityAbdm, {
      pathParams: { facilityId },
      silent: true,
    }),
    retry: false,
  });

  useEffect(() => {
    if (settings.data) setConfig({ ...blankConfig, ...settings.data });
  }, [settings.data]);

  const applyResult = (data: AbdmFacilityConfig) => {
    setConfig({ ...blankConfig, ...data });
    qc.setQueryData(["abdm", "facility", facilityId], data);
  };

  const save = useMutation<AbdmFacilityConfig, unknown, AbdmFacilityConfig>({
    mutationFn: mutate(careApi.updateFacilityAbdm, {
      pathParams: { facilityId },
      silent: true,
    }),
    onMutate: () => setActionError(undefined),
    onSuccess: applyResult,
    onError: (error) =>
      setActionError(errorMessage(error, t("abdm_facility_save_failed"))),
  });
  const bridge = useMutation<
    FacilityBridgeActionResponse,
    unknown,
    { url?: string | null }
  >({
    mutationFn: mutate(careApi.registerBridgeUrl, {
      pathParams: { facilityId },
      silent: true,
    }),
    onMutate: () => setActionError(undefined),
    onSuccess: (data) => applyResult(data.config),
    onError: (error) =>
      setActionError(errorMessage(error, t("abdm_bridge_register_failed"))),
  });
  const hrp = useMutation<
    FacilityBridgeActionResponse,
    unknown,
    Record<string, never>
  >({
    mutationFn: mutate(careApi.registerHrpService, {
      pathParams: { facilityId },
      silent: true,
    }),
    onMutate: () => setActionError(undefined),
    onSuccess: (data) => applyResult(data.config),
    onError: (error) =>
      setActionError(errorMessage(error, t("abdm_hrp_register_failed"))),
  });

  const saved = settings.data;
  const dirty = useMemo(() => {
    if (!saved) return false;
    return (Object.keys(blankConfig) as (keyof AbdmFacilityConfig)[]).some(
      (key) => (config[key] ?? "") !== (saved[key] ?? ""),
    );
  }, [config, saved]);

  const busy = save.isPending || bridge.isPending || hrp.isPending;
  const update = (next: Partial<AbdmFacilityConfig>) =>
    setConfig((current) => ({ ...current, ...next }));

  const gatewayVariant = gateway.isLoading
    ? "neutral"
    : gateway.data?.ok
      ? "success"
      : "destructive";
  const gatewayLabel = gateway.isLoading
    ? t("abdm_gateway_checking")
    : gateway.isError || !gateway.data?.ok
      ? t("abdm_gateway_unreachable")
      : t("abdm_gateway_connected");

  return (
    <PluginComponent>
      <div className="mx-auto w-full max-w-4xl p-4 md:p-6">
        <Link
          href={`/facility/${facilityId}/overview`}
          className="text-muted-foreground hover:text-foreground inline-flex items-center gap-1.5 text-sm"
        >
          <ArrowLeft className="size-4" />
          {t("abdm_back_to_facility")}
        </Link>

        <div className="mt-3 flex flex-wrap items-start justify-between gap-3">
          <div className="grid gap-1">
            <h1 className="text-2xl font-semibold">
              {t("abdm_facility_settings")}
            </h1>
            {facility.isLoading ? (
              <Skeleton className="h-4 w-40" />
            ) : facility.data?.name ? (
              <p className="text-muted-foreground text-sm">
                {facility.data.name}
              </p>
            ) : null}
          </div>
          <Badge variant={gatewayVariant} size="lg">
            {gatewayLabel}
          </Badge>
        </div>

        <p className="text-muted-foreground mt-3 max-w-2xl text-sm">
          {t("abdm_facility_setup_intro")}
        </p>

        <div className="mt-6 grid gap-4">
          {settings.isError && (
            <Alert variant="destructive">
              <AlertDescription>
                {t("abdm_facility_load_failed")}
              </AlertDescription>
            </Alert>
          )}
          {actionError && (
            <Alert variant="destructive">
              <AlertDescription>{actionError}</AlertDescription>
            </Alert>
          )}
          {config.last_error && (
            <Alert variant="warning">
              <AlertDescription>{config.last_error}</AlertDescription>
            </Alert>
          )}

          {settings.isLoading ? (
            <div className="grid gap-4">
              <Skeleton className="h-56 w-full rounded-xl" />
              <Skeleton className="h-56 w-full rounded-xl" />
            </div>
          ) : (
            <>
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Hospital className="text-muted-foreground size-4" />
                    {t("abdm_section_facility_identity")}
                  </CardTitle>
                  <CardDescription>
                    {t("abdm_section_facility_identity_help")}
                  </CardDescription>
                </CardHeader>
                <CardContent className="grid gap-4 md:grid-cols-2">
                  <Field
                    name="facility_id"
                    label={t("abdm_facility_hfr_id")}
                    hint={t("abdm_facility_hfr_id_help")}
                    placeholder="IN0710000001"
                    config={config}
                    onChange={update}
                  />
                  <Field
                    name="facility_name"
                    label={t("abdm_facility_name")}
                    hint={t("abdm_facility_name_help")}
                    config={config}
                    onChange={update}
                  />
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Server className="text-muted-foreground size-4" />
                    {t("abdm_section_hip_identity")}
                  </CardTitle>
                  <CardDescription>
                    {t("abdm_section_hip_identity_help")}
                  </CardDescription>
                </CardHeader>
                <CardContent className="grid gap-4">
                  <div className="grid gap-4 md:grid-cols-2">
                    <Field
                      name="hip_id"
                      label={t("abdm_hip_id")}
                      config={config}
                      onChange={update}
                    />
                    <Field
                      name="hip_name"
                      label={t("abdm_hip_name")}
                      config={config}
                      onChange={update}
                    />
                    <Field
                      name="bridge_id"
                      label={t("abdm_bridge_id")}
                      config={config}
                      onChange={update}
                    />
                    <Field
                      name="service_id"
                      label={t("abdm_service_id")}
                      config={config}
                      onChange={update}
                    />
                  </div>
                  <div className="grid gap-1.5">
                    <Label id="abdm-x-hip-id-source-label">
                      {t("abdm_x_hip_id_source")}
                    </Label>
                    <div
                      role="radiogroup"
                      aria-labelledby="abdm-x-hip-id-source-label"
                      className="bg-muted-background flex w-fit gap-1 rounded-lg p-1"
                    >
                      {X_HIP_ID_SOURCES.map((option) => {
                        const active = config.x_hip_id_source === option.value;
                        return (
                          <button
                            key={option.value}
                            type="button"
                            role="radio"
                            aria-checked={active}
                            onClick={() =>
                              update({ x_hip_id_source: option.value })
                            }
                            className={cn(
                              "cursor-pointer rounded-md px-3 py-1.5 text-sm font-medium transition",
                              active
                                ? "bg-background text-foreground shadow-xs"
                                : "text-muted-foreground hover:text-foreground",
                            )}
                          >
                            {t(option.labelKey)}
                          </button>
                        );
                      })}
                    </div>
                    <p className="text-muted-foreground text-xs">
                      {t("abdm_x_hip_id_source_help")}
                    </p>
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Link2 className="text-muted-foreground size-4" />
                    {t("abdm_section_registration")}
                  </CardTitle>
                  <CardDescription>
                    {t("abdm_section_registration_help")}
                  </CardDescription>
                </CardHeader>
                <CardContent className="grid gap-4">
                  <Field
                    name="bridge_url"
                    label={t("abdm_bridge_url")}
                    hint={t("abdm_bridge_url_help")}
                    placeholder="https://care.example.org/api/abdm"
                    config={config}
                    onChange={update}
                  />
                  <div className="grid gap-1.5">
                    <RegistrationStatus
                      label={t("abdm_bridge_registered_at")}
                      timestamp={config.bridge_url_registered_at}
                      notRecorded={t("abdm_not_recorded")}
                    />
                    <RegistrationStatus
                      label={t("abdm_hrp_registered_at")}
                      timestamp={config.hrp_registered_at}
                      notRecorded={t("abdm_not_recorded")}
                    />
                  </div>
                </CardContent>
                <CardFooter className="flex flex-wrap gap-2 border-t">
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    disabled={busy || dirty}
                    onClick={() =>
                      bridge.mutate({ url: config.bridge_url || null })
                    }
                  >
                    {t("abdm_register_bridge_url")}
                  </Button>
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    disabled={busy || dirty}
                    onClick={() => hrp.mutate({})}
                  >
                    {t("abdm_register_hrp_service")}
                  </Button>
                  {dirty && (
                    <span className="text-muted-foreground self-center text-xs">
                      {t("abdm_save_before_register")}
                    </span>
                  )}
                </CardFooter>
              </Card>
            </>
          )}
        </div>

        {/* Sticky, not fixed: the host renders this page inside its scrolling
            <main>, so a fixed bar would sit under the host sidebar. */}
        <div className="bg-background/95 sticky bottom-0 z-10 -mx-4 mt-4 flex flex-wrap items-center gap-3 border-t px-4 py-3 backdrop-blur md:-mx-6 md:px-6">
          <span className="text-muted-foreground text-xs">
            {dirty ? t("abdm_unsaved_changes") : t("abdm_all_changes_saved")}
          </span>
          <div className="ml-auto flex gap-3">
            <Button
              type="button"
              variant="outline"
              size="sm"
              disabled={!dirty || busy}
              onClick={() => saved && setConfig({ ...blankConfig, ...saved })}
            >
              {t("abdm_discard")}
            </Button>
            <Button
              type="button"
              size="sm"
              disabled={!dirty || busy}
              onClick={() => save.mutate(config)}
            >
              {t("abdm_save")}
            </Button>
          </div>
        </div>
      </div>
    </PluginComponent>
  );
}
