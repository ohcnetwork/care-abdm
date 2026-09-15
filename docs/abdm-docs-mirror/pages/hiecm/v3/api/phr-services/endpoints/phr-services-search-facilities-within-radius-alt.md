# Search Facilities Within Radius

`POST /health/service/facility/geo-location/search-within-radius`

The same facility-radius search as
`phr_services_search_facilities_within_radius` in this file. Request
and response are identical. NHA's Postman collection recorded this
as a separate request against a second route, without the `/api`
prefix the other route carries, so it is kept here as a separate
operation rather than merged away.

```bash
curl --request POST \
  --url https://phrsbx.abdm.gov.in/health/service/facility/geo-location/search-within-radius \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "abdmSoftware": "0",
  "centerLat": "11.9601971",
  "centerLon": "79.812865",
  "facilityOwnership": "",
  "hospitalSpecialityType": "",
  "radiusInKm": "50",
  "from": "0",
  "size": "100",
  "speciality": ""
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Body

- `abdmSoftware` (string, required)
- `centerLat` (string, required)
- `centerLon` (string, required)
- `facilityOwnership` (string, required)
- `hospitalSpecialityType` (string, required)
- `radiusInKm` (string, required)
- `from` (string, required)
- `size` (string, required)
- `speciality` (string, required)

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
  "searchCountTotal": 9887,
  "recordList": [
    {
      "mobile_no": "<MOBILE>",
      "abdm_software": null,
      "pincode": "<PIN_CODE>",
      "facility_type": "40",
      "sub_district": "4192",
      "book_app_url": "",
      "facility_website": "",
      "geolocation": "18.<REDACTED_ID>,73.<REDACTED_ID>",
      "district": "490",
      "address2": "<ADDRESS>",
      "state": "27",
      "address1": "<ADDRESS>",
      "facility_subtype_other": null,
      "facility_name": "Test bhavya <REDACTED_ID>",
      "facility_ownership": "P",
      "facility_email": "",
      "system_of_medicine": "D,M,A,UN,P",
      "owner_subtype": "",
      "landline_no": "",
      "fac_unique_id": "IN2710004269",
      "alternate_id": "IN2710004269",
      "distances": "0",
      "speciality": [
        "cardiology",
        "anorectalcareclinic",
        "... 12 more of the same shape"
      ],
      "systemOfMedicine": [
        {
          "id": "D",
          "value": "Dentistry"
        },
        {
          "id": "M",
          "value": "Modern Medicine(Allopathy)"
        },
        "... 3 more of the same shape"
      ]
    },
    {
      "mobile_no": "<MOBILE>",
      "abdm_software": "1",
      "pincode": "<PIN_CODE>",
      "facility_type": "39",
      "sub_district": "4194",
      "book_app_url": null,
      "facility_website": "",
      "geolocation": "18.5615627,73.9079515",
      "district": "490",
      "address2": "<ADDRESS>",
      "state": "27",
      "address1": "<ADDRESS>",
      "facility_subtype_other": null,
      "facility_name": "Mentell hospital",
      "facility_ownership": "P",
      "facility_email": "<EMAIL>",
      "system_of_medicine": "M",
      "owner_subtype": "P",
      "landline_no": "",
      "fac_unique_id": "IN2710001975",
      "alternate_id": "IN2710001975",
      "distances": "4.79",
      "speciality": null,
      "systemOfMedicine": [
        {
          "id": "M",
          "value": "Modern Medicine(Allopathy)"
        }
      ]
    },
    "... 98 more of the same shape"
  ]
}
```
