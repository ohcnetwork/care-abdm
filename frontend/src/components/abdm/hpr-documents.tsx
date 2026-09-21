import { errorMessage } from "@/components/abdm/nhpr-shared";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
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
  type AbdmDocumentSlot,
  type AbdmHprState,
} from "@/lib/careApi";
import { mutate, query } from "@/lib/request";
import { useMutation, useQuery } from "@tanstack/react-query";
import { useState } from "react";

/**
 * The HPR certificate slots (ADR-015), in the documents sheet of the user profile section
 * (ADR-017). The registry names the slots; the person uploads 1 file into a slot to replace it.
 */

function fileToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result).split(",")[1] ?? "");
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(file);
  });
}

export default function HprDocuments({ state }: { state: AbdmHprState }) {
  const { t } = useTranslation();
  const [error, setError] = useState<string>();
  const [message, setMessage] = useState<string>();
  const docs = useQuery<{ slots: AbdmDocumentSlot[] }>({
    queryKey: ["abdm", "me", "hpr", "documents"],
    queryFn: query(careApi.hprDocuments, { silent: true }),
    enabled: Boolean(state.profile && state.session.active),
    retry: false,
  });
  const upload = useMutation<
    Record<string, { status: string; msg: string } | null>,
    unknown,
    { slot: AbdmDocumentSlot; file: File }
  >({
    mutationFn: async ({ slot, file }) =>
      mutate(careApi.hprUploadDocuments, { silent: true })({
        documents: [
          {
            document_id: slot.id,
            document_type: slot.type,
            fileType: (file.name.split(".").pop() || "pdf").toLowerCase(),
            data: await fileToBase64(file),
          },
        ],
      }),
    onMutate: () => {
      setError(undefined);
      setMessage(undefined);
    },
    onSuccess: (data) => {
      const lines = Object.entries(data)
        .filter(([, v]) => v)
        .map(([k, v]) => `${k}: ${v?.msg ?? v?.status}`);
      setMessage(lines.join(" · ") || t("abdm_hpr_upload_done"));
      docs.refetch();
    },
    onError: (e) => setError(errorMessage(e, t("abdm_hpr_upload_failed"))),
  });

  return (
    <div className="grid gap-3">
      {!state.session.active && (
        <Alert variant="warning">
          <AlertDescription>
            {t("abdm_hpr_documents_need_session")}
          </AlertDescription>
        </Alert>
      )}
      {docs.isLoading && <Skeleton className="h-20 w-full rounded-md" />}
      {docs.isError && (
        <Alert variant="destructive">
          <AlertDescription>{t("abdm_hpr_documents_failed")}</AlertDescription>
        </Alert>
      )}
      {docs.data && docs.data.slots.length === 0 && (
        <p className="text-muted-foreground text-sm">
          {t("abdm_hpr_documents_none")}
        </p>
      )}
      {docs.data && docs.data.slots.length > 0 && (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>{t("abdm_hpr_document")}</TableHead>
              <TableHead>{t("abdm_hpr_document_group")}</TableHead>
              <TableHead>{t("abdm_hfr_status")}</TableHead>
              <TableHead />
            </TableRow>
          </TableHeader>
          <TableBody>
            {docs.data.slots.map((slot) => (
              <TableRow key={`${slot.group}-${slot.type}-${slot.id}`}>
                <TableCell>{slot.type}</TableCell>
                <TableCell className="text-muted-foreground text-xs">
                  {[slot.group, slot.system].filter(Boolean).join(" · ")}
                </TableCell>
                <TableCell>
                  <Badge
                    variant={slot.hasData ? "success" : "neutral"}
                    size="sm"
                  >
                    {slot.hasData
                      ? t("abdm_hpr_document_present")
                      : t("abdm_hpr_document_missing")}
                  </Badge>
                </TableCell>
                <TableCell className="text-right">
                  <Input
                    type="file"
                    className="h-9 max-w-56"
                    accept="application/pdf,image/png,image/jpeg"
                    disabled={upload.isPending}
                    onChange={(e) => {
                      const file = e.target.files?.[0];
                      if (file) upload.mutate({ slot, file });
                    }}
                  />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}
      {message && <p className="text-xs">{message}</p>}
      {error && (
        <Alert variant="destructive">
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
    </div>
  );
}
