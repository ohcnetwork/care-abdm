# {{aarogya-setu-sandbox-url}}api/health/service/doctor/geo-location/search-within-radius

`POST /health/service/doctor/geo-location/search-within-radius`

Finds doctors within a radius of a point, filtered by name, speciality, facility ownership and type, with paging.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/health/service/doctor/geo-location/search-within-radius \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "abdmSoftware": "0",
  "centerLat": "18.<REDACTED_ID>",
  "centerLon": "73.<REDACTED_ID>",
  "facilityOwnership": "",
  "from": "0",
  "hospitalSpecialityType": "",
  "radiusInKm": "5000",
  "size": "100",
  "speciality": "",
  "doctorName": "",
  "gender": "",
  "doctorSystemOfMedicine": "M",
  "languages": ""
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `abdmSoftware` (string, required)
- `centerLat` (string, required)
- `centerLon` (string, required)
- `facilityOwnership` (string, required)
- `from` (string, required)
- `hospitalSpecialityType` (string, required)
- `radiusInKm` (string, required)
- `size` (string, required)
- `speciality` (string, required)
- `doctorName` (string, required)
- `gender` (string, required)
- `doctorSystemOfMedicine` (string, required)
- `languages` (string, required)

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
  "searchCountTotal": 165,
  "recordList": [
    {
      "name": "<NAME>",
      "hprProfileId": 31426,
      "healthIdNumber": "<ABHA_NUMBER>",
      "mobileOfficial": "<MOBILE>",
      "emailOfficial": "<EMAIL>",
      "gender": "Male",
      "registrationNumber": "1234567890",
      "systemOfMedicine": "Modern Medicine",
      "facilityLocation": {
        "lat": 18.53145937529085,
        "lon": 73.87545685498799
      },
      "distances": "0",
      "facilityId": "IN2710004269",
      "courseName": "MBBS - Bachelor of Medicine and Bachelor of Surgery, test 12345",
      "piLanguages": [
        "3"
      ],
      "facilityName": "Test bhavya <REDACTED_ID>",
      "facilityAddress": "test 123r",
      "facilityContact": null,
      "designationWithOrganisation": "Sr. Doctor",
      "workExperienceInYear": "5",
      "facilitySystemOfMedicine": [
        "Dentistry, Modern Medicine(Allopathy), Ayurveda, Unani, Physiotherapy",
        "Modern Medicine"
      ],
      "facilityDepartment": "Cardio",
      "speciality": null
    },
    {
      "name": "<NAME>",
      "hprProfileId": 33389,
      "healthIdNumber": "<ABHA_NUMBER>",
      "mobileOfficial": "<MOBILE>",
      "emailOfficial": "<EMAIL>",
      "gender": "Female",
      "registrationNumber": "56789",
      "systemOfMedicine": "Modern Medicine",
      "facilityLocation": {
        "lat": 18.504648793596203,
        "lon": 73.76347481875169
      },
      "distances": "12.18",
      "facilityId": "IN2710004268",
      "courseName": "MBBS - Bachelor of Medicine and Bachelor of Surgery",
      "piLanguages": [
        "1",
        "2",
        "... 1 more of the same shape"
      ],
      "facilityName": "Manish Test 21 Aug",
      "facilityAddress": "Test 123456",
      "facilityContact": "<MOBILE>",
      "designationWithOrganisation": "fefefjenfejnfejfnejfn",
      "workExperienceInYear": "6",
      "facilitySystemOfMedicine": [
        "Modern Medicine(Allopathy), Dentistry, Physiotherapy, Ayurveda, Unani",
        "Modern Medicine"
      ],
      "facilityDepartment": "fhfjdfjeff",
      "speciality": [
        "AmrazAtfal  (Paediatrics)",
        "AmrazeJigar wa Mirara (Hepato-biliary System)",
        "... 9 more of the same shape"
      ]
    },
    "... 98 more of the same shape"
  ]
}
```
