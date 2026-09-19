# P2 Management errors

Seeing a symptom rather than a code? Start at [Troubleshooting](/docs/hiecm/v3/troubleshooting/).

## Codes

| Code        | HTTP | Message             | Returned by                                    |
| ----------- | ---- | ------------------- | ---------------------------------------------- |
| `900902`    | 401  | Missing Credentials | `p2_get_v3_phr_app_login_profile`              |
| `ABDM-9999` | 400  | Invalid LoginId     | `p2_post_v3_phr_app_login_profile_request_otp` |

Every code above is recorded in the specification that owns it. The aggregated list across modules is at [error codes](/docs/hiecm/v3/reference/error-codes).

[Next Still stuck? Ask for help Where to file what you hit, so the answer lands back in these pages.](/docs/support)
