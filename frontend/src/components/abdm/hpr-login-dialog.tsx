import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import NhprField from "@/components/abdm/nhpr-field";
import { Input } from "@/components/ui/input";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { errorMessage, hprQueryKey } from "@/components/abdm/nhpr-shared";
import { useTranslation } from "@/hooks/use-translation";
import careApi, {
  type AbdmHprPublicRecord,
  type AbdmHprState,
} from "@/lib/careApi";
import { HttpError, mutate, query } from "@/lib/request";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Loader2, ShieldCheck } from "lucide-react";
import { useEffect, useState } from "react";

/**
 * HPR login (ADR-015). The person types their HPR ID; the plug shows the public record behind it
 * (`searchByHprId`) so a typo is caught before the password goes out. Two methods have a published
 * verify step: password, and Aadhaar OTP (`auth/init` -> `confirmWithAadhaarOtp`). The token stays
 * on the server; the dialog only learns that the session is active.
 */

export default function HprLoginDialog({
  open,
  onOpenChange,
  pendingLogin,
  onDone,
}: {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  pendingLogin: AbdmHprState["pendingLogin"];
  onDone?: (state: AbdmHprState) => void;
}) {
  const { t } = useTranslation();
  const qc = useQueryClient();
  const [hprId, setHprId] = useState("");
  const [method, setMethod] = useState<"password" | "aadhaar_otp">("password");
  const [password, setPassword] = useState("");
  const [otp, setOtp] = useState("");
  const [error, setError] = useState<string>();

  useEffect(() => {
    if (!open) return;
    setPassword("");
    setOtp("");
    setError(undefined);
  }, [open]);

  const trimmed = hprId.trim();
  // 1 registry call per complete id (registries/nhpr/hpr: the 14-digit number or `name@hpr.abdm`),
  // not 1 per keystroke: the sandbox answers HTTP 422 "Invalid HPID" to every partial value.
  const complete =
    /^\d{2}-?\d{4}-?\d{4}-?\d{4}$/.test(trimmed) ||
    /^[a-zA-Z0-9][a-zA-Z0-9._-]{2,}@hpr\.abdm$/i.test(trimmed);
  const record = useQuery<AbdmHprPublicRecord>({
    queryKey: ["abdm", "hpr", "verify-id", trimmed],
    queryFn: query.debounced(careApi.hprVerifyId, {
      queryParams: { hpr_id: trimmed },
      silent: true,
    }),
    enabled: open && complete && !pendingLogin,
    retry: false,
  });
  const recordUnknown =
    record.isError && (record.error as HttpError).status === 404;
  /** True when the registry names a mobile method for this HPR ID (findings N5). */
  const mobileOffered = Boolean(
    record.data?.auth_methods.some((m) => m.toLowerCase().includes("mobile")),
  );

  const apply = (state: AbdmHprState) => {
    qc.setQueryData(hprQueryKey, state);
    onDone?.(state);
  };
  const login = useMutation<AbdmHprState, unknown, void>({
    mutationFn: () =>
      mutate(careApi.hprLogin, { silent: true })({
        method,
        hpr_id: trimmed,
        password: method === "password" ? password : undefined,
      }),
    onMutate: () => setError(undefined),
    onSuccess: (state) => {
      apply(state);
      if (state.session.active) onOpenChange(false);
    },
    onError: (e) => setError(errorMessage(e, t("abdm_hpr_login_failed"))),
  });
  const verify = useMutation<AbdmHprState, unknown, void>({
    mutationFn: () =>
      mutate(careApi.hprLoginVerify, { silent: true })({
        login_id: pendingLogin?.id ?? "",
        otp,
      }),
    onMutate: () => setError(undefined),
    onSuccess: (state) => {
      apply(state);
      if (state.session.active) onOpenChange(false);
    },
    onError: (e) => setError(errorMessage(e, t("abdm_hpr_login_failed"))),
  });
  const busy = login.isPending || verify.isPending;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <ShieldCheck className="text-muted-foreground size-4" />
            {t("abdm_hpr_login_title")}
          </DialogTitle>
          <DialogDescription>{t("abdm_hpr_login_intro")}</DialogDescription>
        </DialogHeader>

        {pendingLogin ? (
          <div className="grid gap-3 text-sm">
            <p>
              {t("abdm_hpr_otp_sent")
                .replace("{{id}}", pendingLogin.hprId)
                .replace("{{mobile}}", pendingLogin.mobileMasked || "******")}
            </p>
            <NhprField labelKey="abdm_otp" htmlFor="abdm-hpr-otp">
              <Input
                id="abdm-hpr-otp"
                inputMode="numeric"
                maxLength={6}
                value={otp}
                onChange={(e) => setOtp(e.target.value.replace(/\D/g, ""))}
              />
            </NhprField>
          </div>
        ) : (
          <div className="grid gap-3 text-sm">
            <NhprField labelKey="abdm_hpr_id" htmlFor="abdm-hpr-id">
              <Input
                id="abdm-hpr-id"
                placeholder="name@hpr.abdm"
                value={hprId}
                onChange={(e) => setHprId(e.target.value)}
                autoComplete="username"
              />
              <span className="text-muted-foreground min-h-4 text-xs">
                {record.isFetching && t("abdm_hpr_checking")}
                {record.data &&
                  `${record.data.name} · ${record.data.hpr_id_number} · ${record.data.auth_methods.join(", ")}`}
                {recordUnknown && t("abdm_hpr_id_unknown")}
                {record.isError &&
                  !recordUnknown &&
                  errorMessage(record.error, t("abdm_hpr_id_check_failed"))}
              </span>
            </NhprField>
            <div className="grid gap-1.5">
              <span className="text-sm font-medium">
                {t("abdm_hpr_login_method")}
              </span>
              <RadioGroup
                value={method}
                onValueChange={(next) =>
                  setMethod(next as "password" | "aadhaar_otp")
                }
                className="grid-cols-2 gap-2"
              >
                {(["password", "aadhaar_otp"] as const).map((m) => (
                  <label
                    key={m}
                    className="border-input has-[[data-checked]]:border-primary has-[[data-checked]]:bg-primary/5 flex cursor-pointer items-center gap-2.5 rounded-lg border p-3"
                  >
                    <RadioGroupItem value={m} />
                    {t(`abdm_hpr_method_${m}`)}
                  </label>
                ))}
              </RadioGroup>
            </div>
            {method === "password" && (
              <NhprField
                labelKey="abdm_hpr_password"
                htmlFor="abdm-hpr-password"
              >
                <Input
                  id="abdm-hpr-password"
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  autoComplete="current-password"
                />
              </NhprField>
            )}
            {/*
             * The registry names a mobile OTP for some HPR IDs, but publishes a send call and no
             * verify call (findings N5). Name that gap only for a person whose record offers the
             * method; for everybody else it is noise (Rithvik, 2026-09-21).
             */}
            {mobileOffered && (
              <p className="text-muted-foreground text-xs">
                {t("abdm_hpr_login_help")}
              </p>
            )}
          </div>
        )}

        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        <DialogFooter>
          <Button
            type="button"
            variant="outline"
            disabled={busy}
            onClick={() => onOpenChange(false)}
          >
            {t("abdm_cancel")}
          </Button>
          {pendingLogin ? (
            <Button
              type="button"
              disabled={busy || otp.length < 4}
              onClick={() => verify.mutate()}
            >
              {busy && <Loader2 className="size-4 animate-spin" />}
              {t("abdm_verify")}
            </Button>
          ) : (
            <Button
              type="button"
              disabled={
                busy ||
                trimmed.length < 3 ||
                (method === "password" && !password)
              }
              onClick={() => login.mutate()}
            >
              {busy && <Loader2 className="size-4 animate-spin" />}
              {method === "password" ? t("abdm_hpr_login") : t("abdm_send_otp")}
            </Button>
          )}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
