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
  type AbdmAdminOverview,
  type AbdmBridgeState,
} from "@/lib/careApi";
import { mutate, query } from "@/lib/request";
import { cn } from "@/lib/utils";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  CheckCircle2,
  CircleDashed,
  Hospital,
  Inbox,
  RefreshCcw,
  Router,
  Server,
} from "lucide-react";
import { useState } from "react";

/**
 * Instance dashboard at /admin/abdm (manifest `routes` + `adminNavItems`).
 *
 * The bridge is 1 per clientId (docs /getting-started/sandbox: "One URL covers your whole
 * integration"), so it belongs here and not on a facility page. Every value on this page is
 * read live from the gateway through the plug; nothing is snapshotted (ADR-011).
 */

const OVERVIEW_KEY = ["abdm", "admin", "overview"];

function errorMessage(error: unknown, fallback: string) {
  if (error && typeof error === "object" && "cause" in error) {
    const cause = (error as { cause?: Record<string, unknown> }).cause;
    const value = cause?.errors ?? cause?.message;
    if (typeof value === "string") return value;
  }
  return fallback;
}

function formatDate(value?: string | null) {
  return value ? new Date(value).toLocaleString() : "\u2014";
}

function text(value: unknown, yes: string, no: string) {
  if (value === null || value === undefined || value === "") return "\u2014";
  if (typeof value === "boolean") return value ? yes : no;
  if (typeof value === "string" || typeof value === "number") return `${value}`;
  return JSON.stringify(value);
}

/**
 * Sandbox shape observed 2026-09-15 (findings B18): `{id, name, types: ["HIP","HIU"], active}`.
 * The docs page gateway-get-bridge-service-by-id names `serviceId`, `isHip`, `isHiu`,
 * `registerTime` instead; both shapes are read.
 */
function serviceRows(services: unknown[]) {
  return services.map((service, index) => {
    const row =
      service && typeof service === "object"
        ? (service as Record<string, unknown>)
        : { name: service };
    const types = Array.isArray(row.types)
      ? row.types.map(String)
      : [row.isHip ? "HIP" : "", row.isHiu ? "HIU" : ""].filter(Boolean);
    return {
      key: `${row.id ?? row.serviceId ?? index}`,
      serviceId: row.id ?? row.serviceId,
      name: row.name ?? row.hipName ?? row.facilityName,
      type: types.join(", "),
      active: row.active,
      registered: row.registerTime ?? row.dateCreated,
    };
  });
}

function Value({ label, value }: { label: string; value?: string | null }) {
  return (
    <div className="grid gap-0.5">
      <span className="text-muted-foreground text-xs">{label}</span>
      <span className="font-mono text-xs break-all">{value || "\u2014"}</span>
    </div>
  );
}

function StatusLine({ done, label }: { done: boolean; label: string }) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 text-xs",
        done ? "text-green-800" : "text-muted-foreground",
      )}
    >
      {done ? (
        <CheckCircle2 className="size-3.5" />
      ) : (
        <CircleDashed className="size-3.5" />
      )}
      {label}
    </span>
  );
}

