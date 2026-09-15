# 05 - Upload Record [POST]

`POST /digi-locker/upload`

Uploads a file the person holds into their DigiLocker as a health record.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/digi-locker/upload \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "attachment": "base64_encoded_file_content_here",
  "fileName": "sample_report.pdf"
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `attachment` (string, required)
- `fileName` (string, required)

## Responses

- `200`: No response body is documented for this request.
