# Update fields on an ABHA profile

`PATCH /v3/profile/account`

Changes self declared profile details. Changing a mobile number or an
email address is not done here: those need the OTP pair below, because
NHA verifies the new value before accepting it.

```bash
curl --request PATCH \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'BENEFIT_NAME: healthid api' \
  --header 'X-token: <X_TOKEN_FROM_LOGIN_VERIFY>' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaNumber": "<ABHA_NUMBER>",
  "name": "<NAME>",
  "dob": "<DATE_OF_BIRTH>",
  "gender": "M"
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.
- `BENEFIT_NAME` (string): The benefit scheme an enrolment belongs to. Send `healthid api` on the enrol and search calls, and `healthid` on the login OTP and verify calls under Find ABHA. On the enrolment OTP request the header is present but explicitly disabled, so it is not sent there. A login OTP request sent with `healthid api` rather than `healthid` was accepted on the sandbox on 2026-09-11, so the login calls may take either. NHA's files spell this header four different ways and use scheme values beyond healthid. Which spelling each endpoint accepts is not confirmed against the sandbox. The Conventions page for this module lists all four.
- `X-token` (string): The user scoped token returned when a person logs in or verifies an OTP. Profile calls act on one account, so they need this in addition to the gateway token. Required on the calls that read or change a specific person's account. Send the bare token. Unlike the Authorization header this one carries no `Bearer ` prefix, and adding one is refused as `ABDM-1094` with the message `X-token expired`. That message names the wrong thing: a token rejected one second after it was issued has not expired, it was malformed. Check the prefix before the lifetime.

## Body

- `abhaNumber` (string)
- `name` (string)
- `dob` (string)
- `gender` (string)
- `profilePhoto` (string)
- `mobile` (string)
- `accountStatus` (string)

## Responses

- `200`: The ABHA profile as held by NHA.
- `400`: Bad Request, invalid scope, loginHint, or encrypted field
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: Unauthorized, missing, invalid, or expired Bearer token
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden, the token is valid but not permitted for this operation
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `500`: Server error, retry
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "ABHANumber": "<ABHA_NUMBER>",
  "preferredAbhaAddress": "<ABHA_ADDRESS>",
  "mobile": "<MOBILE>",
  "firstName": "<FIRST_NAME>",
  "middleName": "<MIDDLE_NAME>",
  "lastName": "<LAST_NAME>",
  "name": "<NAME>",
  "yearOfBirth": 1999,
  "dayOfBirth": 26,
  "monthOfBirth": 6,
  "gender": "M",
  "email": "<EMAIL>",
  "profilePhoto": "<BASE64_PHOTO>",
  "status": "ACTIVE",
  "stateCode": 32,
  "districtCode": 563,
  "subDistrictCode": null,
  "villageCode": null,
  "townCode": null,
  "wardCode": null,
  "pincode": "<PIN_CODE>",
  "address": "<ADDRESS>",
  "kycPhoto": "<BASE64_PHOTO>",
  "stateName": "<STATE>",
  "districtName": "<DISTRICT>",
  "subdistrictName": "<SUB_DISTRICT>",
  "villageName": null,
  "townName": null,
  "wardName": null,
  "authMethods": [
    "EMAIL_OTP",
    "MOBILE_OTP"
  ],
  "tags": {},
  "kycVerified": true,
  "verificationStatus": "VERIFIED",
  "verificationType": "DRIVING_LICENCE",
  "emailVerified": "<EMAIL>"
}
```
