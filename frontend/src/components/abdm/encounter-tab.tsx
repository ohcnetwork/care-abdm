import {
  careContextQueryKey,
  formatDay,
  formatTime,
  hiTypeLabel,
  retryAfter,
  statusKey,
  toneFor,
  useCareContext,
  viewFor,
} from "@/components/abdm/care-context-state";
import FetchRecordsCard from "@/components/abdm/fetch-records-card";
import {
  HeroFact,
  HeroIcon,
  HeroLayers,
  heroBadge,
  heroCard,
  heroLead,
} from "@/components/abdm/hero";
import DevFooter from "@/components/abdm/dev/dev-footer";
import PluginComponent from "@/components/common/plugin-component";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { useTranslation } from "@/hooks/use-translation";
import careApi, {
  type AbdmCareContextState,
  type AbdmShareItem,
  type AbdmShareItemStatus,
} from "@/lib/careApi";
import { mutate } from "@/lib/request";
import { cn } from "@/lib/utils";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Link2, Loader2, Share2 } from "lucide-react";
import { useMemo, useState } from "react";

/**
 * Encounter tab "ABDM Records" (host `encounterTabs["abdm"]`, EncounterShow.tsx:192-200; the
 * host owns the label `ENCOUNTER_TAB__abdm`). ADR-013: every shareable record of the visit is
 * staged here; the desk selects records and links them, or excludes a record. When the visit is
 * completed or discharged the backend links every staged record by itself.
 *
 * Layout is append-only: the header card keeps its height, rows are added below, never
 * reshuffled. A failure is never hidden (ADR-012 D7).
 */

function errorMessage(error: unknown, fallback: string) {
  if (error && typeof error === "object" && "cause" in error) {
    const cause = (error as { cause?: Record<string, unknown> }).cause;
    const value = cause?.errors ?? cause?.message;
    if (typeof value === "string") return value;
  }
  return fallback;
}

const SELECTABLE: AbdmShareItemStatus[] = ["staged", "failed", "excluded"];

function itemTone(status: AbdmShareItemStatus) {
  if (status === "linked") return "success" as const;
  if (status === "queued") return "warning" as const;
  if (status === "failed") return "destructive" as const;
  return "neutral" as const;
}

function ItemRow({
  item,
  checked,
  onCheck,
  onToggleExclude,
  busy,
  t,
}: {
  item: AbdmShareItem;
  checked: boolean;
  onCheck: (checked: boolean) => void;
  onToggleExclude: () => void;
  busy: boolean;
  t: (key: string) => string;
}) {
  const selectable = SELECTABLE.includes(item.status);
  const next = item.nextAttemptAt ? new Date(item.nextAttemptAt) : null;
  return (
    <TableRow className={item.status === "excluded" ? "opacity-60" : undefined}>
      <TableCell className="w-8">
        <Checkbox
          checked={checked}
          disabled={!selectable || busy}
          onCheckedChange={(value) => onCheck(Boolean(value))}
          aria-label={item.label}
        />
      </TableCell>
      <TableCell>
        <div className="grid gap-0.5">
          <span>{item.label}</span>
          {item.failure && item.status !== "linked" && (
            <span className="text-destructive text-xs">
              {item.failure.what} {item.failure.nextStep}
            </span>
          )}
        </div>
      </TableCell>
      <TableCell className="whitespace-nowrap">
        {hiTypeLabel(t, item.hiType)}
      </TableCell>
      <TableCell>
        <div className="grid gap-0.5">
          <Badge variant={itemTone(item.status)} size="sm">
            {t(`abdm_item_status_${item.status}`)}
          </Badge>
          {item.status === "queued" && next && next.getTime() > Date.now() && (
            <span className="text-muted-foreground text-xs">
              {t("abdm_item_retry_at")} {formatTime(next)}
            </span>
          )}
          {item.status === "linked" && item.linkedAt && (
            <span className="text-muted-foreground text-xs">
              {formatDay(item.linkedAt)} {formatTime(new Date(item.linkedAt))}
            </span>
          )}
        </div>
      </TableCell>
      <TableCell className="text-muted-foreground text-xs tabular-nums">
        {item.attempts > 0 ? item.attempts : "\u2014"}
      </TableCell>
      <TableCell className="text-right">
        {(item.status === "staged" || item.status === "excluded") && (
          <Button
            type="button"
            variant="ghost"
            size="sm"
            disabled={busy}
            onClick={onToggleExclude}
          >
            {item.status === "excluded"
              ? t("abdm_item_include")
              : t("abdm_item_exclude")}
          </Button>
        )}
      </TableCell>
    </TableRow>
  );
}

