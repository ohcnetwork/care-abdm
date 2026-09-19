# Get child ABHA address

`GET /abha/api/v3/enrollment/profile/children`

Retrieve the ABHA (Ayushman Bharat Health Account) profile of a child, making it especially useful for managing minors’ health records and information. It provides essential details such as the child’s ABHA number, date of birth, name, and gender. Additionally, this endpoint allows users to access all child records linked to a parent’s ABHA number.

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/profile/children \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'Content-Type: application/json' \
  --header 'BENEFIT_NAME: {{Benefit Name}}' \
  --header 'X-token: Bearer {{X-token}}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `TIMESTAMP` (string, required)
- `REQUEST-ID` (string, required)
- `Content-Type` (string, required)
- `BENEFIT_NAME` (string, required)
- `X-token` (string, required)

## Responses

- `200`: Indicates a successful request. The response includes the updated child ABHA profile details
- `401`: Indicates an unauthorized request due to invalid credentials
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: <b>Internal Server Error</b><br><br>  An Internal Server Error (500) indicates that the server encountered an unexpected condition that prevented it from fulfilling the request.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "parentAbhaNumber": "<ABHA_NUMBER>",
  "mobileNumber": "******0903",
  "childrenCount": 2,
  "children": [
    {
      "dateOfBirth": "<DOB>",
      "name": "<NAME>",
      "gender": "M",
      "phrAddress": "<ABHA_ADDRESS>",
      "ABHANumber": "<ABHA_NUMBER>"
    },
    {
      "dateOfBirth": "<DOB>",
      "name": "<NAME>",
      "gender": "F",
      "phrAddress": "<ABHA_ADDRESS>",
      "ABHANumber": "<ABHA_NUMBER>"
    }
  ]
}
```