export default function AbdmAdminDashboard() {
  const { t } = useTranslation();
  const qc = useQueryClient();
  const [actionError, setActionError] = useState<string>();

  const overview = useQuery<AbdmAdminOverview>({
    queryKey: OVERVIEW_KEY,
    queryFn: query(careApi.adminOverview, { silent: true }),
    retry: false,
  });
  const callbacks = useQuery({
    queryKey: ["abdm", "admin", "callbacks"],
    queryFn: query(careApi.callbacks, {
      queryParams: { limit: "20" },
      silent: true,
    }),
    retry: false,
  });
  const registerUrl = useMutation<AbdmBridgeState, unknown, Record<string, never>>({
    mutationFn: mutate(careApi.bridgeRegisterUrl, { silent: true }),
    onMutate: () => setActionError(undefined),
    onSuccess: () => qc.invalidateQueries({ queryKey: OVERVIEW_KEY }),
    onError: (error) =>
      setActionError(errorMessage(error, t("abdm_bridge_register_failed"))),
  });

  const data = overview.data;
  const bridgeUrl = data?.bridge?.url ?? "";
  const registered = Boolean(bridgeUrl) && bridgeUrl === data?.callback_url;
  const busy = registerUrl.isPending || overview.isFetching;

  return (
    <PluginComponent>
      <div className="mx-auto w-full max-w-5xl p-4 md:p-6">
        <div className="mt-3 flex flex-wrap items-start justify-between gap-3">
          <div className="grid gap-1">
            <h1 className="text-2xl font-semibold">{t("abdm_admin_title")}</h1>
            <p className="text-muted-foreground max-w-2xl text-sm">
              {t("abdm_admin_intro")}
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Badge
              variant={
                overview.isLoading
                  ? "neutral"
                  : data?.gateway.ok
                    ? "success"
                    : "destructive"
              }
              size="lg"
            >
              {overview.isLoading
                ? t("abdm_gateway_checking")
                : data?.gateway.ok
                  ? t("abdm_gateway_connected")
                  : t("abdm_gateway_unreachable")}
            </Badge>
            <Button
              type="button"
              variant="outline"
              size="sm"
              disabled={busy}
              onClick={() => {
                overview.refetch();
                callbacks.refetch();
              }}
            >
              <RefreshCcw className="size-4" />
              {t("abdm_refresh_from_gateway")}
            </Button>
          </div>
        </div>

        <div className="mt-6 grid gap-4">
          {overview.isError && (
            <Alert variant="destructive">
              <AlertDescription>
                {errorMessage(overview.error, t("abdm_bridge_load_failed"))}
              </AlertDescription>
            </Alert>
          )}
          {actionError && (
            <Alert variant="destructive">
              <AlertDescription>{actionError}</AlertDescription>
            </Alert>
          )}
          {data?.error && (
            <Alert variant="warning">
              <AlertDescription>{data.error}</AlertDescription>
            </Alert>
          )}

          {overview.isLoading ? (
            <div className="grid gap-4">
              <Skeleton className="h-48 w-full rounded-xl" />
              <Skeleton className="h-48 w-full rounded-xl" />
            </div>
          ) : (
            <>
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Router className="text-muted-foreground size-4" />
                    {t("abdm_bridge")}
                  </CardTitle>
                  <CardDescription>{t("abdm_bridge_description")}</CardDescription>
                </CardHeader>
                <CardContent className="grid gap-3 md:grid-cols-2">
                  <Value label={t("abdm_callback_url")} value={data?.callback_url} />
                  <Value label={t("abdm_registered_url")} value={bridgeUrl} />
                  <Value label={t("abdm_bridge_id")} value={data?.bridge?.id} />
                  <Value label={t("abdm_bridge_name")} value={data?.bridge?.name} />
                  <Value
                    label={t("abdm_active")}
                    value={text(data?.bridge?.active, t("abdm_yes"), t("abdm_no"))}
                  />
                  <Value
                    label={t("abdm_blocklisted")}
                    value={text(data?.bridge?.blocklisted, t("abdm_yes"), t("abdm_no"))}
                  />
                </CardContent>
                <CardFooter className="flex flex-wrap items-center gap-3 border-t">
                  <StatusLine
                    done={registered}
                    label={
                      registered
                        ? t("abdm_bridge_registered")
                        : t("abdm_bridge_not_registered")
                    }
                  />
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    className="ml-auto"
                    disabled={busy || !data?.callback_url}
                    onClick={() => registerUrl.mutate({})}
                  >
                    {t("abdm_register_callback_url")}
                  </Button>
                </CardFooter>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Server className="text-muted-foreground size-4" />
                    {t("abdm_bridge_services")}
                  </CardTitle>
                  <CardDescription>
                    {t("abdm_bridge_services_description")}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {!data?.services.length ? (
                    <p className="text-muted-foreground text-sm">
                      {t("abdm_no_bridge_services")}
                    </p>
                  ) : (
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>{t("abdm_service_id")}</TableHead>
                          <TableHead>{t("abdm_facility_name")}</TableHead>
                          <TableHead>{t("abdm_type")}</TableHead>
                          <TableHead>{t("abdm_active")}</TableHead>
                          <TableHead>{t("abdm_last_registration")}</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {serviceRows(data.services).map((row) => (
                          <TableRow key={row.key}>
                            <TableCell className="font-mono text-xs">
                              {text(row.serviceId, "", "")}
                            </TableCell>
                            <TableCell>{text(row.name, "", "")}</TableCell>
                            <TableCell>{row.type || "\u2014"}</TableCell>
                            <TableCell>
                              {text(row.active, t("abdm_yes"), t("abdm_no"))}
                            </TableCell>
                            <TableCell className="text-xs">
                              {typeof row.registered === "string"
                                ? formatDate(row.registered)
                                : "\u2014"}
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  )}
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Hospital className="text-muted-foreground size-4" />
                    {t("abdm_admin_facilities")}
                  </CardTitle>
                  <CardDescription>
                    {t("abdm_admin_facilities_description")}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {!data?.facilities.length ? (
                    <p className="text-muted-foreground text-sm">
                      {t("abdm_admin_no_facilities")}
                    </p>
                  ) : (
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>{t("abdm_facility_name")}</TableHead>
                          <TableHead>{t("abdm_facility_hfr_id")}</TableHead>
                          <TableHead>{t("abdm_hip_id")}</TableHead>
                          <TableHead>{t("abdm_hip_name")}</TableHead>
                          <TableHead>{t("abdm_admin_hip_status")}</TableHead>
                          <TableHead />
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {data.facilities.map((row) => (
                          <TableRow key={row.id}>
                            <TableCell>
                              <div className="grid">
                                <span>{row.name}</span>
                                {row.last_error && (
                                  <span className="text-destructive text-xs">
                                    {row.last_error}
                                  </span>
                                )}
                                {row.last_failure && (
                                  <span className="text-destructive text-xs">
                                    {row.last_failure.operation_id}
                                    {row.last_failure.code &&
                                      ` \u00b7 ${row.last_failure.code}`}
                                    {` \u00b7 ${formatDate(row.last_failure.sent_at)}`}
                                    {row.last_failure.detail &&
                                      ` \u00b7 ${row.last_failure.detail}`}
                                  </span>
                                )}
                              </div>
                            </TableCell>
                            <TableCell className="font-mono text-xs">
                              {row.facility_id}
                            </TableCell>
                            <TableCell className="font-mono text-xs">
                              {row.hip_id || "\u2014"}
                            </TableCell>
                            <TableCell>{row.hip_name || "\u2014"}</TableCell>
                            <TableCell>
                              <div className="grid gap-0.5">
                                <Badge
                                  variant={row.hip_id ? "success" : "neutral"}
                                  size="sm"
                                >
                                  {row.hip_id
                                    ? t("abdm_admin_hip_registered")
                                    : t("abdm_admin_hip_not_registered")}
                                </Badge>
                                {row.hrp_registered_at && (
                                  <span className="text-muted-foreground text-[11px]">
                                    {formatDate(row.hrp_registered_at)}
                                  </span>
                                )}
                              </div>
                            </TableCell>
                            <TableCell className="text-right">
                              {/* Full page load on purpose: a client-side move from /admin to an
                                  app route crashes the host's PinPageDialog (hooks order). */}
                              <a
                                href={`/facility/${row.id}/abdm/setup`}
                                className="text-primary text-xs underline-offset-4 hover:underline"
                              >
                                {t("abdm_open_setup")}
                              </a>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  )}
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Inbox className="text-muted-foreground size-4" />
                    {t("abdm_admin_callbacks")}
                  </CardTitle>
                  <CardDescription>
                    {t("abdm_admin_callbacks_description")}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  {!callbacks.data?.results.length ? (
                    <p className="text-muted-foreground text-sm">
                      {t("abdm_admin_no_callbacks")}
                    </p>
                  ) : (
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>{t("abdm_admin_received_at")}</TableHead>
                          <TableHead>{t("abdm_admin_operation")}</TableHead>
                          <TableHead>{t("abdm_request_id")}</TableHead>
                          <TableHead>{t("abdm_admin_signature")}</TableHead>
                          <TableHead>{t("abdm_admin_processed")}</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {callbacks.data.results.map((row) => (
                          <TableRow key={row.id}>
                            <TableCell className="text-xs whitespace-nowrap">
                              {formatDate(row.received_at)}
                            </TableCell>
                            <TableCell className="font-mono text-xs">
                              {row.operation_id || row.path}
                            </TableCell>
                            <TableCell className="font-mono text-[11px]">
                              <div className="grid gap-0.5">
                                <span title={row.request_id_header}>
                                  {row.request_id_header.slice(0, 13) || "\u2014"}
                                </span>
                                {row.response_request_id && (
                                  <span
                                    className="text-muted-foreground"
                                    title={row.response_request_id}
                                  >
                                    {"\u21A9 "}
                                    {row.response_request_id.slice(0, 8)}
                                  </span>
                                )}
                              </div>
                            </TableCell>
                            <TableCell>
                              <div className="grid gap-0.5">
                                <Badge
                                  variant={
                                    row.signature_status === "ok"
                                      ? "success"
                                      : "destructive"
                                  }
                                  size="sm"
                                >
                                  {row.signature_status}
                                  {row.signature_header && ` · ${row.signature_header}`}
                                </Badge>
                                {row.signature_error && (
                                  <span className="text-muted-foreground max-w-xs truncate text-[11px]">
                                    {row.signature_error}
                                  </span>
                                )}
                              </div>
                            </TableCell>
                            <TableCell>
                              <Badge
                                variant={
                                  row.processed_status === "handled"
                                    ? "success"
                                    : row.processed_status === "failed"
                                      ? "destructive"
                                      : "neutral"
                                }
                                size="sm"
                              >
                                {row.processed_status}
                              </Badge>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  )}
                </CardContent>
              </Card>
            </>
          )}
        </div>
      </div>
    </PluginComponent>
  );
}
