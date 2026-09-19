# Edit the subscription details

`PUT /api/hiecm/subscription-requests/v3/patients/{subscription-id}`

Edit the details of an existing subscription. By invoking this API, users can update the parameters and preferences associated with a specific subscription identified by the subscription ID.

```bash
curl --request PUT \
  --url https://dev.abdm.gov.in/api/hiecm/subscription-requests/v3/patients/{subscription-id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-AUTH-TOKEN: <TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hiuId": "INDIA_HIU",
  "subscriptionEditAndApprovalRequest": {
    "isApplicableForAllHIPs": true,
    "includedSources": [
      {
        "hiTypes": [
          "Prescription"
        ],
        "purpose": {
          "text": "Care Management",
          "code": "CAREMGT",
          "refUri": "https://abc.def.in"
        },
        "hip": {
          "id": "INDIA_HIP",
          "name": "INDIA HIP",
          "type": "HIP"
        },
        "categories": [
          "LINK"
        ],
        "period": {
          "from": "2024-05-09T10:34:00.389Z",
          "to": "2024-05-09T10:34:00.389Z"
        },
        "status": "SUCCESS"
      }
    ],
    "excludedSources": [
      {
        "hiTypes": [
          "Prescription"
        ],
        "purpose": {
          "text": "Care Management",
          "code": "CAREMGT",
          "refUri": "https://abc.def.in"
        },
        "hip": {
          "id": "INDIA_HIP",
          "name": "INDIA HIP",
          "type": "HIP"
        },
        "categories": [
          "LINK"
        ],
        "period": {
          "from": "2024-05-09T10:34:00.389Z",
          "to": "2024-05-09T10:34:00.389Z"
        },
        "status": "SUCCESS"
      }
    ]
  }
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended
- `X-AUTH-TOKEN` (string, required): JWT Authentication token which was issued by ABDM after successful validation of username and password

## Path parameters

- `subscription-id` (string, required): The subscription id

## Body

- `hiuId` (string, required): The service ID of the health information provider Allows alphanumeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \":]{0,255}$"
- `subscriptionEditAndApprovalRequest` (object, required)
- `subscriptionEditAndApprovalRequest.isApplicableForAllHIPs` (boolean, required): A boolean value to denote if the policy is applicable to all the HIPs or only the specified HIP
- `subscriptionEditAndApprovalRequest.includedSources` (object[], required): Included sources, carrying the list of hi types.
- `subscriptionEditAndApprovalRequest.includedSources.hiTypes` (string[], required): Types of health information document.
- `subscriptionEditAndApprovalRequest.includedSources.purpose` (object, required)
- `subscriptionEditAndApprovalRequest.includedSources.purpose.text` (string, required) One of: Care Management, Break the Glass, Public Health, Healthcare Payment, Disease Specific Healthcare Research, Self Requested.
- `subscriptionEditAndApprovalRequest.includedSources.purpose.code` (string, required) One of: CAREMGT, BTG, PUBHLTH, HPAYMT, DSRCH, PATRQT.
- `subscriptionEditAndApprovalRequest.includedSources.purpose.refUri` (string, required): The reference URL.Allows alpha numeric character and special characters like "^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&//=]*)$"
- `subscriptionEditAndApprovalRequest.includedSources.hip` (object, required): Identifier and name of the health information provider.
- `subscriptionEditAndApprovalRequest.includedSources.hip.id` (string, required): The service ID of the health information provider. Allows alpha numeric character and special characters like [A-Z a-z 0-9]+[A-Z a-z 0-9 //_//-]*[A-Z a-z 0-9]$
- `subscriptionEditAndApprovalRequest.includedSources.hip.name` (string, required): The name of the health information provider. Allows alphanumeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \":]{0,255}$"
- `subscriptionEditAndApprovalRequest.includedSources.hip.type` (string): The type of the health information provider. Allows alphanumeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \":]{0,255}$"
- `subscriptionEditAndApprovalRequest.includedSources.categories` (string[], required)
- `subscriptionEditAndApprovalRequest.includedSources.period` (object, required): The date range between when the subscription will be active
- `subscriptionEditAndApprovalRequest.includedSources.period.from` (string, required): UTC date time in ISO format. Allows alpha numeric character and special characters like "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$"
- `subscriptionEditAndApprovalRequest.includedSources.period.to` (string, required): UTC date time in ISO format. Allows alpha numeric character and special characters like "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$"
- `subscriptionEditAndApprovalRequest.includedSources.status` (string, required): The status of the subscription approval
- `subscriptionEditAndApprovalRequest.excludedSources` (object[], required): Excluded sources, carrying the list of hi types.
- `subscriptionEditAndApprovalRequest.excludedSources.hiTypes` (string[], required): Types of health information document.
- `subscriptionEditAndApprovalRequest.excludedSources.purpose` (object, required)
- `subscriptionEditAndApprovalRequest.excludedSources.purpose.text` (string, required) One of: Care Management, Break the Glass, Public Health, Healthcare Payment, Disease Specific Healthcare Research, Self Requested.
- `subscriptionEditAndApprovalRequest.excludedSources.purpose.code` (string, required) One of: CAREMGT, BTG, PUBHLTH, HPAYMT, DSRCH, PATRQT.
- `subscriptionEditAndApprovalRequest.excludedSources.purpose.refUri` (string, required): The reference URL. Allows alpha numeric character and special characters like "^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&//=]*)$"
- `subscriptionEditAndApprovalRequest.excludedSources.hip` (object, required): Identifier and name of the health information provider.
- `subscriptionEditAndApprovalRequest.excludedSources.hip.id` (string, required): The service ID of the health information provider. Allows alpha numeric character and special characters like [A-Z a-z 0-9]+[A-Z a-z 0-9 //_//-]*[A-Z a-z 0-9]$
- `subscriptionEditAndApprovalRequest.excludedSources.hip.name` (string, required): The name of the health information provider. Allows alphanumeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \":]{0,255}$"
- `subscriptionEditAndApprovalRequest.excludedSources.hip.type` (string): The type of the health information provider. Allows alphanumeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \":]{0,255}$"
- `subscriptionEditAndApprovalRequest.excludedSources.categories` (string[], required)
- `subscriptionEditAndApprovalRequest.excludedSources.period` (object, required): The date range between when the subscription will be active
- `subscriptionEditAndApprovalRequest.excludedSources.period.from` (string, required): UTC date time in ISO format.Allows alpha numeric character and special characters like "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$"
- `subscriptionEditAndApprovalRequest.excludedSources.period.to` (string, required): UTC date time in ISO format.Allows alpha numeric character and special characters like "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$"
- `subscriptionEditAndApprovalRequest.excludedSources.status` (string, required): The status of the subscription approval

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad Request
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
- `404`: server cannot find the requested resource
- `500`: Internal Server Error -> It is just one example, for every api the path will be changed.
- `503`: Service Unavailable

Shape of the 202 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "subscriptionId": "f29f0e59-8388-4698-9fe6-05db67aeac46",
  "message": "Successfully approved Subscription request"
}
```
