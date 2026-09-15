# ABHA, the patient registry

[ABHA](/docs/hiecm/v3/getting-started/glossary#abha) is the Ayushman Bharat Health Account, the patient half of [Registries](/docs/hiecm/v3/registries). It answers "who is this patient", and every record flow in [ABDM](/docs/hiecm/v3/getting-started/glossary#abdm) starts from that answer.

## One account, two identifiers

|                    | ABHA number                                                                            | ABHA address                                               |
| ------------------ | -------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| What it looks like | 14 digits, hyphenated in samples as `91-XXXX-XXXX-XXXX`                                | A readable name, such as `name@abdm`                       |
| How it is issued   | After an Aadhaar based [KYC](/docs/hiecm/v3/getting-started/glossary#kyc) check passes | Chosen by the person, or issued as a default               |
| What it is for     | The identity anchor. One person, one number                                            | Routing. It is the handle other systems address records to |
| Can exist alone    | No. It always carries a default address                                                | Yes. A person can hold an address with no number           |

Store both. You match a patient record against the number, and you send the address when you link a [care context](/docs/hiecm/v3/getting-started/glossary#care-context) or ask for consent. The number is issued only after a strong KYC process completes.

## The check digit

Two validation utilities exist: ABHA number validation by the Luhn algorithm, and Aadhaar number validation by the Verhoeff algorithm. Luhn derives the last digit from the ones before it, so you catch a mistyped number locally before spending a call.

## How identity is verified

Verification runs against Aadhaar through the ABHA service, so your system never calls Aadhaar directly. There are four routes:

| Route                                                      | How the person proves identity                                                      | Private integrators | Government integrators |
| ---------------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------- | ---------------------- |
| Aadhaar [OTP](/docs/hiecm/v3/getting-started/glossary#otp) | A code sent to the Aadhaar linked mobile number                                     | Mandatory           | Mandatory              |
| Face authentication                                        | A QR code scanned in the ABHA app, then face capture through the Aadhaar RD service | Optional            | Optional               |
| Biometrics                                                 | Fingerprint or IRIS on a registered device, which returns a signed PID block        | Optional            | Optional               |
| Demographic authentication                                 | Name, date of birth and gender matched against Aadhaar                              | Not required        | Mandatory              |

Build Aadhaar OTP first. It is mandatory for everyone and needs no hardware.

### Child ABHA

A child under six has no Aadhaar number. Child ABHA is a 14 digit identifier created with a parent or legal guardian's consent, so a health record exists from birth. It is restricted to specific government integrators approved by NHA leadership, through programmes including UWIN, RCH and POSHAN. Private integrators cannot use it.

## The ABHA address

The shape is `name@abdm`.

- **Every number gets a default address**, the number with a suffix: `14digit@sbx` in [sandbox](/docs/hiecm/v3/getting-started/glossary#sandbox), `14digit@abdm` in production. The M1 Postman collection shows a `preferredAbhaAddress` field holding the 14 digits with the `@abdm` suffix and no hyphens.
- **A person can then create a memorable one.** A suggestion call offers addresses, and a custom address is accepted, linked to the number.
- **An address can exist without a number.** One can be created on the [HIE-CM](/docs/hiecm/v3/getting-started/glossary#hie-cm) from mobile number, name, age and gender, self declared and with no KYC. Expect accounts with no number behind them.

### Address policy

These rules apply:

- Letters, numbers and a dot are allowed.
- It cannot begin with a number.
- It cannot begin or end with a dot.
- An all numeric address is allowed only in the `14digit@abdm` default form.
- A 10 digit mobile number as an address is restricted and not created.

Minimum length differs by flow. Validate against the error the endpoint returns rather than assuming one rule across all of them.

## What an address is allowed to be

NHA validates the address on creation, so a form that accepts what NHA refuses produces a failure the person cannot act on. Letters, digits and a single dot are allowed, and beyond that:

- It cannot begin with a digit.
- It cannot begin or end with a dot.
- An all digit address is allowed for an ABHA number and nothing else, which is what makes the default `14digit@abdm` legal.

Three shapes read as though they should work and do not. A ten digit mobile number as an address is restricted. An ABHA number as an address you create is not allowed, although the default one is issued automatically and signing in with it works on both web and mobile. And anything failing the rules above is refused at creation rather than at submission.

The minimum length is stated twice, differently

NHA's PHR document gives the minimum as 4 characters in its narrative and as 8 in the test case for creating an address by mobile number. Neither has been run against the sandbox from here. Build to 8, which is the stricter reading.

A password is created alongside the address: at least 8 characters, at least one uppercase letter, one lowercase letter, one digit and one symbol, no spaces, and no more than two consecutive characters or keyboard keys. NHA describes enforcing it as optional for the application, not the password itself as optional.

Offer suggestions rather than an empty box and a policy. Two calls exist for it, address suggestions and address exists, and NHA asks that suggestions be built from the person's name and the username part of their email.

## What an ABHA record holds

The profile response carries:

| Field                                         | What it is                                          |
| --------------------------------------------- | --------------------------------------------------- |
| `ABHANumber`                                  | The 14 digit number, hyphenated                     |
| `preferredAbhaAddress`                        | The address, with its suffix                        |
| `mobile`                                      | The communication mobile number                     |
| `firstName`, `middleName`, `lastName`, `name` | Name parts and the joined name                      |
| `yearOfBirth`, `monthOfBirth`, `dayOfBirth`   | Date of birth as three separate strings             |
| `gender`                                      | A single letter                                     |
| `email`                                       | Present once an email is verified, otherwise `null` |
| `profilePhoto`                                | Base64 image data with no data URI prefix           |

The communication mobile number need not be the Aadhaar linked one. It is verified separately, by its own OTP, after enrolment. Email is optional throughout. An ABHA also carries a card, downloadable as an image, and a QR code, both M1 calls. Field level detail is on [M1 APIs](/docs/hiecm/v3/api/m1/apis).

## Where the calls go

```text
Sandbox     https://abhasbx.abdm.gov.in/abha/api/v3/Production  https://abha.abdm.gov.in/api/abha/v3/
```

One exception: login by Aadhaar number using fingerprint or IRIS uses the v3.1 base URL, `https://abhasbx.abdm.gov.in/abha/api/v3.1/`. No production v3.1 URL is given.

## What M1 does with it

[M1](/docs/hiecm/v3/api/m1) is the only milestone that writes to this registry. It covers creation, login, profile management and sessions. Login by mobile number, Aadhaar number, ABHA number and ABHA address are all four mandatory for both private and government integrators.

## What every other milestone assumes

- **[M2](/docs/hiecm/v3/api/m2)** links a care context to the ABHA address and answers [discovery](/docs/hiecm/v3/getting-started/glossary#discovery) against it. See [Linking records](/docs/hiecm/v3/concepts/linking).
- **[M3](/docs/hiecm/v3/api/m3)** raises a consent request against the ABHA address. See [Consent](/docs/hiecm/v3/concepts/consent).
- **[PHR applications](/docs/hiecm/v3/concepts/phr)** sign a person in by ABHA address and show the records linked to it.

No flow starts without an ABHA, so M1 comes first even when your real goal is M2 or M3.

## Next

- [NHPR](/docs/hiecm/v3/registries/nhpr), the professional and facility registries.
- [M1, ABHA identity](/docs/hiecm/v3/api/m1), the guide.
- [M1 API reference](/reference/hiecm-m1).
- [Sandbox data dictionary](/docs/hiecm/v3/reference/data-dictionary), test identities.
