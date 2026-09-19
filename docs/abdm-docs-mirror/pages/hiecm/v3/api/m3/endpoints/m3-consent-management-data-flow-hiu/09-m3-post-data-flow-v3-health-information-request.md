# Submit the health information data request from HIU

`POST /api/hiecm/data-flow/v3/health-information/request`

Facilitates the exchange of health data between Health Information Providers (HIP) and Health Information Users (HIU) within the ABDM system. It ensures secure and efficient data transfer, enabling seamless communication and interoperability between different healthcare entities.
1. **X-HIU-ID** if the requester is HIU (SERVICE-ID).

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/data-flow/v3/health-information/request \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-HIU-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "hiRequest": {
    "consent": {
      "id": "18235d89-cb13-479d-ad71-7a57d5f669a8"
    },
    "dateRange": {
      "from": "2022-10-06T15:10:00.587Z",
      "to": "2022-11-06T15:10:00.587Z"
    },
    "dataPushUrl": "https://live.ndhm.gov.in/api-hiu/data/notification",
    "keyMaterial": {
      "cryptoAlg": "ECDH",
      "curve": "curve25519",
      "dhPublicKey": {
        "expiry": "2022-12-28T13:18:20.742Z",
        "parameters": "Ephemeral public key",
        "keyValue": "BFN7KTdOT0jIAExG2A8Jg+01wMPWxptiGqwHRVvtiVEsUq2FR7P2UdqZxJyPJSeR6muai21iQhasNxnhh8I5M+g="
      },
      "nonce": "28236d89-cb13-479d-ad71-7a57d5f669a9"
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
- `X-HIU-ID` (string, required): Identifier of the health information user to which the request was intended

## Body

- `hiRequest` (object, required)
- `hiRequest.consent` (object, required)
- `hiRequest.consent.id` (string, required): The consent artefact id for health information request. Allows alpha numeric character and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `hiRequest.dateRange` (object, required): Health information created between this date range is requested
- `hiRequest.dateRange.from` (string, required): Should be a UTC date time in ISO Format.Allows alpha numeric character and special characters like ^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$
- `hiRequest.dateRange.to` (string, required): Should be a UTC date time in ISO Format.Allows alpha numeric character and special characters like ^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$
- `hiRequest.dataPushUrl` (string, required): The URL to which the Health Information Provider has to send the health information data. Allows alpha numeric character and special characters like "^[a-zA-Z0-9_\\-@,. \":=?/&]{0,255}$"
- `hiRequest.keyMaterial` (object, required): The key and algorithm details that is used to encrypt/decrypt the data
- `hiRequest.keyMaterial.cryptoAlg` (string, required): Allows alpha numeric character and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `hiRequest.keyMaterial.curve` (string, required): Allows alpha numeric character and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `hiRequest.keyMaterial.dhPublicKey` (object, required)
- `hiRequest.keyMaterial.dhPublicKey.expiry` (string, required): date and time format "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'"
- `hiRequest.keyMaterial.dhPublicKey.parameters` (string, required): Allows alpha numeric character and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `hiRequest.keyMaterial.dhPublicKey.keyValue` (string, required)
- `hiRequest.keyMaterial.nonce` (string)

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Access Denied
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `404`: Not Found
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
- `503`: Service Unavailable
  See Error codes for this module: /docs/hiecm/v3/api/m3/errors
