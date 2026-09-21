import {
  formatDay,
  formatTime,
  hiTypeLabel,
} from "@/components/abdm/care-context-state";
import ConsentRequestDialog from "@/components/abdm/consent-request-dialog";
import FhirRecordViewer from "@/components/abdm/fhir-record-viewer";
import {
  availableRecords,
  fetchStatusKey,
  fetchTone,
  hiuQueryKey,
  latestFetch,
  requestInFlight,
  requestStatusKey,
  requestTone,
  useHiuState,
} from "@/components/abdm/hiu-state";
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
  type AbdmConsentRequest,
  type AbdmConsentRequestCreate,
  type AbdmFetchedRecord,
  type AbdmHiuState,
} from "@/lib/careApi";
import { mutate } from "@/lib/request";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { Download, Eye, Loader2, RefreshCw } from "lucide-react";
import { useState } from "react";

/**
 * 3rd card of the ABDM Records tab: "Records from other facilities" (ADR-014, M3 as HIU).
 *
 * The desk raises a consent request for this patient; the patient grants it in an ABHA app; the
 * plug fetches the artefacts, requests the data, decrypts the push and lists the records here.
 * The card is append-only: requests are listed newest first and rows never reshuffle; a request
 * grows a records table below it when records arrive. Every failure is shown (ADR-012 D7).
 */

function errorMessage(error: unknown, fallback: string) {
  if (error && typeof error === "object" && "cause" in error) {
    const cause = (error as { cause?: Record<string, unknown> }).cause;
    const value = cause?.errors ?? cause?.message;
    if (typeof value === "string") return value;
  }
  return fallback;
}

