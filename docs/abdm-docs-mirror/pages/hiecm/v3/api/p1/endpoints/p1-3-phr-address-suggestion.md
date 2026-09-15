# 3. PHR Address Suggestion

`POST /api/registration/phr/suggestion`

Suggests available ABHA addresses from the person's name and date of birth, for a mobile-based registration transaction.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/api/registration/phr/suggestion \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "<TXN_ID>",
  "firstName": "<FIRST_NAME>",
  "lastName": "<LAST_NAME>",
  "dayOfBirth": "14",
  "monthOfBirth": "10",
  "yearOfBirth": "1999"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `txnId` (string, required)
- `firstName` (string, required)
- `lastName` (string, required)
- `dayOfBirth` (string, required)
- `monthOfBirth` (string, required)
- `yearOfBirth` (string, required)

## Responses

- `200`: No response body is documented for this request.
