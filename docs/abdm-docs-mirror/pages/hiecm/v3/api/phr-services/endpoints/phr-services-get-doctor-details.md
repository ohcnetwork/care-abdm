# Get Doctor Details

`GET /health/service/facility/doctors/{searchId}`

Lists the doctors at a facility, by the facility's search id.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/health/service/facility/doctors/{searchId} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Path parameters

- `searchId` (string, required): Passed as a path segment.

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
  "totalCount": 1,
  "doctorDetails": [
    {
      "id": 80285,
      "name": "<NAME>",
      "hprProfileId": 31426,
      "designationWithOrganisation": "Sr. Doctor",
      "facilityId": "IN2710004269",
      "systemOfMedicine": "1",
      "doctorQualification": [
        {
          "courseName": "MBBS - Bachelor of Medicine and Bachelor of Surgery",
          "systemOfMedicine": "1"
        },
        {
          "courseName": " test 12345",
          "systemOfMedicine": "1"
        }
      ],
      "hospitalId": null,
      "state": null,
      "district": null,
      "facilityTransactionId": null,
      "digiDoctorId": null,
      "facilityName": null,
      "facilityType": null,
      "facilityAddress": null,
      "facilityPincode": 0,
      "status": null,
      "createdAt": null,
      "updatedAt": null,
      "facilityOwnership": null,
      "facilitySystemOfMedicine": null,
      "facilityDepartment": null,
      "facilityStatus": null,
      "facilityEloc": null,
      "facilityLat": 0,
      "facilityLong": 0,
      "verificationStatus": null,
      "remark": null,
      "facilitySuggesstionId": null,
      "selfDeclared": false,
      "current": false
    }
  ]
}
```
