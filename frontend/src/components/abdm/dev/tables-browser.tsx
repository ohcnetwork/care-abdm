import { Label } from "@/components/abdm/dev/console";
import {
  CONSOLE_CLASS,
  devKeys,
  formatWhen,
  redactionMarker,
} from "@/components/abdm/dev/dev-state";
import JsonTree from "@/components/abdm/dev/json-tree";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
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
  type AbdmDevTable,
  type AbdmDevTableRow,
  type AbdmDevTableRows,
} from "@/lib/careApi";
import { query } from "@/lib/request";
import { cn } from "@/lib/utils";
import { useQuery } from "@tanstack/react-query";
import { ChevronRight, Lock } from "lucide-react";
import { useEffect, useState } from "react";

/**
 * The read-only browser over the 17 plug tables. Left: the tables with counts, by module. Right: the
 * rows of the chosen table (its list columns), newest first, "Load more" appends. A row opens in a
 * sheet with every column as a tree; a secret column shows as a lock badge; the exchanges and
 * callbacks the row names are links into the explorer.
 */

function Cell({ value }: { value: unknown }) {
  const marker = redactionMarker(value);
  if (marker) {
    return (
      <span className="border-strong-border text-muted-foreground inline-flex items-center gap-1 rounded border border-dashed px-1.5 text-[11px] leading-4 whitespace-nowrap">
        <Lock className="size-3" /> {marker.chars}
      </span>
    );
  }
  if (value === null || value === undefined || value === "") {
    return <span className="text-muted-foreground">—</span>;
  }
  if (typeof value === "boolean")
    return (
      <span className="text-[color:var(--console-keyword)]">
        {value ? "true" : "false"}
      </span>
    );
  if (typeof value === "object") {
    const ref = value as {
      label?: string;
      table?: string;
      kind?: string;
      id?: string;
    };
    if (ref.label && (ref.table || ref.kind)) {
      return (
        <Badge
          variant="neutral"
          size="sm"
          className="max-w-56 truncate font-mono"
          title={ref.id}
        >
          {ref.kind ?? ref.table} · {ref.label}
        </Badge>
      );
    }
    return (
      <span className="text-muted-foreground font-mono">
        {JSON.stringify(value).slice(0, 60)}
      </span>
    );
  }
  const text = String(value);
  if (/^\d{4}-\d{2}-\d{2}T/.test(text))
    return (
      <span className="whitespace-nowrap tabular-nums">{formatWhen(text)}</span>
    );
  return <span className="[overflow-wrap:anywhere]">{text}</span>;
}

