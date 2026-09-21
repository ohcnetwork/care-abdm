import HpidCreateWizard from "@/components/abdm/hpid-create-wizard";
import HprLoginDialog from "@/components/abdm/hpr-login-dialog";
import { errorMessage, hprQueryKey } from "@/components/abdm/nhpr-shared";
import HprRegisterForm from "@/components/abdm/hpr-register-form";
import PluginComponent from "@/components/common/plugin-component";
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
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  IdCard,
  Loader2,
  LogIn,
  LogOut,
  RefreshCw,
  Unlink,
  Upload,
} from "lucide-react";
import { useState } from "react";

/**
 * "My HPR ID" (ADR-015), at /abdm/hpr from the user menu (host slot `userNavItems`). One page for the
 * caller's own professional identity: link an existing HPID by an HPR login, or create one through
 * the Aadhaar link; then register the professional profile, keep the documents, and read what the
 * registry holds. The HPR token stays on the server; the page only sees "session active".
 */

function fileToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(String(reader.result).split(",")[1] ?? "");
    reader.onerror = () => reject(reader.error);
    reader.readAsDataURL(file);
  });
}

function Documents({ state }: { state: AbdmHprState }) {
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
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Upload className="text-muted-foreground size-4" />{" "}
          {t("abdm_hpr_documents_title")}
        </CardTitle>
        <CardDescription>{t("abdm_hpr_documents_intro")}</CardDescription>
      </CardHeader>
      <CardContent className="grid gap-3">
        {!state.session.active && (
          <p className="text-muted-foreground text-sm">
            {t("abdm_hpr_documents_need_session")}
          </p>
        )}
        {docs.isLoading && <Skeleton className="h-20 w-full rounded-md" />}
        {docs.isError && (
          <Alert variant="destructive">
            <AlertDescription>
              {t("abdm_hpr_documents_failed")}
            </AlertDescription>
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
      </CardContent>
    </Card>
  );
}

export default function HprPage({ username }: { username?: string }) {
  const { t } = useTranslation();
  const qc = useQueryClient();
  const [loginOpen, setLoginOpen] = useState(false);
  const [creating, setCreating] = useState(false);
  const [editing, setEditing] = useState(false);
  const [error, setError] = useState<string>();
  const state = useQuery<AbdmHprState>({
    queryKey: hprQueryKey,
    queryFn: query(careApi.hprState, { silent: true }),
    retry: false,
  });
  const session = useMutation<AbdmHprState, unknown, "logout" | "unlink">({
    mutationFn: (action) =>
      mutate(careApi.hprSessionAction, {
        pathParams: { action },
        silent: true,
      })({}),
    onMutate: () => setError(undefined),
    onSuccess: (next) => qc.setQueryData(hprQueryKey, next),
    onError: (e) => setError(errorMessage(e, t("abdm_hpr_action_failed"))),
  });
  const info = useMutation<Record<string, unknown>, unknown, void>({
    mutationFn: () =>
      query(careApi.hprProfessionalInfo, { silent: true })({
        signal: new AbortController().signal,
      }),
    onMutate: () => setError(undefined),
    onSuccess: () => qc.invalidateQueries({ queryKey: hprQueryKey }),
    onError: (e) => setError(errorMessage(e, t("abdm_hpr_action_failed"))),
  });
  const data = state.data;
  const profile = data?.profile ?? null;
  const busy = session.isPending || info.isPending;
  const showCreate = Boolean(
    data && !profile && (creating || data.transaction),
  );
  const professional =
    (profile?.professional?.info as Record<string, unknown> | undefined) ??
    null;

  return (
    <PluginComponent>
      <div className="mx-auto grid max-w-4xl gap-4 p-4 md:p-6">
        <div className="flex items-center gap-3">
          <IdCard className="text-muted-foreground size-5" />
          <h1 className="text-lg font-semibold">{t("abdm_hpr_page_title")}</h1>
        </div>
        <p className="text-muted-foreground text-sm">
          {t("abdm_hpr_page_intro")}
        </p>
        {data && username && username !== data.careUser.username && (
          <Alert variant="warning">
            <AlertDescription>
              {t("abdm_hpr_own_account_only").replace(
                "{{username}}",
                data.careUser.username,
              )}
            </AlertDescription>
          </Alert>
        )}

        {state.isLoading && <Skeleton className="h-40 w-full rounded-xl" />}
        {state.isError && (
          <Alert variant="destructive">
            <AlertDescription>{t("abdm_hpr_load_failed")}</AlertDescription>
          </Alert>
        )}
        {error && (
          <Alert variant="destructive">
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {data && !profile && !showCreate && (
          <Card>
            <CardHeader>
              <CardTitle>{t("abdm_hpr_none_title")}</CardTitle>
              <CardDescription>{t("abdm_hpr_none_intro")}</CardDescription>
            </CardHeader>
            <CardFooter className="flex flex-wrap gap-2 border-t">
              <Button
                type="button"
                size="sm"
                onClick={() => setLoginOpen(true)}
              >
                <LogIn className="size-4" /> {t("abdm_hpr_link_existing")}
              </Button>
              <Button
                type="button"
                variant="outline"
                size="sm"
                onClick={() => setCreating(true)}
              >
                <IdCard className="size-4" /> {t("abdm_hpr_create_new")}
              </Button>
            </CardFooter>
          </Card>
        )}

        {showCreate && data && <HpidCreateWizard state={data} />}

        {profile && data && (
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                {profile.name || profile.hprId}
                <Badge
                  variant={data.session.active ? "success" : "neutral"}
                  size="sm"
                  className="ml-auto"
                >
                  {data.session.active
                    ? t("abdm_hpr_session_active")
                    : t("abdm_hpr_session_inactive")}
                </Badge>
              </CardTitle>
              <CardDescription>
                {t(`abdm_hpr_source_${profile.source}`)}
              </CardDescription>
            </CardHeader>
            <CardContent className="grid gap-2 text-sm sm:grid-cols-[10rem_1fr]">
              <span className="text-muted-foreground">{t("abdm_hpr_id")}</span>
              <span className="font-mono">{profile.hprId || "—"}</span>
              <span className="text-muted-foreground">
                {t("abdm_hpr_id_number")}
              </span>
              <span className="font-mono">{profile.hprIdNumber || "—"}</span>
              <span className="text-muted-foreground">
                {t("abdm_hpid_role")}
              </span>
              <span>
                {data.roles.find((r) => r.code === profile.role)?.name ?? "—"}
              </span>
              <span className="text-muted-foreground">
                {t("abdm_hpr_registration_status")}
              </span>
              <span>
                {profile.registeredAt
                  ? t("abdm_hpr_registered")
                  : t("abdm_hpr_not_registered")}
              </span>
              {data.session.expiresAt && (
                <>
                  <span className="text-muted-foreground">
                    {t("abdm_hpr_session_until")}
                  </span>
                  <span>
                    {new Date(data.session.expiresAt).toLocaleString()}
                  </span>
                </>
              )}
            </CardContent>
            <CardFooter className="flex flex-wrap gap-2 border-t">
              <Button
                type="button"
                size="sm"
                variant={data.session.active ? "outline" : "default"}
                disabled={busy}
                onClick={() => setLoginOpen(true)}
              >
                <LogIn className="size-4" />{" "}
                {data.session.active
                  ? t("abdm_hpr_login_again")
                  : t("abdm_hpr_login")}
              </Button>
              {data.session.active && (
                <Button
                  type="button"
                  size="sm"
                  variant="ghost"
                  disabled={busy}
                  onClick={() => session.mutate("logout")}
                >
                  <LogOut className="size-4" /> {t("abdm_hpr_logout")}
                </Button>
              )}
              <Button
                type="button"
                size="sm"
                variant="ghost"
                disabled={busy || !data.session.active}
                onClick={() => info.mutate()}
              >
                {info.isPending ? (
                  <Loader2 className="size-4 animate-spin" />
                ) : (
                  <RefreshCw className="size-4" />
                )}{" "}
                {t("abdm_hpr_refresh_info")}
              </Button>
              <Button
                type="button"
                size="sm"
                variant="ghost"
                className="text-destructive ml-auto"
                disabled={busy}
                onClick={() =>
                  window.confirm(t("abdm_hpr_unlink_confirm")) &&
                  session.mutate("unlink")
                }
              >
                <Unlink className="size-4" /> {t("abdm_hpr_unlink")}
              </Button>
            </CardFooter>
          </Card>
        )}

        {profile && data && (!profile.registeredAt || editing) && (
          <HprRegisterForm state={data} onDone={() => setEditing(false)} />
        )}
        {profile && data && profile.registeredAt && !editing && (
          <Card>
            <CardHeader>
              <CardTitle>{t("abdm_hpr_professional_title")}</CardTitle>
              <CardDescription>
                {t("abdm_hpr_professional_intro")}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {professional ? (
                <pre className="bg-muted max-h-80 overflow-auto rounded p-3 text-xs">
                  {JSON.stringify(professional, null, 2)}
                </pre>
              ) : (
                <p className="text-muted-foreground text-sm">
                  {t("abdm_hpr_professional_none")}
                </p>
              )}
            </CardContent>
            <CardFooter className="border-t">
              <Button
                type="button"
                size="sm"
                variant="outline"
                onClick={() => setEditing(true)}
              >
                {t("abdm_hpr_update")}
              </Button>
            </CardFooter>
          </Card>
        )}
        {profile && data && <Documents state={data} />}

        <HprLoginDialog
          open={loginOpen}
          onOpenChange={setLoginOpen}
          pendingLogin={data?.pendingLogin ?? null}
        />
      </div>
    </PluginComponent>
  );
}
