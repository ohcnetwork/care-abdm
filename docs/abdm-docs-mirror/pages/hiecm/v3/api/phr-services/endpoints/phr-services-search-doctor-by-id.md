# search-doctor-by-id

`GET /health/service/doctor/search/{abhaNumber}`

Returns a doctor's registry profile by their ABHA number: registration, qualifications, system of medicine and experience.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/health/service/doctor/search/{abhaNumber} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Path parameters

- `abhaNumber` (string, required): Passed as a path segment.

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
  "doctorName": "Anshul Atul Siddhamshettiwar",
  "healthIdNumber": "<ABHA_NUMBER>",
  "mobileOfficial": "<MOBILE>",
  "emailOfficial": "<EMAIL>",
  "gender": "Male",
  "registrationNumber": "1234567890",
  "systemOfMedicine": "Modern Medicine",
  "courseName": "MBBS - Bachelor of Medicine and Bachelor of Surgery",
  "internationalDegree": " test 12345",
  "workExperienceInYear": "5",
  "facilityDetails": [
    {
      "facilityId": "IN2710004268",
      "facilityName": "Manish Test 21 Aug",
      "facilityAddress": "Test 123456  Pune Maharashtra 412115",
      "facilityContact": "<MOBILE>",
      "designationWithFacility": "Sr. Doctor",
      "distanceInKm": "12.18"
    },
    {
      "facilityId": "IN2710004269",
      "facilityName": "Test bhavya <REDACTED_ID>",
      "facilityAddress": "test 123r",
      "facilityContact": null,
      "designationWithFacility": "Sr. Doctor",
      "distanceInKm": "0"
    }
  ],
  "languages": [
    " Bengali "
  ]
}
```
