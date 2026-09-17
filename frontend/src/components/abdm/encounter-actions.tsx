import {
  careContextQueryKey,
  formatDay,
  formatTime,
  hiTypeLabel,
  retryAfter,
  useCareContext,
  viewFor,
} from "@/components/abdm/care-context-state";
import PluginComponent from "@/components/common/plugin-component";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { useTranslation } from "@/hooks/use-translation";
import careApi, { type AbdmCareContextState } from "@/lib/careApi";
import { mutate } from "@/lib/request";
import { cn } from "@/lib/utils";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { CheckCircle2, Loader2, Share2 } from "lucide-react";
import { useState } from "react";

/**
 * Slot: EncounterActions (pluginTypes.ts:46-49), mounted in the encounter summary
 * actions (summary-panel-actions.tab.tsx:95). The host passes a button className.
 * Opens a compact dialog: "Share this visit's records with the patient's ABHA". One
 * plain state per view (care-context-state.ts `viewFor`), one action, no codes.
 *
 * A failure is never hidden (ADR-012 D7): the dialog shows what happened and what to do, both
 * written by the backend. The support reference appears only when support needs it.
 */

function errorMessage(error: unknown, fallback: string) {
  if (error && typeof error === "object" && "cause" in error) {
    const cause = (error as { cause?: Record<string, unknown> }).cause;
    const value = cause?.errors ?? cause?.message;
    if (typeof value === "string") return value;
  }
  return fallback;
}

export default function AbdmEncounterActions({
  encounter,
  className,
}: {
  encounter: { id: string };
  className?: string;
}) {
  const { t } = useTranslation();
  const qc = useQueryClient();
  const [open, setOpen] = useState(false);
  const [actionError, setActionError] = useState<string>();
  const { data, isLoading } = useCareContext(encounter.id);
  const share = useMutation<AbdmCareContextState, unknown, Record<string, never>>({
    mutationFn: mutate(careApi.encounterCareContextLink, {
      pathParams: { encounterId: encounter.id },
      silent: true,
    }),
    onMutate: () => setActionError(undefined),
    onSuccess: (next) => qc.setQueryData(careContextQueryKey(encounter.id), next),
    onError: (error) =>
      setActionError(errorMessage(error, t("abdm_cc_share_failed"))),
  });
  if (isLoading || !data || !data.facilityConfigured) return null;
  const view = viewFor(data);
  const context = data.careContext;
  const failure = data.failure;
  const blockedUntil = retryAfter(data);
  const busy = share.isPending;
  const primaryLabel =
    view === "failed" || view === "waiting"
      ? t("abdm_cc_action_retry")
      : t("abdm_cc_action_share");
  const primaryDisabled =
    busy || view === "no_abha" || view === "in_progress" || blockedUntil !== null;
  return (
    <PluginComponent>
      <Button
        type="button"
        variant="outline"
        className={cn(className)}
        onClick={() => setOpen(true)}
      >
        <Share2 className="size-4" />
        {view === "shared" ? t("abdm_cc_action_shared") : t("abdm_cc_action_share")}
      </Button>
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Share2 className="size-4" />
              {t("abdm_cc_dialog_title")}
            </DialogTitle>
            <DialogDescription>{t("abdm_cc_explainer")}</DialogDescription>
          </DialogHeader>
          <div className="grid gap-4 text-sm">
            {view === "no_abha" && <p>{t("abdm_cc_no_abha")}</p>}
            {view === "no_records" && <p>{t("abdm_cc_no_records")}</p>}
            {view === "ready" && <p>{t("abdm_cc_ready")}</p>}
            {view === "in_progress" && (
              <p className="flex items-center gap-2">
                <Loader2 className="text-muted-foreground size-4 shrink-0 animate-spin" />
                {t("abdm_cc_in_progress")}
              </p>
            )}
            {view === "shared" && context && (
              <div className="grid gap-2">
                <p className="flex items-center gap-2">
                  <CheckCircle2 className="size-4 shrink-0 text-green-700" />
                  {context.linkedAt
                    ? t("abdm_cc_shared_on", { date: formatDay(context.linkedAt) })
                    : t("abdm_cc_status_shared")}
                </p>
                <div className="grid gap-1">
                  <span className="text-muted-foreground text-xs">
                    {t("abdm_cc_shared_items")}
                  </span>
                  <ul className="list-disc pl-5">
                    {context.hiTypes.map((hiType) => (
                      <li key={hiType}>{hiTypeLabel(t, hiType)}</li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
            {(view === "failed" || view === "waiting") && (
              <Alert variant={view === "waiting" ? "default" : "destructive"}>
                <AlertDescription className="grid gap-1">
                  <span>{failure?.what || t("abdm_cc_failed")}</span>
                  {blockedUntil ? (
                    <span>
                      {t("abdm_cc_retry_after", { time: formatTime(blockedUntil) })}
                    </span>
                  ) : (
                    failure?.nextStep && <span>{failure.nextStep}</span>
                  )}
                </AlertDescription>
              </Alert>
            )}
            {actionError && (
              <Alert variant="destructive">
                <AlertDescription>{actionError}</AlertDescription>
              </Alert>
            )}
            <div className="flex justify-end gap-2">
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => setOpen(false)}
              >
                {t("abdm_close")}
              </Button>
              {view === "shared" ? (
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  disabled={busy}
                  onClick={() => share.mutate({})}
                >
                  {t("abdm_cc_action_update")}
                </Button>
              ) : (
                <Button
                  type="button"
                  size="sm"
                  disabled={primaryDisabled}
                  onClick={() => share.mutate({})}
                >
                  {busy && <Loader2 className="size-4 animate-spin" />}
                  {primaryLabel}
                </Button>
              )}
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </PluginComponent>
  );
}
