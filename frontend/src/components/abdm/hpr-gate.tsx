import HprLoginDialog from "@/components/abdm/hpr-login-dialog";
import { hprQueryKey } from "@/components/abdm/nhpr-shared";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useTranslation } from "@/hooks/use-translation";
import careApi, { type AbdmHfrState, type AbdmHprState } from "@/lib/careApi";
import { query } from "@/lib/request";
import { cn } from "@/lib/utils";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { IdCard, LogIn, ShieldAlert } from "lucide-react";
import { navigate } from "raviger";
import type { ReactNode } from "react";
import { useState } from "react";

/**
 * The HPR gate (ADR-016 revision, 2026-09-22).
 *
 * The registry work a facility needs — linking an HFR record and the 5-step HFR onboarding — is
 * done as a person, not as a deployment: `nhpr/facility.py:159-165` refuses every onboarding step
 * without a valid HPR token, and the registry wants that token to belong to a facility manager
 * (`nhpr/rules.py:29`: role 2 "Facility Manager", role 3 both). Rather than carrying a "logged in"
 * status card beside a form that will be refused anyway, the entrances render this gate and nothing
 * else until the person can actually do the work.
 *
 * 3 reasons to block, in the order they must be fixed:
 * - `no_profile`   no HPR ID on the Care account at all -> the user profile page links one.
 * - `inactive`     an HPR ID is linked but the registry session expired -> log in here.
 * - `not_manager`  logged in as role 1 (healthcare professional) -> the registry refuses facility
 *                  work; another person, or a facility-manager role, is needed.
 */

/** The 4 values the gate reads, as `hfr_state` publishes them (`nhpr/facility.py:366-372`). */
export type HprGateSession = AbdmHfrState["hprSession"];

export type HprGateBlock = "no_profile" | "inactive" | "not_manager";

/** The `users/me/abdm/hpr` shape (`nhpr/professional.py:686-698`) as the gate's 4 values. */
export function gateSessionFromHprState(
  state: AbdmHprState | undefined,
): HprGateSession | undefined {
  if (!state) return undefined;
  return {
    hprId: state.profile?.hprId || state.profile?.hprIdNumber || "",
    name: state.profile?.name || "",
    active: Boolean(state.session.active),
    expiresAt: state.session.expiresAt,
    role: state.profile?.role ?? null,
  };
}

/**
 * Why this person cannot do registry work, or null when they can. A null role is not a refusal:
 * the plug heals it from the category (`nhpr/professional.py:126-127`) and only a role the
 * registry itself named as 1 is known to be short of facility-manager rights.
 */
export function hprGateBlock(
  session: HprGateSession | undefined,
): HprGateBlock | null {
  if (!session || !session.hprId) return "no_profile";
  if (!session.active) return "inactive";
  if (session.role === 1) return "not_manager";
  return null;
}

/**
 * The blocked card. `children` render only when nothing blocks, so a caller wraps its registry
 * panel in this and stops thinking about the session.
 */
export default function HprGate({
  session,
  loading,
  children,
  className,
  onSession,
}: {
  session: HprGateSession | undefined;
  /** The caller's state query is still in flight: render nothing rather than a wrong refusal. */
  loading?: boolean;
  children: ReactNode;
  className?: string;
  /** A login finished here; the caller refetches whatever holds the session. */
  onSession?: () => void;
}) {
  const { t } = useTranslation();
  const qc = useQueryClient();
  const [loginOpen, setLoginOpen] = useState(false);
  const block = hprGateBlock(session);

  // Only for the login dialog's resumable transaction; the gate's verdict comes from `session`.
  const hpr = useQuery<AbdmHprState>({
    queryKey: hprQueryKey,
    queryFn: query(careApi.hprState, { silent: true }),
    enabled: block === "inactive" || block === "no_profile",
    retry: false,
  });

  if (loading) return null;
  if (!block) return <>{children}</>;

  const Icon = block === "not_manager" ? ShieldAlert : IdCard;

  return (
    <>
      <Card className={cn(className)}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Icon className="text-muted-foreground size-4" />
            {t(`abdm_hpr_gate_${block}_title`)}
          </CardTitle>
          <CardDescription>{t(`abdm_hpr_gate_${block}_help`)}</CardDescription>
        </CardHeader>
        {session?.hprId && (
          <CardContent className="text-muted-foreground grid gap-1 text-sm">
            <span>
              {t("abdm_hpr_gate_current", {
                id: [session.name, session.hprId].filter(Boolean).join(" · "),
              })}
            </span>
          </CardContent>
        )}
        <CardFooter className="flex flex-wrap items-center gap-2 border-t">
          {block === "inactive" ? (
            <Button type="button" size="sm" onClick={() => setLoginOpen(true)}>
              <LogIn className="size-4" /> {t("abdm_hpr_login")}
            </Button>
          ) : (
            <Button
              type="button"
              size="sm"
              variant={block === "not_manager" ? "outline" : "default"}
              onClick={() => navigate("/user/profile")}
            >
              <IdCard className="size-4" /> {t("abdm_hpr_gate_open_profile")}
            </Button>
          )}
          {block === "not_manager" && (
            <Button
              type="button"
              size="sm"
              variant="ghost"
              onClick={() => setLoginOpen(true)}
            >
              <LogIn className="size-4" /> {t("abdm_hpr_gate_login_other")}
            </Button>
          )}
        </CardFooter>
      </Card>
      <HprLoginDialog
        open={loginOpen}
        onOpenChange={setLoginOpen}
        pendingLogin={hpr.data?.pendingLogin ?? null}
        onDone={() => {
          qc.invalidateQueries({ queryKey: hprQueryKey });
          onSession?.();
        }}
      />
    </>
  );
}
