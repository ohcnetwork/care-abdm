# Submit the healdthloginwithmobile

`POST /healdthloginwithmobile`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/healdthloginwithmobile \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "<TXN_ID>",
  "issueToken": "<ISSUE_TOKEN>",
  "token": "<TOKEN>"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `txnId` (string)
- `issueToken` (string)
- `token` (string)

## Responses

- `200`: OK
- `404`: Not Found
