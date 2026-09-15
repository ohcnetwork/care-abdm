# get Orders by ABHA id

`GET /api/teleconsulting/getOrdersByAbhaId`

Lists the teleconsultation orders placed by an ABHA address.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/teleconsulting/getOrdersByAbhaId \
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
