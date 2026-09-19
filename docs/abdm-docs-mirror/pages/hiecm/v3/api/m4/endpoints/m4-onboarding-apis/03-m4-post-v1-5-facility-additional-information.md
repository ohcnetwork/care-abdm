# Submit the v15Facility additional information

`POST /v1.5/facility/additional-information`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/additional-information \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "trackingId": "80266",
  "linkedProgramIds": {
    "nhrrId": "1234",
    "nin": "1234",
    "abpmjayId": "1234",
    "rohiniId": "1234",
    "echsId": "1234",
    "cghsId": "1234",
    "ceaRegistration": "1234",
    "stateInsuranceSchemeId": "1234"
  },
  "generalInformation": {
    "hasDialysisCenter": "YALL",
    "hasPharmacy": "YALL",
    "hasBloodBank": "YALL",
    "hasCathLab": "YALL",
    "hasDiagnosticLab": "YALL",
    "hasImagingCenter": "YALL",
    "servicesByImagingCenter": [
      {
        "service": "S36",
        "count": 7
      },
      {
        "service": "S16",
        "count": 5
      },
      {
        "service": "S23",
        "count": 3
      }
    ]
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `trackingId` (string, required)
- `linkedProgramIds` (object)
- `linkedProgramIds.nhrrId` (string)
- `linkedProgramIds.nin` (string)
- `linkedProgramIds.abpmjayId` (string)
- `linkedProgramIds.rohiniId` (string)
- `linkedProgramIds.echsId` (string)
- `linkedProgramIds.cghsId` (string)
- `linkedProgramIds.ceaRegistration` (string)
- `linkedProgramIds.stateInsuranceSchemeId` (string)
- `generalInformation` (object)
- `generalInformation.hasDialysisCenter` (string)
- `generalInformation.hasPharmacy` (string)
- `generalInformation.hasBloodBank` (string)
- `generalInformation.hasCathLab` (string)
- `generalInformation.hasDiagnosticLab` (string)
- `generalInformation.hasImagingCenter` (string)
- `generalInformation.servicesByImagingCenter` (object[])

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "trackingId": "76803",
  "status": "Created",
  "message": "Facility details have been saved successfully. Please login at https://nhpr.abdm.gov.in/ and submit your facility details for approval.",
  "errorStatus": null
}
```
