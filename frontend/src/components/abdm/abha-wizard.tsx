import {
  Alert,
  AlertAction,
  AlertDescription,
  AlertTitle,
} from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import {
  InputOTP,
  InputOTPGroup,
  InputOTPSlot,
} from "@/components/ui/input-otp";
import { Label } from "@/components/ui/label";
import { useTranslation } from "@/hooks/use-translation";
import careApi, {
  type AbdmRelayError,
  type AbhaAccount,
  type AbhaAccountProfile,
  type AbhaSource,
  type EnrolByAadhaarResponse,
  type ExistingPatient,
  type LoginCompleted,
  type LoginHint,
  type OtpSystem,
} from "@/lib/careApi";
import { HttpError, mutate } from "@/lib/request";
import { cn } from "@/lib/utils";
import { useMutation } from "@tanstack/react-query";
import {
  AtSign,
  CheckCircle2,
  ChevronLeft,
  CreditCard,
  Fingerprint,
  Smartphone,
} from "lucide-react";
import { useEffect, useState } from "react";

/**
 * One dialog, two journeys from the docs' M1 milestone page:
 *   create — Journey 1 (+2): Aadhaar OTP → [mobile OTP] → ABHA address → done
 *   link   — log in to an existing ABHA by mobile / ABHA number / ABHA address /
 *            Aadhaar (m1-login-request-otp loginHint; phr variant for address).
 *            Mobile may return several accounts → pick one; the others finish in
 *            one OTP.
 * A login against an identifier that has no ABHA ends the journey with nothing to
 * link (ABDM answers `404 ABDM-1114`, or the account list comes back empty). The
 * error then carries one action that starts the create journey with the typed
 * Aadhaar and mobile, so the desk does not type them a second time.
 * The browser only ever talks to the Care backend plug; it never sees ABDM tokens.
 * On completion the caller receives the server-side transaction id, which is the
 * only thing the backend trusts (abdm/signals.py, abdm/abha/views.py PatientAbhaLink).
 */

export type AbhaWizardResult = {
  txnId: string;
  abhaNumber?: string;
  abhaAddress?: string;
  profile?: AbhaAccountProfile;
  source: AbhaSource;
  /** Set on login when this ABHA is already linked to a Care patient. */
  existingPatient?: ExistingPatient | null;
};

type Mode = "choose" | "create" | "link";
type CreateStep = "aadhaar" | "otp" | "mobile-otp" | "address" | "done";
type LinkStep = "identify" | "otp" | "accounts" | "done";

const LOGIN_HINTS: LoginHint[] = [
  "mobile",
  "abha-number",
  "abha-address",
  "aadhaar",
];

const SOURCE_BY_HINT: Record<LoginHint, AbhaSource> = {
  mobile: "login_mobile",
  "abha-number": "login_abha_number",
  "abha-address": "login_abha_address",
  aadhaar: "login_aadhaar",
};

/**
 * The OTP system that an identifier uses when the desk makes no choice.
 * A `mobile` login only supports `abdm`. An `aadhaar` login authenticates
 * against UIDAI, so the OTP must go to the Aadhaar-linked mobile.
 */
const defaultOtpSystem = (h: LoginHint): OtpSystem =>
  h === "aadhaar" ? "aadhaar" : "abdm";

/** Only an ABHA number or an ABHA address supports both OTP systems. */
const canChooseOtpSystem = (h: LoginHint) =>
  h === "abha-number" || h === "abha-address";

type Props = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  /** Skip the chooser and start directly in one journey. */
  initialMode?: Exclude<Mode, "choose">;
  /** Which identifier the link journey opens on (default mobile). */
  initialHint?: LoginHint;
  /** Prefill for the mobile fields (10 digits, no +91). */
  defaultMobile?: string;
  onComplete: (result: AbhaWizardResult) => void;
  /** Rendered on the final step below the summary (e.g. a "linking…" state). */
  finishing?: boolean;
  finishLabel?: string;
  /** Rendered on the final step when the caller's own step failed (e.g. the link call). */
  finishError?: string;
  /** Replace the default done-step body + footer (e.g. "open patient / register"). */
  renderDone?: (result: AbhaWizardResult) => {
    body?: React.ReactNode;
    footer?: React.ReactNode;
  };
};

export function relayMessage(err: unknown, fallback: string): string {
  if (err instanceof HttpError) {
    const cause = err.cause as Partial<AbdmRelayError> | undefined;
    if (cause?.message) {
      return cause.abdm_code
        ? `${cause.message} (${cause.abdm_code})`
        : cause.message;
    }
    const errors = (err.cause as { errors?: string } | undefined)?.errors;
    if (errors) return errors;
  }
  return fallback;
}

