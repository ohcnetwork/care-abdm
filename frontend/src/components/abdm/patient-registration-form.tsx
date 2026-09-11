import AbhaWizard, {
  type AbhaWizardResult,
  formatAbhaNumber,
} from "@/components/abdm/abha-wizard";
import PluginComponent from "@/components/common/plugin-component";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useTranslation } from "@/hooks/use-translation";
import careApi, { type AbhaAccountProfile } from "@/lib/careApi";
import { query } from "@/lib/request";
import { useQuery } from "@tanstack/react-query";
import { CheckCircle2, ShieldCheck, X } from "lucide-react";
import { useQueryParams } from "raviger";
import { useCallback, useEffect, useState } from "react";

/**
 * PatientRegistrationForm slot (care_fe/src/pluginTypes.ts:55-60); host mounts it
 * at PatientRegistration.tsx:410-416 and posts `extensions` from the form
 * (PatientRegistration.tsx:322-362 via useEntityExtensions.prepareForSubmit).
 *
 * We set `extensions.abdm.txn_id`; the backend post_save receiver
 * (abdm/signals.py) resolves that server-recorded transaction into the ABHA
 * identifiers. The ABHA number itself is never trusted from the browser.
 */
type HostForm = {
  setValue: (
    name: string,
    value: unknown,
    options?: { shouldDirty?: boolean },
  ) => void;
  getValues: (name: string) => unknown;
};

type Props = {
  form: HostForm;
  facilityId?: string;
  patientId?: string;
  submitForm?: () => void;
};

/** ABDM dob is observed as strings; try dd-mm-yyyy and yyyy-mm-dd, else leave. */
function toIsoDate(dob?: string): string | undefined {
  if (!dob) return undefined;
  const dmy = dob.match(/^(\d{1,2})[-/](\d{1,2})[-/](\d{4})$/);
  if (dmy)
    return `${dmy[3]}-${dmy[2].padStart(2, "0")}-${dmy[1].padStart(2, "0")}`;
  if (/^\d{4}-\d{2}-\d{2}$/.test(dob)) return dob;
  return undefined;
}

/** Account profile carries dob split into parts; prefer them when whole. */
function isoFromParts(p: AbhaAccountProfile): string | undefined {
  if (p.yearOfBirth && p.monthOfBirth && p.dayOfBirth) {
    return `${p.yearOfBirth}-${p.monthOfBirth.padStart(2, "0")}-${p.dayOfBirth.padStart(2, "0")}`;
  }
  return toIsoDate(p.dob);
}

const GENDER_MAP: Record<string, string> = {
  M: "male",
  F: "female",
  O: "transgender",
};

type QParams = { abdm_txn?: string };

export default function AbdmPatientRegistrationForm({
  form,
  patientId,
}: Props) {
  const { t } = useTranslation();
  const [open, setOpen] = useState(false);
  const [result, setResult] = useState<AbhaWizardResult>();
  const [{ abdm_txn }] = useQueryParams<QParams>();

  // Arrived from "Find by ABHA" on the search page: the login already happened,
  // read the server-side transaction back and prefill. The txnId is opaque and
  // the backend re-derives everything from its own record (signals.py).
  const handoff = useQuery({
    queryKey: ["abdm", "transaction", abdm_txn],
    queryFn: query(careApi.transaction, {
      pathParams: { txnId: abdm_txn ?? "" },
      silent: true,
    }),
    enabled: !!abdm_txn && !patientId && !result,
    retry: false,
  });

  const apply = useCallback(
    (r: AbhaWizardResult) => {
      setResult(r);
      const p = r.profile;
      if (p) {
        const name =
          p.name ??
          [p.firstName, p.middleName, p.lastName].filter(Boolean).join(" ");
        if (name) form.setValue("name", name, { shouldDirty: true });
        const iso = isoFromParts(p);
        if (iso) {
          form.setValue("age_or_dob", "dob");
          form.setValue("date_of_birth", iso, { shouldDirty: true });
        }
        if (p.gender && GENDER_MAP[p.gender]) {
          form.setValue("gender", GENDER_MAP[p.gender], { shouldDirty: true });
        }
        if (p.mobile) {
          form.setValue("phone_number", `+91${p.mobile}`, {
            shouldDirty: true,
          });
        }
        // Address/pincode only come from the account read-back (login flows).
        const address = [p.address, p.districtName, p.stateName]
          .filter(Boolean)
          .join(", ");
        if (address && !form.getValues("address")) {
          form.setValue("address", address, { shouldDirty: true });
        }
        if (p.pinCode && /^\d{6}$/.test(p.pinCode)) {
          form.setValue("pincode", Number(p.pinCode), { shouldDirty: true });
        }
      }
      form.setValue("extensions.abdm.txn_id", r.txnId, { shouldDirty: true });
    },
    [form],
  );

  useEffect(() => {
    const s = handoff.data;
    if (!s || result) return;
    apply({
      txnId: s.txnId,
      abhaNumber: s.ABHANumber,
      abhaAddress: s.preferredAbhaAddress,
      profile: s.profile,
      source: s.kind,
      existingPatient: s.existingPatient,
    });
  }, [handoff.data, result, apply]);

  // Editing an existing patient: the ABHA panel on the patient page owns linking.
  if (patientId) return null;

  const currentMobile = () => {
    const v = form.getValues("phone_number");
    return typeof v === "string" ? v.replace(/\D/g, "").slice(-10) : "";
  };

  const clear = () => {
    setResult(undefined);
    form.setValue("extensions.abdm.txn_id", undefined, { shouldDirty: true });
  };

  return (
    <PluginComponent>
      {result ? (
        <div className="flex items-center justify-between gap-3 rounded-xl border border-emerald-200 bg-emerald-50/60 p-3 dark:border-emerald-900 dark:bg-emerald-950/40">
          <div className="flex min-w-0 items-center gap-3">
            <CheckCircle2 className="size-5 shrink-0 text-emerald-600" />
            <div className="min-w-0 text-sm">
              <div className="flex items-center gap-2">
                <span className="font-semibold">{t("abdm_abha_ready")}</span>
                {(result.source === "enrol_aadhaar" ||
                  result.profile?.kycVerified) && (
                  <Badge variant="success" size="sm">
                    <ShieldCheck /> {t("abdm_kyc_verified")}
                  </Badge>
                )}
              </div>
              <div className="font-mono tracking-wider">
                {formatAbhaNumber(result.abhaNumber)}
                {result.abhaAddress && (
                  <span className="text-muted-foreground">
                    {" "}
                    · {result.abhaAddress}
                  </span>
                )}
              </div>
              <div className="text-muted-foreground text-xs">
                {t("abdm_will_link_on_save")}
              </div>
            </div>
          </div>
          <Button
            type="button"
            variant="ghost"
            size="icon-xs"
            onClick={clear}
            aria-label={t("abdm_remove")}
          >
            <X />
          </Button>
        </div>
      ) : (
        <div className="flex items-center justify-between gap-3 rounded-xl border p-3">
          <div className="text-sm">
            <div className="font-semibold">{t("abdm_abha")}</div>
            <div className="text-muted-foreground">
              {t("abdm_registration_hint")}
            </div>
          </div>
          <Button
            type="button"
            variant="outline"
            size="sm"
            onClick={() => setOpen(true)}
          >
            {t("abdm_add_abha")}
          </Button>
        </div>
      )}

      <AbhaWizard
        open={open}
        onOpenChange={setOpen}
        defaultMobile={currentMobile()}
        onComplete={apply}
      />
    </PluginComponent>
  );
}
