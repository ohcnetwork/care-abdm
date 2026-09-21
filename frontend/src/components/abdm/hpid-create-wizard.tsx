import {
  embeddedCard,
  errorMessage,
  hprQueryKey,
} from "@/components/abdm/nhpr-shared";
import MasterSelect from "@/components/abdm/master-select";
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
import { useTranslation } from "@/hooks/use-translation";
import careApi, { type AbdmHprState } from "@/lib/careApi";
import { mutate } from "@/lib/request";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { cn } from "@/lib/utils";
import { ExternalLink, IdCard, Loader2, RefreshCw } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

/**
 * HPID creation (ADR-015, M4 journey 1). The plug never sees the Aadhaar number or its OTP: the
 * person completes them on the NHPR page the link opens. This card polls `isAuthenticated` every
 * 5 s while the link is live (5 minutes), then walks mobile match -> OTP -> username -> create.
 * The mobile number, the OTP and the password are encrypted by the plug with the NHPR certificate.
 */

type Action =
  | "start"
  | "poll"
  | "mobile"
  | "mobile-verify"
  | "suggestions"
  | "finish"
  | "cancel";

export default function HpidCreateWizard({
  state,
  embedded,
  onDone,
}: {
  state: AbdmHprState;
  /** True when a sheet holds this wizard: the sheet header carries the title (ADR-017). */
  embedded?: boolean;
  /** The sheet closes itself when the registry gives the HPR ID (ADR-017). */
  onDone?: () => void;
}) {
  const { t } = useTranslation();
  const qc = useQueryClient();
  const txn = state.transaction;
  const [error, setError] = useState<string>();
  const [mobile, setMobile] = useState("");
  const [otp, setOtp] = useState("");
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [names, setNames] = useState({ first: "", middle: "", last: "" });
  const [category, setCategory] = useState("");
  const [subCategory, setSubCategory] = useState("");
  const [stateCode, setStateCode] = useState("");
  const [districtCode, setDistrictCode] = useState("");
  const [role, setRole] = useState(1);

  const act = useMutation<
    AbdmHprState,
    unknown,
    { action: Action; body?: Record<string, unknown> }
  >({
    mutationFn: ({ action, body }) =>
      mutate(careApi.hpidCreate, { pathParams: { action }, silent: true })(
        body ?? {},
      ),
    onMutate: () => setError(undefined),
    onSuccess: (next) => {
      qc.setQueryData(hprQueryKey, next);
      if (next.profile) onDone?.();
    },
    onError: (e) => {
      const cause = (e as { cause?: AbdmHprState }).cause;
      if (cause && "transaction" in cause)
        qc.setQueryData(hprQueryKey, { ...cause, errors: undefined });
      setError(errorMessage(e, t("abdm_hpid_failed")));
    },
  });
  const busy = act.isPending;

  // Poll while the Aadhaar link is live and the person has not finished it yet.
  const linkLive = Boolean(
    txn &&
    txn.status === "link_created" &&
    txn.linkExpiresAt &&
    new Date(txn.linkExpiresAt).getTime() > Date.now(),
  );
  useEffect(() => {
    if (!linkLive) return;
    const id = window.setInterval(() => {
      if (!act.isPending) act.mutate({ action: "poll" });
    }, 5000);
    return () => window.clearInterval(id);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [linkLive, txn?.id]);

  useEffect(() => {
    if (
      txn?.status === "aadhaar_verified" ||
      txn?.status === "mobile_verified"
    ) {
      const parts = String(txn.details.name ?? "")
        .split(/\s+/)
        .filter(Boolean);
      setNames((n) =>
        n.first || n.last
          ? n
          : {
              first: parts[0] ?? "",
              middle: parts.length > 2 ? parts.slice(1, -1).join(" ") : "",
              last: parts.length > 1 ? parts[parts.length - 1] : "",
            },
      );
    }
  }, [txn?.status, txn?.details.name]);

  const details = useMemo(
    () =>
      Object.entries(txn?.details ?? {}).filter(
        ([k]) => !["txnId", "mobileNumber"].includes(k),
      ),
    [txn?.details],
  );

  if (!txn) {
    return (
      <Card className={cn(embedded && embeddedCard.card)}>
        {!embedded && (
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <IdCard className="text-muted-foreground size-4" />{" "}
              {t("abdm_hpid_create_title")}
            </CardTitle>
            <CardDescription>{t("abdm_hpid_create_intro")}</CardDescription>
          </CardHeader>
        )}
        <CardFooter
          className={cn(
            "border-t",
            embedded && `${embeddedCard.padding} border-t-0`,
          )}
        >
          <Button
            type="button"
            size="sm"
            disabled={busy}
            onClick={() => act.mutate({ action: "start" })}
          >
            {busy && <Loader2 className="size-4 animate-spin" />}{" "}
            {t("abdm_hpid_start")}
          </Button>
          {error && (
            <span className="text-destructive ml-3 text-xs">{error}</span>
          )}
        </CardFooter>
      </Card>
    );
  }

  return (
    <Card className={cn(embedded && embeddedCard.card)}>
      {!embedded && (
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <IdCard className="text-muted-foreground size-4" />{" "}
            {t("abdm_hpid_create_title")}
            <Badge variant="warning" size="sm" className="ml-auto">
              {t(`abdm_hpid_status_${txn.status}`)}
            </Badge>
          </CardTitle>
          <CardDescription>{t("abdm_hpid_create_intro")}</CardDescription>
        </CardHeader>
      )}
      <CardContent
        className={cn("grid gap-4 text-sm", embedded && embeddedCard.padding)}
      >
        {embedded && (
          <div className="flex">
            <Badge variant="warning" size="sm" className="ml-auto">
              {t(`abdm_hpid_status_${txn.status}`)}
            </Badge>
          </div>
        )}
        {txn.status === "link_created" && (
          <div className="grid gap-2">
            <p>{t("abdm_hpid_link_help")}</p>
            {txn.aadhaarUrl ? (
              <a
                href={txn.aadhaarUrl}
                target="_blank"
                rel="noreferrer"
                className="text-primary inline-flex items-center gap-1 underline-offset-2 hover:underline"
              >
                <ExternalLink className="size-4" /> {t("abdm_hpid_open_link")}
              </a>
            ) : (
              <Alert variant="warning">
                <AlertDescription>{t("abdm_hpid_no_url")}</AlertDescription>
              </Alert>
            )}
            <span className="text-muted-foreground text-xs">
              {linkLive ? t("abdm_hpid_polling") : t("abdm_hpid_link_expired")}
            </span>
            <div className="flex gap-2">
              <Button
                type="button"
                variant="outline"
                size="sm"
                disabled={busy}
                onClick={() => act.mutate({ action: "poll" })}
              >
                <RefreshCw className="size-4" /> {t("abdm_hpid_check")}
              </Button>
              {!linkLive && (
                <Button
                  type="button"
                  size="sm"
                  disabled={busy}
                  onClick={() => act.mutate({ action: "start" })}
                >
                  {t("abdm_hpid_new_link")}
                </Button>
              )}
            </div>
          </div>
        )}

        {details.length > 0 && (
          <div className="grid gap-1 rounded-md border p-3 sm:grid-cols-[10rem_1fr]">
            {details.map(([k, v]) => (
              <span key={k} className="contents">
                <span className="text-muted-foreground text-xs">{k}</span>
                <span className="text-xs">{String(v)}</span>
              </span>
            ))}
          </div>
        )}

        {txn.status === "aadhaar_verified" && (
          <div className="grid gap-3">
            <p>{t("abdm_hpid_mobile_help")}</p>
            <div className="grid gap-2 sm:grid-cols-[1fr_auto]">
              <Input
                inputMode="tel"
                placeholder={t("abdm_hpid_mobile")}
                value={mobile}
                onChange={(e) => setMobile(e.target.value)}
              />
              <Button
                type="button"
                size="sm"
                className="h-12 md:h-10"
                disabled={busy || mobile.replace(/\D/g, "").length < 10}
                onClick={() =>
                  act.mutate({ action: "mobile", body: { mobile } })
                }
              >
                {busy && <Loader2 className="size-4 animate-spin" />}{" "}
                {txn.otpSentAt
                  ? t("abdm_hpid_resend_otp")
                  : t("abdm_hpid_check_mobile")}
              </Button>
            </div>
            {txn.otpSentAt && (
              <div className="grid gap-2 sm:grid-cols-[1fr_auto]">
                <Input
                  inputMode="numeric"
                  maxLength={6}
                  placeholder={t("abdm_otp")}
                  value={otp}
                  onChange={(e) => setOtp(e.target.value.replace(/\D/g, ""))}
                />
                <Button
                  type="button"
                  size="sm"
                  className="h-12 md:h-10"
                  disabled={busy || otp.length < 4}
                  onClick={() =>
                    act.mutate({ action: "mobile-verify", body: { otp } })
                  }
                >
                  {t("abdm_verify")}
                </Button>
              </div>
            )}
          </div>
        )}

        {txn.status === "mobile_verified" && (
          <div className="grid gap-3">
            <p>{t("abdm_hpid_finish_help")}</p>
            <NhprField labelKey="abdm_hpid_username" htmlFor="hpid-username">
              <div className="flex gap-2">
                <Input
                  id="hpid-username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="name.surname"
                />
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  className="h-12 shrink-0 md:h-10"
                  disabled={busy}
                  onClick={() => act.mutate({ action: "suggestions" })}
                >
                  {t("abdm_hpid_suggest")}
                </Button>
              </div>
              {txn.suggestions.length > 0 && (
                <div className="flex flex-wrap gap-1">
                  {txn.suggestions.map((s) => (
                    <button
                      key={s}
                      type="button"
                      className="bg-muted rounded px-2 py-0.5 text-xs"
                      onClick={() => setUsername(s)}
                    >
                      {s}@hpr.abdm
                    </button>
                  ))}
                </div>
              )}
            </NhprField>
            <div className="grid gap-3 sm:grid-cols-3">
              <NhprField labelKey="abdm_hpid_first_name" htmlFor="hpid-first">
                <Input
                  id="hpid-first"
                  value={names.first}
                  onChange={(e) =>
                    setNames({ ...names, first: e.target.value })
                  }
                />
              </NhprField>
              <NhprField labelKey="abdm_hpid_middle_name" htmlFor="hpid-middle">
                <Input
                  id="hpid-middle"
                  value={names.middle}
                  onChange={(e) =>
                    setNames({ ...names, middle: e.target.value })
                  }
                />
              </NhprField>
              <NhprField labelKey="abdm_hpid_last_name" htmlFor="hpid-last">
                <Input
                  id="hpid-last"
                  value={names.last}
                  onChange={(e) => setNames({ ...names, last: e.target.value })}
                />
              </NhprField>
            </div>
            <div className="grid gap-3 sm:grid-cols-2">
              <NhprField labelKey="abdm_hfr_email" htmlFor="hpid-email">
                <Input
                  id="hpid-email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </NhprField>
              <NhprField labelKey="abdm_hpid_password" htmlFor="hpid-password">
                <Input
                  id="hpid-password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  autoComplete="new-password"
                />
              </NhprField>
              <NhprField labelKey="abdm_hpid_category" htmlFor="hpid-category">
                <MasterSelect
                  id="hpid-category"
                  kind="hpr-categories"
                  params={{ role: String(role) }}
                  value={category}
                  onChange={(v) => {
                    setCategory(v);
                    setSubCategory("");
                  }}
                />
              </NhprField>
              <NhprField
                labelKey="abdm_hpid_subcategory"
                htmlFor="hpid-subcategory"
              >
                <MasterSelect
                  id="hpid-subcategory"
                  kind="hpr-subcategories"
                  params={{ category, role: String(role) }}
                  enabled={Boolean(category)}
                  value={subCategory}
                  onChange={setSubCategory}
                />
              </NhprField>
              <NhprField labelKey="abdm_hfr_state" htmlFor="hpid-state">
                <MasterSelect
                  id="hpid-state"
                  kind="hpr-states"
                  value={stateCode}
                  onChange={(v) => {
                    setStateCode(v);
                    setDistrictCode("");
                  }}
                />
              </NhprField>
              <NhprField labelKey="abdm_hfr_district" htmlFor="hpid-district">
                <MasterSelect
                  id="hpid-district"
                  kind="hpr-districts"
                  params={{ state: stateCode }}
                  enabled={Boolean(stateCode)}
                  value={districtCode}
                  onChange={setDistrictCode}
                />
              </NhprField>
              <NhprField labelKey="abdm_hpid_role" htmlFor="hpid-role">
                <select
                  id="hpid-role"
                  className="border-input h-12 w-full rounded-md border bg-transparent px-3 text-base md:h-10 md:text-sm"
                  value={role}
                  onChange={(e) => setRole(Number(e.target.value))}
                >
                  {state.roles.map((r) => (
                    <option key={r.code} value={r.code}>
                      {r.name}
                    </option>
                  ))}
                </select>
              </NhprField>
            </div>
          </div>
        )}

        {txn.failure && (
          <Alert variant="destructive">
            <AlertDescription>
              {txn.failure.what} {txn.failure.nextStep}
            </AlertDescription>
          </Alert>
        )}
        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
      </CardContent>
      <CardFooter
        className={cn(
          "flex gap-2 border-t",
          embedded && `${embeddedCard.padding} border-t-0`,
        )}
      >
        <Button
          type="button"
          variant="ghost"
          size="sm"
          disabled={busy}
          onClick={() => act.mutate({ action: "cancel" })}
        >
          {t("abdm_cancel")}
        </Button>
        {txn.status === "mobile_verified" && (
          <Button
            type="button"
            size="sm"
            className="ml-auto"
            disabled={
              busy ||
              !username ||
              !email ||
              !password ||
              !category ||
              !subCategory ||
              !stateCode ||
              !districtCode
            }
            onClick={() =>
              act.mutate({
                action: "finish",
                body: {
                  username,
                  email,
                  password,
                  first_name: names.first,
                  middle_name: names.middle,
                  last_name: names.last,
                  category_code: category,
                  sub_category_code: subCategory,
                  state_code: stateCode,
                  district_code: districtCode,
                  role,
                },
              })
            }
          >
            {busy && <Loader2 className="size-4 animate-spin" />}{" "}
            {t("abdm_hpid_create")}
          </Button>
        )}
      </CardFooter>
    </Card>
  );
}
