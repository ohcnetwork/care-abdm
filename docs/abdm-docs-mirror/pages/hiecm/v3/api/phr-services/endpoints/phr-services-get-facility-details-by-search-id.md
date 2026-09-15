# Get Facility Details By Search ID

`GET /health/service/facility/search/IN3310027864`

Returns a facility's registry entry by its search id, including its contact person and address.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/health/service/facility/search/IN3310027864 \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
- `401`: Example values, scrubbed.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `404`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors
- `500`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/phr-services/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "facUniqueId": "string",
  "facContactPerPrefix": "null",
  "facContactPerName": "string",
  "facContactPerMiddleName": "string",
  "facContactPerSurname": "string",
  "facContactPerDesg": "null",
  "facContactPerCountryCode": "null",
  "facContactPerMobNo": "string",
  "facContactPerEmail": "string",
  "facContactPerStdCode": "null",
  "facContactPerLandlineNo": "null",
  "facName": "string",
  "facOwnership": "string",
  "facPAN": "null",
  "facTAN": "null",
  "facGST": "null",
  "country": "string",
  "state": "string",
  "district": "string",
  "pincode": "string",
  "geolocation": "string",
  "subDistrict": "string",
  "facRegion": "string",
  "vilCityTown": "string",
  "address1": "string",
  "address2": "string",
  "landlineNo": "string",
  "mobileNo": "string",
  "facEmail": "string",
  "daysOfOperation": "null",
  "hoursOfOperation": "null",
  "aboutUs": "null",
  "itAvailable": "null",
  "netAvailable": "null",
  "emrSystem": "string",
  "emrSoftware": "string",
  "powerBackup": "null",
  "facOperStatus": "string",
  "typeOfService": "string",
  "typeOfServiceOth": "null",
  "facOwnerGovt": "string",
  "facOwnerPrivate": "string",
  "ownerSubType": "string",
  "facCentral": "string",
  "facCentralOth": "null",
  "systemOfMedicine": "string",
  "facilityType": "string",
  "facilityTypeOth": "null",
  "hospitalCntLinkColg": "null",
  "stdCode": "null",
  "addProofType": "null",
  "addProofType2": "null",
  "addProofType3": "null",
  "facWebsite": "string",
  "openTime": "null",
  "closeTime": "null",
  "crtDt": "string",
  "crtUsr": "string",
  "lstUpdDt": "string",
  "lstUpdUsr": "string",
  "termsAgreeFlag": "string",
  "submitFlag": "null",
  "status": "string",
  "healthId": "string",
  "appSubmitDt": "string",
  "nhrrFacilityId": "null",
  "nhrrFormId": "null",
  "hospitalLinkToColg": "null",
  "colgCntLinkHospital": "null",
  "altHealthDtls": "null",
  "healthWellnessCenter": "null",
  "ufid": "null",
  "mobileNoPerCountryCode": "null",
  "activeYn": "string",
  "alternateId": "string",
  "alternateContactDtls": "null",
  "facAltContactPerPrefix": "null",
  "facAltContactPerName": "null",
  "facAltContactPerMiddleName": "null",
  "facAltContactPerSurname": "null",
  "facAltContactPerDesg": "null",
  "facAltContactPerCountryCode": "null",
  "facAltContactPerMobNo": "null",
  "facAltContactPerEmail": "null",
  "facAltContactPerStdCode": "null",
  "facAltContactPerLandlineNo": "null",
  "mobileNoVerified": "string",
  "facEmailVerified": "string",
  "facContactPerEmailVerified": "string",
  "facAltContactPerEmailVerified": "null",
  "nameAsInPanCard": "null",
  "progressValue": "null",
  "bookAppUrl": "string",
  "ehospitalid": "null",
  "identificationNo": "null",
  "rohiniId": "null",
  "pmjayHospitalId": "null",
  "cghsHospitalId": "null",
  "echsHospitalId": "null",
  "yearOfEstablish": "null",
  "hospitalSpecialType": "null",
  "privateProfitType": "string",
  "powerBackupIT": "null",
  "pharmacySoftware": "null",
  "pharmacySoftwareName": "null",
  "source": "string",
  "entityType": "string",
  "hmisCode": "null",
  "facilitySubtype": "string",
  "facilitySubtypeOther": "null",
  "ceaId": "null",
  "declaredBy": "string",
  "hrpSource": "null",
  "hrpSourceFacilityId": "null",
  "isStandaloneIS": "null",
  "standaloneISName": "null",
  "isLMISorRISSystem": "null",
  "ifAnyOther": "string",
  "emrSoftwareOther": "null",
  "form1": "null",
  "form2": "null",
  "form3": "null",
  "pharmacySoftwareOther": "null",
  "abdmSoftware": "null",
  "resubmitted": "boolean",
  "facilityPassword": "boolean",
  "facilityStatus": "string",
  "workDetailslist": "array",
  "bridgeDetails": "array",
  "daysOfOperationObject": "array",
  "stinsid": "null",
  "esushrutId": "null",
  "earogya": "null",
  "lmisorRISSystemName": "null",
  "sourceId": "null"
}
```
