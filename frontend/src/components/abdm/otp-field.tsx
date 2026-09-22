import { Button } from "@/components/ui/button";
import {
  InputOTP,
  InputOTPGroup,
  InputOTPSlot,
} from "@/components/ui/input-otp";
import { useTranslation } from "@/hooks/use-translation";
import { useEffect, useState } from "react";

/**
 * Shared OTP entry for every ABDM flow (ABHA enrol/login, HPR login, HPID
 * creation, HFR facility OTP). All ABDM OTPs are 6 numeric digits, so the
 * slotted Care UI `input-otp` is the single entry widget — do not hand-roll a
 * plain `Input` for an OTP.
 */
export function OtpField({
  value,
  onChange,
  onEnter,
  autoFocus,
  disabled,
  length = 6,
  className,
  containerClassName = "justify-center",
}: {
  value: string;
  onChange: (v: string) => void;
  onEnter?: () => void;
  autoFocus?: boolean;
  disabled?: boolean;
  length?: number;
  className?: string;
  containerClassName?: string;
}) {
  return (
    <InputOTP
      maxLength={length}
      value={value}
      onChange={(v) => onChange(v.replace(/\D/g, ""))}
      autoFocus={autoFocus}
      disabled={disabled}
      onKeyDown={(e) => {
        if (e.key === "Enter" && value.length === length) onEnter?.();
      }}
      containerClassName={containerClassName}
      className={className}
    >
      <InputOTPGroup>
        {Array.from({ length }, (_, i) => (
          <InputOTPSlot key={i} index={i} className="size-11 text-lg" />
        ))}
      </InputOTPGroup>
    </InputOTP>
  );
}

export function ResendTimer({
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
