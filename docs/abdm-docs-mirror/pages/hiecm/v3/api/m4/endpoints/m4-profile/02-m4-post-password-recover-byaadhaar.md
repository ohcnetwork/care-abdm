# Recover password via Aadhaar

`POST /password/recover/byAadhaar`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/password/recover/byAadhaar \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hprId": "<HPR_ID>"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `hprId` (string, required)
- `categories` (object)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "9b78fdfb-3ba4-4707-8913-63c7c5e3a743",
  "mobileNumber": "******8063",
  "msg": "",
  "verified": false
}
```
