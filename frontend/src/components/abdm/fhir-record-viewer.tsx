import {
  formatDay,
  formatTime,
  hiTypeLabel,
} from "@/components/abdm/care-context-state";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Skeleton } from "@/components/ui/skeleton";
import { useTranslation } from "@/hooks/use-translation";
import careApi, { type AbdmFetchedRecord } from "@/lib/careApi";
import { query } from "@/lib/request";
import { useQuery } from "@tanstack/react-query";
import { Download, FileText } from "lucide-react";
import { useMemo, useState } from "react";

/**
 * Renders 1 decrypted FHIR R4 document bundle another facility pushed (ADR-014). The bundle
 * follows an NRCES document profile (concepts/fhir): entry[0] is a Composition whose sections
 * reference the clinical resources. Each resource type gets a short summary; anything unknown
 * falls back to its JSON. The desk can always read the raw bundle and download it.
 */

type Resource = Record<string, unknown> & {
  resourceType?: string;
  id?: string;
};
type Bundle = { entry?: { fullUrl?: string; resource?: Resource }[] };

type T = (key: string) => string;

function str(value: unknown): string {
  return typeof value === "string" || typeof value === "number"
    ? String(value)
    : "";
}

function obj(value: unknown): Record<string, unknown> {
  return value && typeof value === "object" && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : {};
}

function arr(value: unknown): unknown[] {
  return Array.isArray(value) ? value : [];
}

/** `CodeableConcept` → its text, else the first coding's display or code. */
function codeText(value: unknown): string {
  const cc = obj(value);
  if (str(cc.text)) return str(cc.text);
  const coding = obj(arr(cc.coding)[0]);
  return str(coding.display) || str(coding.code);
}

function quantity(value: unknown): string {
  const q = obj(value);
  const number = str(q.value);
  return number ? `${number} ${str(q.unit) || str(q.code)}`.trim() : "";
}

function when(value: unknown): string {
  const text = str(value);
  if (!text) return "";
  const d = new Date(text);
  return Number.isNaN(d.getTime())
    ? text
    : `${formatDay(text)} ${formatTime(d)}`;
}

function period(value: unknown): string {
  const p = obj(value);
  const start = when(p.start);
  const end = when(p.end);
  return start && end ? `${start} – ${end}` : start || end;
}

function resolve(bundle: Bundle, reference: unknown): Resource | undefined {
  const ref = str(obj(reference).reference);
  if (!ref) return undefined;
  for (const entry of bundle.entry ?? []) {
    if (entry.fullUrl === ref) return entry.resource;
    const r = entry.resource;
    if (r && `${r.resourceType}/${r.id}` === ref) return r;
  }
  return undefined;
}

function Attachment({ value, t }: { value: unknown; t: T }) {
  const a = obj(value);
  const type = str(a.contentType) || "application/octet-stream";
  const title = str(a.title) || type;
  const href = str(a.data) ? `data:${type};base64,${str(a.data)}` : str(a.url);
  if (!href) return null;
  const name = title.includes(".")
    ? title
    : `${title}.${type.split("/")[1] ?? "bin"}`;
  return (
    <a
      href={href}
      download={str(a.data) ? name : undefined}
      target={str(a.data) ? undefined : "_blank"}
      rel="noreferrer"
      className="text-primary inline-flex items-center gap-1 text-xs underline-offset-2 hover:underline"
    >
      <Download className="size-3" /> {title} {t("abdm_record_open_attachment")}
    </a>
  );
}

function Row({ label, value }: { label: string; value: string }) {
  if (!value) return null;
  return (
    <div className="grid gap-0.5 sm:grid-cols-[8rem_1fr]">
      <span className="text-muted-foreground text-xs">{label}</span>
      <span className="text-sm">{value}</span>
    </div>
  );
}

