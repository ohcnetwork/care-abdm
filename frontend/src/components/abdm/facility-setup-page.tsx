import { type FieldHelpContent } from "@/components/abdm/field-help";
import RegistryCard from "@/components/abdm/registry-card";
import DevFooter from "@/components/abdm/dev/dev-footer";
import PluginComponent from "@/components/common/plugin-component";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Skeleton } from "@/components/ui/skeleton";
import { useTranslation } from "@/hooks/use-translation";
import careApi, {
  type AbdmBridgeState,
  type AbdmFacilityConfig,
  type AbdmFacilityConfigUpdate,
  type FacilityBridgeActionResponse,
} from "@/lib/careApi";
import { mutate, query } from "@/lib/request";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { QrCode, X } from "lucide-react";
import { QRCodeSVG } from "qrcode.react";
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
  facility_id: "",
  facility_name: "",
  hip_name: "",
  counters: [],
};

const HIP_NAME_RE = /^[A-Za-z0-9 ]{1,15}$/;
// The 2 typed fields (ADR-016). The HFR id and name come from a registry link.
const editableConfigKeys = ["hip_name", "counters"] as const;

/**
 * The docs say only that the counter QR code holds a URL with the HIP ID and a
 * context (docs/findings.md). The deployment gives the format through
 * ABDM_SHARE_QR_URL_TEMPLATE; the page fills {hip_id} and {context}.
 */
function shareQrUrl(
  template: string | undefined,
  hipId: string,
  context: string,
): string | undefined {
  if (!template || !hipId || !context) return undefined;
  return template
    .replace("{hip_id}", encodeURIComponent(hipId))
    .replace("{context}", encodeURIComponent(context));
}

function editablePayload(config: AbdmFacilityConfig): AbdmFacilityConfigUpdate {
  return { hip_name: config.hip_name, counters: config.counters };
}

function errorMessage(error: unknown, fallback: string) {
  if (error && typeof error === "object" && "cause" in error) {
    const cause = (error as { cause?: Record<string, unknown> }).cause;
    const value = cause?.errors ?? cause?.message;
    if (typeof value === "string") return value;
  }
  return fallback;
}

