import {
  careContextQueryKey,
  statusKey,
  toneFor,
  useCareContext,
} from "@/components/abdm/care-context-state";
import PluginComponent from "@/components/common/plugin-component";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { useTranslation } from "@/hooks/use-translation";
import careApi, { type AbdmCareContextState } from "@/lib/careApi";
import { mutate } from "@/lib/request";
import { cn } from "@/lib/utils";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Link2 } from "lucide-react";
import { useState } from "react";

/**
 * Slot: EncounterActions (pluginTypes.ts:46-49), mounted in the encounter summary
 * actions (summary-panel-actions.tab.tsx:95). The host passes a button className.
 * Opens a dialog that shows the care-context state and runs the link.
 */

function errorMessage(error: unknown, fallback: string) {
  if (error && typeof error === "object" && "cause" in error) {
    const cause = (error as { cause?: Record<string, unknown> }).cause;
    const value = cause?.errors ?? cause?.message;
    if (typeof value === "string") return value;
  }
  return fallback;
}

function Row({ label, value }: { label: string; value?: string | null }) {
  return (
    <div className="grid gap-0.5">
      <span className="text-muted-foreground text-xs">{label}</span>
      <span className="font-mono text-xs break-all">{value || "\u2014"}</span>
    </div>
  );
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
  const link = useMutation<AbdmCareContextState, unknown, Record<string, never>>({
    mutationFn: mutate(careApi.encounterCareContextLink, {
      pathParams: { encounterId: encounter.id },
      silent: true,
    }),
    onMutate: () => setActionError(undefined),
    onSuccess: (next) => qc.setQueryData(careContextQueryKey(encounter.id), next),
    onError: (error) =>
      setActionError(errorMessage(error, t("abdm_cc_link_failed"))),
  });
  if (isLoading || !data || !data.facilityConfigured) return null;
  const context = data.careContext;
  const canLink = Boolean(data.patientAbhaAddress);
  const isLinked = context?.status === "linked";
  return (
    <PluginComponent>
      <Button
        type="button"
        variant="outline"
        className={cn(className)}
        onClick={() => setOpen(true)}
      >
        <Link2 className="size-4" />
        {isLinked ? t("abdm_cc_action_linked") : t("abdm_cc_action_link")}
      </Button>
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Link2 className="size-4" />
              {t("abdm_care_context")}
            </DialogTitle>
          </DialogHeader>
          <div className="grid gap-4 text-sm">
            <div className="flex items-center justify-between gap-3">
              <span>{context?.display ?? t("abdm_cc_not_created")}</span>
              <Badge variant={toneFor(data)} size="sm">
                {t(statusKey(data))}
              </Badge>
            </div>
            <p className="text-muted-foreground text-xs">
              {t("abdm_cc_explainer")}
            </p>
            {actionError && (
              <Alert variant="destructive">
                <AlertDescription>{actionError}</AlertDescription>
              </Alert>
            )}
            {context?.errorMessage && context.status !== "linked" && (
              <Alert variant="warning">
                <AlertDescription>{context.errorMessage}</AlertDescription>
              </Alert>
            )}
            <div className="grid gap-3 sm:grid-cols-2">
              <Row label={t("abdm_abha_address")} value={data.patientAbhaAddress} />
              <Row
                label={t("abdm_cc_reference")}
                value={context?.referenceNumber}
              />
              <Row
                label={t("abdm_cc_hi_types")}
                value={context?.hiTypes.join(", ")}
              />
              <Row
                label={t("abdm_cc_linked_at")}
                value={
                  context?.linkedAt
                    ? new Date(context.linkedAt).toLocaleString()
                    : undefined
                }
              />
            </div>
            {data.activity.length > 0 && (
              <div className="grid gap-1">
                <span className="text-muted-foreground text-xs">
                  {t("abdm_cc_activity")}
                </span>
                <ul className="grid gap-1 font-mono text-[11px]">
                  {data.activity.map((row) => (
                    <li
                      key={row.requestId}
                      className="flex items-center justify-between gap-2 rounded border px-2 py-1"
                    >
                      <span className="truncate">{row.operationId}</span>
                      <span className="text-muted-foreground shrink-0">
                        {row.status}
                        {row.callbacks.length > 0 &&
                          ` \u00B7 ${row.callbacks.length} ${t("abdm_cc_callbacks")}`}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
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
              <Button
                type="button"
                size="sm"
                disabled={!canLink || link.isPending}
                onClick={() => link.mutate({})}
              >
                {isLinked ? t("abdm_cc_action_refresh") : t("abdm_cc_action_link_now")}
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </PluginComponent>
  );
}
