# Get the ABHA address suggestion

`GET /abha/api/v3/enrollment/enrol/suggestion`

Provide suggestions for ABHA addresses based on the user’s personal information. It helps users find suitable ABHA addresses by generating a list of suggestions. This is particularly useful during the ABHA enrolment process to ensure that users can choose an appropriate and unique ABHA address.

```bash
curl --request GET \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/suggestion \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'TRANSACTION_ID: {{txnId}}' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `TRANSACTION_ID` (string, required)
- `REQUEST-ID` (string, required)
- `TIMESTAMP` (string, required)

## Responses

- `200`: The 200 response code indicates a successful request. In this context, it refers to the successful operation of the Suggestion API, suggestions for ABHA addresses based on the user’s personal information.
- `400`: The 400 response code indicates a bad request. In this context, it refers to various errors encountered during the operation of the Suggestion API.<br><br> <p><strong>Types of Suggestion API Errors:</strong></p> <ol> <li><strong>Abha Address - Invalid Transaction Id:</strong> This error occurs when the transaction ID provided in the request is invalid. The transaction ID is essential for tracking the request and ensuring that the correct information is processed..</li> </ol> <ol start="2"> <li><strong>Abha Address - Invalid Preferred Flag:</strong> This error occurs when the preferred flag provided in the request is invalid. The preferred flag indicates the user’s preference for the suggested ABHA address.</li> </ol>
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: The 401 response code indicates an unauthorized request. In this context, This error occurs when the transaction ID provided in the request is invalid. The transaction ID is essential for tracking the request and ensuring that the correct information is processed. An invalid transaction ID means the server cannot verify the request, leading to a failure in generating ABHA address suggestions.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: <b>Internal Server Error</b><br><br>  An Internal Server Error (500) indicates that the server encountered an unexpected condition that prevented it from fulfilling the request.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "23acf181-339d-4771-b532-5c5df4a28d19",
  "abhaAddressList": [
    "<ABHA_ADDRESS>",
    "<ABHA_ADDRESS>",
    "... 11 more of the same shape"
  ]
}
```
