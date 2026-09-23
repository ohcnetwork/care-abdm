import { cn } from "@/lib/utils";
import type { ReactNode } from "react";

/**
 * The inverted card face that every ABDM identity uses (ADR-017 decision 7): a green gradient, 2
 * blurred orbs and white words. 3 cards show an identity and now read alike — the care context of
 * an encounter, the HPR ID on the user profile, and the ABHA of a patient.
 *
 * To build one, put `heroCard` on the container and `<HeroLayers />` as its first child. A `Card`
 * trims the orbs itself; a plain container must add `overflow-hidden`.
 */
export const heroCard =
  "text-primary-50 shadow-primary-950/25 relative isolate shadow-lg ring-white/10";

/**
 * The 3 decorative layers of the hero. `isolate` on the container holds them, and `-z-10` keeps
 * them behind the words.
 */
export function HeroLayers() {
  return (
    <>
      <div
        aria-hidden
        className="from-primary-700 via-primary-900 to-primary-950 pointer-events-none absolute inset-0 -z-10 bg-linear-to-br"
      />
      <div
        aria-hidden
        className="bg-primary-300/25 pointer-events-none absolute -top-24 -right-12 -z-10 size-72 rounded-full blur-3xl"
      />
      <div
        aria-hidden
        className="bg-primary-400/15 pointer-events-none absolute -bottom-28 -left-16 -z-10 size-72 rounded-full blur-3xl"
      />
    </>
  );
}

/** The square that holds the icon of a hero card. */
export function HeroIcon({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <span
      className={cn(
        "grid size-9 shrink-0 place-items-center rounded-lg bg-white/10 ring-1 ring-white/20",
        className,
      )}
    >
      {children}
    </span>
  );
}

/** A badge on the hero. The plain tones are too pale on the gradient. */
export const heroBadge =
  "border-white/25 bg-white/15 text-white backdrop-blur-sm";

/** The lead words under a hero title. */
export const heroLead = "text-primary-100/85";

/** The quiet words on a hero: a label, a summary, a hint. */
export const heroMuted = "text-primary-200";

/**
 * A solid button on the hero: a white face with green words. The `default` variant is green on
 * green there, so it disappears.
 */
export const heroSolid =
  "border-white bg-white text-primary-900 shadow-none hover:border-white/90 hover:bg-white/90 dark:bg-white dark:text-primary-900";

/** A quiet button on the hero: a translucent white face. */
export const heroGhost =
  "border-white/25 bg-white/10 text-white shadow-none hover:bg-white/20 hover:text-white dark:bg-white/10 dark:hover:bg-white/20 [:active,[data-pressed]]:bg-white/25";

/** A block of the hero that holds a value the reader must not miss. */
export const heroTile = "rounded-lg bg-white/5 p-3 ring-1 ring-white/10";

/**
 * A panel on the hero that holds normal controls. An input or a table keeps its usual light face,
 * because a form control on the gradient is hard to read.
 */
export const heroPanel =
  "bg-card text-card-foreground rounded-xl p-4 ring-1 ring-white/15";

/** 1 fact of a hero card: a small label above the value. */
export function HeroFact({
  label,
  children,
  mono,
  className,
}: {
  label: string;
  children: ReactNode;
  mono?: boolean;
  className?: string;
}) {
  return (
    <div className={cn("grid gap-1", heroTile, className)}>
      <span
        className={cn(
          "text-[11px] font-medium tracking-wide uppercase",
          heroMuted,
        )}
      >
        {label}
      </span>
      <span className={cn("text-xs text-white", mono && "font-mono break-all")}>
        {children}
      </span>
    </div>
  );
}
