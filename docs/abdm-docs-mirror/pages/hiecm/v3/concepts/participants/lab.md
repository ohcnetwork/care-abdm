# Diagnostics

A diagnostic laboratory or imaging centre publishes records as the [HIP](/docs/hiecm/v3/getting-started/glossary#hip), the same role a hospital takes. The machinery is identical. What changes is the records you hold.

## Who you are in ABDM

You enrol on the [HFR](/docs/hiecm/v3/getting-started/glossary#hfr), which lists diagnostic laboratories and imaging centres alongside hospitals, clinics and pharmacies. A verified facility is issued a facility ID, and linking a [bridge](/docs/hiecm/v3/getting-started/glossary#bridge) makes your software resolvable as that facility.

Two things in the facility record are yours. The additional information layer carries yes or no flags for a diagnostic lab and an imaging centre. The detailed information layer asks for diagnostic and imaging services, and an imaging centre or diagnostic laboratory does not have to submit medical infrastructure or bed counts at all.

## What you can do

Everything a hospital does as a HIP, and by the same calls. Group results into a [care context](/docs/hiecm/v3/getting-started/glossary#care-context), link it, answer [discovery](/docs/hiecm/v3/getting-started/glossary#discovery), validate the consent, then encrypt and push. Nothing in [ABDM](/docs/hiecm/v3/getting-started/glossary#abdm) gives diagnostics a separate API surface.

The difference is the record type. Radiology and laboratory reports are the Diagnostic Report Record, code `DiagnosticReport`. Billing is the Invoice Record. All eight record types are mandatory for an [HMIS](/docs/hiecm/v3/getting-started/glossary#hmis), and which of them a diagnostics only system must implement is not documented here.

Large images are the one place your build differs in practice. Split a CT or MRI study into parts and stream it, inside the same 20 minute window.

If you also read a patient's earlier results, that is the [HIU](/docs/hiecm/v3/getting-started/glossary#hiu) direction and a separate integration.

## Why it is worth it

The registry gives your centre a trusted identity, a listing in national search results, less paperwork on licence renewals and insurance empanelment, and access to ABDM's digital services.

A report you link reaches the patient's own app. The doctor who ordered it can ask for it under consent rather than waiting for a printout to travel.

## Next

[Hospital, lab and pharmacy systems](/docs/hiecm/v3/concepts/hip-hiu) is the build guide, and [FHIR](/docs/hiecm/v3/concepts/fhir) has the record formats.
