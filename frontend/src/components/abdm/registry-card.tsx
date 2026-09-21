import FieldHelp, { type FieldHelpContent } from "@/components/abdm/field-help";
import MasterSelect from "@/components/abdm/master-select";
import FailureNotice from "@/components/abdm/failure-notice";
import {
  type FailureNoticeProps,
  noticeFromError,
} from "@/components/abdm/failure-notice-shared";
import { errorMessage, statusTone } from "@/components/abdm/nhpr-shared";
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
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useTranslation } from "@/hooks/use-translation";
import careApi, {
  type AbdmBridgeState,
  type AbdmFacilityConfig,
  type AbdmHfrFacility,
  type AbdmHfrSearchResult,
  type AbdmHfrState,
} from "@/lib/careApi";
import { mutate, query } from "@/lib/request";
import { cn } from "@/lib/utils";
import { useMutation, useQuery } from "@tanstack/react-query";
import {
  Building2,
  CheckCircle2,
  CircleDashed,
  Link2,
  Loader2,
  Search,
} from "lucide-react";
import { navigate } from "raviger";
import type { ReactNode } from "react";
import { useState } from "react";

/**
 * Setup page card "Health Facility Registry" (ADR-016). 1 card, 2 states.
 *
 * Not linked: find the registry record by ID or by name and state and link it, or start the HFR
 * registration wizard. Nobody types the HFR ID or the registered name into CARE: the registry is
 * the source, and the record is stored as it came (the 2026-09-14 name-mismatch refusal).
 *
 * Linked: the record read-only, the HIP name (the 1 typed field, what patients see), and the
 * services block: register the facility as HIP and HIU on the bridge, the issued HIP ID, the
 * bridge status. Layout is append-only: results grow below the fields.
 */

const HIP_NAME_RE = /^[A-Za-z0-9 ]{1,15}$/;

/** 1 registry record as a compact block: name, ID, status, type line, address line. */
export function RegistryRecord({
  record,
  action,
  className,
}: {
  record: Partial<AbdmHfrFacility>;
  action?: ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("grid gap-2 rounded-md border p-3 text-sm", className)}>
      <div className="flex flex-wrap items-center gap-2">
        <span className="font-medium">{record.facilityName}</span>
        <span className="text-muted-foreground font-mono text-xs">
          {record.facilityId}
        </span>
        {record.facilityStatus && (
          <Badge variant={statusTone(record.facilityStatus)} size="sm">
            {record.facilityStatus}
          </Badge>
        )}
      </div>
      {[record.facilityType, record.ownership, record.systemOfMedicine].some(
        Boolean,
      ) && (
        <span className="text-muted-foreground text-xs">
          {[record.facilityType, record.ownership, record.systemOfMedicine]
            .filter(Boolean)
            .join(" · ")}
        </span>
      )}
      {[record.address, record.districtName, record.stateName].some(
        Boolean,
      ) && (
        <span className="text-muted-foreground text-xs">
          {[
            record.address,
            record.districtName,
            record.stateName,
            record.pincode,
          ]
            .filter(Boolean)
            .join(", ")}
        </span>
      )}
      {action && <div>{action}</div>}
    </div>
  );
}

/** The 3 values a registry name search needs (m4-search/02; the registry refuses one without the
 * state and the ownership, HIS-1070, observed 2026-09-21). */
export type RegistrySearchArgs = {
  name: string;
  state: string;
  ownership: string;
};

/**
 * The registry finder: lookup by ID, or search by name, state and ownership. Shared by the setup
 * card and the "Add a facility" wizard; the caller decides what "pick" does. Layout is append-only:
 * results grow below the fields.
 */
