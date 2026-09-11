# abdm (CARE backend plug)

ABDM HIE-CM v3 integration for CARE, built solely from https://abdm-docs.dev.eka.care.
Design docs and ADRs live in `../docs/`.

## Install into Care (local dev)

In `care/plug_config.py`:

```python
from plugs.plug import Plug
plugs = [Plug(name="abdm", package_name="/absolute/path/to/care-abdm-sbx/backend", version="", configs={})]
```

Configuration (env or `PLUGIN_CONFIGS["abdm"]`): `ABDM_CLIENT_ID`, `ABDM_CLIENT_SECRET`,
`ABDM_GATEWAY_URL` (default `https://dev.abdm.gov.in`), `ABDM_ABHA_URL`,
`ABDM_CM_ID` (`sbx`|`abdm`), `ABDM_CALLBACK_BASE_URL`.

## Endpoints
- `GET /api/abdm/health`
- `GET /api/abdm/gateway/status` (authenticated) — creates/caches a gateway session.
