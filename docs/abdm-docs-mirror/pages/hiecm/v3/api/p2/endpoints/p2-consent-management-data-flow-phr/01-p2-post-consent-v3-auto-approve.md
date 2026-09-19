# Setup an auto-approval policy for given HIU

`POST /api/hiecm/consent/v3/auto/approve`

Set up an auto-approval policy for a specified Health Information User (HIU). By invoking this API, users can configure automatic approval of consent requests from the designated HIU, streamlining the process of granting access to health data. This functionality is essential for enhancing efficiency and reducing manual intervention in the consent management process. The API supports secure and compliant health information exchange, ensuring that auto-approval policies are implemented in accordance with user preferences and regulatory requirements.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/api/hiecm/consent/v3/auto/approve \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx' \
  --header 'X-AUTH-TOKEN: <TOKEN>' \
  --header 'Content-Type: application/json' \
  --data '{
  "isApplicableForAllHIPs": false,
  "hiu": {
    "id": "cowin_hiu_01",
    "name": "Cowin",
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
        "refUri": "www.abc.com"
      },
      "hip": {
        "id": "cowin_hip_01",
        "name": "Cowin",
        "type": "HIP"
      },
      "period": {
        "from": "2021-09-28T12:30:08.573Z",
        "to": "2021-09-28T12:30:08.573Z"
      }
    }
  ],
  "excludedSources": [
    {
      "hiTypes": [
        "Prescription"
      ],
      "purpose": {
        "text": "Care Management",
        "code": "CAREMGT",
        "refUri": "www.abc.com"
      },
      "hip": {
        "id": "cowin_hip_01",
        "name": "Cowin",
        "type": "HIP"
      },
      "period": {
        "from": "2021-09-28T12:30:08.573Z",
        "to": "2021-09-28T12:30:08.573Z"
      }
    }
  ]
}'
```

## Authorization

- `Authorization` (bearer token, required): The access token from POST /api/hiecm/gateway/v3/sessions.

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended
- `X-AUTH-TOKEN` (string, required): JWT Authentication token which was issued by ABDM after successful validation of username and password

## Body

- `isApplicableForAllHIPs` (boolean, required): A boolean value to denote if the policy is applicable to all the HIPs or only the specified HIP
- `hiu` (object, required)
- `hiu.id` (string, required): The service ID of the health information user.  Allows alpha numeric character and special characters like [A-Z a-z 0-9]+[A-Z a-z 0-9 //_//-]*[A-Z a-z 0-9]$
- `hiu.name` (string, required): The name of the health information user. Allows alpha numeric and special characters like  "^[a-zA-Z]+[A-Za-z0-9_\\-@,().\\s\\xa0:/]+"
- `hiu.type` (string, required): The type of the health information user. Allows alpha numeric and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `includedSources` (object[], required): Included sources, carrying the list of hi types.
- `includedSources.hiTypes` (string[], required): Types of health information document.
- `includedSources.purpose` (object, required)
- `includedSources.purpose.text` (string, required) One of: Care Management, Break the Glass, Public Health, Healthcare Payment, Disease Specific Healthcare Research, Self Requested.
- `includedSources.purpose.code` (string, required) One of: CAREMGT, BTG, PUBHLTH, HPAYMT, DSRCH, PATRQT.
- `includedSources.purpose.refUri` (string, required): The reference URL. Should be a valid URL. Allows alpha numeric character and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `includedSources.hip` (object): Identifier and name of the health information provider.
- `includedSources.hip.id` (string, required): The service ID of the health information provider. Allows alpha numeric character and special characters like [A-Z a-z 0-9]+[A-Z a-z 0-9 //_//-]*[A-Z a-z 0-9]$
- `includedSources.hip.name` (string, required): The name of the health information provider. Allows alpha numeric and special characters like "^[a-zA-Z]+[A-Za-z0-9_\\-@,().\\s\\xa0:/]+"
- `includedSources.hip.type` (string, required): The type of the health information provider. Allows alpha numeric and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `includedSources.period` (object, required)
- `includedSources.period.from` (string, required): Should be UTC date time in ISO format.Allows alpha numeric and special characters like "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$"
- `includedSources.period.to` (string, required): Should be UTC date time in ISO format.Allows alpha numeric and special characters like "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$"
- `excludedSources` (object[]): Excluded sources, carrying the list of hi types.
- `excludedSources.hiTypes` (string[], required): Types of health information document.
- `excludedSources.purpose` (object)
- `excludedSources.purpose.text` (string, required) One of: Care Management, Break the Glass, Public Health, Healthcare Payment, Disease Specific Healthcare Research, Self Requested.
- `excludedSources.purpose.code` (string, required) One of: CAREMGT, BTG, PUBHLTH, HPAYMT, DSRCH, PATRQT.
- `excludedSources.purpose.refUri` (string, required): The reference URL. Should be a valid URL. Allows alpha numeric and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `excludedSources.hip` (object): Identifier and name of the health information provider.
- `excludedSources.hip.id` (string, required): The service ID of the health information provider. Allows alpha numeric character and special characters like [A-Z a-z 0-9]+[A-Z a-z 0-9 //_//-]*[A-Z a-z 0-9]$
- `excludedSources.hip.name` (string, required): The name of the health information provider. Allows alpha numeric and special characters like "^[a-zA-Z]+[A-Za-z0-9_\\-@,().\\s\\xa0:/]+"
- `excludedSources.hip.type` (string, required): The type of the health information provider. Allows alpha numeric and special characters like "^[a-zA-Z0-9_\\-@,. \":/]{0,255}$"
- `excludedSources.period` (object, required)
- `excludedSources.period.from` (string, required): Should be UTC date time in ISO format.Allows alpha numeric and special characters like "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$"
- `excludedSources.period.to` (string, required): Should be UTC date time in ISO format. Allows alpha numeric and special characters like "\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}.\\d{3}Z$"

## Responses

- `202`: Accepted
  See The callback never arrives: /docs/hiecm/v3/troubleshooting/callback-never-arrives
- `400`: Bad Request
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `401`: Unauthorized
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `404`: Not Found
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `500`: Internal Server Error
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
- `503`: Service Unavailable
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors
