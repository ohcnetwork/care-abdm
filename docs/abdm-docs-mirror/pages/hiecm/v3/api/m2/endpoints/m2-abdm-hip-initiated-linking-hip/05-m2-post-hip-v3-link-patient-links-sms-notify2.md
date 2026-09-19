# Send SMS notification to patient that a care context is linked

`POST /api/hiecm/hip/v3/link/patient/links/sms/notify2`

Send SMS notifications to patients, informing them that a care context has been successfully linked to their ABHA (Ayushman Bharat Health Account) address. By invoking this API, HIPs can ensure that patients are promptly notified about the linkage of their health records, enhancing transparency and patient engagement. This notification process is essential for keeping patients informed and involved in the management of their health information, thereby supporting a more connected and responsive healthcare system.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/hip/v3/link/patient/links/sms/notify2 \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "notification": {
    "phoneNo": "986543***",
    "hip": {
      "id": "ABDM_HIP",
      "name": "ABC Hospital"
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

- `notification` (object, required)
- `notification.phoneNo` (string, required): The mobile number to send SMS
- `notification.hip` (object, required): Identifier and name of the health information provider.
- `notification.hip.id` (string, required): The service ID of the health information provider
- `notification.hip.name` (string, required): The name of the health information provider

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `404`: server cannot find the requested resource
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
