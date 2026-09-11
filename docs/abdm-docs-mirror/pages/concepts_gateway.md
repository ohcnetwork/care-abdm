# The ABDM gateway

The gateway is the routing layer for [ABDM](/docs/hiecm/v3/getting-started/glossary#abdm). You never call a hospital, a lab or a [PHR](/docs/hiecm/v3/getting-started/glossary#phr) app directly. The answer to a call arrives later at an endpoint you expose, and the gateway issues the access token every other call carries.

## Gateway and HIE-CM are not the same thing

[HIE-CM](/docs/hiecm/v3/getting-started/glossary#hie-cm) is the service: patient identity, care context links and consent. Its four modules and who builds which are on [Integration milestones](/docs/hiecm/v3/milestones).

The gateway is its front door. It authenticates you, validates your headers, and routes each call. Your consent request goes to `/api/hiecm/consent/v3/request/init` on the gateway host, and the gateway puts it in front of the patient's consent manager.

## HIE-CM is data blind

It never holds a patient's health record, only identifiers, metadata about where records live, and consent artefacts. Once consent exists the record goes straight from the system that holds it to the system that asked, encrypted. Your system keeps the data. HIE-CM keeps the permission.

## Nothing goes participant to participant

Every request is addressed to the gateway, which forwards it. Three things follow.

- **You get an acknowledgement, not an answer.** In the [M3](/docs/hiecm/v3/getting-started/glossary#m3) consent flow the [HIU](/docs/hiecm/v3/getting-started/glossary#hiu) asks, the HIE-CM acknowledges with a consent request id, and the patient's decision comes back later. Each call's page in the [API reference](/docs/hiecm/v3/api) names the callback it produces.
- **You have to be reachable.** Half of [M2](/docs/hiecm/v3/getting-started/glossary#m2) is endpoints the gateway calls on your system. A [HIP](/docs/hiecm/v3/getting-started/glossary#hip) it cannot reach fails on someone else's logs, as `ABDM-1028 HIP is unavailable`.
- **Order is enforced.** The M2 error list carries `ABDM-2406 Invalid API sequence flow, please follow logical flow`.

One exception. In the health information flow the HIU supplies a data push URL, and the HIP encrypts the records and pushes them there. That URL may differ from the HIU's registered gateway URL, to improve privacy. The permission came through the gateway. The bytes do not.

## What moves through it

| Module | What the gateway routes | Reference |
|---|---|---|
| [M1](/docs/hiecm/v3/api/m1) | Session tokens, and the calls that create and authenticate an ABHA identity | [M1 API reference](/reference/hiecm-m1) |
| [M2](/docs/hiecm/v3/api/m2) | [Discovery](/docs/hiecm/v3/getting-started/glossary#discovery), care context linking, health information requests to a HIP | [M2 API reference](/reference/hiecm-m2) |
| [M3](/docs/hiecm/v3/api/m3) | Consent requests, consent notifications, artefact fetches, data flow requests | [M3 API reference](/reference/hiecm-m3) |
| [M4](/docs/hiecm/v3/api/m4) | Session tokens for the [HPR](/docs/hiecm/v3/getting-started/glossary#hpr) and [HFR](/docs/hiecm/v3/getting-started/glossary#hfr) registry calls | [M4 API reference](/reference/hiecm-m4) |

The gateway holds no health record. It routes the permission and the metadata.

## The session endpoint

One endpoint issues the token every other call carries. It is the same call in [M1](/docs/hiecm/v3/getting-started/glossary#m1) and [M4](/docs/hiecm/v3/getting-started/glossary#m4).

**POST** `/api/hiecm/gateway/v3/sessions`

Headers:

| Header | Value in the collection | What it is |
|---|---|---|
| `REQUEST-ID` | `{{$randomUUID}}` | A fresh UUID for this call |
| `TIMESTAMP` | `{{$isoTimestamp}}` | The time you made the call, ISO 8601 |
| `X-CM-ID` | `sbx` | The consent manager. Use `sbx` for sandbox and `abdm` for production |
| `Content-Type` | `application/json` | |

No `Authorization` header on this call. It is the one call with no token yet, and the collection marks it `noauth`.

Body, transcribed from the collection:

```json
{
  "clientId": "healthid-api",
  "clientSecret": "<CLIENT_SECRET_FROM_SANDBOX_SIGNUP>",
  "grantType": "client_credentials"
}
```

The collection sends the literal `healthid-api` as the client id. The M4 document shows a per integrator value in the same field. Send whatever you were issued.

Response shape, from the M4 document, which prints it as text:

```json
{
  "accessToken": "<JWT>",
  "expiresIn": 1200,
  "refreshExpiresIn": 1800,
  "refreshToken": "<JWT>",
  "tokenType": "bearer"
}
```

The response carries the token in `accessToken`.

Send the token back as `Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>` on every other call. Headers per call, and the second token M1 login issues, are on [authentication](/docs/hiecm/v3/reference/authentication). Interactive: [gateway API reference](/reference/hiecm-gateway).

## Which host

Four hosts serve gateway paths.

| Host | Environment |
|---|---|
| `https://dev.abdm.gov.in` | Sandbox |
| `https://apissbx.abdm.gov.in` | Sandbox, on the sessions call |
| `https://live.abdm.gov.in` | Production, alongside `apis` for the same call |
| `https://apis.abdm.gov.in` | Production |

Take the host from the sandbox documentation issued at onboarding, and keep it in configuration, not in code.

## Limits to code against

- **Callback retries.** Make your endpoint idempotent and assume a repeat.
- **Gateway token lifetime.** Read `expiresIn` from your own response rather than hard coding a value.
- **Rate limits.** Two codes enforce them: `ABDM-1022 Too many requests` and `ABDM-1027 You are blocked. Please try again after 24 hours.` The thresholds are not published, so back off on both.
- **Request signing.** The gateway request itself is not signed. Payload encryption and signing apply to health records, on the [M2](/docs/hiecm/v3/api/m2) side.

## Next

- [Authentication](/docs/hiecm/v3/reference/authentication), credentials and headers.
- [API references](/docs/hiecm/v3/api), every call and the callback it produces.
- [Integration milestones](/docs/hiecm/v3/milestones), the four modules and who builds which.
- [Registries](/docs/hiecm/v3/registries), who and what ABDM identifies.
- [Error codes](/docs/hiecm/v3/reference/error-codes), what a rejection means.
