import { Label } from "@/components/abdm/dev/console";
import { redactionMarker, useCopy } from "@/components/abdm/dev/dev-state";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useTranslation } from "@/hooks/use-translation";
import { cn } from "@/lib/utils";
import {
  Check,
  ChevronDown,
  ChevronRight,
  Copy,
  Lock,
  Search,
} from "lucide-react";
import { useMemo, useState } from "react";

/**
 * A collapsible JSON tree for the developer explorer (ADR-018). Written in the plug, on the console
 * skin: an editor's 4 value hues (`--console-key/string/number/keyword` in `style/index.css`), a
 * guide line per depth, and a hover row. A redaction marker (`<redacted, N chars>`,
 * `<encrypted, N chars>`, `<N chars, base64>`) renders as a dashed lock chip with the length, so a
 * reader sees that a value was there and how long it was, never the value (abdm-m2 design.md).
 *
 * Search filters keys and values (case-insensitive); a match keeps its ancestors open. Hover a row
 * to copy the JSON path or the value. "Raw" shows the pretty-printed text.
 */

type Json = null | boolean | number | string | Json[] | { [key: string]: Json };

function isObject(v: unknown): v is Record<string, Json> {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}

function pathJoin(base: string, key: string | number): string {
  if (typeof key === "number") return `${base}[${key}]`;
  return /^[A-Za-z_$][\w$]*$/.test(key)
    ? base
      ? `${base}.${key}`
      : key
    : `${base}["${key}"]`;
}

function matches(value: Json, key: string | number, needle: string): boolean {
  if (!needle) return true;
  if (String(key).toLowerCase().includes(needle)) return true;
  if (isObject(value))
    return Object.entries(value).some(([k, v]) => matches(v, k, needle));
  if (Array.isArray(value)) return value.some((v, i) => matches(v, i, needle));
  return String(value ?? "null")
    .toLowerCase()
    .includes(needle);
}

function Primitive({ value }: { value: Json }) {
  const marker = redactionMarker(value);
  if (marker) {
    return (
      <span className="border-strong-border text-muted-foreground inline-flex items-center gap-1 rounded border border-dashed px-1.5 text-[11px] leading-4">
        <Lock className="size-3" />
        {marker.kind} · {marker.chars} chars
      </span>
    );
  }
  if (value === null)
    return <span className="text-muted-foreground italic">null</span>;
  if (typeof value === "boolean")
    return (
      <span className="text-[color:var(--console-keyword)]">
        {String(value)}
      </span>
    );
  if (typeof value === "number")
    return (
      <span className="text-[color:var(--console-number)] tabular-nums">
        {value}
      </span>
    );
  return (
    <span className="[overflow-wrap:anywhere] text-[color:var(--console-string)]">
      &quot;{String(value)}&quot;
    </span>
  );
}

function Node({
  name,
  value,
  path,
  depth,
  needle,
  openAll,
  copy,
  copied,
  inset = 0,
}: {
  name: string | number | null;
  value: Json;
  path: string;
  depth: number;
  needle: string;
  openAll: boolean;
  copy: (id: string, text: string) => void;
  copied: string | null;
  /** Pixels the parent's guide line already took, so the row's indent is relative to it. */
  inset?: number;
}) {
  const { t } = useTranslation();
  const container = isObject(value) || Array.isArray(value);
  const entries: [string | number, Json][] = isObject(value)
    ? Object.entries(value)
    : Array.isArray(value)
      ? value.map((v, i) => [i, v] as [number, Json])
      : [];
  const [manual, setManual] = useState<boolean | null>(null);
  const open = manual ?? (openAll || depth < 2 || Boolean(needle));
  const label = name === null ? "" : String(name);
  const count = entries.length;
  const valueText = container
    ? JSON.stringify(value, null, 2)
    : String(value ?? "null");
  const row = (
    <div
      className="group/row flex min-w-0 items-start gap-1 rounded-sm px-1 py-px hover:bg-white/[0.05]"
      style={{ paddingLeft: `${depth * 14 + 4 - inset}px` }}
    >
      {container ? (
        <button
          type="button"
          className="text-muted-foreground mt-0.5 shrink-0"
          aria-label={open ? t("abdm_dev_collapse") : t("abdm_dev_expand")}
          onClick={() => setManual(!open)}
        >
          {open ? (
            <ChevronDown className="size-3.5" />
          ) : (
            <ChevronRight className="size-3.5" />
          )}
        </button>
      ) : (
        <span className="mt-0.5 size-3.5 shrink-0" />
      )}
      <span className="min-w-0 flex-1 [overflow-wrap:anywhere]">
        {name !== null && (
          <span
            className={cn(
              "text-[color:var(--console-key)]",
              typeof name === "number" && "text-muted-foreground",
            )}
          >
            {typeof name === "number" ? `[${name}]` : label}
            <span className="text-muted-foreground">: </span>
          </span>
        )}
        {container ? (
          <span className="text-muted-foreground">
            {Array.isArray(value) ? "[" : "{"}
            {!open && (
              <>
                {" "}
                {t("abdm_dev_items", { count })}{" "}
                {Array.isArray(value) ? "]" : "}"}
              </>
            )}
          </span>
        ) : (
          <Primitive value={value} />
        )}
      </span>
      <span className="invisible flex shrink-0 gap-0.5 group-focus-within/row:visible group-hover/row:visible">
        {path && (
          <Button
            type="button"
            variant="ghost"
            size="sm"
            className="h-5 px-1 text-[10px]"
            onClick={() => copy(`${path}:path`, path)}
            title={t("abdm_dev_copy_path")}
          >
            {copied === `${path}:path` ? (
              <Check className="size-3" />
            ) : (
              <Copy className="size-3" />
            )}
            {t("abdm_dev_path")}
          </Button>
        )}
        {!redactionMarker(value) && (
          <Button
            type="button"
            variant="ghost"
            size="sm"
            className="h-5 px-1 text-[10px]"
            onClick={() => copy(`${path}:value`, valueText)}
            title={t("abdm_dev_copy_value")}
          >
            {copied === `${path}:value` ? (
              <Check className="size-3" />
            ) : (
              <Copy className="size-3" />
            )}
            {t("abdm_dev_value")}
          </Button>
        )}
      </span>
    </div>
  );
  if (!container) return row;
  return (
    <div>
      {row}
      {open && (
        <div
          className="border-l border-white/[0.08]"
          style={{ marginLeft: `${depth * 14 + 10 - inset}px` }}
        >
          {entries
            .filter(([k, v]) => matches(v, k, needle))
            .map(([k, v]) => (
              <Node
                key={String(k)}
                name={k}
                value={v}
                path={pathJoin(path, k)}
                depth={depth + 1}
                needle={needle}
                openAll={openAll}
                copy={copy}
                copied={copied}
                inset={depth * 14 + 10}
              />
            ))}
          <div
            className="text-muted-foreground"
            style={{ paddingLeft: "12px" }}
          >
            {Array.isArray(value) ? "]" : "}"}
          </div>
        </div>
      )}
    </div>
  );
}

