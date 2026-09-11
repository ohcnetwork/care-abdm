# HIE-CM P3 build

Scaffolds an ABDM P3 integration one flow at a time. P3 covers subscriptions, auto approval policies, and fetching the records a granted consent covers.

## How this skill runs

Every flow below is an OODA loop, not a recipe: observe the actual state (last response, last error), orient against the flow step matched below, decide the cheapest next action, act, and return to observe. A flow step is done only when its exit condition is observed against the sandbox, never because it "should have worked."

Loop limit: 8 passes per flow step. Hitting the limit is an escalation: state what was observed, what was tried, and which atom to read, then ask one question.

## Flows

### Fetch and store the records a linked care context points at (`hiecm.flow.p3-fetch-records`)

**Before you start**

Four things must already be true, each checkable:

- The care context is linked to the person's health address. See
  find records held elsewhere and link them.
- Your application implements the consent and data flow calls. This is
  work it does as well as linking, not instead of it.
- You have a subscription, so you are told when a care context appears or
  changes. See
  subscribe and set an auto approval policy.
- You can store records for the long term. Fetching without storing means
  fetching again, and the person loses their history when the request
  window closes.

**Act: the calls in this flow, in order**

#### Fetch a consent artefact in full (`hiecm.endpoint.p3-consent-fetch`)

```bash
curl -X POST 'https://dev.abdm.gov.in/api/hiecm/consent/v3/fetch' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{ "consentId": "d6a83f24-6c96-421e-b8b8-844e5344ef69" }'
```

#### Get all consent Request for an ABHA Address (`hiecm.endpoint.p3-get-all-consent-request-for-an-abha-address`)

```bash
curl -X GET 'https://dev.abdm.gov.in/api/hiecm/consent/v3/request?limit=10&offset=0&status=ALL' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '<REQUEST_BODY>'
```

#### Get consent-artefact-details-by-artifact-id (`hiecm.endpoint.p3-get-consent-artefact-details-by-artifact-id`)

```bash
curl -X GET 'https://dev.abdm.gov.in/api/hiecm/consent/v3/artefact/{{consentId}}' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '<REQUEST_BODY>'
```

#### Deny - Consent Request (`hiecm.endpoint.p3-deny-consent-request`)

```bash
curl -X POST 'https://dev.abdm.gov.in/api/hiecm/consent/v3/request/{{consentRequestId}}/deny' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{ "reason": "Not authorized" }'
```

#### Revoke - Consent Request (`hiecm.endpoint.p3-revoke-consent-request`)

```bash
curl -X POST 'https://dev.abdm.gov.in/api/hiecm/consent/v3/revoke' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{ "consents": [ "*{{consentId}}*" ] }'
```

#### Request status (`hiecm.endpoint.p3-request-status`)

```bash
curl -X GET 'https://dev.abdm.gov.in/api/hiecm/data-flow/v3/health-information/request/status/{{transactionId}}' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '<REQUEST_BODY>'
```

**Exit condition (Observe until this is true)**

The records arrive for the care context the notification named, your
application has stored them, and they are displayed in date order. Asking
again is not needed, which is what proves they were stored rather than
held for the length of a screen.

A grant on its own is not the exit condition. A granted consent with no
health information request behind it leaves the person with permission
and no records.

**If it goes wrong**

The failures, in rough order of frequency:

- ABDM-1112 (hiecm.error.abdm-1112) when the artefact is expired or has
  been revoked. Revocation is the person exercising a right, so it is a
  state to handle rather than an error to report.
- Records fetched but not stored, which reads as working until the
  consent window closes and the history disappears.
- A health information type the application cannot display, from the
  seven the test cases cover.

### Subscribe to a user's account and set an auto approval policy (`hiecm.flow.p3-subscribe-and-auto-approve`)

**Before you start**

Three things must already be true, each checkable:

- The person is signed in and holds an
  ABHA address (shared.glossary.abha-address). See
  sign a user in.
- You can receive and surface device notifications, because that is what
  a subscription produces.
- You have screens to list subscriptions, approve them, deny them and
  edit them. Editing covers health information types, types of visit and
  the time period.

**Act: the calls in this flow, in order**

#### Request a subscription to a person's account (`hiecm.endpoint.p3-subscription-init`)

