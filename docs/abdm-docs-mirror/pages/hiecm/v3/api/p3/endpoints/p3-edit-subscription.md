# Edit Subscription

`PUT /api/consent-management/patients/subscription-requests/{subscriptionId}`

Edits a subscription and approves it in the same step, changing which HIPs and categories the HIU is subscribed to.

```bash
curl --request PUT \
  --url https://phrsbx.abdm.gov.in/api/consent-management/patients/subscription-requests/{subscriptionId} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hiuId": "<HIU_ID>",
  "subscriptionEditAndApprovalRequest": {
    "isApplicableForAllHIPs": true,
    "includedSources": [
      {
        "hiTypes": [
          "DiagnosticReport",
          "Prescription",
          "ImmunizationRecord",
          "DischargeSummary",
          "OPConsultation",
          "HealthDocumentRecord",
          "WellnessRecord"
        ],
        "purpose": {
          "text": "Care Management",
          "code": "CAREMGT",
          "refUri": "www.abdm.gov.in"
        },
        "categories": [
          "DATA",
          "LINK"
        ],
        "period": {
          "from": "2024-01-09T09:00:00.000Z",
          "to": "2123-12-31T09:00:00.000Z"
        }
      }
    ],
    "excludedSources": []
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Path parameters

- `subscriptionId` (string, required): Passed as a path segment.

## Body

- `hiuId` (string, required)
- `subscriptionEditAndApprovalRequest` (object, required)
- `subscriptionEditAndApprovalRequest.isApplicableForAllHIPs` (boolean, required)
- `subscriptionEditAndApprovalRequest.includedSources` (object[], required)
- `subscriptionEditAndApprovalRequest.includedSources.hiTypes` (string[], required)
- `subscriptionEditAndApprovalRequest.includedSources.purpose` (object, required)
- `subscriptionEditAndApprovalRequest.includedSources.purpose.text` (string, required)
- `subscriptionEditAndApprovalRequest.includedSources.purpose.code` (string, required)
- `subscriptionEditAndApprovalRequest.includedSources.purpose.refUri` (string, required)
- `subscriptionEditAndApprovalRequest.includedSources.categories` (string[], required)
- `subscriptionEditAndApprovalRequest.includedSources.period` (object, required)
- `subscriptionEditAndApprovalRequest.includedSources.period.from` (string, required)
- `subscriptionEditAndApprovalRequest.includedSources.period.to` (string, required)
- `subscriptionEditAndApprovalRequest.excludedSources` (object[], required)

## Responses

- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors
