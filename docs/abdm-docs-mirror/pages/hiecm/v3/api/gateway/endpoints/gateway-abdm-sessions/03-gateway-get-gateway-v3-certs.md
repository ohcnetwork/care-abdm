# Get the certificate information

`GET /api/hiecm/gateway/v3/certs`

Retrieve certificate information. When invoked, it provides details about the certificates used within the system. These certificates are crucial for ensuring secure communication and authentication between different components of the system. By using this API, users can access the necessary certificate information required for validating secure connections and maintaining the integrity of data exchanges.

```bash
curl --request GET \
  --url https://dev.abdm.gov.in/api/hiecm/gateway/v3/certs \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'REQUEST-ID: 18235d89-cb13-479d-ad71-7a57d5f669a8' \
  --header 'TIMESTAMP: 2022-10-06T15:10:00.587Z' \
  --header 'X-CM-ID: sbx'
```

## Authorization

- `Authorization` (bearer token, required): The access token from POST /api/hiecm/gateway/v3/sessions.

## Headers

- `REQUEST-ID` (string, required): Unique UUID for track the end to end request transaction
- `TIMESTAMP` (string, required): Actual time of the request was initiated, ISO 8601 represents date and time by starting with the year, followed by the month, the day, the hour, the minutes, seconds and milliseconds
- `X-CM-ID` (string, required): Suffix of the consent manager to which the request was intended

## Responses

- `200`: OK
- `204`: No Content
- `400`: Bad Request
- `401`: Unauthorized. The request carried no valid credentials, or the access token has expired. Obtain a fresh token from the session API and retry.
  See Everything returns 401: /docs/hiecm/v3/troubleshooting/everything-returns-401
- `403`: Forbidden. The caller is authenticated but is not permitted to perform this operation on this resource.
- `500`: Internal Server Error
- `503`: Service Unavailable

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "keys": [
    {
      "e": "AQAB",
      "kid": "AlRb5WCm8Tm9EJ_IfO9z06j9oCv51pKK",
      "kty": "RSA",
      "n": "mgmW7W5ZGF_G5cJevwYi8HiPcI-6qS_psnZxa4v3bkwAkyOoOd8-6ketrOI-ZA2PbRbGnxFfZHiI94rdFXJ4Q9ampscsz9NocTIPMPmWydJ8A50pZaYWyikYDSJiDltq7i3WspPKSOuQHr",
      "use": "sig",
      "x5c": [
        "MIICrzCCAZcCBgFy/3WZBjANBgkqhkiG9w0BAQsFADAbMRkwFwYDVQQDDBBjZW50cmFsLXJlZ2lzdHJ5MB4XDTIwMDYyOTA5NDEzNloXDTMwMDYyOTA5NDMxNlowGzEZMBcGA1UEAwwQY2VudHJhbC1yZWdpc3RyeTCCASIwDQYJK"
      ],
      "x5t": "EaMhYGUIvMkp8tvS",
      "x5t2": "vGer6Pt8AhZn8RlbHhAFksOCcGf3u1UWU7Qq",
      "alg": "RS256"
    }
  ]
}
```
