import type { FieldHelpContent } from "@/components/abdm/field-help";
import { useTranslation } from "@/hooks/use-translation";
import careApi, { type AbdmMasterRow } from "@/lib/careApi";
import { query } from "@/lib/request";
import { useQuery } from "@tanstack/react-query";

/** Shared, non-component exports of the M4 components (ADR-015). */

export const hprQueryKey = ["abdm", "me", "hpr"];

export const selectClass =
  "border-input dark:bg-input/30 h-12 w-full rounded-md border bg-transparent px-3 py-1 text-base shadow-2xs outline-none disabled:cursor-not-allowed disabled:opacity-50 md:h-10 md:px-2.5 md:text-sm";

export function errorMessage(error: unknown, fallback: string) {
  if (error && typeof error === "object" && "cause" in error) {
    const cause = (error as { cause?: Record<string, unknown> }).cause;
    const value = cause?.errors ?? cause?.message;
    if (typeof value === "string") return value;
  }
  return fallback;
}

/** 1 NHPR code list (`GET nhpr/masters/<kind>`), cached 1 h in the browser and 24 h on the server. */
export function useMaster(
  kind: string,
  params: Record<string, string> = {},
  enabled = true,
) {
  const clean = Object.fromEntries(Object.entries(params).filter(([, v]) => v));
  return useQuery<{ results: AbdmMasterRow[] }>({
    queryKey: ["abdm", "nhpr", "masters", kind, clean],
    queryFn: query(careApi.nhprMasters, {
      pathParams: { kind },
      queryParams: clean,
      silent: true,
    }),
    enabled,
    staleTime: 60 * 60 * 1000,
    retry: false,
  });
}

/** Badge tone for a registry facility status (Verified, Submitted, Draft, ...). */
export function statusTone(status: string) {
  const s = status.toLowerCase();
  if (s.includes("verified") || s === "active") return "success" as const;
  if (s.includes("submitted")) return "warning" as const;
  if (s.includes("draft")) return "neutral" as const;
  return "info" as const;
}

/**
 * Field help by label key (ADR-016 §Field help): `abdm_nhpr_help_<key without abdm_>_{title,what,
 * how,example}` when the locale has it, else undefined so the field renders without an icon.
 */
export function useNhprHelp() {
  const { t, i18n } = useTranslation();
  return (labelKey: string): FieldHelpContent | undefined => {
    const base = `abdm_nhpr_help_${labelKey.replace(/^abdm_/, "")}`;
    if (!i18n.exists(`${base}_what`, { ns: "care_abdm_fe" })) return undefined;
    return {
      title: t(`${base}_title`),
      what: t(`${base}_what`),
      how: t(`${base}_how`),
      example: t(`${base}_example`),
    };
  };
}

/** The "Add a facility" wizard route (ADR-016). `organizationId` is optional context for the geo picker. */
export function addFacilityPath(organizationId?: string) {
  return organizationId
    ? `/abdm/facilities/new?organization=${encodeURIComponent(organizationId)}`
    : "/abdm/facilities/new";
}

const COORDINATE_LIMIT = { latitude: 90, longitude: 180 } as const;

/**
 * Shortens a typed latitude or longitude to the form the registry accepts: 6 decimal places at
 * most and 1 at least (findings N23). The same rule is in `nhpr/rules.py:coordinate`, which is the
 * one that the registry body uses. This one only tidies the field, so it keeps an empty value and
 * an out-of-range value as the person typed them, and the field validator reports those.
 */
export function shortenCoordinate(
  value: string,
  kind: "latitude" | "longitude",
): string {
  const text = value.trim();
  if (!text) return value;
  const number = Number(text);
  const limit = COORDINATE_LIMIT[kind];
  if (Number.isNaN(number) || number < -limit || number > limit) return value;
  const short = number.toFixed(6).replace(/0+$/, "");
  return short.endsWith(".") ? `${short}0` : short;
}

/**
 * A card that a sheet holds drops its own frame and its side padding (ADR-017): the sheet is the
 * frame, and its header carries the title the card header would repeat.
 */
export const embeddedCard = {
  card: "border-0 bg-transparent py-0 shadow-none ring-0",
  padding: "px-0",
} as const;
