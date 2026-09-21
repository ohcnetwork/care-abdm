import {
  CHECK_TONE,
  devKeys,
  formatWhen,
} from "@/components/abdm/dev/dev-state";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
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
 * each ok, warning or blocker, with what is wrong and the next step in the backend's words. The
 * overall badge is the worst row. A refresh makes 1 live gateway call (the bridge read).
 */

const ICON = {
  ok: CheckCircle2,
  warning: AlertTriangle,
  blocker: OctagonX,
} as const;

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
      <ul className="flex flex-wrap gap-1">
        {Object.entries(values).map(([name, set]) => (
          <li key={name}>
            <Badge
              variant={set ? "success" : "destructive"}
              size="sm"
              className="font-mono"
            >
              ABDM_{name}
            </Badge>
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
    <Card>
      <CardHeader>
        <CardTitle className="flex flex-wrap items-center gap-2">
          {t("abdm_dev_readiness_title")}
          {d && (
            <Badge variant={CHECK_TONE[d.status]} size="sm" className="ml-auto">
              {t(`abdm_dev_check_${d.status}`)}
            </Badge>
          )}
          <Button
            type="button"
            variant="ghost"
            size="sm"
            className="h-7 px-2"
            onClick={() => readiness.refetch()}
            disabled={readiness.isFetching}
            aria-label={t("abdm_dev_refresh")}
          >
            {readiness.isFetching ? (
              <Loader2 className="size-3.5 animate-spin" />
            ) : (
              <RefreshCw className="size-3.5" />
            )}
          </Button>
        </CardTitle>
        <CardDescription>{t("abdm_dev_readiness_intro")}</CardDescription>
      </CardHeader>
      <CardContent className="grid gap-3">
        {readiness.isLoading && <Skeleton className="h-48 w-full rounded-md" />}
        {readiness.isError && (
          <p className="text-destructive text-sm">
            {t("abdm_dev_load_failed")}
          </p>
        )}
        {d && (
          <>
            <ul className="grid gap-2">
              {d.checks.map((check) => {
                const Icon = ICON[check.status];
                return (
                  <li
                    key={check.id}
                    className="grid gap-1 rounded-md border p-3"
                  >
                    <div className="flex items-start gap-2">
                      <Icon
                        className={
                          check.status === "ok"
                            ? "mt-0.5 size-4 shrink-0 text-emerald-600"
                            : check.status === "warning"
                              ? "mt-0.5 size-4 shrink-0 text-amber-600"
                              : "text-destructive mt-0.5 size-4 shrink-0"
                        }
                      />
                      <div className="grid min-w-0 flex-1 gap-0.5">
                        <div className="flex flex-wrap items-center gap-2">
                          <span className="text-sm font-medium">
                            {t(`abdm_dev_check_id_${check.id}`)}
                          </span>
                          <Badge variant={CHECK_TONE[check.status]} size="sm">
                            {t(`abdm_dev_check_${check.status}`)}
                          </Badge>
                        </div>
                        <p className="text-sm [overflow-wrap:anywhere]">
                          {check.what}
                        </p>
                        {check.nextStep && (
                          <p className="text-muted-foreground text-xs [overflow-wrap:anywhere]">
                            {check.nextStep}
                          </p>
                        )}
                        <Extra check={check} />
                      </div>
                    </div>
                  </li>
                );
              })}
            </ul>
            <p className="text-muted-foreground font-mono text-[11px] [overflow-wrap:anywhere]">
              {t("abdm_dev_checked_at")} {formatWhen(d.checkedAt)} · gateway{" "}
              {d.hosts.gateway} · abha {d.hosts.abha} · hsp {d.hosts.hsp} ·
              X-CM-ID {d.hosts.cmId} · callback {d.hosts.callbackBase || "—"}
            </p>
          </>
        )}
      </CardContent>
    </Card>
  );
}
