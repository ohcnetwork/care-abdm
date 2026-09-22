import careApi, {
  type AbdmDevKind,
  type AbdmDevModule,
  type AbdmDevState,
  type AbdmDevStatus,
} from "@/lib/careApi";
import { HttpError, query } from "@/lib/request";
import { useQuery } from "@tanstack/react-query";
import { useCallback, useState } from "react";

/**
 * Shared, non-component exports of the developer explorer (ADR-018).
 *
 * The explorer exists only when `ABDM_DEVELOPER_MODE=true`: `useDeveloperMode()` asks
 * `GET dev/status` once (5 minutes stale) and every entry point renders on `enabled` alone.
 */

export const DEV_ROUTE = "/abdm/developer";

/* ── Console skin (console.tsx renders these) ───────────────────────────── */

export const CONSOLE_CLASS = "dark abdm-console";

export type Tone =
  "neutral" | "info" | "success" | "warning" | "destructive" | "primary";

export const DOT_TONE: Record<Tone, string> = {
  neutral: "bg-muted-foreground/70",
  info: "bg-sky-400",
  success: "bg-emerald-400",
  warning: "bg-amber-400",
  destructive: "bg-red-400",
  primary: "bg-cyan-300",
};

/** The hollow dot: a ring in the tone's colour (literal classes, so Tailwind emits them). */
export const RING_TONE: Record<Tone, string> = {
  neutral: "border-muted-foreground/70",
  info: "border-sky-400",
  success: "border-emerald-400",
  warning: "border-amber-400",
  destructive: "border-red-400",
  primary: "border-cyan-300",
};

export const TEXT_TONE: Record<Tone, string> = {
  neutral: "text-muted-foreground",
  info: "text-sky-300",
  success: "text-emerald-300",
  warning: "text-amber-300",
  destructive: "text-red-300",
  primary: "text-cyan-300",
};

export function toneText(tone: Tone): string {
  return TEXT_TONE[tone];
}

/** The views of an exchange sheet (the inspector's tabs). In the URL as `?view=`. */
export const EXCHANGE_VIEWS = [
  "general",
  "request",
  "response",
  "callbacks",
  "rows",
] as const;
export type ExchangeView = (typeof EXCHANGE_VIEWS)[number];
export function isExchangeView(value: unknown): value is ExchangeView {
  return (EXCHANGE_VIEWS as readonly string[]).includes(String(value));
}

/** The standard reason phrases (RFC 9110) for the codes the plug meets; the code alone otherwise. */
const HTTP_REASON: Record<number, string> = {
  200: "OK",
  201: "Created",
  202: "Accepted",
  204: "No Content",
  400: "Bad Request",
  401: "Unauthorized",
  403: "Forbidden",
  404: "Not Found",
  409: "Conflict",
  422: "Unprocessable Content",
  429: "Too Many Requests",
  500: "Internal Server Error",
  502: "Bad Gateway",
  503: "Service Unavailable",
  504: "Gateway Timeout",
};
export function httpReason(status: number | null | undefined): string {
  if (status === null || status === undefined) return "";
  return HTTP_REASON[status] ?? "";
}

/** A 2xx answer is fine, a 3xx is odd, anything from 400 is a refusal. */
export function httpTone(status: number | null | undefined): Tone {
  if (status === null || status === undefined) return "neutral";
  if (status >= 400) return "destructive";
  if (status >= 300) return "warning";
  return "success";
}

/** Copy with a 1.2 s check mark. `copied` is the id of the text last copied. */
export function useCopy() {
  const [copied, setCopied] = useState<string | null>(null);
  const copy = useCallback((id: string, text: string) => {
    void navigator.clipboard?.writeText(text).then(() => {
      setCopied(id);
      window.setTimeout(() => setCopied((c) => (c === id ? null : c)), 1200);
    });
  }, []);
  return { copied, copy };
}

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

/** The day of a log line, short: "21 Sep". */
export function formatDay(iso: string | null | undefined): string {
  if (!iso) return "";
  return new Date(iso).toLocaleDateString([], {
    day: "2-digit",
    month: "short",
  });
}

/** The 2 states in which something is still expected, so the dot pulses. */
export function statePulse(state: AbdmDevState): boolean {
  return state === "sent" || state === "accepted_waiting";
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
