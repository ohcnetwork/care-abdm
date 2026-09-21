import {
  KIND_TONE,
  MODULES,
  STATES,
  STATE_TONE,
  devKeys,
  formatMs,
  formatSeconds,
  formatWhen,
} from "@/components/abdm/dev/dev-state";
import { selectClass } from "@/components/abdm/nhpr-shared";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useTranslation } from "@/hooks/use-translation";
import careApi, {
  type AbdmDevExchange,
  type AbdmDevExchangeList,
} from "@/lib/careApi";
import { query } from "@/lib/request";
import { cn } from "@/lib/utils";
import { useQuery } from "@tanstack/react-query";
import { ArrowDown, Loader2, RefreshCw, X } from "lucide-react";
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

export function StateBadge({ state }: { state: AbdmDevExchange["state"] }) {
  const { t } = useTranslation();
  return (
    <Badge variant={STATE_TONE[state]} size="sm">
      {t(`abdm_dev_state_${state}`)}
    </Badge>
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
    <div className="grid min-w-0 gap-3">
      {!embedded && onFilters && (
        <div className="flex flex-wrap items-end gap-2">
          <label className="grid gap-1 text-xs">
            <span className="text-muted-foreground">
              {t("abdm_dev_module")}
            </span>
            <select
              className={cn(selectClass, "h-8 w-32 md:h-8")}
              value={filters.module ?? ""}
              onChange={(e) => set("module", e.target.value)}
            >
              <option value="">{t("abdm_dev_any")}</option>
              {MODULES.map((m) => (
                <option key={m} value={m}>
                  {m.toUpperCase()}
                </option>
              ))}
            </select>
          </label>
          <label className="grid gap-1 text-xs">
            <span className="text-muted-foreground">{t("abdm_dev_state")}</span>
            <select
              className={cn(selectClass, "h-8 w-44 md:h-8")}
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
          <label className="grid gap-1 text-xs">
            <span className="text-muted-foreground">
              {t("abdm_dev_operation")}
            </span>
            <Input
              className="h-8 w-56 font-mono text-xs md:h-8"
              placeholder="m2-generate-link-token"
              value={operationDraft}
              onChange={(e) => setOperationDraft(e.target.value)}
            />
          </label>
          <label className="grid gap-1 text-xs">
            <span className="text-muted-foreground">REQUEST-ID</span>
            <Input
              className="h-8 w-64 font-mono text-xs md:h-8"
              placeholder="0a194641-…"
              value={requestIdDraft}
              onChange={(e) => setRequestIdDraft(e.target.value)}
            />
          </label>
          {active.length > 0 && (
            <Button
              type="button"
              variant="ghost"
              size="sm"
              className="h-8"
              onClick={() => onFilters({})}
            >
              <X className="size-3.5" /> {t("abdm_dev_clear_filters")}
            </Button>
          )}
          <span className="text-muted-foreground ml-auto flex items-center gap-1 text-xs">
            {live.isFetching ? (
              <Loader2 className="size-3 animate-spin" />
            ) : (
              <RefreshCw className="size-3" />
            )}
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
            className="h-8"
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
        <p className="text-muted-foreground text-sm">
          {t("abdm_dev_no_exchanges")}
        </p>
      )}
      {rows.length > 0 && (
        <div className="overflow-x-auto rounded-md border">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead className="w-28">{t("abdm_dev_when")}</TableHead>
                <TableHead>{t("abdm_dev_exchange")}</TableHead>
                <TableHead className="w-36">{t("abdm_dev_state")}</TableHead>
                <TableHead className="w-24 text-right">HTTP</TableHead>
                <TableHead className="w-28 text-right">
                  {t("abdm_dev_callback")}
                </TableHead>
                {!embedded && (
                  <TableHead className="w-72">REQUEST-ID</TableHead>
                )}
              </TableRow>
            </TableHeader>
            <TableBody>
              {rows.map((r) => (
                <TableRow
                  key={r.requestId}
                  data-state={selected === r.requestId ? "selected" : undefined}
                  className={cn(
                    "cursor-pointer",
                    selected === r.requestId && "bg-muted/60",
                  )}
                  onClick={() => onOpen(r.requestId)}
                >
                  <TableCell className="text-muted-foreground font-mono text-xs whitespace-nowrap tabular-nums">
                    {formatWhen(r.sentAt)}
                  </TableCell>
                  <TableCell className="min-w-0">
                    <div className="grid gap-0.5">
                      <div className="flex flex-wrap items-center gap-1.5">
                        <Badge
                          variant="neutral"
                          size="sm"
                          className="font-mono uppercase"
                        >
                          {r.module}
                        </Badge>
                        <Badge variant={KIND_TONE[r.kind]} size="sm">
                          {t(`abdm_dev_kind_${r.kind}`)}
                        </Badge>
                        <span className="font-mono text-xs">
                          {r.operationId}
                        </span>
                      </div>
                      <span className="text-muted-foreground font-mono text-[11px] [overflow-wrap:anywhere]">
                        {r.method} {r.path}
                        {r.facility ? ` · ${r.facility.label}` : ""}
                      </span>
                      {r.errorSummary && (
                        <span className="text-destructive text-xs [overflow-wrap:anywhere]">
                          {r.errorSummary}
                        </span>
                      )}
                    </div>
                  </TableCell>
                  <TableCell>
                    <StateBadge state={r.state} />
                  </TableCell>
                  <TableCell className="text-right font-mono text-xs tabular-nums">
                    <div className="grid">
                      <span
                        className={cn(
                          r.httpStatus &&
                            r.httpStatus >= 400 &&
                            "text-destructive",
                        )}
                      >
                        {r.httpStatus ?? "—"}
                      </span>
                      <span className="text-muted-foreground">
                        {formatMs(r.httpMs)}
                      </span>
                    </div>
                  </TableCell>
                  <TableCell className="text-right font-mono text-xs tabular-nums">
                    {r.kind === "call" ? (
                      <div className="grid">
                        <span>{r.callbacks > 0 ? `${r.callbacks}×` : "—"}</span>
                        <span className="text-muted-foreground">
                          {formatSeconds(r.callbackSeconds)}
                        </span>
                      </div>
                    ) : (
                      <span className="text-muted-foreground">—</span>
                    )}
                  </TableCell>
                  {!embedded && (
                    <TableCell className="font-mono text-[11px] select-all">
                      {r.requestId}
                    </TableCell>
                  )}
                </TableRow>
              ))}
            </TableBody>
          </Table>
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
