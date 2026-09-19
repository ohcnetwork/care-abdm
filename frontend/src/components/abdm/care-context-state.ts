import careApi, { type AbdmCareContextState } from "@/lib/careApi";
import { query } from "@/lib/request";
import { useQuery } from "@tanstack/react-query";

/**
 * Shared read side for the 2 encounter slots. Polls while ABDM has not answered yet: a link is
 * confirmed only by the `/v3/link/on_carecontext` callback (docs whats-new 2026-09-10), so the
 * state changes after the desk action returns. The desk sees plain states (`viewFor`), never
 * the backend status codes or the `activity` log; those belong to /admin/abdm.
 *
 * The backend classifies every failure once (ADR-012) and sends a `failure` block. This module
 * never reads an ABDM code: it reads `failure.retry` only. A failure that can be repeated later
 * is the `waiting` view, which shows the time and holds the button until then.
 */

export const careContextQueryKey = (encounterId: string) => [
  "abdm",
  "encounter",
  encounterId,
  "care-context",
];

/** What the desk sees. One state, one sentence, one action. */
export type CareContextView =
  | "no_abha"
  | "no_records"
  | "ready"
  | "in_progress"
  | "waiting"
  | "shared"
  | "failed";

export function viewFor(state: AbdmCareContextState): CareContextView {
  if (!state.patientAbhaAddress) return "no_abha";
  const context = state.careContext;
  // No row yet: the visit was never synced (it may predate the facility setup). The action runs
  // the sync, which is when the backend learns whether there is anything to share.
  if (!context) return "ready";
  if (context.status === "linked") return "shared";
  if (context.errorCode === "NO_RECORDS" || !context.hiTypes.length)
    return "no_records";
  const failure = state.failure;
  if (failure) return failure.retry === "after" ? "waiting" : "failed";
  if (context.status === "failed") return "failed";
  return "in_progress";
}

/** The moment the desk may try again, or null when it may try now. */
export function retryAfter(state: AbdmCareContextState): Date | null {
  const at = state.failure?.retryAt;
  if (!at) return null;
  const moment = new Date(at);
  return moment.getTime() > Date.now() ? moment : null;
}

export function formatTime(value: Date): string {
  return value.toLocaleTimeString(undefined, {
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function useCareContext(encounterId: string) {
  return useQuery<AbdmCareContextState>({
    queryKey: careContextQueryKey(encounterId),
    queryFn: query(careApi.encounterCareContext, {
      pathParams: { encounterId },
      silent: true,
    }),
    retry: false,
    refetchInterval: (q) => {
      const state = q.state.data;
      if (!state) return false;
      const view = viewFor(state);
      if (view === "in_progress") return 5000;
      // A wait is minutes long. Poll slowly, so the button frees itself without a second timer.
      return view === "waiting" ? 15000 : false;
    },
  });
}

export type BadgeTone = "success" | "warning" | "destructive" | "neutral";

export function toneFor(view: CareContextView): BadgeTone {
  if (view === "shared") return "success";
  if (view === "in_progress" || view === "waiting") return "warning";
  if (view === "failed") return "destructive";
  return "neutral";
}

/** i18n key for the short status badge. Family: abdm_cc_status_*. */
export function statusKey(view: CareContextView): string {
  return `abdm_cc_status_${view}`;
}

/** ABDM record type → i18n key of its human label. Family: abdm_hi_type_*. */
const HI_TYPE_KEYS: Record<string, string> = {
  OPConsultation: "abdm_hi_type_op_consultation",
  Prescription: "abdm_hi_type_prescription",
  DiagnosticReport: "abdm_hi_type_diagnostic_report",
  DischargeSummary: "abdm_hi_type_discharge_summary",
  WellnessRecord: "abdm_hi_type_wellness_record",
  ImmunizationRecord: "abdm_hi_type_immunization_record",
  HealthDocumentRecord: "abdm_hi_type_health_document_record",
  Invoice: "abdm_hi_type_invoice",
};

export function hiTypeLabel(
  t: (key: string) => string,
  hiType: string,
): string {
  const key = HI_TYPE_KEYS[hiType];
  return key ? t(key) : hiType;
}

export function formatDay(value: string): string {
  return new Date(value).toLocaleDateString(undefined, {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}
