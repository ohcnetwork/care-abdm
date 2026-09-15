# Find Bridge Service by Service ID

`GET /api/hiecm/gateway/v3/bridge-service/serviceId/{serviceId}`

Look up a specific registered HIP/HIU service by its service ID.

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/bridge-service/serviceId/{serviceId} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 5f7a4a1e-59ba-4c0c-9e0c-8e6b3b6e2f11' \
  --header 'TIMESTAMP: 2026-08-25T15:51:15.339Z' \
  --header 'X-CM-ID: <X_CM_ID>'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` returned by `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): A fresh UUID that you generate for this request. It is how you and the gateway correlate a call with its callback and with a support ticket, so log it. Reusing one across requests makes both impossible.
- `TIMESTAMP` (string, required): The current time in ISO 8601 UTC, with milliseconds and the `Z` suffix. The gateway rejects a request whose timestamp has drifted too far from its own clock, so take this from a synchronised clock rather than from a local one.
- `X-CM-ID` (string, required): Which consent manager you are talking to. `sbx` on the sandbox and `abdm` in production. Sending the wrong one against the right host is a common first-day failure and reads as an authorisation error.

## Path parameters

- `serviceId` (string, required): Service identifier

## Responses

- `200`: Service details

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "id": 0,
  "bridgeId": "<BRIDGE_ID>",
  "serviceId": "<SERVICE_ID>",
  "name": "<NAME>",
  "isHip": false,
  "isHiu": false,
  "isHealthLocker": false,
  "isPhr": false,
  "active": false,
  "registerTime": "2026-08-24T10:15:30.000Z",
  "dateCreated": "2026-08-24T10:15:30.000Z",
  "dateModified": "2026-08-24T10:15:30.000Z"
}
```
