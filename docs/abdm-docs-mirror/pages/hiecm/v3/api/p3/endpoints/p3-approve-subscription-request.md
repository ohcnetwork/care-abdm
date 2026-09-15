# Approve Subscription Request

`POST /api/consent-management/subscription-requests/{subscriptionRequestId}/approve`

Approves a subscription request for the sources included and not the ones excluded, or for every HIP.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/consent-management/subscription-requests/{subscriptionRequestId}/approve \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "isApplicableForAllHIPs": true,
  "includedSources": [
    {
      "hiTypes": [
        "Invoice",
        "HealthDocumentRecord"
      ],
      "purpose": {
        "text": "Care Management",
        "code": "CAREMGT",
        "refUri": "www.abdm.gov.in"
      },
      "categories": [
        "LINK",
        "DATA"
      ],
      "period": {
        "from": "2025-05-22T13:12:55.297Z",
        "to": "2125-05-22T13:11:55.300Z"
      }
    }
  ],
  "excludedSources": []
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Path parameters

- `subscriptionRequestId` (string, required): Passed as a path segment.

## Body

- `isApplicableForAllHIPs` (boolean, required)
- `includedSources` (object[], required)
- `includedSources.hiTypes` (string[], required)
- `includedSources.purpose` (object, required)
- `includedSources.purpose.text` (string, required)
- `includedSources.purpose.code` (string, required)
- `includedSources.purpose.refUri` (string, required)
- `includedSources.categories` (string[], required)
- `includedSources.period` (object, required)
- `includedSources.period.from` (string, required)
- `includedSources.period.to` (string, required)
- `excludedSources` (object[], required)

## Responses

- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors
