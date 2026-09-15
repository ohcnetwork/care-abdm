# Add My Record Bookmark

`POST /api/care-context-link/my-record/bookmark`

Bookmarks a self-uploaded record by its care context reference.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/my-record/bookmark \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "careContextReference": "care-context-ref-001",
  "abhaAddress": "<ABHA_ADDRESS>"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `careContextReference` (string, required)
- `abhaAddress` (string, required)

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "id": 254,
  "patientId": "<PATIENT_ID>",
  "careContextReference": "25ac532f-178d-5885-9bcb-b82052f345eb_20260604190956854815",
  "dateCreated": "2026-06-13T19:01:35.955"
}
```
