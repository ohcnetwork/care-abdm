# Receive a patient's shared profile

`POST /patient-share/v3/share`

Also known as: [HIP Callback] Receive Patient Profile Share.
**This endpoint is implemented by the HIP**, the ABDM Gateway forwards the
patient's profile to the HIP's registered callback URL when the patient
scans the HIP's QR code and consents to share their profile.

The HIP must respond with a 2xx status and subsequently call `POST /patient-share/v3/on-share`.

```bash
curl --request POST \
  --url https://abhasbx.abdm.gov.in/abha/api/patient-share/v3/share \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: <REQUEST_ID>' \
  --header 'TIMESTAMP: <TIMESTAMP>' \
  --header 'Content-Type: application/json' \
  --data '{
  "intent": "PROFILE_SHARE",
  "metaData": {
    "hipId": "CityGeneralHospital_HIP",
    "context": "123",
    "hprId": "testhpr@hpr.abdm"
  },
  "profile": {
    "patient": {
      "abhaNumber": "91-1234-5678-9012",
      "abhaAddress": "johnkumar@sbx",
      "name": "John Kumar",
      "gender": "M",
      "dob": "1990-01-15",
      "mobile": "9876543210",
      "kycPhoto": "{{base64_photo}}",
      "address": {
        "line": "123 Main Street",
        "district": "Mumbai",
        "state": "Maharashtra",
        "pinCode": "400001"
      }
    }
  }
}'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Headers

- `REQUEST-ID` (string, required): Unique UUID v4 per request. Used for idempotency and distributed tracing. Generate a fresh UUID for every call.
- `TIMESTAMP` (string, required): ISO 8601 UTC timestamp of the request.

## Body

- `intent` (string, required): Always `PROFILE_SHARE` for scan-and-share flows One of: PROFILE_SHARE.
- `metaData` (object, required)
- `metaData.hipId` (string, required): HIP identifier embedded in the QR code
- `metaData.context` (string, required): Counter or context value from the QR code
- `metaData.hprId` (string): Health Professional Registry ID of the scanning clinician
- `profile` (object, required)
- `profile.patient` (object)

## Responses

- `200`: Profile received by HIP
