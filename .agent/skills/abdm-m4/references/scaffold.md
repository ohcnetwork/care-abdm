# HIE-CM M4 build

Scaffolds an ABDM M4 integration one flow at a time. M4 covers creating an HPID, registering a professional on the HPR, onboarding a facility to the HFR, and linking that facility to its bridges.

## How this skill runs

Every flow below is an OODA loop, not a recipe: observe the actual state (last response, last error), orient against the flow step matched below, decide the cheapest next action, act, and return to observe. A flow step is done only when its exit condition is observed against the sandbox, never because it "should have worked."

Loop limit: 8 passes per flow step. Hitting the limit is an escalation: state what was observed, what was tried, and which atom to read, then ask one question.

## Flows

### Get a healthcare professional an HPID (`hiecm.flow.m4-create-hpid`)

**Before you start**

Four things must already be true, each checkable:

- You hold a gateway session token. See
  the gateway session (hiecm.concept.gateway-session). Every call in
  this flow carries it in `Authorization`.
- You can redirect the professional to a URL and bring them back. The
  Aadhaar step happens in a browser, not in your API client.
- You can encrypt a value with the NHPR certificate, fetched from
  `/v4/int/api/v1/auth/cert`. The mobile number, the email address and
  the password all travel encrypted. The padding here is
  `RSA/ECB/PKCS1Padding`, which belongs to this registry: M1 uses
  RSA-OAEP with SHA-1 under a different certificate, so an M1 code path
  reused here encrypts with the wrong scheme and the wrong key. See
  encrypting an identifier (hiecm.concept.input-encryption).
- You know which category and subcategory the professional falls in, as
  codes rather than names. Fetch them from the HPR master data calls
  rather than hard coding them: the subcategory codes create HPID uses
  are not the same as the ones register professional uses.

**Act: the calls in this flow, in order**

#### Send the Aadhaar OTP that starts an HPID (`hiecm.endpoint.m4-hpr-generate-aadhaar-otp`)

```bash
curl -X POST 'https://hpridsbx.abdm.gov.in/api/v1/registration/aadhaar/generateOtp' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '<REQUEST_BODY>'
```

#### Check whether the mobile number is the one on the Aadhaar record (`hiecm.endpoint.m4-hpr-demographic-auth-mobile`)

```bash
curl -X POST 'https://hpridsbx.abdm.gov.in/api/v1/registration/aadhaar/demographicAuthViaMobile' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '<REQUEST_BODY>'
```

#### Create the HPID (`hiecm.endpoint.m4-hpr-create-hprid`)

```bash
curl -X POST 'https://hpridsbx.abdm.gov.in/api/v1/registration/aadhaar/createHprIdWithPreVerified' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '<REQUEST_BODY>'
```

**Exit condition (Observe until this is true)**

The create HPID response carries an HPID of 14 digits and a non empty
`hprToken`. Calling check HPID exists by Aadhaar again, for the same
Aadhaar, then returns that same HPID rather than none.

Neither of those means the professional has a profile. The HPID is an
identity, not a registration. See
register the professional.

**If it goes wrong**

The failures the M4 sources document, each with its fix in the linked
error atom:

- HIS-3021 (hiecm.error.his-3021) when an HPID already exists for this
  Aadhaar. Step 4 is what stops you reaching this.
- HIS-2045 (hiecm.error.his-2045) when the session behind the `txnId`
  has expired, which the five minute URL window makes easy to hit.
- A bare boolean where your client expected an object, from the optional
  status poll. That is the documented shape, not a fault.

### Link a facility to its bridge (`hiecm.flow.m4-link-bridge`)

**Before you start**

Three things must already be true, each checkable:

- The facility is onboarded and holds a facility ID in the form `IN`
  followed by 10 characters. See
  onboard a facility. A facility still in draft
  has no id to link.
- You hold the bridge id for the software that will act for the facility.
- You have chosen the name patients will see. Three rules bind it: 15
  characters or fewer, no special characters, and unique for every bridge
  on that facility.

**Act: the calls in this flow, in order**

The Catalogue does not yet record this flow's calls as endpoint atoms, so this skill cannot give you the exact requests. Read the operations under /docs/hiecm/v3/api/m4 before acting, and treat the exit condition below as the thing to observe.

**Exit condition (Observe until this is true)**

The link is present and `active` is true for the facility and bridge you
sent. The proof that it works, rather than merely exists, is the flow it
unblocks: a facility with an active HIP link can complete
linking a care context, and one with an active
HIU link can raise a consent request.

**If it goes wrong**

The failures you will see, each with its fix in the linked error atom:

- HIS-1124 (hiecm.error.his-1124) when a call needs a bridge that is
  not linked to this facility.
- HIS-1128 (hiecm.error.his-1128) when the HIP name is already in use,
  which the uniqueness rule makes common on a facility's second bridge.
