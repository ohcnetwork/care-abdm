import AbhaWizard, {
  type AbhaWizardResult,
  formatAbhaNumber,
  relayMessage,
} from "@/components/abdm/abha-wizard";
import PluginComponent from "@/components/common/plugin-component";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Skeleton } from "@/components/ui/skeleton";
import { useTranslation } from "@/hooks/use-translation";
import careApi, {
  type PatientAbhaStatus,
  patientAbhaCardUrl,
} from "@/lib/careApi";
import { getHeaders, mutate, query } from "@/lib/request";
import { cn } from "@/lib/utils";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { Copy, CreditCard, IdCard, Link2, ShieldCheck } from "lucide-react";
import { useEffect, useState } from "react";

/**
 * Shared ABHA panel for an existing patient. Mounted from two host slots:
 *  - PatientDetailsTabDemographyGeneralInfo (Demography.tsx:172) — full card
 *  - PatientHomeActions (PatientProfile.tsx:177) — compact button
 * Data: GET /api/abdm/patients/<id>/abha; link: POST .../abha/link {txn_id}.
 */

export const abhaQueryKey = (patientId: string) => [
  "abdm",
  "patient",
  patientId,
];

export function usePatientAbha(patientId: string) {
  return useQuery({
    queryKey: abhaQueryKey(patientId),
    queryFn: query(careApi.patientAbha, {
      pathParams: { patientId },
      silent: true,
    }),
    retry: false,
  });
}

/** Fetch the authenticated card binary into an object URL for <img>. */
function useAuthedImage(url: string | null) {
  const [src, setSrc] = useState<string>();
  const [error, setError] = useState<string>();
  useEffect(() => {
    if (!url) return;
    let objectUrl: string | undefined;
    const ctrl = new AbortController();
    setSrc(undefined);
    setError(undefined);
    fetch(new URL(url, window.CARE_API_URL), {
      headers: getHeaders(),
      signal: ctrl.signal,
    })
      .then(async (res) => {
        if (!res.ok) {
          const body = await res.json().catch(() => ({}));
          throw new Error(body.message ?? body.errors ?? `HTTP ${res.status}`);
        }
        const blob = await res.blob();
        objectUrl = URL.createObjectURL(blob);
        setSrc(objectUrl);
      })
      .catch((e) => {
        if (e.name !== "AbortError") setError(String(e.message ?? e));
      });
    return () => {
      ctrl.abort();
      if (objectUrl) URL.revokeObjectURL(objectUrl);
    };
  }, [url]);
  return { src, error };
}

function AbhaCardDialog({
  patientId,
  open,
  onOpenChange,
}: {
  patientId: string;
  open: boolean;
  onOpenChange: (o: boolean) => void;
}) {
  const { t } = useTranslation();
  const url = open ? patientAbhaCardUrl(patientId) : null;
  const { src, error } = useAuthedImage(url);
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-2xl">
        <DialogHeader>
          <DialogTitle>{t("abdm_abha_card")}</DialogTitle>
        </DialogHeader>
        <div className="flex min-h-48 items-center justify-center">
          {error ? (
            <p className="text-destructive text-sm">{error}</p>
          ) : src ? (
            <img
              src={src}
              alt={t("abdm_abha_card")}
              className="max-h-[70vh] w-auto rounded-lg"
            />
          ) : (
            <Skeleton className="h-64 w-full" />
          )}
        </div>
        {src && (
          <div className="flex justify-end">
            <Button asChild variant="outline" size="sm">
              <a href={src} download="abha-card.png">
                {t("abdm_download")}
              </a>
            </Button>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}

function useLinkAbha(patientId: string) {
  const qc = useQueryClient();
  const { t } = useTranslation();
  const [error, setError] = useState<string>();
  const m = useMutation<
    NonNullable<typeof careApi.patientAbhaLink.TResponse>,
    unknown,
    NonNullable<typeof careApi.patientAbhaLink.TRequest>
  >({
    mutationFn: mutate(careApi.patientAbhaLink, {
      pathParams: { patientId },
      silent: true,
    }),
    onMutate: () => setError(undefined),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: abhaQueryKey(patientId) });
      // Host caches (PatientProfile.tsx:44, PatientHome.tsx:84) hold identifiers/extensions.
      qc.invalidateQueries({ queryKey: ["patient", patientId] });
      qc.invalidateQueries({ queryKey: ["patient-verify"] });
    },
    onError: (e) => setError(relayMessage(e, t("abdm_error_generic"))),
  });
  return { ...m, error };
}

function CopyButton({ value }: { value: string }) {
  const { t } = useTranslation();
  const [copied, setCopied] = useState(false);
  return (
    <Button
      type="button"
      variant="ghost"
      size="icon-xs"
      aria-label={t("abdm_copy")}
      onClick={() => {
        navigator.clipboard?.writeText(value);
        setCopied(true);
        setTimeout(() => setCopied(false), 1200);
      }}
    >
      {copied ? <ShieldCheck className="text-emerald-600" /> : <Copy />}
    </Button>
  );
}

