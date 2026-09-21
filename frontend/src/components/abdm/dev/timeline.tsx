import {
  STATE_TONE,
  formatMs,
  formatSeconds,
  formatTime,
} from "@/components/abdm/dev/dev-state";
import { Badge } from "@/components/ui/badge";
import { useTranslation } from "@/hooks/use-translation";
import type { AbdmDevExchange } from "@/lib/careApi";
import { cn } from "@/lib/utils";
import { ArrowRight, CircleDashed, Clock } from "lucide-react";

/**
 * 1 exchange as 3 stops: sent, the HTTP answer, the callback. Elapsed figures between them, and
 * the docs' state as the last word. A `no_answer` reads "nothing arrived in N min", never "failed"
 * (abdm-m2 design.md: "the honest words for the fifth outcome").
 */
export default function Timeline({
  exchange,
  windowSeconds,
  className,
}: {
  exchange: AbdmDevExchange;
  windowSeconds: number;
  className?: string;
}) {
  const { t } = useTranslation();
  const async = exchange.kind === "call";
  const stops: {
    key: string;
    label: string;
    when: string;
    done: boolean;
    elapsed?: string;
  }[] = [
    {
      key: "sent",
      label: t("abdm_dev_stop_sent"),
      when: formatTime(exchange.sentAt),
      done: true,
    },
    {
      key: "http",
      label:
        exchange.httpStatus !== null
          ? t("abdm_dev_stop_http", { status: exchange.httpStatus })
          : t("abdm_dev_stop_http_pending"),
      when: formatTime(exchange.completedAt),
      done: exchange.httpStatus !== null,
      elapsed: formatMs(exchange.httpMs),
    },
  ];
  if (async) {
    stops.push({
      key: "callback",
      label:
        exchange.callbacks > 0
          ? t("abdm_dev_stop_callback", { count: exchange.callbacks })
          : exchange.state === "no_answer"
            ? t("abdm_dev_stop_no_answer", {
                minutes: Math.round(windowSeconds / 60),
              })
            : exchange.state === "refused"
              ? t("abdm_dev_stop_never_pending")
              : t("abdm_dev_stop_waiting"),
      when: "",
      done: exchange.callbacks > 0,
      elapsed: formatSeconds(exchange.callbackSeconds),
    });
  }
  return (
    <div className={cn("grid gap-2", className)}>
      <ol className="flex flex-wrap items-center gap-x-2 gap-y-1 text-xs">
        {stops.map((stop, i) => (
          <li key={stop.key} className="flex items-center gap-2">
            {i > 0 && (
              <span className="text-muted-foreground flex items-center gap-1">
                <ArrowRight className="size-3" />
                <span className="font-mono tabular-nums">{stop.elapsed}</span>
                <ArrowRight className="size-3" />
              </span>
            )}
            <span
              className={cn(
                "flex items-center gap-1.5 rounded-md border px-2 py-1",
                stop.done ? "bg-card" : "text-muted-foreground border-dashed",
              )}
            >
              {stop.done ? (
                <Clock className="size-3" />
              ) : (
                <CircleDashed className="size-3" />
              )}
              <span>{stop.label}</span>
              {stop.when && (
                <span className="text-muted-foreground font-mono tabular-nums">
                  {stop.when}
                </span>
              )}
            </span>
          </li>
        ))}
        <li>
          <Badge variant={STATE_TONE[exchange.state]} size="sm">
            {t(`abdm_dev_state_${exchange.state}`)}
          </Badge>
        </li>
      </ol>
      {exchange.reason && (
        <p className="text-destructive text-xs [overflow-wrap:anywhere]">
          {exchange.reason}
          {exchange.errorSummary ? ` · ${exchange.errorSummary}` : ""}
        </p>
      )}
    </div>
  );
}
