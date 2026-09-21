import HprLoginDialog from "@/components/abdm/hpr-login-dialog";
import { errorMessage } from "@/components/abdm/nhpr-shared";
import MasterSelect from "@/components/abdm/master-select";
import { selectClass } from "@/components/abdm/nhpr-shared";
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
import NhprField from "@/components/abdm/nhpr-field";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { useTranslation } from "@/hooks/use-translation";
import careApi, { type AbdmHfrState, type AbdmHfrStep } from "@/lib/careApi";
import { mutate, query } from "@/lib/request";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Building2,
  CheckCircle2,
  CircleDashed,
  Loader2,
  LogIn,
} from "lucide-react";
import { navigate } from "raviger";
import { Fragment, useEffect, useMemo, useState } from "react";

/**
 * HFR onboarding wizard (ADR-015, M4 journey 3), at /facility/:facilityId/abdm/hfr/register.
 * Five calls in a fixed order: dedup, basic (creates the tracking id), additional, detailed, submit.
 * Basic and submit need the manager's HPR token, so the page opens the HPR login first. Every
 * coded field is a master pick (registries/nhpr/hfr §Codes, not names). The plug relays the
 * documented body; the desk fills it here. Photos go as base64; the plug stores only their names.
 */

type Json = Record<string, unknown>;

const STEPS: AbdmHfrStep[] = [
  "dedup",
  "basic",
  "additional",
  "detailed",
  "submit",
];
const DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"];
const YES_NO = ["Y", "N"];

const Field = NhprField;

function Text({
  id,
  value,
  onChange,
  placeholder,
  type = "text",
  inputMode,
}: {
  id: string;
  value: string;
  onChange: (v: string) => void;
  placeholder?: string;
  type?: string;
  inputMode?: "numeric" | "decimal" | "email" | "tel" | "url";
}) {
  return (
    <Input
      id={id}
      type={type}
      inputMode={inputMode}
      value={value}
      placeholder={placeholder}
      onChange={(e) => onChange(e.target.value)}
    />
  );
}

function Select({
  id,
  value,
  onChange,
  options,
  placeholder,
}: {
  id: string;
  value: string;
  onChange: (v: string) => void;
  options: { code: string; name: string }[];
  placeholder?: string;
}) {
  return (
    <select
      id={id}
      className={selectClass}
      value={value}
      onChange={(e) => onChange(e.target.value)}
    >
      <option value="">{placeholder ?? "—"}</option>
      {options.map((o) => (
        <option key={o.code} value={o.code}>
          {o.name}
        </option>
      ))}
    </select>
  );
}

function fileToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result).split(",")[1] ?? "");
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(file);
  });
}

function Photo({
  id,
  labelKey,
  value,
  onChange,
  t,
}: {
  id: string;
  labelKey: string;
  value: { name: string; value: string };
  onChange: (v: { name: string; value: string }) => void;
  t: (k: string) => string;
}) {
  return (
    <Field
      labelKey={labelKey}
      htmlFor={id}
      hint={
        value.name
          ? `${value.name}${value.value ? "" : ` (${t("abdm_hfr_photo_saved")})`}`
          : t("abdm_hfr_photo_help")
      }
    >
      <Input
        id={id}
        type="file"
        accept="image/png,image/jpeg"
        onChange={async (e) => {
          const file = e.target.files?.[0];
          if (!file) return;
          if (file.size > 5 * 1024 * 1024) return;
          onChange({ name: file.name, value: await fileToBase64(file) });
        }}
      />
    </Field>
  );
}

function num(value: string): number | undefined {
  const n = Number(value);
  return value === "" || Number.isNaN(n) ? undefined : n;
}