export function AbhaPanel({
  patientId,
  phoneNumber,
  canWrite,
  className,
}: {
  patientId: string;
  phoneNumber?: string | null;
  canWrite: boolean;
  className?: string;
}) {
  const { t } = useTranslation();
  const status = usePatientAbha(patientId);
  const link = useLinkAbha(patientId);
  const [wizard, setWizard] = useState(false);
  const [card, setCard] = useState(false);

  // The wizard only proves the ABHA; the link call is ours. Close the dialog when the link
  // succeeds — the panel below shows the result. A refusal keeps the dialog open and shows
  // the reason on the done step (`finishError`).
  const onComplete = (r: AbhaWizardResult) =>
    link.mutate({ txn_id: r.txnId }, { onSuccess: () => setWizard(false) });

  const s: PatientAbhaStatus | undefined = status.data;

  return (
    <div className={cn("pr-4 sm:col-span-2", className)}>
      <div className="rounded-xl border">
        <div className="flex items-center justify-between gap-3 border-b px-4 py-2.5">
          <div className="flex items-center gap-2 text-sm font-semibold whitespace-nowrap">
            <IdCard className="text-primary size-4" />
            {t("abdm_abha_short")}
            {s?.linked && s.kyc_verified && (
              <Badge variant="success" size="sm">
                <ShieldCheck /> {t("abdm_kyc_verified")}
              </Badge>
            )}
          </div>
          {s?.linked ? (
            <div className="flex items-center gap-1">
              <Button
                type="button"
                variant="outline"
                size="xs"
                disabled={!s.card_available}
                title={
                  s.card_available ? undefined : t("abdm_card_unavailable")
                }
                onClick={() => setCard(true)}
              >
                <CreditCard /> {t("abdm_abha_card")}
              </Button>
            </div>
          ) : (
            canWrite &&
            !status.isLoading && (
              <Button
                type="button"
                variant="default"
                size="xs"
                onClick={() => setWizard(true)}
              >
                <Link2 /> {t("abdm_link_abha")}
              </Button>
            )
          )}
        </div>

        <div className="px-4 py-3">
          {status.isLoading ? (
            <div className="grid gap-2">
              <Skeleton className="h-5 w-48" />
              <Skeleton className="h-4 w-32" />
            </div>
          ) : status.isError ? (
            <p className="text-muted-foreground text-sm">
              {t("abdm_status_unavailable")}
            </p>
          ) : s?.linked ? (
            <div className="grid gap-3 lg:grid-cols-2">
              <div>
                <div className="text-muted-foreground text-xs">
                  {t("abdm_abha_number")}
                </div>
                <div className="flex items-center gap-1 font-mono text-base font-semibold tracking-wider whitespace-nowrap">
                  {formatAbhaNumber(s.abha_number)}
                  {s.abha_number && <CopyButton value={s.abha_number} />}
                </div>
              </div>
              <div>
                <div className="text-muted-foreground text-xs">
                  {t("abdm_abha_address")}
                </div>
                <div className="flex items-center gap-1 font-mono text-sm">
                  {s.abha_address ?? "—"}
                  {s.abha_address && <CopyButton value={s.abha_address} />}
                </div>
              </div>
              {s.abha_linked_at && (
                <div className="text-muted-foreground text-xs lg:col-span-2">
                  {t("abdm_linked_on", {
                    date: new Date(s.abha_linked_at).toLocaleString(),
                    source: t(`abdm_source_${s.abha_source ?? "unknown"}`),
                  })}
                </div>
              )}
            </div>
          ) : (
            <p className="text-muted-foreground text-sm">
              {t("abdm_not_linked_hint")}
            </p>
          )}
          {link.error && (
            <p className="text-destructive mt-2 text-sm">{link.error}</p>
          )}
        </div>
      </div>

      <AbhaWizard
        open={wizard}
        onOpenChange={setWizard}
        defaultMobile={phoneNumber?.replace(/\D/g, "").slice(-10) ?? ""}
        onComplete={onComplete}
        finishing={link.isPending}
        finishError={link.error}
      />
      {card && (
        <AbhaCardDialog
          patientId={patientId}
          open
          onOpenChange={(o) => !o && setCard(false)}
        />
      )}
    </div>
  );
}

/** Minimal shape read from PatientRead (care_fe/src/types/emr/patient/patient.ts). */
type PatientLike = {
  id: string;
  phone_number?: string | null;
  permissions?: string[];
};

/** Slot: PatientDetailsTabDemographyGeneralInfo (pluginTypes.ts:62-66). */
export default function AbdmDemographyGeneralInfo({
  patientId,
  patientData,
}: {
  facilityId: string;
  patientId: string;
  patientData: PatientLike;
}) {
  // Object-level permissions come from the host (PatientRead.permissions). Superusers
  // may carry none (PermissionContext.tsx:38); the backend is the real gate (403).
  const canWrite =
    !patientData.permissions?.length ||
    patientData.permissions.includes("can_write_patient");
  return (
    <PluginComponent>
      <AbhaPanel
        patientId={patientId}
        phoneNumber={patientData.phone_number}
        canWrite={canWrite}
      />
    </PluginComponent>
  );
}
