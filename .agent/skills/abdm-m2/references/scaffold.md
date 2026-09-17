# HIE-CM M2 build

Scaffolds an ABDM M2 integration one flow at a time. M2 covers care contexts, HIP initiated linking, discovery, and pushing encrypted records to a requester.

## How this skill runs

Every flow below is an OODA loop, not a recipe: observe the actual state (last response, last error), orient against the flow step matched below, decide the cheapest next action, act, and return to observe. A flow step is done only when its exit condition is observed against the sandbox, never because it "should have worked."

Loop limit: 8 passes per flow step. Hitting the limit is an escalation: state what was observed, what was tried, and which atom to read, then ask one question.

## Rules to hold before you call anything

#### Proving a callback really came from ABDM (`hiecm.concept.callback-authenticity`)

To receive callbacks you register a URL that ABDM can reach. Reachable by
ABDM means reachable by everyone, because it is an ordinary address on the
public internet. Nothing about receiving a POST at that URL tells you the
POST came from ABDM.

This matters more here than in most integrations. The callbacks you host
carry instructions about a named person's health records: a request to
discover what you hold, a consent artefact saying somebody agreed, an
instruction to transfer records to a given address. A system that acts on
whatever arrives will act on whatever an attacker sends.

ABDM signs the callbacks it sends. The gateway publishes its public keys as
a JSON Web Key Set, usually shortened to JWKS. You fetch those keys, and you
use them to check the signature on every callback before your handler does
any work.

This is separate from the signature you may already have met inside a
consent artefact (hiecm.concept.consent-artefact). That one signs the artefact's
contents, so it travels with the artefact and proves the artefact was not
altered. The one on this page signs the delivery, and proves who sent it.
Verifying one does not verify the other.

Fetch the key set from the gateway. The response is a standard JWKS, so any
JWT library in your language can consume it directly.

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/certs \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>'
```

Each key in the set carries a `kid` that identifies it, `kty: RSA`, `use:
sig`, and an `alg` the specification gives as `RS256`. The `n` and `e`
fields are the RSA modulus and exponent, Base64URL encoded. Some keys also
carry `x5c`, a certificate chain.

The same key set is discoverable through the OIDC document at
`/api/hiecm/gateway/v3/.well-known/openid-configuration`, which names it in
`jwks_uri`. Reading the discovery document first is the more durable choice,
because it survives the key set moving.

Cache the keys rather than fetching them per callback, and key your cache by
`kid`. When a callback presents a `kid` you have not seen, refetch once
before rejecting it, because that is what key rotation looks like from your
side.

Verification is then the ordinary JWT check your library already does:
signature against the key named by `kid`, algorithm pinned to `RS256`, and
the expiry and issuer claims if the token carries them.

```observation schema=exit-condition
channel: response
path: /api/hiecm/gateway/v3/certs
match:
  status: 200
  body_contains: keys
timeout_seconds: 30
```

#### What this catalogue cannot yet tell you

The gateway specification says the key set exists and says what it is for.
It does not say which header carries the signed token on an inbound
callback, and none of the webhook definitions in the M2 or M3 specifications
declare a header or a security scheme at all. So the transport is documented
and the field that carries it is not.

Two things follow. Confirm the header name against the sandbox before you
write the lookup, by logging the full header set of the first real callback
you receive. And treat this page as unverified until somebody has done that,
which is what its status says.

Pin the algorithm to `RS256` when you verify, and reject `none`. A verifier
that accepts whatever algorithm the token names accepts a token an attacker
signed, and that is a defect in the verifier rather than in ABDM.

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