export function RegistryFinder({
  lookup,
  search,
  onPick,
  pickLabel,
  currentId,
  busy,
  idPrefix = "abdm-hfr",
}: {
  lookup: (id: string) => Promise<AbdmHfrFacility>;
  search: (args: RegistrySearchArgs) => Promise<AbdmHfrSearchResult>;
  onPick: (record: AbdmHfrFacility) => void;
  pickLabel: string;
  currentId?: string;
  busy?: boolean;
  idPrefix?: string;
}) {
  const { t } = useTranslation();
  const [lookupId, setLookupId] = useState("");
  const [name, setName] = useState("");
  const [state, setState] = useState("");
  const [ownership, setOwnership] = useState("");
  const [searched, setSearched] = useState<RegistrySearchArgs | null>(null);
  const [error, setError] = useState<FailureNoticeProps>();
  const [lookedUp, setLookedUp] = useState<AbdmHfrFacility | null>(null);

  const lookupRun = useMutation<AbdmHfrFacility, unknown, string>({
    mutationFn: (id) => lookup(id.trim().toUpperCase()),
    onMutate: () => {
      setError(undefined);
      setLookedUp(null);
    },
    onSuccess: setLookedUp,
    onError: (e) => setError(noticeFromError(e, t("abdm_hfr_not_found"))),
  });
  const searchRun = useQuery<AbdmHfrSearchResult>({
    queryKey: [idPrefix, "hfr-search", searched],
    queryFn: () => search(searched as RegistrySearchArgs),
    enabled: Boolean(searched && searched.name.length >= 3),
    retry: false,
  });
  const pending = Boolean(busy) || lookupRun.isPending;
  const canSearch =
    name.trim().length >= 3 && Boolean(state) && Boolean(ownership);
  const runSearch = () => {
    if (!canSearch) return;
    setSearched({ name: name.trim(), state, ownership });
  };

  return (
    <div className="grid gap-5">
      <div className="grid gap-1.5">
        <Label htmlFor={`${idPrefix}-lookup`}>
          {t("abdm_hfr_lookup_label")}
        </Label>
        <div className="flex gap-2">
          <Input
            id={`${idPrefix}-lookup`}
            className="font-mono uppercase"
            placeholder="IN1410000232"
            value={lookupId}
            onChange={(e) => setLookupId(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && lookupId.trim().length === 12) {
                e.preventDefault();
                lookupRun.mutate(lookupId);
              }
            }}
            maxLength={12}
          />
          <Button
            type="button"
            variant="outline"
            size="sm"
            className="h-12 shrink-0 md:h-10"
            disabled={pending || lookupId.trim().length !== 12}
            onClick={() => lookupRun.mutate(lookupId)}
          >
            {lookupRun.isPending ? (
              <Loader2 className="size-4 animate-spin" />
            ) : (
              <Search className="size-4" />
            )}
            {t("abdm_hfr_lookup")}
          </Button>
        </div>
        <p className="text-muted-foreground text-xs">
          {t("abdm_hfr_lookup_help")}
        </p>
      </div>

      {lookedUp && (
        <RegistryRecord
          record={lookedUp}
          action={
            <Button
              type="button"
              size="sm"
              disabled={pending || currentId === lookedUp.facilityId}
              onClick={() => onPick(lookedUp)}
            >
              <Link2 className="size-4" />
              {currentId === lookedUp.facilityId
                ? t("abdm_hfr_linked_badge")
                : pickLabel}
            </Button>
          }
        />
      )}

      <div className="grid gap-1.5">
        <span className="text-sm font-medium">
          {t("abdm_hfr_search_label")}
        </span>
        <div className="grid gap-2 sm:grid-cols-2">
          <div className="grid gap-1">
            <Label htmlFor={`${idPrefix}-search-name`} className="text-xs">
              {t("abdm_facility_name")}
            </Label>
            <Input
              id={`${idPrefix}-search-name`}
              placeholder={t("abdm_hfr_search_name")}
              value={name}
              onChange={(e) => setName(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  e.preventDefault();
                  runSearch();
                }
              }}
            />
          </div>
          <div className="grid gap-1">
            <Label htmlFor={`${idPrefix}-search-state`} className="text-xs">
              {t("abdm_hfr_state")}
            </Label>
            <MasterSelect
              id={`${idPrefix}-search-state`}
              kind="lgd-states"
              value={state}
              onChange={setState}
              placeholder={t("abdm_hfr_pick_state")}
            />
          </div>
          <div className="grid gap-1">
            <Label htmlFor={`${idPrefix}-search-ownership`} className="text-xs">
              {t("abdm_hfr_ownership")}
            </Label>
            <MasterSelect
              id={`${idPrefix}-search-ownership`}
              kind="facility-master"
              params={{ type: "OWNER" }}
              value={ownership}
              onChange={setOwnership}
              placeholder={t("abdm_hfr_pick_ownership")}
            />
          </div>
          <div className="flex items-end">
            <Button
              type="button"
              variant="outline"
              size="sm"
              className="h-12 w-full md:h-10"
              disabled={pending || !canSearch}
              onClick={runSearch}
            >
              <Search className="size-4" /> {t("abdm_hfr_search")}
            </Button>
          </div>
        </div>
        <p className="text-muted-foreground text-xs">
          {t("abdm_hfr_search_help")}
        </p>
      </div>
      {searched && (
        <div className="grid gap-2">
          {searchRun.isFetching && (
            <span className="text-muted-foreground flex items-center gap-2 text-xs">
              <Loader2 className="size-3 animate-spin" />{" "}
              {t("abdm_hfr_searching")}
            </span>
          )}
          {searchRun.isError && (
            <span className="text-destructive text-xs">
              {errorMessage(searchRun.error, t("abdm_hfr_search_failed"))}
            </span>
          )}
          {searchRun.data && searchRun.data.facilities.length === 0 && (
            <span className="text-muted-foreground text-xs">
              {t("abdm_hfr_search_none")}
            </span>
          )}
          {searchRun.data && searchRun.data.facilities.length > 0 && (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>{t("abdm_facility_name")}</TableHead>
                  <TableHead>{t("abdm_hfr_facility_id")}</TableHead>
                  <TableHead>{t("abdm_hfr_status")}</TableHead>
                  <TableHead />
                </TableRow>
              </TableHeader>
              <TableBody>
                {searchRun.data.facilities.map((f) => (
                  <TableRow key={f.facilityId || f.facilityName}>
                    <TableCell>
                      <div className="grid gap-0.5">
                        <span>{f.facilityName}</span>
                        <span className="text-muted-foreground text-xs">
                          {[f.facilityType, f.districtName, f.stateName]
                            .filter(Boolean)
                            .join(", ")}
                        </span>
                      </div>
                    </TableCell>
                    <TableCell className="font-mono text-xs">
                      {f.facilityId || "—"}
                    </TableCell>
                    <TableCell>
                      <Badge variant={statusTone(f.facilityStatus)} size="sm">
                        {f.facilityStatus || "—"}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-right">
                      <Button
                        type="button"
                        size="sm"
                        variant="outline"
                        disabled={
                          pending || !f.facilityId || currentId === f.facilityId
                        }
                        onClick={() => onPick(f)}
                      >
                        <Link2 className="size-4" /> {pickLabel}
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
          {searchRun.data &&
            searchRun.data.total > searchRun.data.facilities.length && (
              <span className="text-muted-foreground text-xs">
                {t("abdm_hfr_search_more", {
                  total: String(searchRun.data.total),
                })}
              </span>
            )}
        </div>
      )}
      {error && <FailureNotice {...error} />}
    </div>
  );
}

function StatusLine({
  done,
  label,
  value,
}: {
  done: boolean;
  label: string;
  value: string;
}) {
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
      {label}: {value}
    </span>
  );
}

export default function RegistryCard({
  facilityId,
  config,
  hipNameHelp,
  dirty,
  busy,
  bridge,
  onChange,
  onLinked,
  onRegisterServices,
}: {
  facilityId: string;
  config: AbdmFacilityConfig;
  hipNameHelp: FieldHelpContent;
  /** The page holds unsaved edits; services registration waits for a save. */
  dirty: boolean;
  busy: boolean;
  bridge?: AbdmBridgeState;
  onChange: (next: Partial<AbdmFacilityConfig>) => void;
  onLinked: (config: AbdmFacilityConfig) => void;
  onRegisterServices: () => void;
}) {
  const { t } = useTranslation();
  const [error, setError] = useState<FailureNoticeProps>();
  const [changing, setChanging] = useState(false);
  const [otpTxn, setOtpTxn] = useState("");
  const [otp, setOtp] = useState("");
  const [otpSource, setOtpSource] = useState("");
  const [otpMessage, setOtpMessage] = useState("");

  const state = useQuery<AbdmHfrState>({
    queryKey: ["abdm", "facility", facilityId, "hfr"],
    queryFn: query(careApi.hfrOnboarding, {
      pathParams: { facilityId },
      silent: true,
    }),
    retry: false,
  });
  const link = useMutation<
    { config: AbdmFacilityConfig; registry: AbdmHfrFacility },
    unknown,
    string
  >({
    mutationFn: (id) =>
      mutate(careApi.hfrLink, { pathParams: { facilityId }, silent: true })({
        facility_id: id,
      }),
    onMutate: () => setError(undefined),
    onSuccess: (data) => {
      onLinked(data.config);
      setChanging(false);
    },
    onError: (e) => setError(noticeFromError(e, t("abdm_hfr_link_failed"))),
  });
  const otpAction = useMutation<
    { transactionId?: string; message: string; status: string },
    unknown,
    "send" | "validate"
  >({
    mutationFn: (action) =>
      mutate(careApi.hfrOtp, { pathParams: { facilityId }, silent: true })({
        action,
        facility_id: config.facility_id,
        transaction_id: otpTxn,
        otp,
        source: otpSource,
        source_id: otpSource,
      }),
    onMutate: () => setError(undefined),
    onSuccess: (data, action) => {
      if (action === "send") setOtpTxn(data.transactionId ?? "");
      setOtpMessage(data.message);
    },
    onError: (e) => setError(noticeFromError(e, t("abdm_hfr_otp_failed"))),
  });

  const pending = busy || link.isPending || otpAction.isPending;
  const onboarding = state.data?.onboarding;
  const onboardingOpen =
    onboarding &&
    onboarding.status !== "submitted" &&
    onboarding.status !== "failed";
  const linked = Boolean(config.facility_id);
  const hipNameInvalid =
    Boolean(config.hip_name) && !HIP_NAME_RE.test(config.hip_name);
  const bridgeOk = Boolean(
    bridge?.bridge?.url && bridge.bridge.url === bridge.callback_url,
  );

  const finder = (
    <RegistryFinder
      idPrefix={`abdm-hfr-${facilityId}`}
      currentId={config.facility_id}
      busy={pending}
      pickLabel={t("abdm_hfr_link")}
      lookup={(id) =>
        query(careApi.hfrLookup, {
          pathParams: { facilityId },
          queryParams: { facility_id: id },
          silent: true,
        })({ signal: new AbortController().signal })
      }
      search={({ name, state: stateCode, ownership }) =>
        query(careApi.hfrSearch, {
          pathParams: { facilityId },
          queryParams: { name, state: stateCode, ownership },
          silent: true,
        })({ signal: new AbortController().signal })
      }
      onPick={(record) => link.mutate(record.facilityId)}
    />
  );

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Building2 className="text-muted-foreground size-4" />
          {t("abdm_hfr_title")}
          <Badge
            variant={linked ? "success" : "neutral"}
            size="sm"
            className="ml-auto"
          >
            {linked
              ? t("abdm_hfr_linked_badge")
              : t("abdm_hfr_not_linked_badge")}
          </Badge>
        </CardTitle>
        <CardDescription>
          {linked ? t("abdm_hfr_linked_intro") : t("abdm_hfr_intro")}
        </CardDescription>
      </CardHeader>
      <CardContent className="grid gap-5">
        {!linked && finder}

        {linked && (
          <>
            <RegistryRecord
              record={{
                ...(config.hfr ?? {}),
                facilityId: config.facility_id,
                facilityName: config.facility_name,
              }}
              action={
                <div className="flex flex-wrap items-center gap-3">
                  {config.hfr?.linked_at && (
                    <span className="text-muted-foreground text-xs">
                      {t("abdm_hfr_linked_on", {
                        date: new Date(config.hfr.linked_at).toLocaleString(),
                        user: config.hfr.linked_by || "—",
                      })}
                    </span>
                  )}
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    className="ml-auto"
                    disabled={pending}
                    onClick={() => setChanging((c) => !c)}
                  >
                    {changing ? t("abdm_close") : t("abdm_hfr_change_link")}
                  </Button>
                </div>
              }
            />
            {changing && (
              <div className="grid gap-3 rounded-md border border-dashed p-3">
                <p className="text-muted-foreground text-xs">
                  {t("abdm_hfr_change_link_help")}
                </p>
                {finder}
              </div>
            )}

            <div className="grid gap-4 md:grid-cols-2">
              <div className="grid gap-1.5">
                <div className="flex min-h-5 items-center gap-1.5">
                  <Label htmlFor="abdm-hip_name">{t("abdm_hip_name")}</Label>
                  <FieldHelp {...hipNameHelp} />
                  <span className="text-muted-foreground ml-auto w-12 text-right font-mono text-xs tabular-nums">
                    {config.hip_name.length}/15
                  </span>
                </div>
                <Input
                  id="abdm-hip_name"
                  value={config.hip_name}
                  autoComplete="off"
                  spellCheck={false}
                  maxLength={15}
                  onChange={(e) => onChange({ hip_name: e.target.value })}
                />
                <p className="text-muted-foreground min-h-4 text-xs">
                  {t("abdm_hip_name_help")}
                </p>
                <p className="text-destructive min-h-4 text-xs">
                  {hipNameInvalid ? t("abdm_hip_name_invalid") : "\u00A0"}
                </p>
              </div>
              <div className="grid gap-1.5">
                <Label>{t("abdm_hip_id_issued")}</Label>
                {config.hip_id ? (
                  <p className="font-mono text-sm">{config.hip_id}</p>
                ) : (
                  <p className="text-muted-foreground text-sm">
                    {t("abdm_hip_id_pending")}
                  </p>
                )}
                <p className="text-muted-foreground text-xs">
                  {t("abdm_hip_id_help")}
                </p>
              </div>
            </div>

            <details className="rounded-md border p-3 text-sm">
              <summary className="cursor-pointer font-medium">
                {t("abdm_hfr_otp_title")}
              </summary>
              <div className="grid gap-2 pt-3">
                <p className="text-muted-foreground text-xs">
                  {t("abdm_hfr_otp_help")}
                </p>
                <div className="grid gap-2 sm:grid-cols-[1fr_auto]">
                  <Input
                    placeholder={t("abdm_hfr_otp_source")}
                    value={otpSource}
                    onChange={(e) => setOtpSource(e.target.value)}
                  />
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    className="h-12 md:h-10"
                    disabled={pending || !otpSource}
                    onClick={() => otpAction.mutate("send")}
                  >
                    {t("abdm_send_otp")}
                  </Button>
                </div>
                {otpTxn && (
                  <div className="grid gap-2 sm:grid-cols-[1fr_auto]">
                    <Input
                      inputMode="numeric"
                      placeholder={t("abdm_otp")}
                      value={otp}
                      onChange={(e) =>
                        setOtp(e.target.value.replace(/\D/g, ""))
                      }
                    />
                    <Button
                      type="button"
                      size="sm"
                      className="h-12 md:h-10"
                      disabled={pending || otp.length < 4}
                      onClick={() => otpAction.mutate("validate")}
                    >
                      {t("abdm_verify")}
                    </Button>
                  </div>
                )}
                {otpMessage && <span className="text-xs">{otpMessage}</span>}
              </div>
            </details>
          </>
        )}

        {error && <FailureNotice {...error} />}
      </CardContent>
      <CardFooter className="flex flex-wrap items-center gap-3 border-t">
        {linked ? (
          <>
            <div className="grid gap-1">
              <StatusLine
                done={Boolean(config.hrp_registered_at)}
                label={t("abdm_hrp_registered_at")}
                value={
                  config.hrp_registered_at
                    ? new Date(config.hrp_registered_at).toLocaleString()
                    : t("abdm_not_recorded")
                }
              />
              <span className="text-muted-foreground inline-flex items-center gap-1.5 text-xs">
                {bridgeOk
                  ? t("abdm_bridge_registered")
                  : t("abdm_bridge_not_registered")}
                <a
                  href="/admin/abdm"
                  className="text-primary underline-offset-4 hover:underline"
                >
                  {t("abdm_bridge_admin_link")}
                </a>
              </span>
            </div>
            <div className="ml-auto flex items-center gap-2">
              {dirty && (
                <span className="text-muted-foreground text-xs">
                  {t("abdm_save_before_register")}
                </span>
              )}
              <Button
                type="button"
                variant={config.hrp_registered_at ? "outline" : "default"}
                size="sm"
                disabled={
                  pending || dirty || hipNameInvalid || !config.hip_name
                }
                onClick={onRegisterServices}
              >
                {t("abdm_register_hrp_service")}
              </Button>
            </div>
          </>
        ) : (
          <>
            <div className="grid gap-0.5 text-xs">
              <span className="text-muted-foreground">
                {t("abdm_hfr_register_hint")}
              </span>
              {onboarding && (
                <span>
                  {t("abdm_hfr_onboarding_status")}:{" "}
                  {t(`abdm_hfr_ob_${onboarding.status}`)}
                  {onboarding.trackingId &&
                    ` · ${t("abdm_hfr_tracking_id")} ${onboarding.trackingId}`}
                </span>
              )}
            </div>
            <Button
              type="button"
              className="ml-auto"
              size="sm"
              variant={onboardingOpen ? "default" : "outline"}
              onClick={() =>
                navigate(`/facility/${facilityId}/abdm/hfr/register`)
              }
            >
              <Building2 className="size-4" />
              {onboardingOpen
                ? t("abdm_hfr_continue_onboarding")
                : t("abdm_hfr_register")}
            </Button>
          </>
        )}
      </CardFooter>
    </Card>
  );
}
