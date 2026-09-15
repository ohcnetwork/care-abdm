# PHR - Fetch Care Context Bundle URL

`GET /api/care-context-link/phr/care-context/bundle-url/{careContextLinkId}`

Returns the download URLs for the FHIR bundles of one linked care context, with the fetch status.

```bash
curl --request GET \
  --url https://phrsbx.abdm.gov.in/api/care-context-link/phr/care-context/bundle-url/{careContextLinkId} \
  --header 'Authorization: Bearer <ACCESS_TOKEN_FROM_SESSIONS_CALL>'
```

## Authorization

- `Authorization` (bearer token, required): The access token from `POST /api/hiecm/gateway/v3/sessions`.

## Path parameters

- `careContextLinkId` (string, required): Passed as a path segment.

## Responses

- `200`: Example values, scrubbed.
- `400`: Example values, scrubbed.
  See Error codes for this module: /docs/hiecm/v3/api/p2/errors

Shape of the 200 response, generated from the schema. The values are placeholders, not a captured response:

```json
{
  "lockerView": null,
  "fetchRecordStatus": "SUCCESS",
  "bundleUrls": [
    {
      "id": 873302,
      "careContextLinkId": 496112,
      "bundleUrl": "nithishjanithi@sbx/DigiLocker_NEGD/25ac532f-178d-5885-9bcb-b82052f345eb_20260604192056317009/<TXN_ID>.json",
      "transactionId": "<TXN_ID>",
      "dateCreated": "2026-06-12 15:32:34.231",
      "dateModified": "2026-06-12 15:32:34.231"
    }
  ]
}
```
