# get-policies

`POST /nhcx/get-policies`

Lists the insurance policies held against an ABHA number. `encryptedAbhaNumber` is the ABHA number encrypted.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/nhcx/get-policies \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "encryptedAbhaNumber": "<ABHA_NUMBER>",
  "insuranceType": "pmjay"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `encryptedAbhaNumber` (string, required)
- `insuranceType` (string, required)

## Responses

- `200`: Example values, scrubbed.
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `404`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "sno": "<SNO>",
    "abhanumber": "<ABHANUMBER>",
    "mobilenumber": "<MOBILENUMBER>",
    "memberid": "<MEMBERID>",
    "payerid": "<PAYERID>",
    "productid": "<PRODUCTID>",
    "productname": "<PRODUCTNAME>",
    "processingid": "<PROCESSINGID>"
  }
]
```