export default function AbdmEncounterTab({
  encounter,
  patient,
}: {
  encounter: { id: string; facility: { id: string } };
  patient: { id: string };
}) {
  const { t } = useTranslation();
  const qc = useQueryClient();
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [actionError, setActionError] = useState<string>();
  const { data, isLoading, isError } = useCareContext(encounter.id);

  const apply = (next: AbdmCareContextState) => {
    qc.setQueryData(careContextQueryKey(encounter.id), next);
    setSelected(new Set());
  };
  const link = useMutation<
    AbdmCareContextState,
    unknown,
    { items?: string[]; all?: boolean }
  >({
    mutationFn: mutate(careApi.encounterCareContextLink, {
      pathParams: { encounterId: encounter.id },
      silent: true,
    }),
    onMutate: () => setActionError(undefined),
    onSuccess: apply,
    onError: (error) =>
      setActionError(errorMessage(error, t("abdm_cc_link_failed"))),
  });
  const toggle = useMutation<
    AbdmCareContextState,
    unknown,
    { itemId: string; action: "exclude" | "include" }
  >({
    mutationFn: ({ itemId, action }) =>
      mutate(careApi.shareItemAction, {
        pathParams: { encounterId: encounter.id, itemId, action },
        silent: true,
      })({}),
    onMutate: () => setActionError(undefined),
    onSuccess: apply,
    onError: (error) =>
      setActionError(errorMessage(error, t("abdm_item_action_failed"))),
  });

  const items = useMemo(() => data?.shareItems ?? [], [data?.shareItems]);
  const counts = useMemo(() => {
    const c: Record<AbdmShareItemStatus, number> = {
      staged: 0,
      queued: 0,
      linked: 0,
      failed: 0,
      excluded: 0,
    };
    for (const item of items) c[item.status] += 1;
    return c;
  }, [items]);
  const selectableIds = items
    .filter((i) => SELECTABLE.includes(i.status))
    .map((i) => i.id);
  const busy = link.isPending || toggle.isPending;
  const view = data ? viewFor(data) : undefined;
  const waitUntil = data ? retryAfter(data) : null;
  const canLink =
    Boolean(data?.facilityConfigured) &&
    Boolean(data?.patientAbhaAddress) &&
    !waitUntil;

  return (
    <PluginComponent>
      <div className="grid gap-4 p-1">
        {/*
         * Hero card. The visit summary carries the gradient, so the desk reads the
         * ABHA address and the share state first. `isolate` holds the decorative
         * layers in this card, and the card's own `overflow-hidden` trims them.
         */}
        <Card className={heroCard}>
          <HeroLayers />
          <CardHeader>
            <CardTitle className="flex items-center gap-3">
              <HeroIcon>
                <Link2 className="size-4.5 text-white" />
              </HeroIcon>
              <span className="text-base font-semibold text-white">
                {data?.careContext?.display ?? t("abdm_care_context")}
              </span>
              {view && (
                <Badge
                  variant={toneFor(view)}
                  size="sm"
                  className={cn("ml-auto", heroBadge)}
                >
                  {t(statusKey(view))}
                </Badge>
              )}
            </CardTitle>
            <CardDescription className={cn("max-w-3xl", heroLead)}>
              {t("abdm_tab_intro")}
            </CardDescription>
          </CardHeader>
          <CardContent className="grid gap-3 md:grid-cols-4">
            <HeroFact label={t("abdm_abha_address")} mono>
              {data?.patientAbhaAddress || "\u2014"}
            </HeroFact>
            <HeroFact label={t("abdm_cc_reference")} mono>
              {data?.careContext?.referenceNumber ?? "\u2014"}
            </HeroFact>
            <HeroFact label={t("abdm_tab_shared_types")}>
              {data?.careContext?.hiTypes.length
                ? data.careContext.hiTypes
                    .map((h) => hiTypeLabel(t, h))
                    .join(", ")
                : "\u2014"}
            </HeroFact>
            <HeroFact label={t("abdm_tab_counts")} className="tabular-nums">
              {counts.linked} {t("abdm_item_status_linked").toLowerCase()} ·{" "}
              {counts.staged} {t("abdm_item_status_staged").toLowerCase()} ·{" "}
              {counts.queued} {t("abdm_item_status_queued").toLowerCase()}
              {counts.failed > 0 &&
                ` · ${counts.failed} ${t("abdm_item_status_failed").toLowerCase()}`}
            </HeroFact>
          </CardContent>
          {(actionError ||
            isError ||
            data?.failure ||
            (data && !data.facilityConfigured) ||
            (data && !data.patientAbhaAddress)) && (
            <CardFooter className="grid gap-2 border-t border-white/15">
              {isError && (
                <Alert variant="destructive">
                  <AlertDescription>
                    {t("abdm_tab_load_failed")}
                  </AlertDescription>
                </Alert>
              )}
              {actionError && (
                <Alert variant="destructive">
                  <AlertDescription>{actionError}</AlertDescription>
                </Alert>
              )}
              {data && !data.facilityConfigured && (
                <Alert variant="warning">
                  <AlertDescription>
                    {t("abdm_cc_status_facility_not_setup")}
                  </AlertDescription>
                </Alert>
              )}
              {data && data.facilityConfigured && !data.patientAbhaAddress && (
                <Alert variant="warning">
                  <AlertDescription>{t("abdm_tab_no_abha")}</AlertDescription>
                </Alert>
              )}
              {data?.failure && (
                <Alert
                  variant={
                    data.failure.retry === "after" ? "warning" : "destructive"
                  }
                >
                  <AlertDescription className="grid gap-0.5">
                    <span>
                      {data.failure.what} {data.failure.nextStep}
                    </span>
                    {waitUntil && (
                      <span className="text-xs">
                        {t("abdm_cc_retry_after", {
                          time: formatTime(waitUntil),
                        })}
                      </span>
                    )}
                  </AlertDescription>
                </Alert>
              )}
            </CardFooter>
          )}
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Share2 className="text-muted-foreground size-4" />
              {t("abdm_tab_records")}
            </CardTitle>
            <CardDescription>
              {data?.encounterClosed
                ? t("abdm_tab_records_closed_help")
                : t("abdm_tab_records_help")}
            </CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <Skeleton className="h-32 w-full rounded-md" />
            ) : items.length === 0 ? (
              <p className="text-muted-foreground text-sm">
                {t("abdm_tab_no_records")}
              </p>
            ) : (
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-8">
                      <Checkbox
                        checked={
                          selectableIds.length > 0 &&
                          selectableIds.every((id) => selected.has(id))
                        }
                        disabled={selectableIds.length === 0 || busy}
                        onCheckedChange={(value) =>
                          setSelected(
                            value ? new Set(selectableIds) : new Set(),
                          )
                        }
                        aria-label={t("abdm_tab_select_all")}
                      />
                    </TableHead>
                    <TableHead>{t("abdm_tab_record")}</TableHead>
                    <TableHead>{t("abdm_cc_hi_types")}</TableHead>
                    <TableHead>{t("abdm_tab_status")}</TableHead>
                    <TableHead>{t("abdm_tab_attempts")}</TableHead>
                    <TableHead />
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {items.map((item) => (
                    <ItemRow
                      key={item.id}
                      item={item}
                      checked={selected.has(item.id)}
                      busy={busy}
                      t={t}
                      onCheck={(checked) =>
                        setSelected((prev) => {
                          const next = new Set(prev);
                          if (checked) next.add(item.id);
                          else next.delete(item.id);
                          return next;
                        })
                      }
                      onToggleExclude={() =>
                        toggle.mutate({
                          itemId: item.id,
                          action:
                            item.status === "excluded" ? "include" : "exclude",
                        })
                      }
                    />
                  ))}
                </TableBody>
              </Table>
            )}
          </CardContent>
          <CardFooter className="flex flex-wrap items-center gap-3 border-t">
            <span className="text-muted-foreground text-xs">
              {selected.size > 0
                ? `${selected.size} ${t("abdm_tab_selected")}`
                : t("abdm_tab_select_hint")}
            </span>
            <div className="ml-auto flex gap-2">
              <Button
                type="button"
                variant="outline"
                size="sm"
                disabled={
                  !canLink || busy || counts.staged + counts.failed === 0
                }
                onClick={() => link.mutate({ all: true })}
              >
                {t("abdm_tab_link_all")}
              </Button>
              <Button
                type="button"
                size="sm"
                disabled={!canLink || busy || selected.size === 0}
                onClick={() => link.mutate({ items: [...selected] })}
              >
                {busy ? (
                  <Loader2 className="size-4 animate-spin" />
                ) : (
                  <Share2 className="size-4" />
                )}
                {t("abdm_tab_link_selected")}
              </Button>
            </div>
          </CardFooter>
        </Card>

        {/* ADR-014: M3 as HIU. Consent requests are per patient; the entry point is the visit. */}
        <FetchRecordsCard
          patientId={patient.id}
          facilityId={encounter.facility.id}
        />
        {/* ADR-018: the developer entry, last and collapsed, so the tab above never moves. */}
        <DevFooter filters={{ encounter: encounter.id }} />
      </div>
    </PluginComponent>
  );
}
