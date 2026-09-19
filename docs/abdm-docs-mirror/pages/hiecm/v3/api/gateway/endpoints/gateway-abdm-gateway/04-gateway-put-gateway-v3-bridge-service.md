# Update the bridge service

`PUT /api/hiecm/gateway/v3/bridge-service`

```bash
curl --request PUT \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/bridge-service \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'Content-Type: application/json' \
  --data '{
  "bridgeId": "{{bridgeId}}",
  "serviceId": "{{serviceId}}",
  "name": "TEST Gateway",
  "isHip": true,
  "isHiu": true,
  "isHealthLocker": null,
  "isPhr": false,
  "endpoints": {},
  "attributes": null,
  "active": true
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from POST /api/hiecm/gateway/v3/sessions.

## Headers

- `REQUEST-ID` (string, required): Unique UUID for each request.
- `TIMESTAMP` (string, required): Request timestamp in UTC, ISO-8601 with Z.
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended

## Body

- `bridgeId` (string)
- `serviceId` (string)
- `name` (string)
- `isHip` (boolean)
- `isHiu` (boolean)
- `isHealthLocker` (object)
- `isPhr` (boolean)
- `endpoints` (object)
- `attributes` (object)
- `active` (boolean)

## Responses

- `default`: No response was saved in the Postman collection and no documented definition exists.
