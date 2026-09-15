# Build it well

Every call on this site can be made correctly and still leave you with an integration that fails at a busy counter. What separates the two is handling: what you check before you call, what you do with what comes back, and what the person in front of you sees while it happens.

## In short

- Check locally what can be checked locally. A round trip that fails a format rule costs the person thirty seconds and tells them nothing.
- Read the body, not the status. ABDM returns four error shapes and only some carry a code.
- Retry only what is safe to retry. Enrolment and one time password calls are not.
- Say what failed and what the person can do next. A code on its own is not an error message.
- Map every field the profile returns, not the four you need this week.

## Validate before you send

These rules are the service's, and it applies them after it decrypts. Checking them in your own form turns a failed call into an inline message.

| What           | Rule                                                                                                                     | What it costs to skip                             |
| -------------- | ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| ABHA number    | 14 digits with dashes, `NN-NNNN-NNNN-NNNN`, before encryption                                                            | `400 {"loginId": "LoginId is invalid"}`           |
| ABHA address   | 8 to 18 characters, letters and digits with an optional `.` or `_`, then `@` and the domain                              | A rejected address after the person has chosen it |
| Mobile number  | 10 digits, no country code and no `+`                                                                                    | A failed call that reads as a wrong number        |
| Aadhaar number | 12 digits, no spaces                                                                                                     | The same                                          |
| `REQUEST-ID`   | A fresh UUID version 4 on every call                                                                                     | Two calls you cannot tell apart later             |
| `TIMESTAMP`    | ISO 8601 in UTC, from a synchronised clock. Every header is in [authentication](/docs/hiecm/v3/reference/authentication) | Every call fails at once                          |

One thing you cannot check locally is whether the account exists. A well formed ABHA number that belongs to nobody returns `404 ABDM-1114 User not found`, and that is a different message to the person than a badly formed one. The plaintext shape for every encrypted field is in [encryption](/docs/hiecm/v3/concepts/encryption).

## Read the error, then decide

ABDM returns [four different error shapes](/docs/hiecm/v3/api/m1/errors), and only two of them carry a code. Parse for all four before you write any handling, because the shape tells you where the failure came from.

Every code in the [error code reference](/docs/hiecm/v3/reference/error-codes) carries an action. Key your handling to that column rather than to a list of codes you maintain by hand.

| Action         | What your code does                                                           |
| -------------- | ----------------------------------------------------------------------------- |
| Fix request    | Do not retry. Something you sent is wrong, and sending it again will not help |
| Fix auth       | Fetch a fresh token, then retry once                                          |
| New request id | Generate a new `REQUEST-ID`, then retry once                                  |
| Retry          | Back off and retry, with a ceiling on attempts                                |
| Cannot proceed | Stop, and tell the person why in their own terms                              |
| Ask support    | Stop, and collect the ids before the context is lost                          |
| Unclassified   | Treat as Cannot proceed until you have seen it once and know better           |

Symptom first debugging, for the failures that produce no useful code at all, is in [troubleshooting](/docs/hiecm/v3/troubleshooting).

## Retries, and the calls you must not repeat

A retry is safe when repeating the call cannot create a second thing or burn a single use value. Most of M1 fails that test.

| Call                            | Safe to repeat | Why                                                                                               |
| ------------------------------- | -------------- | ------------------------------------------------------------------------------------------------- |
| Session token                   | Yes            | It issues a token and changes nothing else                                                        |
| Profile, card and QR code reads | Yes            | Reads                                                                                             |
| Request an OTP                  | No             | Rate limited. A retry loop is the usual cause of the lockout it is trying to escape               |
| Verify an OTP                   | No             | The OTP and the transaction id are both single use                                                |
| Enrol, or create an ABHA        | No             | A success you did not see still created an account                                                |
| Your callback handler           | It must be     | ABDM repeats callbacks, so deduplicate on the id the callback repeats before you apply any effect |

`REQUEST-ID` is the idempotency key, one fresh UUID per call, and it is what lets you tell a repeat from a new attempt in your own logs. See [authentication](/docs/hiecm/v3/reference/authentication) for the headers and [the gateway](/docs/hiecm/v3/concepts/gateway) for the limits.

## What the screen says when a call fails

The person at the counter cannot act on a code. They can act on what to do next.

| What happened                            | What the screen says                               | What it must not do                      |
| ---------------------------------------- | -------------------------------------------------- | ---------------------------------------- |
| The OTP did not match                    | Say so, keep the field, offer a resend             | Close the form or show a generic failure |
| Rate limited or locked out               | Name the actual wait, for example thirty minutes   | Say something went wrong                 |
| No account found                         | Show it as a result, not as an error               | Turn a normal empty result red           |
| The address already exists               | Offer the login route instead                      | Report a creation failure                |
| ABDM or the other party is not answering | Say it is not answering and to try again           | Imply the person typed something wrong   |
| Anything with no code at all             | Show the reference the person can quote to support | Print the raw response body              |

