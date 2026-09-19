# Generate Keycloak token/access token

`POST /api/hiecm/gateway/v3/sessions`

Generate an access token. When invoked, it facilitates the authentication process by providing a secure token that can be used to access various services and resources within the system. This functionality is essential for ensuring secure and authorised access, enabling users to interact with protected endpoints and perform operations that require authentication. By using this API, users can obtain the necessary tokens to maintain secure sessions and access the system’s features effectively.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/sessions \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "clientId": "SBX_0000",
  "clientSecret": "0******-***-***-***-a****",
  "grantType": "client_credentials"
}'
```

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended

## Body

- `clientId` (string, required): Mandatory when the clientId.
- `clientSecret` (string, required): Mandatory when the clientSecret.
- `grantType` (string, required): The method used by the client to obtain an access token, e.g. client_credentials.

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `204`: No Content
- `400`: Bad Request
- `401`: Unauthorized. The request carried no valid credentials, or the access token has expired. Obtain a fresh token from the session API and retry.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden. The caller is authenticated but is not permitted to perform this operation on this resource.
- `500`: Internal Server Error
- `503`: Service Unavailable

Shape of the 202 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "accessToken": "<TOKEN>",
  "expiresIn": 1200,
  "refreshExpiresIn": 1800,
  "refreshToken": "<TOKEN>",
  "tokenType": "bearer"
}
```
