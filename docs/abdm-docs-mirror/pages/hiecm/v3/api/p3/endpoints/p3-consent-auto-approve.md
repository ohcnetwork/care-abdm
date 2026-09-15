# Consent Auto Approve

`POST /api/consent-management/consents/auto-approve`

Creates an auto-approval policy: consent requests from the HIU named are approved without asking, for the sources included and not the ones excluded.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/consent-management/consents/auto-approve \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "isApplicableForAllHIPs": true,
  "hiu": {
    "id": "IN0002222",
    "name": "<NAME>"
  },
  "includedSources": [
    {
      "hiTypes": [
        "OPCONSULTATION"
      ],
      "purpose": {
        "text": "Care Management",
        "code": "CAREMGT",
        "refUri": "string"
      },
      "hip": null,
      "period": {
        "from": "2025-09-30T16:51:40.617Z",
        "to": "2026-07-09T16:51:40.617Z"
      }
    }
  ],
  "excludedSources": null
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `isApplicableForAllHIPs` (boolean, required)
- `hiu` (object, required)
- `hiu.id` (string, required)
- `hiu.name` (string, required)
- `includedSources` (object[], required)
- `includedSources.hiTypes` (string[], required)
- `includedSources.purpose` (object, required)
- `includedSources.purpose.text` (string, required)
- `includedSources.purpose.code` (string, required)
- `includedSources.purpose.refUri` (string, required)
- `includedSources.hip` (null, required)
- `includedSources.period` (object, required)
- `includedSources.period.from` (string, required)
- `includedSources.period.to` (string, required)
- `excludedSources` (null, required)

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "autoApprovalId": "<AUTO_APPROVAL_ID>",
  "message": "<MESSAGE>",
  "supportedHITypes": [
    "<SUPPORTED_HITYPES>"
  ]
}
```
