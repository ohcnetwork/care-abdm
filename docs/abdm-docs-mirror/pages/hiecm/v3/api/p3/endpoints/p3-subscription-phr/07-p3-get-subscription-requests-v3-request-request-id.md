# Fetch his/her subscription details by subscription REQUEST-ID

`GET /api/hiecm/subscription-requests/v3/request/{request-id}`

Be invoked by the patient or user through the Personal Health Record (PHR) application to fetch their subscription details using the subscription REQUEST-ID. By using this API, individuals can retrieve comprehensive information about a specific subscription request, including its status, scope, and any associated conditions. This functionality is essential for enabling users to manage their health data subscriptions effectively, ensuring they have access to accurate and up-to-date subscription information.

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/subscription-requests/v3/request/{request-id} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-AUTH-TOKEN: <TOKEN>'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended
- `X-AUTH-TOKEN` (string, required): JWT Authentication token which was issued by ABDM after successful validation of username and password

## Path parameters

- `request-id` (string, required): The subscription request id

## Responses

- `200`: OK
- `400`: Bad Request
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
- `404`: server cannot find the requested resource
- `500`: Internal Server Error -> It is just one example, for every api the path will be changed.
- `503`: Service Unavailable

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "id": 1234,
  "requestId": "ab1f0e59-8388-4698-9fe6-05db67aeac46",
  "subscriptionId": "c12f0e59-8388-4698-9fe6-05db67aea3c4",
  "patientId": "<ABHA_ADDRESS>",
  "requesterType": "phr",
  "status": "GRANTED",
  "details": {
    "subscriptionRequestId": "38d8dbfc-9ea6-4f9f-b807-b00d2b885a54",
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
  },
  "dateCreated": "2022-10-06T10:10:00.587Z",
  "dateModified": "2022-10-06T10:10:00.587Z",
  "healthIdNumber": "<ABHA_NUMBER>"
}
```
