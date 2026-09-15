# 08 - Fetch Incoming Records Bundle [POST]

`POST /digi-locker/incoming/records`

Fetches the FHIR bundle for one care context that a HIP has sent to the person's DigiLocker.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/digi-locker/incoming/records \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hipId": "IN0710000700",
  "careContextReference": "<TXN_ID>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `hipId` (string, required)
- `careContextReference` (string, required)

## Responses

- `200`: No response body is documented for this request.
