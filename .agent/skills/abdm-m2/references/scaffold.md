# HIE-CM M2 build

Scaffolds an ABDM M2 integration one flow at a time. M2 covers care contexts, HIP initiated linking, discovery, and pushing encrypted records to a requester.

## How this skill runs

Every flow below is an OODA loop, not a recipe: observe the actual state (last response, last error), orient against the flow step matched below, decide the cheapest next action, act, and return to observe. A flow step is done only when its exit condition is observed against the sandbox, never because it "should have worked."

Loop limit: 8 passes per flow step. Hitting the limit is an escalation: state what was observed, what was tried, and which atom to read, then ask one question.

## Flows

### Link a care context to a patient's ABHA (`hiecm.flow.m2-link-care-context`)

**Before you start**

Three things must already be true, each checkable:

- Your facility holds a facility ID from the
  HFR (shared.glossary.hfr) and a bridge linked with type `HIP`. See
  link a facility to its bridge.
- You hold a gateway session token from the sessions endpoint
  (gateway_sessions_create in the gateway reference).
- The patient has an ABHA address, which is the M1 module's job.

**Act: the calls in this flow, in order**

#### Generate Link Token (`hiecm.endpoint.m2-generate-link-token`)

```bash
curl -X POST 'https://dev.abdm.gov.in/api/hiecm/v3/token/generate-token' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'X-CM-ID: sbx' \
  -H 'Content-Type: application/json' \
  -d '{
    "abhaNumber": <PATIENT_ABHA_NUMBER_14_DIGITS>,
    "abhaAddress": "<PATIENT_ABHA_ADDRESS>",
    "name": "<PATIENT_NAME_AS_HELD>",
    "gender": "<M_F_OR_O>",
    "yearOfBirth": <PATIENT_YEAR_OF_BIRTH>
  }'
```

#### Link care contexts to an ABHA address (`hiecm.endpoint.m2-hip-link-care-context`)

```bash
curl -X POST 'https://dev.abdm.gov.in/api/hiecm/hip/v3/link/carecontext' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'X-CM-ID: sbx' \
  -H 'Content-Type: application/json' \
  -d '{
    "abhaNumber": "<PATIENT_ABHA_NUMBER_14_DIGITS>",
    "abhaAddress": "<PATIENT_ABHA_ADDRESS>",
    "patient": [
      {
        "referenceNumber": "<YOUR_PATIENT_REFERENCE>",
        "display": "<PATIENT_NAME_AS_HELD>",
        "careContexts": [
          {
            "referenceNumber": "<YOUR_VISIT_REFERENCE>",
            "display": "<WHAT_THE_PATIENT_WILL_SEE>"
          }
        ],
        "hiType": ["<HI_TYPE>"],
        "count": 1
      }
    ]
  }'
```

#### Link Care Context Notify (`hiecm.endpoint.m2-link-care-context-notify`)

```bash
curl -X POST 'https://dev.abdm.gov.in/api/hiecm/hip/v3/link/context/notify' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'REQUEST-ID: <FRESH_UUID>' \
  -H 'TIMESTAMP: <ISO_8601_TIMESTAMP>' \
  -H 'X-CM-ID: sbx' \
  -H 'Content-Type: application/json' \
  -d '{
    "notification": {
      "patient": {"id": "<PATIENT_ABHA_ADDRESS>"},
      "careContext": {
        "patientReference": "<PATIENT_ABHA_ADDRESS>",
        "careContextReference": "<YOUR_VISIT_REFERENCE>"
      },
      "hiTypes": ["<HI_TYPE>"],
      "date": "<ISO_8601_TIMESTAMP>",
      "hip": {
        "id": "<YOUR_HIP_ID>",
        "name": "<YOUR_FACILITY_NAME>",
        "type": "HIP"
      }
    }
  }'
```

**Exit condition (Observe until this is true)**

Your bridge receives a POST at `/v3/link/on_carecontext` whose
`response.requestId` matches the `REQUEST-ID` you sent on the link call,
carrying a success `status` rather than an `error`. The care context then
appears when the patient's PHR app runs discovery against your facility.

Do not treat the synchronous acknowledgement on the link call as success.
It says the request was accepted, not that anything was linked.

```observation schema=exit-condition
channel: callback
path: <YOUR_BRIDGE_URL>/v3/link/on_carecontext
match:
  response.requestId: <THE_REQUEST_ID_YOU_SENT>
  status: SUCCESS
timeout_seconds: unknown
note: >
  The timeout is not published. Wait on the callback rather than on a
  deadline of your own.
```

**If it goes wrong**

The frequent failures, in rough order of frequency, each with its fix in
the linked error atom:

- hiecm.error.abdm-1056 when the care context is already linked or the
  link reference number is invalid.
- hiecm.error.abdm-1062 when the ABHA number does not match the link
  token.
- hiecm.error.abdm-1063 when the HIP id does not match the link token.
- hiecm.error.abdm-2406 when calls are made out of the logical sequence.

## Where the detail is

- Every operation in this milestone, with its body fields and responses: /docs/hiecm/v3/api/m2
- The flows as diagrams: /docs/hiecm/v3/milestones/m2
- Every error code across milestones: /docs/hiecm/v3/reference/error-codes
- Terms: /docs/hiecm/v3/getting-started/glossary
