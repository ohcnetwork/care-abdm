# Initiate subscription request

`POST /api/hiecm/subscription-requests/v3/init`

Be invoked by Health Information Users (HIUs), patients, or users through the Personal Health Record (PHR) application to initiate a subscription request. By using this API, individuals can start the process of subscribing to specific health information services or updates. This functionality is essential for enabling users to manage their health data subscriptions effectively, ensuring they receive timely and relevant health information.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/subscription-requests/v3/init \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "subscription": {
    "purpose": {
      "text": "Care Management",
      "code": "CAREMGT",
      "refUri": "https://abc.def.in"
    },
    "patient": {
      "id": "<ABHA_ADDRESS>"
    },
    "hiu": {
      "id": "INDIA_HIU",
      "name": "INDIA HIU",
      "type": "HIU"
    },
    "hips": [
      {
        "id": "INDIA_HIP",
        "name": "INDIA HIP",
        "type": "HIP"
      }
    ],
    "categories": [
      "LINK"
    ],
    "period": {
      "from": "2024-05-09T10:34:00.389Z",
      "to": "2024-05-09T10:34:00.389Z"
    }
  }
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended

## Body

- `subscription` (object, required)
- `subscription.purpose` (object, required)
- `subscription.purpose.text` (string, required) One of: Care Management, Break the Glass, Public Health, Healthcare Payment, Disease Specific Healthcare Research, Self Requested.
- `subscription.purpose.code` (string, required) One of: CAREMGT, BTG, PUBHLTH, HPAYMT, DSRCH, PATRQT.
- `subscription.purpose.refUri` (string, required): The reference URL.Allows alpha numeric character and special characters like  "^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&//=]*)$"
- `subscription.patient` (object, required)
- `subscription.patient.id` (string, required): The abha address of the patient. Must start with Alphanumeric . and  _  in the middle and must be ending with @abdm or @sbx. Allows alpha numeric character and special characters like ^[a-zA-Z0-9][a-zA-Z0-9_.\\-!]+[a-zA-Z0-9]@(abdm|sbx)$
- `subscription.hiu` (object, required)
- `subscription.hiu.id` (string, required): The service ID of the health information user. Allows alpha numeric character and special characters like [A-Z a-z 0-9]+[A-Z a-z 0-9 //_//-]*[A-Z a-z 0-9]$
- `subscription.hiu.name` (string): The name of the health information user. Allows alphanumeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \":]{0,255}$"
- `subscription.hiu.type` (string): The type of the health information user. Allows alphanumeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \":]{0,255}$"
- `subscription.hips` (object[], required)
- `subscription.hips.id` (string, required): The service ID of the health information provider. Allows alpha numeric character and special characters like [A-Z a-z 0-9]+[A-Z a-z 0-9 //_//-]*[A-Z a-z 0-9]$
- `subscription.hips.name` (string): The name of the health information provider. Allows alphanumeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \":]{0,255}$"
- `subscription.hips.type` (string): The type of the health information provider. Allows alphanumeric characters and special characters like "^[a-zA-Z0-9_\\-@,. \":]{0,255}$"
- `subscription.categories` (object[], required)
- `subscription.period` (object, required): The date range between when the subscription will be active
- `subscription.period.from` (string, required): UTC date time in ISO format. Allows alpha numeric character and special characters like "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$"
- `subscription.period.to` (string, required): UTC date time in ISO format.Allows alpha numeric character and special characters like "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$"

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/subscription/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/subscription/errors
- `404`: server cannot find the requested resource
  See Error codes for this module: /docs/hiecm/v3/api/subscription/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/subscription/errors
- `503`: Internal Server Error -> It is just one example, for every api the path will be changed.
  See Error codes for this module: /docs/hiecm/v3/api/subscription/errors
