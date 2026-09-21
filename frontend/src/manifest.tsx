import { Suspense, lazy } from "react";
import { Network } from "lucide-react";
// Static: an override renders inside the host tree with no Suspense boundary of its own.
import AddFacilitySheetOverride from "@/components/abdm/add-facility-sheet-override";

// Slot names must match care_fe/src/pluginTypes.ts `SupportedPluginComponents`
// (read 2026-09-09). Host mount points:
//   FacilityHomeActions                     FacilityHome
//   PatientRegistrationForm                 PatientRegistration.tsx:410
//   PatientDetailsTabDemographyGeneralInfo  PatientDetailsTab/Demography.tsx:172
//   PatientHomeActions                      PatientProfile.tsx:177
//   PatientSearchActions                    PatientIndex.tsx:259
//   EncounterActions                        summary-panel-actions.tab.tsx:95
//   EncounterOverviewTop                    pages/Encounters/tabs/overview.tsx:56
//   UserProfileSections                     Users/UserSummary.tsx:203
const AbdmFacilitySetupPage = lazy(
  () => import("@/components/abdm/facility-setup-page"),
);
const AbdmAdminDashboard = lazy(
  () => import("@/components/abdm/admin-dashboard"),
);
const AbdmHfrOnboardingWizard = lazy(
  () => import("@/components/abdm/hfr-onboarding-wizard"),
);
const AbdmAddFacilityWizard = lazy(
  () => import("@/components/abdm/add-facility-wizard"),
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
    // Instance level: the bridge is 1 per clientId. The host appends plug
    // adminNavItems after its own admin links (admin-nav.tsx:104).
    "/admin/abdm": () => (
      <Suspense fallback={null}>
        <AbdmAdminDashboard />
      </Suspense>
    ),
    // ADR-015 (M4). The HFR onboarding wizard stays outside the host's
    // /facility/:facilityId/settings* prefix, like the setup page.
    "/facility/:facilityId/abdm/hfr/register": ({
      facilityId,
    }: {
      facilityId: string;
    }) => (
      <Suspense fallback={null}>
        <AbdmHfrOnboardingWizard facilityId={facilityId} />
      </Suspense>
    ),
    // ADR-016: "Add a facility", from the ABDM admin dashboard or the organization facilities page
    // (the AddFacilitySheet override). `?organization=<id>` is optional context for the geo picker.
    "/abdm/facilities/new": () => (
      <Suspense fallback={null}>
        <AbdmAddFacilityWizard />
      </Suspense>
    ),
  },
  // ADR-016: replace the host's "Add facility" sheet with the wizard entry. Needs the host build
  // variable REACT_MFE_REGISTERED_COMPONENTS to name AddFacilitySheet (care_fe
  // docs/care-apps-plugin-overrides.md); otherwise the host keeps its own sheet.
  overrides: [
    {
      component: "AddFacilitySheet",
      replacement: AddFacilitySheetOverride,
      description:
        "ABDM: every new facility passes the registry choice (Add a facility wizard).",
    },
  ],
  // ADR-017: "My HPR ID" is a section of the user profile page, not a route. The host builds a
  // `userNavItems` entry into `/facility/:facilityId/users/:username/<url>` with no fallback
  // (care_fe nav-user.tsx:123-131), so outside a facility that link went to `/facility/undefined/`.
  adminNavItems: [
    {
      name: "ABDM",
      url: "/admin/abdm",
      icon: <Network />,
    },
  ],
  // Host slot `encounterTabs` (EncounterShow.tsx:80,192-200). The host owns the tab label
  // `ENCOUNTER_TAB__abdm` ("ABDM Records") and the route `.../encounter/:encounterId/abdm`.
  encounterTabs: {
    abdm: lazy(() => import("@/components/abdm/encounter-tab")),
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
    EncounterActions: lazy(() => import("@/components/abdm/encounter-actions")),
    EncounterOverviewTop: lazy(
      () => import("@/components/abdm/encounter-overview-top"),
    ),
    // ADR-017: the HPR section of the user profile summary (UserSummary.tsx:203-207).
    UserProfileSections: lazy(
      () => import("@/components/abdm/user-profile-hpr-section"),
    ),
  },
} as const;

export default manifest;
