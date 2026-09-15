# Get Orders by Abha Id and Type

`GET /teleconsulting/getOrdersByAbhaIdAndType/kushal.1122000@sbx`

Lists the teleconsultation orders of an ABHA address, filtered by order type.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/teleconsulting/getOrdersByAbhaIdAndType/kushal.1122000@sbx \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "pinCode": 0,
    "districtCode": 589,
    "districtName": "THIRUVALLUR",
    "stateCode": 33,
    "stateName": "TAMIL NADU"
  }
]
```
