# Add Feedback

`POST /api/notification/feedback`

Records feedback from the person, with a title and body, against their ABHA.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/notification/feedback \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "healthId": "<ABHA_ADDRESS>",
  "emailId": "<EMAIL>",
  "title": "feedback",
  "body": "AarogyaSethu feedback test-1"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `healthId` (string, required)
- `emailId` (string, required)
- `title` (string, required)
- `body` (string, required)

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p3/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "id": 71,
  "healthId": "<ABHA_ADDRESS>",
  "emailId": "<EMAIL>",
  "title": "feedback",
  "body": "AarogyaSethu feedback test-1",
  "dateCreated": "2026-06-01T08:15:27.682Z"
}
```
