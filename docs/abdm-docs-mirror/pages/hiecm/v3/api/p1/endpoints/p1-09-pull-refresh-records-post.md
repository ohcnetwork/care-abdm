# 09 - Pull / Refresh Records [POST]

`POST /digi-locker/pull/records`

Asks a HIP to send the person's latest records to DigiLocker. The records arrive later; poll the refresh endpoint for them.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/digi-locker/pull/records \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hipId": "IN0710000700"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `hipId` (string, required)

## Responses

- `200`: No response body is documented for this request.
