# Fetch documents

`POST /apis/v1/doctors/fetch-documents-list`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/doctors/fetch-documents-list \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hprid": "<HPR_ID>"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `hprid` (string)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "documentList": {
    "profileDetails": {
      "profilePhoto": {
        "id": 30106,
        "data": "<BASE64_PHOTO>"
      },
      "proofOfWorkCertificate": {
        "id": 30106,
        "data": "JVBERi0xLjMK"
      }
    },
    "registrationDetails": [
      {
        "registrationCertificate": {
          "id": 21021,
          "systemOfMedicide": "modern_medicine",
          "data": "JVBERi0xLjMK"
        },
        "proofOfNameChangeRegCertificate": {
          "id": 21021,
          "systemOfMedicide": "modern_medicine",
          "data": "JVBERi0xLjMK"
        }
      }
    ],
    "qualificationDetails": [
      {
        "degreeCertificate": {
          "id": 9693,
          "courseName": "PhD Biostatistics",
          "qualificationYear": "2021",
          "data": "JVBERi0xLjMK"
        },
        "proofOfNameChangeQualCertificate": {
          "id": 9693,
          "courseName": "PhD Biostatistics",
          "qualificationYear": "2021",
          "data": "JVBERi0xLjMK"
        }
      }
    ],
    "qualification": null
  },
  "Message": "Data fetched successfully"
}
```
