# HIE-CM P3 build

Scaffolds an ABDM P3 integration one flow at a time. P3 covers subscriptions, auto approval policies, and fetching the records a granted consent covers.

## How this skill runs

Every flow below is an OODA loop, not a recipe: observe the actual state (last response, last error), orient against the flow step matched below, decide the cheapest next action, act, and return to observe. A flow step is done only when its exit condition is observed against the sandbox, never because it "should have worked."

Loop limit: 8 passes per flow step. Hitting the limit is an escalation: state what was observed, what was tried, and which atom to read, then ask one question.

## Rules to hold before you call anything

#### The five things a personal health record application must let a person do with consent (`hiecm.concept.consent-in-a-phr-app`)

Consent in ABDM is granted by a person, not by a system, and the
personal health record application (shared.glossary.phr) is where they do it.
Everything else in the network assumes that screen exists and works.

NHA sets a floor of five capabilities. An application missing one of them
leaves a person able to give access they cannot inspect, change or withdraw.

#### 1. See the request

Every request the person has received, showing the
health information user (shared.glossary.hiu) asking, the purpose, the record
types wanted, the date range of records, how long the consent would last, and
its current status.

#### 2. Change it before allowing it

Where the request permits it, the person adjusts it rather than facing all or
nothing. Four things are adjustable: how long access lasts, the date range of
records covered, which categories of record are shared, and the validity
period of the consent itself.

This is the capability most often left out, and it is the one that turns a
consent screen into a negotiation rather than a demand.

#### 3. Allow or refuse

The decision goes back to the consent manager. NHA's own flow names three
outcomes, not two: approve, reject, and ignore. Ignoring is a real outcome
with a real effect, because a request the person never touches expires on the
window the requester set, and your interface has to be able to show that
state.

Approving is `POST /api/consent-management/consent-requests/{consentRequestId}/approve`,
and its reference page carries the headers and the body. Denying and revoking
have a written page each as well, which approving does not yet, so read the
reference for that one rather than looking for prose that is not there.

#### 4. See what is already allowed

Every consent currently granted, its details and status, so the person can see
which organisations hold access to their records right now. A list of past
decisions is not the same thing as a list of live ones.

#### 5. Take it back

The person withdraws a granted consent at any time. Two things follow, and
both matter: the status is updated at the consent manager, and sharing under
that consent stops immediately. Not at the end of the period, not at the next
request.

#### Subscriptions, and why a personal health record application needs one (`hiecm.concept.phr-subscriptions`)

A care context (hiecm.concept.care-context) can be linked to a person's
address at any time, by any facility they visit, without your application
being part of it. A subscription is how you find out. It is a standing watch
on one address: once it exists, the consent manager posts to your callback
whenever something changes for that person.

Either a health information user (shared.glossary.hiu) or a
personal health record application (shared.glossary.phr) may hold one.
Without it, the only way to notice a new record is to ask repeatedly, and
nothing in ABDM is built for that.

NHA expects every personal health record application to set one up at two
moments: when it creates an address, and when a person signs in with an
address it has not seen before.

#### The four events it delivers

Once the person approves the subscription, the consent manager notifies you
on:

- a new care context linked to the address,
- a modified care context,
- a new consent request,
- a new subscription request.

Delivery is to your callback. Showing it to the person on their device is
your job, and NHA names a push service, Firebase on Android, as the example
rather than a requirement.

#### The states a request moves through

The interface NHA describes carries two groups, and a request sits in exactly
one state within them. Building a screen per state is the point of listing
them:

| Group | State | What it means |
| --- | --- | --- |
| Requests | Requested | Sent to the person, who has not acted yet |
| Requests | Denied | The person refused it |
| Requests | Expired | The person did not act inside the window the requester set |
| Approved | Granted | The person allowed it |
| Approved | Revoked | The person allowed it and later withdrew that |

The same five states carry consent requests, subscription requests and health
locker requests, so one screen serves all three.

#### What a subscription is not

It is not consent, and it does not give anybody a record. It tells you that a
record exists. Reading it still needs a consent, which is why a subscription
usually runs alongside an auto approval policy: the notification arrives, your
application raises a consent request for the care context it names, the policy
grants it without troubling the person, and only then can the record be
fetched and stored. That sequence is
subscribe and auto approve (hiecm.flow.p3-subscribe-and-auto-approve).

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
