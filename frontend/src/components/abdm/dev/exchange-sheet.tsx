import {
  CopyButton,
  Label,
  Pairs,
  Status,
  TabStrip,
} from "@/components/abdm/dev/console";
import {
  CONSOLE_CLASS,
  EXCHANGE_VIEWS,
  STATE_TONE,
  devKeys,
  formatMs,
  formatSeconds,
  formatTime,
  formatWhen,
  httpReason,
  httpTone,
  isExchangeView,
  statePulse,
  toneText,
  type ExchangeView,
} from "@/components/abdm/dev/dev-state";
import JsonTree from "@/components/abdm/dev/json-tree";
import Timeline from "@/components/abdm/dev/timeline";
import FailureNotice from "@/components/abdm/failure-notice";
import { noticeFromFailure } from "@/components/abdm/failure-notice-shared";
import { Badge } from "@/components/ui/badge";
import {
  Sheet,
  SheetBody,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { Skeleton } from "@/components/ui/skeleton";
import { useTranslation } from "@/hooks/use-translation";
import careApi, {
  type AbdmDevCallback,
  type AbdmDevExchangeDetail,
  type AbdmDevRowRef,
} from "@/lib/careApi";
import { query } from "@/lib/request";
import { useQuery } from "@tanstack/react-query";
import { Link } from "raviger";
import { useState } from "react";

/**
 * 1 exchange in full, in a side sheet over the list (the list keeps its place). The sheet is a
 * console panel (`CONSOLE_CLASS` on its content: a portal sits outside the page wrapper) laid out
 * like a browser's network inspector, 5 views under a tab strip:
 *
 * - General — the ADR-012 failure notice when refused; `Request URL`, method, status code with its
 *   reason phrase, operation, REQUEST-ID; what happened when (sent, HTTP answer, first callback)
 *   and the timeline rail; scope; request headers and answer headers (values are lengths).
 * - Request — the query string, then the body tree.
 * - Response — the status line and the body tree; for a `call`, the reminder that a 202 is the
 *   gateway's acceptance and the answer is the callback.
 * - Callbacks — every callback (`CallbackBlock`, with its own small strip: headers, body,
 *   traceback, rows), the inbound this exchange answers first.
 * - Rows — the plug rows that name this exchange.
 *
 * The view is the caller's state when `view`/`onView` are given (the explorer keeps it in the URL,
 * so a link can point at a response); otherwise the sheet keeps it. It survives a move to another
 * exchange, as an inspector's tab does. Keys 1–5 switch the view when no field has the focus.
 */

export function HeaderList({
  headers,
}: {
  headers: Record<string, string | number>;
}) {
  const entries = Object.entries(headers ?? {});
  return (
    <Pairs
      entries={entries.map(([name, value]) => [
        name,
        typeof value === "number" ? (
          <span className="text-muted-foreground">
            {"<"}
            {value} chars{">"}
          </span>
        ) : (
          <span className="[overflow-wrap:anywhere]">{value}</span>
        ),
      ])}
    />
  );
}

export function RowRefs({
  rows,
  onTable,
}: {
  rows: AbdmDevRowRef[];
  onTable?: (table: string, id: string) => void;
}) {
  const { t } = useTranslation();
  if (!rows.length)
    return (
      <span className="text-muted-foreground text-xs">
        {t("abdm_dev_no_rows")}
      </span>
    );
  return (
    <ul className="flex flex-wrap gap-1">
      {rows.map((r, i) => (
        <li key={`${r.field}-${r.id}-${i}`}>
          {r.table && onTable ? (
            <button
              type="button"
              onClick={() => onTable(r.table as string, r.id)}
            >
              <Badge
                variant="info"
                size="sm"
                className="cursor-pointer font-mono"
              >
                {r.table}.{r.field}
                <span className="text-muted-foreground"> · {r.label}</span>
              </Badge>
            </button>
          ) : (
            <Badge variant="neutral" size="sm" className="font-mono">
              {r.kind ?? r.table}.{r.field}
              <span className="text-muted-foreground"> · {r.label}</span>
            </Badge>
          )}
        </li>
      ))}
    </ul>
  );
}

type CallbackView = "headers" | "body" | "traceback" | "rows";

export function CallbackBlock({
  callback,
  onTable,
  onExchange,
}: {
  callback: AbdmDevCallback;
  onTable?: (table: string, id: string) => void;
  onExchange?: (requestId: string) => void;
}) {
  const { t } = useTranslation();
  const processedTone =
    callback.processed.status === "handled"
      ? "success"
      : callback.processed.status === "failed"
        ? "destructive"
        : "warning";
  const raised = Boolean(callback.processed.error);
  // What the reader wants first: the traceback when the handler raised, the body otherwise.
  const [view, setView] = useState<CallbackView>(raised ? "traceback" : "body");
  const tabs: {
    id: CallbackView;
    label: string;
    count?: number;
    tone?: "destructive";
  }[] = [
    {
      id: "headers",
      label: t("abdm_dev_view_headers"),
      count: Object.keys(callback.headers ?? {}).length,
    },
    { id: "body", label: t("abdm_dev_view_body") },
  ];
  if (raised)
    tabs.push({
      id: "traceback",
      label: t("abdm_dev_view_traceback"),
      tone: "destructive",
    });
  if (callback.rows.length > 0)
    tabs.push({
      id: "rows",
      label: t("abdm_dev_view_rows"),
      count: callback.rows.length,
    });
  return (
    <div className="grid min-w-0 gap-2 rounded-md border bg-black/20 p-3">
      <div className="flex flex-wrap items-baseline gap-x-2 gap-y-1 text-xs">
        <span className="text-sky-300">←</span>
        <span className="text-foreground/80">POST</span>
        <span className="[overflow-wrap:anywhere]">{callback.path}</span>
        <span className="text-muted-foreground">
          {callback.operationId || t("abdm_dev_unknown_operation")}
        </span>
        <span className="text-muted-foreground ml-auto tabular-nums">
          {formatWhen(callback.receivedAt)}
          {callback.seconds !== null
            ? ` · +${formatSeconds(callback.seconds)}`
            : ""}
        </span>
      </div>
      <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs">
        <Status
          tone={callback.signature.status === "ok" ? "success" : "destructive"}
        >
          {t("abdm_dev_signature")} {callback.signature.status}
          {callback.signature.header ? ` · ${callback.signature.header}` : ""}
        </Status>
        <Status tone={processedTone}>
          {t("abdm_dev_processed")} {callback.processed.status}
        </Status>
        {callback.hipIdHeader && (
          <span className="text-muted-foreground">
            X-HIP-ID {callback.hipIdHeader}
          </span>
        )}
        {callback.answersRequestId && onExchange && (
          <button
            type="button"
            onClick={() => onExchange(callback.answersRequestId as string)}
          >
            <Badge
              variant="info"
              size="sm"
              className="cursor-pointer font-mono"
            >
              {t("abdm_dev_answers")} {callback.answersRequestId.slice(0, 8)}…
            </Badge>
          </button>
        )}
      </div>
      {callback.signature.error && (
        <p className="text-muted-foreground text-xs [overflow-wrap:anywhere]">
          {callback.signature.error}
        </p>
      )}
      <TabStrip
        size="sm"
        tabs={tabs}
        value={view}
        onChange={setView}
        aria-label={t("abdm_dev_callback")}
      />
      {view === "headers" && <HeaderList headers={callback.headers} />}
      {view === "body" && (
        <JsonTree value={callback.body} title={t("abdm_dev_callback_body")} />
      )}
      {view === "traceback" && raised && (
        <div className="grid gap-1">
          <Label className="text-red-300">{t("abdm_dev_traceback")}</Label>
          <pre className="max-h-72 overflow-auto rounded-md border border-red-400/30 bg-red-950/30 p-2 font-mono text-[11px] leading-4 [overflow-wrap:anywhere] whitespace-pre-wrap text-red-100">
            {callback.processed.error}
          </pre>
        </div>
      )}
      {view === "rows" && <RowRefs rows={callback.rows} onTable={onTable} />}
    </div>
  );
}

/** `?a=1&b=2` of a URL as rows; nothing when the URL has no query string. */
function queryPairs(url: string): [string, string][] {
  const at = url.indexOf("?");
  if (at < 0) return [];
  return [...new URLSearchParams(url.slice(at + 1)).entries()];
}

/** True when the key press belongs to a field inside the sheet, so a digit must not switch the view. */
function inField(target: EventTarget | null): boolean {
  return Boolean(
    target instanceof HTMLElement &&
    target.closest("input, textarea, select, [contenteditable=true]"),
  );
}

export default function ExchangeSheet({
  requestId,
  windowSeconds,
  onClose,
  onTable,
  onExchange,
  view: viewProp,
  onView,
}: {
  requestId: string | null;
  windowSeconds: number;
  onClose: () => void;
  onTable?: (table: string, id: string) => void;
  onExchange?: (requestId: string) => void;
  /** The chosen view, when the caller keeps it (the explorer: in the URL). */
  view?: string;
  onView?: (view: ExchangeView) => void;
}) {
  const { t } = useTranslation();
  const [viewLocal, setViewLocal] = useState<ExchangeView>("general");
  const view: ExchangeView = isExchangeView(viewProp) ? viewProp : viewLocal;
  const setView = (next: ExchangeView) => {
    if (onView) onView(next);
    else setViewLocal(next);
  };
  const detail = useQuery<AbdmDevExchangeDetail>({
    queryKey: devKeys.exchange(requestId ?? ""),
    queryFn: query(careApi.devExchange, {
      pathParams: { requestId: requestId ?? "" },
      silent: true,
    }),
    enabled: Boolean(requestId),
    refetchInterval: (q) =>
      q.state.data?.state === "accepted_waiting" ||
      q.state.data?.state === "sent"
        ? 5000
        : false,
    retry: false,
  });
  const d = detail.data;
  const tabs: {
    id: ExchangeView;
    label: string;
    count?: number;
    tone?: "destructive";
  }[] = [
    { id: "general", label: t("abdm_dev_view_general") },
    { id: "request", label: t("abdm_dev_view_request") },
    { id: "response", label: t("abdm_dev_view_response") },
    {
      id: "callbacks",
      label: t("abdm_dev_view_callbacks"),
      count: d ? d.callbackList.length + (d.answers ? 1 : 0) : undefined,
      tone: d?.callbackList.some((c) => c.processed.error)
        ? "destructive"
        : undefined,
    },
    { id: "rows", label: t("abdm_dev_view_rows"), count: d?.rows.length },
  ];
  const reason = d ? httpReason(d.response.status) : "";
  return (
    <Sheet
      open={Boolean(requestId)}
      onOpenChange={(open) => !open && onClose()}
    >
      <SheetContent
        size="xl"
        className={`${CONSOLE_CLASS} font-mono`}
        onKeyDown={(e) => {
          if (e.metaKey || e.ctrlKey || e.altKey || inField(e.target)) return;
          const index = ["1", "2", "3", "4", "5"].indexOf(e.key);
          if (index >= 0) {
            e.preventDefault();
            setView(EXCHANGE_VIEWS[index]);
          }
        }}
      >
        <SheetHeader className="border-b">
          <SheetTitle className="font-mono text-sm [overflow-wrap:anywhere]">
            <span className="text-muted-foreground">{d?.kind ?? ""} </span>
            {d?.operationId ?? t("abdm_dev_exchange")}
          </SheetTitle>
          <SheetDescription className="text-muted-foreground font-mono text-xs [overflow-wrap:anywhere] select-all">
            REQUEST-ID {requestId}
          </SheetDescription>
          {/* Reserved height: the line fills in when the detail lands, and the tabs below do not move. */}
          <div className="flex min-h-5 flex-wrap items-center gap-x-4 gap-y-1 pt-1 text-xs">
            {d && (
              <>
                <Status
                  tone={STATE_TONE[d.state]}
                  pulse={statePulse(d.state)}
                  hollow={d.state === "no_answer"}
                >
                  {t(`abdm_dev_state_${d.state}`)}
                </Status>
                <span className={toneText(httpTone(d.response.status))}>
                  {d.response.status ?? "—"}
                  {reason ? ` ${reason}` : ""}
                </span>
                <span className="text-muted-foreground tabular-nums">
                  {formatMs(d.response.ms)}
                </span>
                <span className="text-muted-foreground [overflow-wrap:anywhere]">
                  {d.method} {d.path}
                </span>
              </>
            )}
          </div>
        </SheetHeader>
        <TabStrip
          tabs={tabs}
          value={view}
          onChange={setView}
          keys
          className="px-4 pt-1"
          aria-label={t("abdm_dev_exchange")}
        />
        <SheetBody className="grid min-w-0 content-start gap-4 text-xs">
          {detail.isLoading && <Skeleton className="h-40 w-full rounded-md" />}
          {detail.isError && (
            <p className="text-destructive text-sm">
              {t("abdm_dev_load_failed")}
            </p>
          )}
          {d && view === "general" && (
            <GeneralView d={d} windowSeconds={windowSeconds} />
          )}
          {d && view === "request" && <RequestView d={d} />}
          {d && view === "response" && <ResponseView d={d} />}
          {d && view === "callbacks" && (
            <CallbacksView d={d} onTable={onTable} onExchange={onExchange} />
          )}
          {d && view === "rows" && <RowRefs rows={d.rows} onTable={onTable} />}
        </SheetBody>
      </SheetContent>
    </Sheet>
  );
}

function Group({
  label,
  count,
  children,
}: {
  label: React.ReactNode;
  count?: number;
  children: React.ReactNode;
}) {
  return (
    <section className="grid min-w-0 gap-1.5">
      <div className="flex items-baseline gap-2 border-b pb-1">
        <Label>{label}</Label>
        {count !== undefined && (
          <span className="text-muted-foreground text-[11px] tabular-nums">
            {count}
          </span>
        )}
      </div>
      {children}
    </section>
  );
}

function GeneralView({
  d,
  windowSeconds,
}: {
  d: AbdmDevExchangeDetail;
  windowSeconds: number;
}) {
  const { t } = useTranslation();
  const reason = httpReason(d.response.status);
  const general: [string, React.ReactNode][] = [
    [
      t("abdm_dev_request_url"),
      <span className="flex min-w-0 items-start gap-1">
        <span className="min-w-0 [overflow-wrap:anywhere] select-all">
          {d.request.url}
        </span>
        <CopyButton text={d.request.url} label={null} variant="ghost" />
      </span>,
    ],
    [t("abdm_dev_request_method"), d.method],
    [
      t("abdm_dev_status_code"),
      <Status tone={httpTone(d.response.status)}>
        {d.response.status ?? "—"}
        {reason ? ` ${reason}` : ""}
        {d.response.ms !== null && (
          <span className="text-muted-foreground">
            {" "}
            · {formatMs(d.response.ms)}
          </span>
        )}
      </Status>,
    ],
    [
      t("abdm_dev_operation"),
      <span>
        {d.operationId}
        <span className="text-muted-foreground">
          {" "}
          · {d.module} · {t(`abdm_dev_kind_${d.kind}`)}
        </span>
      </span>,
    ],
    [
      "REQUEST-ID",
      <span className="flex min-w-0 items-start gap-1">
        <span className="min-w-0 [overflow-wrap:anywhere] select-all">
          {d.requestId}
        </span>
        <CopyButton text={d.requestId} label={null} variant="ghost" />
      </span>,
    ],
    [
      t("abdm_dev_state"),
      <Status
        tone={STATE_TONE[d.state]}
        pulse={statePulse(d.state)}
        hollow={d.state === "no_answer"}
      >
        {t(`abdm_dev_state_${d.state}`)}
      </Status>,
    ],
  ];
  if (d.reason)
    general.push([
      t("abdm_dev_reason"),
      <span className="[overflow-wrap:anywhere] text-red-300">
        {d.reason}
        {d.errorSummary ? ` · ${d.errorSummary}` : ""}
      </span>,
    ]);
  const timing: [string, React.ReactNode][] = [
    [t("abdm_dev_sent_at"), formatWhen(d.sentAt)],
    [
      t("abdm_dev_answered_at"),
      d.completedAt ? (
        <span>
          {formatTime(d.completedAt)}
          <span className="text-muted-foreground">
            {" "}
            · +{formatMs(d.httpMs)}
          </span>
        </span>
      ) : (
        <span className="text-muted-foreground">
          {t("abdm_dev_stop_http_pending")}
        </span>
      ),
    ],
  ];
  if (d.kind === "call")
    timing.push([
      t("abdm_dev_first_callback"),
      d.callbacks > 0 ? (
        <span>
          +{formatSeconds(d.callbackSeconds)}
          <span className="text-muted-foreground">
            {" "}
            · {t("abdm_dev_stop_callback", { count: d.callbacks })}
          </span>
        </span>
      ) : (
        <span className="text-muted-foreground">
          {d.state === "no_answer"
            ? t("abdm_dev_stop_no_answer", {
                minutes: Math.round(windowSeconds / 60),
              })
            : d.state === "refused"
              ? t("abdm_dev_stop_never_pending")
              : t("abdm_dev_stop_waiting")}
        </span>
      ),
    ]);
  const scope: [string, React.ReactNode][] = [];
  if (d.facility) scope.push([t("abdm_dev_scope_facility"), d.facility.label]);
  if (d.patient)
    scope.push([
      t("abdm_dev_scope_patient"),
      <Link
        href={`/patient/${d.patient.id}`}
        className="text-primary hover:underline"
      >
        {d.patient.label || d.patient.id}
      </Link>,
    ]);
  if (d.encounter)
    scope.push([
      t("abdm_dev_scope_encounter"),
      d.encounter.label || d.encounter.id,
    ]);
  return (
    <>
      {d.failure && <FailureNotice {...(noticeFromFailure(d.failure) ?? {})} />}
      <Group label={t("abdm_dev_view_general")}>
        <Pairs entries={general} />
      </Group>
      <Group label={t("abdm_dev_timing")}>
        <Pairs entries={timing} />
        <Timeline exchange={d} windowSeconds={windowSeconds} className="pt-1" />
      </Group>
      {scope.length > 0 && (
        <Group label={t("abdm_dev_scope")}>
          <Pairs entries={scope} />
        </Group>
      )}
      <Group
        label={t("abdm_dev_request_headers")}
        count={Object.keys(d.request.headers ?? {}).length}
      >
        <HeaderList headers={d.request.headers} />
      </Group>
      <Group
        label={t("abdm_dev_response_headers")}
        count={Object.keys(d.response.headers ?? {}).length}
      >
        <HeaderList headers={d.response.headers} />
      </Group>
    </>
  );
}

function RequestView({ d }: { d: AbdmDevExchangeDetail }) {
  const { t } = useTranslation();
  const params = queryPairs(d.request.url);
  return (
    <>
      <p className="flex flex-wrap items-baseline gap-x-2 [overflow-wrap:anywhere]">
        <span className="text-sky-300">→</span>
        <span className="text-foreground/80">{d.method}</span>
        <span className="min-w-0 select-all">{d.request.url}</span>
      </p>
      {params.length > 0 && (
        <Group label={t("abdm_dev_query_params")} count={params.length}>
          <Pairs entries={params} />
        </Group>
      )}
      <JsonTree value={d.request.body} title={t("abdm_dev_request_body")} />
    </>
  );
}

function ResponseView({ d }: { d: AbdmDevExchangeDetail }) {
  const { t } = useTranslation();
  const reason = httpReason(d.response.status);
  return (
    <>
      <p className="flex flex-wrap items-baseline gap-x-2">
        <span className="text-sky-300">←</span>
        <span className={toneText(httpTone(d.response.status))}>
          {d.response.status ?? "—"}
          {reason ? ` ${reason}` : ""}
        </span>
        <span className="text-muted-foreground tabular-nums">
          {formatMs(d.response.ms)}
        </span>
      </p>
      {d.kind === "call" && (
        <p className="text-muted-foreground flex items-start gap-2 leading-5">
          <span aria-hidden className="select-none">
            →
          </span>
          <span className="min-w-0 [overflow-wrap:anywhere]">
            {t("abdm_dev_response_async_hint")}
          </span>
        </p>
      )}
      <JsonTree value={d.response.body} title={t("abdm_dev_response_body")} />
    </>
  );
}

function CallbacksView({
  d,
  onTable,
  onExchange,
}: {
  d: AbdmDevExchangeDetail;
  onTable?: (table: string, id: string) => void;
  onExchange?: (requestId: string) => void;
}) {
  const { t } = useTranslation();
  return (
    <>
      {d.answers && (
        <Group label={t("abdm_dev_answers_inbound")}>
          <CallbackBlock
            callback={d.answers}
            onTable={onTable}
            onExchange={onExchange}
          />
        </Group>
      )}
      <Group label={t("abdm_dev_view_callbacks")} count={d.callbackList.length}>
        {d.callbackList.length === 0 && (
          <p className="text-muted-foreground text-xs">
            {d.kind === "call"
              ? t("abdm_dev_no_callback_yet")
              : t("abdm_dev_sync_no_callback")}
          </p>
        )}
        {d.callbackList.map((c) => (
          <CallbackBlock
            key={c.id}
            callback={c}
            onTable={onTable}
            onExchange={onExchange}
          />
        ))}
      </Group>
    </>
  );
}
