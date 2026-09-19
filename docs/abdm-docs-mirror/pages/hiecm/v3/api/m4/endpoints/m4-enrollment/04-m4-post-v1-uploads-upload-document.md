# Upload documents

`POST /apis/v1/uploads/upload-document`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/uploads/upload-document \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hpr_token": "<JWT TOKEN>",
  "document": [
    {
      "document_id": 20931,
      "document_type": "registrationCertificate",
      "fileType": "",
      "data": "JVBERi0xLjMK"
    }
  ]
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `hpr_token` (string)
- `document` (object[])
- `document.document_id` (integer)
- `document.document_type` (string)
- `document.fileType` (string)
- `document.data` (string)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "profilePhoto": null,
  "degreeCertificate": null,
  "registrationCertificate": {
    "status": "pass",
    "msg": "Registration certificate updated"
  },
  "proofOfWorkCertificate": null
}
```
