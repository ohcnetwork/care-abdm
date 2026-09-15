# Citizen

You are the person the health records are about. You build nothing and call nothing. You hold an identity, and you decide who sees what.

## Who you are in ABDM

Your identity is an [ABHA](/docs/hiecm/v3/getting-started/glossary#abha), the Ayushman Bharat Health Account. It has two parts.

|                | ABHA number                                                                            | ABHA address                               |
| -------------- | -------------------------------------------------------------------------------------- | ------------------------------------------ |
| What it is     | 14 digits, such as `91-XXXX-XXXX-XXXX`                                                 | A readable name, such as `name@abdm`       |
| How you get it | After an Aadhaar based [KYC](/docs/hiecm/v3/getting-started/glossary#kyc) check passes | You choose it, or you are issued a default |
| What it does   | Anchors one person to one number                                                       | Routes records and consent requests to you |

You can hold an address without a number, created from a mobile number, name, age and gender. That profile is self declared and carries no KYC.

A [PHR](/docs/hiecm/v3/getting-started/glossary#phr) app holds your account and acts for you. Hospitals, laboratories and pharmacies address records to your ABHA address.

## What you can do

- Create an ABHA, by Aadhaar [OTP](/docs/hiecm/v3/getting-started/glossary#otp), face authentication, biometrics or a demographic match.
- Share your profile at a counter by scanning the facility's QR code, and see what is being shared before you agree.
- Search for a facility you visited, find records nobody has linked yet, and link them to your address.
- Read a consent request in full: who is asking, why, which record types, which dates, and how long the access lasts.
- Narrow it before you approve. You can change the access duration, the record date range, the data categories and the validity period.
- Grant, deny, or revoke later. Revoking stops sharing under that consent immediately.

## Why it is worth it

Your records stay in the systems that created them. The [HIE-CM](/docs/hiecm/v3/getting-started/glossary#hie-cm) holds identifiers, pointers and consent, never the record itself. Nothing central collects your health history.

One address pulls records from many facilities into one app you choose. A permission you give is scoped and time boxed rather than open ended. Both sides of a transfer report it, so an exchange under your consent leaves a trail you can see.

## Next

[Consent](/docs/hiecm/v3/concepts/consent) explains what a request carries and the states it moves through.
