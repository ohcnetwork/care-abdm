import GeoOrganizationPicker from "@/components/abdm/geo-organization-picker";
import { selectClass, shortenCoordinate } from "@/components/abdm/nhpr-shared";
import { Button } from "@/components/ui/button";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Skeleton } from "@/components/ui/skeleton";
import { useTranslation } from "@/hooks/use-translation";
import type { CareFacilityDraft } from "@/components/abdm/care-facility-draft";
import careApi, {
  type AbdmFacilityFormOptions,
  type CareGovtOrganization,
} from "@/lib/careApi";
import { query } from "@/lib/request";
import { useQuery } from "@tanstack/react-query";
import { LocateFixed } from "lucide-react";
import type { ReactNode } from "react";

/**
 * The Care facility form the plug ships (ADR-016). The host does not share its `FacilityForm`
 * (care_fe vite.config.mts shares only react, i18next, react-query, raviger, sonner, decimal.js),
 * so the wizard renders the same fields against the same `FacilityCreateSpec`
 * (care/emr/resources/facility/spec.py:100-134): name, facility type, features, description,
 * address, pincode, phone number, latitude and longitude, government organization, public flag.
 * The choice lists come from Care through the plug, so they never drift from the host.
 */

function Field({
  label,
  htmlFor,
  error,
  hint,
  children,
  className,
}: {
  label: string;
  htmlFor?: string;
  error?: string;
  hint?: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <div className={className ?? "grid gap-1.5"}>
      <Label htmlFor={htmlFor}>{label}</Label>
      {children}
      {hint && !error && (
        <span className="text-muted-foreground text-xs">{hint}</span>
      )}
      {error && <span className="text-destructive text-xs">{error}</span>}
    </div>
  );
}

