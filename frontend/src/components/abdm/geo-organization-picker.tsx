import { Label } from "@/components/ui/label";
import { Skeleton } from "@/components/ui/skeleton";
import { useTranslation } from "@/hooks/use-translation";
import careApi, { type CareGovtOrganization } from "@/lib/careApi";
import { query } from "@/lib/request";
import { selectClass } from "@/components/abdm/nhpr-shared";
import { useQuery } from "@tanstack/react-query";
import { useEffect, useRef, useState } from "react";

/**
 * Cascading picker over Care's government organizations (state → district → local body → ward),
 * from the public list `GET /api/v1/govt/organization/?parent=` (care/emr/api/viewsets/organization.py).
 * The core facility form accepts a leaf only (care_fe FacilityForm.tsx:110-114), so the picker
 * reports a value only when the picked organization has no children. `initial` prefills the first
 * levels, for a registry record whose state and district were matched by name (ADR-016).
 */

function useChildren(parentId: string | null) {
  return useQuery<{ results: CareGovtOrganization[]; count: number }>({
    queryKey: ["abdm", "govt-organizations", parentId ?? "root"],
    queryFn: query(careApi.govtOrganizations, {
      queryParams: { parent: parentId ?? "", limit: 200 },
      silent: true,
    }),
    staleTime: 5 * 60 * 1000,
  });
}

function Level({
  parentId,
  value,
  onChange,
  label,
  first,
}: {
  parentId: string | null;
  value: string;
  onChange: (org: CareGovtOrganization | null) => void;
  label: string;
  first: boolean;
}) {
  const { t } = useTranslation();
  const children = useChildren(parentId);
  const options = children.data?.results ?? [];
  if (children.isLoading) return <Skeleton className="h-10 w-full" />;
  if (!first && options.length === 0) return null;
  return (
    <div className="grid gap-1.5">
      <Label htmlFor={`geo-${parentId ?? "root"}`}>{label}</Label>
      <select
        id={`geo-${parentId ?? "root"}`}
        className={selectClass}
        value={value}
        onChange={(e) =>
          onChange(options.find((o) => o.id === e.target.value) ?? null)
        }
      >
        <option value="">{t("abdm_geo_pick")}</option>
        {options.map((o) => (
          <option key={o.id} value={o.id}>
            {o.name}
          </option>
        ))}
      </select>
      {children.data && children.data.count > options.length && (
        <span className="text-muted-foreground text-xs">
          {t("abdm_geo_more").replace("{{count}}", String(children.data.count))}
        </span>
      )}
    </div>
  );
}

export default function GeoOrganizationPicker({
  initial,
  onChange,
}: {
  /** The chain to prefill, root first (for example the matched state and district). */
  initial?: CareGovtOrganization[];
  /** The leaf organization id, or "" while the chain is incomplete. */
  onChange: (leafId: string, chain: CareGovtOrganization[]) => void;
}) {
  const { t } = useTranslation();
  const [chain, setChain] = useState<CareGovtOrganization[]>(initial ?? []);

  useEffect(() => {
    if (initial && initial.length) setChain(initial);
  }, [initial]);

  // The parent starts with no organization. A report of "" on the first render tells it nothing, and
  // it makes the parent form look changed before the person picked an organization.
  const reported = useRef("");
  useEffect(() => {
    const last = chain[chain.length - 1];
    const leafId = last && !last.has_children ? last.id : "";
    if (leafId === reported.current) return;
    reported.current = leafId;
    onChange(leafId, chain);
    // The parent owns the callback; re-running on a new callback identity would loop.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [chain]);

  const pick = (depth: number) => (org: CareGovtOrganization | null) =>
    setChain((current) => (org ? [...current.slice(0, depth), org] : current.slice(0, depth)));

  const levelLabel = (depth: number, parent?: CareGovtOrganization) => {
    const kind = parent?.metadata?.govt_org_children_type;
    if (typeof kind === "string" && kind) return kind;
    return t(depth === 0 ? "abdm_geo_state" : "abdm_geo_level").replace(
      "{{n}}",
      String(depth + 1),
    );
  };

  const last = chain[chain.length - 1];
  return (
    <div className="grid gap-3">
      <Level
        parentId={null}
        value={chain[0]?.id ?? ""}
        onChange={pick(0)}
        label={levelLabel(0)}
        first
      />
      {chain.map((org, depth) =>
        org.has_children ? (
          <Level
            key={org.id}
            parentId={org.id}
            value={chain[depth + 1]?.id ?? ""}
            onChange={pick(depth + 1)}
            label={levelLabel(depth + 1, org)}
            first={false}
          />
        ) : null,
      )}
      <p className="text-muted-foreground text-xs">
        {last && !last.has_children
          ? t("abdm_geo_complete").replace(
              "{{path}}",
              chain.map((o) => o.name).join(" › "),
            )
          : t("abdm_geo_help")}
      </p>
    </div>
  );
}
