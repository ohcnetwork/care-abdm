# Fetch his/her subscription requests details

`GET /api/hiecm/subscription-requests/v3/requests`

Be invoked by the patient or user through the Personal Health Record (PHR) application to fetch details of their subscription requests. By using this API, patients can retrieve comprehensive information about all their subscription requests, including the status and specifics of each request. This functionality is essential for maintaining transparency and enabling patients to manage their subscriptions effectively. The API supports secure and efficient access to subscription data, enhancing the overall user experience within the healthcare ecosystem.

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/subscription-requests/v3/requests \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-AUTH-TOKEN: <TOKEN>'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended
- `X-AUTH-TOKEN` (string, required): JWT Authentication token which was issued by ABDM after successful validation of username and password

## Query parameters

- `limit` (integer): How many items to return at one time
- `offset` (integer): How many items out of line
- `status` (string): Query string parameter restricts the data returned from your request

## Responses

- `200`: OK
- `400`: Bad Request
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
- `404`: server cannot find the requested resource
- `500`: Internal Server Error -> It is just one example, for every api the path will be changed.
- `503`: Service Unavailable

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "size": 0,
  "limit": 5,
  "offset": 5,
  "requests": [
    {
      "subscriptionId": "f29f0e59-8388-4698-9fe6-05db67aeac46",
      "requestId": "f29f0e59-8388-4698-9fe6-05db67aeac46",
      "createdAt": "2024-05-09T10:34:00.389Z",
      "lastUpdated": "2024-05-09T10:34:00.389Z",
      "purpose": {
        "text": "Care Management",
        "code": "CAREMGT",
        "refUri": "https://abc.def.in"
      },
      "patient": {
        "id": "<ABHA_ADDRESS>"
      },
      "hiu": {
        "id": "INDIA_HIU",
        "name": "INDIA HIU",
        "type": "HIU"
      },
      "hips": [
        {
          "id": "INDIA_HIP",
          "name": "INDIA HIP",
          "type": "HIP"
        }
      ],
      "categories": [
        "LINK"
      ],
      "period": {
        "from": "2024-05-09T10:34:00.389Z",
        "to": "2024-05-09T10:34:00.389Z"
      },
      "status": "GRANTED",
      "requestType": "HEALTH_LOCKER"
    }
  ]
}
```
