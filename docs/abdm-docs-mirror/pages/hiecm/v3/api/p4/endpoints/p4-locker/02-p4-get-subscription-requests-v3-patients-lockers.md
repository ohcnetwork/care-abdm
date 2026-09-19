# Get the subscription requests patients lockers

`GET /api/hiecm/subscription-requests/v3/patients/lockers`

Retrieve a list of health lockers associated with a given ABHA address. It includes both active and inactive subscriptions based on the `includeInactive` parameter.

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/subscription-requests/v3/patients/lockers \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-AUTH-TOKEN: <TOKEN>'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for tracking the end-to-end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds, and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended
- `X-AUTH-TOKEN` (string, required): JWT Authentication token issued by ABDM after successful validation of username and password

## Query parameters

- `includeInactive` (string, required): Indicates whether to include inactive records

## Responses

- `200`: OK
- `400`: Bad Request. The request could not be processed because it was malformed or failed validation - a missing mandatory field, a value in the wrong format, or a header that did not match the body.
- `401`: Unauthorized. The request carried no valid credentials, or the access token has expired. Obtain a fresh token from the session API and retry.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden. The caller is authenticated but is not permitted to perform this operation on this resource.

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "id": 212,
    "lockerId": "HIU_V3",
    "lockerName": "HIU_V3",
    "patientId": "<ABHA_ADDRESS>",
    "dateCreated": "2024-03-15T01:49:16.316Z",
    "dateModified": "2024-03-120T01:49:16.316Z",
    "isActive": true
  }
]
```