export default function HfrOnboardingWizard({
  facilityId,
  embedded = false,
  onSubmitted,
}: {
  facilityId: string;
  /** Inside the "Add a facility" wizard (ADR-016): no page frame, no header, no setup link. */
  embedded?: boolean;
  /** Called once the submit step succeeds. */
  onSubmitted?: (state: AbdmHfrState) => void;
}) {
  const { t } = useTranslation();
  const qc = useQueryClient();
  const key = ["abdm", "facility", facilityId, "hfr"];
  const state = useQuery<AbdmHfrState>({
    queryKey: key,
    queryFn: query(careApi.hfrOnboarding, {
      pathParams: { facilityId },
      silent: true,
    }),
    retry: false,
  });
  const hpr = useQuery({
    queryKey: ["abdm", "me", "hpr"],
    queryFn: query(careApi.hprState, { silent: true }),
    retry: false,
  });
  const [loginOpen, setLoginOpen] = useState(false);
  const [step, setStep] = useState<AbdmHfrStep>("dedup");
  const [error, setError] = useState<string>();
  const onboarding = state.data?.onboarding ?? null;

  // Form state, 1 object per step, in the documented shape.
  const [dedup, setDedup] = useState({
    name: "",
    address: "",
    state: "",
    district: "",
    subDistrict: "",
  });
  const [basic, setBasic] = useState<Json>({});
  const [additional, setAdditional] = useState<Json>({
    linkedProgramIds: {},
    generalInformation: {},
  });
  const [detailed, setDetailed] = useState<Json>({
    specialities: [],
    medicalInfrastructure: {},
    pharmacyDetails: {},
    bloodBankDetails: {},
    imagingServices: [],
    diagnosticServices: [],
  });
  const [submitInfo, setSubmitInfo] = useState({ sourceOfInformation: "" });
  const [photos, setPhotos] = useState<{
    board: { name: string; value: string };
    building: { name: string; value: string };
  }>({ board: { name: "", value: "" }, building: { name: "", value: "" } });

  useEffect(() => {
    const s = state.data;
    if (!s) return;
    setDedup((d) => ({
      ...d,
      name: d.name || s.prefill.facilityName,
      address: d.address || s.prefill.address,
    }));
    if (s.onboarding?.basic && Object.keys(s.onboarding.basic).length) {
      setBasic((b) => (Object.keys(b).length ? b : s.onboarding!.basic));
      const uploads = s.onboarding.basic.facilityUploads as Json | undefined;
      if (uploads) {
        setPhotos({
          board: (uploads.facilityBoardPhoto as {
            name: string;
            value: string;
          }) ?? { name: "", value: "" },
          building: (uploads.facilityBuildingPhoto as {
            name: string;
            value: string;
          }) ?? { name: "", value: "" },
        });
      }
    } else {
      setBasic((b) =>
        Object.keys(b).length
          ? b
          : {
              facilityName: s.prefill.facilityName,
              facilityAddressDetails: {
                country: "India",
                addressLine1: s.prefill.address,
                pincode: s.prefill.pincode,
                latitude: s.prefill.latitude,
                longitude: s.prefill.longitude,
                facilityRegion: "U",
              },
              facilityContactInformation: {
                facilityContactNumber: s.prefill.phone.replace(/^\+91/, ""),
              },
              timingsOfFacility: DAYS.slice(0, 6).map((d) => ({
                workingDays: d,
                openingHours: "9:00 AM - 6:00 PM",
              })),
              abdmCompliantSoftware: [
                { existingSoftwares: ["CARE"], anyOther: "" },
              ],
              facilityOperationalStatus: "F",
              specialityTypeCode: "SINGLE",
            },
      );
    }
    if (s.onboarding?.additional && Object.keys(s.onboarding.additional).length)
      setAdditional((a) =>
        Object.keys(a.linkedProgramIds as Json).length
          ? a
          : s.onboarding!.additional,
      );
    if (s.onboarding?.detailed && Object.keys(s.onboarding.detailed).length)
      setDetailed((d) =>
        (d.specialities as unknown[]).length ? d : s.onboarding!.detailed,
      );
    if (s.onboarding) {
      const next: Record<string, AbdmHfrStep> = {
        draft: "basic",
        basic_saved: "additional",
        additional_saved: "detailed",
        detailed_saved: "submit",
        submitted: "submit",
        failed: "basic",
      };
      setStep((current) =>
        current === "dedup" && s.onboarding!.status !== "draft"
          ? next[s.onboarding!.status]
          : current,
      );
    }
  }, [state.data]);

  const run = useMutation<
    AbdmHfrState,
    unknown,
    { step: AbdmHfrStep; payload: Json }
  >({
    mutationFn: mutate(careApi.hfrOnboardingStep, {
      pathParams: { facilityId },
      silent: true,
    }),
    onMutate: () => setError(undefined),
    onSuccess: (data, vars) => {
      qc.setQueryData(key, data);
      qc.invalidateQueries({ queryKey: ["abdm", "facility", facilityId] });
      const index = STEPS.indexOf(vars.step);
      if (vars.step !== "submit" && index >= 0) setStep(STEPS[index + 1]);
      if (vars.step === "submit") onSubmitted?.(data);
    },
    onError: (e) => {
      const cause = (e as { cause?: AbdmHfrState }).cause;
      if (cause && cause.onboarding !== undefined)
        qc.setQueryData(key, { ...cause, errors: undefined });
      setError(errorMessage(e, t("abdm_hfr_step_failed")));
    },
  });

  const address = (basic.facilityAddressDetails as Json) ?? {};
  const contact = (basic.facilityContactInformation as Json) ?? {};
  const setBasicField = (k: string, v: unknown) =>
    setBasic((b) => ({ ...b, [k]: v }));
  const setAddress = (k: string, v: unknown) =>
    setBasicField("facilityAddressDetails", { ...address, [k]: v });
  const setContact = (k: string, v: unknown) =>
    setBasicField("facilityContactInformation", { ...contact, [k]: v });
  const somCodes = useMemo(
    () =>
      String(basic.systemOfMedicineCode ?? "")
        .split(",")
        .filter(Boolean),
    [basic.systemOfMedicineCode],
  );
  const general = (additional.generalInformation as Json) ?? {};
  const programs = (additional.linkedProgramIds as Json) ?? {};
  const infra = (detailed.medicalInfrastructure as Json) ?? {};
  const pharmacy = (detailed.pharmacyDetails as Json) ?? {};
  const bloodBank = (detailed.bloodBankDetails as Json) ?? {};
  const specialities = (detailed.specialities as Json[]) ?? [];
  const setDetailedField = (k: string, v: unknown) =>
    setDetailed((d) => ({ ...d, [k]: v }));

  const sessionActive = Boolean(state.data?.hprSession.active);
  const busy = run.isPending;
  const submitted = onboarding?.status === "submitted";

  const timings = (basic.timingsOfFacility as Json[]) ?? [];
  const setTiming = (day: string, hours: string) => {
    const rest = timings.filter((x) => x.workingDays !== day);
    setBasicField(
      "timingsOfFacility",
      hours ? [...rest, { workingDays: day, openingHours: hours }] : rest,
    );
  };

  const basicPayload = (): Json => ({
    ...basic,
    facilityUploads: {
      facilityBoardPhoto: photos.board,
      facilityBuildingPhoto: photos.building,
    },
    facilityAddressDetails: address,
    facilityContactInformation: contact,
  });

  const stepTitle = (s: AbdmHfrStep) => t(`abdm_hfr_step_${s}`);

  const Frame = embedded ? Fragment : PluginComponent;

  return (
    <Frame>
      <div
        className={
          embedded ? "grid gap-4" : "mx-auto grid max-w-4xl gap-4 p-4 md:p-6"
        }
      >
        {!embedded && (
          <>
            <div className="flex flex-wrap items-center gap-3">
              <Building2 className="text-muted-foreground size-5" />
              <h1 className="text-lg font-semibold">
                {t("abdm_hfr_wizard_title")}
              </h1>
              <span className="text-muted-foreground text-sm">
                {state.data?.prefill.facilityName}
              </span>
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="ml-auto"
                onClick={() => navigate(`/facility/${facilityId}/abdm/setup`)}
              >
                {t("abdm_open_setup")}
              </Button>
            </div>
            <p className="text-muted-foreground text-sm">
              {t("abdm_hfr_wizard_intro")}
            </p>
          </>
        )}

        <Card>
          <CardContent className="flex flex-wrap items-center gap-3 pt-6 text-sm">
            <LogIn className="text-muted-foreground size-4" />
            {sessionActive ? (
              <span>
                {t("abdm_hfr_session_active").replace(
                  "{{id}}",
                  state.data?.hprSession.hprId || "",
                )}
                {state.data?.hprSession.role &&
                  state.data.hprSession.role < 2 && (
                    <span className="text-destructive">
                      {" "}
                      · {t("abdm_hfr_session_role_warning")}
                    </span>
                  )}
              </span>
            ) : (
              <span>{t("abdm_hfr_session_needed")}</span>
            )}
            <Button
              type="button"
              size="sm"
              variant={sessionActive ? "outline" : "default"}
              className="ml-auto"
              onClick={() => setLoginOpen(true)}
            >
              {sessionActive ? t("abdm_hpr_login_again") : t("abdm_hpr_login")}
            </Button>
          </CardContent>
        </Card>

        <ol className="grid gap-1 text-sm sm:grid-cols-5">
          {STEPS.map((s, i) => {
            const done = onboarding
              ? STEPS.indexOf(s) < STEPS.indexOf(step) ||
                (submitted && s === "submit")
              : false;
            return (
              <li key={s}>
                <button
                  type="button"
                  className={`flex w-full items-center gap-2 rounded-md border px-2 py-1.5 text-left ${step === s ? "border-primary" : ""}`}
                  onClick={() => setStep(s)}
                >
                  {done ? (
                    <CheckCircle2 className="size-4 text-green-600" />
                  ) : (
                    <CircleDashed className="text-muted-foreground size-4" />
                  )}
                  <span>
                    {i + 1}. {stepTitle(s)}
                  </span>
                </button>
              </li>
            );
          })}
        </ol>

        {state.isLoading && <Skeleton className="h-64 w-full rounded-xl" />}
        {state.isError && (
          <Alert variant="destructive">
            <AlertDescription>{t("abdm_hfr_load_failed")}</AlertDescription>
          </Alert>
        )}
        {onboarding?.failure && (
          <Alert variant="destructive">
            <AlertDescription>
              {onboarding.failure.what} {onboarding.failure.nextStep}
            </AlertDescription>
          </Alert>
        )}
        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {state.data && step === "dedup" && (
          <Card>
            <CardHeader>
              <CardTitle>{stepTitle("dedup")}</CardTitle>
              <CardDescription>{t("abdm_hfr_dedup_help")}</CardDescription>
            </CardHeader>
            <CardContent className="grid gap-3 sm:grid-cols-2">
              <Field labelKey="abdm_facility_name" htmlFor="dd-name">
                <Text
                  id="dd-name"
                  value={dedup.name}
                  onChange={(v) => setDedup({ ...dedup, name: v })}
                />
              </Field>
              <Field labelKey="abdm_hfr_address" htmlFor="dd-address">
                <Text
                  id="dd-address"
                  value={dedup.address}
                  onChange={(v) => setDedup({ ...dedup, address: v })}
                />
              </Field>
              <Field labelKey="abdm_hfr_state" htmlFor="dd-state">
                <MasterSelect
                  id="dd-state"
                  kind="lgd-states"
                  value={dedup.state}
                  onChange={(v) =>
                    setDedup({
                      ...dedup,
                      state: v,
                      district: "",
                      subDistrict: "",
                    })
                  }
                />
              </Field>
              <Field labelKey="abdm_hfr_district" htmlFor="dd-district">
                <MasterSelect
                  id="dd-district"
                  kind="lgd-districts"
                  params={{ state: dedup.state }}
                  enabled={Boolean(dedup.state)}
                  value={dedup.district}
                  onChange={(v) =>
                    setDedup({ ...dedup, district: v, subDistrict: "" })
                  }
                />
              </Field>
              <Field labelKey="abdm_hfr_subdistrict" htmlFor="dd-sub">
                <MasterSelect
                  id="dd-sub"
                  kind="lgd-subdistricts"
                  params={{ district: dedup.district }}
                  enabled={Boolean(dedup.district)}
                  value={dedup.subDistrict}
                  onChange={(v) => setDedup({ ...dedup, subDistrict: v })}
                />
              </Field>
              {onboarding && onboarding.dedupResults.length > 0 && (
                <div className="sm:col-span-2">
                  <Alert variant="warning">
                    <AlertDescription className="grid gap-1">
                      <span>
                        {t("abdm_hfr_dedup_matches").replace(
                          "{{count}}",
                          String(onboarding.dedupResults.length),
                        )}
                      </span>
                      <ul className="list-disc pl-4 text-xs">
                        {onboarding.dedupResults.map((r, i) => (
                          <li key={i}>
                            {[r.name, r.address, r.facilityId]
                              .filter(Boolean)
                              .join(" · ")}
                          </li>
                        ))}
                      </ul>
                    </AlertDescription>
                  </Alert>
                </div>
              )}
              {onboarding &&
                onboarding.dedupResults.length === 0 &&
                onboarding.lastMessage === "" &&
                onboarding.status === "draft" && (
                  <p className="text-muted-foreground text-xs sm:col-span-2">
                    {t("abdm_hfr_dedup_none")}
                  </p>
                )}
            </CardContent>
            <CardFooter className="flex gap-2 border-t">
              <Button
                type="button"
                variant="outline"
                size="sm"
                disabled={busy || dedup.name.length < 3}
                onClick={() =>
                  run.mutate({
                    step: "dedup",
                    payload: {
                      name: dedup.name,
                      address: dedup.address,
                      district: dedup.district,
                      subDistrict: dedup.subDistrict,
                    },
                  })
                }
              >
                {busy && <Loader2 className="size-4 animate-spin" />}{" "}
                {t("abdm_hfr_dedup_run")}
              </Button>
              <Button
                type="button"
                size="sm"
                className="ml-auto"
                onClick={() => {
                  setAddress(
                    "stateLGDCode",
                    dedup.state || address.stateLGDCode,
                  );
                  setAddress(
                    "districtLGDCode",
                    dedup.district || address.districtLGDCode,
                  );
                  setStep("basic");
                }}
              >
                {t("abdm_next")}
              </Button>
            </CardFooter>
          </Card>
        )}

        {state.data && step === "basic" && (
          <Card>
            <CardHeader>
              <CardTitle>{stepTitle("basic")}</CardTitle>
              <CardDescription>{t("abdm_hfr_basic_help")}</CardDescription>
            </CardHeader>
            <CardContent className="grid gap-4">
              <div className="grid gap-3 sm:grid-cols-2">
                <Field labelKey="abdm_facility_name" htmlFor="b-name">
                  <Text
                    id="b-name"
                    value={String(basic.facilityName ?? "")}
                    onChange={(v) => setBasicField("facilityName", v)}
                  />
                </Field>
                <Field labelKey="abdm_hfr_ownership" htmlFor="b-own">
                  <MasterSelect
                    id="b-own"
                    kind="facility-master"
                    params={{ type: "OWNER" }}
                    value={String(basic.ownershipCode ?? "")}
                    onChange={(v) => {
                      setBasicField("ownershipCode", v);
                      setBasicField("ownershipSubTypeCode", "");
                      setBasicField("ownershipSubTypeCode2", "");
                    }}
                  />
                </Field>
                <Field labelKey="abdm_hfr_ownership_subtype" htmlFor="b-own2">
                  {/* No master lists these: the registry accepts C (government), P or NP (private, PPP). */}
                  <MasterSelect
                    id="b-own2"
                    kind="owner-subtype-codes"
                    params={{ ownership: String(basic.ownershipCode ?? "") }}
                    enabled={Boolean(basic.ownershipCode)}
                    value={String(basic.ownershipSubTypeCode ?? "")}
                    onChange={(v) => {
                      setBasicField("ownershipSubTypeCode", v);
                      setBasicField("ownershipSubTypeCode2", "");
                    }}
                  />
                </Field>
                <Field
                  labelKey="abdm_hfr_ownership_subtype2"
                  htmlFor="b-own3"
                >
                  <MasterSelect
                    id="b-own3"
                    kind="owner-subtypes"
                    params={{
                      ownership: String(basic.ownershipCode ?? ""),
                      subtype: String(basic.ownershipSubTypeCode ?? ""),
                    }}
                    enabled={Boolean(
                      basic.ownershipCode && basic.ownershipSubTypeCode,
                    )}
                    value={String(basic.ownershipSubTypeCode2 ?? "")}
                    onChange={(v) => setBasicField("ownershipSubTypeCode2", v)}
                  />
                </Field>
                <Field
                  labelKey="abdm_hfr_system_of_medicine"
                  htmlFor="b-som"
                  hint={t("abdm_hfr_multi_hint")}
                >
                  <MasterSelect
                    id="b-som"
                    kind="facility-master"
                    params={{ type: "MEDICINE" }}
                    multiple
                    value={somCodes}
                    onChange={(v) => setBasicField("systemOfMedicineCode", v)}
                  />
                </Field>
                <Field
                  labelKey="abdm_hfr_type_of_service"
                  htmlFor="b-tos"
                  hint={t("abdm_hfr_multi_hint")}
                >
                  <MasterSelect
                    id="b-tos"
                    kind="facility-master"
                    params={{ type: "TYPE-SERVICE" }}
                    multiple
                    value={String(basic.typeOfServiceCode ?? "")
                      .split(",")
                      .filter(Boolean)}
                    onChange={(v) => setBasicField("typeOfServiceCode", v)}
                  />
                </Field>
                <Field labelKey="abdm_hfr_facility_type" htmlFor="b-type">
                  <MasterSelect
                    id="b-type"
                    kind="facility-types"
                    params={{
                      ownership: String(basic.ownershipCode ?? ""),
                      som: somCodes[0] ?? "",
                    }}
                    enabled={Boolean(basic.ownershipCode && somCodes.length)}
                    value={String(basic.facilityTypeCode ?? "")}
                    onChange={(v) => {
                      setBasicField("facilityTypeCode", v);
                      setBasicField("facilitySubType", "");
                    }}
                  />
                </Field>
                <Field labelKey="abdm_hfr_facility_subtype" htmlFor="b-sub">
                  <MasterSelect
                    id="b-sub"
                    kind="facility-subtypes"
                    params={{ type: String(basic.facilityTypeCode ?? "") }}
                    enabled={Boolean(basic.facilityTypeCode)}
                    value={String(basic.facilitySubType ?? "")}
                    onChange={(v) => setBasicField("facilitySubType", v)}
                  />
                </Field>
                <Field labelKey="abdm_hfr_speciality_type" htmlFor="b-spec">
                  <MasterSelect
                    id="b-spec"
                    kind="facility-master"
                    params={{ type: "SPECIALITY-TYPE" }}
                    value={String(basic.specialityTypeCode ?? "")}
                    onChange={(v) => setBasicField("specialityTypeCode", v)}
                  />
                </Field>
                <Field labelKey="abdm_hfr_operational_status" htmlFor="b-ops">
                  <MasterSelect
                    id="b-ops"
                    kind="facility-master"
                    params={{ type: "FAC-STATUS" }}
                    value={String(basic.facilityOperationalStatus ?? "")}
                    onChange={(v) =>
                      setBasicField("facilityOperationalStatus", v)
                    }
                  />
                </Field>
              </div>

              <h3 className="text-sm font-semibold">{t("abdm_hfr_address")}</h3>
              <div className="grid gap-3 sm:grid-cols-2">
                <Field labelKey="abdm_hfr_state" htmlFor="b-state">
                  <MasterSelect
                    id="b-state"
                    kind="lgd-states"
                    value={String(address.stateLGDCode ?? "")}
                    onChange={(v) =>
                      setBasicField("facilityAddressDetails", {
                        ...address,
                        stateLGDCode: v,
                        districtLGDCode: "",
                        subDistrictLGDCode: "",
                      })
                    }
                  />
                </Field>
                <Field labelKey="abdm_hfr_district" htmlFor="b-district">
                  <MasterSelect
                    id="b-district"
                    kind="lgd-districts"
                    params={{ state: String(address.stateLGDCode ?? "") }}
                    enabled={Boolean(address.stateLGDCode)}
                    value={String(address.districtLGDCode ?? "")}
                    onChange={(v) =>
                      setBasicField("facilityAddressDetails", {
                        ...address,
                        districtLGDCode: v,
                        subDistrictLGDCode: "",
                      })
                    }
                  />
                </Field>
                <Field labelKey="abdm_hfr_subdistrict" htmlFor="b-subd">
                  <MasterSelect
                    id="b-subd"
                    kind="lgd-subdistricts"
                    params={{ district: String(address.districtLGDCode ?? "") }}
                    enabled={Boolean(address.districtLGDCode)}
                    value={String(address.subDistrictLGDCode ?? "")}
                    onChange={(v) => setAddress("subDistrictLGDCode", v)}
                  />
                </Field>
                <Field labelKey="abdm_hfr_region" htmlFor="b-region">
                  <MasterSelect
                    id="b-region"
                    kind="facility-master"
                    params={{ type: "FACILITY-REGION" }}
                    value={String(address.facilityRegion ?? "")}
                    onChange={(v) => setAddress("facilityRegion", v)}
                  />
                </Field>
                <Field
                  labelKey="abdm_hfr_village_code"
                  htmlFor="b-village"
                  hint={t("abdm_hfr_village_hint")}
                >
                  <Text
                    id="b-village"
                    value={String(address.villageCityTownLGDCode ?? "")}
                    onChange={(v) => setAddress("villageCityTownLGDCode", v)}
                  />
                </Field>
                <Field labelKey="abdm_hfr_pincode" htmlFor="b-pin">
                  <Text
                    id="b-pin"
                    inputMode="numeric"
                    value={String(address.pincode ?? "")}
                    onChange={(v) => setAddress("pincode", v)}
                  />
                </Field>
                <Field labelKey="abdm_hfr_address_line1" htmlFor="b-a1">
                  <Text
                    id="b-a1"
                    value={String(address.addressLine1 ?? "")}
                    onChange={(v) => setAddress("addressLine1", v)}
                  />
                </Field>
                <Field labelKey="abdm_hfr_address_line2" htmlFor="b-a2">
                  <Text
                    id="b-a2"
                    value={String(address.addressLine2 ?? "")}
                    onChange={(v) => setAddress("addressLine2", v)}
                  />
                </Field>
                <Field labelKey="abdm_hfr_latitude" htmlFor="b-lat">
                  <Text
                    id="b-lat"
                    inputMode="decimal"
                    value={String(address.latitude ?? "")}
                    onChange={(v) => setAddress("latitude", v)}
                  />
                </Field>
                <Field labelKey="abdm_hfr_longitude" htmlFor="b-lon">
                  <Text
                    id="b-lon"
                    inputMode="decimal"
                    value={String(address.longitude ?? "")}
                    onChange={(v) => setAddress("longitude", v)}
                  />
                </Field>
              </div>

              <h3 className="text-sm font-semibold">{t("abdm_hfr_contact")}</h3>
              <div className="grid gap-3 sm:grid-cols-2">
                <Field labelKey="abdm_hfr_email" htmlFor="b-email">
                  <Text
                    id="b-email"
                    type="email"
                    value={String(contact.facilityEmailId ?? "")}
                    onChange={(v) => setContact("facilityEmailId", v)}
                  />
                </Field>
                <Field labelKey="abdm_hfr_mobile" htmlFor="b-mobile">
                  <Text
                    id="b-mobile"
                    inputMode="tel"
                    value={String(contact.facilityContactNumber ?? "")}
                    onChange={(v) => setContact("facilityContactNumber", v)}
                  />
                </Field>
                <Field labelKey="abdm_hfr_website" htmlFor="b-web">
                  <Text
                    id="b-web"
                    inputMode="url"
                    value={String(contact.websiteLink ?? "")}
                    onChange={(v) => setContact("websiteLink", v)}
                  />
                </Field>
                <Field labelKey="abdm_hfr_landline" htmlFor="b-land">
                  <div className="flex gap-2">
                    <Input
                      id="b-std"
                      className="w-24"
                      placeholder="STD"
                      value={String(contact.facilityStdCode ?? "")}
                      onChange={(e) =>
                        setContact("facilityStdCode", e.target.value)
                      }
                    />
                    <Input
                      id="b-land"
                      value={String(contact.facilityLandlineNumber ?? "")}
                      onChange={(e) =>
                        setContact("facilityLandlineNumber", e.target.value)
                      }
                    />
                  </div>
                </Field>
              </div>

              <h3 className="text-sm font-semibold">{t("abdm_hfr_photos")}</h3>
              <div className="grid gap-3 sm:grid-cols-2">
                <Photo
                  id="b-board"
                  labelKey="abdm_hfr_board_photo"
                  value={photos.board}
                  onChange={(v) => setPhotos((p) => ({ ...p, board: v }))}
                  t={t}
                />
                <Photo
                  id="b-building"
                  labelKey="abdm_hfr_building_photo"
                  value={photos.building}
                  onChange={(v) => setPhotos((p) => ({ ...p, building: v }))}
                  t={t}
                />
              </div>

              <h3 className="text-sm font-semibold">{t("abdm_hfr_timings")}</h3>
              <div className="grid gap-2 sm:grid-cols-2">
                {DAYS.map((day) => (
                  <div key={day} className="flex items-center gap-2">
                    <span className="w-12 text-xs font-medium">{day}</span>
                    <Input
                      value={String(
                        timings.find((x) => x.workingDays === day)
                          ?.openingHours ?? "",
                      )}
                      placeholder={t("abdm_hfr_closed")}
                      onChange={(e) => setTiming(day, e.target.value)}
                    />
                  </div>
                ))}
              </div>
            </CardContent>
            <CardFooter className="flex gap-2 border-t">
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => setStep("dedup")}
              >
                {t("abdm_back")}
              </Button>
              <Button
                type="button"
                size="sm"
                className="ml-auto"
                disabled={
                  busy ||
                  !sessionActive ||
                  !basic.facilityName ||
                  !address.stateLGDCode
                }
                onClick={() =>
                  run.mutate({ step: "basic", payload: basicPayload() })
                }
              >
                {busy && <Loader2 className="size-4 animate-spin" />}{" "}
                {onboarding?.trackingId
                  ? t("abdm_hfr_save_and_next")
                  : t("abdm_hfr_create_and_next")}
              </Button>
            </CardFooter>
          </Card>
        )}

        {state.data && step === "additional" && (
          <Card>
            <CardHeader>
              <CardTitle>{stepTitle("additional")}</CardTitle>
              <CardDescription>{t("abdm_hfr_additional_help")}</CardDescription>
            </CardHeader>
            <CardContent className="grid gap-4">
              <h3 className="text-sm font-semibold">
                {t("abdm_hfr_services")}
              </h3>
              <div className="grid gap-3 sm:grid-cols-3">
                {[
                  "hasDialysisCenter",
                  "hasPharmacy",
                  "hasBloodBank",
                  "hasCathLab",
                  "hasDiagnosticLab",
                  "hasImagingCenter",
                ].map((k) => (
                  <Field key={k} labelKey={`abdm_hfr_${k}`} htmlFor={`a-${k}`}>
                    <Select
                      id={`a-${k}`}
                      value={String(general[k] ?? "")}
                      onChange={(v) =>
                        setAdditional((a) => ({
                          ...a,
                          generalInformation: { ...general, [k]: v },
                        }))
                      }
                      options={[
                        { code: "Y", name: t("abdm_yes") },
                        { code: "N", name: t("abdm_no") },
                        { code: "YALL", name: t("abdm_hfr_yes_all") },
                      ]}
                    />
                  </Field>
                ))}
              </div>
              <h3 className="text-sm font-semibold">
                {t("abdm_hfr_programs")}
              </h3>
              <div className="grid gap-3 sm:grid-cols-2">
                {[
                  "nhrrId",
                  "nin",
                  "abpmjayId",
                  "rohiniId",
                  "echsId",
                  "cghsId",
                  "ceaRegistration",
                  "stateInsuranceSchemeId",
                ].map((k) => (
                  <Field key={k} labelKey={`abdm_hfr_${k}`} htmlFor={`a-${k}`}>
                    <Text
                      id={`a-${k}`}
                      value={String(programs[k] ?? "")}
                      onChange={(v) =>
                        setAdditional((a) => ({
                          ...a,
                          linkedProgramIds: { ...programs, [k]: v },
                        }))
                      }
                    />
                  </Field>
                ))}
              </div>
            </CardContent>
            <CardFooter className="flex gap-2 border-t">
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => setStep("basic")}
              >
                {t("abdm_back")}
              </Button>
              <Button
                type="button"
                size="sm"
                className="ml-auto"
                disabled={busy || !sessionActive || !onboarding?.trackingId}
                onClick={() =>
                  run.mutate({
                    step: "additional",
                    payload: {
                      linkedProgramIds: Object.fromEntries(
                        Object.entries(programs).filter(([, v]) => v),
                      ),
                      generalInformation: Object.fromEntries(
                        Object.entries(general).filter(([, v]) => v),
                      ),
                    },
                  })
                }
              >
                {busy && <Loader2 className="size-4 animate-spin" />}{" "}
                {t("abdm_hfr_save_and_next")}
              </Button>
            </CardFooter>
          </Card>
        )}

        {state.data && step === "detailed" && (
          <Card>
            <CardHeader>
              <CardTitle>{stepTitle("detailed")}</CardTitle>
              <CardDescription>{t("abdm_hfr_detailed_help")}</CardDescription>
            </CardHeader>
            <CardContent className="grid gap-4">
              <h3 className="text-sm font-semibold">
                {t("abdm_hfr_specialities")}
              </h3>
              {somCodes.length === 0 && (
                <p className="text-muted-foreground text-xs">
                  {t("abdm_hfr_specialities_need_som")}
                </p>
              )}
              {somCodes.map((som) => {
                const row = specialities.find(
                  (s) => s.systemOfMedicineCode === som,
                ) ?? {
                  systemOfMedicineCode: som,
                  isSpecializationAvalaible: "N",
                  specialities: [],
                };
                const update = (patch: Json) =>
                  setDetailedField("specialities", [
                    ...specialities.filter(
                      (s) => s.systemOfMedicineCode !== som,
                    ),
                    { ...row, ...patch },
                  ]);
                return (
                  <div
                    key={som}
                    className="grid gap-2 rounded-md border p-3 sm:grid-cols-[8rem_1fr]"
                  >
                    <div className="grid gap-1">
                      <span className="text-sm font-medium">{som}</span>
                      <Select
                        id={`d-avail-${som}`}
                        value={String(row.isSpecializationAvalaible ?? "N")}
                        onChange={(v) =>
                          update({ isSpecializationAvalaible: v })
                        }
                        options={YES_NO.map((c) => ({
                          code: c,
                          name: c === "Y" ? t("abdm_yes") : t("abdm_no"),
                        }))}
                      />
                    </div>
                    <MasterSelect
                      kind="specialities"
                      params={{ som }}
                      multiple
                      enabled={row.isSpecializationAvalaible === "Y"}
                      value={(row.specialities as string[]) ?? []}
                      onChange={(v) =>
                        update({ specialities: v.split(",").filter(Boolean) })
                      }
                    />
                  </div>
                );
              })}

              <h3 className="text-sm font-semibold">
                {t("abdm_hfr_infrastructure")}
              </h3>
              <p className="text-muted-foreground text-xs">
                {t("abdm_hfr_infrastructure_help")}
              </p>
              <div className="grid gap-3 sm:grid-cols-3">
                {[
                  "totalNumberOfBeds",
                  "countIPDBedsWithoutOxygen",
                  "countIPDBedsWithOxygen",
                  "countICUBedsWithVentilators",
                  "countICUBedsWithoutVentilators",
                  "countHDUBedsWithVentilators",
                  "countHDUBedsWithoutVentilators",
                  "totalNumberOfVentilators",
                  "countDayCareBedsWithoutOxygen",
                  "countDayCareBedsWithOxygen",
                  "countDentalChairs",
                ].map((k) => (
                  <Field key={k} labelKey={`abdm_hfr_${k}`} htmlFor={`d-${k}`}>
                    <Text
                      id={`d-${k}`}
                      inputMode="numeric"
                      value={infra[k] === undefined ? "" : String(infra[k])}
                      onChange={(v) =>
                        setDetailedField("medicalInfrastructure", {
                          ...infra,
                          [k]: num(v),
                        })
                      }
                    />
                  </Field>
                ))}
              </div>

              {Boolean(general.hasPharmacy) && general.hasPharmacy !== "N" && (
                <>
                  <h3 className="text-sm font-semibold">
                    {t("abdm_hfr_pharmacy")}
                  </h3>
                  <div className="grid gap-3 sm:grid-cols-2">
                    <Field
                      labelKey="abdm_hfr_isJanAushadhiKendra"
                      htmlFor="d-jak"
                    >
                      <Select
                        id="d-jak"
                        value={String(pharmacy.isJanAushadhiKendra ?? "")}
                        onChange={(v) =>
                          setDetailedField("pharmacyDetails", {
                            ...pharmacy,
                            isJanAushadhiKendra: v,
                          })
                        }
                        options={YES_NO.map((c) => ({ code: c, name: c }))}
                      />
                    </Field>
                    {[
                      "janAushadhiKendraId",
                      "drugLicenseNumber",
                      "pharmacyGstinNumber",
                      "pharmacistRegistrationNumber",
                    ].map((k) => (
                      <Field
                        key={k}
                        labelKey={`abdm_hfr_${k}`}
                        htmlFor={`d-${k}`}
                      >
                        <Text
                          id={`d-${k}`}
                          value={String(pharmacy[k] ?? "")}
                          onChange={(v) =>
                            setDetailedField("pharmacyDetails", {
                              ...pharmacy,
                              [k]: v,
                            })
                          }
                        />
                      </Field>
                    ))}
                  </div>
                </>
              )}
              {Boolean(general.hasBloodBank) &&
                general.hasBloodBank !== "N" && (
                  <>
                    <h3 className="text-sm font-semibold">
                      {t("abdm_hfr_blood_bank")}
                    </h3>
                    <div className="grid gap-3 sm:grid-cols-2">
                      {[
                        "isFacilityRegisteredInERaktkosh",
                        "bloodStorageCenters",
                      ].map((k) => (
                        <Field
                          key={k}
                          labelKey={`abdm_hfr_${k}`}
                          htmlFor={`d-${k}`}
                        >
                          <Select
                            id={`d-${k}`}
                            value={String(bloodBank[k] ?? "")}
                            onChange={(v) =>
                              setDetailedField("bloodBankDetails", {
                                ...bloodBank,
                                [k]: v,
                              })
                            }
                            options={YES_NO.map((c) => ({ code: c, name: c }))}
                          />
                        </Field>
                      ))}
                      {[
                        "eRaktoshId",
                        "bloodBankLicenseNumber",
                        "bloodCollectedPerAnnum",
                        "bloodRequiredPerAnnum",
                      ].map((k) => (
                        <Field
                          key={k}
                          labelKey={`abdm_hfr_${k}`}
                          htmlFor={`d-${k}`}
                        >
                          <Text
                            id={`d-${k}`}
                            value={String(bloodBank[k] ?? "")}
                            onChange={(v) =>
                              setDetailedField("bloodBankDetails", {
                                ...bloodBank,
                                [k]: v,
                              })
                            }
                          />
                        </Field>
                      ))}
                      <Field
                        labelKey="abdm_hfr_storageCentersCount"
                        htmlFor="d-scc"
                      >
                        <Text
                          id="d-scc"
                          inputMode="numeric"
                          value={
                            bloodBank.storageCentersCount === undefined
                              ? ""
                              : String(bloodBank.storageCentersCount)
                          }
                          onChange={(v) =>
                            setDetailedField("bloodBankDetails", {
                              ...bloodBank,
                              storageCentersCount: num(v),
                            })
                          }
                        />
                      </Field>
                    </div>
                  </>
                )}
            </CardContent>
            <CardFooter className="flex gap-2 border-t">
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => setStep("additional")}
              >
                {t("abdm_back")}
              </Button>
              <Button
                type="button"
                size="sm"
                className="ml-auto"
                disabled={busy || !sessionActive || !onboarding?.trackingId}
                onClick={() => {
                  const payload: Json = {
                    specialities,
                    medicalInfrastructure: Object.fromEntries(
                      Object.entries(infra).filter(([, v]) => v !== undefined),
                    ),
                  };
                  if (general.hasPharmacy && general.hasPharmacy !== "N")
                    payload.pharmacyDetails = pharmacy;
                  if (general.hasBloodBank && general.hasBloodBank !== "N")
                    payload.bloodBankDetails = bloodBank;
                  run.mutate({ step: "detailed", payload });
                }}
              >
                {busy && <Loader2 className="size-4 animate-spin" />}{" "}
                {t("abdm_hfr_save_and_next")}
              </Button>
            </CardFooter>
          </Card>
        )}

        {state.data && step === "submit" && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                {stepTitle("submit")}
                {onboarding && (
                  <Badge
                    variant={submitted ? "success" : "warning"}
                    size="sm"
                    className="ml-auto"
                  >
                    {t(`abdm_hfr_ob_${onboarding.status}`)}
                  </Badge>
                )}
              </CardTitle>
              <CardDescription>{t("abdm_hfr_submit_help")}</CardDescription>
            </CardHeader>
            <CardContent className="grid gap-3 text-sm">
              <div className="grid gap-1 sm:grid-cols-[10rem_1fr]">
                <span className="text-muted-foreground">
                  {t("abdm_hfr_tracking_id")}
                </span>
                <span className="font-mono">
                  {onboarding?.trackingId || "—"}
                </span>
                <span className="text-muted-foreground">
                  {t("abdm_hfr_facility_id")}
                </span>
                <span className="font-mono">
                  {onboarding?.facilityId ||
                    state.data.config.facility_id ||
                    "—"}
                </span>
                {onboarding?.lastMessage && (
                  <>
                    <span className="text-muted-foreground">
                      {t("abdm_hfr_registry_said")}
                    </span>
                    <span>{onboarding.lastMessage}</span>
                  </>
                )}
              </div>
              {!submitted && (
                <Field
                  labelKey="abdm_hfr_source_of_information"
                  htmlFor="s-src"
                  hint={t("abdm_hfr_source_hint")}
                >
                  <Text
                    id="s-src"
                    value={submitInfo.sourceOfInformation}
                    onChange={(v) => setSubmitInfo({ sourceOfInformation: v })}
                  />
                </Field>
              )}
              {submitted && <p>{t("abdm_hfr_submitted_next")}</p>}
            </CardContent>
            <CardFooter className="flex gap-2 border-t">
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => setStep("detailed")}
              >
                {t("abdm_back")}
              </Button>
              {submitted ? (
                <Button
                  type="button"
                  size="sm"
                  className="ml-auto"
                  onClick={() => navigate(`/facility/${facilityId}/abdm/setup`)}
                >
                  {t("abdm_open_setup")}
                </Button>
              ) : (
                <Button
                  type="button"
                  size="sm"
                  className="ml-auto"
                  disabled={busy || !sessionActive || !onboarding?.trackingId}
                  onClick={() =>
                    run.mutate({
                      step: "submit",
                      payload: submitInfo.sourceOfInformation
                        ? {
                            sourceOfInformation: submitInfo.sourceOfInformation,
                          }
                        : {},
                    })
                  }
                >
                  {busy && <Loader2 className="size-4 animate-spin" />}{" "}
                  {t("abdm_hfr_submit")}
                </Button>
              )}
            </CardFooter>
          </Card>
        )}

        <HprLoginDialog
          open={loginOpen}
          onOpenChange={setLoginOpen}
          pendingLogin={hpr.data?.pendingLogin ?? null}
          onDone={() => qc.invalidateQueries({ queryKey: key })}
        />
      </div>
    </Frame>
  );
}
