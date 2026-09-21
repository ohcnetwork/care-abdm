import {
  statusKey,
  toneFor,
  useCareContext,
  viewFor,
} from "@/components/abdm/care-context-state";
import PluginComponent from "@/components/common/plugin-component";
import { Badge } from "@/components/ui/badge";
import { useTranslation } from "@/hooks/use-translation";
import { cn } from "@/lib/utils";
import { Share2 } from "lucide-react";
import { navigate, usePath } from "raviger";

/**
 * Slot: EncounterActions (pluginTypes.ts:46-49), mounted in the encounter summary actions
 * (summary-panel-actions.tab.tsx:95). The host passes a button className. ADR-013 D5: the
 * action opens the "ABDM Records" tab, which owns the sharing UI. The row shows the count of
 * records that wait to be shared, so the desk sees at a glance whether the tab needs a visit.
 */
export default function AbdmEncounterActions({
  encounter,
  className,
}: {
  encounter: { id: string };
  className?: string;
}) {
  const { t } = useTranslation();
  const path = usePath() ?? "";
  const { data, isLoading } = useCareContext(encounter.id);
  if (isLoading || !data || !data.facilityConfigured) return null;
  const view = viewFor(data);
  const waiting = data.shareItems.filter(
    (i) => i.status === "staged" || i.status === "failed",
  ).length;
  // The tab route is the encounter route with its last segment replaced (EncounterShow `tab`).
  const target = path.replace(
    /\/encounter\/([^/]+)(\/[^/]*)?$/,
    "/encounter/$1/abdm",
  );
  return (
    <PluginComponent>
      <button
        type="button"
        className={cn(className, "gap-2")}
        onClick={() => navigate(target)}
      >
        <Share2 className="size-4" />
        <span className="flex-1 text-left">{t("abdm_cc_action_open_tab")}</span>
        {waiting > 0 ? (
          <Badge variant="warning" size="sm">
            {waiting}
          </Badge>
        ) : (
          <Badge variant={toneFor(view)} size="sm">
            {t(statusKey(view))}
          </Badge>
        )}
      </button>
    </PluginComponent>
  );
}