function RecordRows({
  request,
  onOpen,
  t,
}: {
  request: AbdmConsentRequest;
  onOpen: (record: AbdmFetchedRecord) => void;
  t: (key: string, options?: Record<string, unknown>) => string;
}) {
  const records = request.artefacts.flatMap((a) => a.records);
  if (records.length === 0) return null;
  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>{t("abdm_fetch_record")}</TableHead>
          <TableHead>{t("abdm_cc_hi_types")}</TableHead>
          <TableHead>{t("abdm_fetch_record_from")}</TableHead>
          <TableHead>{t("abdm_fetch_record_received")}</TableHead>
          <TableHead />
        </TableRow>
      </TableHeader>
      <TableBody>
        {records.map((record) => (
          <TableRow
            key={record.id}
            className={record.available ? undefined : "opacity-60"}
          >
            <TableCell>
              <div className="grid gap-0.5">
                <span>
                  {record.title ||
                    hiTypeLabel(t, record.hiType) ||
                    t("abdm_record_unknown_type")}
                </span>
                <span className="text-muted-foreground font-mono text-xs">
                  {record.careContextReference}
                </span>
              </div>
            </TableCell>
            <TableCell className="whitespace-nowrap">
              {hiTypeLabel(t, record.hiType) || "\u2014"}
            </TableCell>
            <TableCell>{record.hipName || record.hipId || "\u2014"}</TableCell>
            <TableCell className="text-xs whitespace-nowrap">
              {formatDay(record.receivedAt)}{" "}
              {formatTime(new Date(record.receivedAt))}
              {record.erasedAt && (
                <span className="text-muted-foreground block">
                  {t("abdm_fetch_record_erased")}
                </span>
              )}
            </TableCell>
            <TableCell className="text-right">
              <Button
                type="button"
                variant="outline"
                size="sm"
                disabled={!record.available}
                onClick={() => onOpen(record)}
              >
                <Eye className="size-4" /> {t("abdm_fetch_record_open")}
              </Button>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}

function RequestRow({
  request,
  busy,
  onRefresh,
  onFetch,
  onOpen,
  t,
}: {
  request: AbdmConsentRequest;
  busy: boolean;
  onRefresh: () => void;
  onFetch: () => void;
  onOpen: (record: AbdmFetchedRecord) => void;
  t: (key: string, options?: Record<string, unknown>) => string;
}) {
  const fetch = latestFetch(request);
  const inFlight = requestInFlight(request);
  const records = availableRecords(request);
  const liveArtefact = request.artefacts.some((a) => a.live);
  const artefactFailure = request.artefacts.map((a) => a.failure).find(Boolean);
  const failure = request.failure ?? fetch?.failure ?? artefactFailure ?? null;
  return (
    <div className="grid gap-3 rounded-md border p-3">
      <div className="flex flex-wrap items-start gap-3">
        <div className="grid grow gap-0.5 text-sm">
          <span className="flex flex-wrap items-center gap-2">
            <Badge variant={requestTone(request.status)} size="sm">
              {t(requestStatusKey(request.status))}
            </Badge>
            {fetch && request.status === "GRANTED" && (
              <Badge variant={fetchTone(fetch.status)} size="sm">
                {t(fetchStatusKey(fetch.status))}
              </Badge>
            )}
            {inFlight && (
              <Loader2 className="text-muted-foreground size-3.5 animate-spin" />
            )}
          </span>
          <span>
            {request.hiTypes.map((h) => hiTypeLabel(t, h)).join(", ")}
          </span>
          <span className="text-muted-foreground text-xs">
            {t("abdm_fetch_range")} {formatDay(request.dateFrom)} –{" "}
            {formatDay(request.dateTo)} · {request.purposeText} ·{" "}
            {request.hipName || t("abdm_fetch_all_providers")}
          </span>
          <span className="text-muted-foreground text-xs">
            {t("abdm_fetch_requested_by", {
              name: request.requestedBy || "\u2014",
              when: `${formatDay(request.requestedAt)} ${formatTime(new Date(request.requestedAt))}`,
            })}
            {request.decidedAt &&
              ` · ${t("abdm_fetch_decided_at")} ${formatDay(request.decidedAt)} ${formatTime(new Date(request.decidedAt))}`}
            {request.reason && ` · ${request.reason}`}
          </span>
        </div>
        <div className="flex shrink-0 gap-2">
          {(request.open ||
            (fetch &&
              (fetch.status === "requested" ||
                fetch.status === "acknowledged"))) && (
            <Button
              type="button"
              variant="ghost"
              size="sm"
              disabled={busy}
              onClick={onRefresh}
            >
              <RefreshCw className="size-4" /> {t("abdm_fetch_check")}
            </Button>
          )}
          {request.status === "GRANTED" && liveArtefact && !inFlight && (
            <Button
              type="button"
              variant="outline"
              size="sm"
              disabled={busy}
              onClick={onFetch}
            >
              <Download className="size-4" /> {t("abdm_fetch_again")}
            </Button>
          )}
        </div>
      </div>
      {failure && (
        <Alert variant={failure.retry === "after" ? "warning" : "destructive"}>
          <AlertDescription>
            {failure.what} {failure.nextStep}
          </AlertDescription>
        </Alert>
      )}
      {request.status === "GRANTED" && records === 0 && !failure && (
        <p className="text-muted-foreground text-xs">
          {inFlight
            ? t("abdm_fetch_waiting_for_records")
            : t("abdm_fetch_no_records_yet")}
        </p>
      )}
      <RecordRows request={request} onOpen={onOpen} t={t} />
    </div>
  );
}

export default function FetchRecordsCard({
  patientId,
  facilityId,
}: {
  patientId: string;
  facilityId: string;
}) {
  const { t } = useTranslation();
  const qc = useQueryClient();
  const [dialogOpen, setDialogOpen] = useState(false);
  const [record, setRecord] = useState<AbdmFetchedRecord | null>(null);
  const [actionError, setActionError] = useState<string>();
  const { data, isLoading, isError } = useHiuState(patientId, facilityId);

  const apply = (next: AbdmHiuState) => {
    qc.setQueryData(hiuQueryKey(patientId, facilityId), next);
  };
  const create = useMutation<AbdmHiuState, unknown, AbdmConsentRequestCreate>({
    mutationFn: mutate(careApi.createConsentRequest, {
      pathParams: { patientId },
      silent: true,
    }),
    onMutate: () => setActionError(undefined),
    onSuccess: (next) => {
      apply(next);
      setDialogOpen(false);
    },
    onError: (error) => {
      // A refused init answers 502 with the full state: show it, the row carries the failure.
      const cause = (error as { cause?: AbdmHiuState }).cause;
      if (cause && Array.isArray(cause.requests)) {
        apply(cause);
        setDialogOpen(false);
        return;
      }
      setActionError(errorMessage(error, t("abdm_fetch_request_failed")));
    },
  });
  const action = useMutation<
    AbdmHiuState,
    unknown,
    { requestId: string; action: "refresh" | "fetch" }
  >({
    mutationFn: ({ requestId, action }) =>
      mutate(careApi.consentRequestAction, {
        pathParams: { patientId, requestId, action },
        silent: true,
      })({}),
    onMutate: () => setActionError(undefined),
    onSuccess: apply,
    onError: (error) =>
      setActionError(errorMessage(error, t("abdm_fetch_action_failed"))),
  });

  const busy = create.isPending || action.isPending;
  const canRequest =
    Boolean(data?.facilityConfigured) &&
    Boolean(data?.callbackUrlSet) &&
    Boolean(data?.patientAbhaAddress);

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Download className="text-muted-foreground size-4" />
          {t("abdm_fetch_title")}
        </CardTitle>
        <CardDescription>{t("abdm_fetch_intro")}</CardDescription>
      </CardHeader>
      <CardContent className="grid gap-3">
        {isLoading && <Skeleton className="h-24 w-full rounded-md" />}
        {isError && (
          <Alert variant="destructive">
            <AlertDescription>{t("abdm_fetch_load_failed")}</AlertDescription>
          </Alert>
        )}
        {data && !data.facilityConfigured && (
          <Alert variant="warning">
            <AlertDescription>
              {t("abdm_cc_status_facility_not_setup")}
            </AlertDescription>
          </Alert>
        )}
        {data && data.facilityConfigured && !data.callbackUrlSet && (
          <Alert variant="warning">
            <AlertDescription>
              {t("abdm_fetch_no_callback_url")}
            </AlertDescription>
          </Alert>
        )}
        {data && !data.patientAbhaAddress && (
          <Alert variant="warning">
            <AlertDescription>{t("abdm_tab_no_abha")}</AlertDescription>
          </Alert>
        )}
        {actionError && (
          <Alert variant="destructive">
            <AlertDescription>{actionError}</AlertDescription>
          </Alert>
        )}
        {data && data.requests.length === 0 && canRequest && (
          <p className="text-muted-foreground text-sm">
            {t("abdm_fetch_none")}
          </p>
        )}
        {data?.requests.map((request) => (
          <RequestRow
            key={request.id}
            request={request}
            busy={busy}
            t={t}
            onRefresh={() =>
              action.mutate({ requestId: request.id, action: "refresh" })
            }
            onFetch={() =>
              action.mutate({ requestId: request.id, action: "fetch" })
            }
            onOpen={setRecord}
          />
        ))}
      </CardContent>
      <CardFooter className="flex items-center gap-3 border-t">
        <span className="text-muted-foreground text-xs">
          {t("abdm_fetch_footer_hint")}
        </span>
        <Button
          type="button"
          size="sm"
          className="ml-auto"
          disabled={!canRequest || busy}
          onClick={() => setDialogOpen(true)}
        >
          {busy ? (
            <Loader2 className="size-4 animate-spin" />
          ) : (
            <Download className="size-4" />
          )}
          {t("abdm_fetch_request")}
        </Button>
      </CardFooter>
      {data && (
        <ConsentRequestDialog
          open={dialogOpen}
          onOpenChange={setDialogOpen}
          state={data}
          facilityId={facilityId}
          onSubmit={(body) => create.mutate(body)}
          pending={create.isPending}
          error={actionError}
        />
      )}
      <FhirRecordViewer
        patientId={patientId}
        record={record}
        onOpenChange={(open) => !open && setRecord(null)}
      />
    </Card>
  );
}