- A name longer than 15 characters or carrying a special character,
  rejected as validation rather than as a naming rule.

### Onboard a facility to the HFR (`hiecm.flow.m4-onboard-facility`)

**Before you start**

Four things must already be true, each checkable:

- Someone at the facility holds an HPR account. Onboarding needs an HPR
  token in the header of the create calls, generated from an HPR id and
  password, so it usually starts with a person getting an
  HPID.
- You hold a gateway session token. See
  the gateway session (hiecm.concept.gateway-session).
- You hold the LGD codes for the facility's state, district, sub district
  and village. They come from the Local Government Directory and from the
  LGD lookup calls.
- You hold the facility's board photograph and building photograph, each
  under 5 MB, base64 encoded, with the file extension in the name
  matching the file.

**Act: the calls in this flow, in order**

#### Search the facility registry before creating anything (`hiecm.endpoint.m4-hfr-search-facility`)

```bash
curl -X POST 'https://facilitysbx.abdm.gov.in/FacilityManagement/v1.5/facility/search' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '<REQUEST_BODY>'
```

**Exit condition (Observe until this is true)**

The basic information call returns a `trackingId`, and the submit call
accepts that same `trackingId` and reports the facility submitted for
verification. Searching for the facility afterwards returns it rather
than nothing.

A facility that was written but never submitted stays in draft. A draft
is invisible to ABDM, so an integration that stopped after step 4 has not
onboarded anything, whatever the three write calls returned.

**If it goes wrong**

The failures the M4 sources document, each with its fix in the linked
error atom:

- HIS-1132 (hiecm.error.his-1132) when the registry detects a duplicate
  facility. Step 1 is what stops you reaching this.
- HIS-4003 (hiecm.error.his-4003) when the facility already exists
  under the identifiers you sent.
- A conditional field rejected on detailed information, because the rule
  that makes it mandatory depends on the facility type and the system of
  medicine rather than on the field itself.

### Register a professional's profile on the HPR (`hiecm.flow.m4-register-professional`)

**Before you start**

Four things must already be true, each checkable:

- The professional holds an HPID. See
  get an HPID.
- You hold the `hprToken` that create HPID returned. This call carries it
  in the payload, not only in a header.
- You hold a gateway session token. See
  the gateway session (hiecm.concept.gateway-session).
- You have fetched the code lists this call needs. Council, course,
  college, university, state, district and language all go in as codes.
  The call takes codes, not names, and the subcategory codes here are
  not the ones create HPID used.

**Act: the calls in this flow, in order**

#### Register the professional's profile (`hiecm.endpoint.m4-hpr-register-professional`)

```bash
curl -X POST 'https://doctorsbx.abdm.gov.in/apis/v1/doctors/register-professional-new' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '<REQUEST_BODY>'
```

#### Read a professional's profile (`hiecm.endpoint.m4-hpr-fetch-professional-info`)

```bash
curl -X POST 'https://doctorsbx.abdm.gov.in/apis/v1/doctors/fetch-professional-info' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '<REQUEST_BODY>'
```

#### List the documents this professional must upload (`hiecm.endpoint.m4-hpr-fetch-documents-list`)

```bash
curl -X POST 'https://doctorsbx.abdm.gov.in/apis/v1/doctors/fetch-documents-list' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '<REQUEST_BODY>'
```

#### Upload one of the professional's documents (`hiecm.endpoint.m4-hpr-upload-document`)

```bash
curl -X POST 'https://doctorsbx.abdm.gov.in/apis/v1/uploads/upload-document' \
  -H 'Authorization: Bearer <ACCESS_TOKEN>' \
  -H 'Content-Type: application/json' \
  -d '<REQUEST_BODY>'
```

**Exit condition (Observe until this is true)**

The register professional call returns a success result for the HPID you
sent, and the document list call then returns the ids that professional
must upload against. After the uploads, retrieving the professional's
profile shows the qualification and council registration you sent rather
than an empty profile.

A registration with its mandatory documents missing is not finished, even
where the registration call itself was accepted.

**If it goes wrong**

The failures the M4 sources document, each with its fix in the linked
error atom:

- HIS-5005 (hiecm.error.his-5005) when this professional is already
  registered, which is a state to read rather than an error to retry.
- HIS-5011 (hiecm.error.his-5011) when the `hprToken` has expired
  between creating the HPID and registering the profile.
- A code that is not on the current master list, which reads as a
  validation failure on a field you believed was correct. Refetch the
  list rather than trusting a value you cached.

## Where the detail is

- Every operation in this milestone, with its body fields and responses: /docs/hiecm/v3/api/m4
- The flows as diagrams: /docs/hiecm/v3/milestones/m4
- Every error code across milestones: /docs/hiecm/v3/reference/error-codes
- Terms: /docs/hiecm/v3/getting-started/glossary
