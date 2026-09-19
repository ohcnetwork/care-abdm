# Validate OTP

`POST /v1.5/facility/validateOtp`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/validateOtp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "facilityId": "IN2810002702",
  "sourceId": "AB-PMJAY",
  "otp": "885210",
  "source": "AB-PMJAY",
  "transactionId": "2ddfc7ec-9a9f-412c-8c50-c2be92da5781"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `facilityId` (string)
- `sourceId` (string)
- `otp` (string)
- `source` (string)
- `transactionId` (string)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "facilityId": "IN2810002702",
  "status": "success",
  "message": "OTP validated successfully!!! Hospital id linked to HFR",
  "errorStatus": null
}
```
