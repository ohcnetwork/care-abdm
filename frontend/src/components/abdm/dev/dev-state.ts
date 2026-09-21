import careApi, {
  type AbdmDevKind,
  type AbdmDevModule,
  type AbdmDevState,
  type AbdmDevStatus,
} from "@/lib/careApi";
import { HttpError, query } from "@/lib/request";
import { useQuery } from "@tanstack/react-query";

/**
 * Shared, non-component exports of the developer explorer (ADR-018).
 *
 * The explorer exists only when `ABDM_DEVELOPER_MODE=true`: `useDeveloperMode()` asks
 * `GET dev/status` once (5 minutes stale) and every entry point renders on `enabled` alone.
 */

export const DEV_ROUTE = "/abdm/developer";

export const devKeys = {
  status: ["abdm", "dev", "status"] as const,
  exchanges: (filters: Record<string, string>) =>
    ["abdm", "dev", "exchanges", filters] as const,
  exchange: (requestId: string) =>
    ["abdm", "dev", "exchange", requestId] as const,
  inbound: (filters: Record<string, string>) =>
    ["abdm", "dev", "inbound", filters] as const,
  callback: (id: string) => ["abdm", "dev", "callback", id] as const,
  tables: ["abdm", "dev", "tables"] as const,
  tableRows: (name: string, filters: Record<string, string>) =>
    ["abdm", "dev", "table", name, filters] as const,
  tableRow: (name: string, id: string) =>
    ["abdm", "dev", "table", name, "row", id] as const,
  readiness: ["abdm", "dev", "readiness"] as const,
};

export function useDeveloperMode() {
  const status = useQuery<AbdmDevStatus>({
    queryKey: devKeys.status,
    queryFn: query(careApi.devStatus, { silent: true }),
    staleTime: 5 * 60 * 1000,
    retry: false,
  });
  return {
    enabled: Boolean(status.data?.enabled),
    status: status.data,
    isLoading: status.isLoading,
  };
}

/** True when the API refused because the flag is off (HTTP 403 with the setting named). */
export function isDeveloperModeOff(error: unknown): boolean {
  return (
    error instanceof HttpError &&
    error.status === 403 &&
    JSON.stringify(error.cause ?? {}).includes("ABDM_DEVELOPER_MODE")
  );
}

/** Badge tones for the docs' 5 exchange states. */
export const STATE_TONE: Record<
  AbdmDevState,
  "neutral" | "info" | "success" | "destructive" | "warning"
> = {
  sent: "neutral",
  accepted_waiting: "info",
  answered: "success",
  refused: "destructive",
  no_answer: "warning",
};

export const KIND_TONE: Record<AbdmDevKind, "neutral" | "info" | "primary"> = {
  call: "primary",
  ack: "info",
  push: "info",
  sync: "neutral",
};

export const MODULES: AbdmDevModule[] = ["gateway", "m1", "m2", "m3", "m4"];
export const STATES: AbdmDevState[] = [
  "sent",
  "accepted_waiting",
  "answered",
  "refused",
  "no_answer",
];

export const CHECK_TONE: Record<
  "ok" | "warning" | "blocker",
  "success" | "warning" | "destructive"
> = { ok: "success", warning: "warning", blocker: "destructive" };

export function formatMs(ms: number | null | undefined): string {
  if (ms === null || ms === undefined) return "—";
  if (ms < 1000) return `${ms} ms`;
  return `${(ms / 1000).toFixed(1)} s`;
}

export function formatSeconds(s: number | null | undefined): string {
  if (s === null || s === undefined) return "—";
  if (s < 60) return `${s.toFixed(1)} s`;
  const minutes = Math.floor(s / 60);
  const rest = Math.round(s - minutes * 60);
  return `${minutes} min ${rest} s`;
}

export function formatWhen(iso: string | null | undefined): string {
  if (!iso) return "—";
  const d = new Date(iso);
  return `${d.toLocaleDateString()} ${d.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  })}`;
}

export function formatTime(iso: string | null | undefined): string {
  if (!iso) return "—";
  return new Date(iso).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

/** `<redacted, 755 chars>`, `<encrypted, 344 chars>`, `<600 chars, base64>`, `<N chars, omitted>`. */
const MARKER_RE =
  /^<(redacted|encrypted), (\d+) chars>$|^<(\d+) chars, (base64|omitted)>$/;

export function redactionMarker(
  value: unknown,
): { kind: string; chars: number } | null {
  if (typeof value !== "string") return null;
  const m = MARKER_RE.exec(value);
  if (!m) return null;
  if (m[1]) return { kind: m[1], chars: Number(m[2]) };
  return { kind: m[4], chars: Number(m[3]) };
}

/** The explorer URL with filters in the query string, for the contextual footers. */
export function devPath(
  filters: Record<string, string | undefined> = {},
  tab: "exchanges" | "inbound" | "tables" | "readiness" = "exchanges",
): string {
  const params = new URLSearchParams();
  params.set("tab", tab);
  for (const [k, v] of Object.entries(filters)) if (v) params.set(k, v);
  return `${DEV_ROUTE}?${params.toString()}`;
}
