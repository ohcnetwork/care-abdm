# Retrieve the benefit details associated with a specific ABHA number

`GET /abha/api/v3/profile/benefit/abha/{abhanumber}`

Retrieve the benefit details associated with a specific ABHA (Ayushman Bharat Health Account) number. By providing the ABHA number in the request, the API returns information about the benefits linked to that account. This includes details such as the type of benefits, eligibility, and any other relevant information associated with the ABHA number. This endpoint ensures that users can access and manage their health benefits securely and efficiently.

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/profile/benefit/abha/{abhanumber} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'BENEFIT_NAME: {{Benefit Name}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `BENEFIT_NAME` (string, required)
- `REQUEST-ID` (string, required)
- `TIMESTAMP` (string, required)

## Path parameters

- `abhanumber` (string, required)

## Responses

- `200`: This scenario occurs when an ABHA (Ayushman Bharat Health Account) is linked to one or multiple benefit programs. Each benefit program may offer different types of health services, financial assistance, or other healthcare-related benefits. The system ensures that the ABHA number is correctly associated with all the relevant benefit programs, allowing the user to access and manage their benefits efficiently
- `401`: The 401 response code indicates an unauthorized request. In this context, it refers to the lack of proper authentication
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `404`: The 404 response code indicates that the requested resource could not be found. In the context of searching for an ABHA (Ayushman Bharat Health Account) number using the endpoint API, this error occurs when the specified ABHA number does not exist or cannot be found in the system.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `500`: <b>Internal Server Error</b><br><br>  An Internal Server Error (500) indicates that the server encountered an unexpected condition that prevented it from fulfilling the request.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "abhaNumber": "<ABHA_NUMBER>",
  "programme": [
    {
      "benefitName": "Poshan Abhiyaan"
    },
    {
      "benefitName": "Test Benefit Program"
    },
    "... 1 more of the same shape"
  ]
}
```