export function relayCode(err: unknown): string | undefined {
  if (err instanceof HttpError) {
    const cause = err.cause as Partial<AbdmRelayError> | undefined;
    return cause?.abdm_code ?? undefined;
  }
  return undefined;
}

/**
 * The login answer for an identifier that carries no ABHA account. The M1 error
 * table gives this code a different message, but the sandbox returns it as
 * `404 ABDM-1114 User not found` on every login path (docs/findings.md A8), and
 * a DigiLocker name mismatch cannot happen in a login journey.
 */
const NO_ABHA_CODE = "ABDM-1114";

export function formatAbhaNumber(n?: string | null) {
  if (!n) return "";
  const d = n.replace(/\D/g, "");
  return d.length === 14
    ? `${d.slice(0, 2)}-${d.slice(2, 6)}-${d.slice(6, 10)}-${d.slice(10)}`
    : n;
}

function OtpField({
  value,
  onChange,
  onEnter,
  autoFocus,
}: {
  value: string;
  onChange: (v: string) => void;
  onEnter?: () => void;
  autoFocus?: boolean;
}) {
  return (
    <InputOTP
      maxLength={6}
      value={value}
      onChange={(v) => onChange(v.replace(/\D/g, ""))}
      autoFocus={autoFocus}
      onKeyDown={(e) => {
        if (e.key === "Enter" && value.length === 6) onEnter?.();
      }}
      containerClassName="justify-center"
    >
      <InputOTPGroup>
        {[0, 1, 2, 3, 4, 5].map((i) => (
          <InputOTPSlot key={i} index={i} className="size-11 text-lg" />
        ))}
      </InputOTPGroup>
    </InputOTP>
  );
}

function ResendTimer({
  seconds = 60,
  onResend,
  disabled,
  resetKey,
}: {
  seconds?: number;
  onResend: () => void;
  disabled?: boolean;
  resetKey: string;
}) {
  const { t } = useTranslation();
  const [left, setLeft] = useState(seconds);
  useEffect(() => {
    setLeft(seconds);
    const id = setInterval(() => setLeft((s) => (s > 0 ? s - 1 : 0)), 1000);
    return () => clearInterval(id);
  }, [seconds, resetKey]);
  return (
    <Button
      type="button"
      variant="link"
      size="xs"
      disabled={disabled || left > 0}
      onClick={onResend}
      className="text-muted-foreground"
    >
      {left > 0 ? t("abdm_resend_in", { seconds: left }) : t("abdm_resend_otp")}
    </Button>
  );
}

function ModeCard({
  icon,
  title,
  description,
  onClick,
}: {
  icon: React.ReactNode;
  title: string;
  description: string;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        "group flex w-full items-start gap-3 rounded-xl border p-4 text-left transition-colors",
        "hover:border-primary hover:bg-primary/5 focus-visible:ring-ring/50 focus-visible:ring-[3px] focus-visible:outline-none",
      )}
    >
      <div className="bg-primary/10 text-primary rounded-lg p-2">{icon}</div>
      <div className="min-w-0">
        <div className="font-semibold">{title}</div>
        <div className="text-muted-foreground text-sm">{description}</div>
      </div>
    </button>
  );
}

