import {
  CONSOLE_CLASS,
  DOT_TONE,
  RING_TONE,
  TEXT_TONE,
  useCopy,
  type Tone,
} from "@/components/abdm/dev/dev-state";
import { Button } from "@/components/ui/button";
import { useTranslation } from "@/hooks/use-translation";
import { cn } from "@/lib/utils";
import { Check, Copy } from "lucide-react";
import type { HTMLAttributes } from "react";

/**
 * The console skin of developer mode (ADR-018, visual identity 2026-09-22).
 *
 * One idea: a developer surface looks like a terminal, and a clinical surface never does. The
 * wrapper carries `dark abdm-console` (`style/index.css`): `.dark` makes every `dark:` utility fire
 * and `.abdm-console` swaps the Care UI tokens for a navy palette, so every Card, Badge, Button,
 * Sheet and Table inside keeps working unchanged. The pieces here are the terminal furniture the
 * design system has no word for: the `$` prompt, a command block with its copy button, a key cap,
 * a state dot, an uppercase label.
 *
 * Sheets render in a portal, outside the wrapper, so `SheetContent` takes `CONSOLE_CLASS` itself.
 * The non-component parts (the class, the tones, `useCopy`) live in `dev-state.ts`.
 */

/** The console surface. `frame` draws the panel border; off inside a sheet that has its own. */
export function Console({
  className,
  frame = true,
  children,
  ...props
}: HTMLAttributes<HTMLDivElement> & { frame?: boolean }) {
  return (
    <div
      {...props}
      className={cn(
        CONSOLE_CLASS,
        "bg-background text-foreground min-w-0 font-mono text-sm antialiased",
        frame && "overflow-hidden rounded-lg border shadow-sm",
        className,
      )}
    >
      {children}
    </div>
  );
}

/** A small uppercase caption, the label of a section or a column. */
export function Label({
  className,
  children,
  ...props
}: HTMLAttributes<HTMLSpanElement>) {
  return (
    <span
      {...props}
      className={cn(
        "text-muted-foreground text-[10.5px] font-medium tracking-[0.14em] uppercase",
        className,
      )}
    >
      {children}
    </span>
  );
}

/** The `$` of a shell line. */
export function Prompt({ className }: { className?: string }) {
  return (
    <span
      aria-hidden
      className={cn("text-muted-foreground shrink-0 select-none", className)}
    >
      $
    </span>
  );
}

/** A state dot. `pulse` while something is still expected; `hollow` when nothing arrived. */
export function Dot({
  tone,
  pulse = false,
  hollow = false,
  className,
}: {
  tone: Tone;
  pulse?: boolean;
  hollow?: boolean;
  className?: string;
}) {
  return (
    <span
      aria-hidden
      className={cn(
        "inline-block size-1.5 shrink-0 rounded-full",
        hollow ? cn("border", RING_TONE[tone]) : DOT_TONE[tone],
        pulse && "animate-pulse",
        className,
      )}
    />
  );
}

/** A dot and a word: the lean form of a state chip. */
export function Status({
  tone,
  pulse,
  hollow,
  children,
  className,
}: {
  tone: Tone;
  pulse?: boolean;
  hollow?: boolean;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 whitespace-nowrap",
        TEXT_TONE[tone],
        className,
      )}
    >
      <Dot tone={tone} pulse={pulse} hollow={hollow} />
      {children}
    </span>
  );
}

/** A key cap, for a shortcut hint. */
export function Kbd({ children }: { children: React.ReactNode }) {
  return (
    <kbd className="border-strong-border text-muted-foreground inline-flex h-4 min-w-4 items-center justify-center rounded border bg-white/5 px-1 font-mono text-[10px] leading-none">
      {children}
    </kbd>
  );
}

/**
 * A copy button whose label never changes: only the icon swaps to a check mark, so the row it sits
 * in does not move. `label={null}` gives the icon alone (the aria-label says "Copy").
 */
export function CopyButton({
  text,
  label,
  variant = "outline",
  className,
}: {
  text: string;
  label?: string | null;
  variant?: "outline" | "ghost";
  className?: string;
}) {
  const { t } = useTranslation();
  const { copied, copy } = useCopy();
  const done = copied === text;
  const iconOnly = label === null;
  return (
    <Button
      type="button"
      variant={variant}
      size="sm"
      className={cn(
        "h-7 gap-1.5 font-mono text-xs",
        iconOnly ? "size-6 p-0" : "px-2",
        className,
      )}
      onClick={() => copy(text, text)}
      aria-live="polite"
      aria-label={
        done ? t("abdm_dev_copied") : iconOnly ? t("abdm_dev_copy") : undefined
      }
      title={iconOnly ? t("abdm_dev_copy") : undefined}
    >
      {done ? (
        <Check className="size-3.5 text-emerald-300" />
      ) : (
        <Copy className="size-3.5" />
      )}
      {!iconOnly && (label ?? t("abdm_dev_copy"))}
    </Button>
  );
}