export default function CareFacilityForm({
  draft,
  onChange,
  errors,
  serverErrors,
  geoInitial,
  disabled,
  prefilled,
}: {
  draft: CareFacilityDraft;
  onChange: (next: Partial<CareFacilityDraft>) => void;
  errors: Partial<Record<keyof CareFacilityDraft, string>>;
  /** Care's own validation answer, by field (`loc[0]`). */
  serverErrors?: Record<string, string>;
  /** The government organizations to prefill, root first. */
  geoInitial?: CareGovtOrganization[];
  disabled?: boolean;
  /** Field names a registry record filled, marked so the person knows what to check. */
  prefilled?: Set<keyof CareFacilityDraft>;
}) {
  const { t } = useTranslation();
  const options = useQuery<AbdmFacilityFormOptions>({
    queryKey: ["abdm", "facility-form-options"],
    queryFn: query(careApi.facilityFormOptions, { silent: true }),
    staleTime: 60 * 60 * 1000,
  });
  const problem = (field: keyof CareFacilityDraft) =>
    errors[field] ?? serverErrors?.[field];
  const mark = (field: keyof CareFacilityDraft) =>
    prefilled?.has(field) ? t("abdm_form_prefilled") : undefined;

  return (
    <div className="grid gap-4">
      <div className="grid gap-4 md:grid-cols-2">
        <Field
          label={t("abdm_form_name")}
          htmlFor="cf-name"
          error={problem("name")}
          hint={mark("name")}
        >
          <Input
            id="cf-name"
            value={draft.name}
            disabled={disabled}
            onChange={(e) => onChange({ name: e.target.value })}
          />
        </Field>
        <Field
          label={t("abdm_form_facility_type")}
          htmlFor="cf-type"
          error={problem("facility_type")}
          hint={mark("facility_type")}
        >
          {options.isLoading ? (
            <Skeleton className="h-10 w-full" />
          ) : (
            <select
              id="cf-type"
              className={selectClass}
              value={draft.facility_type}
              disabled={disabled}
              onChange={(e) => onChange({ facility_type: e.target.value })}
            >
              <option value="">{t("abdm_geo_pick")}</option>
              {(options.data?.facilityTypes ?? []).map((o) => (
                <option key={o.id} value={o.name}>
                  {o.name}
                </option>
              ))}
            </select>
          )}
        </Field>
      </div>

      <Field label={t("abdm_form_description")} htmlFor="cf-description">
        <textarea
          id="cf-description"
          className={`${selectClass} min-h-20 py-2`}
          value={draft.description}
          disabled={disabled}
          onChange={(e) => onChange({ description: e.target.value })}
        />
      </Field>

      <Field label={t("abdm_form_features")}>
        <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
          {(options.data?.features ?? []).map((f) => {
            const checked = draft.features.includes(f.id);
            return (
              <label
                key={f.id}
                className="flex items-center gap-2 text-sm"
                htmlFor={`cf-feature-${f.id}`}
              >
                <Checkbox
                  id={`cf-feature-${f.id}`}
                  checked={checked}
                  disabled={disabled}
                  onCheckedChange={(next) =>
                    onChange({
                      features: next
                        ? [...draft.features, f.id]
                        : draft.features.filter((x) => x !== f.id),
                    })
                  }
                />
                {f.name}
              </label>
            );
          })}
        </div>
      </Field>

      <Field
        label={t("abdm_form_address")}
        htmlFor="cf-address"
        error={problem("address")}
        hint={mark("address")}
      >
        <textarea
          id="cf-address"
          className={`${selectClass} min-h-16 py-2`}
          value={draft.address}
          disabled={disabled}
          onChange={(e) => onChange({ address: e.target.value })}
        />
      </Field>

      <div className="grid gap-4 md:grid-cols-2">
        <Field
          label={t("abdm_form_pincode")}
          htmlFor="cf-pincode"
          error={problem("pincode")}
          hint={mark("pincode")}
        >
          <Input
            id="cf-pincode"
            inputMode="numeric"
            maxLength={6}
            value={draft.pincode}
            disabled={disabled}
            onChange={(e) =>
              onChange({ pincode: e.target.value.replace(/\D/g, "") })
            }
          />
        </Field>
        <Field
          label={t("abdm_form_phone")}
          htmlFor="cf-phone"
          error={problem("phone_number")}
          hint={t("abdm_form_phone_help")}
        >
          <Input
            id="cf-phone"
            inputMode="tel"
            value={draft.phone_number}
            disabled={disabled}
            onChange={(e) =>
              onChange({ phone_number: e.target.value.replace(/[^\d+]/g, "") })
            }
          />
        </Field>
      </div>

      <div className="grid gap-4 md:grid-cols-[1fr_1fr_auto]">
        <Field
          label={t("abdm_form_latitude")}
          htmlFor="cf-lat"
          error={problem("latitude")}
          hint={mark("latitude")}
        >
          <Input
            id="cf-lat"
            inputMode="decimal"
            value={draft.latitude}
            disabled={disabled}
            onChange={(e) => onChange({ latitude: e.target.value })}
            onBlur={(e) =>
              onChange({
                latitude: shortenCoordinate(e.target.value, "latitude"),
              })
            }
          />
        </Field>
        <Field
          label={t("abdm_form_longitude")}
          htmlFor="cf-lng"
          error={problem("longitude")}
          hint={mark("longitude")}
        >
          <Input
            id="cf-lng"
            inputMode="decimal"
            value={draft.longitude}
            disabled={disabled}
            onChange={(e) => onChange({ longitude: e.target.value })}
            onBlur={(e) =>
              onChange({
                longitude: shortenCoordinate(e.target.value, "longitude"),
              })
            }
          />
        </Field>
        <div className="grid content-end">
          <Button
            type="button"
            variant="outline"
            size="sm"
            className="h-12 md:h-10"
            disabled={disabled || !("geolocation" in navigator)}
            onClick={() =>
              navigator.geolocation.getCurrentPosition((position) =>
                onChange({
                  latitude: position.coords.latitude.toFixed(6),
                  longitude: position.coords.longitude.toFixed(6),
                }),
              )
            }
          >
            <LocateFixed className="size-4" /> {t("abdm_form_use_location")}
          </Button>
        </div>
      </div>

      <Field
        label={t("abdm_form_geo")}
        error={problem("geo_organization")}
        hint={geoInitial?.length ? t("abdm_form_geo_prefilled") : undefined}
      >
        <GeoOrganizationPicker
          initial={geoInitial}
          onChange={(leafId) => onChange({ geo_organization: leafId })}
        />
      </Field>

      <label className="flex items-center gap-2 text-sm" htmlFor="cf-public">
        <Checkbox
          id="cf-public"
          checked={draft.is_public}
          disabled={disabled}
          onCheckedChange={(next) => onChange({ is_public: Boolean(next) })}
        />
        {t("abdm_form_is_public")}
      </label>
    </div>
  );
}