export function RowSheet({
  table,
  rowId,
  onClose,
  onExchange,
  onCallback,
}: {
  table: string | null;
  rowId: string | null;
  onClose: () => void;
  onExchange: (requestId: string) => void;
  onCallback?: (callbackId: string) => void;
}) {
  const { t } = useTranslation();
  const detail = useQuery<AbdmDevTableRow>({
    queryKey: devKeys.tableRow(table ?? "", rowId ?? ""),
    queryFn: query(careApi.devTableRow, {
      pathParams: { name: table ?? "", rowId: rowId ?? "" },
      silent: true,
    }),
    enabled: Boolean(table && rowId),
    retry: false,
  });
  const d = detail.data;
  return (
    <Sheet
      open={Boolean(table && rowId)}
      onOpenChange={(open) => !open && onClose()}
    >
      <SheetContent size="lg" className={`${CONSOLE_CLASS} font-mono`}>
        <SheetHeader className="border-b">
          <SheetTitle className="font-mono text-sm">
            <span className="text-muted-foreground">{table} </span>
            {d?.title ?? ""}
          </SheetTitle>
          <SheetDescription className="text-muted-foreground font-mono text-xs select-all">
            {rowId}
          </SheetDescription>
        </SheetHeader>
        <SheetBody className="grid min-w-0 gap-4 text-xs">
          {detail.isLoading && <Skeleton className="h-40 w-full rounded-md" />}
          {detail.isError && (
            <p className="text-destructive text-sm">
              {t("abdm_dev_load_failed")}
            </p>
          )}
          {d && (
            <>
              {(d.exchanges.length > 0 || d.callbacks.length > 0) && (
                <div className="grid gap-1">
                  <Label>{t("abdm_dev_row_links")}</Label>
                  <ul className="flex flex-wrap gap-1">
                    {d.exchanges.map((e) => (
                      <li key={`${e.field}-${e.requestId}`}>
                        <button
                          type="button"
                          onClick={() => onExchange(e.requestId)}
                        >
                          <Badge
                            variant="info"
                            size="sm"
                            className="cursor-pointer font-mono"
                          >
                            {e.field} → {e.operationId}
                          </Badge>
                        </button>
                      </li>
                    ))}
                    {d.callbacks.map((c) => (
                      <li key={`${c.field}-${c.id}`}>
                        <button
                          type="button"
                          onClick={() => onCallback?.(c.id)}
                          disabled={!onCallback}
                        >
                          <Badge
                            variant="primary"
                            size="sm"
                            className="cursor-pointer font-mono"
                          >
                            {c.field} → {c.path}
                          </Badge>
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              <JsonTree value={d.row} title={t("abdm_dev_row")} />
            </>
          )}
        </SheetBody>
      </SheetContent>
    </Sheet>
  );
}

export default function TablesBrowser({
  table,
  onTable,
  onRow,
}: {
  table: string | null;
  onTable: (name: string) => void;
  onRow: (table: string, id: string) => void;
}) {
  const { t } = useTranslation();
  const tables = useQuery<{ tables: AbdmDevTable[] }>({
    queryKey: devKeys.tables,
    queryFn: query(careApi.devTables, { silent: true }),
    refetchInterval: 15000,
    retry: false,
  });
  const byModule = new Map<string, AbdmDevTable[]>();
  for (const tbl of tables.data?.tables ?? []) {
    byModule.set(tbl.module, [...(byModule.get(tbl.module) ?? []), tbl]);
  }
  const current = tables.data?.tables.find((x) => x.name === table);

  return (
    <div className="grid min-w-0 gap-4 md:grid-cols-[17rem_1fr]">
      <nav className="grid content-start gap-3 text-xs">
        {tables.isLoading && <Skeleton className="h-64 w-full rounded-md" />}
        {[...byModule.entries()].map(([module, list]) => (
          <div key={module} className="grid gap-px">
            <Label className="px-2 pb-1">{module}/</Label>
            {list.map((tbl) => (
              <button
                key={tbl.name}
                type="button"
                onClick={() => onTable(tbl.name)}
                aria-current={table === tbl.name ? "true" : undefined}
                className={cn(
                  "flex items-center gap-2 rounded-sm px-2 py-1 text-left hover:bg-white/[0.05]",
                  table === tbl.name &&
                    "bg-primary/10 text-foreground shadow-[inset_2px_0_0_0_var(--primary)]",
                )}
              >
                <span className="min-w-0 flex-1 truncate">{tbl.name}</span>
                <span className="text-muted-foreground tabular-nums">
                  {tbl.count}
                </span>
                <ChevronRight className="text-muted-foreground size-3 shrink-0" />
              </button>
            ))}
          </div>
        ))}
      </nav>
      <div className="grid min-w-0 content-start gap-3">
        {!table && (
          <p className="text-muted-foreground text-xs">
            {t("abdm_dev_pick_table")}
          </p>
        )}
        {table && current && (
          <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1 text-xs">
            <span className="text-sm">{current.title}</span>
            <span className="text-muted-foreground tabular-nums">
              {current.model} · {current.count} {t("abdm_dev_rows_word")}
            </span>
            {current.secretFields.length > 0 && (
              <span className="text-muted-foreground flex items-center gap-1">
                <Lock className="size-3" />
                {t("abdm_dev_secret_columns", {
                  columns: current.secretFields.join(", "),
                })}
              </span>
            )}
          </div>
        )}
        {/* `key` remounts the rows on a table change, so the cursor and the loaded pages start
            over whatever moved the URL: a click, Back, or a link. */}
        {table && <TableRows key={table} table={table} onRow={onRow} />}
      </div>
    </div>
  );
}

function TableRows({
  table,
  onRow,
}: {
  table: string;
  onRow: (table: string, id: string) => void;
}) {
  const { t } = useTranslation();
  const [pages, setPages] = useState<AbdmDevTableRows[]>([]);
  const [before, setBefore] = useState("");
  const rows = useQuery<AbdmDevTableRows>({
    queryKey: devKeys.tableRows(table, { before }),
    queryFn: query(careApi.devTableRows, {
      pathParams: { name: table },
      queryParams: { limit: "50", before: before || undefined },
      silent: true,
    }),
    retry: false,
  });
  // Pages append below the first (no reshuffle).
  useEffect(() => {
    const page = rows.data;
    if (!page) return;
    setPages((current) => {
      if (before === "") return [page];
      return current.includes(page) ? current : [...current, page];
    });
  }, [rows.data, before]);
  const first = pages[0];
  const visible = pages.flatMap((p) => p.rows);
  const last = pages[pages.length - 1];

  return (
    <>
      {rows.isLoading && pages.length === 0 && (
        <Skeleton className="h-40 w-full rounded-md" />
      )}
      {rows.isError && (
        <p className="text-destructive text-xs">{t("abdm_dev_load_failed")}</p>
      )}
      {first && visible.length === 0 && (
        <p className="text-muted-foreground text-sm">{t("abdm_dev_no_rows")}</p>
      )}
      {first && visible.length > 0 && (
        <div className="overflow-x-auto rounded-md border">
          <table className="w-full border-collapse text-xs">
            <thead>
              <tr className="border-b bg-white/[0.03] text-left">
                {first.columns.map((c) => (
                  <th
                    key={c}
                    className="px-3 py-1.5 font-normal whitespace-nowrap"
                  >
                    <Label>{c}</Label>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {visible.map((r) => (
                <tr
                  key={String(r.id)}
                  className="cursor-pointer border-b border-white/[0.06] align-top last:border-b-0 hover:bg-white/[0.04]"
                  onClick={() => onRow(table, String(r.id))}
                >
                  {first.columns.map((c) => (
                    <td
                      key={c}
                      className={cn(
                        "max-w-64 px-3 py-1.5 leading-5",
                        c === "id" && "text-muted-foreground text-[11px]",
                      )}
                    >
                      {c === "id" ? (
                        String(r.id).slice(0, 8) + "…"
                      ) : (
                        <Cell value={r[c]} />
                      )}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      {last?.more && (
        <div>
          <Button
            type="button"
            variant="outline"
            size="sm"
            className="font-mono text-xs"
            onClick={() => setBefore(last.next)}
            disabled={rows.isFetching}
          >
            {t("abdm_dev_load_more")}
          </Button>
        </div>
      )}
    </>
  );
}