/**
 * A tab strip, the inspector's: a row of buttons with an underline on the chosen one, an optional
 * count per tab, an optional key cap (1..n). `size="sm"` for a strip inside a block.
 */
export function TabStrip<T extends string>({
  tabs,
  value,
  onChange,
  size = "md",
  keys = false,
  className,
  "aria-label": ariaLabel,
}: {
  tabs: { id: T; label: React.ReactNode; count?: number; tone?: Tone }[];
  value: T;
  onChange: (id: T) => void;
  size?: "sm" | "md";
  /** Show 1..n key caps (the caller binds the keys). */
  keys?: boolean;
  className?: string;
  "aria-label"?: string;
}) {
  return (
    <div
      role="tablist"
      aria-label={ariaLabel}
      className={cn(
        "flex flex-wrap items-stretch gap-1 border-b",
        size === "sm" ? "text-[11px]" : "text-xs",
        className,
      )}
    >
      {tabs.map((tab, index) => {
        const active = tab.id === value;
        return (
          <button
            key={tab.id}
            type="button"
            role="tab"
            aria-selected={active}
            onClick={() => onChange(tab.id)}
            className={cn(
              "-mb-px flex items-center gap-1.5 rounded-t border-b-2",
              size === "sm" ? "px-2 py-1" : "px-3 py-2",
              active
                ? "border-primary text-foreground bg-white/[0.03]"
                : "text-muted-foreground hover:text-foreground border-transparent hover:bg-white/[0.02]",
            )}
          >
            {tab.tone && <Dot tone={tab.tone} />}
            {tab.label}
            {tab.count !== undefined && (
              <span className="text-muted-foreground tabular-nums">
                {tab.count}
              </span>
            )}
            {keys && <Kbd>{index + 1}</Kbd>}
          </button>
        );
      })}
    </div>
  );
}

/**
 * A command block, after the terminal block of the ABDM docs: `$`, the command (wraps, never
 * scrolls sideways), an optional `→` note under it, and "Copy command". Used for the flag, the
 * worker start line, and any next step the backend writes in backticks.
 */
export function Command({
  command,
  note,
  className,
}: {
  command: string;
  note?: React.ReactNode;
  className?: string;
}) {
  const { t } = useTranslation();
  return (
    <div
      className={cn(
        "grid min-w-0 gap-2 rounded-md border bg-black/25 p-3 text-xs",
        className,
      )}
    >
      <div className="flex items-start gap-2">
        <Prompt />
        <code className="min-w-0 flex-1 leading-5 [overflow-wrap:anywhere] whitespace-pre-wrap select-all">
          {command}
        </code>
      </div>
      {note && (
        <div className="text-muted-foreground flex items-start gap-2 leading-5">
          <span aria-hidden className="shrink-0 select-none">
            →
          </span>
          <span className="min-w-0 [overflow-wrap:anywhere]">{note}</span>
        </div>
      )}
      <div>
        <CopyButton text={command} label={t("abdm_dev_copy_command")} />
      </div>
    </div>
  );
}

/**
 * Prose from the backend with commands in backticks (`...`), rendered as a `→` note followed by 1
 * command block per backticked span. Plain text when there is no backtick.
 */
export function NextStep({ text }: { text: string }) {
  const parts = text.split("`");
  if (parts.length < 3) {
    return (
      <p className="text-muted-foreground text-xs [overflow-wrap:anywhere]">
        {text}
      </p>
    );
  }
  const prose = parts
    .filter((_, i) => i % 2 === 0)
    .map((s) => s.trim())
    .filter(Boolean)
    .join(" ");
  const commands = parts.filter((_, i) => i % 2 === 1);
  return (
    <div className="grid gap-2">
      {commands.map((command, i) => (
        <Command
          key={`${i}-${command}`}
          command={command}
          note={i === 0 ? prose : undefined}
        />
      ))}
    </div>
  );
}

/** A monospace line of `name: value` pairs, one per row, like an HTTP header block. */
export function Pairs({
  entries,
  className,
}: {
  entries: [string, React.ReactNode][];
  className?: string;
}) {
  if (entries.length === 0)
    return <span className="text-muted-foreground text-xs">—</span>;
  return (
    <dl
      className={cn(
        "grid grid-cols-[max-content_1fr] gap-x-3 gap-y-0.5 text-xs",
        className,
      )}
    >
      {entries.map(([name, value]) => (
        <div key={name} className="contents">
          <dt className="text-muted-foreground [overflow-wrap:anywhere]">
            {name}
          </dt>
          <dd className="min-w-0 [overflow-wrap:anywhere]">{value}</dd>
        </div>
      ))}
    </dl>
  );
}
