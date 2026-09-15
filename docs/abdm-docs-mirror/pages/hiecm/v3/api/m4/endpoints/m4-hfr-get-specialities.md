# List the specialities a facility can declare

`GET /v1.5/facility/get-specialities`

One of the two HFR master data calls whose path appears in text. Not
run against the ABDM sandbox, so the response shape is unconfirmed.

```bash
curl --request GET \
  --url https://apihspsbx.abdm.gov.in/v4/int/v1.5/facility/get-specialities \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Responses

- `200`: The speciality list. NHA's document carries the response as a screenshot, so the field list is not transcribed.
