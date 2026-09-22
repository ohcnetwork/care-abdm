import { Dot, Label, Status, Tool } from "@/components/abdm/dev/console";
import {
  KIND_TONE,
  MODULES,
  STATES,
  STATE_TONE,
  devKeys,
  formatDay,
  formatMs,
  formatSeconds,
  formatTime,
  httpTone,
  statePulse,
  toneText,
} from "@/components/abdm/dev/dev-state";
import { selectClass } from "@/components/abdm/nhpr-shared";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { useTranslation } from "@/hooks/use-translation";
import careApi, {
  type AbdmDevExchange,
  type AbdmDevExchangeList,
} from "@/lib/careApi";
import { query } from "@/lib/request";
import { cn } from "@/lib/utils";
import { useQuery } from "@tanstack/react-query";
import { ArrowDown, X } from "lucide-react";
import { useEffect, useMemo, useRef, useState } from "react";

/**
 * Every exchange as 1 row (abdm-m2 design.md: "an outbound call, the wait, and the callback that
 * answers it are one exchange, and they should read as one row with a timeline"). Newest first.
 *
 * The list polls every 5 s. New rows do not insert themselves while a person reads: a "N new
 * exchanges" button at the top merges them (the layout stays where it is). Filters live in the URL,
 * so a footer on an Encounter can open the list already narrowed. A typed filter reaches the URL
 * 300 ms after the last key, so a keystroke is not a history entry or a request.
 */

export type ExchangeFilters = {
  module?: string;
  operation?: string;
  state?: string;
  status?: string;
  facility?: string;
  patient?: string;
  encounter?: string;
  request_id?: string;
};

const FILTER_KEYS: (keyof ExchangeFilters)[] = [
  "module",
  "operation",
  "state",
  "status",
  "facility",
  "patient",
  "encounter",
  "request_id",
];

const TYPING_PAUSE_MS = 300;

function clean(filters: ExchangeFilters): Record<string, string> {
  return Object.fromEntries(
    FILTER_KEYS.filter((k) => filters[k]).map((k) => [k, String(filters[k])]),
  );
}

/**
 * A text filter as a draft: the input follows the keys at once; `commit` gets the trimmed text
 * after a pause. An outside change of `value` (the "Clear filters" button, Back) resets the draft.
 */
function useDraft(
  value: string | undefined,
  commit: (next: string) => void,
): [string, (next: string) => void] {
  const [draft, setDraft] = useState(value ?? "");
  const committed = useRef(value ?? "");
  const commitRef = useRef(commit);
  commitRef.current = commit;
  useEffect(() => {
    const outside = value ?? "";
    if (outside !== committed.current) {
      committed.current = outside;
      setDraft(outside);
    }
  }, [value]);
  useEffect(() => {
    const next = draft.trim();
    if (next === committed.current) return;
    const timer = setTimeout(() => {
      committed.current = next;
      commitRef.current(next);
    }, TYPING_PAUSE_MS);
    return () => clearTimeout(timer);
  }, [draft]);
  return [draft, setDraft];
}

export function StateBadge({
  state,
  className,
}: {
  state: AbdmDevExchange["state"];
  className?: string;
}) {
  const { t } = useTranslation();
  return (
    <Status
      tone={STATE_TONE[state]}
      pulse={statePulse(state)}
      hollow={state === "no_answer"}
      className={className}
    >
      {t(`abdm_dev_state_${state}`)}
    </Status>
  );
}

