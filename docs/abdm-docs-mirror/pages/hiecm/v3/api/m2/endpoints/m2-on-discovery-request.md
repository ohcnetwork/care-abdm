# A discovery request for a patient you may hold records for

`POST /api/v3/hip/patient/care-context/discover`

Inbound to every HIP. Answer with care context metadata only: a discovery response carries no clinical or sensitive data. A rejected answer is reported as ABDM-1109.

Retry count, backoff and timeout for this callback are not stated in NHA's material, so treat them as unknown.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/api/v3/hip/patient/care-context/discover \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIP-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "transactionId": "<TRANSACTION_ID>",
  "patient": {
    "id": "<ID>",
    "verifiedIdentifiers": [
      "<VERIFIED_IDENTIFIERS>"
    ],
    "unverifiedIdentifiers": [
      "<UNVERIFIED_IDENTIFIERS>"
    ],
    "name": "<NAME>",
    "gender": "M",
    "yearOfBirth": 0
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`. M2 also uses per flow tokens, a link token for linking and an authorisation token for patient scoped calls. Their header names are not yet published.

## Headers

- `REQUEST-ID` (string, required): A fresh UUID that you generate for this request. The callback that answers it carries the same value, so this is how you match an asynchronous reply to the call that caused it. Store it before you send the request, not after.
- `TIMESTAMP` (string, required): The current time in ISO 8601, UTC, with milliseconds and a `Z` suffix, from a synchronised clock. The sandbox rejects IST and accepts UTC.
- `X-HIP-ID` (string, required): Identifier of the Health Information Provider the request or callback belongs to. This is per facility, and it is what a callback arriving at your one bridge URL is routed on. The bridge URL and your credentials belong to the integration, not to the facility.

## Body

- `transactionId` (string, required): A fresh identifier for this discovery flow. Echo it back as response.requestId when you answer on m2_on_discover_care_contexts.
- `patient` (object, required)
- `patient.id` (string, required): A patient identifier to search your records by.
- `patient.verifiedIdentifiers` (object[], required)
- `patient.unverifiedIdentifiers` (object[]): Identifiers to search your own records by, not verified by ABDM.
- `patient.name` (string, required)
- `patient.gender` (string, required) One of: M, F, O, D, T, U.
- `patient.yearOfBirth` (integer, required)

## Responses

- `202`: Your bridge accepted the callback. The gateway validates the body you send back, so a 202 carrying the wrong body is still a failure.
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
