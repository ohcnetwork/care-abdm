# Read the signed in person's ABHA profile

`GET /v3/profile/account`

Needs the `X-token` from login, because it reads one person's account
rather than anything about your application.

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/account \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'X-token: <X_TOKEN_FROM_LOGIN_VERIFY>'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.
- `X-token` (string, required): The user scoped token returned when a person logs in or verifies an OTP. Required on this operation. See the shared `XToken` parameter, and note that this header takes the bare token with no prefix.

## Responses

- `200`: The response.
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
  "ABHANumber": "<ABHANUMBER>",
  "preferredAbhaAddress": "<PREFERRED_ABHA_ADDRESS>",
  "mobile": "<MOBILE>",
  "firstName": "<FIRST_NAME>",
  "middleName": "<MIDDLE_NAME>",
  "lastName": "<LAST_NAME>",
  "name": "<NAME>",
  "yearOfBirth": "<YEAR_OF_BIRTH>",
  "dayOfBirth": "<DAY_OF_BIRTH>",
  "monthOfBirth": "<MONTH_OF_BIRTH>",
  "gender": "<GENDER>",
  "profilePhoto": "<PROFILE_PHOTO>",
  "status": "<STATUS>",
  "stateCode": "<STATE_CODE>",
  "districtCode": "<DISTRICT_CODE>",
  "pincode": "<PINCODE>",
  "address": "<ADDRESS>",
  "kycPhoto": "<KYC_PHOTO>",
  "stateName": "<STATE_NAME>",
  "districtName": "<DISTRICT_NAME>",
  "subdistrictName": "<SUBDISTRICT_NAME>",
  "authMethods": [
    "<AUTH_METHODS>"
  ],
  "kycVerified": false,
  "verificationStatus": "<VERIFICATION_STATUS>",
  "verificationType": "<VERIFICATION_TYPE>",
  "createdDate": "<CREATED_DATE>"
}
```
