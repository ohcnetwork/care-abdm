# Get All Care Context Links for ABHA Address

`POST /api/care-context-link/my-records/fetch/all`

Lists the care context links for an ABHA address with paging and filters: HIP, record type, bookmarked, self-uploaded and date range.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/my-records/fetch/all \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "abhaAddress": "<ABHA_ADDRESS>",
  "limit": 10,
  "offset": 0,
  "hipId": "",
  "hiType": "",
  "bookmarked": null,
  "selfUploaded": null,
  "dateRange": null,
  "sortHipName": null
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `abhaAddress` (string, required)
- `limit` (integer, required)
- `offset` (integer, required)
- `hipId` (string, required)
- `hiType` (string, required)
- `bookmarked` (null, required)
- `selfUploaded` (null, required)
- `dateRange` (null, required)
- `sortHipName` (null, required)

## Responses

- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
