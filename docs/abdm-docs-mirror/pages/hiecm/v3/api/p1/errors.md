# P1 Registration and login errors

Seeing a symptom rather than a code? Start at [Troubleshooting](/docs/hiecm/v3/troubleshooting/).

## Codes

| Code        | HTTP | Message                        | Returned by                                 |
| ----------- | ---- | ------------------------------ | ------------------------------------------- |
| `900902`    | 401  | Missing Credentials            | `p1_get_v3_phr_app_enrollment_isexists`     |
| `ABDM-1107` | 400  | Invalid combinations of scopes | `p1_post_v3_phr_app_login_verify`           |
| `ABDM-1211` | 400  | User not found.                | `p1_post_v3_phr_app_login_search`           |
| `ABDM-9999` | 400  | Invalid LoginId                | `p1_post_v3_phr_app_enrollment_request_otp` |

Every code above is recorded in the specification that owns it. The aggregated list across modules is at [error codes](/docs/hiecm/v3/reference/error-codes).

[Next Still stuck? Ask for help Where to file what you hit, so the answer lands back in these pages.](/docs/support)
