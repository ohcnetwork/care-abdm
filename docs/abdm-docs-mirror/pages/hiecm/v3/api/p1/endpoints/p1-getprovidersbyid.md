# getProvidersByID

`GET /global/providers/000`

Returns one provider's registry entry: its identifier, facility type, whether it is registered in the HIP role, and whether it supports scan and pay.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/global/providers/000 \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `403`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "identifier": {
    "name": "<NAME>",
    "id": "37913"
  },
  "facilityType": [
    "HIP",
    "HIU"
  ],
  "isHIP": true,
  "isPaymentShare": true,
  "scanPayVersion": "V3"
}
```