## The screens themselves

| Rule                                                                              | Why                                                                                                                                                                                                                                                                                                                |
| --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| A step happening on somebody else's device is not a spinner                       | Face authentication waits on a person. Say that is what you are waiting for                                                                                                                                                                                                                                        |
| Show the masked destination before the wait                                       | The search response names the mobile the OTP went to, which stops somebody waiting for a message that will never arrive                                                                                                                                                                                            |
| Say upfront when the account will be restricted                                   | Otherwise the person meets the limit later, when something unrelated fails                                                                                                                                                                                                                                         |
| Answer scan and share inside thirty seconds                                       | The patient's screen is open for that long, and an acknowledgement after it shows them nothing                                                                                                                                                                                                                     |
| Offer the login methods the account actually has                                  | `authMethods` on the profile says which ones the person can use. A screen offering an Aadhaar OTP to a profile with no Aadhaar behind it fails for a reason nobody can see                                                                                                                                         |
| Put a setting at the level it belongs to                                          | Your credentials and your callback URL belong to the integration, the facility ID and the `hipId` belong to each facility. A settings screen that mixes them works for the first facility and fails on the next. See [one bridge, many facilities](/docs/hiecm/v3/concepts/how-it-fits#one-bridge-many-facilities) |
| Aadhaar numbers, one time passwords and passwords never reach a log or a database | Encrypting a value and then logging the plain one is the same leak, moved. See [encryption](/docs/hiecm/v3/concepts/encryption)                                                                                                                                                                                    |

The first four are journey specific and each is explained where it happens, on [the M1 journeys](/docs/hiecm/v3/milestones/m1).

## Map everything ABHA gives you

The most common M1 defect is a registration form wired to four fields when the profile returned thirty. The rest is then either retyped by a person who already gave it to Aadhaar, or lost.

`GET /v3/profile/account` returns the fields below. Map all of them, and decide for each whether your form shows it, locks it or lets a receptionist correct it.

| Profile field                                                                    | Goes to                                                               | Editable in your form                                    |
| -------------------------------------------------------------------------------- | --------------------------------------------------------------------- | -------------------------------------------------------- |
| `ABHANumber`, `preferredAbhaAddress`                                             | The patient's ABDM identity, and the key you match on later           | Never                                                    |
| `name`, `firstName`, `middleName`, `lastName`                                    | Patient name. Keep the parts, not only the joined string              | Only on a Self-Declared profile                          |
| `dayOfBirth`, `monthOfBirth`, `yearOfBirth`                                      | Date of birth, assembled by you                                       | Only on a Self-Declared profile                          |
| `gender`                                                                         | Gender, as `M`, `F` or `O`                                            | Only on a Self-Declared profile                          |
| `mobile`                                                                         | Contact number                                                        | Yes, it is the communication number and people change it |
| `address`, `pincode`, `stateName`, `districtName`, `subdistrictName`, `townName` | Address. The `*Code` twins are the machine values, keep both          | Yes                                                      |
| `stateCode`, `districtCode`, `subDistrictCode`                                   | Your own reporting, which should key on codes rather than names       | Never                                                    |
| `kycVerified`, `verificationStatus`, `verificationType`                          | Whether this identity was proved, and by what                         | Never                                                    |
| `authMethods`                                                                    | What the person can log in with next time, so you offer the right one | Never                                                    |
| `kycPhoto`, `profilePhoto`                                                       | Identity photo. Decide whether you store it at all before you do      | Never                                                    |
| `status`                                                                         | Whether the account is active                                         | Never                                                    |
| `localizedDetails`                                                               | The same details in the person's own language, where NHA holds them   | Never                                                    |

`kycVerified` is the field the form design hangs off. A [KYC verified profile](/docs/hiecm/v3/milestones/m1#abha-with-aadhaar) was proved against Aadhaar, so its demographics are better evidence than anything typed at a desk and your form should lock them. A [Self-Declared profile](/docs/hiecm/v3/milestones/m1#abha-address-with-a-mobile-number) is what the person typed themselves, so it is correctable, and it becomes KYC verified in place if they link an ABHA number later.

Two traps. Several of these fields are nullable, and `villageName`, `wardName` and `townName` are commonly null, so a form that renders a blank labelled row for each is worse than one that hides them. And the profile comes back in more than one shape across M1: the update response types `yearOfBirth` as an integer where this one types it as a string, and the patient share payload and the PHR profile carry different names again. Map from one named endpoint and say which, rather than writing one mapper for something called the ABHA profile.

## Where to go next

- [Build with AI](/docs/hiecm/v3/getting-started/build-with-ai) for setting an agent up, and for how to prompt it against these rules.
- [Troubleshooting](/docs/hiecm/v3/troubleshooting) when something is already broken.
- [Go live](/docs/hiecm/v3/getting-started/going-live) for what certification asks of you.