function labelHelp(
  field: string,
  t: (key: string) => string,
): FieldHelpContent {
  return {
    title: t(`abdm_facility_help_${field}_title`),
    what: t(`abdm_facility_help_${field}_what`),
    how: t(`abdm_facility_help_${field}_how`),
    example: t(`abdm_facility_help_${field}_example`),
  };
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

  const save = useMutation<
    AbdmFacilityConfig,
    unknown,
    AbdmFacilityConfigUpdate
  >({
    mutationFn: mutate(careApi.updateFacilityAbdm, {
      pathParams: { facilityId },
      silent: true,
    }),
    onMutate: () => setActionError(undefined),
    onSuccess: applyResult,
    onError: (error) =>
      setActionError(errorMessage(error, t("abdm_facility_save_failed"))),
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

  const bridge = useQuery<AbdmBridgeState>({
    queryKey: ["abdm", "bridge"],
    queryFn: query(careApi.bridge, { silent: true }),
    retry: false,
  });

  const saved = settings.data;
  const dirty = useMemo(() => {
    if (!saved) return false;
    return editableConfigKeys.some(
      (key) =>
        JSON.stringify(config[key] ?? "") !== JSON.stringify(saved[key] ?? ""),
    );
  }, [config, saved]);
  const formInvalid =
    Boolean(config.hip_name) && !HIP_NAME_RE.test(config.hip_name);

  const busy = save.isPending || hrp.isPending;
  const [newCounter, setNewCounter] = useState("");
  const counterValid = /^[A-Za-z0-9]{1,20}$/.test(newCounter);
  const counterDuplicate = config.counters.some(
    (c) => c.toLowerCase() === newCounter.toLowerCase(),
  );
  const addCounter = () => {
    if (!counterValid || counterDuplicate) return;
    update({ counters: [...config.counters, newCounter] });
    setNewCounter("");
  };
  // The QR carries the HIP ID the gateway routes on: the service id it issued, once known.
  const qrHipId = config.hip_id || config.facility_id;
  const qrTemplate = settings.data?.share_qr_url_template;
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

        {/* The facility ID comes from the facility's HFR record (registered by hand on the NHPR
            portal, docs update 2026-09-15); record sharing (M2) needs it and a registered HIP service.
            Sources:
            https://abdm-docs.dev.eka.care/docs/hiecm/v3/milestones/m2/index.md
            https://abdm-docs.dev.eka.care/docs/hiecm/v3/milestones/m4/index.md */}
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
              <AlertDescription className="grid gap-1">
                <span className="font-medium">{t("abdm_last_error")}</span>
                <span>{config.last_error}</span>
              </AlertDescription>
            </Alert>
          )}

          {settings.isLoading ? (
            <div className="grid gap-4">
              <Skeleton className="h-56 w-full rounded-xl" />
              <Skeleton className="h-56 w-full rounded-xl" />
            </div>
          ) : (
            <>
              {/* ADR-016: 1 card for the registry link, the HIP name and the services registration. */}
              <RegistryCard
                facilityId={facilityId}
                config={config}
                hipNameHelp={labelHelp("hip_name", t)}
                dirty={dirty}
                busy={busy}
                bridge={bridge.data}
                onChange={update}
                onLinked={applyResult}
                onRegisterServices={() => hrp.mutate({})}
              />

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <QrCode className="text-muted-foreground size-4" />
                    {t("abdm_section_scan_share")}
                  </CardTitle>
                  <CardDescription>
                    {t("abdm_section_scan_share_help")}
                  </CardDescription>
                </CardHeader>
                <CardContent className="grid gap-4">
                  <div className="grid gap-1.5">
                    <Label htmlFor="abdm-new-counter">
                      {t("abdm_counter_code")}
                    </Label>
                    <div className="flex gap-2">
                      <Input
                        id="abdm-new-counter"
                        value={newCounter}
                        maxLength={20}
                        placeholder="OPD1"
                        onChange={(e) => setNewCounter(e.target.value.trim())}
                        onKeyDown={(e) => {
                          if (e.key === "Enter") {
                            e.preventDefault();
                            addCounter();
                          }
                        }}
                      />
                      <Button
                        type="button"
                        variant="outline"
                        size="sm"
                        disabled={!counterValid || counterDuplicate}
                        onClick={addCounter}
                      >
                        {t("abdm_add_counter")}
                      </Button>
                    </div>
                    <p className="text-muted-foreground text-xs">
                      {t("abdm_counter_code_help")}
                    </p>
                  </div>
                  {!qrTemplate && (
                    <Alert variant="warning">
                      <AlertDescription>
                        {t("abdm_share_qr_template_missing")}
                      </AlertDescription>
                    </Alert>
                  )}
                  {config.counters.length === 0 ? (
                    <p className="text-muted-foreground text-sm">
                      {t("abdm_no_counters")}
                    </p>
                  ) : (
                    <ul className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                      {config.counters.map((code) => {
                        const url = shareQrUrl(qrTemplate, qrHipId, code);
                        return (
                          <li
                            key={code}
                            className="flex flex-col items-center gap-2 rounded-lg border p-3"
                          >
                            <div className="flex w-full items-center justify-between">
                              <span className="font-mono text-sm font-medium">
                                {code}
                              </span>
                              <Button
                                type="button"
                                variant="ghost"
                                size="icon"
                                aria-label={t("abdm_remove_counter")}
                                onClick={() =>
                                  update({
                                    counters: config.counters.filter(
                                      (c) => c !== code,
                                    ),
                                  })
                                }
                              >
                                <X className="size-4" />
                              </Button>
                            </div>
                            {url ? (
                              <>
                                <QRCodeSVG
                                  value={url}
                                  size={160}
                                  marginSize={1}
                                  className="rounded bg-white p-1"
                                />
                                <span className="text-muted-foreground w-full truncate text-center font-mono text-[10px]">
                                  {url}
                                </span>
                              </>
                            ) : (
                              <span className="text-muted-foreground text-xs">
                                {qrHipId
                                  ? t("abdm_qr_unavailable")
                                  : t("abdm_qr_needs_hip_id")}
                              </span>
                            )}
                          </li>
                        );
                      })}
                    </ul>
                  )}
                </CardContent>
              </Card>
            </>
          )}
        </div>

        <DevFooter filters={{ facility: facilityId }} />

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
              disabled={!dirty || busy || formInvalid}
              onClick={() => save.mutate(editablePayload(config))}
            >
              {t("abdm_save")}
            </Button>
          </div>
        </div>
      </div>
    </PluginComponent>
  );
}
