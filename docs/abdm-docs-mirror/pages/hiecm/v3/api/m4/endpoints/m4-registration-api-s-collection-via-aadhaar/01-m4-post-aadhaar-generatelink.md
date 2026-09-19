# Generate Aadhaar link

`POST /aadhaar/generateLink`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/aadhaar/generateLink \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "scopes": [
    "nhpr-register"
  ],
  "source": "NHPR"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `scopes` (string[])
- `source` (string)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "de4ff682-fcc6-4bcf-a978-0dbb19a288b4",
  "mobileNumber": "******1234"
}
```
