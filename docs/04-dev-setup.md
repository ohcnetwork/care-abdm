# 04 — Local dev setup (as of 2026-09-10, M2 steps 1-2)

## Backend

- Plug source: `backend/` (package `abdm`, Django app label `abdm`).
- Care installs the plug through `~/ohc.network/care/.env` `ADDITIONAL_PLUGS`.
  Use this JSON entry: `{"name":"abdm","package_name":"/Users/rithviknishad/ohc.network/care-abdm-sbx/backend","version":""}`.
- Also install it with `.venv/bin/pip install -e backend`.
  Rithvik's local `plugs/manager.py` passes `-e`.
- Settings read env with prefix `ABDM_`.
  See `.env.example`.
- Names carry no environment marker.
  Sandbox and production differ only by value.
- The plug must not run with the legacy `care_abdm` plug.
  Both plugs use `ABDM_*` vars.
- Use `ABDM_GATEWAY_URL=https://dev.abdm.gov.in`.
  Do not add an `/api/hiecm` suffix.
- Use `ABDM_ABHA_URL=https://abhasbx.abdm.gov.in/abha/api`.
  Do not add `/v3`.
- M2 callback signature env: `ABDM_CALLBACK_SIGNATURE_HEADER=Authorization`.
  The docs do not publish the header name.
  The code fails closed.
- Apply the local migration after pull:
  `cd ~/ohc.network/care && set -a && . ./.env && set +a && .venv/bin/python manage.py migrate abdm`.
- Run Care:
  `cd ~/ohc.network/care && set -a && . ./.env && set +a && .venv/bin/python manage.py runserver 0.0.0.0:8000`.
- Run Celery for M2 callbacks:
  `cd ~/ohc.network/care && ./scripts/celery-dev.sh`.
- Probe: `GET /api/abdm/health`; `GET /api/abdm/gateway/status`.
- M2 probe: `GET /api/abdm/callbacks?limit=20`; `GET /api/abdm/callbacks/<callback_id>`.

## Frontend

- Plug source: `frontend/`.
  It keeps the reference plug chassis, request helper, plug wrapper, and vendored UI components.
- Container class: `.care-abdm-fe-container`.
- i18n namespace: `care_abdm_fe`.
  It must equal PlugConfig `meta.name`.
- Build and serve:
  `npm run build && npx vite preview --port 4174`.
- The MFE serves `/assets/remoteEntry.js`.
- Care DB plug config:
  `PlugConfig(slug="abdm", meta={url, name: "care_abdm_fe", plug: "abdm"})`.
- care_fe host:
  `cd ~/ohc.network/care_fe && npx vite --port 4000`.
- Point `REACT_CARE_API_URL` at `http://localhost:8000`.
  You can also use the `care-local.localhost` URL map in `.env.local`.

## Tunnel (ADR-005)

- Tunnel name: `care-abdm-sbx`.
- Public hostname: `https://care-abdm-sbx.rithviknishad.dev`.
- Target: local Care on `http://localhost:8000`.
- Bridge URL: registered on 2026-09-09 with HTTP 202.
- Run command: `cloudflared tunnel run care-abdm-sbx`.
