import { Dot, Status } from "@/components/abdm/dev/console";
import {
  STATE_TONE,
  formatMs,
  formatSeconds,
  formatTime,
  statePulse,
} from "@/components/abdm/dev/dev-state";
import { useTranslation } from "@/hooks/use-translation";
import type { AbdmDevExchange } from "@/lib/careApi";
import { cn } from "@/lib/utils";

/**
 * 1 exchange as a rail of stops: sent, the HTTP answer, the callback. The elapsed figure sits on
 * the line between 2 stops; the docs' state is the last word. A `no_answer` reads "nothing arrived
 * in N min", never "failed" (abdm-m2 design.md: "the honest words for the fifth outcome").
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
  const pending = statePulse(exchange.state);
  return (
    <div className={cn("grid gap-2", className)}>
      <ol className="flex flex-wrap items-start gap-y-4 text-xs">
        {stops.map((stop, i) => (
          <li key={stop.key} className="flex min-w-0 items-start">
            {i > 0 && (
              <span
                aria-hidden
                className="text-muted-foreground mt-[3px] flex w-20 shrink-0 flex-col items-center gap-0.5 sm:w-24"
              >
                <span
                  className={cn(
                    "h-px w-full",
                    stop.done ? "bg-strong-border" : "bg-white/10",
                  )}
                  style={
                    stop.done
                      ? undefined
                      : {
                          backgroundImage:
                            "repeating-linear-gradient(90deg, currentColor 0 4px, transparent 4px 8px)",
                          backgroundColor: "transparent",
                        }
                  }
                />
                <span className="text-[10.5px] tabular-nums">
                  {stop.elapsed}
                </span>
              </span>
            )}
            <span className="grid min-w-0 gap-0.5">
              <span className="flex items-center gap-1.5">
                <Dot
                  tone={stop.done ? "success" : "neutral"}
                  hollow={!stop.done}
                  pulse={!stop.done && pending}
                />
                <span
                  className={cn(
                    "[overflow-wrap:anywhere]",
                    !stop.done && "text-muted-foreground",
                  )}
                >
                  {stop.label}
                </span>
              </span>
              {stop.when && (
                <span className="text-muted-foreground pl-3 text-[10.5px] tabular-nums">
                  {stop.when}
                </span>
              )}
            </span>
          </li>
        ))}
        <li className="ml-auto pl-3">
          <Status
            tone={STATE_TONE[exchange.state]}
            pulse={pending}
            hollow={exchange.state === "no_answer"}
          >
            {t(`abdm_dev_state_${exchange.state}`)}
          </Status>
        </li>
      </ol>
      {exchange.reason && (
        <p className="text-xs [overflow-wrap:anywhere] text-red-300">
          {exchange.reason}
          {exchange.errorSummary ? ` · ${exchange.errorSummary}` : ""}
        </p>
      )}
    </div>
  );
}
