# Submit the regenerate mobile OTP

`POST /apis/v1/doctors/regenerate-mobile-otp`

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/apis/v1/doctors/regenerate-mobile-otp \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>' \
  --header 'Content-Type: application/json' \
  --data '{
  "hpr_token": "<JWT TOKEN>",
  "officialMobile": "PFiI0AQJkAKIdLL6ytdJLKFObqXab9rwTvOEPHflksQBkMzIIb8HMDYUzZfN3AUdefedSbb+B4sPwi72lsaaNRkpXygWRF0GWntEwD/WL80JbXaW9DJkwPpDEzQpMYKKT17iCTp7pQer8337NZofO1D1aYiDfEnA9E1HMTyPCGFjvmbcL32hNqGsgpHKYNh4rHXCo4RwP5UQKWDYI1jLZqbWLp0a9GQu9nC1hyP5IR5LRCASzvhiRfrRk+Y660xuDSCvOKb+uUPcN3ZFA==xxxxxxxx"
}'
```

## Authorization

- `Authorization` (bearer token, required): M4 declares bearer authentication. The HPID calls publish POST /getManagementToken.

## Body

- `hpr_token` (string, required)
- `officialMobile` (string, required)

## Responses

- `200`: OK
- `404`: Not Found
