# Submit the demographic auth via mobile

`POST /v2/registration/aadhaar/demographicAuthViaMobile`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v2/registration/aadhaar/demographicAuthViaMobile \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "de4ff682-fcc6-4bcf-a978-0dbb19a288b4",
  "mobileNumber": "JrHfDROoEcsYJ41g2wdkicsI7mT1ATCP347iqwBhWbfaEIgZ03/WHAYvDHRG2WXl4HBNuP2orD+3O75pN0xFhOz4oLXrePAxKTLK8uG5jdeAiGE2lKwOrShq9/gg+BckrQcDYjpMUePRuDau4mqLHa8FdSCQ8npGPY9KCpD2hZkscWNqZR68gRo/EwpY4u32kDzv5i1K/s+A7FNVwXqZS5AK2BadEhG5drSRk7P83eFxJZUlwtsvDK6iipOsM4VtMXXXXXXXXXXXXXXXXXXXXXXXXXXX"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `txnId` (string)
- `mobileNumber` (string)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "verified": true,
  "errorCode": null,
  "reason": null,
  "uidaiToken": null
}
```
