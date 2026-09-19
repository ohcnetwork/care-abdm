# PHR applications

A [PHR](/docs/hiecm/v3/getting-started/glossary#phr) application is the patient's app in [ABDM](/docs/hiecm/v3/getting-started/glossary#abdm): it holds a person's [ABHA](/docs/hiecm/v3/getting-started/glossary#abha) address, finds their records, takes consent and shows the records back. You build [M1](/docs/hiecm/v3/api/m1) for identity, [M3](/docs/hiecm/v3/api/m3) for consent and record fetching, and some [M2](/docs/hiecm/v3/api/m2) if users upload their own records.

## What a PHR app does

Every user needs an ABHA address, `username@abdm`. Consent, notifications and record sharing hang off it. There are six jobs:

| Job                            | What the user sees                                                                                                                                                    |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Create or link an ABHA address | Register with a mobile number, or with an existing 14 digit ABHA number                                                                                               |
| Log in                         | Mobile number, ABHA address, or ABHA number                                                                                                                           |
| Manage a profile               | Demographics, photo, password, QR code, downloadable ABHA card                                                                                                        |
| Share a profile at a facility  | Scan the facility QR code, consent, receive a queue token                                                                                                             |
| Find and link past records     | Search a facility, discover [care contexts](/docs/hiecm/v3/getting-started/glossary#care-context), verify by [OTP](/docs/hiecm/v3/getting-started/glossary#otp), link |
| Hold records                   | Receive notifications, request consent, fetch records, store and display them                                                                                         |

## Your app needs a server

A PHR app is two parts, whatever it looks like to the user. The app on the phone signs the person in, shows the screens and scans codes. A server you run holds the client ID and secret, mints the [gateway session token](/docs/hiecm/v3/concepts/gateway), and hosts the callback URL registered for your bridge. Every answer to a linking, consent or data request arrives at that URL as a POST, so an app with no server never hears the answer. Never ship the client secret inside the app.

## What you build in M1

The ABHA sandbox base URL is `https://abhasbx.abdm.gov.in/abha/api/v3/`. PHR enrolment uses `https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/request/otp`.

### Creating an ABHA address

Build both paths.

| Path                 | Validated by            | Profile details             | Result                                                                   |
| -------------------- | ----------------------- | --------------------------- | ------------------------------------------------------------------------ |
| Mobile number        | Mobile OTP              | The user types them         | **Self-Declared**, no [KYC](/docs/hiecm/v3/getting-started/glossary#kyc) |
| 14 digit ABHA number | Aadhaar OTP or ABHA OTP | Returned by the ABHA system | **KYC Verified**                                                         |

After validation on either path, show the ABHA addresses already linked to that mobile number or ABHA number, so the user picks one instead of creating a duplicate. ABDM wants one address per person.

Address rules:

- Letters, numbers, one optional dot and one optional underscore.
- Starts and ends with a letter or number, 8 to 18 characters long.
- Creating a `10digitmobile@abdm` address is currently blocked.
- Creating a `14digit@abdm` address is not allowed, but a user can log in with one. Every 14 digit ABHA number is issued a default address of this shape, written as `14digit@sbx` or `14digit@abdm`. Which environment uses which suffix is not documented yet.
- Password, where you collect one: 8 characters or longer, one A to Z, one digit, one special character from `!@#$^*_-`, no spaces, no more than 2 consecutive characters or keyboard keys. Password validation is now optional.

### Linking an ABHA number to an ABHA address

The ABHA number is the KYC verified identity; the ABHA address is what shares records. A user can hold several ABHA addresses but only one ABHA number.

A Self-Declared profile needs a "Link ABHA number" action: enter the 14 digit number, validate by Aadhaar OTP or ABHA OTP. Profile details then follow the ABHA number, the number becomes visible, and the status changes to KYC Verified.

### Login

All these routes are mandatory.

| Route                                           | Validated by                                                                |
| ----------------------------------------------- | --------------------------------------------------------------------------- |
| Mobile number                                   | Mobile OTP, then the user picks which linked ABHA address to sign in as     |
| An easy to remember address such as `name@abdm` | Password, mobile OTP or email OTP, by the auth methods the address supports |
| The 14 digit ABHA number                        | ABHA OTP or Aadhaar OTP                                                     |

Resend OTP unlocks after 60 seconds in every flow. You also need a reset password screen behind login with a confirmation message, secure storage of the refresh token to extend the session, and more than one user profile per install with sign in and sign out.

### Profile, card and QR code

| Element                  | What it holds                                                                                                                              |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Profile screen           | Editable demographics. KYC Verified with a green tick when an ABHA number is linked, Self-Declared with an exclamation mark when it is not |
| ABHA number              | Visible only on a KYC Verified profile                                                                                                     |
| ABHA address card, a PDF | Profile photo, full name, ABHA number as `91-0098-2416-3421` if one is linked, ABHA address, QR code, date of birth, gender, mobile number |
| Editable, KYC Verified   | Mobile number, with an OTP to the new number, and address                                                                                  |
| Editable, Self-Declared  | The same, plus photo, full name, gender and date of birth                                                                                  |

### Scan and share at a facility

The facility displays a QR code holding a URL with two parameters: the [HIP](/docs/hiecm/v3/getting-started/glossary#hip) ID and a facility defined context such as a counter code. Your app scans it, then:

1. Shows the user what will be shared.
2. Takes consent in ABDM's specified wording, covering sharing the ABHA address and profile information with that facility for registration, and the facility linking any records it generates.
3. Calls the [HIE-CM](/docs/hiecm/v3/getting-started/glossary#hie-cm) API to share the details.
4. Waits for the facility, currently expected to respond within 30 seconds.
5. Displays the token number if the facility returned one.

Counter names arrive in the QR code: 1 to 250 characters, letters, digits and spaces, with `.`, `-` or `_` allowed inside the name, examples OPD, OPD1, OPD cardio, IPD1, Pharmacy. A counter name cannot be the [HFR](/docs/hiecm/v3/getting-started/glossary#hfr) facility ID, the [HPID](/docs/hiecm/v3/getting-started/glossary#hpid), the HIP ID or the HIP name.

Opened from a third party scanner or the phone camera, go to the share profile screen if the user is signed in, to login first if not.

## What you build in M3

A citizen fetching records is the [HIU](/docs/hiecm/v3/getting-started/glossary#hiu), so every PHR application must implement that side.

### Subscriptions and notifications

A subscription is how your app hears about changes to a user's ABHA address. Set one up when you create an ABHA address, and when a user logs in with an address your install has not seen. Ask the user for consent first.

An approved subscription notifies your app when a care context is linked or updated. Surface these as device notifications, for example through Firebase on Android. You need screens to list subscriptions, approve, deny and edit them, where editing covers health information types, purpose, categories and the time period.

### Auto approval

So the user does not approve a request every time a hospital adds a record:

1. Ask the user to confirm your app may retrieve new linked records automatically.
2. Set up an auto approval policy with the HIE-CM.
3. Save the auto approval ID the HIE-CM returns.

While the policy is active, the consent request you raise on a new or updated care context notification is granted immediately and you fetch and store the record. The user must be able to disable a policy. A request then arrives for each record.

### Consent management

You build five capabilities:

| Capability           | What it covers                                                       |
| -------------------- | -------------------------------------------------------------------- |
| View requests        | Requesting HIU, purpose, data types, date range, validity, status    |
| Modify a request     | Access duration, record date range, data categories, validity period |
| Grant or deny        | The decision goes back to the HIE-CM                                 |
| View active consents | Who currently has access, and to what                                |
| Revoke               | Withdraw at any time. Sharing under that consent stops immediately   |

The Consents tab and the Subscriptions tab group state the same way: a Requests section holding Requested, Denied and Expired, and an Approved section holding Granted and Revoked.

### Fetching and displaying records

Once a care context is linked to the user's ABHA address:

1. Your app receives the notification.
2. It creates a consent request for that record and sends it to the HIE-CM.
3. The consent is granted, automatically if a policy exists, otherwise by the user.
4. It raises a health information request with the approved [consent artefact](/docs/hiecm/v3/getting-started/glossary#consent-artefact).
5. The HIP sends the records across the network.
6. Your app stores them for long term access and displays them, preferably in chronological order.

## Subscriptions, and why you need one

A care context can be linked to a person's address by any facility they visit, without your application being part of it. A subscription is how you find out: a standing watch on one address, delivering to your callback whenever something changes.

NHA expects a PHR app to set one up at two moments, when it creates an address and when a person signs in with an address it has not seen before. The person must be asked to consent to it; signing in does not imply it.

Once approved, a notification arrives when a care context is linked or updated. Showing it on the device is your job.

A request sits in exactly one state, and the same five carry consent requests, subscription requests and health locker requests, so one screen serves all three.

| Group    | State     | What it means                                        |
| -------- | --------- | ---------------------------------------------------- |
| Requests | Requested | Sent, and the person has not acted                   |
| Requests | Denied    | The person refused it                                |
| Requests | Expired   | The person did not act inside the requester's window |
| Approved | Granted   | The person allowed it                                |
| Approved | Revoked   | Allowed, then withdrawn                              |

A subscription is not consent and gives nobody a record. It tells you a record exists. Reading it still needs a consent, which is why a subscription usually runs alongside an auto approval policy.

## Discovery and user initiated linking

For a facility the user visited without giving an ABHA address, or for old records.

The user searches for the facility by name. Only facilities participating in ABDM appear, and the facility must be a HIP linked to an [HRP](/docs/hiecm/v3/getting-started/glossary#hrp). Your app sends a discovery request to the HIE-CM carrying name, year of birth, gender, verified identifiers such as mobile number or ABHA address, and optionally unverified identifiers such as a medical record number issued by that provider. The HIP is expected to respond within 10 seconds.

Care contexts already linked must not be shown again. When everything is linked, show the message "All your existing records are linked. No additional records available for linking".

The user selects care contexts and confirms, the HIP sends an OTP to the registered mobile number, and on successful verification the care contexts link to the ABHA address.

The same flow works for government health programmes such as CoWIN, AB-PMJAY, e-Sanjeevani OPD, e-Sanjeevani HWC and RCH.

Three failures have specified copy:

| Situation                           | Message                                                                                                   |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------- |
| The HIP is unreachable              | "Couldn't Connect: We are sorry. Unable to contact your hospital. Please try again later"                 |
| The user never visited the facility | "No health records found"                                                                                 |
| Everything is already linked        | "No new health record to link: Records of all visits are already linked and there is nothing new to link" |

Send the data transfer request within 5 minutes of the user tapping Pull Records. Records should arrive within 2 hours.

## Deep links

A patient who registers at a facility without an ABHA address gets an SMS carrying a deep link of the form `phr.abdm.gov.in/uhi/(hipcode)`. Tapping it lists approved ABHA mobile applications in random order, filtered to the user's operating system.

Your app must accept the HIPCODE parameter. Launched through a deep link, it must skip its normal login or home screen and go straight into discovery for that HIPCODE, guiding the user to enter the same name, date of birth, gender and mobile number they gave the facility. A mismatch stops the records being found.

To be listed, you submit three things at sandbox exit: application name, Play Store URL and App Store URL.

## Where the citizen is the HIP

A citizen pushing a record into your app is the HIP. A health locker, where users upload their own records, puts you on that publishing side. A PHR app must accept scanned physical records and output from devices such as BP meters, glucose meters, fitness trackers and smartwatches. Your app sets the health information type from the contents or from user input, and uses `HealthDocumentRecord` when it cannot be determined.

An uploaded record is shareable once you have three things: a linking token from the M1 APIs, a care context added to the user's ABHA address by HIP initiated linking from [M2](/docs/hiecm/v3/api/m2), and the M2 health information transfer APIs.

## What you do not need to build

- **Facility side clinical records.** No [FHIR](/docs/hiecm/v3/getting-started/glossary#fhir) bundles from a hospital or lab system, other than records your users upload.
- **[HPR](/docs/hiecm/v3/getting-started/glossary#hpr) and HFR registration.** M4 covers the professional and facility registries.
- **[UHI](/docs/hiecm/v3/getting-started/glossary#uhi).** Consultation, ambulance and pharmacy booking runs on a separate gateway.
- **[NHCX](/docs/hiecm/v3/getting-started/glossary#nhcx).** Claims and insurance exchange runs on a separate gateway.

## What to read next

- [M1 overview](/docs/hiecm/v3/api/m1) for ABHA creation, login and session APIs, and the [M1 API reference](/reference/hiecm-m1).
- [M3 overview](/docs/hiecm/v3/api/m3) for consent, subscriptions and data fetch, and the [M3 API reference](/reference/hiecm-m3).
- [M2 overview](/docs/hiecm/v3/api/m2) if you are building a health locker, and the [M2 API reference](/reference/hiecm-m2).
- [Get started](/docs/hiecm/v3/getting-started/sandbox) for sandbox signup and your first call.
- [Hospital, lab and pharmacy systems](/docs/hiecm/v3/concepts/hip-hiu) for the other side of every flow on this page.
