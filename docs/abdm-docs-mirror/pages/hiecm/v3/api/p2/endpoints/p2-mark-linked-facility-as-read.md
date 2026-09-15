# Mark Linked Facility as Read

`DELETE /api/care-context-link/read/link/patient/links/{hipId}`

Marks the records from one HIP as seen, clearing the unread indicator for that facility.

```bash
curl --request DELETE \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/read/link/patient/links/{hipId} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Path parameters

- `hipId` (string, required): Passed as a path segment.

## Responses

- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