export default function JsonTree({
  value,
  title,
  className,
  defaultRaw = false,
  compact = false,
}: {
  value: unknown;
  title?: string;
  className?: string;
  defaultRaw?: boolean;
  /** No toolbar: for a small body inside a table cell or a footer. */
  compact?: boolean;
}) {
  const { t } = useTranslation();
  const [needle, setNeedle] = useState("");
  const [raw, setRaw] = useState(defaultRaw);
  const [openAll, setOpenAll] = useState(false);
  const { copied, copy } = useCopy();
  const json = (value ?? null) as Json;
  const text = useMemo(() => JSON.stringify(json, null, 2) ?? "null", [json]);
  const empty =
    json === null ||
    (isObject(json) && Object.keys(json).length === 0) ||
    (Array.isArray(json) && json.length === 0);
  return (
    <div className={cn("min-w-0 rounded-md border bg-black/20", className)}>
      {!compact && (
        <div className="flex flex-wrap items-center gap-2 border-b bg-white/[0.03] px-2 py-1.5">
          {title && <Label>{title}</Label>}
          <span className="text-muted-foreground text-[11px] tabular-nums">
            {text.length} chars
          </span>
          <div className="ml-auto flex items-center gap-1">
            {!raw && (
              <div className="relative">
                <Search className="text-muted-foreground absolute top-1/2 left-2 size-3 -translate-y-1/2" />
                <Input
                  value={needle}
                  onChange={(e) => setNeedle(e.target.value.toLowerCase())}
                  placeholder={t("abdm_dev_search_json")}
                  className="h-7 w-44 pl-6 font-mono text-xs md:h-7"
                />
              </div>
            )}
            {!raw && (
              <Button
                type="button"
                variant="ghost"
                size="sm"
                className="h-7 px-2 text-xs"
                onClick={() => setOpenAll((o) => !o)}
              >
                {openAll
                  ? t("abdm_dev_collapse_all")
                  : t("abdm_dev_expand_all")}
              </Button>
            )}
            <Button
              type="button"
              variant={raw ? "default" : "ghost"}
              size="sm"
              className="h-7 px-2 text-xs"
              onClick={() => setRaw((r) => !r)}
            >
              {t("abdm_dev_raw")}
            </Button>
            <Button
              type="button"
              variant="ghost"
              size="sm"
              className="h-7 px-2 text-xs"
              onClick={() => copy("__all", text)}
            >
              {copied === "__all" ? (
                <Check className="size-3" />
              ) : (
                <Copy className="size-3" />
              )}
              {t("abdm_dev_copy_json")}
            </Button>
          </div>
        </div>
      )}
      <div className="max-h-[32rem] overflow-auto p-2 font-mono text-xs leading-5">
        {empty ? (
          <span className="text-muted-foreground">
            {t("abdm_dev_empty_body")}
          </span>
        ) : raw ? (
          <pre className="[overflow-wrap:anywhere] whitespace-pre-wrap">
            {text}
          </pre>
        ) : (
          <Node
            key={openAll ? "open" : "closed"}
            name={null}
            value={json}
            path=""
            depth={0}
            needle={needle}
            openAll={openAll}
            copy={copy}
            copied={copied}
          />
        )}
      </div>
    </div>
  );
}