function ResourceSummary({
  resource,
  bundle,
  t,
}: {
  resource: Resource;
  bundle: Bundle;
  t: T;
}) {
  const type = str(resource.resourceType);
  const rows: { label: string; value: string }[] = [];
  const attachments: unknown[] = [];
  const push = (label: string, value: string) =>
    value && rows.push({ label, value });
  switch (type) {
    case "Condition":
      push(t("abdm_record_field_problem"), codeText(resource.code));
      push(t("abdm_record_field_status"), codeText(resource.clinicalStatus));
      push(
        t("abdm_record_field_onset"),
        when(resource.onsetDateTime) || str(resource.onsetString),
      );
      break;
    case "AllergyIntolerance":
      push(t("abdm_record_field_allergy"), codeText(resource.code));
      push(t("abdm_record_field_criticality"), str(resource.criticality));
      push(
        t("abdm_record_field_reaction"),
        arr(resource.reaction)
          .flatMap((r) => arr(obj(r).manifestation).map(codeText))
          .filter(Boolean)
          .join(", "),
      );
      break;
    case "MedicationRequest":
    case "MedicationStatement": {
      const medication =
        codeText(resource.medicationCodeableConcept) ||
        codeText(obj(resolve(bundle, resource.medicationReference)).code);
      push(t("abdm_record_field_medication"), medication);
      push(
        t("abdm_record_field_dosage"),
        arr(resource.dosageInstruction ?? resource.dosage)
          .map((d) => str(obj(d).text))
          .filter(Boolean)
          .join("; "),
      );
      push(
        t("abdm_record_field_reason"),
        arr(resource.reasonCode).map(codeText).filter(Boolean).join(", "),
      );
      push(
        t("abdm_record_field_date"),
        when(resource.authoredOn ?? resource.dateAsserted),
      );
      break;
    }
    case "Observation": {
      push(t("abdm_record_field_observation"), codeText(resource.code));
      const value =
        quantity(resource.valueQuantity) ||
        str(resource.valueString) ||
        codeText(resource.valueCodeableConcept) ||
        (resource.valueBoolean === undefined
          ? ""
          : String(resource.valueBoolean));
      push(t("abdm_record_field_value"), value);
      push(
        t("abdm_record_field_components"),
        arr(resource.component)
          .map(
            (c) =>
              `${codeText(obj(c).code)}: ${quantity(obj(c).valueQuantity) || str(obj(c).valueString)}`,
          )
          .join("; "),
      );
      push(
        t("abdm_record_field_date"),
        when(resource.effectiveDateTime) || period(resource.effectivePeriod),
      );
      break;
    }
    case "Procedure":
      push(t("abdm_record_field_procedure"), codeText(resource.code));
      push(
        t("abdm_record_field_date"),
        when(resource.performedDateTime) || period(resource.performedPeriod),
      );
      break;
    case "DiagnosticReport":
      push(t("abdm_record_field_report"), codeText(resource.code));
      push(t("abdm_record_field_conclusion"), str(resource.conclusion));
      push(
        t("abdm_record_field_date"),
        when(resource.effectiveDateTime) || when(resource.issued),
      );
      attachments.push(...arr(resource.presentedForm));
      break;
    case "DocumentReference":
      push(
        t("abdm_record_field_document"),
        codeText(resource.type) || str(resource.description),
      );
      push(t("abdm_record_field_date"), when(resource.date));
      attachments.push(...arr(resource.content).map((c) => obj(c).attachment));
      break;
    case "Binary":
      attachments.push({
        contentType: resource.contentType,
        data: resource.data,
        title: "Binary",
      });
      break;
    case "Immunization":
      push(t("abdm_record_field_vaccine"), codeText(resource.vaccineCode));
      push(t("abdm_record_field_date"), when(resource.occurrenceDateTime));
      push(t("abdm_record_field_lot"), str(resource.lotNumber));
      break;
    case "ServiceRequest":
      push(t("abdm_record_field_order"), codeText(resource.code));
      push(t("abdm_record_field_date"), when(resource.authoredOn));
      break;
    case "Appointment":
      push(
        t("abdm_record_field_appointment"),
        codeText(arr(resource.serviceType)[0]) || str(resource.description),
      );
      push(t("abdm_record_field_date"), when(resource.start));
      break;
    case "Encounter":
      push(
        t("abdm_record_field_visit"),
        codeText(obj(resource.class)) || codeText(arr(resource.type)[0]),
      );
      push(t("abdm_record_field_date"), period(resource.period));
      break;
    default:
      break;
  }
  const generic = rows.length === 0 && attachments.length === 0;
  return (
    <div className="grid gap-1 rounded-md border p-3">
      <span className="text-muted-foreground text-xs font-medium">{type}</span>
      {rows.map((row) => (
        <Row key={row.label} label={row.label} value={row.value} />
      ))}
      {attachments.map((a, i) => (
        <Attachment key={i} value={a} t={t} />
      ))}
      {generic && (
        <pre className="bg-muted max-h-48 overflow-auto rounded p-2 text-xs">
          {JSON.stringify(resource, null, 2)}
        </pre>
      )}
    </div>
  );
}

const HEADER_TYPES = new Set([
  "Composition",
  "Patient",
  "Practitioner",
  "Organization",
]);

function Sections({ bundle, t }: { bundle: Bundle; t: T }) {
  const composition = (bundle.entry ?? [])
    .map((e) => e.resource)
    .find((r) => r?.resourceType === "Composition");
  const sections = arr(composition?.section);
  if (sections.length > 0) {
    return (
      <>
        {sections.map((section, i) => {
          const s = obj(section);
          const entries = arr(s.entry)
            .map((ref) => resolve(bundle, ref))
            .filter((r): r is Resource => Boolean(r));
          return (
            <div key={i} className="grid gap-2">
              <h4 className="text-sm font-semibold">
                {str(s.title) || codeText(s.code) || t("abdm_record_section")}
              </h4>
              {entries.length === 0 && (
                <p className="text-muted-foreground text-xs">
                  {t("abdm_record_section_empty")}
                </p>
              )}
              {entries.map((r, j) => (
                <ResourceSummary
                  key={`${str(r.id)}-${j}`}
                  resource={r}
                  bundle={bundle}
                  t={t}
                />
              ))}
            </div>
          );
        })}
      </>
    );
  }
  const rest = (bundle.entry ?? [])
    .map((e) => e.resource)
    .filter(
      (r): r is Resource =>
        Boolean(r) && !HEADER_TYPES.has(str(r?.resourceType)),
    );
  return (
    <div className="grid gap-2">
      {rest.map((r, i) => (
        <ResourceSummary
          key={`${str(r.id)}-${i}`}
          resource={r}
          bundle={bundle}
          t={t}
        />
      ))}
    </div>
  );
}

