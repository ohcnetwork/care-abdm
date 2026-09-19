# Deny subscription request

`POST /api/hiecm/subscription-requests/v3/{request-id}/deny`

Be invoked by the patient or user through the Personal Health Record (PHR) application to deny a subscription request. By using this API, individuals can reject the requested subscription, ensuring that they do not receive unwanted health information services or updates. This functionality is essential for enabling users to manage their health data subscriptions effectively, maintaining control over the information they receive. The API supports secure and efficient denial of subscription requests, enhancing the overall user experience within the healthcare ecosystem.

```bash
curl --request POST \
  --url https://dev.abdm.gov.in/api/hiecm/subscription-requests/v3/{request-id}/deny \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-AUTH-TOKEN: <TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '{
  "reason": "Subscription denied."
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended
- `X-AUTH-TOKEN` (string, required): JWT Authentication token which was issued by ABDM after successful validation of username and password

## Path parameters

- `request-id` (string, required): The subscription request id

## Body

- `reason` (string, required): Reason for denying subscription request. Allows alpha numeric character and special characters like "^[A-Za-z .,]{1,50}$"

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad Request
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
- `404`: server cannot find the requested resource
- `500`: Internal Server Error -> It is just one example, for every api the path will be changed.
- `503`: Service Unavailable

Shape of the 202 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "message": "Successfully denied Subscription request"
}
```
