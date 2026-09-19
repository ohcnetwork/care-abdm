# Get professional info

`POST /apis/v1/doctors/fetch-professional-info`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/doctors/fetch-professional-info \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "practitioner": {
    "id": "<HPR_ID>",
    "name": "",
    "contactNumber": "976243XXXX",
    "state": "UTTAR PRADESH",
    "registrationNumber": ""
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `practitioner` (object)
- `practitioner.id` (string)
- `practitioner.name` (string)
- `practitioner.contactNumber` (string)
- `practitioner.state` (string)
- `practitioner.registrationNumber` (string)
- `practitioner.stateCouncilName` (string)

## Responses

- `200`: OK
- `404`: Not Found

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "practitioners": [
    [
      {
        "identifier": 38053,
        "active": false,
        "name": "Ayushman Bharat Mission",
        "gender": "Male",
        "salutation": "Mr",
        "communicationLanguage": " English ",
        "registrations": [
          {
            "identifier": 25989,
            "category": "Dentistry",
            "nuidnumber": null,
            "nuidvalidtill": null,
            "systemOfMedicide": null,
            "isRenewable": "false",
            "dueDate": null,
            "councilName": "Karnataka State Dental Council",
            "registeredAt": null,
            "registrationNumber": "REG12032",
            "registrationDate": "2024-12-01"
          }
        ],
        "qualifications": [
          {
            "identifier": 12835,
            "courseName": "Bds - Bachelor Of Dental Surgery",
            "collegeName": "A.j. Institute Of Dental Sciences, Mangalore",
            "universityName": "Rajiv Gandhi University Of Health Sciences (rguhs)",
            "qualificationYear": "2024",
            "qualificationMonth": ""
          }
        ],
        "hpr_id": "<HPR_ID>",
        "application_status": null,
        "is_council_verified": "true",
        "is_work_verified": null,
        "email": "",
        "mobileNumber": "******2125",
        "hpr_category": "doctor"
      }
    ]
  ],
  "message": "Data fetched successfully"
}
```
