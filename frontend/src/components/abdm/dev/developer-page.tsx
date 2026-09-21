import { DEV_ROUTE, useDeveloperMode } from "@/components/abdm/dev/dev-state";
import ExchangeList, {
  type ExchangeFilters,
} from "@/components/abdm/dev/exchange-list";
import ExchangeSheet from "@/components/abdm/dev/exchange-sheet";
import InboundList from "@/components/abdm/dev/inbound-list";
import ReadinessCard from "@/components/abdm/dev/readiness-card";
import TablesBrowser, { RowSheet } from "@/components/abdm/dev/tables-browser";
import PluginComponent from "@/components/common/plugin-component";
import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { useTranslation } from "@/hooks/use-translation";
import { cn } from "@/lib/utils";
import { Bug, ListTree, Radio, ShieldCheck, Table2 } from "lucide-react";
import { useQueryParams } from "raviger";

/**
 * The developer explorer (ADR-018), at /abdm/developer. An app route (not /admin): the gate is "any
 * authenticated user when ABDM_DEVELOPER_MODE=true", and a move between the admin layout and the
 * app layout crashes the host (findings J7).
 *
 * 4 tabs, URL-addressed (`?tab=`), so a link from an Encounter footer opens the list already
 * filtered and a refresh keeps the place: Exchanges, Inbound, Tables, Readiness. A chosen exchange
 * or row opens in a sheet over the tab, so the tab keeps its place.
 */

type Tab = "exchanges" | "inbound" | "tables" | "readiness";
type Params = ExchangeFilters & {
  tab?: Tab;
  exchange?: string;
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

function OffCard({ setting }: { setting: string }) {
  const { t } = useTranslation();
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Bug className="text-muted-foreground size-4" />{" "}
          {t("abdm_dev_off_title")}
        </CardTitle>
        <CardDescription>{t("abdm_dev_off_intro")}</CardDescription>
      </CardHeader>
      <CardContent className="grid gap-2 text-sm">
        <pre className="bg-muted rounded-md p-3 font-mono text-xs">
          {setting}=true
        </pre>
        <p className="text-muted-foreground text-xs">{t("abdm_dev_off_how")}</p>
      </CardContent>
    </Card>
  );
}

export default function DeveloperPage() {
  const { t } = useTranslation();
  const mode = useDeveloperMode();
  const [params, setParams] = useQueryParams<Params>();
  const tab: Tab = params.tab ?? "exchanges";
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
  const set = (next: Partial<Params>) => setParams({ ...params, ...next });
  const openExchange = (requestId: string) =>
    set({ exchange: requestId, row: undefined, table: params.table });
  const openRow = (table: string, id: string) =>
    set({ table, row: id, exchange: undefined });

  return (
    <PluginComponent>
      <div className="mx-auto grid max-w-7xl min-w-0 gap-4 p-4 md:p-6 [&>*]:min-w-0">
        <div className="flex flex-wrap items-center gap-3">
          <Bug className="text-muted-foreground size-5" />
          <h1 className="text-lg font-semibold">{t("abdm_dev_title")}</h1>
          <Badge variant="neutral" size="sm" className="font-mono">
            {t("abdm_dev_redaction_badge")}
          </Badge>
          {mode.status?.hosts && (
            <span className="text-muted-foreground ml-auto font-mono text-xs">
              {mode.status.hosts.gateway.replace(/^https?:\/\//, "")} · X-CM-ID{" "}
              {mode.status.hosts.cmId}
            </span>
          )}
        </div>
        <p className="text-muted-foreground text-sm">{t("abdm_dev_intro")}</p>

        {mode.isLoading && <Skeleton className="h-64 w-full rounded-xl" />}
        {!mode.isLoading && !mode.enabled && (
          <OffCard setting={mode.status?.setting ?? "ABDM_DEVELOPER_MODE"} />
        )}

        {mode.enabled && (
          <>
            <nav
              className="flex flex-wrap gap-1 border-b"
              aria-label={t("abdm_dev_title")}
            >
              {TABS.map(({ id, icon: Icon, key }) => (
                <a
                  key={id}
                  href={`${DEV_ROUTE}?tab=${id}`}
                  onClick={(e) => {
                    e.preventDefault();
                    set({ tab: id, exchange: undefined, row: undefined });
                  }}
                  className={cn(
                    "-mb-px flex items-center gap-1.5 border-b-2 px-3 py-2 text-sm",
                    tab === id
                      ? "border-primary text-foreground font-medium"
                      : "text-muted-foreground hover:text-foreground border-transparent",
                  )}
                  aria-current={tab === id ? "page" : undefined}
                >
                  <Icon className="size-4" /> {t(key)}
                </a>
              ))}
            </nav>

            {tab === "exchanges" && (
              <ExchangeList
                filters={filters}
                onFilters={(next) =>
                  set({
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
                onTable={(name) => set({ table: name, row: undefined })}
                onRow={openRow}
              />
            )}
            {tab === "readiness" && <ReadinessCard />}

            <ExchangeSheet
              requestId={params.exchange ?? null}
              windowSeconds={windowSeconds}
              onClose={() => set({ exchange: undefined })}
              onTable={openRow}
              onExchange={openExchange}
            />
            <RowSheet
              table={params.row ? (params.table ?? null) : null}
              rowId={params.row ?? null}
              onClose={() => set({ row: undefined })}
              onExchange={openExchange}
            />
          </>
        )}
      </div>
    </PluginComponent>
  );
}
