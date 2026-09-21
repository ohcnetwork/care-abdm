import { formatAbhaNumber } from "@/components/abdm/abha-wizard";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Skeleton } from "@/components/ui/skeleton";
import { useTranslation } from "@/hooks/use-translation";
import careApi, { type AbdmProfileShare } from "@/lib/careApi";
import { mutate, query } from "@/lib/request";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Check, UserPlus, UserRound } from "lucide-react";

/**
 * Scan and Share inbox (SHARE_PATIENT_PROFILE_701). The gateway posted the
 * profile a person shared at a counter; the plug answered with a token
 * number (abdm/share/service.py). The desk opens the existing patient or
 * registers a new one, prefilled through `?abdm_txn=<txnId>`.
 *
 * Polls every 10 seconds while open. The list is append-only in time order,
 * so rows do not move when a new share arrives above them.
 */
export default function ProfileShareInbox({
  facilityId,
  open,
  onOpenChange,
  onOpenPatient,
  onRegister,
}: {
  facilityId: string;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onOpenPatient: (patientId: string) => void;
  onRegister: (txnId: string) => void;
}) {
  const { t } = useTranslation();
  const qc = useQueryClient();
  const key = ["abdm", "profile-shares", facilityId];

  const shares = useQuery({
    queryKey: key,
    queryFn: query(careApi.profileShares, {
      pathParams: { facilityId },
      silent: true,
    }),
    enabled: open,
    refetchInterval: open ? 10_000 : false,
  });

  const dismiss = useMutation<AbdmProfileShare, unknown, { shareId: string }>({
    mutationFn: ({ shareId }) =>
      mutate(careApi.dismissProfileShare, {
        pathParams: { facilityId, shareId },
        silent: true,
      })({}),
    onSuccess: () => qc.invalidateQueries({ queryKey: key }),
  });

  const rows = shares.data?.results ?? [];

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>{t("abdm_shared_profiles")}</DialogTitle>
          <DialogDescription>
            {t("abdm_shared_profiles_help")}
          </DialogDescription>
        </DialogHeader>

        {shares.isError && (
          <Alert variant="destructive">
            <AlertDescription>
              {t("abdm_shared_profiles_load_failed")}
            </AlertDescription>
          </Alert>
        )}

        {shares.isLoading ? (
          <div className="grid gap-2">
            <Skeleton className="h-20 w-full rounded-lg" />
            <Skeleton className="h-20 w-full rounded-lg" />
          </div>
        ) : rows.length === 0 ? (
          <p className="text-muted-foreground py-6 text-center text-sm">
            {t("abdm_no_shared_profiles")}
          </p>
        ) : (
          <ul className="grid max-h-[60vh] gap-2 overflow-y-auto">
            {rows.map((row) => (
              <ShareRow
                key={row.id}
                row={row}
                busy={dismiss.isPending}
                onOpenPatient={onOpenPatient}
                onRegister={onRegister}
                onDismiss={() => dismiss.mutate({ shareId: row.id })}
              />
            ))}
          </ul>
        )}
      </DialogContent>
    </Dialog>
  );
}

function ShareRow({
  row,
  busy,
  onOpenPatient,
  onRegister,
  onDismiss,
}: {
  row: AbdmProfileShare;
  busy: boolean;
  onOpenPatient: (patientId: string) => void;
  onRegister: (txnId: string) => void;
  onDismiss: () => void;
}) {
  const { t } = useTranslation();
  const p = row.profile;
  const rejected = row.status === "rejected";
  const time = new Date(row.receivedAt).toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
  });
  return (
    <li className="grid gap-2 rounded-lg border p-3 text-sm">
      <div className="flex items-start justify-between gap-2">
        <div className="grid gap-0.5">
          <span className="font-semibold">
            {p.name || row.abhaAddress || t("abdm_unknown_person")}
          </span>
          <span className="text-muted-foreground font-mono text-xs">
            {[
              formatAbhaNumber(row.abhaNumber) || row.abhaAddress,
              p.gender,
              p.dob,
              p.mobile,
            ]
              .filter(Boolean)
              .join(" · ")}
          </span>
        </div>
        <div className="flex shrink-0 flex-col items-end gap-1">
          {row.tokenNumber ? (
            <Badge variant="primary" size="lg">
              {row.tokenNumber}
            </Badge>
          ) : (
            <Badge variant={rejected ? "destructive" : "warning"}>
              {t(`abdm_share_status_${row.status}`)}
            </Badge>
          )}
          <span className="text-muted-foreground text-xs">
            {row.context} · {time}
          </span>
        </div>
      </div>
      {row.errorMessage && (
        <p className="text-destructive text-xs">{row.errorMessage}</p>
      )}
      <div className="flex flex-wrap justify-end gap-2">
        <Button
          type="button"
          variant="ghost"
          size="sm"
          disabled={busy}
          onClick={onDismiss}
        >
          <Check /> {t("abdm_dismiss_share")}
        </Button>
        {row.patient ? (
          <Button
            type="button"
            size="sm"
            onClick={() => onOpenPatient(row.patient as string)}
          >
            <UserRound /> {t("abdm_open_patient")}
          </Button>
        ) : row.txnId ? (
          <Button
            type="button"
            size="sm"
            onClick={() => onRegister(row.txnId as string)}
          >
            <UserPlus /> {t("abdm_register_with_abha")}
          </Button>
        ) : null}
      </div>
    </li>
  );
}
