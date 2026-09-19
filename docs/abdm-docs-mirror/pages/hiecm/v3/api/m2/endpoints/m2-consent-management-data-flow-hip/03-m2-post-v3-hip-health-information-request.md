# Receive the health information data request to HIP

`POST /api/v3/hip/health-information/request`

**Hosted by the HIP/HIU, not by ABDM.** ABDM calls this endpoint at the callback URL registered for your bridge, so the path below is relative to that URL.
Callback API to provide Health information request of HIP. CM calls this API when it has validated the Health Information request given the consent ID.<br> Either the hiRequest or error would need to be specified. If the health info request was valid, then the hiRequest.transactionId specifies the transaction context against which HIP would send over the data.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/v3/hip/health-information/request \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-HIP-ID: IN2810014366' \
  --header 'Content-Type: application/json' \
  --data '{
  "transactionId": "49455d89-cb13-483d-ad71-7a57d5f669a8",
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
- `X-HIP-ID` (string, required): Identifier of the health information provider to which the request was intended

## Body

- `transactionId` (string, required)
- `hiRequest` (object, required)
- `hiRequest.consent` (object, required)
- `hiRequest.consent.id` (string, required): The consent artefact id for health information request. Allows alpha numeric character and special characters like "^[0-9a-fA-F]{8}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{4}\\b-[0-9a-fA-F]{12}$"
- `hiRequest.dateRange` (object, required): Health information created between this date range is requested
- `hiRequest.dateRange.from` (string, required): Should be a UTC date time in ISO Format. Allows alpha numeric character and special characters like \\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$
- `hiRequest.dateRange.to` (string, required): Should be a UTC date time in ISO Format.Allows alpha numeric character and special characters like \\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$
- `hiRequest.dataPushUrl` (string, required): The URL to which the Health Information Provider has to send the health information data. Allows alpha numeric character and special characters like ^[a-zA-Z0-9_\\-@,. \":/]{0,255}$
- `hiRequest.keyMaterial` (object, required): The key and algorithm details that is used to encrypt/decrypt the data
- `hiRequest.keyMaterial.cryptoAlg` (string, required): Allows alpha numeric character and special characters like ^[a-zA-Z0-9_\\-@,. \":/]{0,255}$
- `hiRequest.keyMaterial.curve` (string, required): Allows alpha numeric character and special characters like ^[a-zA-Z0-9_\\-@,. \":/]{0,255}$
- `hiRequest.keyMaterial.dhPublicKey` (object, required)
- `hiRequest.keyMaterial.dhPublicKey.expiry` (string, required): UTC.Allows alpha numeric character and special characters like "yyyy-MM-dd'T'HH:mm:ss.SSS'Z'"
- `hiRequest.keyMaterial.dhPublicKey.parameters` (string, required): Allows alpha numeric character and special characters like ^[a-zA-Z0-9_\-@,+#=. ":/]{0,255}$
- `hiRequest.keyMaterial.dhPublicKey.keyValue` (string, required)
- `hiRequest.keyMaterial.nonce` (string)

## Responses

- `200`: OK
- `400`: Bad Request. The request could not be processed because it was malformed or failed validation - a missing mandatory field, a value in the wrong format, or a header that did not match the body.
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `401`: Unauthorized. The request carried no valid credentials, or the access token has expired. Obtain a fresh token from the session API and retry.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden. The caller is authenticated but is not permitted to perform this operation on this resource.
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
- `404`: server cannot find the requested resource
  See Error codes for this module: /docs/hiecm/v3/api/m2/errors
