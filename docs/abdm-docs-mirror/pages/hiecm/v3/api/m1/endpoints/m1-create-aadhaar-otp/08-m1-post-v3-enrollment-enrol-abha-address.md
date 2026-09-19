# Create ABHA address

`POST /abha/api/v3/enrollment/enrol/abha-address`

Enrol a new ABHA address. It allows users to create a unique ABHA address that can be used for accessing and managing their health records. The endpoint ensures that the provided ABHA address is unique and valid..

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/abha-address \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "txnId": "{{txnId}}",
  "abhaAddress": "{{ABHA Address}}",
  "preferred": 1
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required)
- `TIMESTAMP` (string, required)

## Body

- `txnId` (string, required)
- `abhaAddress` (string, required)
- `preferred` (integer, required)

## Responses

- `200`: The 200 response code indicates a successful request. In this context, it refers to the successful operation of the Enroll ABHA Address API.
- `400`: The 400 response code indicates a bad request. In this context, it refers to various errors encountered during the operation of the Suggestion API.<br><br> <p><strong>Types of Suggestion API Errors:</strong></p> <ol> <li><strong>Invalid Preferred Flag:</strong> This error occurs when the transaction ID provided in the request is invalid. The transaction ID is essential for tracking the request and ensuring that the correct information is processed. An invalid transaction ID means the server cannot verify the request, leading to a failure in enrolling the ABHA address. .</li> </ol> <ol start="2"> <li><strong>Invalid Transaction Id:</strong>This error occurs when the preferred flag provided in the request is invalid. The preferred flag indicates the user’s preference for the suggested ABHA address. An invalid preferred flag means the server cannot process the user’s preference correctly, leading to a failure in enrolling the ABHA address.</li> </ol>
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: The 401 response code indicates an unauthorized request. In this context, it refers to the lack of proper authentication during the operation of the Invalid Credentials.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: <b>Internal Server Error</b><br><br>  An Internal Server Error (500) indicates that the server encountered an unexpected condition that prevented it from fulfilling the request.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "txnId": "23acf181-339d-4771-b532-5c5df4a28d19",
  "healthIdNumber": "<ABHA_NUMBER>",
  "preferredAbhaAddress": "<ABHA_ADDRESS>"
}
```
