# Fetch the list of providers filtered by name

`GET /api/hiecm/gateway/v3/providers`

Retrieve a list of providers, filtered by their names. When invoked, it queries the system to fetch providers that match the specified name criteria. This functionality is particularly useful for narrowing down provider options based on specific naming conventions or patterns. By using this API, users can efficiently locate and manage providers within the network, ensuring they have access to the relevant provider information needed for various operational tasks.

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/providers \
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

## Query parameters

- `name` (string): Name of the provider

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
[
  {
    "identifier": {
      "name": "AB - PMJAY",
      "id": "PMJAY"
    },
    "facilityType": [
      "HIP"
    ],
    "isHIP": true,
    "isHiu": false,
    "isHealthLocker": true,
    "isPhr": true,
    "isGovtEntity": false,
    "endpoints": {
      "healthLockerEndpoints": [
        {
          "use": "registration",
          "connectionType": "HTTPS",
          "address": "https://abc.com/register"
        }
      ]
    }
  }
]
```
