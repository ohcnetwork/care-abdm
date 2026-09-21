import {
  embeddedCard,
  errorMessage,
  hprQueryKey,
} from "@/components/abdm/nhpr-shared";
import MasterSelect from "@/components/abdm/master-select";
import { selectClass } from "@/components/abdm/nhpr-shared";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import NhprField from "@/components/abdm/nhpr-field";
import { Input } from "@/components/ui/input";
import { useTranslation } from "@/hooks/use-translation";
import careApi, { type AbdmHprState } from "@/lib/careApi";
import { mutate } from "@/lib/request";
import { cn } from "@/lib/utils";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { FileText, Loader2, Plus, Trash2 } from "lucide-react";
import { useMemo, useState } from "react";

/**
 * Register professional (ADR-015, M4 journey 2): the full `practitioner` block of
 * `m4-enrollment/01`, 5 blocks, coded fields from the HPR masters, certificates as base64. The plug
 * wraps it with the person's `hprToken` and passes only the documented top-level keys. Fields the
 * docs type as a code without a master call (salutation, category, work status) are free text with
 * the example value as the hint (docs/findings.md N6).
 */

type Json = Record<string, unknown>;
type Attachment = { fileType: string; data: string };

const EMPTY_REGISTRATION: Json = {
  registeredWithCouncil: "",
  registrationNumber: "",
  registrationDate: "",
  registrationCertificate: { fileType: "", data: "" },
  isPermanentOrRenewable: "Permanent",
  renewableDueDate: "",
  categoryId: "",
  isNameDifferentInCertificate: "false",
  proofOfNameChangeCertificate: "",
  qualifications: [],
};
const EMPTY_QUALIFICATION: Json = {
  nameOfDegreeOrDiplomaObtained: "",
  country: "356",
  state: "",
  college: "",
  university: "",
  yearOfAwardingDegreeDiploma: "",
  monthOfAwardingDegreeDiploma: "",
  degreeCertificate: { fileType: "", data: "" },
  isNameDifferentInCertificate: "false",
  proofOfNameChangeCertificate: "",
};
const MONTHS = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

function fileToAttachment(file: File): Promise<Attachment> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () =>
      resolve({
        fileType: (file.name.split(".").pop() || "pdf").toLowerCase(),
        data: String(reader.result).split(",")[1] ?? "",
      });
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(file);
  });
}

const F = NhprField;

function Txt({
  id,
  value,
  onChange,
  placeholder,
  type,
}: {
  id: string;
  value: unknown;
  onChange: (v: string) => void;
  placeholder?: string;
  type?: string;
}) {
  return (
    <Input
      id={id}
      type={type ?? "text"}
      value={String(value ?? "")}
      placeholder={placeholder}
      onChange={(e) => onChange(e.target.value)}
    />
  );
}

function Sel({
  id,
  value,
  onChange,
  options,
}: {
  id: string;
  value: unknown;
  onChange: (v: string) => void;
  options: { code: string; name: string }[];
}) {
  return (
    <select
      id={id}
      className={selectClass}
      value={String(value ?? "")}
      onChange={(e) => onChange(e.target.value)}
    >
      <option value="">—</option>
      {options.map((o) => (
        <option key={o.code} value={o.code}>
          {o.name}
        </option>
      ))}
    </select>
  );
}

function FileField({
  id,
  labelKey,
  value,
  onChange,
  accept = "application/pdf,image/png,image/jpeg",
  t,
}: {
  id: string;
  labelKey: string;
  value: Attachment | string | undefined;
  onChange: (v: Attachment) => void;
  accept?: string;
  t: (k: string) => string;
}) {
  const has = typeof value === "string" ? Boolean(value) : Boolean(value?.data);
  return (
    <F
      labelKey={labelKey}
      htmlFor={id}
      hint={has ? t("abdm_hpr_file_attached") : t("abdm_hpr_file_help")}
    >
      <Input
        id={id}
        type="file"
        accept={accept}
        onChange={async (e) => {
          const file = e.target.files?.[0];
          if (!file || file.size > 5 * 1024 * 1024) return;
          onChange(await fileToAttachment(file));
        }}
      />
    </F>
  );
}

const YES_NO = (t: (k: string) => string) => [
  { code: "true", name: t("abdm_yes") },
  { code: "false", name: t("abdm_no") },
];