export default function ExchangeList({
  filters,
  onFilters,
  onOpen,
  selected,
  embedded = false,
  limit = 50,
}: {
  filters: ExchangeFilters;
  onFilters?: (next: ExchangeFilters) => void;
  onOpen: (requestId: string) => void;
  selected?: string;
  /** Inside a footer: no filter bar, no polling button row, a short list. */
  embedded?: boolean;
  limit?: number;
}) {
  const { t } = useTranslation();
  const params = useMemo(
    () => ({ ...clean(filters), limit: String(limit) }),
    [filters, limit],
  );
  // Filters by value: `filters` is a new object on every parent render.
  const paramsKey = new URLSearchParams(params).toString();
  const live = useQuery<AbdmDevExchangeList>({
    queryKey: devKeys.exchanges(params),
    queryFn: query(careApi.devExchanges, { queryParams: params, silent: true }),
    refetchInterval: 5000,
    retry: false,
  });
  // What the person sees. It follows `live` only when the person asks, when the filters change, or
  // when nothing is shown yet.
  const [shown, setShown] = useState<AbdmDevExchangeList | null>(null);
  const [keyShown, setKeyShown] = useState(paramsKey);
  useEffect(() => {
    if (!live.data) return;
    if (shown === null || keyShown !== paramsKey) {
      setShown(live.data);
      setKeyShown(paramsKey);
    }
  }, [live.data, shown, paramsKey, keyShown]);
  const fresh = live.data && shown && live.data !== shown ? live.data : null;
  const shownIds = useMemo(
    () => new Set(shown?.rows.map((r) => r.requestId) ?? []),
    [shown],
  );
  const newCount = fresh
    ? fresh.rows.filter((r) => !shownIds.has(r.requestId)).length
    : 0;
  // A row already shown may have changed state (a callback landed): update it in place.
  const rows = useMemo(() => {
    if (!shown) return [];
    if (!fresh) return shown.rows;
    const byId = new Map(fresh.rows.map((r) => [r.requestId, r]));
    return shown.rows.map((r) => byId.get(r.requestId) ?? r);
  }, [shown, fresh]);
  const set = (key: keyof ExchangeFilters, value: string) =>
    onFilters?.({ ...filters, [key]: value || undefined });
  const [operationDraft, setOperationDraft] = useDraft(
    filters.operation,
    (next) => set("operation", next),
  );
  const [requestIdDraft, setRequestIdDraft] = useDraft(
    filters.request_id,
    (next) => set("request_id", next),
  );
  const active = FILTER_KEYS.filter((k) => filters[k]);

  return (
    <div className="grid min-w-0 gap-4">
      {!embedded && onFilters && (
        <div className="flex flex-wrap items-end gap-3">
          <label className="grid gap-1">
            <Label>{t("abdm_dev_module")}</Label>
            <select
              className={cn(selectClass, "h-8 w-28 font-mono text-xs md:h-8")}
              value={filters.module ?? ""}
              onChange={(e) => set("module", e.target.value)}
            >
              <option value="">{t("abdm_dev_any")}</option>
              {MODULES.map((m) => (
                <option key={m} value={m}>
                  {m}
                </option>
              ))}
            </select>
          </label>
          <label className="grid gap-1">
            <Label>{t("abdm_dev_state")}</Label>
            <select
              className={cn(selectClass, "h-8 w-44 font-mono text-xs md:h-8")}
              value={filters.state ?? ""}
              onChange={(e) => set("state", e.target.value)}
            >
              <option value="">{t("abdm_dev_any")}</option>
              {STATES.map((s) => (
                <option key={s} value={s}>
                  {t(`abdm_dev_state_${s}`)}
                </option>
              ))}
            </select>
          </label>
          <label className="grid gap-1">
            <Label>{t("abdm_dev_operation")}</Label>
            <Input
              data-console-search
              className="h-8 w-56 font-mono text-xs md:h-8"
              placeholder="m2-generate-link-token"
              value={operationDraft}
              onChange={(e) => setOperationDraft(e.target.value)}
            />
          </label>
          <label className="grid gap-1">
            <Label>REQUEST-ID</Label>
            <Input
              className="h-8 w-64 font-mono text-xs md:h-8"
              placeholder="0a194641-…"
              value={requestIdDraft}
              onChange={(e) => setRequestIdDraft(e.target.value)}
            />
          </label>
          {active.length > 0 && (
            <Tool className="h-8 px-2 text-xs" onClick={() => onFilters({})}>
              <X className="size-3.5" /> {t("abdm_dev_clear_filters")}
            </Tool>
          )}
          <span className="text-muted-foreground ml-auto flex h-8 items-center gap-1.5 text-[11px]">
            <Dot tone={live.isFetching ? "primary" : "success"} pulse />
            {t("abdm_dev_polling")}
          </span>
        </div>
      )}
      {(filters.facility || filters.patient || filters.encounter) &&
        !embedded && (
          <div className="flex flex-wrap gap-1 text-xs">
            {(["facility", "patient", "encounter"] as const)
              .filter((k) => filters[k])
              .map((k) => (
                <Badge
                  key={k}
                  variant="neutral"
                  size="sm"
                  className="font-mono"
                >
                  {t(`abdm_dev_scope_${k}`)} {String(filters[k]).slice(0, 8)}…
                  {onFilters && (
                    <button
                      type="button"
                      aria-label={t("abdm_dev_clear_filters")}
                      onClick={() => set(k, "")}
                    >
                      <X className="size-3" />
                    </button>
                  )}
                </Badge>
              ))}
          </div>
        )}

      {/* New rows wait here until asked for: no layout shift under a reader. */}
      <div className="min-h-8">
        {newCount > 0 && fresh && (
          <Button
            type="button"
            variant="outline"
            size="sm"
            className="h-8 font-mono text-xs"
            onClick={() => setShown(fresh)}
          >
            <ArrowDown className="size-3.5" />{" "}
            {t("abdm_dev_new_rows", { count: newCount })}
          </Button>
        )}
      </div>

      {live.isLoading && !shown && (
        <Skeleton className="h-40 w-full rounded-md" />
      )}
      {live.isError && (
        <p className="text-destructive text-xs">{t("abdm_dev_load_failed")}</p>
      )}
      {shown && rows.length === 0 && (
        <p className="text-muted-foreground text-xs">
          {t("abdm_dev_no_exchanges")}
        </p>
      )}
      {rows.length > 0 && (
        <div className="overflow-x-auto rounded-md border">
          <table className="w-full border-collapse text-xs">
            <thead>
              <tr className="border-b bg-white/[0.03] text-left">
                <th className="px-3 py-2 font-normal">
                  <Label>{t("abdm_dev_when")}</Label>
                </th>
                <th className="px-3 py-2 font-normal">
                  <Label>{t("abdm_dev_module")}</Label>
                </th>
                <th className="px-3 py-2 font-normal">
                  <Label>{t("abdm_dev_exchange")}</Label>
                </th>
                <th className="px-3 py-2 font-normal">
                  <Label>{t("abdm_dev_state")}</Label>
                </th>
                <th className="px-3 py-2 text-right font-normal">
                  <Label>HTTP</Label>
                </th>
                <th className="px-3 py-2 text-right font-normal">
                  <Label>{t("abdm_dev_callback")}</Label>
                </th>
                {!embedded && (
                  <th className="px-3 py-2 font-normal">
                    <Label>REQUEST-ID</Label>
                  </th>
                )}
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => (
                <tr
                  key={r.requestId}
                  aria-selected={selected === r.requestId || undefined}
                  className={cn(
                    "cursor-pointer border-b border-white/[0.06] align-top last:border-b-0 hover:bg-white/[0.04]",
                    selected === r.requestId &&
                      "bg-primary/10 shadow-[inset_2px_0_0_0_var(--primary)]",
                  )}
                  onClick={() => onOpen(r.requestId)}
                >
                  <td className="text-muted-foreground px-3 py-2.5 whitespace-nowrap tabular-nums">
                    <div className="grid leading-4">
                      <span className="text-foreground">
                        {formatTime(r.sentAt)}
                      </span>
                      <span className="text-[10.5px]">
                        {formatDay(r.sentAt)}
                      </span>
                    </div>
                  </td>
                  <td className="px-3 py-2.5 whitespace-nowrap">
                    <div className="grid leading-4">
                      <span className="text-muted-foreground">{r.module}</span>
                      <span
                        className={cn(
                          "text-[10.5px]",
                          toneText(KIND_TONE[r.kind]),
                        )}
                      >
                        {t(`abdm_dev_kind_${r.kind}`)}
                      </span>
                    </div>
                  </td>
                  <td className="min-w-0 px-3 py-2.5">
                    <div className="grid gap-1 leading-4">
                      <span className="text-foreground [overflow-wrap:anywhere]">
                        {r.operationId}
                      </span>
                      <span className="text-muted-foreground text-[10.5px] [overflow-wrap:anywhere]">
                        <span className="text-foreground/80">{r.method}</span>{" "}
                        {r.path}
                        {r.facility ? ` · ${r.facility.label}` : ""}
                      </span>
                      {r.errorSummary && (
                        <span className="[overflow-wrap:anywhere] text-red-300">
                          {r.errorSummary}
                        </span>
                      )}
                    </div>
                  </td>
                  <td className="px-3 py-2.5 whitespace-nowrap">
                    <StateBadge state={r.state} />
                  </td>
                  <td className="px-3 py-2.5 text-right whitespace-nowrap tabular-nums">
                    <div className="grid leading-4">
                      <span className={toneText(httpTone(r.httpStatus))}>
                        {r.httpStatus ?? "—"}
                      </span>
                      <span className="text-muted-foreground text-[10.5px]">
                        {formatMs(r.httpMs)}
                      </span>
                    </div>
                  </td>
                  <td className="px-3 py-2.5 text-right whitespace-nowrap tabular-nums">
                    {r.kind === "call" ? (
                      <div className="grid leading-4">
                        <span>{r.callbacks > 0 ? `${r.callbacks}×` : "—"}</span>
                        <span className="text-muted-foreground text-[10.5px]">
                          {formatSeconds(r.callbackSeconds)}
                        </span>
                      </div>
                    ) : (
                      <span className="text-muted-foreground">—</span>
                    )}
                  </td>
                  {!embedded && (
                    <td className="text-muted-foreground px-3 py-2.5 text-[11px] select-all">
                      {r.requestId}
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {shown?.more && !embedded && (
        <p className="text-muted-foreground text-xs">
          {t("abdm_dev_more_rows", { count: limit })}
        </p>
      )}
    </div>
  );
}
