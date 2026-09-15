# Log in to the HPR with a username and password

`POST /v4/int/api/v1/auth/authPassword`

One of the five HPR login routes, and the only one with a published
path. Returns the
`hprToken` that the HFR create call carries in its header.

The password is encrypted with the ABDM public certificate before it goes
in the body. Not run against the ABDM sandbox, so the request and
response shapes are unconfirmed.

```bash
curl --request POST \
  --url https://apihspsbx.abdm.gov.in/v4/int/v4/int/api/v1/auth/authPassword \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The `accessToken` from `POST /api/hiecm/gateway/v3/sessions`. Send it as `Authorization: Bearer <ACCESS_TOKEN>`.

## Responses

- `200`: A token for the professional. NHA's document shows the response as a screenshot, so the field list is not transcribed.
