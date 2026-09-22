import { Console, Dot } from "@/components/abdm/dev/console";
import { devPath, useDeveloperMode } from "@/components/abdm/dev/dev-state";
import ExchangeList, {
  type ExchangeFilters,
} from "@/components/abdm/dev/exchange-list";
import ExchangeSheet from "@/components/abdm/dev/exchange-sheet";
import { useTranslation } from "@/hooks/use-translation";
import { cn } from "@/lib/utils";
import { ChevronDown, ChevronRight, ExternalLink } from "lucide-react";
import { useState } from "react";

/**
 * The contextual entry to the explorer (ADR-018): a collapsed "Developer" disclosure appended at the
 * bottom of a surface (the encounter ABDM tab, the patient ABHA panel, the facility setup page, the
 * HPR section). Rendered only when developer mode is on; closed by default, so the surface itself
 * does not move. Open: the last exchanges for this entity and a link into the explorer with the
 * same filter. It wears the console skin: a dark strip on a clinical page says "developer mode is
 * on here" at a glance.
 */
export default function DevFooter({
  filters,
  className,
}: {
  filters: ExchangeFilters;
  className?: string;
}) {
  const { t } = useTranslation();
  const mode = useDeveloperMode();
  const [open, setOpen] = useState(false);
  const [exchange, setExchange] = useState<string | null>(null);
  if (!mode.enabled) return null;
  const href = devPath(filters as Record<string, string | undefined>);
  return (
    <Console className={cn("text-xs", className)}>
      <div className="flex items-center gap-2 px-3 py-1.5">
        <button
          type="button"
          className="flex items-center gap-2"
          aria-expanded={open}
          onClick={() => setOpen((o) => !o)}
        >
          {open ? (
            <ChevronDown className="text-muted-foreground size-3.5" />
          ) : (
            <ChevronRight className="text-muted-foreground size-3.5" />
          )}
          <Dot tone="success" pulse />
          <span className="font-semibold">abdm</span>
          <span className="text-muted-foreground">/</span>
          <span>{t("abdm_dev_footer_title").toLowerCase()}</span>
        </button>
        {/* A full page load: the explorer is an app route, and the host owns the route table. */}
        <a
          href={href}
          className="text-muted-foreground hover:text-foreground ml-auto flex items-center gap-1"
        >
          {t("abdm_dev_footer_open")} <ExternalLink className="size-3" />
        </a>
      </div>
      {open && (
        <div className="border-t px-3 py-3">
          <ExchangeList
            filters={filters}
            onOpen={setExchange}
            selected={exchange ?? undefined}
            embedded
            limit={5}
          />
          <ExchangeSheet
            requestId={exchange}
            windowSeconds={mode.status?.callbackWindowSeconds ?? 600}
            onClose={() => setExchange(null)}
          />
        </div>
      )}
    </Console>
  );
}