export default function AbhaWizard({
  open,
  onOpenChange,
  initialMode,
  initialHint = "mobile",
  defaultMobile = "",
  onComplete,
  finishing,
  finishLabel,
  finishError,
  renderDone,
}: Props) {
  const { t } = useTranslation();
  const [mode, setMode] = useState<Mode>(initialMode ?? "choose");
  const [error, setError] = useState<string>();
  const [info, setInfo] = useState<string>();

  // create journey
  const [createStep, setCreateStep] = useState<CreateStep>("aadhaar");
  const [aadhaar, setAadhaar] = useState("");
  const [consent, setConsent] = useState(false);
  const [mobile, setMobile] = useState(defaultMobile);
  const [otp, setOtp] = useState("");
  const [txnId, setTxnId] = useState("");
  const [profile, setProfile] = useState<EnrolByAadhaarResponse>();
  const [addresses, setAddresses] = useState<string[]>([]);
  const [address, setAddress] = useState("");

  // link journey
  const [linkStep, setLinkStep] = useState<LinkStep>("identify");
  const [hint, setHint] = useState<LoginHint>(initialHint);
  const [loginId, setLoginId] = useState("");
  const [otpSystem, setOtpSystem] = useState<OtpSystem>(
    defaultOtpSystem(initialHint),
  );
  const [accounts, setAccounts] = useState<AbhaAccount[]>([]);
  const [selected, setSelected] = useState<string>("");
  const [result, setResult] = useState<AbhaWizardResult>();
  /** The login found no ABHA, so the create journey is the way out. */
  const [noAbha, setNoAbha] = useState(false);
  /** The create journey started from a failed login; the back arrow returns there. */
  const [fromLink, setFromLink] = useState(false);

  useEffect(() => {
    if (!open) return;
    setMode(initialMode ?? "choose");
    setError(undefined);
    setInfo(undefined);
    setCreateStep("aadhaar");
    setLinkStep("identify");
    setHint(initialHint);
    setLoginId(initialHint === "mobile" ? defaultMobile : "");
    setOtpSystem(defaultOtpSystem(initialHint));
    setAadhaar("");
    setConsent(false);
    setMobile(defaultMobile);
    setOtp("");
    setTxnId("");
    setProfile(undefined);
    setAddresses([]);
    setAddress("");
    setAccounts([]);
    setSelected("");
    setResult(undefined);
    setNoAbha(false);
    setFromLink(false);
  }, [open, initialMode, initialHint, defaultMobile]);

  const clearError = () => {
    setError(undefined);
    setNoAbha(false);
  };

  const fail = (fallback: string) => (err: unknown) =>
    setError(relayMessage(err, fallback));

  /** A login failure can also mean "this person has no ABHA yet". */
  const failLogin = (fallback: string) => (err: unknown) => {
    setError(relayMessage(err, fallback));
    setNoAbha(relayCode(err) === NO_ABHA_CODE);
  };

  /**
   * Leave the failed login and start the create journey with what the desk
   * already typed. The login transaction is dropped: the create journey opens
   * its own.
   */
  const createFromLink = () => {
    clearError();
    setInfo(undefined);
    setOtp("");
    setTxnId("");
    setAccounts([]);
    setSelected("");
    if (hint === "aadhaar") setAadhaar(loginId.replace(/\D/g, "").slice(0, 12));
    if (hint === "mobile") setMobile(loginId.replace(/\D/g, "").slice(0, 10));
    setConsent(false);
    setFromLink(true);
    setCreateStep("aadhaar");
    setMode("create");
  };

  const generic = t("abdm_error_generic");

  // ---- Journey 1 ----------------------------------------------------------
  const requestOtp = useMutation<
    NonNullable<typeof careApi.requestAadhaarOtp.TResponse>,
    unknown,
    NonNullable<typeof careApi.requestAadhaarOtp.TRequest>
  >({
    mutationFn: mutate(careApi.requestAadhaarOtp, { silent: true }),
    onMutate: () => clearError(),
    onSuccess: (res) => {
      setTxnId(res.txnId);
      setInfo(res.message);
      setOtp("");
      setCreateStep("otp");
    },
    onError: fail(generic),
  });

  const enrol = useMutation<
    NonNullable<typeof careApi.enrolByAadhaar.TResponse>,
    unknown,
    NonNullable<typeof careApi.enrolByAadhaar.TRequest>
  >({
    mutationFn: mutate(careApi.enrolByAadhaar, { silent: true }),
    onMutate: () => clearError(),
    onSuccess: (res) => {
      setProfile(res);
      const id = res.txnId ?? txnId;
      setTxnId(id);
      setOtp("");
      const abhaMobile = res.ABHAProfile?.mobile;
      if (abhaMobile && abhaMobile !== mobile) {
        requestMobileOtp.mutate({ txn_id: id, mobile });
      } else {
        suggestions.mutate({ txn_id: id });
      }
    },
    onError: fail(generic),
  });

  const requestMobileOtp = useMutation<
    NonNullable<typeof careApi.requestMobileOtp.TResponse>,
    unknown,
    NonNullable<typeof careApi.requestMobileOtp.TRequest>
  >({
    mutationFn: mutate(careApi.requestMobileOtp, { silent: true }),
    onSuccess: (res) => {
      setTxnId(res.txnId);
      setInfo(res.message);
      setCreateStep("mobile-otp");
    },
    onError: fail(generic),
  });

  const verifyMobileOtp = useMutation<
    NonNullable<typeof careApi.verifyMobileOtp.TResponse>,
    unknown,
    NonNullable<typeof careApi.verifyMobileOtp.TRequest>
  >({
    mutationFn: mutate(careApi.verifyMobileOtp, { silent: true }),
    onMutate: () => clearError(),
    onSuccess: (res) => {
      setTxnId(res.txnId);
      suggestions.mutate({ txn_id: res.txnId });
    },
    onError: fail(generic),
  });

  const suggestions = useMutation<
    NonNullable<typeof careApi.addressSuggestions.TResponse>,
    unknown,
    NonNullable<typeof careApi.addressSuggestions.TRequest>
  >({
    mutationFn: mutate(careApi.addressSuggestions, { silent: true }),
    onSuccess: (res) => {
      setAddresses(res.abhaAddressList ?? []);
      setAddress(res.abhaAddressList?.[0] ?? "");
      setInfo(undefined);
      setCreateStep("address");
    },
    onError: fail(generic),
  });

  const claim = useMutation<
    NonNullable<typeof careApi.claimAbhaAddress.TResponse>,
    unknown,
    NonNullable<typeof careApi.claimAbhaAddress.TRequest>
  >({
    mutationFn: mutate(careApi.claimAbhaAddress, { silent: true }),
    onMutate: () => clearError(),
    onSuccess: (res) => {
      const r: AbhaWizardResult = {
        txnId,
        abhaNumber: res.healthIdNumber ?? profile?.ABHAProfile?.ABHANumber,
        abhaAddress: res.preferredAbhaAddress ?? address,
        profile: profile?.ABHAProfile,
        source: "enrol_aadhaar",
      };
      setResult(r);
      setCreateStep("done");
      onComplete(r);
    },
    onError: fail(generic),
  });

  // ---- Login to an existing ABHA ------------------------------------------
  const finishLogin = (res: LoginCompleted, fallbackName?: string) => {
    const r: AbhaWizardResult = {
      txnId: res.txnId,
      abhaNumber: res.ABHANumber,
      abhaAddress: res.preferredAbhaAddress,
      profile: {
        ...res.profile,
        name: res.profile?.name ?? res.name ?? fallbackName,
        mobile:
          res.profile?.mobile ?? (hint === "mobile" ? loginId : undefined),
      },
      source: SOURCE_BY_HINT[hint],
      existingPatient: res.existingPatient,
    };
    setResult(r);
    setLinkStep("done");
    onComplete(r);
  };

  const loginOtp = useMutation<
    NonNullable<typeof careApi.loginRequestOtp.TResponse>,
    unknown,
    NonNullable<typeof careApi.loginRequestOtp.TRequest>
  >({
    mutationFn: mutate(careApi.loginRequestOtp, { silent: true }),
    onMutate: () => clearError(),
    onSuccess: (res) => {
      setTxnId(res.txnId);
      setInfo(res.message);
      setOtp("");
      setLinkStep("otp");
    },
    onError: failLogin(generic),
  });

  const loginVerify = useMutation<
    NonNullable<typeof careApi.loginVerifyOtp.TResponse>,
    unknown,
    NonNullable<typeof careApi.loginVerifyOtp.TRequest>
  >({
    mutationFn: mutate(careApi.loginVerifyOtp, { silent: true }),
    onMutate: () => clearError(),
    onSuccess: (res) => {
      setTxnId(res.txnId);
      setInfo(undefined);
      if (res.completed) {
        finishLogin(res);
        return;
      }
      const list = res.accounts ?? [];
      setAccounts(list);
      if (list.length === 0) {
        setError(t("abdm_no_accounts"));
        setNoAbha(true);
        return;
      }
      setSelected(list[0].ABHANumber);
      if (list.length === 1) {
        loginSelect.mutate({
          txn_id: res.txnId,
          abha_number: list[0].ABHANumber,
        });
      } else {
        setLinkStep("accounts");
      }
    },
    onError: failLogin(generic),
  });

  const loginSelect = useMutation<
    NonNullable<typeof careApi.loginSelectAccount.TResponse>,
    unknown,
    NonNullable<typeof careApi.loginSelectAccount.TRequest>
  >({
    mutationFn: mutate(careApi.loginSelectAccount, { silent: true }),
    onMutate: () => clearError(),
    onSuccess: (res) => {
      const acc = accounts.find((a) => a.ABHANumber === res.ABHANumber);
      finishLogin(res, acc?.name);
    },
    onError: failLogin(generic),
  });

  const sendLoginOtp = () =>
    loginOtp.mutate({
      hint,
      login_id: loginId,
      otp_system: canChooseOtpSystem(hint) ? otpSystem : defaultOtpSystem(hint),
    });

  const busy =
    requestOtp.isPending ||
    enrol.isPending ||
    requestMobileOtp.isPending ||
    verifyMobileOtp.isPending ||
    suggestions.isPending ||
    claim.isPending ||
    loginOtp.isPending ||
    loginVerify.isPending ||
    loginSelect.isPending;

  const done =
    (mode === "create" && createStep === "done") ||
    (mode === "link" && linkStep === "done");
  const customDone =
    done && result && renderDone ? renderDone(result) : undefined;

  const title =
    mode === "create"
      ? t("abdm_create_abha")
      : mode === "link"
        ? t("abdm_link_abha")
        : t("abdm_abha");
  const description =
    mode === "choose"
      ? t("abdm_choose_hint")
      : mode === "create"
        ? t(`abdm_step_${createStep}`)
        : t(`abdm_link_step_${linkStep}`);

  const canGoBack =
    !done &&
    !busy &&
    ((mode !== "choose" && !initialMode) ||
      (mode === "create" && (createStep !== "aadhaar" || fromLink)) ||
      (mode === "link" && linkStep !== "identify"));

  const goBack = () => {
    clearError();
    setInfo(undefined);
    setOtp("");
    if (mode === "create") {
      if (createStep === "aadhaar" && fromLink) {
        setFromLink(false);
        setLinkStep("identify");
        return setMode("link");
      }
      if (createStep === "aadhaar") return setMode("choose");
      if (createStep === "address" || createStep === "mobile-otp")
        return setCreateStep("aadhaar");
      return setCreateStep("aadhaar");
    }
    if (mode === "link") {
      if (linkStep === "identify") return setMode("choose");
      return setLinkStep("identify");
    }
  };

  const mobileValid = mobile.length === 10 && /^[6-9]/.test(mobile);

  // Per-identifier input rules. Backend re-validates (abdm/abha/views.py LoginOtpRequest);
  // this only gates the button so the desk gets instant feedback.
  const loginIdDigits = loginId.replace(/\D/g, "");
  const loginIdValid =
    hint === "mobile"
      ? /^[6-9]\d{9}$/.test(loginIdDigits)
      : hint === "abha-number"
        ? loginIdDigits.length === 14
        : hint === "aadhaar"
          ? loginIdDigits.length === 12
          : /^[a-z0-9._]{3,}(@[a-z]+)?$/i.test(loginId.trim());

  const setLoginIdFor = (h: LoginHint, raw: string) => {
    if (h === "abha-address") {
      setLoginId(raw.replace(/[^a-zA-Z0-9._@]/g, "").toLowerCase());
      return;
    }
    const max = h === "mobile" ? 10 : h === "aadhaar" ? 12 : 14;
    setLoginId(raw.replace(/\D/g, "").slice(0, max));
  };

  const changeHint = (h: LoginHint) => {
    setHint(h);
    setLoginId(h === "mobile" ? defaultMobile : "");
    setOtpSystem(defaultOtpSystem(h));
    clearError();
  };

  const loginIdDisplay =
    hint === "abha-number"
      ? formatAbhaNumber(loginId) || loginId
      : hint === "aadhaar"
        ? loginId.replace(/(\d{4})(?=\d)/g, "$1 ")
        : loginId;

  // Where the OTP went, for the OTP-step label.
  const otpDestination =
    hint === "mobile"
      ? t("abdm_mobile_otp", { mobile: loginId })
      : otpSystem === "aadhaar"
        ? t("abdm_login_otp_aadhaar_mobile")
        : t("abdm_login_otp_abha_mobile");

  return (
    <Dialog open={open} onOpenChange={(o) => !busy && onOpenChange(o)}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <div className="flex items-center gap-2">
            {canGoBack && (
              <Button
                type="button"
                variant="ghost"
                size="icon-xs"
                onClick={goBack}
                aria-label={t("abdm_back")}
              >
                <ChevronLeft />
              </Button>
            )}
            <DialogTitle>{title}</DialogTitle>
          </div>
          <DialogDescription>{description}</DialogDescription>
        </DialogHeader>

        {error && (
          <Alert variant="destructive">
            <AlertTitle>{t("abdm_error")}</AlertTitle>
            <AlertDescription>{error}</AlertDescription>
            {mode === "link" && noAbha && !busy && (
              <AlertAction>
                <Button
                  type="button"
                  size="sm"
                  variant="outline"
                  onClick={createFromLink}
                >
                  <Fingerprint />
                  {t("abdm_create_abha_instead")}
                </Button>
              </AlertAction>
            )}
          </Alert>
        )}
        {info && !error && !done && (
          <Alert variant="info">
            <AlertDescription>{info}</AlertDescription>
          </Alert>
        )}

        {mode === "choose" && (
          <div className="grid gap-2">
            <ModeCard
              icon={<Fingerprint className="size-5" />}
              title={t("abdm_create_abha")}
              description={t("abdm_create_abha_hint")}
              onClick={() => setMode("create")}
            />
            <ModeCard
              icon={<Smartphone className="size-5" />}
              title={t("abdm_link_abha")}
              description={t("abdm_link_abha_hint")}
              onClick={() => setMode("link")}
            />
          </div>
        )}

        {/* ---------------- create ---------------- */}
        {mode === "create" && createStep === "aadhaar" && (
          <div className="grid gap-4">
            <div className="grid gap-1.5">
              <Label htmlFor="abdm-aadhaar">{t("abdm_aadhaar_number")}</Label>
              <Input
                id="abdm-aadhaar"
                inputMode="numeric"
                maxLength={14}
                autoComplete="off"
                autoFocus
                placeholder="0000 0000 0000"
                className="font-mono text-lg tracking-[0.2em]"
                value={aadhaar.replace(/(\d{4})(?=\d)/g, "$1 ")}
                onChange={(e) =>
                  setAadhaar(e.target.value.replace(/\D/g, "").slice(0, 12))
                }
              />
            </div>
            <div className="grid gap-1.5">
              <Label htmlFor="abdm-mobile">{t("abdm_mobile_number")}</Label>
              <div className="flex items-center gap-2">
                <span className="text-muted-foreground font-mono text-sm">
                  +91
                </span>
                <Input
                  id="abdm-mobile"
                  inputMode="numeric"
                  maxLength={10}
                  className="font-mono tracking-wider"
                  value={mobile}
                  onChange={(e) =>
                    setMobile(e.target.value.replace(/\D/g, "").slice(0, 10))
                  }
                />
              </div>
              <p className="text-muted-foreground text-xs">
                {t("abdm_mobile_hint")}
              </p>
            </div>
            <label
              htmlFor="abdm-consent"
              className="flex cursor-pointer items-start gap-3 rounded-lg border p-3 text-sm"
            >
              <Checkbox
                id="abdm-consent"
                checked={consent}
                onCheckedChange={(v) => setConsent(v === true)}
                className="mt-0.5"
              />
              <span className="text-muted-foreground text-xs leading-relaxed">
                {t("abdm_consent_note")}
              </span>
            </label>
          </div>
        )}

        {mode === "create" &&
          (createStep === "otp" || createStep === "mobile-otp") && (
            <div className="grid gap-3">
              <Label className="justify-center">
                {createStep === "otp"
                  ? t("abdm_aadhaar_otp")
                  : t("abdm_mobile_otp", { mobile })}
              </Label>
              <OtpField
                value={otp}
                onChange={setOtp}
                autoFocus
                onEnter={() =>
                  createStep === "otp"
                    ? enrol.mutate({ txn_id: txnId, otp, mobile })
                    : verifyMobileOtp.mutate({ txn_id: txnId, otp })
                }
              />
              <div className="flex justify-center">
                <ResendTimer
                  resetKey={txnId}
                  disabled={busy}
                  onResend={() =>
                    createStep === "otp"
                      ? requestOtp.mutate({ aadhaar_number: aadhaar, consent })
                      : requestMobileOtp.mutate({ txn_id: txnId, mobile })
                  }
                />
              </div>
            </div>
          )}

        {mode === "create" && createStep === "address" && (
          <div className="grid gap-4">
            {profile?.ABHAProfile?.ABHANumber && (
              <div className="bg-muted/50 flex items-center gap-3 rounded-lg border p-3">
                <CheckCircle2 className="size-5 shrink-0 text-emerald-600" />
                <div className="min-w-0 text-sm">
                  <div className="text-muted-foreground text-xs">
                    {t("abdm_abha_number")}
                  </div>
                  <div className="font-mono font-semibold tracking-wider">
                    {formatAbhaNumber(profile.ABHAProfile.ABHANumber)}
                  </div>
                  {profile.ABHAProfile.firstName && (
                    <div className="text-muted-foreground truncate">
                      {[
                        profile.ABHAProfile.firstName,
                        profile.ABHAProfile.middleName,
                        profile.ABHAProfile.lastName,
                      ]
                        .filter(Boolean)
                        .join(" ")}
                    </div>
                  )}
                </div>
              </div>
            )}
            <div className="grid gap-1.5">
              <Label htmlFor="abdm-address">{t("abdm_abha_address")}</Label>
              <div className="flex items-center gap-1">
                <Input
                  id="abdm-address"
                  autoFocus
                  className="font-mono"
                  value={address}
                  onChange={(e) =>
                    setAddress(e.target.value.replace(/[^a-zA-Z0-9._]/g, ""))
                  }
                />
                <span className="text-muted-foreground font-mono text-sm">
                  @abdm
                </span>
              </div>
              <p className="text-muted-foreground text-xs">
                {t("abdm_address_hint")}
              </p>
            </div>
            {addresses.length > 0 && (
              <div className="flex flex-wrap gap-1.5">
                {addresses.slice(0, 6).map((a) => (
                  <Button
                    key={a}
                    type="button"
                    size="xs"
                    variant={a === address ? "secondary" : "outline"}
                    className="font-mono"
                    onClick={() => setAddress(a)}
                  >
                    {a}
                  </Button>
                ))}
              </div>
            )}
          </div>
        )}

        {/* ---------------- link ---------------- */}
        {mode === "link" && linkStep === "identify" && (
          <div className="grid gap-4">
            <div
              role="tablist"
              aria-label={t("abdm_link_identify_with")}
              className="bg-muted grid grid-cols-4 gap-1 rounded-lg p-1"
            >
              {LOGIN_HINTS.map((h) => {
                const Icon =
                  h === "mobile"
                    ? Smartphone
                    : h === "abha-number"
                      ? CreditCard
                      : h === "abha-address"
                        ? AtSign
                        : Fingerprint;
                return (
                  <button
                    key={h}
                    type="button"
                    role="tab"
                    aria-selected={hint === h}
                    onClick={() => changeHint(h)}
                    className={cn(
                      "flex flex-col items-center gap-1 rounded-md px-1 py-1.5 text-xs transition-colors",
                      hint === h
                        ? "bg-background text-foreground shadow-sm"
                        : "text-muted-foreground hover:text-foreground",
                    )}
                  >
                    <Icon className="size-4" />
                    <span className="truncate">{t(`abdm_hint_${h}`)}</span>
                  </button>
                );
              })}
            </div>

            <div className="grid gap-1.5">
              <Label htmlFor="abdm-login-id">
                {t(`abdm_hint_${hint}_label`)}
              </Label>
              <div className="flex items-center gap-2">
                {hint === "mobile" && (
                  <span className="text-muted-foreground font-mono text-sm">
                    +91
                  </span>
                )}
                <Input
                  id="abdm-login-id"
                  key={hint}
                  inputMode={hint === "abha-address" ? "email" : "numeric"}
                  autoComplete="off"
                  autoFocus
                  maxLength={
                    hint === "mobile"
                      ? 10
                      : hint === "abha-number"
                        ? 17
                        : hint === "aadhaar"
                          ? 14
                          : 64
                  }
                  placeholder={
                    hint === "abha-number"
                      ? "91-0000-0000-0000"
                      : hint === "aadhaar"
                        ? "0000 0000 0000"
                        : hint === "abha-address"
                          ? "name@abdm"
                          : undefined
                  }
                  className={cn(
                    "font-mono",
                    hint !== "abha-address" && "tracking-wider",
                  )}
                  value={loginIdDisplay}
                  onChange={(e) => setLoginIdFor(hint, e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" && loginIdValid) sendLoginOtp();
                  }}
                />
              </div>
              <p className="text-muted-foreground text-xs">
                {t(`abdm_hint_${hint}_help`)}
              </p>
            </div>

            {canChooseOtpSystem(hint) && (
              <div className="grid gap-1.5">
                <Label>{t("abdm_otp_send_to")}</Label>
                <div className="grid grid-cols-2 gap-2">
                  {(["abdm", "aadhaar"] as OtpSystem[]).map((s) => (
                    <button
                      key={s}
                      type="button"
                      onClick={() => setOtpSystem(s)}
                      className={cn(
                        "rounded-lg border p-2.5 text-left text-sm transition-colors",
                        otpSystem === s
                          ? "border-primary bg-primary/5"
                          : "hover:bg-muted/50",
                      )}
                    >
                      <div className="font-medium">
                        {t(`abdm_otp_system_${s}`)}
                      </div>
                      <div className="text-muted-foreground text-xs">
                        {t(`abdm_otp_system_${s}_hint`)}
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {mode === "link" && linkStep === "otp" && (
          <div className="grid gap-3">
            <Label className="justify-center">{otpDestination}</Label>
            <OtpField
              value={otp}
              onChange={setOtp}
              autoFocus
              onEnter={() => loginVerify.mutate({ txn_id: txnId, otp })}
            />
            <div className="flex justify-center">
              <ResendTimer
                resetKey={txnId}
                disabled={busy}
                onResend={sendLoginOtp}
              />
            </div>
          </div>
        )}

        {mode === "link" && linkStep === "accounts" && (
          <div className="grid gap-2">
            {accounts.map((a) => (
              <button
                key={a.ABHANumber}
                type="button"
                onClick={() => setSelected(a.ABHANumber)}
                className={cn(
                  "flex w-full items-center justify-between gap-3 rounded-lg border p-3 text-left transition-colors",
                  selected === a.ABHANumber
                    ? "border-primary bg-primary/5"
                    : "hover:bg-muted/50",
                )}
              >
                <div className="min-w-0">
                  <div className="truncate font-semibold">{a.name ?? "—"}</div>
                  <div className="text-muted-foreground font-mono text-xs tracking-wider">
                    {formatAbhaNumber(a.ABHANumber)}
                  </div>
                  {a.preferredAbhaAddress && (
                    <div className="text-muted-foreground font-mono text-xs">
                      {a.preferredAbhaAddress}
                    </div>
                  )}
                </div>
                {selected === a.ABHANumber && (
                  <CheckCircle2 className="text-primary size-5 shrink-0" />
                )}
              </button>
            ))}
          </div>
        )}

        {/* ---------------- done ---------------- */}
        {done && result && (
          <div className="grid gap-3">
            <div className="flex items-center gap-3 rounded-lg border border-emerald-200 bg-emerald-50 p-3 dark:border-emerald-900 dark:bg-emerald-950">
              <CheckCircle2 className="size-6 shrink-0 text-emerald-600" />
              <div className="min-w-0">
                <div className="font-semibold">{t("abdm_done_title")}</div>
                <div className="font-mono text-sm tracking-wider">
                  {formatAbhaNumber(result.abhaNumber)}
                </div>
                {result.abhaAddress && (
                  <div className="text-muted-foreground font-mono text-xs">
                    {result.abhaAddress}
                  </div>
                )}
              </div>
            </div>
            {finishing && (
              <p className="text-muted-foreground text-center text-xs">
                {finishLabel ?? t("abdm_linking")}
              </p>
            )}
            {finishError && (
              <p className="text-destructive text-center text-sm">
                {finishError}
              </p>
            )}
            {customDone?.body}
          </div>
        )}

        <DialogFooter>
          {mode === "create" && createStep === "aadhaar" && (
            <Button
              type="button"
              disabled={
                busy || aadhaar.length !== 12 || !mobileValid || !consent
              }
              onClick={() =>
                requestOtp.mutate({ aadhaar_number: aadhaar, consent })
              }
            >
              {t("abdm_send_otp")}
            </Button>
          )}
          {mode === "create" && createStep === "otp" && (
            <Button
              type="button"
              disabled={busy || otp.length !== 6}
              onClick={() => enrol.mutate({ txn_id: txnId, otp, mobile })}
            >
              {t("abdm_verify")}
            </Button>
          )}
          {mode === "create" && createStep === "mobile-otp" && (
            <Button
              type="button"
              disabled={busy || otp.length !== 6}
              onClick={() => verifyMobileOtp.mutate({ txn_id: txnId, otp })}
            >
              {t("abdm_verify")}
            </Button>
          )}
          {mode === "create" && createStep === "address" && (
            <Button
              type="button"
              disabled={busy || address.length < 4}
              onClick={() =>
                claim.mutate({ txn_id: txnId, abha_address: address })
              }
            >
              {t("abdm_claim_address")}
            </Button>
          )}
          {mode === "link" && linkStep === "identify" && (
            <Button
              type="button"
              disabled={busy || !loginIdValid}
              onClick={sendLoginOtp}
            >
              {t("abdm_send_otp")}
            </Button>
          )}
          {mode === "link" && linkStep === "otp" && (
            <Button
              type="button"
              disabled={busy || otp.length !== 6}
              onClick={() => loginVerify.mutate({ txn_id: txnId, otp })}
            >
              {t("abdm_verify")}
            </Button>
          )}
          {mode === "link" && linkStep === "accounts" && (
            <Button
              type="button"
              disabled={busy || !selected}
              onClick={() =>
                loginSelect.mutate({ txn_id: txnId, abha_number: selected })
              }
            >
              {t("abdm_use_account")}
            </Button>
          )}
          {done &&
            (customDone?.footer ?? (
              <Button
                type="button"
                disabled={finishing}
                onClick={() => onOpenChange(false)}
              >
                {t("abdm_close")}
              </Button>
            ))}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
