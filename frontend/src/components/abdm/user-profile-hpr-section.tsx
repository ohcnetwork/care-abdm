import HpidCreateWizard from "@/components/abdm/hpid-create-wizard";
import HprDocuments from "@/components/abdm/hpr-documents";
import HprLoginDialog from "@/components/abdm/hpr-login-dialog";
import HprRegisterForm from "@/components/abdm/hpr-register-form";
import {
  errorMessage,
  hprQueryKey,
  useMaster,
} from "@/components/abdm/nhpr-shared";
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
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Sheet,
  SheetBody,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
} from "@/components/ui/sheet";
import { Skeleton } from "@/components/ui/skeleton";
import { useTranslation } from "@/hooks/use-translation";
import careApi, { type AbdmHprState } from "@/lib/careApi";
import { mutate, query } from "@/lib/request";
import { cn } from "@/lib/utils";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  FileText,
  IdCard,
  Loader2,
  LogIn,
  LogOut,
  MoreHorizontal,
  RefreshCw,
  Unlink,
  Upload,
} from "lucide-react";
import { type ReactNode, useState } from "react";

/**
 * Slot: `UserProfileSections` (care_fe pluginTypes.ts:141-146), mounted on the user profile summary
 * (UserSummary.tsx:203-207). ADR-017 moves "My HPR ID" here from a route of its own.
 *
 * The host built a plug `userNavItems` entry into
 * `/facility/:facilityId/users/:username/<url>` with no fallback (nav-user.tsx:123-131), so the
 * menu item went to `/facility/undefined/...` outside a facility. This slot needs no facility.
 *
 * The section stays a summary card, so the profile page keeps its height. Every long flow — create
 * an HPR ID, register or update the professional profile, the documents — opens in a sheet.
 * The HPR API reads the caller (`users/me/...`), so another person's profile shows nothing.
 */

type Sheets = "create" | "profile" | "documents" | null;

/**
 * A solid button on the inverted hero card: a white face with green words. The `default` variant is
 * green on green there, so it disappears.
 */
const heroSolid =
  "border-white bg-white text-primary-900 shadow-none hover:border-white/90 hover:bg-white/90 dark:bg-white dark:text-primary-900";

/** A quiet button on the inverted hero card: a translucent white face. */
const heroGhost =
  "border-white/25 bg-white/10 text-white shadow-none hover:bg-white/20 hover:text-white dark:bg-white/10 dark:hover:bg-white/20 [:active,[data-pressed]]:bg-white/25";

/** `camelCase` or `snake_case` from the registry, as words a reader knows. */
function humanise(key: string) {
  const words = key
    .replace(/[_-]+/g, " ")
    .replace(/([a-z0-9])([A-Z])/g, "$1 $2")
    .toLowerCase()
    .trim();
  return words.charAt(0).toUpperCase() + words.slice(1);
}

/** What the registry answered, as a field list. Nested blocks stay behind a disclosure. */
function RegistryFacts({
  data,
  inverted,
}: {
  data: Record<string, unknown>;
  inverted?: boolean;
}) {
  const { t } = useTranslation();
  const entries = Object.entries(data).filter(
    ([, v]) => v !== null && v !== "" && v !== undefined,
  );
  const flat = entries.filter(([, v]) => typeof v !== "object");
  const nested = entries.filter(([, v]) => typeof v === "object");
  const labelClass = inverted ? "text-primary-200" : "text-muted-foreground";
  if (!entries.length)
    return (
      <p className={cn("text-sm", labelClass)}>
        {t("abdm_hpr_professional_none")}
      </p>
    );
  return (
    <div className="grid gap-3">
      <dl className="grid gap-x-4 gap-y-2 text-sm sm:grid-cols-[12rem_1fr]">
        {flat.map(([key, value]) => (
          <div key={key} className="contents">
            <dt className={labelClass}>{humanise(key)}</dt>
            <dd className="break-words">{String(value)}</dd>
          </div>
        ))}
      </dl>
      {nested.length > 0 && (
        <details className="text-sm">
          <summary className={cn("cursor-pointer", labelClass)}>
            {t("abdm_hpr_registry_raw")}
          </summary>
          <pre
            className={cn(
              "mt-2 max-h-80 overflow-auto rounded p-3 text-xs",
              inverted ? "bg-white/10" : "bg-muted",
            )}
          >
            {JSON.stringify(Object.fromEntries(nested), null, 2)}
          </pre>
        </details>
      )}
    </div>
  );
}

