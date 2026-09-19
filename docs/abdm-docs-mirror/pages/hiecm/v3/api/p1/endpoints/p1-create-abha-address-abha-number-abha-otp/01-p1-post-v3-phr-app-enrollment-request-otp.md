# Request enrolment OTP

`POST /abha/api/v3/phr/app/enrollment/request/otp`

Flows in the Postman collection:
- P1-Registration-login › P1 - Create ABHA Address Flow › Enrolment via Mobile › OTP Request - Mobile
- P1-Registration-login › P1 - Create ABHA Address Flow › Enrolment via ABHA Number-ABHA OTP › OTP Request - ABHA OTP
- P1-Registration-login › P1 - Create ABHA Address Flow › Enrolment via ABHA Number-Aadhaar OTP › OTP Request - AADHAR OTP

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/app/enrollment/request/otp \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-login",
    "mobile-verify"
  ],
  "loginHint": "abha-number",
  "loginId": "{{encryptedData}}",
  "otpSystem": "abdm"
}'
```

## Headers

- `REQUEST-ID` (string, required): Unique UUID for each request.
- `TIMESTAMP` (string, required): Request timestamp in UTC, ISO-8601 with Z.

## Body

- `scope` (string[])
- `loginHint` (string)
- `loginId` (string)
- `otpSystem` (string)

## Responses

- `200`: OK
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "1bda575d-02pd-40be-77e6-1e3efca52a82",
  "message": "OTP is sent to Mobile number ending with ******2425"
}
```
