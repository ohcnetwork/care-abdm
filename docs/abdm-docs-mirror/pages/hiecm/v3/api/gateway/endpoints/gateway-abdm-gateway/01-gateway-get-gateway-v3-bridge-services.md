# Fetch the service ids registered against a bridge

`GET /api/hiecm/gateway/v3/bridge-services`

Retrieve the unique identifiers, known as service IDs, that are associated with a specific bridge. In this context, a bridge acts as an intermediary component that connects various services or networks, enabling them to communicate with each other. When you call this API, it queries the bridge to gather a list of all the service IDs that have been registered with it.

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/bridge-services \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx'
```

## Authorization

- `Authorization` (bearer token, required): The access token from POST /api/hiecm/gateway/v3/sessions.

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended

## Responses

- `200`: OK
- `204`: No Content
- `400`: Bad Request
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden. The caller is authenticated but is not permitted to perform this operation on this resource.
- `500`: Internal Server Error
- `503`: Service Unavailable

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "bridge": {
    "id": "Bridge_ABC",
    "name": "ABC Bridge",
    "url": "https://abc.def.in",
    "active": true,
    "blocklisted": false
  },
  "services": [
    {
      "id": "ABC_Service",
      "name": "Service ABC",
      "types": [
        "HIP"
      ],
      "endpoints": {
        "hipEndpoints": [
          {
            "use": "registration",
            "connectionType": "HTTPS",
            "address": "https://abc.com/register"
          }
        ],
        "hiuEndpoints": [
          {
            "use": "registration",
            "connectionType": "HTTPS",
            "address": "https://abc.com/register"
          }
        ],
        "healthLockerEndpoints": [
          {
            "use": "registration",
            "connectionType": "HTTPS",
            "address": "https://abc.com/register"
          }
        ]
      },
      "active": true
    }
  ]
}
```