/**
 * 1 fact of the inverted hero card. The same tile as the encounter hero
 * (encounter-tab.tsx), so the 2 ABDM identity cards read alike.
 */
function HeroFact({
  label,
  children,
  mono,
}: {
  label: string;
  children: ReactNode;
  mono?: boolean;
}) {
  return (
    <div className="grid gap-1 rounded-lg bg-white/5 p-3 ring-1 ring-white/10">
      <span className="text-primary-200 text-[11px] font-medium tracking-wide uppercase">
        {label}
      </span>
      <span className={cn("text-xs text-white", mono && "font-mono break-all")}>
        {children}
      </span>
    </div>
  );
}

export default function AbdmUserProfileSection({
  isOwnProfile,
  className,
}: {
  user?: { username: string };
  isOwnProfile: boolean;
  className?: string;
}) {
  const { t } = useTranslation();
  const qc = useQueryClient();
  const [sheet, setSheet] = useState<Sheets>(null);
  const [loginOpen, setLoginOpen] = useState(false);
  const [error, setError] = useState<string>();

  const state = useQuery<AbdmHprState>({
    queryKey: hprQueryKey,
    queryFn: query(careApi.hprState, { silent: true }),
    enabled: isOwnProfile,
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
  // The category name from the registry's own list for the person's role (100 "Facility Manager"
  // under role 2; 1 "Doctor", 2 "Nurse", … under role 1; observed 2026-09-21). Before the early
  // return: a hook runs on every render.
  const categories = useMaster(
    "hpr-categories",
    { role: String(profile?.role ?? 1) },
    isOwnProfile && Boolean(profile?.categoryCode),
  );

  // The HPR API answers for the caller only, so another person's profile carries no section.
  if (!isOwnProfile) return null;

  const busy = session.isPending || info.isPending;
  const active = Boolean(data?.session.active);
  const professional =
    (profile?.professional?.info as Record<string, unknown> | undefined) ??
    null;
  const account = (profile?.account ?? {}) as Record<string, unknown>;
  const roleName =
    data?.roles.find((r) => r.code === profile?.role)?.name ?? "—";
  const categoryName =
    categories.data?.results.find((c) => c.code === profile?.categoryCode)
      ?.name ??
    (profile?.categoryCode
      ? `${t("abdm_hpr_category_code")} ${profile.categoryCode}`
      : "—");

  return (
    <PluginComponent>
      <section
        className={cn("flex flex-col gap-5 sm:flex-row", className)}
        aria-labelledby="abdm-hpr-section-heading"
      >
        <div className="sm:w-1/4">
          <div className="my-1 text-sm leading-5">
            <p id="abdm-hpr-section-heading" className="mb-2 font-semibold">
              {t("abdm_hpr_page_title")}
            </p>
            <p className="text-muted-foreground">{t("abdm_hpr_page_intro")}</p>
          </div>
        </div>

        <div className="grid gap-3 sm:w-3/4">
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

          {data && !profile && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <IdCard className="text-muted-foreground size-4" />
                  {t("abdm_hpr_none_title")}
                </CardTitle>
                <CardDescription>{t("abdm_hpr_none_intro")}</CardDescription>
              </CardHeader>
              <CardFooter className="flex flex-wrap items-center gap-2 border-t">
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
                  onClick={() => setSheet("create")}
                >
                  <IdCard className="size-4" />{" "}
                  {data.transaction
                    ? t("abdm_hpr_create_continue")
                    : t("abdm_hpr_create_new")}
                </Button>
                {data.transaction && (
                  <Badge variant="warning" size="sm">
                    {t(`abdm_hpid_status_${data.transaction.status}`)}
                  </Badge>
                )}
              </CardFooter>
            </Card>
          )}

          {profile && data && (
            /*
             * Inverted hero card (Rithvik, 2026-09-21). A linked HPR ID is an identity, so it
             * carries the same gradient as the care-context hero in the encounter ABDM tab.
             * `isolate` holds the decorative layers here; the card's `overflow-hidden` trims them.
             */
            <Card className="text-primary-50 shadow-primary-950/25 relative isolate shadow-lg ring-white/10">
              <div
                aria-hidden
                className="from-primary-700 via-primary-900 to-primary-950 pointer-events-none absolute inset-0 -z-10 bg-linear-to-br"
              />
              <div
                aria-hidden
                className="bg-primary-300/25 pointer-events-none absolute -top-24 -right-12 -z-10 size-72 rounded-full blur-3xl"
              />
              <div
                aria-hidden
                className="bg-primary-400/15 pointer-events-none absolute -bottom-28 -left-16 -z-10 size-72 rounded-full blur-3xl"
              />
              <CardHeader>
                <CardTitle className="flex items-center gap-3">
                  <span className="grid size-9 shrink-0 place-items-center rounded-lg bg-white/10 ring-1 ring-white/20">
                    <IdCard className="size-4.5 text-white" />
                  </span>
                  <span className="text-base font-semibold break-all text-white">
                    {profile.name || profile.hprId}
                  </span>
                  <Badge
                    variant={active ? "success" : "neutral"}
                    size="sm"
                    className="ml-auto shrink-0 border-white/25 bg-white/15 text-white backdrop-blur-sm"
                  >
                    {active
                      ? t("abdm_hpr_session_active")
                      : t("abdm_hpr_session_inactive")}
                  </Badge>
                </CardTitle>
                <CardDescription className="text-primary-100/85">
                  {t(`abdm_hpr_source_${profile.source}`)}
                </CardDescription>
              </CardHeader>
              <CardContent className="grid gap-3">
                <div className="grid gap-3 sm:grid-cols-2">
                  <HeroFact label={t("abdm_hpr_id")} mono>
                    {profile.hprId || "\u2014"}
                  </HeroFact>
                  <HeroFact label={t("abdm_hpr_id_number")} mono>
                    {profile.hprIdNumber || "\u2014"}
                  </HeroFact>
                  <HeroFact label={t("abdm_hpid_role")}>{roleName}</HeroFact>
                  <HeroFact label={t("abdm_hpid_category")}>
                    {categoryName}
                  </HeroFact>
                  <HeroFact label={t("abdm_hpr_registration_status")}>
                    {profile.registeredAt
                      ? t("abdm_hpr_registered")
                      : t("abdm_hpr_not_registered")}
                  </HeroFact>
                  {data.session.expiresAt && (
                    <HeroFact label={t("abdm_hpr_session_until")}>
                      {new Date(data.session.expiresAt).toLocaleString()}
                    </HeroFact>
                  )}
                </div>
                {Object.keys(account).length > 0 && (
                  <details className="text-sm">
                    <summary className="text-primary-200 cursor-pointer">
                      {t("abdm_hpr_account_details")}
                    </summary>
                    <div className="mt-2 rounded-lg bg-white/5 p-3 text-white ring-1 ring-white/10">
                      <RegistryFacts data={account} inverted />
                    </div>
                  </details>
                )}
              </CardContent>
              <CardFooter className="flex flex-wrap items-center gap-2 border-t border-white/15">
                {!active && (
                  <Button
                    type="button"
                    size="sm"
                    variant="secondary"
                    disabled={busy}
                    className={heroSolid}
                    onClick={() => setLoginOpen(true)}
                  >
                    <LogIn className="size-4" /> {t("abdm_hpr_login")}
                  </Button>
                )}
                <Button
                  type="button"
                  size="sm"
                  variant={active ? "secondary" : "outline"}
                  className={active ? heroSolid : heroGhost}
                  onClick={() => setSheet("profile")}
                >
                  <FileText className="size-4" />{" "}
                  {t("abdm_hpr_registration_status")}
                </Button>
                <Button
                  type="button"
                  size="sm"
                  variant="outline"
                  className={heroGhost}
                  onClick={() => setSheet("documents")}
                >
                  <Upload className="size-4" /> {t("abdm_hpr_documents_title")}
                </Button>
                <DropdownMenu>
                  <DropdownMenuTrigger
                    render={
                      <Button
                        type="button"
                        size="icon-sm"
                        variant="outline"
                        className={cn("ml-auto", heroGhost)}
                        aria-label={t("abdm_hpr_more_actions")}
                        disabled={busy}
                      >
                        {busy ? (
                          <Loader2 className="size-4 animate-spin" />
                        ) : (
                          <MoreHorizontal className="size-4" />
                        )}
                      </Button>
                    }
                  />
                  <DropdownMenuContent align="end" className="w-auto min-w-52">
                    <DropdownMenuItem onClick={() => setLoginOpen(true)}>
                      <LogIn /> {t("abdm_hpr_login_again")}
                    </DropdownMenuItem>
                    <DropdownMenuItem
                      disabled={!active}
                      onClick={() => info.mutate()}
                    >
                      <RefreshCw /> {t("abdm_hpr_refresh_info")}
                    </DropdownMenuItem>
                    {active && (
                      <DropdownMenuItem
                        onClick={() => session.mutate("logout")}
                      >
                        <LogOut /> {t("abdm_hpr_logout")}
                      </DropdownMenuItem>
                    )}
                    <DropdownMenuSeparator />
                    <DropdownMenuItem
                      variant="destructive"
                      onClick={() =>
                        window.confirm(t("abdm_hpr_unlink_confirm")) &&
                        session.mutate("unlink")
                      }
                    >
                      <Unlink /> {t("abdm_hpr_unlink")}
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </CardFooter>
            </Card>
          )}
        </div>

        {/* Create an HPR ID. The Aadhaar page of the registry opens in a new tab. */}
        <Sheet
          open={sheet === "create"}
          onOpenChange={(open) => setSheet(open ? "create" : null)}
        >
          <SheetContent size="lg">
            <SheetHeader>
              <SheetTitle>{t("abdm_hpid_create_title")}</SheetTitle>
              <SheetDescription>{t("abdm_hpid_create_intro")}</SheetDescription>
            </SheetHeader>
            <SheetBody>
              {data && (
                <HpidCreateWizard
                  state={data}
                  embedded
                  onDone={() => setSheet(null)}
                />
              )}
            </SheetBody>
          </SheetContent>
        </Sheet>

        {/* The professional profile: what the registry holds, then the register or update form. */}
        <Sheet
          open={sheet === "profile"}
          onOpenChange={(open) => setSheet(open ? "profile" : null)}
        >
          <SheetContent size="xl">
            <SheetHeader>
              <SheetTitle>
                {profile?.registeredAt
                  ? t("abdm_hpr_update_title")
                  : t("abdm_hpr_register_title")}
              </SheetTitle>
              <SheetDescription>
                {t("abdm_hpr_register_intro")}
              </SheetDescription>
            </SheetHeader>
            <SheetBody className="grid gap-4">
              {!active && (
                <Alert variant="warning">
                  <AlertDescription>
                    {t("abdm_hpr_documents_need_session")}
                  </AlertDescription>
                </Alert>
              )}
              <details className="text-sm">
                <summary className="text-muted-foreground cursor-pointer">
                  {t("abdm_hpr_professional_title")}
                </summary>
                <div className="mt-2 grid gap-2">
                  {professional ? (
                    <RegistryFacts data={professional} />
                  ) : (
                    <p className="text-muted-foreground">
                      {t("abdm_hpr_professional_none")}
                    </p>
                  )}
                  <div>
                    <Button
                      type="button"
                      size="sm"
                      variant="outline"
                      disabled={!active || info.isPending}
                      onClick={() => info.mutate()}
                    >
                      {info.isPending ? (
                        <Loader2 className="size-4 animate-spin" />
                      ) : (
                        <RefreshCw className="size-4" />
                      )}{" "}
                      {t("abdm_hpr_refresh_info")}
                    </Button>
                  </div>
                </div>
              </details>
              {data && (
                <HprRegisterForm
                  state={data}
                  embedded
                  onDone={() => setSheet(null)}
                />
              )}
            </SheetBody>
          </SheetContent>
        </Sheet>

        {/* The certificate slots the registry holds. */}
        <Sheet
          open={sheet === "documents"}
          onOpenChange={(open) => setSheet(open ? "documents" : null)}
        >
          <SheetContent size="lg">
            <SheetHeader>
              <SheetTitle>{t("abdm_hpr_documents_title")}</SheetTitle>
              <SheetDescription>
                {t("abdm_hpr_documents_intro")}
              </SheetDescription>
            </SheetHeader>
            <SheetBody>{data && <HprDocuments state={data} />}</SheetBody>
          </SheetContent>
        </Sheet>

        <HprLoginDialog
          open={loginOpen}
          onOpenChange={setLoginOpen}
          pendingLogin={data?.pendingLogin ?? null}
        />
      </section>
    </PluginComponent>
  );
}
