import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { useTranslation } from "@/hooks/use-translation";
import type { FailureNoticeProps } from "@/components/abdm/failure-notice-shared";
import { cn } from "@/lib/utils";
import { AlertCircle } from "lucide-react";

/**
 * 1 refused call, as the person should read it (abdm-m3 design.md: carry ABDM's own message
 * through; abdm-m2 design.md: 1 exchange, 1 row, the request id as the join key).
 *
 * - `lines`: the registry's own words, 1 bullet each. A long unbroken token (the registry writes
 *   `beds(countIPDBedsWithoutOxygen,…)`) wraps inside the box: `min-w-0` and `overflow-wrap:
 *   anywhere` keep the page width stable.
 * - `title`: the plug sentence when the registry sent no words (a transport failure).
 * - `code` and `requestId`: 1 footer row for support. The id is monospace and selects whole.
 */
export default function FailureNotice({
  title,
  lines = [],
  code,
  requestId,
  className,
}: FailureNoticeProps) {
  const { t } = useTranslation();
  const heading = title || (lines.length ? t("abdm_refused_title") : "");
  if (!heading && !lines.length) return null;
  return (
    <Alert
      variant="destructive"
      className={cn("min-w-0 overflow-hidden", className)}
    >
      <AlertCircle />
      {heading && <AlertTitle className="min-w-0">{heading}</AlertTitle>}
      <AlertDescription className="grid min-w-0 gap-1.5 text-start">
        {lines.length > 0 && (
          <ul
            className={cn(
              "grid gap-1 [overflow-wrap:anywhere] break-words",
              lines.length > 1 && "list-disc pl-4",
            )}
          >
            {lines.map((line, i) => (
              <li key={i}>{line}</li>
            ))}
          </ul>
        )}
        {(code || requestId) && (
          <span className="text-muted-foreground flex flex-wrap items-center gap-2 text-xs">
            {code && (
              <Badge variant="neutral" size="sm" className="font-mono">
                {code}
              </Badge>
            )}
            {requestId && (
              <span className="[overflow-wrap:anywhere]">
                {t("abdm_refused_reference")}{" "}
                <span className="font-mono select-all">{requestId}</span>
              </span>
            )}
          </span>
        )}
      </AlertDescription>
    </Alert>
  );
}
