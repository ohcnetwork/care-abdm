import {
  statusKey,
  toneFor,
  useCareContext,
  viewFor,
} from "@/components/abdm/care-context-state";
import PluginComponent from "@/components/common/plugin-component";
import { Badge } from "@/components/ui/badge";
import { useTranslation } from "@/hooks/use-translation";
import { Share2 } from "lucide-react";

/**
 * Slot: EncounterOverviewTop (pluginTypes.ts:103-107), mounted at the top of the
 * encounter overview (pages/Encounters/tabs/overview.tsx:56). One stable row: the
 * visit's display name (non-clinical, the same one the patient sees in the ABHA app)
 * and a plain sharing status. The action lives in EncounterActions.
 */
export default function AbdmEncounterOverviewTop({
  encounterId,
}: {
  encounter: unknown;
  patientId: string;
  encounterId: string;
}) {
  const { t } = useTranslation();
  const { data, isLoading } = useCareContext(encounterId);
  if (isLoading || !data) return null;
  if (!data.facilityConfigured) return null;
  const view = viewFor(data);
  return (
    <PluginComponent>
      <div className="flex items-center justify-between gap-3 rounded-md border px-3 py-2 text-sm">
        <span className="flex min-w-0 items-center gap-1.5">
          <Share2 className="size-4 shrink-0" />
          <span className="truncate">
            {data.careContext?.display ?? t("abdm_cc_row_title")}
          </span>
        </span>
        <Badge variant={toneFor(view)} size="sm">
          {t(statusKey(view))}
        </Badge>
      </div>
    </PluginComponent>
  );
}