function compositionHeader(bundle: Bundle) {
  const composition = (bundle.entry ?? [])
    .map((e) => e.resource)
    .find((r) => r?.resourceType === "Composition");
  const author = arr(composition?.author)
    .map((ref) => resolve(bundle, ref))
    .map((r) => str(r?.name) || str(obj(arr(r?.name)[0]).text) || "")
    .filter(Boolean)
    .join(", ");
  const custodian = str(resolve(bundle, composition?.custodian)?.name);
  return { author, custodian, status: str(composition?.status) };
}

export default function FhirRecordViewer({
  patientId,
  record,
  onOpenChange,
}: {
  patientId: string;
  record: AbdmFetchedRecord | null;
  onOpenChange: (open: boolean) => void;
}) {
  const { t } = useTranslation();
  const [raw, setRaw] = useState(false);
  const detail = useQuery({
    queryKey: ["abdm", "patient", patientId, "record", record?.id],
    queryFn: query(careApi.fetchedRecord, {
      pathParams: { patientId, recordId: record?.id ?? "" },
      silent: true,
    }),
    enabled: Boolean(record?.id && record.available),
    retry: false,
    staleTime: 60_000,
  });
  const bundle = (detail.data?.bundle ?? null) as Bundle | null;
  const header = useMemo(
    () => (bundle ? compositionHeader(bundle) : null),
    [bundle],
  );
  const download = () => {
    if (!bundle) return;
    const url = URL.createObjectURL(
      new Blob([JSON.stringify(bundle, null, 2)], {
        type: "application/fhir+json",
      }),
    );
    const a = document.createElement("a");
    a.href = url;
    a.download = `${record?.hiType || "record"}-${record?.careContextReference || record?.id}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <Dialog open={Boolean(record)} onOpenChange={onOpenChange}>
      <DialogContent className="max-h-[90vh] overflow-y-auto sm:max-w-3xl">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <FileText className="text-muted-foreground size-4" />
            {record?.title || (record ? hiTypeLabel(t, record.hiType) : "")}
            {record && (
              <Badge variant="neutral" size="sm" className="ml-auto">
                {hiTypeLabel(t, record.hiType) || t("abdm_record_unknown_type")}
              </Badge>
            )}
          </DialogTitle>
          <DialogDescription className="grid gap-0.5 text-xs">
            {record?.hipName && (
              <span>{t("abdm_record_from", { name: record.hipName })}</span>
            )}
            {record?.authoredAt && (
              <span>
                {t("abdm_record_authored")} {when(record.authoredAt)}
              </span>
            )}
            {record && (
              <span>
                {t("abdm_record_received")} {when(record.receivedAt)}
              </span>
            )}
            {record?.eraseAt && (
              <span>
                {t("abdm_record_erase_at")} {when(record.eraseAt)}
              </span>
            )}
            {header?.author && (
              <span>
                {t("abdm_record_author")} {header.author}
              </span>
            )}
            {header?.custodian && (
              <span>
                {t("abdm_record_custodian")} {header.custodian}
              </span>
            )}
          </DialogDescription>
        </DialogHeader>

        {record && !record.checksumOk && (
          <Alert variant="warning">
            <AlertDescription>
              {t("abdm_record_checksum_warning")}
            </AlertDescription>
          </Alert>
        )}
        {record && !record.available && (
          <Alert>
            <AlertDescription>{t("abdm_record_erased")}</AlertDescription>
          </Alert>
        )}
        {detail.isLoading && <Skeleton className="h-40 w-full rounded-md" />}
        {detail.isError && (
          <Alert variant="destructive">
            <AlertDescription>{t("abdm_record_load_failed")}</AlertDescription>
          </Alert>
        )}
        {bundle && !raw && (
          <div className="grid gap-4">
            <Sections bundle={bundle} t={t} />
          </div>
        )}
        {bundle && raw && (
          <pre className="bg-muted max-h-[60vh] overflow-auto rounded p-3 text-xs">
            {JSON.stringify(bundle, null, 2)}
          </pre>
        )}

        <DialogFooter className="flex-wrap">
          {bundle && (
            <>
              <Button
                type="button"
                variant="ghost"
                size="sm"
                onClick={() => setRaw((v) => !v)}
              >
                {raw
                  ? t("abdm_record_show_summary")
                  : t("abdm_record_show_json")}
              </Button>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={download}
              >
                <Download className="size-4" /> {t("abdm_record_download")}
              </Button>
            </>
          )}
          <Button type="button" size="sm" onClick={() => onOpenChange(false)}>
            {t("abdm_close")}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
