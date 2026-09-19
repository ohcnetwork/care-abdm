# Update the bridge URL

`PATCH /api/hiecm/gateway/v3/bridge/url`

Update the URL of a bridge. When invoked, it allows users to modify the existing URL associated with a specific bridge. This functionality is crucial for maintaining accurate and up-to-date connection information within the network. By using this API, administrators can ensure that the bridge URL reflects the current configuration and routing requirements, facilitating seamless communication and integration between different services in the form of webhook site.

```bash
curl --request PATCH \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/bridge/url \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "url": "<YOUR_CALLBACK_URL>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from POST /api/hiecm/gateway/v3/sessions.

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended

## Body

- `url` (string, required): The bridge URL to be updated

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `204`: No Content
- `400`: Bad Request
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden. The caller is authenticated but is not permitted to perform this operation on this resource.
- `500`: Internal Server Error
- `503`: Service Unavailable

Shape of the 204 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "error": {
    "code": "ABDM-1001",
    "message": "No data found"
  }
}
```
