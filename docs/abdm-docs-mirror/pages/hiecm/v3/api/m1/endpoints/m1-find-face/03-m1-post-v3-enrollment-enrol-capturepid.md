# Check the status of the transaction ID

`POST /abha/api/v3/enrollment/enrol/capturePID`

Verify the status of a transaction ID that was generated during the invocation of the <code>auth/init</code> API. It serves as a follow-up mechanism to ensure that the transaction is still valid, active, and has not expired or been invalidated. <br> <br> Wait for PID capture and submission confirmation from the ABHA App. The response of the API will return status of that transactionId. It can be either <strong>PENDING,VERIFIED,FAILED,COMPLETE.</strong> <br> <br> Once the status in the response of this API is returned as <strong> COMPLETE </strong>, it indicates that the face authentication process has been successfully completed. At this stage, the next step is to invoke the <code>/enrollment/enrol/byAadhaar</code> (You can find this API in ABHA ENROLLMENT Via Aadhaar section) API to proceed further. <br><br>User can poll the <code>/capturePID</code> API in every 5 - 10 seconds interval to check the status of face capture process or alternatively skip this step and call the <code>/enrollment/enrol/byAadhaar</code> API once they see the PID submission success message in the ABHA app.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/v3/enrollment/enrol/capturePID \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'Content-Type: application/json' \
  --data '{
  "scope": [
    "abha-enrol",
    "face-verify"
  ],
  "txnId": "ea1dc7aa-d7c3-40ab-bee8-84c6f1eb90fa"
}'
```

## Authorization

- `Authorization` (bearer token, required)

## Headers

- `REQUEST-ID` (string, required)
- `TIMESTAMP` (string, required)

## Body

- `scope` (string[], required)
- `txnId` (string, required)

## Responses

- `200`: The 200 response code indicates a successful request. The reponse of the API will return status of that transactionId. It can be either <strong>PENDING,VERIFIED,FAILED,COMPLETE. </strong>
- `400`: The 400 response code indicates a bad request.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors
- `401`: The 401 response code indicates an unauthorized request. In this context, it refers to the lack of proper authentication during the operation of the Invalid Credentials
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `500`: <b>Internal Server Error</b><br><br>  An Internal Server Error (500) indicates that the server encountered an unexpected condition that prevented it from fulfilling the request.
  See Error codes for this module: /docs/hiecm/v3/api/m1/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "status": "PENDING",
  "message": "Awaiting PID capture"
}
```
