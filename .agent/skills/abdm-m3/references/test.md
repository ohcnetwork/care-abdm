# Test M3, consent and fetching

Each case names the call it makes and what to see when it passes.

## Test cases

32 cases, from NHA's M3 matrix for Consent management and health record fetch. "Mandatory" is NHA's own marking.

### Create Consent Request

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HIU_FLOW_101` | Mandatory | Patient Discovery |  | HIU should check if the ABHA is valid |
| `HIU_FLOW_102` | Mandatory | Consent Request Initiation |  | Consent Request is initiated and sent to the patient PHR app of the patient. |
| `HIU_FLOW_103` | Mandatory | Notification to PHR |  | Consent Request notification should be available on the patient patient PHR app of the patient. Patient will … |
| `HIU_FLOW_104` | Mandatory | Listing of Consent Requests |  | HIU user should be able to view the list of consent requests created |
| `HIU_FLOW_105` | Mandatory | Consent Request is Denied |  | HIU user should not be able to view the health data for the denied consent request |
| `HIU_FLOW_106` | Conditional | Consent Request is Approved |  | The HIU system would fetch health data for the approved consent request. When the request has been edited wit… |
| `HIU_FLOW_107` | Conditional | Fetch health data for (HI Type = DiagnostocReport Structured/Un-Structured) |  | HIU user should be able to view the health data of selected HI type from HIU application. |
| `HIU_FLOW_108` | Conditional | Fetch health data for (HI Type = Prescription-Structured/Un-Structured) |  | HIU user should be able to view the health data of selected HI type from HIU application. |
| `HIU_FLOW_109` | Conditional | Fetch health data for (HI Type = DischargeSummary-Structured/Un-Structured) |  | HIU user should be able to view the health data of selected HI type from HIU application. |
| `HIU_FLOW_110` | Conditional | Fetch health data for (HI Type = CosultingNote-Structured/Un-Structured) |  | HIU user should be able to view the health data of selected HI type from HIU application. |
| `HIU_FLOW_111` | Conditional | Fetch health data for (HI Type = Immunization record-Structured/Un-Structured) |  | HIU user should be able to view the health data of selected HI type from HIU application. |
| `HIU_FLOW_112` | Conditional | Fetch health data for (HI Type = Health Record-Structured/Un-Structured) |  | HIU user should be able to view the health data of selected HI type from HIU application. |
| `HIU_FLOW_113` | Conditional | Fetch health data for (HI Type = Wellness Record-Structured/Un-Structured) |  | HIU user should be able to view the health data of selected HI type from HIU application. |

### Revoke Consent Request

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HIU_FLOW_201` | Mandatory | Revoke Consent |  | The patient patient PHR app user should have an option to revoke consent |
| `HIU_FLOW_202` | Mandatory | Revoke Consent |  | The health record should not be available to the HIU application after consent is revoked. Consent request li… |

### Expiry of Consent Request

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `HIU_FLOW_301` | Unmarked | Consent Expiry |  | HIUs should not be able to view health records after expiry of consent. Consent request list should be update… |

### Further checks this portal suggests

| Case | Type | What it proves | Call | Passes when |
| --- | --- | --- | --- | --- |
| `CNS_01` | Portal check | Raise a consent request for a patient's previous records | `null /api/hiecm/consent/v3/request/init` | You receive an on-init callback carrying a consent request id. |
| `CNS_02` | Portal check | Poll the request status before the patient acts | `null /api/hiecm/consent/v3/request/status` | Status comes back `Requested`. |
| `CNS_03` | Portal check | Handle a consent request that produces no on-init callback at all | `null /api/hiecm/consent/v3/request/init` | The on-init callback arrives at your registered URL. Nothing arriving means the URL is not registered or not … |
| `CNS_04` | Portal check | Send one consent request per purpose of use code you will use in production | `null /api/hiecm/consent/v3/request/init` | Each code is accepted and reaches the patient's PHR app. |
| `CNS_05` | Portal check | Send one consent request per HI type you will display | `null /api/hiecm/consent/v3/request/init` | Each type is accepted, and your system renders what comes back for it. |
| `GRT_01` | Portal check | Receive a grant and acknowledge the consent artefact ids | `null /api/hiecm/consent/v3/request/hiu/on-notify` | You receive a notify callback with one or more consent artefact ids and the request id. |
| `GRT_02` | Portal check | Handle a denial on a second request | webhook `/api/v3/hiu/consent/request/notify` | You receive a notify callback with status `Denied` and no artefact ids. |
| `GRT_03` | Portal check | Handle a grant that produces more than one artefact | `null /api/hiecm/consent/v3/fetch` | Every artefact id in the notify callback is fetched and used, not only the first. |
| `ART_01` | Portal check | Fetch a consent artefact by id | `null /api/hiecm/consent/v3/fetch` | You receive an on-fetch callback for the artefact id you quoted. |
| `ART_02` | Portal check | Stop fetching once the consent has expired | `null /api/hiecm/consent/v3/fetch` | The fetch fails and your code stops, rather than retrying forever. |
| `DAT_01` | Portal check | Request the health information under a granted consent | `null /api/hiecm/data-flow/v3/health-information/request` | You receive an on-request callback with a transaction id, request id and status. |
| `DAT_02` | Portal check | Receive the encrypted records |  | Encrypted records arrive at the data push callback URL you supplied. |
| `DAT_03` | Portal check | Decrypt the records and render them |  | The records read as FHIR content your system can display, as plain text or structured output. |
| `DAT_04` | Portal check | Render a partial result when only some requested HI types exist | `null /api/hiecm/data-flow/v3/health-information/request` | The types that exist render. Your system does not treat the missing ones as a failure. |
| `DAT_05` | Portal check | Notify receipt and close the transaction | `null /api/hiecm/data-flow/v3/health-information/notify` | You call health information notify and the transaction closes. |
| `REV_01` | Portal check | Stop fetching once the patient revokes consent | `null /api/hiecm/consent/v3/fetch` | The fetch fails and your system stops. Access ends from the point of revocation. |
