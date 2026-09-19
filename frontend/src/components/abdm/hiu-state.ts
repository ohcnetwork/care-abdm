import careApi, {
  type AbdmConsentRequest,
  type AbdmConsentRequestStatus,
  type AbdmFetchStatus,
  type AbdmHiuState,
} from "@/lib/careApi";
import { query } from "@/lib/request";
import { useQuery } from "@tanstack/react-query";

import type { BadgeTone } from "@/components/abdm/care-context-state";

/**
 * Read side for the "Records from other facilities" card (ADR-014). Every answer from ABDM is
 * asynchronous: the request id, the patient's decision, the artefact, the transaction id and the
 * push all arrive as callbacks. The card polls every 10 s while something may still arrive and
 * stops when nothing is open. The desk never reads an ABDM code: the backend classifies each
 * failure once (ADR-012) and the card shows `failure.what` and `failure.nextStep`.
 */

export const hiuQueryKey = (patientId: string, facilityId: string) => [
  "abdm",
  "patient",
  patientId,
  "consent-requests",
  facilityId,
];

/** Something may still arrive for this request: the decision, the artefact or the push. */
export function requestInFlight(request: AbdmConsentRequest): boolean {
  if (request.open) return true;
  return request.artefacts.some((artefact) =>
    artefact.fetches.some(
      (fetch) =>
        (fetch.status === "requested" || fetch.status === "acknowledged") &&
        new Date(fetch.deadlineAt).getTime() > Date.now(),
    ),
  );
}

export function useHiuState(patientId: string, facilityId: string) {
  return useQuery<AbdmHiuState>({
    queryKey: hiuQueryKey(patientId, facilityId),
    queryFn: query(careApi.consentRequests, {
      pathParams: { patientId },
      queryParams: { facility: facilityId },
      silent: true,
    }),
    retry: false,
    refetchInterval: (q) => {
      const state = q.state.data;
      if (!state) return false;
      return state.requests.some(requestInFlight) ? 10_000 : false;
    },
  });
}

export function requestTone(status: AbdmConsentRequestStatus): BadgeTone {
  if (status === "GRANTED") return "success";
  if (status === "REQUESTED") return "warning";
  if (status === "failed" || status === "DENIED" || status === "REVOKED")
    return "destructive";
  return "neutral";
}

/** i18n key of the request status badge. Family: abdm_cr_status_*. */
export function requestStatusKey(status: AbdmConsentRequestStatus): string {
  return `abdm_cr_status_${status.toLowerCase()}`;
}

export function fetchTone(status: AbdmFetchStatus): BadgeTone {
  if (status === "received") return "success";
  if (status === "partial") return "warning";
  if (status === "failed") return "destructive";
  return "warning";
}

/** i18n key of the transfer status. Family: abdm_fetch_status_*. */
export function fetchStatusKey(status: AbdmFetchStatus): string {
  return `abdm_fetch_status_${status}`;
}

/** Count of records the desk can open across every artefact of a request. */
export function availableRecords(request: AbdmConsentRequest): number {
  return request.artefacts.reduce(
    (n, artefact) => n + artefact.records.filter((r) => r.available).length,
    0,
  );
}

/** The latest transfer of a request, if any: what the status column reports after a grant. */
export function latestFetch(request: AbdmConsentRequest) {
  const fetches = request.artefacts.flatMap((a) => a.fetches);
  fetches.sort(
    (a, b) =>
      new Date(b.requestedAt).getTime() - new Date(a.requestedAt).getTime(),
  );
  return fetches[0];
}

/** `YYYY-MM-DD` for a date input, in the browser's zone. */
export function toDateInput(value: string | Date): string {
  const d = typeof value === "string" ? new Date(value) : value;
  const pad = (n: number) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
}

/** A date input value to the ISO instant at the start (or the end) of that local day. */
export function fromDateInput(value: string, endOfDay = false): string {
  const [y, m, d] = value.split("-").map(Number);
  const date = endOfDay
    ? new Date(y, m - 1, d, 23, 59, 59, 999)
    : new Date(y, m - 1, d, 0, 0, 0, 0);
  return date.toISOString();
}
