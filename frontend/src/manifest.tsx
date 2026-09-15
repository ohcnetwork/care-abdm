import { Suspense, lazy } from "react";

// Slot names must match care_fe/src/pluginTypes.ts `SupportedPluginComponents`
// (read 2026-09-09). Host mount points:
//   FacilityHomeActions                     FacilityHome
//   PatientRegistrationForm                 PatientRegistration.tsx:410
//   PatientDetailsTabDemographyGeneralInfo  PatientDetailsTab/Demography.tsx:172
//   PatientHomeActions                      PatientProfile.tsx:177
//   PatientSearchActions                    PatientIndex.tsx:259
//   EncounterActions                        summary-panel-actions.tab.tsx:95
//   EncounterOverviewTop                    pages/Encounters/tabs/overview.tsx:56
const AbdmFacilitySetupPage = lazy(
  () => import("@/components/abdm/facility-setup-page"),
);

const manifest = {
  plugin: "care-abdm-fe",
  routes: {
    // The host merges plug routes into its router
    // (care_fe/src/Routers/AppRouter.tsx:104-115) and host routes win on a
    // collision. This path stays clear of /facility/:facilityId/settings*,
    // which the host claims. The host does not wrap a route node in Suspense,
    // so the lazy page carries its own boundary.
    "/facility/:facilityId/abdm/setup": ({
      facilityId,
    }: {
      facilityId: string;
    }) => (
      <Suspense fallback={null}>
        <AbdmFacilitySetupPage facilityId={facilityId} />
      </Suspense>
    ),
  },
  components: {
    FacilityHomeActions: lazy(
      () => import("@/components/abdm/facility-home-actions"),
    ),
    PatientRegistrationForm: lazy(
      () => import("@/components/abdm/patient-registration-form"),
    ),
    PatientDetailsTabDemographyGeneralInfo: lazy(
      () => import("@/components/abdm/patient-abha-panel"),
    ),
    PatientHomeActions: lazy(
      () => import("@/components/abdm/patient-home-actions"),
    ),
    PatientSearchActions: lazy(
      () => import("@/components/abdm/patient-search-actions"),
    ),
    EncounterActions: lazy(
      () => import("@/components/abdm/encounter-actions"),
    ),
    EncounterOverviewTop: lazy(
      () => import("@/components/abdm/encounter-overview-top"),
    ),
  },
} as const;

export default manifest;
