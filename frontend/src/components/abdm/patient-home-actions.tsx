import { formatAbhaNumber } from "@/components/abdm/abha-wizard";
import { usePatientAbha } from "@/components/abdm/patient-abha-panel";
import PluginComponent from "@/components/common/plugin-component";
import { Badge } from "@/components/ui/badge";
import { useTranslation } from "@/hooks/use-translation";
import { cn } from "@/lib/utils";
import { IdCard } from "lucide-react";

/**
 * Slot: PatientHomeActions (pluginTypes.ts:30-34), mounted in the patient
 * profile sidebar (PatientProfile.tsx:177-182). A compact status chip; the full
 * panel with link/card lives in the Demography tab.
 */
export default function AbdmPatientHomeActions({
  patient,
  className,
}: {
  patient: { id: string };
  facilityId?: string;
  className?: string;
}) {
  const { t } = useTranslation();
  const { data, isLoading } = usePatientAbha(patient.id);
  if (isLoading || !data) return null;
  return (
    <PluginComponent>
      <div
        className={cn(
          "flex items-center justify-between gap-2 rounded-md border px-3 py-2 text-sm font-normal",
          className,
        )}
      >
        <span className="flex items-center gap-1.5">
          <IdCard className="size-4" /> {t("abdm_abha_short")}
        </span>
        {data.linked ? (
          <span className="font-mono text-xs tracking-wider">
            {formatAbhaNumber(data.abha_number)}
          </span>
        ) : (
          <Badge variant="neutral" size="sm">
            {t("abdm_not_linked")}
          </Badge>
        )}
      </div>
    </PluginComponent>
  );
}
