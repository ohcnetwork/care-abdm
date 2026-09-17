"""
Callback paths, relative to the bridge URL, and the operation each one answers. Pure: no Django.

What the gateway really posts (observed 2026-09-17, first real callback):

    POST {bridgeUrl}/api/v3/hip/token/on-generate-token

The docs page for that callback names the path `/v3/hip/token/on-generate-token` while its curl
example carries `/api/v3/...`; the other result pages follow the same pattern, and the inbound
pages (discover, init, confirm, health-information) already spell `/api/v3/hip/...`. So the table
below holds every path without the `/api` prefix and `operation_for_path()` drops a leading
`/api` before it looks a path up. The older `/v0.5/...` spellings the prose still names are kept
as aliases. A path the table does not know is stored anyway (operation id empty) so the row
shows what the gateway sent (docs/findings.md E3).
"""

CALLBACK_OPERATION_BY_PATH = {
    # M1 Scan and Share (SHARE_PATIENT_PROFILE_701). Handled by abdm/share/service.py.
    "/patient-share/v3/share": "m1-receive-patient-share",
    "/v3/hip/patient/share": "m1-receive-patient-share",
    # M2 answers to calls this HIP made (abdm/hip/contexts.py).
    "/v3/hip/token/on-generate-token": "m2-on-generate-token-result",
    "/v3/link/on_carecontext": "m2-on-carecontext-result",
    "/v3/links/context/on-notify": "m2-on-context-notify-result",
    "/v3/patients/sms/on-notify": "m2-on-sms-notify-result",
    # M2 requests the gateway makes of this HIP (abdm/hip/discovery.py, consent.py, transfer.py).
    "/v3/hip/patient/care-context/discover": "m2-on-discovery-request",
    "/v0.5/care-contexts/discover": "m2-on-discovery-request",
    "/v3/hip/link/care-context/init": "m2-on-link-init",
    "/v0.5/links/link/init": "m2-on-link-init",
    "/v3/hip/link/care-context/confirm": "m2-on-link-confirm",
    "/v0.5/links/link/confirm": "m2-on-link-confirm",
    "/v3/consent/request/hip/notify": "m2-consent-hip-notify",
    "/v0.5/consents/hip/notify": "m2-consent-hip-notify",
    "/v3/hip/health-information/request": "m2-on-health-information-request",
    "/v0.5/health-information/hip/request": "m2-on-health-information-request",
}


def normalize_path(path: str) -> str:
    """`api/v3/x/`, `/api/v3/x` and `/v3/x` all become `/v3/x`."""
    path = "/" + (path or "").strip("/")
    return path.removeprefix("/api") if path.startswith("/api/") else path


def operation_for_path(path: str) -> str:
    """The operation id a callback path answers, or an empty string for a path the docs never named."""
    return CALLBACK_OPERATION_BY_PATH.get(normalize_path(path), "")
