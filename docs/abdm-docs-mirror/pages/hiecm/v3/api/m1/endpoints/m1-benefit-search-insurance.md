# Find insurance cover recorded against an ABHA number

`GET /v3/profile/benefit/abha/search/insurance/{abhaNumber}`

Documented responses include 400, 401 and 500 as well as 200. Handle
all four.

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/benefit/abha/search/insurance/{abhaNumber} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.

## Path parameters

- `abhaNumber` (string, required): A fourteen digit ABHA number, written in the hyphenated form NHA uses, for example 91-1234-5678-9012.

## Responses

- `200`: The insurance programmes linked to the ABHA.
- `400`: The error returned, with its code and message.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: The error returned, with its code and message.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden, the token is valid but not permitted for this operation
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `404`: Resource not found
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `500`: The error returned, with its code and message.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "abhaNumber": "<ABHA_NUMBER>",
  "entityType": "Insurance",
  "insuranceProgramsLinked": [
    "Health ID Test"
  ]
}
```
