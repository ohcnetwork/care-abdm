# Notify HIU when consent is APPROVED, DENIED or REVOKED

`POST /api/v3/hiu/consent/request/notify`

**Hosted by the HIP/HIU, not by ABDM.** ABDM calls this endpoint at the callback URL registered for your bridge, so the path below is relative to that URL.
Health information user will get notified about the consent request granted or denied, consent revoked, consent expired.
For consent request grant, status=GRANTED, consentRequestId=<consent-REQUEST-ID>, and consentArtefacts is an array of generated consent artefact Ids. For consent request expiry, status=EXPIRED, consentRequestId=<consent-REQUEST-ID> For consent request denied, status=DENIED, consentRequestId=<consent-REQUEST-ID> For consent revocation, status=REVOKED, consentArtefacts is an array of revoked consent artefact ids.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/v3/hiu/consent/request/notify \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "notification": {
    "consentRequestId": "e3c74829-3f82-4f94-959e-e10f57bcd57b",
    "status": "GRANTED",
    "reason": null,
    "consentArtefacts": [
      {
        "id": "6f0b4665-a915-4c92-aa36-65afb4a2cd71"
      }
    ]
  }
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds.
- `X-HIU-ID` (string, required): Identifier of the health information user to which the request was intended

## Body

- `notification` (object, required)
- `notification.consentRequestId` (string, required): The consent request id from a consent. Allows alpha numeric character and special characters like "^[a-zA-Z0-9_\-@,. ":/]{0,255}$"
- `notification.status` (string, required) One of: GRANTED, EXPIRED, DENIED, REQUESTED, REVOKED.
- `notification.reason` (string, required)
- `notification.consentArtefacts` (object[], required): List of consent artefact ids that were created.
- `notification.consentArtefacts.id` (string, required)

## Responses

- `200`: OK
- `400`: Bad Request. The request could not be processed because it was malformed or failed validation - a missing mandatory field, a value in the wrong format, or a header that did not match the body.
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `404`: Not Found
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `503`: Service Unavailable
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
