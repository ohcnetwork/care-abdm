# Create an ABHA from an identity document

`POST /v3/enrollment/enrol/byDocument`

The route for somebody who cannot complete Aadhaar authentication. A
driving licence is one accepted document. The account created this way is
restricted until it is upgraded through Aadhaar KYC, so tell the person
that rather than letting them discover it later.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/byDocument \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "<TXN_ID>",
  "documentType": "DRIVING_LICENCE",
  "documentId": "DL0820****858",
  "firstName": "<FIRST_NAME>",
  "middleName": "<MIDDLE_NAME>",
  "lastName": "<LAST_NAME>",
  "dob": "<DATE_OF_BIRTH>",
  "gender": "M",
  "frontSidePhoto": "<ENCRYPTED_VALUE>",
  "backSidePhoto": "<ENCRYPTED_VALUE>",
  "address": "<ADDRESS>",
  "state": "<STATE>",
  "district": "<DISTRICT>",
  "pinCode": "<PIN_CODE>",
  "consent": {
    "code": "abha-enrollment",
    "version": "1.4"
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.

## Body

- `txnId` (string, required)
- `documentType` (string, required)
- `documentId` (string, required)
- `firstName` (string, required)
- `middleName` (string, required)
- `lastName` (string, required)
- `dob` (string, required)
- `gender` (string, required)
- `frontSidePhoto` (string, required)
- `backSidePhoto` (string, required)
- `address` (string, required)
- `state` (string, required)
- `district` (string, required)
- `pinCode` (string, required)
- `consent` (object, required)
- `consent.code` (string, required)
- `consent.version` (string, required)

## Responses

- `200`: The specification does not describe this body. Send the call with Try it to see what comes back.
- `400`: Bad Request, invalid scope, loginHint, or encrypted field
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: Unauthorized, missing, invalid, or expired Bearer token
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden, the token is valid but not permitted for this operation
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `422`: Unprocessable, the request parsed but failed validation
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `500`: Server error, retry
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
