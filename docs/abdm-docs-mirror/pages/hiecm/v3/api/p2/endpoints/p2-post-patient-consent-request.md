# Post Patient Consent Request

`POST /api/care-context-link/patient/consent-request`

Raises a consent request from the person's own PHR for records at the HIPs given, so they can be fetched into the app.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/patient/consent-request \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaAddress": "<ABHA_ADDRESS>",
  "hipIds": [
    "HIP001",
    "HIP002"
  ],
  "consentArtefactIds": [
    "consent-001",
    "consent-002"
  ]
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `abhaAddress` (string, required)
- `hipIds` (string[], required)
- `consentArtefactIds` (string[], required)

## Responses

- `200`: No response body is documented for this request.
