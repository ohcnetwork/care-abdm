# Enrol auth init

`POST /abha/api/v3/enrollment/enrol/auth/init`

Help to generate transaction ID. This transaction ID will be used for whole face authentication process. <br><br> The user can submit this transaction ID to the <strong>ABHA</strong> app using either intent-based sharing or by generating a QR code. <br><br>User can use this transaction ID to generate QR code using any QR generator tool. Open ABHA app and scan this QR code on ABHA App to start and complete the face capture process.<br><br>The data format of the QR code should follow this pattern: <br>https://<PHR-env-base-URL>/face-auth?txnId=<txn-ID-from-the-response-of-init-API>. <br><br><strong>For example:</strong> https://phrsbx.ABDM.gov.in/face-auth?txnId=bac7251b-cd25-44d5-9707-f3d2ba181c1c <br><br> For Sandbox- PHR-env-base-URL - https://phrsbx.ABDM.gov.in<br> For Production - PHR-env-base-URL - https://phr.ABDM.gov.in

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/auth/init \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-enrol",
    "face-auth"
  ]
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required)
- `TIMESTAMP` (string, required)

## Body

- `scope` (string[], required)

## Responses

- `200`: The 200 response code indicates a successful request. In this context, it refers to the successful generation of Transaction Id.
- `400`: The 400 response code indicates a bad request.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: The 401 response code indicates an unauthorized request. In this context, it refers to the lack of proper authentication during the operation of the Invalid Credentials
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: <b>Internal Server Error</b><br><br>  An Internal Server Error (500) indicates that the server encountered an unexpected condition that prevented it from fulfilling the request.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "23acf181-339d-4771-b532-5c5df4a28d19",
  "message": "Transaction Id generated Successfully"
}
```