```bash
curl -X POST 'https://dev.abdm.gov.in/api/hiecm/subscription-requests/v3/init' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{
  "subscription": {
    "purpose": {
      "text": "Care Management",
      "code": "CAREMGT",
      "refUri": "www.abdm.gov.in"
    },
    "patient": {
      "id": "xxxxx@sbx"
    },
    "hiu": {
      "id": "{ Health locker/PHR ID}"
    },
    "hips": [
      {
        "id": "HIP_ID",
        "name": "HIP_NAME",
        "type": "HIP"
      }
    ],
    "categories": [
      "LINK",
      "DATA"
    ],
    "period": {
      "from": "2024-06-01T09:00:00.000Z",
      "to": "2124-12-31T09:00:00.000Z"
    }
  }
}'
```

#### Set an auto approval policy (`hiecm.endpoint.p3-consent-auto-approve`)

```bash
curl -X POST 'https://dev.abdm.gov.in/api/hiecm/consent/v3/auto/approve' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{ "isApplicableForAllHIPs": **true**, "hiu": { "id": "*{{hiu-id}}*" }, "includedSources": [ { "hiTypes": [ "Prescription", "DiagnosticReport", "OPConsultation", "DischargeSummary", "ImmunizationRecord", "HealthDocumentRecord", "WellnessRecord", "Invoice" ], "purpose": { "text": "Care Management", "code": "CAREMGT", "refUri": "www.abdm.gov.in" }, "period": { "from": "2024-11-27T16:21:00.000Z", "to": "2024-12-30T00:00:00.000Z" } } ], "excludedSources": [] }'
```

#### Approve Subscription Request (`hiecm.endpoint.p3-approve-subscription-request`)

```bash
curl -X POST 'https://dev.abdm.gov.in/api/hiecm/subscription-' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '{ "isApplicableForAllHIPs": **false**, "includedSources": [ { "hiTypes": [ "Prescription", "DiagnosticReport", "OPConsultation", "DischargeSummary", "ImmunizationRecord", "HealthDocumentRecord", "WellnessRecord" , "Invoice" ], "purpose": { "text": "Care Management", "code": "CAREMGT", "refUri": "www.abc.com7" }, "hip": { "id": "HIP\_ID", "name": "HIP\_NAME " }, "categories": [ "DATA", "LINK" ], "period": { "from": "2023-04-27T04:03:40.079Z", "to": "2023-04-27T04:03:40.079Z" } } ] } "LINK", "DATA" ], "period": { "from": "2023-04-04T09:52:39.235Z", "to": "2023-04-20T09:52:39.235Z" } } ], "excludedSources": [ { "hiTypes": [ "PRESCRIPTION" ], "purpose": { "text": "Self Requested", "code": "PATRQT", "refUri": "www.test.com" },'
```

#### Consent Enable Auto Approve (`hiecm.endpoint.p3-consent-enable-auto-approve`)

```bash
curl -X POST 'https://dev.abdm.gov.in//api/hiecm/consent/v3/auto/approve/{{consentId}}/enable' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '<REQUEST_BODY>'
```

#### Consent Disable Auto Approve (`hiecm.endpoint.p3-consent-disable-auto-approve`)

```bash
curl -X POST 'https://dev.abdm.gov.in/api/hiecm/consent/v3/auto/approve/{{consentId}}/disable' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '<REQUEST_BODY>'
```

#### Get all subscription requests for an ABHA Address (`hiecm.endpoint.p3-get-all-subscription-requests-for-an-abha-address`)

```bash
curl -X GET 'https://dev.abdm.gov.in/api/hiecm/subscription-requests/v3/requests' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'Content-Type: application/json' \
  -d '<REQUEST_BODY>'
```

**Exit condition (Observe until this is true)**

The subscription is listed as approved on your own subscriptions screen,
and a change to the person's account produces a notification your
application receives.

For the policy, the HIE-CM returned an auto approval id and you stored
it. The observable proof is the next new care context: a consent request
raised against it is granted without the person being asked.

**If it goes wrong**

The failures these sources document, in rough order of frequency:

- A policy with no stored auto approval id, which leaves the person
  unable to turn it off. The person must be able to disable a policy at
  any time.
- A subscription created before the person was asked, which is a consent
  failure rather than a technical one.
- Notifications received but not surfaced, so the application knows about
  a new record and the person does not.

## Where the detail is

- Every operation in this milestone, with its body fields and responses: /docs/hiecm/v3/api/p3
- The flows as diagrams: /docs/hiecm/v3/milestones/p3
- Every error code across milestones: /docs/hiecm/v3/reference/error-codes
- Terms: /docs/hiecm/v3/getting-started/glossary
