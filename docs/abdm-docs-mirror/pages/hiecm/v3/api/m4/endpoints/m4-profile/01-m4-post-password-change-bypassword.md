# Change password

`POST /password/change/byPassword`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/password/change/byPassword \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "newPassword": "<BASE64 ENCODED STRING>",
  "oldPassword": "<BASE64 ENCODED STRING>"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `oldPassword` (string)
- `newPassword` (string)
- `txnId` (string)
- `hprID` (string)
- `otp` (string)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "message": "Password has been changed successfully!"
}
```
