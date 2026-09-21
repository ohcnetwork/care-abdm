import {
  devKeys,
  formatSeconds,
  formatWhen,
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

/**
 * 1 exchange in full, in a side sheet over the list (the list keeps its place). Sections, in the
 * order things happened: the timeline, the request, the answer, every callback (with its
 * traceback when the handler raised), the inbound it answers, and the plug rows that name it.
 * Every body is a JSON tree; header values are lengths.
 */

export function HeaderList({
  headers,
}: {
  headers: Record<string, string | number>;
}) {
  const entries = Object.entries(headers ?? {});
  if (entries.length === 0)
    return <span className="text-muted-foreground text-xs">—</span>;
  return (
    <ul className="flex flex-wrap gap-1">
      {entries.map(([name, value]) => (
        <li key={name}>
          <Badge variant="neutral" size="sm" className="font-mono">
            {name}
            <span className="text-muted-foreground">
              {typeof value === "number" ? ` · ${value} chars` : ` · ${value}`}
            </span>
          </Badge>
        </li>
      ))}
    </ul>
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
  return (
    <div className="grid min-w-0 gap-2 rounded-md border p-3">
      <div className="flex flex-wrap items-center gap-1.5 text-xs">
        <Badge variant="primary" size="sm" className="font-mono">
          POST {callback.path}
        </Badge>
        <span className="font-mono">
          {callback.operationId || t("abdm_dev_unknown_operation")}
        </span>
        <span className="text-muted-foreground ml-auto font-mono tabular-nums">
          {formatWhen(callback.receivedAt)}
          {callback.seconds !== null
            ? ` · +${formatSeconds(callback.seconds)}`
            : ""}
        </span>
      </div>
      <div className="flex flex-wrap gap-1.5">
        <Badge
          variant={
            callback.signature.status === "ok" ? "success" : "destructive"
          }
          size="sm"
        >
          {t("abdm_dev_signature")} {callback.signature.status}
          {callback.signature.header ? ` · ${callback.signature.header}` : ""}
        </Badge>
        <Badge variant={processedTone} size="sm">
          {t("abdm_dev_processed")} {callback.processed.status}
        </Badge>
        {callback.hipIdHeader && (
          <Badge variant="neutral" size="sm" className="font-mono">
            X-HIP-ID {callback.hipIdHeader}
          </Badge>
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
      <div className="grid gap-1">
        <span className="text-muted-foreground text-xs">
          {t("abdm_dev_headers")}
        </span>
        <HeaderList headers={callback.headers} />
      </div>
      <JsonTree value={callback.body} title={t("abdm_dev_callback_body")} />
      {callback.processed.error && (
        <div className="grid gap-1">
          <span className="text-destructive text-xs font-medium">
            {t("abdm_dev_traceback")}
          </span>
          <pre className="bg-muted max-h-72 overflow-auto rounded-md p-2 font-mono text-[11px] leading-4 [overflow-wrap:anywhere] whitespace-pre-wrap">
            {callback.processed.error}
          </pre>
        </div>
      )}
      {callback.rows.length > 0 && (
        <div className="grid gap-1">
          <span className="text-muted-foreground text-xs">
            {t("abdm_dev_rows_named")}
          </span>
          <RowRefs rows={callback.rows} onTable={onTable} />
        </div>
      )}
    </div>
  );
}

export default function ExchangeSheet({
  requestId,
  windowSeconds,
  onClose,
  onTable,
  onExchange,
}: {
  requestId: string | null;
  windowSeconds: number;
  onClose: () => void;
  onTable?: (table: string, id: string) => void;
  onExchange?: (requestId: string) => void;
}) {
  const { t } = useTranslation();
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
  return (
    <Sheet
      open={Boolean(requestId)}
      onOpenChange={(open) => !open && onClose()}
    >
      <SheetContent size="xl">
        <SheetHeader>
          <SheetTitle className="font-mono text-base [overflow-wrap:anywhere]">
            {d?.operationId ?? t("abdm_dev_exchange")}
          </SheetTitle>
          <SheetDescription className="font-mono text-xs [overflow-wrap:anywhere] select-all">
            REQUEST-ID {requestId}
          </SheetDescription>
        </SheetHeader>
        <SheetBody className="grid min-w-0 gap-5">
          {detail.isLoading && <Skeleton className="h-40 w-full rounded-md" />}
          {detail.isError && (
            <p className="text-destructive text-sm">
              {t("abdm_dev_load_failed")}
            </p>
          )}
          {d && (
            <>
              <Timeline exchange={d} windowSeconds={windowSeconds} />
              <div className="flex flex-wrap gap-1.5 text-xs">
                {d.facility && (
                  <Badge variant="neutral" size="sm">
                    {t("abdm_dev_scope_facility")} {d.facility.label}
                  </Badge>
                )}
                {d.patient && (
                  <Link href={`/patient/${d.patient.id}`} className="contents">
                    <Badge
                      variant="neutral"
                      size="sm"
                      className="cursor-pointer"
                    >
                      {t("abdm_dev_scope_patient")} {d.patient.id.slice(0, 8)}…
                    </Badge>
                  </Link>
                )}
                {d.encounter && (
                  <Badge variant="neutral" size="sm" className="font-mono">
                    {t("abdm_dev_scope_encounter")} {d.encounter.id.slice(0, 8)}
                    …
                  </Badge>
                )}
              </div>
              {d.failure && (
                <FailureNotice {...(noticeFromFailure(d.failure) ?? {})} />
              )}

              <section className="grid gap-2">
                <h3 className="text-sm font-semibold">
                  {t("abdm_dev_request")}
                </h3>
                <p className="font-mono text-xs [overflow-wrap:anywhere]">
                  <span className="font-semibold">{d.request.method}</span>{" "}
                  {d.request.url}
                </p>
                <HeaderList headers={d.request.headers} />
                <JsonTree
                  value={d.request.body}
                  title={t("abdm_dev_request_body")}
                />
              </section>

              <section className="grid gap-2">
                <h3 className="text-sm font-semibold">
                  {t("abdm_dev_response")}{" "}
                  <span className="text-muted-foreground font-mono text-xs">
                    {d.response.status ?? "—"} ·{" "}
                    {d.response.ms !== null ? `${d.response.ms} ms` : "—"}
                  </span>
                </h3>
                {Object.keys(d.response.headers).length > 0 && (
                  <HeaderList headers={d.response.headers} />
                )}
                <JsonTree
                  value={d.response.body}
                  title={t("abdm_dev_response_body")}
                />
              </section>

              {d.answers && (
                <section className="grid gap-2">
                  <h3 className="text-sm font-semibold">
                    {t("abdm_dev_answers_inbound")}
                  </h3>
                  <CallbackBlock
                    callback={d.answers}
                    onTable={onTable}
                    onExchange={onExchange}
                  />
                </section>
              )}

              <section className="grid gap-2">
                <h3 className="text-sm font-semibold">
                  {t("abdm_dev_callbacks_heading", {
                    count: d.callbackList.length,
                  })}
                </h3>
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
              </section>

              <section className="grid gap-2">
                <h3 className="text-sm font-semibold">
                  {t("abdm_dev_rows_named")}
                </h3>
                <RowRefs rows={d.rows} onTable={onTable} />
              </section>
            </>
          )}
        </SheetBody>
      </SheetContent>
    </Sheet>
  );
}
