import AbhaWizard, {
  type AbhaWizardResult,
  formatAbhaNumber,
} from "@/components/abdm/abha-wizard";
import ProfileShareInbox from "@/components/abdm/profile-share-inbox";
import PluginComponent from "@/components/common/plugin-component";
import { Button } from "@/components/ui/button";
import { useTranslation } from "@/hooks/use-translation";
import { IdCard, QrCode, UserPlus, UserRound } from "lucide-react";
import { navigate } from "raviger";
import { useState } from "react";

/**
 * Slot: PatientSearchActions (care_fe/src/pluginTypes.ts:73-76), mounted next to
 * "Add patient" on the patient search page (PatientIndex.tsx:259-266) with a
 * primary-button className supplied by the host.
 *
 * Front-desk use case: the patient hands over an ABHA card / knows their ABHA
 * address / has their ABDM mobile. We log them into ABDM (OTP), then:
 *  - if a Care patient already carries that ABHA -> open them (no duplicate),
 *  - otherwise -> registration form, prefilled from the ABHA profile via
 *    `?abdm_txn=<txnId>` (consumed by patient-registration-form.tsx).
 * The ABHA number is never typed into Care's own search box: it is verified by
 * ABDM before we trust it, and identifiers are only written server-side.
 *
 * "Shared profiles" opens the Scan and Share inbox (profile-share-inbox.tsx):
 * profiles that people shared by scanning a counter QR code in the PHR app.
 */
export default function AbdmPatientSearchActions({
  facilityId,
}: {
  facilityId: string;
}) {
  const { t } = useTranslation();
  const [open, setOpen] = useState(false);
  const [inboxOpen, setInboxOpen] = useState(false);

  // Both dialogs hand the desk to another page. Close them first, or the dialog stays over
  // the new page until the route change removes it.
  const closeDialogs = () => {
    setOpen(false);
    setInboxOpen(false);
  };

  const openPatient = (id: string) => {
    closeDialogs();
    navigate(`/facility/${facilityId}/patient/${id}`);
  };
  const registerTxn = (txnId: string) => {
    closeDialogs();
    navigate(
      `/facility/${facilityId}/patient/create?abdm_txn=${encodeURIComponent(txnId)}`,
    );
  };
  const register = (r: AbhaWizardResult) => registerTxn(r.txnId);

  return (
    <PluginComponent>
      <Button type="button" variant="tertiary" onClick={() => setOpen(true)}>
        <IdCard />
        {t("abdm_find_by_abha")}
      </Button>
      <Button
        type="button"
        variant="tertiary"
        onClick={() => setInboxOpen(true)}
      >
        <QrCode />
        {t("abdm_shared_profiles")}
      </Button>
      <ProfileShareInbox
        facilityId={facilityId}
        open={inboxOpen}
        onOpenChange={setInboxOpen}
        onOpenPatient={openPatient}
        onRegister={registerTxn}
      />
      <AbhaWizard
        open={open}
        onOpenChange={setOpen}
        initialMode="link"
        initialHint="abha-number"
        onComplete={() => undefined}
        renderDone={(r) => {
          const existing = r.existingPatient;
          return {
            body: existing ? (
              <div className="rounded-lg border p-3 text-sm">
                <div className="text-muted-foreground text-xs">
                  {t("abdm_existing_patient")}
                </div>
                <div className="font-semibold">{existing.name}</div>
                <div className="text-muted-foreground font-mono text-xs">
                  {[
                    existing.phone_number,
                    existing.date_of_birth ??
                      (existing.year_of_birth
                        ? String(existing.year_of_birth)
                        : null),
                    existing.gender,
                  ]
                    .filter(Boolean)
                    .join(" · ")}
                </div>
              </div>
            ) : (
              <p className="text-muted-foreground text-center text-sm">
                {t("abdm_no_patient_for_abha", {
                  abha: formatAbhaNumber(r.abhaNumber) || r.abhaAddress,
                })}
              </p>
            ),
            footer: existing ? (
              <>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => register(r)}
                >
                  <UserPlus /> {t("abdm_register_anyway")}
                </Button>
                <Button type="button" onClick={() => openPatient(existing.id)}>
                  <UserRound /> {t("abdm_open_patient")}
                </Button>
              </>
            ) : (
              <Button type="button" onClick={() => register(r)}>
                <UserPlus /> {t("abdm_register_with_abha")}
              </Button>
            ),
          };
        }}
      />
    </PluginComponent>
  );
}
