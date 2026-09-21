import type { CareFacilityCreate } from "@/lib/careApi";

/** The plug's Care facility draft (ADR-016): strings while typed, `FacilityCreateSpec` when sent. */

export type CareFacilityDraft = {
  name: string;
  description: string;
  facility_type: string;
  features: number[];
  pincode: string;
  address: string;
  phone_number: string;
  latitude: string;
  longitude: string;
  geo_organization: string;
  is_public: boolean;
};

export const blankFacilityDraft: CareFacilityDraft = {
  name: "",
  description: "",
  facility_type: "",
  features: [],
  pincode: "",
  address: "",
  phone_number: "+91",
  latitude: "",
  longitude: "",
  geo_organization: "",
  is_public: true,
};

const PHONE_RE = /^\+[1-9]\d{7,14}$/;
const PINCODE_RE = /^[1-9]\d{5}$/;

/** Field-level problems the person must fix before the create call. Keys are field names. */
export function validateDraft(
  draft: CareFacilityDraft,
  t: (k: string) => string,
): Partial<Record<keyof CareFacilityDraft, string>> {
  const errors: Partial<Record<keyof CareFacilityDraft, string>> = {};
  if (!draft.name.trim()) errors.name = t("abdm_form_required");
  if (!draft.facility_type) errors.facility_type = t("abdm_form_required");
  if (!draft.address.trim()) errors.address = t("abdm_form_required");
  if (!PINCODE_RE.test(draft.pincode)) errors.pincode = t("abdm_form_pincode_invalid");
  if (!PHONE_RE.test(draft.phone_number)) errors.phone_number = t("abdm_form_phone_invalid");
  const lat = Number(draft.latitude);
  const lng = Number(draft.longitude);
  if (draft.latitude && (Number.isNaN(lat) || lat < -90 || lat > 90))
    errors.latitude = t("abdm_form_latitude_invalid");
  if (draft.longitude && (Number.isNaN(lng) || lng < -180 || lng > 180))
    errors.longitude = t("abdm_form_longitude_invalid");
  if (!draft.geo_organization) errors.geo_organization = t("abdm_form_geo_invalid");
  return errors;
}

/** The `FacilityCreateSpec` body for a valid draft. */
export function toCreateBody(draft: CareFacilityDraft): CareFacilityCreate {
  return {
    name: draft.name.trim(),
    description: draft.description.trim(),
    facility_type: draft.facility_type,
    features: draft.features,
    pincode: Number(draft.pincode),
    address: draft.address.trim(),
    phone_number: draft.phone_number.trim(),
    latitude: draft.latitude ? Number(draft.latitude) : undefined,
    longitude: draft.longitude ? Number(draft.longitude) : undefined,
    geo_organization: draft.geo_organization,
    is_public: draft.is_public,
  };
}
