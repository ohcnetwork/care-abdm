import PluginComponent from "@/components/common/plugin-component";
import { useTranslation } from "@/hooks/use-translation";
import careApi from "@/lib/careApi";
import { query } from "@/lib/request";
import { type FacilityLike } from "@/lib/types/facility";
import { cn } from "@/lib/utils";
import { useQuery } from "@tanstack/react-query";
import { ChevronRight, Settings2 } from "lucide-react";
import { Link } from "raviger";

/**
 * Slot: FacilityHomeActions (care_fe/src/components/Facility/FacilityHome.tsx:253-257).
 *
 * The host renders this inside its "Configurations" dropdown and passes the
 * row styling through `className`. Render ONE row only: two side-by-side
 * elements stretched the dropdown far past its 48-unit minimum width.
 *
 * The row links to the plug's own page. A dialog cannot open from here. The
 * dropdown popup is a transformed ancestor of this subtree, so a portalled
 * `position: fixed` panel anchors to the dropdown and not to the viewport.
 * See components/abdm/facility-setup-page.tsx.
 */
export default function AbdmFacilityHomeActions({
  facility,
  className,
}: {
  facility: FacilityLike;
  className?: string;
}) {
  const { t } = useTranslation();

  const gateway = useQuery({
    queryKey: ["abdm", "gateway-status"],
    queryFn: query(careApi.gatewayStatus, { silent: true }),
    retry: false,
  });

  const status = gateway.isLoading
    ? { dot: "bg-gray-400", label: t("abdm_gateway_checking") }
    : gateway.data?.ok
      ? { dot: "bg-green-600", label: t("abdm_gateway_connected") }
      : { dot: "bg-red-600", label: t("abdm_gateway_unreachable") };

  return (
    <PluginComponent>
      <Link
        href={`/facility/${facility.id}/abdm/setup`}
        className={cn(
          "hover:bg-muted flex w-full cursor-pointer items-center gap-2 rounded-md px-2 py-1.5 text-left text-sm",
          className,
        )}
      >
        <Settings2 className="text-muted-foreground size-4 shrink-0" />
        <span className="grid gap-0.5">
          <span className="font-medium">{t("abdm_facility_settings")}</span>
          <span className="text-muted-foreground flex items-center gap-1.5 text-xs">
            <span className={cn("size-1.5 rounded-full", status.dot)} />
            {status.label}
          </span>
        </span>
        <ChevronRight className="text-muted-foreground ml-auto size-4 shrink-0" />
      </Link>
    </PluginComponent>
  );
}
