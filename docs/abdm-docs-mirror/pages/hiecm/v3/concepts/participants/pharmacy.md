# Pharmacy

A pharmacy publishes records as the [HIP](/docs/hiecm/v3/getting-started/glossary#hip), the same role a hospital takes. The calls, the linking and the encryption are identical. What changes is the records you hold, and one thing that is not on this gateway at all.

## Who you are in ABDM

You enrol on the [HFR](/docs/hiecm/v3/getting-started/glossary#hfr), which lists pharmacies alongside hospitals, clinics and laboratories. A verified facility is issued a facility ID, and linking a [bridge](/docs/hiecm/v3/getting-started/glossary#bridge) makes your software resolvable as that facility.

Pharmacy appears twice in a facility record: as a facility type, and as a yes or no flag in the additional information layer for a facility that runs a pharmacy inside it. A pharmacy does not have to submit medical infrastructure or bed counts.

Your pharmacists can register on the [HPR](/docs/hiecm/v3/getting-started/glossary#hpr) as well. Pharmacist is one of the three professional categories open today.

## What you can do

Everything a hospital does as a HIP, and by the same calls. Group records into a [care context](/docs/hiecm/v3/getting-started/glossary#care-context), link it, answer [discovery](/docs/hiecm/v3/getting-started/glossary#discovery), validate the consent, then encrypt and push.

Two of the eight record types are the ones closest to your work. The Prescription Record holds medication advice and follows Pharmacy Council of India guidelines. The Invoice Record holds pharmacy invoices and other billing.

warning

Check the swagger before you send `Invoice`

`Invoice` appears in the [M2](/docs/hiecm/v3/api/m2) error message for an invalid health information type, and is missing from the [M3](/docs/hiecm/v3/api/m3) list of supported types. The two sources disagree.

Whether dispensing has a record type of its own is not documented here. Ordering and fulfilment are not on this gateway: they run on [UHI](/docs/hiecm/v3/getting-started/glossary#uhi), which has a separate specification.

## Why it is worth it

The registry gives your pharmacy a trusted identity, a listing in national search results, less paperwork on licence renewals and insurance empanelment, and access to [ABDM](/docs/hiecm/v3/getting-started/glossary#abdm)'s digital services.

A record you link reaches the patient's own app, so their medication history sits with the rest of their records instead of in a paper bag.

## Next

[Hospital, lab and pharmacy systems](/docs/hiecm/v3/concepts/hip-hiu) is the build guide, and [FHIR](/docs/hiecm/v3/concepts/fhir) has the record formats.
