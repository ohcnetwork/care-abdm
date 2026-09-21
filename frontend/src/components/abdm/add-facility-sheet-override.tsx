import { addFacilityPath } from "@/components/abdm/nhpr-shared";
import PluginComponent from "@/components/common/plugin-component";
import { Button } from "@/components/ui/button";
import { useTranslation } from "@/hooks/use-translation";
import { Plus } from "lucide-react";
import { navigate } from "raviger";
import type { ComponentType } from "react";

export function AddFacilityButton({
  organizationId,
  size = "sm",
}: {
  organizationId?: string;
  size?: "sm" | "default";
}) {
  const { t } = useTranslation();
  return (
    <Button
      type="button"
      size={size}
      onClick={() => navigate(addFacilityPath(organizationId))}
    >
      <Plus className="size-4" /> {t("abdm_add_facility")}
    </Button>
  );
}

/**
 * Override of the host's `AddFacilitySheet` (ADR-016). The host renders that sheet on the
 * organization's facilities page when the person may create facilities
 * (care_fe OrganizationFacilities.tsx:87). This replacement takes its place and opens the
 * "Add a facility" wizard instead, so every new facility passes the ABDM choice.
 *
 * How it lands (care_fe docs/care-apps-plugin-overrides.md): the host build wraps the components
 * named in `REACT_MFE_REGISTERED_COMPONENTS` with `register()`; the plug manifest declares
 * `overrides: [{ component: "AddFacilitySheet", replacement }]` and `PluginEngine` registers it.
 * The deployment must list `AddFacilitySheet` in that variable, or the host renders its own sheet.
 * `__base` is the host component, for a fall-through that this override does not need.
 */
export default function AddFacilitySheetOverride({
  organizationId,
}: {
  organizationId: string;
  __base?: ComponentType<{ organizationId: string }>;
}) {
  return (
    <PluginComponent>
      <AddFacilityButton organizationId={organizationId} />
    </PluginComponent>
  );
}
