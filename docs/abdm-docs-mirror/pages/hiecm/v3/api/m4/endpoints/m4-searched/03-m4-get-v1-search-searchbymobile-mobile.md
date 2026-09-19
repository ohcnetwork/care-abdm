# Search user by mobile no

`GET /v1/search/searchByMobile/{mobile}`

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1/search/searchByMobile/{mobile} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Path parameters

- `mobile` (string, required)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
[
  {
    "hprIdNumber": "<HPR_ID>",
    "name": "Ayushman Bharat Mission",
    "authMethods": [
      "PASSWORD",
      "MOBILE_OTP",
      "... 1 more of the same shape"
    ],
    "hprId": "<EMAIL>",
    "categoryId": "1",
    "subCategoryId": "1"
  }
]
```
