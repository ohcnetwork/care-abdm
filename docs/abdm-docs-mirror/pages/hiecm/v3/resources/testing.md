# Testing use cases

Every [HIE-CM](/docs/hiecm/v3/getting-started/glossary#hie-cm) module has a set of cases your integration is tested against. They are listed here, one page per module, and each case keeps the id it carries at certification.

## Where you run them

You run these cases against the [sandbox](/docs/hiecm/v3/getting-started/glossary#sandbox), on sandbox credentials. [Get your sandbox credentials](/docs/hiecm/v3/getting-started/sandbox) covers registration, the client id and secret, the callback URL and the base URLs.

Three things about the sandbox decide how a case behaves:

- **It runs on its own hosts, under its own credentials.** A production client id against a sandbox host fails, and so does the reverse. [Go live](/docs/hiecm/v3/getting-started/going-live) lists both sets.
- **Nothing in it is a real person or a real record.** Every identity a case needs is one you create in an earlier case.
- **Passing every case is not certification.** Functional testing is run by an empanelled agency as part of the sandbox exit process. Passing here is how you arrive at that ready.

## How to read a case

Each case is one row. Open it for the detail and the calls it exercises.

| Column          | What it holds                                                                                                                                                                    |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Id              | The id you will be asked about at certification, such as `CRT_ABHA_101`. Quote it when you report a result or ask about a case.                                                  |
| Type            | Mandatory, Optional or Conditional. A conditional case names the condition it applies under. A few cases carry no marking at all and read as Unmarked, which is how they arrive. |
| Functionality   | What the case exercises, in one line.                                                                                                                                            |
| Expected result | What your system has to be able to show.                                                                                                                                         |

One type is this portal's own: **Portal check**. A case marked Portal check is a suggestion rather than a requirement, and skipping one costs you nothing at certification. Each covers a failure path the mandatory cases leave untested, which is where an integration usually breaks after it is live.

## The four modules

| Module                                    | What the cases cover                                                   | Certification cases | Portal checks |
| ----------------------------------------- | ---------------------------------------------------------------------- | ------------------- | ------------- |
| [M1](/docs/hiecm/v3/resources/testing/m1) | ABHA creation, verification, profile and share                         | 66                  | 56            |
| [M2](/docs/hiecm/v3/resources/testing/m2) | Care context linking, and sharing the records you hold                 | 36                  | 10            |
| [M3](/docs/hiecm/v3/resources/testing/m3) | Consent requests, and fetching records you did not create              | 16                  | 16            |
| [M4](/docs/hiecm/v3/resources/testing/m4) | Facility registration in the HFR, professional registration in the HPR | 184                 | None          |

## Cases that expect a callback

In M1 the answer comes back in the response to your call. In M2 and M3 it does not. The response acknowledges your request, and the answer arrives afterwards as a POST to the callback URL you registered.

A case that expects a callback needs that URL reachable from the public internet and listening, whether or not you are ready for the answer. In development that usually means a tunnel, and a tunnel gives you a new URL every restart. Register the new one each time. [Get your sandbox credentials](/docs/hiecm/v3/getting-started/sandbox) covers what the URL has to do.

## Next

- Start with [M1](/docs/hiecm/v3/resources/testing/m1).
- The calls each case makes: [API references](/docs/hiecm/v3/api).
- What happens once they pass: [Go live](/docs/hiecm/v3/getting-started/going-live).
