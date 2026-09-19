# Get health locker settings of a patient by locker ID

`GET /api/hiecm/subscription-requests/v3/patients/lockers/{lockerId}`

Retrieve the health locker settings of a patient using the locker ID. By invoking this API, users can access detailed information about the configuration and preferences of the patient’s health locker. This functionality is essential for managing and customizing the storage and access settings of health records, ensuring that patients have control over their health information. The API supports secure and efficient retrieval of health locker settings, enhancing the overall management of health data within the healthcare ecosystem.

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/subscription-requests/v3/patients/lockers/{lockerId} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-AUTH-TOKEN: <TOKEN>'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required): Unique UUID for tracking the end-to-end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds, and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended
- `X-AUTH-TOKEN` (string, required): JWT Authentication token issued by ABDM after successful validation of username and password

## Path parameters

- `lockerId` (string, required): The locker id

## Responses

- `200`: OK
- `400`: Bad Request
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
- `404`: server cannot find the requested resource
- `500`: Internal Server Error
- `503`: Service Unavailable

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "lockerId": "1234",
  "lockerName": "Locker 1",
  "active": true,
  "dateCreated": "2021-09-28T12:30:08.573Z",
  "subscriptions": [
    {
      "subscriptionId": "f29f0e59-8388-4698-9fe6-05db67aeac46",
      "purpose": {
        "text": "Care Management",
        "code": "CAREMGT",
        "refUri": "https://abc.def.in"
      },
      "status": "GRANTED",
      "dateCreated": "2021-09-28T12:30:08.573Z",
      "dateGranted": "2021-09-28T12:30:08.573Z",
      "patient": {
        "id": "<ABHA_ADDRESS>"
      },
      "requester": {
        "id": "<ABHA_ADDRESS>",
        "name": "ABDM_HIU",
        "type": "HIU"
      },
      "includedSources": [
        {
          "hiTypes": [
            "Prescription"
          ],
          "purpose": {
            "text": "Care Management",
            "code": "CAREMGT",
            "refUri": "https://abc.def.in"
          },
          "hip": {
            "id": "INDIA_HIP",
            "name": "INDIA HIP",
            "type": "HIP"
          },
          "categories": [
            "LINK"
          ],
          "period": {
            "from": "2024-05-09T10:34:00.389Z",
            "to": "2024-05-09T10:34:00.389Z"
          },
          "status": "SUCCESS"
        }
      ]
    }
  ],
  "autoApprovals": [
    {
      "id": 1234,
      "autoApprovalId": "e5ec415f-c098-40f6-a0db-faa162fc5295",
      "hiuId": "India_HIU",
      "patientId": "<ABHA_ADDRESS>",
      "isActive": false,
      "dateCreated": "2021-09-28T12:30:08.573Z",
      "dateModified": "2021-09-28T12:30:08.573Z",
      "policy": {
        "isApplicableForAllHIPs": true,
        "hiu": {
          "id": "INDIA_HIU",
          "name": "INDIA HIU",
          "type": "HIU"
        },
        "includedSources": [
          {
            "hiTypes": [],
            "categories": [],
            "status": "SUCCESS"
          }
        ],
        "excludedSources": [
          {
            "hiTypes": [],
            "categories": [],
            "status": "SUCCESS"
          }
        ]
      }
    }
  ]
}
```
