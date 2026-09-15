# 01 discovery

`POST /user-initiated-linking/link/discover`

Discovers the person's care contexts at a HIP using their demographics and any identifiers they hold there.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/user-initiated-linking/link/discover \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hip": {
    "id": "<HIP_ID>",
    "name": "<NAME>"
  },
  "unverifiedIdentifiers": [
    {
      "type": "MR",
      "value": "<MOBILE>"
    }
  ]
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `hip` (object, required)
- `hip.id` (string, required)
- `hip.name` (string, required)
- `unverifiedIdentifiers` (object[], required)
- `unverifiedIdentifiers.type` (string, required)
- `unverifiedIdentifiers.value` (string, required)

## Responses

- `200`: No response body is documented for this request.
