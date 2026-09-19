# Search ABHA profile using ABHA address

`POST /abha/api/v3/phr/web/login/abha/search`

Search for ABHA (Ayushman Bharat Health Account) profiles. It allows users to retrieve information about their ABHA profiles using identifier ABHA address. This is essential for verifying the user’s identity and ensuring secure access to their ABHA profile <br>

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/phr/web/login/abha/search \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaAddress": "<ABHA_ADDRESS>"
}'
```

## Headers

- `REQUEST-ID` (string, required)
- `TIMESTAMP` (string, required)

## Body

- `abhaAddress` (string, required)

## Responses

- `200`: The 200 response code indicates a successful request. In this context, it refers to the successful retrieve of user details based on the ABHA address<br>
- `400`: The 400 response code signifies a bad request. In this context, it means that no user was found for the provided ABHA address.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: A 401 Unauthorized error occurs when a server receives a request without valid authentication credentials or with incorrect credentials. This error indicates that the server cannot authenticate the user,
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `404`: A 404 Not Found error occurs when a server cannot find the requested resource. This error indicates that the server is reachable, but the specific page or resource is not available
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `500`: <b>Internal Server Error</b><br><br>  An Internal Server Error (500) indicates that the server encountered an unexpected condition that prevented it from fulfilling the request.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "healthIdNumber": "<ABHA_NUMBER>",
  "abhaAddress": "<ABHA_ADDRESS>",
  "authMethods": [
    "MOBILE_OTP",
    "AADHAAR_OTP"
  ],
  "blockedAuthMethods": [],
  "status": "ACTIVE",
  "message": null,
  "fullName": "<NAME>",
  "mobile": "9340******"
}
```
