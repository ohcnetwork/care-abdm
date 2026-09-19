# HPR, the professional registry

[HPR](/docs/hiecm/v3/getting-started/glossary#hpr) is the Healthcare Professionals Registry, the people half of [NHPR](/docs/hiecm/v3/registries/nhpr) alongside the [HFR](/docs/hiecm/v3/registries/nhpr/hfr). Registering there issues the professional an [HPID](/docs/hiecm/v3/getting-started/glossary#hpid), their identity everywhere in [ABDM](/docs/hiecm/v3/getting-started/glossary#abdm).

## Who can enrol

Three categories today, with more to be added later: doctor, nurse and pharmacist. Each professional also declares a system of medicine, from modern medicine, dentistry, Ayurveda, Unani, Siddha, Homoeopathy, Sowa-Rigpa, and yoga and naturopathy. A person can also enrol as a facility manager instead of a clinician, set by the role code:

| Role code | What the person is                           |
| --------- | -------------------------------------------- |
| 1         | Healthcare Professional                      |
| 2         | Facility Manager                             |
| 3         | Healthcare Professional and Facility Manager |

If nobody in your organisation holds role 2 or role 3, you cannot register a facility. See [HFR](/docs/hiecm/v3/registries/nhpr/hfr).

## The HPID

A unique 14 digit, Aadhaar authenticated identifier issued on successful registration to a healthcare professional or facility manager. It is written both ways, HPID and HPR ID. Like an [ABHA](/docs/hiecm/v3/registries/abha), it comes in two forms:

| Form        | Sample              | Where it is used                                  |
| ----------- | ------------------- | ------------------------------------------------- |
| The number  | `71-2665-5777-XXXX` | Sent as `hpid` or `hprIdNumber`                   |
| The address | `name@hpr.abdm`     | Sent as `hprId`, with `domainName` of `@hpr.abdm` |

The professional chooses the readable part through a username suggestion call, the same pattern as the ABHA address suggestion in [M1](/docs/hiecm/v3/api/m1).

## What identifies a doctor

An HPID on its own is an authenticated person; the profile behind it makes them a doctor. The register professional call groups it in five blocks:

| Block                 | What it holds                                                                                                                                                                     |
| --------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Personal information  | Salutation and name, date of birth, gender, nationality, languages spoken, profile photo, official mobile and email                                                               |
| Communication address | Country, state, district, sub district, city and pincode, all as master data codes. Skipped if the address matches the [KYC](/docs/hiecm/v3/getting-started/glossary#kyc) address |
| Registration          | The council the professional is registered with, the registration number, the registration certificate, and whether the registration is permanent or renewable                    |
| Qualification         | Degree or diploma obtained, college, university, year of award, and the degree certificate                                                                                        |
| Current work          | Whether they are working, the purpose of that work, whether it is private, government or both, and the facility they work at                                                      |

Three codes decide what the professional may be. **Category** says doctor, nurse or pharmacist. **Subcategory** fixes the system of medicine. The **degree code** must agree with both. The operations that take them, and their fields, are in [the M4 API reference](/docs/hiecm/v3/api/m4).

The subcategory codes differ between two calls

Subcategory codes differ between the create HPID and register professional tables. Fetch the codes from the HPRID subcategories master call rather than hard coding either table.

The SMD ID identifies doctors only. Searching for nurse colleges by SMD returns a null college and university name, and this is expected: for nurses, SMD is always null.

## The registration journey

Two halves, in order. Nothing in the second works until the first produces a token.

**Half one, create the HPID.** Nine calls follow the management token, in this order:

1. Generate Aadhaar link
2. Check Aadhaar authentication status
3. Verify OTP and fetch user details
4. Check whether an HPID already exists for this Aadhaar
5. Mobile match
6. Generate mobile OTP
7. Verify mobile OTP
8. Username suggestions
9. Create HPID

The last returns the HPID and a `token`, which the next call takes as `hprToken`.

**Half two, register the professional.** Register professional writes the full profile, at `POST https://apihspsbx.abdm.gov.in/v4/int/apis/v1/doctors/register-professional-new`. Then retrieve professional document list, upload documents, update professional and fetch professional details.

Three things to know first:

- The Aadhaar link URL is valid for 5 minutes only. Call the API again once it expires.
- `degreeCertificate` and `registrationCertificate` are mandatory uploads, and `proofOfWorkCertificate` is mandatory when the professional is government or both.
- Call `demographicAuthViaMobile` first, and generate the mobile OTP only when it returns false.

Call by call, with the parameters, is on [M4 user journey](/docs/hiecm/v3/milestones/m4) and [the M4 API reference](/docs/hiecm/v3/api/m4).

## Getting an HPR token later

The `hprToken` from creation does not last. Three ways to get a fresh one, all still carrying the bearer token in the `Authorization` header, because the HPR token proves who the professional is, not that your client may call.

| Route                  | Path                                        |
| ---------------------- | ------------------------------------------- |
| By password            | `/v4/int/api/v1/auth/authPassword`          |
| By mobile OTP, send    | `/v4/int/api/v2/auth/loginViaMobileSendOTP` |
| By Aadhaar OTP, send   | `/v4/int/api/v1/auth/init`                  |
| By Aadhaar OTP, verify | `/v4/int/api/v1/auth/confirmWithAadhaarOtp` |

The bodies are on [the M4 API reference](/docs/hiecm/v3/api/m4).

## What your system has to hold

Per professional, store:

- The HPID, in both forms.
- The current HPR token, its expiry, and a way to refresh it without re-registering the person.
- The transaction id, for one flow only.
- The master data ids you sent for council, course, college, university, language, country, state and district. The registry rejects display values.
- The certificates you uploaded, with each document slot identifier.

Once, for the whole integration: the username and password for the management token call, and the public certificate from `v4/int/api/v1/auth/cert`. Three fields are encrypted with it, cipher `RSA/ECB/PKCS1Padding`: the mobile number in mobile match, the OTP in mobile login, and the email and password in create HPID. That cipher and that certificate belong to the NHPR. M1 encrypts with RSA-OAEP and SHA-1 under the ABHA certificate, so the two paths are not interchangeable.

Upload limits: 1 MB for a profile photo, 5 MB for anything else, png, jpeg, jpg or PDF only. Attachments go as a `fileType` and a base64 `data` string.

## Request and response formats

This page gives the behaviour, the call order, the parameter tables and the code lists. Take the request and response shapes from [the M4 API reference](/docs/hiecm/v3/api/m4) alongside it.

## Next

- [HFR](/docs/hiecm/v3/registries/nhpr/hfr), the facility half, which needs a token from this registry.
- [NHPR](/docs/hiecm/v3/registries/nhpr), the parent page.
- [M4 user journey](/docs/hiecm/v3/milestones/m4), the same order as diagrams.
- [the M4 API reference](/docs/hiecm/v3/api/m4), its operations and their fields.
