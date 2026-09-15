# Get Orders by ABHA id desc

`GET /teleconsulting/getOrdersByAbhaIdDesc`

Lists the teleconsultation orders of an ABHA address, newest first.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/teleconsulting/getOrdersByAbhaIdDesc \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
"array"
```
