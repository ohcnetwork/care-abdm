# Notify subscription requests HIU

`POST /api/v3/hiu/subscription-requests/hiu/notify`

**Hosted by the HIP/HIU, not by ABDM.** ABDM calls this endpoint at the callback URL registered for your bridge, so the path below is relative to that URL.
This API endpoint serves as a callback for when a subscription request is approved or denied. By invoking this API, the Health Information User (HIU) is notified about the outcome of their subscription request, whether it has been approved or denied. This functionality is essential for maintaining transparency and ensuring that the HIU is informed about the status of their subscription requests.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/v3/hiu/subscription-requests/hiu/notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "notification": {
    "subscriptionRequestId": "f29f0e59-8388-4698-9fe6-05db67aeac46",
    "reason": "reason",
    "status": "GRANTED",
    "subscription": {
      "id": "f29f0e59-8388-4698-9fe6-05db67aeac46",
      "patient": {
        "id": "<ABHA_ADDRESS>"
      },
      "hiu": {
        "id": "INDIA_HIU",
        "name": "INDIA HIU",
        "type": "HIU"
      },
      "sources": [
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
  }
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-HIU-ID` (string, required): Identifier of the health information user to which the request was intended

## Body

- `notification` (object, required)
- `notification.subscriptionRequestId` (string, required): subscriptionRequestId .Allows alpha numeric character and special characters like [A-Z a-z 0-9]+[A-Z a-z 0-9 //_//-]*[A-Z a-z 0-9]$
- `notification.reason` (string, required)
- `notification.status` (string, required) One of: GRANTED, DENIED.
- `notification.subscription` (object, required)
- `notification.subscription.id` (string)
- `notification.subscription.patient` (object)
- `notification.subscription.patient.id` (string, required): The abha address of the patient. Must start with Alphanumeric . and  _  in the middle and must be ending with @abdm or @sbx.Allows alpha numeric character and special characters like ^[a-zA-Z0-9][a-zA-Z0-9_.\\-!]+[a-zA-Z0-9]@(abdm|sbx)$
- `notification.subscription.hiu` (object)
- `notification.subscription.hiu.id` (string, required): The service ID of the health information user. Allows alpha numeric character and special characters like [A-Z a-z 0-9]+[A-Z a-z 0-9 //_//-]*[A-Z a-z 0-9]$
- `notification.subscription.hiu.name` (string): The name of the health information user. Allows alpha numeric and special characters like ^[a-zA-Z]+[A-Za-z0-9_\\-@,().\\s\\xa0:/]+
- `notification.subscription.hiu.type` (string): The type of the health information user.  Allows alpha numeric and special characters like ^[a-zA-Z0-9_\\-@,. \":/]{0,255}$
- `notification.subscription.sources` (object[])
- `notification.subscription.sources.hiTypes` (string[], required): Types of health information document.
- `notification.subscription.sources.purpose` (object, required)
- `notification.subscription.sources.hip` (object, required): Identifier and name of the health information provider.
- `notification.subscription.sources.categories` (string[], required)
- `notification.subscription.sources.period` (object, required): The date range between when the subscription will be active
- `notification.subscription.sources.status` (string): The status of the subscription approval. Allows alpha numeric character and special characters like ^[a-zA-Z0-9_\-@,. ":]{0,255}$

## Responses

- `200`: OK
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/subscription/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/subscription/errors
- `404`: server cannot find the requested resource
  See Error codes for this module: /docs/hiecm/v3/api/subscription/errors
- `500`: Internal Server Error -> It is just one example, for every api the path will be changed.
  See Error codes for this module: /docs/hiecm/v3/api/subscription/errors
- `503`: Service Unavailable
  See Error codes for this module: /docs/hiecm/v3/api/subscription/errors
