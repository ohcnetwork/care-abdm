import { Label, NextStep, Status } from "@/components/abdm/dev/console";
import {
  CHECK_TONE,
  devKeys,
  formatWhen,
} from "@/components/abdm/dev/dev-state";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useTranslation } from "@/hooks/use-translation";
import careApi, {
  type AbdmDevCheck,
  type AbdmDevReadiness,
} from "@/lib/careApi";
import { query } from "@/lib/request";
import { useQuery } from "@tanstack/react-query";
import {
  AlertTriangle,
  CheckCircle2,
  Loader2,
  OctagonX,
  RefreshCw,
} from "lucide-react";

/**
 * The readiness check (abdm-m2 design.md: "A readiness check that names what is missing"). 8 rows,
 * each ok, warning or blocker, with what is wrong and the next step in the backend's words. A next
 * step with a command in backticks renders as a command block with its copy button. The overall
 * word is the worst row. A refresh makes 1 live gateway call (the bridge read).
 */

const ICON = {
  ok: CheckCircle2,
  warning: AlertTriangle,
  blocker: OctagonX,
} as const;

const MARK: Record<"ok" | "warning" | "blocker", string> = {
  ok: "[ ok ]",
  warning: "[ !! ]",
  blocker: "[FAIL]",
};

function Extra({ check }: { check: AbdmDevCheck }) {
  const { t } = useTranslation();
  const facilities = check.facilities as
    { name: string; facilityId: string; hipId: string }[] | undefined;
  if (facilities?.length) {
    return (
      <ul className="grid gap-0.5 font-mono text-[11px]">
        {facilities.map((f) => (
          <li key={f.facilityId} className="flex flex-wrap gap-2">
            <span>{f.name}</span>
            <span className="text-muted-foreground">{f.facilityId}</span>
            <span className={f.hipId ? "" : "text-destructive"}>
              {f.hipId || t("abdm_dev_no_hip_id")}
            </span>
          </li>
        ))}
      </ul>
    );
  }
  const values = check.values as Record<string, boolean> | undefined;
  if (values) {
    return (
      <ul className="flex flex-wrap gap-x-4 gap-y-1 text-[11px]">
        {Object.entries(values).map(([name, set]) => (
          <li key={name}>
            <Status tone={set ? "success" : "destructive"}>ABDM_{name}</Status>
          </li>
        ))}
      </ul>
    );
  }
  const parts: string[] = [];
  for (const key of [
    "live",
    "expected",
    "lastSeen",
    "lastOutboundAt",
    "lastCallbackAt",
    "requestId",
  ] as const) {
    const v = check[key];
    if (typeof v === "string" && v)
      parts.push(
        `${key}: ${/^\d{4}-\d{2}-\d{2}T/.test(v) ? formatWhen(v) : v}`,
      );
  }
  for (const key of [
    "callbacksQueued",
    "outboundTotal",
    "callbackTotal",
  ] as const) {
    const v = check[key];
    if (typeof v === "number") parts.push(`${key}: ${v}`);
  }
  if (!parts.length) return null;
  return (
    <p className="text-muted-foreground font-mono text-[11px] [overflow-wrap:anywhere]">
      {parts.join(" · ")}
    </p>
  );
}

export default function ReadinessCard() {
  const { t } = useTranslation();
  const readiness = useQuery<AbdmDevReadiness>({
    queryKey: devKeys.readiness,
    queryFn: query(careApi.devReadiness, { silent: true }),
    refetchInterval: 30000,
    retry: false,
  });
  const d = readiness.data;
  return (
    <div className="grid min-w-0 gap-3 text-xs">
      <div className="flex flex-wrap items-center gap-3">
        <span className="text-sm">{t("abdm_dev_readiness_title")}</span>
        {d && (
          <Status tone={CHECK_TONE[d.status]}>
            {t(`abdm_dev_check_${d.status}`)}
          </Status>
        )}
        <Button
          type="button"
          variant="ghost"
          size="sm"
          className="ml-auto h-7 px-2 font-mono text-xs"
          onClick={() => readiness.refetch()}
          disabled={readiness.isFetching}
          aria-label={t("abdm_dev_refresh")}
        >
          {readiness.isFetching ? (
            <Loader2 className="size-3.5 animate-spin" />
          ) : (
            <RefreshCw className="size-3.5" />
          )}
          {t("abdm_dev_refresh")}
        </Button>
      </div>
      <p className="text-muted-foreground flex items-start gap-2 leading-5">
        <span aria-hidden className="select-none">
          →
        </span>
        <span className="min-w-0 [overflow-wrap:anywhere]">
          {t("abdm_dev_readiness_intro")}
        </span>
      </p>
      {readiness.isLoading && <Skeleton className="h-48 w-full rounded-md" />}
      {readiness.isError && (
        <p className="text-destructive">{t("abdm_dev_load_failed")}</p>
      )}
      {d && (
        <>
          <ul className="grid gap-px overflow-hidden rounded-md border">
            {d.checks.map((check) => {
              const Icon = ICON[check.status];
              return (
                <li
                  key={check.id}
                  className="grid gap-2 border-b bg-black/10 p-3 last:border-b-0"
                >
                  <div className="flex items-start gap-3">
                    <span
                      className={
                        check.status === "ok"
                          ? "text-emerald-300"
                          : check.status === "warning"
                            ? "text-amber-300"
                            : "text-red-300"
                      }
                    >
                      <span className="hidden tabular-nums sm:inline">
                        {MARK[check.status]}
                      </span>
                      <Icon className="size-3.5 sm:hidden" />
                    </span>
                    <div className="grid min-w-0 flex-1 gap-1">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="text-foreground">
                          {t(`abdm_dev_check_id_${check.id}`)}
                        </span>
                        <Status
                          tone={CHECK_TONE[check.status]}
                          className="text-[11px]"
                        >
                          {t(`abdm_dev_check_${check.status}`)}
                        </Status>
                      </div>
                      <p className="[overflow-wrap:anywhere]">{check.what}</p>
                      {check.nextStep && <NextStep text={check.nextStep} />}
                      <Extra check={check} />
                    </div>
                  </div>
                </li>
              );
            })}
          </ul>
          <p className="text-muted-foreground text-[11px] [overflow-wrap:anywhere]">
            <Label>{t("abdm_dev_checked_at")}</Label> {formatWhen(d.checkedAt)}{" "}
            · gateway {d.hosts.gateway} · abha {d.hosts.abha} · hsp{" "}
            {d.hosts.hsp} · X-CM-ID {d.hosts.cmId} · callback{" "}
            {d.hosts.callbackBase || "—"}
          </p>
        </>
      )}
    </div>
  );
}
