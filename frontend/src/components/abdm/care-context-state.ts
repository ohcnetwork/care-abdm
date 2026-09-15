import careApi, {
  type AbdmCareContextState,
  type AbdmCareContextStatus,
} from "@/lib/careApi";
import { query } from "@/lib/request";
import { useQuery } from "@tanstack/react-query";

/**
 * Shared read side for the 2 encounter slots. Polls while the gateway answer is
 * pending: a link is confirmed only by the `/v3/link/on_carecontext` callback
 * (docs whats-new 2026-09-10), so the state changes after the desk action returns.
 */

export const careContextQueryKey = (encounterId: string) => [
  "abdm",
  "encounter",
  encounterId,
  "care-context",
];

const PENDING: AbdmCareContextStatus[] = ["pending", "link_requested"];

export function useCareContext(encounterId: string) {
  return useQuery<AbdmCareContextState>({
    queryKey: careContextQueryKey(encounterId),
    queryFn: query(careApi.encounterCareContext, {
      pathParams: { encounterId },
      silent: true,
    }),
    retry: false,
    refetchInterval: (q) => {
      const status = q.state.data?.careContext?.status;
      return status && PENDING.includes(status) ? 5000 : false;
    },
  });
}

export type BadgeTone = "success" | "warning" | "destructive" | "neutral";

export function toneFor(state?: AbdmCareContextState): BadgeTone {
  const status = state?.careContext?.status;
  if (status === "linked") return "success";
  if (status === "link_requested") return "warning";
  if (status === "failed") return "destructive";
  return "neutral";
}

/** i18n key for the status line. The desk sees one short sentence, never a raw code. */
export function statusKey(state?: AbdmCareContextState): string {
  if (!state) return "abdm_cc_status_unknown";
  if (!state.facilityConfigured) return "abdm_cc_status_facility_not_setup";
  if (!state.patientAbhaAddress) return "abdm_cc_status_no_abha";
  const status = state.careContext?.status;
  if (status === "linked") {
    return state.careContext?.notifiedAt
      ? "abdm_cc_status_linked_notified"
      : "abdm_cc_status_linked";
  }
  if (status === "link_requested") return "abdm_cc_status_link_requested";
  if (status === "failed") return "abdm_cc_status_failed";
  if (state.careContext?.errorCode === "NO_RECORDS")
    return "abdm_cc_status_no_records";
  if (state.linkToken?.status === "requested")
    return "abdm_cc_status_token_requested";
  return "abdm_cc_status_not_linked";
}
