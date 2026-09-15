# get Orders by id

`GET /api/teleconsulting/getOrders/6254-172027-4007`

Returns one teleconsultation order by its order id, with the service, the professional and the fulfilment time.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/teleconsulting/getOrders/6254-172027-4007 \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "orderId": "string",
  "categoryId": "string",
  "healthcareServiceName": "string",
  "healthcareServiceId": "string",
  "healthcareProviderUrl": "string",
  "healthcareProfessionalName": "string",
  "healthcareProfessionalImage": "string",
  "healthcareProfessionalId": "string",
  "healthcareProfessionalGender": "string",
  "serviceFulfillmentStartTime": "string",
  "serviceFulfillmentEndTime": "string",
  "serviceFulfillmentType": "string",
  "isServiceFulfilled": "string",
  "message": "string",
  "slotId": "string",
  "patientConsumerUrl": "string",
  "transId": "string",
  "abhaId": "string"
}
```
