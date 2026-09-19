# Get admin token

`POST /getManagementToken`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/getManagementToken \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "username": "<USERNAME>",
  "password": "<PASSWORD>",
  "resend": false
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `username` (string)
- `password` (string)
- `resend` (boolean)

## Responses

- `200`: OK
- `404`: Not Found
