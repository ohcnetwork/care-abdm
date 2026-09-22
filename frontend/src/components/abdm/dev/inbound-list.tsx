import { devKeys } from "@/components/abdm/dev/dev-state";
import { CallbackBlock } from "@/components/abdm/dev/exchange-sheet";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { useTranslation } from "@/hooks/use-translation";
import careApi, { type AbdmDevInboundList } from "@/lib/careApi";
import { query } from "@/lib/request";
import { useQuery } from "@tanstack/react-query";
import { useEffect, useState } from "react";

/**
 * The exchanges the gateway starts (abdm-m2 design.md, "Inbound is a surface, and silence there is
 * a failure state"): discovery, link init and confirm, consent notify, health-information request,
 * Scan and Share. Each block is the inbound callback with our ack joined; an inbound with no ack is
 * the named, visible condition the docs ask for.
 */
export default function InboundList({
  onExchange,
  onTable,
}: {
  onExchange: (requestId: string) => void;
  onTable?: (table: string, id: string) => void;
}) {
  const { t } = useTranslation();
  const [before, setBefore] = useState("");
  const [pages, setPages] = useState<AbdmDevInboundList[]>([]);
  const live = useQuery<AbdmDevInboundList>({
    queryKey: devKeys.inbound({ before }),
    queryFn: query(careApi.devInbound, {
      queryParams: { limit: "20", before: before || undefined },
      silent: true,
    }),
    refetchInterval: before === "" ? 10000 : false,
    retry: false,
  });
  useEffect(() => {
    const page = live.data;
    if (!page) return;
    setPages((current) => {
      if (before === "")
        return current.length ? [page, ...current.slice(1)] : [page];
      return current.includes(page) ? current : [...current, page];
    });
  }, [live.data, before]);
  const rows = pages.flatMap((p) => p.rows);
  const last = pages[pages.length - 1];
  return (
    <div className="grid min-w-0 gap-5">
      <p className="text-muted-foreground flex items-start gap-2 text-xs leading-5">
        <span aria-hidden className="select-none">
          →
        </span>
        <span className="min-w-0 [overflow-wrap:anywhere]">
          {t("abdm_dev_inbound_intro")}
        </span>
      </p>
      {live.isLoading && rows.length === 0 && (
        <Skeleton className="h-40 w-full rounded-md" />
      )}
      {live.isError && (
        <p className="text-destructive text-xs">{t("abdm_dev_load_failed")}</p>
      )}
      {pages.length > 0 && rows.length === 0 && (
        <p className="text-muted-foreground text-xs">
          {t("abdm_dev_no_inbound")}
        </p>
      )}
      {rows.map((c) => (
        <div key={c.id} className="grid gap-2.5">
          <CallbackBlock callback={c} onTable={onTable} />
          <div className="flex flex-wrap items-center gap-2 pl-3 text-xs">
            {c.ack ? (
              <button
                type="button"
                className="text-left hover:underline"
                onClick={() => onExchange(c.ack!.requestId)}
              >
                <span className="text-sky-300">→ </span>
                <span className="text-muted-foreground">
                  {t("abdm_dev_ack_sent")}{" "}
                </span>
                <span>{c.ack.operationId}</span>
                <span className="text-muted-foreground">
                  {" "}
                  · HTTP {c.ack.httpStatus ?? "—"} · +{c.ack.seconds ?? "—"} s
                </span>
              </button>
            ) : (
              <span className="text-red-300">
                <span aria-hidden>→ </span>
                {t("abdm_dev_no_ack")}
              </span>
            )}
          </div>
        </div>
      ))}
      {last?.more && (
        <div>
          <Button
            type="button"
            variant="outline"
            size="sm"
            className="font-mono text-xs"
            onClick={() => setBefore(last.next)}
            disabled={live.isFetching}
          >
            {t("abdm_dev_load_more")}
          </Button>
        </div>
      )}
    </div>
  );
}
