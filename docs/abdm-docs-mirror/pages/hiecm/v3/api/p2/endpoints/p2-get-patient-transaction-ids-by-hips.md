# Get Patient Transaction IDs by HIPs

`POST /api/care-context-link/patient/transaction-ids`

Returns the transfer transaction ids for a person's records at the HIPs given, under the consent artefacts given.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/patient/transaction-ids \
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
