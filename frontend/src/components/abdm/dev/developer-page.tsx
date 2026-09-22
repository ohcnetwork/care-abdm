import {
  Command,
  Console,
  Dot,
  Kbd,
  Label,
} from "@/components/abdm/dev/console";
import { DEV_ROUTE, useDeveloperMode } from "@/components/abdm/dev/dev-state";
import ExchangeList, {
  type ExchangeFilters,
} from "@/components/abdm/dev/exchange-list";
import ExchangeSheet from "@/components/abdm/dev/exchange-sheet";
import InboundList from "@/components/abdm/dev/inbound-list";
import ReadinessCard from "@/components/abdm/dev/readiness-card";
import TablesBrowser, { RowSheet } from "@/components/abdm/dev/tables-browser";
import PluginComponent from "@/components/common/plugin-component";
import { Skeleton } from "@/components/ui/skeleton";
import { useTranslation } from "@/hooks/use-translation";
import { useCleanQueryParams } from "@/lib/query-params";
import { cn } from "@/lib/utils";
import { ListTree, Radio, ShieldCheck, Table2 } from "lucide-react";
import { useEffect, useRef } from "react";

/**
 * The developer explorer (ADR-018), at /abdm/developer. An app route (not /admin): the gate is "any
 * authenticated user when ABDM_DEVELOPER_MODE=true", and a move between the admin layout and the
 * app layout crashes the host (findings J7).
 *
 * One console panel (`console.tsx`): a status line, the 4 tabs, the tab's body. URL-addressed
 * (`?tab=`), so a link from an Encounter footer opens the list already filtered and a refresh keeps
 * the place: Exchanges, Inbound, Tables, Readiness. A chosen exchange or row opens in a sheet over
 * the tab, so the tab keeps its place.
 *
 * The URL is the only state. A place (a tab, a table, an opened sheet) pushes a history entry, so
 * Back returns to the view before it. An adjustment (a filter, a closed sheet) replaces the entry.
 * `useCleanQueryParams` drops a key set to `undefined` (findings J11).
 *
 * Keys, when no field has the focus and no sheet is open: 1–4 switch the tab, / focuses the filter.
 * An open exchange sheet takes 1–5 for its own views (`exchange-sheet.tsx`); `?view=` keeps the
 * chosen view, so a link can point at the response of an exchange.
 */

type Tab = "exchanges" | "inbound" | "tables" | "readiness";
type Params = ExchangeFilters & {
  tab?: Tab;
  exchange?: string;
  /** The exchange sheet's view (general, request, response, callbacks, rows). */
  view?: string;
  table?: string;
  row?: string;
  callback?: string;
};

const TABS: { id: Tab; icon: typeof ListTree; key: string }[] = [
  { id: "exchanges", icon: ListTree, key: "abdm_dev_tab_exchanges" },
  { id: "inbound", icon: Radio, key: "abdm_dev_tab_inbound" },
  { id: "tables", icon: Table2, key: "abdm_dev_tab_tables" },
  { id: "readiness", icon: ShieldCheck, key: "abdm_dev_tab_readiness" },
];

/** True when the key press belongs to a field, so a shortcut must not take it. */
function inField(target: EventTarget | null): boolean {
  return Boolean(
    target instanceof HTMLElement &&
    target.closest(
      "input, textarea, select, button, [contenteditable=true], [role=dialog]",
    ),
  );
}

function StatusLine({ on, right }: { on: boolean; right?: React.ReactNode }) {
  const { t } = useTranslation();
  return (
    <header className="flex flex-wrap items-center gap-x-3 gap-y-1 border-b px-5 py-3 text-xs">
      <span className="flex items-center gap-2">
        <Dot tone={on ? "success" : "neutral"} pulse={on} />
        <span className="font-semibold">abdm</span>
        <span className="text-muted-foreground">/</span>
        <span>developer</span>
      </span>
      <span className="text-muted-foreground hidden sm:inline">
        {t("abdm_dev_title")}
      </span>
      {right && (
        <span className="text-muted-foreground ml-auto flex flex-wrap items-center gap-x-3 gap-y-1">
          {right}
        </span>
      )}
    </header>
  );
}

function OffPanel({ setting }: { setting: string }) {
  const { t } = useTranslation();
  return (
    <Console>
      <StatusLine on={false} right={<span>{t("abdm_dev_card_off")}</span>} />
      <div className="grid gap-4 p-5">
        <p className="text-sm font-medium">{t("abdm_dev_off_title")}</p>
        <p className="text-muted-foreground text-xs [overflow-wrap:anywhere]">
          {t("abdm_dev_off_intro")}
        </p>
        <Command command={`${setting}=true`} note={t("abdm_dev_off_how")} />
      </div>
    </Console>
  );
}