export default function HprRegisterForm({
  state,
  onDone,
  embedded,
}: {
  state: AbdmHprState;
  onDone?: () => void;
  /** True when a sheet holds this form: the sheet header carries the title (ADR-017). */
  embedded?: boolean;
}) {
  const { t } = useTranslation();
  const qc = useQueryClient();
  const account = state.profile?.account ?? {};
  const [error, setError] = useState<string>();
  const [form, setForm] = useState<Json>(() => ({
    healthProfessionalType: "doctor",
    profilePhoto: "",
    officialMobileCode: "+91",
    officialMobile: String(account.mobile ?? "").replace(/\*/g, ""),
    officialMobileStatus: "",
    officialEmail: String(account.email ?? ""),
    officialEmailStatus: "",
    visibleProfilePicture: "0",
    profileVisibleToPublic: "1",
    personalInformation: {
      salutation: "",
      firstName: String(
        account.firstName ?? state.profile?.name?.split(" ")[0] ?? "",
      ),
      middleName: String(account.middleName ?? ""),
      lastName: String(account.lastName ?? ""),
      nationality: "356",
      fatherName: "",
      motherName: "",
      spouseName: "",
      gender: String(account.gender ?? ""),
      dateOfBirth: account.yearOfBirth
        ? `${account.yearOfBirth}-${String(account.monthOfBirth ?? "01").padStart(2, "0")}-${String(account.dayOfBirth ?? "01").padStart(2, "0")}`
        : "",
      placeOfBirthState: String(account.stateCode ?? ""),
      district: String(account.districtCode ?? ""),
      subDistrict: "",
      city: "",
      languagesSpoken: "",
      category: "",
    },
    addressAsPerKYC: String(account.address ?? ""),
    communicationAddress: {
      isCommunicationAddressAsPerKYC: "true",
      address: "",
      name: "",
      country: "356",
      state: "",
      district: "",
      subDistrict: "",
      city: "",
      pincode: "",
    },
    contactInformation: {
      publicMobileNumber: "",
      publicMobileNumberCode: "",
      publicMobileNumberStatus: "",
      landLineNumber: "",
      landLineNumberCode: "",
      publicEmail: "",
      publicEmailStatus: "",
    },
    registrationAcademic: {
      category: String(state.profile?.categoryCode ?? "1"),
      registrationData: [
        {
          ...EMPTY_REGISTRATION,
          registrationNumber: state.careUser.councilRegistration,
          qualifications: [{ ...EMPTY_QUALIFICATION }],
        },
      ],
    },
    currentWorkDetails: {
      currentlyWorking: "1",
      purposeOfWork: "",
      chooseWorkStatus: "",
      reasonForNotWorking: "",
      certificateAttachment: "",
      facilityDeclarationData: {
        facilityId: "",
        facilityName: "",
        facilityAddress: "",
        facilityPincode: "",
        state: "",
        district: "",
        facilityType: "",
        facilityDepartment: "",
        facilityDesignation: "",
        ministry: { ministry: "" },
      },
    },
  }));

  const set = (path: string[], value: unknown) =>
    setForm((f) => {
      const next: Json = structuredClone(f);
      let node: Json = next;
      for (const key of path.slice(0, -1)) {
        node[key] =
          typeof node[key] === "object" && node[key] !== null ? node[key] : {};
        node = node[key] as Json;
      }
      node[path[path.length - 1]] = value;
      return next;
    });
  const get = (path: string[]): unknown =>
    path.reduce<unknown>(
      (node, key) =>
        node && typeof node === "object" ? (node as Json)[key] : undefined,
      form,
    );
  const personal = form.personalInformation as Json;
  const comm = form.communicationAddress as Json;
  const contact = form.contactInformation as Json;
  const academic = form.registrationAcademic as Json;
  const registrations = useMemo(
    () => (academic.registrationData as Json[]) ?? [],
    [academic.registrationData],
  );
  const work = form.currentWorkDetails as Json;
  const declaration = (work.facilityDeclarationData as Json) ?? {};
  const isUpdate = Boolean(state.profile?.registeredAt);

  const register = useMutation<AbdmHprState, unknown, void>({
    mutationFn: () =>
      mutate(isUpdate ? careApi.hprRegisterUpdate : careApi.hprRegister, {
        silent: true,
      })({ practitioner: form }),
    onMutate: () => setError(undefined),
    onSuccess: (next) => {
      qc.setQueryData(hprQueryKey, next);
      onDone?.();
    },
    onError: (e) => setError(errorMessage(e, t("abdm_hpr_register_failed"))),
  });
  const busy = register.isPending;
  const complete = useMemo(
    () =>
      Boolean(personal.firstName) &&
      registrations.length > 0 &&
      registrations.every(
        (r) =>
          r.registeredWithCouncil &&
          r.registrationNumber &&
          (r.registrationCertificate as Attachment)?.data,
      ),
    [personal.firstName, registrations],
  );
  const hprType = String(form.healthProfessionalType ?? "doctor");
  const councilKind =
    hprType === "nurse" ? "nurse-councils" : "medical-councils";
  // The courses master takes the system of medicine by name (m4-utility/08), so the picked
  // sub-category's display name is kept beside its code.
  const [somCode, setSomCode] = useState("");
  const [somName, setSomName] = useState("");

  return (
    <Card className={cn(embedded && embeddedCard.card)}>
      {!embedded && (
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <FileText className="text-muted-foreground size-4" />{" "}
            {isUpdate
              ? t("abdm_hpr_update_title")
              : t("abdm_hpr_register_title")}
          </CardTitle>
          <CardDescription>{t("abdm_hpr_register_intro")}</CardDescription>
        </CardHeader>
      )}
      <CardContent
        className={cn("grid gap-5", embedded && embeddedCard.padding)}
      >
        <section className="grid gap-3">
          <h3 className="text-sm font-semibold">
            {t("abdm_hpr_block_profile")}
          </h3>
          <div className="grid gap-3 sm:grid-cols-3">
            <F labelKey="abdm_hpr_type" htmlFor="r-type">
              <Sel
                id="r-type"
                value={form.healthProfessionalType}
                onChange={(v) => set(["healthProfessionalType"], v)}
                options={["doctor", "nurse", "pharmacist"].map((c) => ({
                  code: c,
                  name: t(`abdm_hpr_type_${c}`),
                }))}
              />
            </F>
            <F labelKey="abdm_hpr_official_mobile" htmlFor="r-mobile">
              <Txt
                id="r-mobile"
                value={form.officialMobile}
                onChange={(v) => set(["officialMobile"], v)}
              />
            </F>
            <F labelKey="abdm_hpr_official_email" htmlFor="r-email">
              <Txt
                id="r-email"
                type="email"
                value={form.officialEmail}
                onChange={(v) => set(["officialEmail"], v)}
              />
            </F>
            <F labelKey="abdm_hpr_visible_public" htmlFor="r-vis">
              <Sel
                id="r-vis"
                value={form.profileVisibleToPublic}
                onChange={(v) => set(["profileVisibleToPublic"], v)}
                options={[
                  { code: "1", name: t("abdm_yes") },
                  { code: "0", name: t("abdm_no") },
                ]}
              />
            </F>
            <F labelKey="abdm_hpr_visible_photo" htmlFor="r-visp">
              <Sel
                id="r-visp"
                value={form.visibleProfilePicture}
                onChange={(v) => set(["visibleProfilePicture"], v)}
                options={[
                  { code: "1", name: t("abdm_yes") },
                  { code: "0", name: t("abdm_no") },
                ]}
              />
            </F>
            <FileField
              id="r-photo"
              labelKey="abdm_hpr_profile_photo"
              accept="image/png,image/jpeg"
              value={String(form.profilePhoto ?? "")}
              onChange={(a) => set(["profilePhoto"], a.data)}
              t={t}
            />
          </div>
        </section>

        <section className="grid gap-3">
          <h3 className="text-sm font-semibold">
            {t("abdm_hpr_block_personal")}
          </h3>
          <div className="grid gap-3 sm:grid-cols-3">
            <F
              labelKey="abdm_hpr_salutation"
              htmlFor="p-sal"
              hint={t("abdm_hpr_code_hint", { example: "1" })}
            >
              <Txt
                id="p-sal"
                value={personal.salutation}
                onChange={(v) => set(["personalInformation", "salutation"], v)}
              />
            </F>
            <F labelKey="abdm_hpid_first_name" htmlFor="p-first">
              <Txt
                id="p-first"
                value={personal.firstName}
                onChange={(v) => set(["personalInformation", "firstName"], v)}
              />
            </F>
            <F labelKey="abdm_hpid_middle_name" htmlFor="p-middle">
              <Txt
                id="p-middle"
                value={personal.middleName}
                onChange={(v) => set(["personalInformation", "middleName"], v)}
              />
            </F>
            <F labelKey="abdm_hpid_last_name" htmlFor="p-last">
              <Txt
                id="p-last"
                value={personal.lastName}
                onChange={(v) => set(["personalInformation", "lastName"], v)}
              />
            </F>
            <F labelKey="abdm_hpr_gender" htmlFor="p-gender">
              <Sel
                id="p-gender"
                value={personal.gender}
                onChange={(v) => set(["personalInformation", "gender"], v)}
                options={[
                  { code: "M", name: t("abdm_gender_m") },
                  { code: "F", name: t("abdm_gender_f") },
                  { code: "O", name: t("abdm_gender_o") },
                ]}
              />
            </F>
            <F labelKey="abdm_hpr_dob" htmlFor="p-dob">
              <Txt
                id="p-dob"
                type="date"
                value={personal.dateOfBirth}
                onChange={(v) => set(["personalInformation", "dateOfBirth"], v)}
              />
            </F>
            <F labelKey="abdm_hpr_nationality" htmlFor="p-nat">
              <MasterSelect
                id="p-nat"
                kind="countries"
                value={String(personal.nationality ?? "")}
                onChange={(v) => set(["personalInformation", "nationality"], v)}
              />
            </F>
            <F labelKey="abdm_hpr_place_of_birth_state" htmlFor="p-state">
              <MasterSelect
                id="p-state"
                kind="hpr-states"
                value={String(personal.placeOfBirthState ?? "")}
                onChange={(v) => {
                  set(["personalInformation", "placeOfBirthState"], v);
                  set(["personalInformation", "district"], "");
                }}
              />
            </F>
            <F labelKey="abdm_hfr_district" htmlFor="p-district">
              <MasterSelect
                id="p-district"
                kind="hpr-districts"
                params={{ state: String(personal.placeOfBirthState ?? "") }}
                enabled={Boolean(personal.placeOfBirthState)}
                value={String(personal.district ?? "")}
                onChange={(v) => set(["personalInformation", "district"], v)}
              />
            </F>
            <F labelKey="abdm_hfr_subdistrict" htmlFor="p-sub">
              <MasterSelect
                id="p-sub"
                kind="hpr-subdistricts"
                params={{ district: String(personal.district ?? "") }}
                enabled={Boolean(personal.district)}
                value={String(personal.subDistrict ?? "")}
                onChange={(v) => set(["personalInformation", "subDistrict"], v)}
              />
            </F>
            <F labelKey="abdm_hpr_city" htmlFor="p-city">
              <Txt
                id="p-city"
                value={personal.city}
                onChange={(v) => set(["personalInformation", "city"], v)}
              />
            </F>
            <F
              labelKey="abdm_hpr_languages"
              htmlFor="p-lang"
              hint={t("abdm_hfr_multi_hint")}
            >
              <MasterSelect
                id="p-lang"
                kind="languages"
                multiple
                value={String(personal.languagesSpoken ?? "")
                  .split(",")
                  .filter(Boolean)}
                onChange={(v) =>
                  set(["personalInformation", "languagesSpoken"], v)
                }
              />
            </F>
            <F
              labelKey="abdm_hpr_category"
              htmlFor="p-cat"
              hint={t("abdm_hpr_code_hint", { example: "C" })}
            >
              <Txt
                id="p-cat"
                value={personal.category}
                onChange={(v) => set(["personalInformation", "category"], v)}
              />
            </F>
            <F labelKey="abdm_hpr_father" htmlFor="p-father">
              <Txt
                id="p-father"
                value={personal.fatherName}
                onChange={(v) => set(["personalInformation", "fatherName"], v)}
              />
            </F>
            <F labelKey="abdm_hpr_mother" htmlFor="p-mother">
              <Txt
                id="p-mother"
                value={personal.motherName}
                onChange={(v) => set(["personalInformation", "motherName"], v)}
              />
            </F>
            <F labelKey="abdm_hpr_spouse" htmlFor="p-spouse">
              <Txt
                id="p-spouse"
                value={personal.spouseName}
                onChange={(v) => set(["personalInformation", "spouseName"], v)}
              />
            </F>
          </div>
        </section>

        <section className="grid gap-3">
          <h3 className="text-sm font-semibold">
            {t("abdm_hpr_block_address")}
          </h3>
          <div className="grid gap-3 sm:grid-cols-3">
            <F labelKey="abdm_hpr_address_kyc" htmlFor="a-kyc">
              <Txt
                id="a-kyc"
                value={form.addressAsPerKYC}
                onChange={(v) => set(["addressAsPerKYC"], v)}
              />
            </F>
            <F labelKey="abdm_hpr_same_as_kyc" htmlFor="a-same">
              <Sel
                id="a-same"
                value={comm.isCommunicationAddressAsPerKYC}
                onChange={(v) =>
                  set(
                    ["communicationAddress", "isCommunicationAddressAsPerKYC"],
                    v,
                  )
                }
                options={YES_NO(t)}
              />
            </F>
          </div>
          {comm.isCommunicationAddressAsPerKYC === "false" && (
            <div className="grid gap-3 sm:grid-cols-3">
              <F labelKey="abdm_hfr_address" htmlFor="a-addr">
                <Txt
                  id="a-addr"
                  value={comm.address}
                  onChange={(v) => set(["communicationAddress", "address"], v)}
                />
              </F>
              <F labelKey="abdm_hpr_address_name" htmlFor="a-name">
                <Txt
                  id="a-name"
                  value={comm.name}
                  onChange={(v) => set(["communicationAddress", "name"], v)}
                />
              </F>
              <F labelKey="abdm_hpr_country" htmlFor="a-country">
                <MasterSelect
                  id="a-country"
                  kind="countries"
                  value={String(comm.country ?? "")}
                  onChange={(v) => set(["communicationAddress", "country"], v)}
                />
              </F>
              <F labelKey="abdm_hfr_state" htmlFor="a-state">
                <MasterSelect
                  id="a-state"
                  kind="hpr-states"
                  value={String(comm.state ?? "")}
                  onChange={(v) => {
                    set(["communicationAddress", "state"], v);
                    set(["communicationAddress", "district"], "");
                  }}
                />
              </F>
              <F labelKey="abdm_hfr_district" htmlFor="a-district">
                <MasterSelect
                  id="a-district"
                  kind="hpr-districts"
                  params={{ state: String(comm.state ?? "") }}
                  enabled={Boolean(comm.state)}
                  value={String(comm.district ?? "")}
                  onChange={(v) => set(["communicationAddress", "district"], v)}
                />
              </F>
              <F labelKey="abdm_hfr_subdistrict" htmlFor="a-sub">
                <MasterSelect
                  id="a-sub"
                  kind="hpr-subdistricts"
                  params={{ district: String(comm.district ?? "") }}
                  enabled={Boolean(comm.district)}
                  value={String(comm.subDistrict ?? "")}
                  onChange={(v) =>
                    set(["communicationAddress", "subDistrict"], v)
                  }
                />
              </F>
              <F labelKey="abdm_hpr_city" htmlFor="a-city">
                <Txt
                  id="a-city"
                  value={comm.city}
                  onChange={(v) => set(["communicationAddress", "city"], v)}
                />
              </F>
              <F labelKey="abdm_hfr_pincode" htmlFor="a-pin">
                <Txt
                  id="a-pin"
                  value={comm.pincode}
                  onChange={(v) => set(["communicationAddress", "pincode"], v)}
                />
              </F>
            </div>
          )}
        </section>

        <section className="grid gap-3">
          <h3 className="text-sm font-semibold">
            {t("abdm_hpr_block_contact")}
          </h3>
          <div className="grid gap-3 sm:grid-cols-3">
            <F labelKey="abdm_hpr_public_mobile" htmlFor="c-mob">
              <Txt
                id="c-mob"
                value={contact.publicMobileNumber}
                onChange={(v) =>
                  set(["contactInformation", "publicMobileNumber"], v)
                }
              />
            </F>
            <F labelKey="abdm_hfr_landline" htmlFor="c-land">
              <Txt
                id="c-land"
                value={contact.landLineNumber}
                onChange={(v) =>
                  set(["contactInformation", "landLineNumber"], v)
                }
              />
            </F>
            <F labelKey="abdm_hpr_public_email" htmlFor="c-email">
              <Txt
                id="c-email"
                type="email"
                value={contact.publicEmail}
                onChange={(v) => set(["contactInformation", "publicEmail"], v)}
              />
            </F>
          </div>
        </section>

        <section className="grid gap-3">
          <div className="flex items-center gap-2">
            <h3 className="text-sm font-semibold">
              {t("abdm_hpr_block_registration")}
            </h3>
            <Button
              type="button"
              variant="ghost"
              size="sm"
              className="ml-auto"
              onClick={() =>
                set(
                  ["registrationAcademic", "registrationData"],
                  [
                    ...registrations,
                    {
                      ...EMPTY_REGISTRATION,
                      qualifications: [{ ...EMPTY_QUALIFICATION }],
                    },
                  ],
                )
              }
            >
              <Plus className="size-4" /> {t("abdm_hpr_add_registration")}
            </Button>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            <F labelKey="abdm_hpid_category" htmlFor="ra-cat">
              <MasterSelect
                id="ra-cat"
                kind="hpr-categories"
                value={String(academic.category ?? "")}
                onChange={(v) => {
                  set(["registrationAcademic", "category"], v);
                  setSomCode("");
                  setSomName("");
                }}
              />
            </F>
            <F
              labelKey="abdm_hpr_system_of_medicine"
              htmlFor="ra-som"
              hint={t("abdm_hpr_som_hint")}
            >
              <MasterSelect
                id="ra-som"
                kind="hpr-subcategories"
                params={{ category: String(academic.category ?? "") }}
                enabled={Boolean(academic.category)}
                value={somCode}
                onChange={(v, row) => {
                  setSomCode(v);
                  setSomName(row?.name ?? "");
                }}
              />
            </F>
          </div>
          {registrations.map((reg, ri) => {
            const base = [
              "registrationAcademic",
              "registrationData",
              String(ri),
            ];
            const quals = (reg.qualifications as Json[]) ?? [];
            return (
              <div key={ri} className="grid gap-3 rounded-md border p-3">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium">
                    {t("abdm_hpr_registration")} {ri + 1}
                  </span>
                  {registrations.length > 1 && (
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon-sm"
                      className="ml-auto"
                      aria-labelKey="abdm_hpr_remove"
                      onClick={() =>
                        set(
                          ["registrationAcademic", "registrationData"],
                          registrations.filter((_, i) => i !== ri),
                        )
                      }
                    >
                      <Trash2 className="size-4" />
                    </Button>
                  )}
                </div>
                <div className="grid gap-3 sm:grid-cols-3">
                  <F labelKey="abdm_hpr_council" htmlFor={`r${ri}-council`}>
                    <MasterSelect
                      id={`r${ri}-council`}
                      kind={councilKind}
                      value={String(reg.registeredWithCouncil ?? "")}
                      onChange={(v) =>
                        set([...base, "registeredWithCouncil"], v)
                      }
                    />
                  </F>
                  <F
                    labelKey="abdm_hpr_registration_number"
                    htmlFor={`r${ri}-num`}
                  >
                    <Txt
                      id={`r${ri}-num`}
                      value={reg.registrationNumber}
                      onChange={(v) => set([...base, "registrationNumber"], v)}
                    />
                  </F>
                  <F
                    labelKey="abdm_hpr_registration_date"
                    htmlFor={`r${ri}-date`}
                  >
                    <Txt
                      id={`r${ri}-date`}
                      type="date"
                      value={reg.registrationDate}
                      onChange={(v) => set([...base, "registrationDate"], v)}
                    />
                  </F>
                  <F labelKey="abdm_hpr_permanent" htmlFor={`r${ri}-perm`}>
                    <Sel
                      id={`r${ri}-perm`}
                      value={reg.isPermanentOrRenewable}
                      onChange={(v) =>
                        set([...base, "isPermanentOrRenewable"], v)
                      }
                      options={[
                        {
                          code: "Permanent",
                          name: t("abdm_hpr_permanent_yes"),
                        },
                        { code: "Renewable", name: t("abdm_hpr_renewable") },
                      ]}
                    />
                  </F>
                  {reg.isPermanentOrRenewable === "Renewable" && (
                    <F labelKey="abdm_hpr_renewable_due" htmlFor={`r${ri}-due`}>
                      <Txt
                        id={`r${ri}-due`}
                        type="date"
                        value={reg.renewableDueDate}
                        onChange={(v) => set([...base, "renewableDueDate"], v)}
                      />
                    </F>
                  )}
                  <F
                    labelKey="abdm_hpr_registration_category_id"
                    htmlFor={`r${ri}-catid`}
                    hint={t("abdm_hpr_code_hint", { example: "2" })}
                  >
                    <Txt
                      id={`r${ri}-catid`}
                      value={reg.categoryId}
                      onChange={(v) => set([...base, "categoryId"], v)}
                    />
                  </F>
                  <FileField
                    id={`r${ri}-cert`}
                    labelKey="abdm_hpr_registration_certificate"
                    value={reg.registrationCertificate as Attachment}
                    onChange={(a) =>
                      set([...base, "registrationCertificate"], a)
                    }
                    t={t}
                  />
                  <F labelKey="abdm_hpr_name_differs" htmlFor={`r${ri}-diff`}>
                    <Sel
                      id={`r${ri}-diff`}
                      value={reg.isNameDifferentInCertificate}
                      onChange={(v) =>
                        set([...base, "isNameDifferentInCertificate"], v)
                      }
                      options={YES_NO(t)}
                    />
                  </F>
                  {reg.isNameDifferentInCertificate === "true" && (
                    <FileField
                      id={`r${ri}-proof`}
                      labelKey="abdm_hpr_name_change_proof"
                      value={String(reg.proofOfNameChangeCertificate ?? "")}
                      onChange={(a) =>
                        set([...base, "proofOfNameChangeCertificate"], a.data)
                      }
                      t={t}
                    />
                  )}
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm font-medium">
                    {t("abdm_hpr_block_qualification")}
                  </span>
                  <Button
                    type="button"
                    variant="ghost"
                    size="sm"
                    className="ml-auto"
                    onClick={() =>
                      set(
                        [...base, "qualifications"],
                        [...quals, { ...EMPTY_QUALIFICATION }],
                      )
                    }
                  >
                    <Plus className="size-4" />{" "}
                    {t("abdm_hpr_add_qualification")}
                  </Button>
                </div>
                {quals.map((q, qi) => {
                  const qb = [...base, "qualifications", String(qi)];
                  return (
                    <div
                      key={qi}
                      className="grid gap-3 rounded-md border p-3 sm:grid-cols-3"
                    >
                      <F labelKey="abdm_hpr_degree" htmlFor={`q${ri}${qi}-deg`}>
                        <MasterSelect
                          id={`q${ri}${qi}-deg`}
                          kind="courses"
                          params={{ system: somName, hpr_type: hprType }}
                          enabled={Boolean(somName)}
                          value={String(q.nameOfDegreeOrDiplomaObtained ?? "")}
                          onChange={(v) =>
                            set([...qb, "nameOfDegreeOrDiplomaObtained"], v)
                          }
                        />
                      </F>
                      <F
                        labelKey="abdm_hpr_country"
                        htmlFor={`q${ri}${qi}-country`}
                      >
                        <MasterSelect
                          id={`q${ri}${qi}-country`}
                          kind="countries"
                          value={String(q.country ?? "")}
                          onChange={(v) => set([...qb, "country"], v)}
                        />
                      </F>
                      <F
                        labelKey="abdm_hfr_state"
                        htmlFor={`q${ri}${qi}-state`}
                      >
                        <MasterSelect
                          id={`q${ri}${qi}-state`}
                          kind="hpr-states"
                          value={String(q.state ?? "")}
                          onChange={(v) => {
                            set([...qb, "state"], v);
                            set([...qb, "college"], "");
                            set([...qb, "university"], "");
                          }}
                        />
                      </F>
                      <F
                        labelKey="abdm_hpr_college"
                        htmlFor={`q${ri}${qi}-college`}
                      >
                        <MasterSelect
                          id={`q${ri}${qi}-college`}
                          kind="colleges-by-state"
                          params={{ state: String(q.state ?? "") }}
                          enabled={Boolean(q.state)}
                          value={String(q.college ?? "")}
                          onChange={(v) => {
                            set([...qb, "college"], v);
                            set([...qb, "university"], "");
                          }}
                        />
                      </F>
                      <F
                        labelKey="abdm_hpr_university"
                        htmlFor={`q${ri}${qi}-uni`}
                      >
                        <MasterSelect
                          id={`q${ri}${qi}-uni`}
                          kind="universities"
                          params={{ college: String(q.college ?? "") }}
                          enabled={Boolean(q.college)}
                          value={String(q.university ?? "")}
                          onChange={(v) => set([...qb, "university"], v)}
                        />
                      </F>
                      <F labelKey="abdm_hpr_year" htmlFor={`q${ri}${qi}-year`}>
                        <Txt
                          id={`q${ri}${qi}-year`}
                          value={q.yearOfAwardingDegreeDiploma}
                          onChange={(v) =>
                            set(
                              [...qb, "yearOfAwardingDegreeDiploma"],
                              v.replace(/\D/g, "").slice(0, 4),
                            )
                          }
                        />
                      </F>
                      <F
                        labelKey="abdm_hpr_month"
                        htmlFor={`q${ri}${qi}-month`}
                      >
                        <Sel
                          id={`q${ri}${qi}-month`}
                          value={q.monthOfAwardingDegreeDiploma}
                          onChange={(v) =>
                            set([...qb, "monthOfAwardingDegreeDiploma"], v)
                          }
                          options={MONTHS.map((m) => ({ code: m, name: m }))}
                        />
                      </F>
                      <FileField
                        id={`q${ri}${qi}-cert`}
                        labelKey="abdm_hpr_degree_certificate"
                        value={q.degreeCertificate as Attachment}
                        onChange={(a) => set([...qb, "degreeCertificate"], a)}
                        t={t}
                      />
                      <F
                        labelKey="abdm_hpr_name_differs"
                        htmlFor={`q${ri}${qi}-diff`}
                      >
                        <Sel
                          id={`q${ri}${qi}-diff`}
                          value={q.isNameDifferentInCertificate}
                          onChange={(v) =>
                            set([...qb, "isNameDifferentInCertificate"], v)
                          }
                          options={YES_NO(t)}
                        />
                      </F>
                      {quals.length > 1 && (
                        <div className="sm:col-span-3">
                          <Button
                            type="button"
                            variant="ghost"
                            size="sm"
                            onClick={() =>
                              set(
                                [...base, "qualifications"],
                                quals.filter((_, i) => i !== qi),
                              )
                            }
                          >
                            <Trash2 className="size-4" /> {t("abdm_hpr_remove")}
                          </Button>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            );
          })}
        </section>

        <section className="grid gap-3">
          <h3 className="text-sm font-semibold">{t("abdm_hpr_block_work")}</h3>
          <div className="grid gap-3 sm:grid-cols-3">
            <F labelKey="abdm_hpr_currently_working" htmlFor="w-cur">
              <Sel
                id="w-cur"
                value={work.currentlyWorking}
                onChange={(v) =>
                  set(["currentWorkDetails", "currentlyWorking"], v)
                }
                options={[
                  { code: "1", name: t("abdm_yes") },
                  { code: "0", name: t("abdm_no") },
                ]}
              />
            </F>
            <F labelKey="abdm_hpr_purpose_of_work" htmlFor="w-purpose">
              <Txt
                id="w-purpose"
                value={work.purposeOfWork}
                onChange={(v) =>
                  set(["currentWorkDetails", "purposeOfWork"], v)
                }
              />
            </F>
            <F
              labelKey="abdm_hpr_work_status"
              htmlFor="w-status"
              hint={t("abdm_hpr_code_hint", { example: "1" })}
            >
              <Txt
                id="w-status"
                value={work.chooseWorkStatus}
                onChange={(v) =>
                  set(["currentWorkDetails", "chooseWorkStatus"], v)
                }
              />
            </F>
            {work.currentlyWorking === "0" && (
              <F labelKey="abdm_hpr_reason_not_working" htmlFor="w-reason">
                <Txt
                  id="w-reason"
                  value={work.reasonForNotWorking}
                  onChange={(v) =>
                    set(["currentWorkDetails", "reasonForNotWorking"], v)
                  }
                />
              </F>
            )}
            <FileField
              id="w-cert"
              labelKey="abdm_hpr_proof_of_work"
              value={String(work.certificateAttachment ?? "")}
              onChange={(a) =>
                set(["currentWorkDetails", "certificateAttachment"], a.data)
              }
              t={t}
            />
          </div>
          {work.currentlyWorking === "1" && (
            <div className="grid gap-3 sm:grid-cols-3">
              <F
                labelKey="abdm_hfr_facility_id"
                htmlFor="w-fid"
                hint={t("abdm_hpr_facility_id_hint")}
              >
                <Txt
                  id="w-fid"
                  value={declaration.facilityId}
                  onChange={(v) =>
                    set(
                      [
                        "currentWorkDetails",
                        "facilityDeclarationData",
                        "facilityId",
                      ],
                      v.toUpperCase(),
                    )
                  }
                />
              </F>
              <F labelKey="abdm_hpr_department" htmlFor="w-dept">
                <Txt
                  id="w-dept"
                  value={declaration.facilityDepartment}
                  onChange={(v) =>
                    set(
                      [
                        "currentWorkDetails",
                        "facilityDeclarationData",
                        "facilityDepartment",
                      ],
                      v,
                    )
                  }
                />
              </F>
              <F labelKey="abdm_hpr_designation" htmlFor="w-desig">
                <Txt
                  id="w-desig"
                  value={declaration.facilityDesignation}
                  onChange={(v) =>
                    set(
                      [
                        "currentWorkDetails",
                        "facilityDeclarationData",
                        "facilityDesignation",
                      ],
                      v,
                    )
                  }
                />
              </F>
              <F labelKey="abdm_hpr_ministry" htmlFor="w-min">
                <MasterSelect
                  id="w-min"
                  kind="psu"
                  value={String((declaration.ministry as Json)?.ministry ?? "")}
                  onChange={(v) =>
                    set(
                      [
                        "currentWorkDetails",
                        "facilityDeclarationData",
                        "ministry",
                        "ministry",
                      ],
                      v,
                    )
                  }
                />
              </F>
            </div>
          )}
        </section>

        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}
        {String(get(["personalInformation", "firstName"]) ?? "") === "" && (
          <p className="text-muted-foreground text-xs">
            {t("abdm_hpr_register_incomplete")}
          </p>
        )}
      </CardContent>
      <CardFooter
        className={cn(
          "flex items-center gap-3 border-t",
          embedded && `${embeddedCard.padding} border-t-0`,
        )}
      >
        <span className="text-muted-foreground text-xs">
          {t("abdm_hpr_register_footer")}
        </span>
        <Button
          type="button"
          size="sm"
          className="ml-auto"
          disabled={busy || !complete || !state.session.active}
          onClick={() => register.mutate()}
        >
          {busy && <Loader2 className="size-4 animate-spin" />}{" "}
          {isUpdate ? t("abdm_hpr_update") : t("abdm_hpr_register")}
        </Button>
      </CardFooter>
    </Card>
  );
}