export default function DeveloperPage() {
  const { t } = useTranslation();
  const mode = useDeveloperMode();
  const [params, setParams] = useCleanQueryParams<Params>();
  const tab: Tab = TABS.some((x) => x.id === params.tab)
    ? (params.tab as Tab)
    : "exchanges";
  const filters: ExchangeFilters = {
    module: params.module,
    operation: params.operation,
    state: params.state,
    status: params.status,
    facility: params.facility,
    patient: params.patient,
    encounter: params.encounter,
    request_id: params.request_id,
  };
  const windowSeconds = mode.status?.callbackWindowSeconds ?? 600;
  const go = (next: Partial<Params>) => setParams(next, { push: true });
  const adjust = (next: Partial<Params>) => setParams(next);
  const openExchange = (requestId: string) =>
    go({ exchange: requestId, row: undefined });
  const openRow = (table: string, id: string) =>
    go({ table, row: id, exchange: undefined });
  const sheetOpen = Boolean(params.exchange || params.row);

  // The latest `go` for the key handler, which is bound once.
  const goRef = useRef(go);
  goRef.current = go;
  useEffect(() => {
    if (!mode.enabled) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.metaKey || e.ctrlKey || e.altKey || sheetOpen || inField(e.target))
        return;
      const index = ["1", "2", "3", "4"].indexOf(e.key);
      if (index >= 0) {
        e.preventDefault();
        goRef.current({
          tab: TABS[index].id,
          exchange: undefined,
          view: undefined,
          row: undefined,
        });
        return;
      }
      if (e.key === "/") {
        const field = document.querySelector<HTMLInputElement>(
          "[data-console-search]",
        );
        if (field) {
          e.preventDefault();
          field.focus();
        }
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [mode.enabled, sheetOpen]);

  return (
    <PluginComponent>
      <div className="mx-auto grid max-w-7xl min-w-0 gap-4 p-4 md:p-6 [&>*]:min-w-0">
        {mode.isLoading && <Skeleton className="h-64 w-full rounded-xl" />}
        {!mode.isLoading && !mode.enabled && (
          <OffPanel setting={mode.status?.setting ?? "ABDM_DEVELOPER_MODE"} />
        )}

        {mode.enabled && (
          <Console>
            <StatusLine
              on
              right={
                <>
                  {mode.status?.hosts && (
                    <span className="tabular-nums">
                      {mode.status.hosts.gateway.replace(/^https?:\/\//, "")} ·
                      X-CM-ID {mode.status.hosts.cmId}
                    </span>
                  )}
                  <Label className="border-strong-border rounded border px-1.5 py-0.5">
                    {t("abdm_dev_redaction_badge")}
                  </Label>
                </>
              }
            />
            <p className="text-muted-foreground flex items-start gap-2 border-b px-5 py-3 text-xs leading-5">
              <span aria-hidden className="select-none">
                →
              </span>
              <span className="min-w-0 [overflow-wrap:anywhere]">
                {t("abdm_dev_intro")}
              </span>
            </p>

            <nav
              className="flex flex-wrap items-stretch gap-1 border-b px-3 pt-2"
              aria-label={t("abdm_dev_title")}
            >
              {TABS.map(({ id, icon: Icon, key }, index) => (
                <a
                  key={id}
                  href={`${DEV_ROUTE}?tab=${id}`}
                  onClick={(e) => {
                    // A modifier click opens a new tab or window: leave it to the browser.
                    if (
                      e.button !== 0 ||
                      e.metaKey ||
                      e.altKey ||
                      e.ctrlKey ||
                      e.shiftKey
                    ) {
                      return;
                    }
                    e.preventDefault();
                    if (tab === id) return;
                    go({
                      tab: id,
                      exchange: undefined,
                      view: undefined,
                      row: undefined,
                    });
                  }}
                  className={cn(
                    "-mb-px flex items-center gap-2 rounded-t border-b-2 px-3.5 py-2.5 text-xs",
                    tab === id
                      ? "border-primary text-foreground bg-white/[0.03]"
                      : "text-muted-foreground hover:text-foreground border-transparent hover:bg-white/[0.02]",
                  )}
                  aria-current={tab === id ? "page" : undefined}
                >
                  <Icon className="size-3.5" />
                  {t(key)}
                  <Kbd>{index + 1}</Kbd>
                </a>
              ))}
              <span className="text-muted-foreground ml-auto hidden items-center gap-1.5 px-2 text-[11px] md:flex">
                <Kbd>/</Kbd> {t("abdm_dev_shortcut_search")}
              </span>
            </nav>

            <div className="grid min-w-0 gap-5 p-5 [&>*]:min-w-0">
              {tab === "exchanges" && (
                <ExchangeList
                  filters={filters}
                  onFilters={(next) =>
                    adjust({
                      ...Object.fromEntries(
                        Object.keys(filters).map((k) => [k, undefined]),
                      ),
                      ...next,
                    })
                  }
                  onOpen={openExchange}
                  selected={params.exchange}
                />
              )}
              {tab === "inbound" && (
                <InboundList onExchange={openExchange} onTable={openRow} />
              )}
              {tab === "tables" && (
                <TablesBrowser
                  table={params.table ?? null}
                  onTable={(name) => go({ table: name, row: undefined })}
                  onRow={openRow}
                />
              )}
              {tab === "readiness" && <ReadinessCard />}
            </div>
          </Console>
        )}

        {mode.enabled && (
          <>
            <ExchangeSheet
              requestId={params.exchange ?? null}
              windowSeconds={windowSeconds}
              onClose={() => adjust({ exchange: undefined, view: undefined })}
              onTable={openRow}
              onExchange={openExchange}
              view={params.view}
              onView={(view) => adjust({ view })}
            />
            <RowSheet
              table={params.row ? (params.table ?? null) : null}
              rowId={params.row ?? null}
              onClose={() => adjust({ row: undefined })}
              onExchange={openExchange}
            />
          </>
        )}
      </div>
    </PluginComponent>
  );
}
