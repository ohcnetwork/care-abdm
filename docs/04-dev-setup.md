# 04 — Local dev setup (as of 2026-09-15, ADR-011)

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
- Use `ABDM_HSP_URL=https://apihspsbx.abdm.gov.in`.
  Only the HRP service registration uses this host.
  The gateway host answers HTTP 503 for that path (findings, 2026-09-14).
- Use `ABDM_ABHA_URL=https://abhasbx.abdm.gov.in/abha/api`.
  Do not add `/v3`.
- M2 callback signature env: `ABDM_CALLBACK_SIGNATURE_HEADER=Authorization`.
  The docs do not publish the header name.
  The code fails closed.
- Migrations restarted at `0001_initial` on 2026-09-15. A database that carries the old `abdm_*`
  tables must be reset once (local test data only):
  `cd ~/ohc.network/care && set -a && . ./.env && set +a && .venv/bin/python manage.py shell -c "from django.db import connection; c=connection.cursor(); [c.execute(f'DROP TABLE IF EXISTS \"{t}\" CASCADE') for t in connection.introspection.table_names() if t.startswith('abdm_')]; c.execute(\"DELETE FROM django_migrations WHERE app='abdm'\")"`
  then `.venv/bin/python manage.py migrate abdm`.
- Apply migrations after every pull:
  `cd ~/ohc.network/care && set -a && . ./.env && set +a && .venv/bin/python manage.py migrate abdm`.
- Run Care:
  `cd ~/ohc.network/care && set -a && . ./.env && set +a && .venv/bin/python manage.py runserver 0.0.0.0:8000`.
- Register the bridge (callback) URL after a deploy or a tunnel URL change. It is 1 per `clientId`:
  `cd ~/ohc.network/care && set -a && . ./.env && set +a && .venv/bin/python manage.py abdm_register_bridge_url`
  (`--dry-run` prints the URL only). The command also prints the live bridge state. A superuser can do
  the same from `/admin/abdm` (admin sidebar → ABDM). Run it before the HRP service registration.
- Run Celery. Every callback handler and the Encounter auto-link run in the worker:
  `cd ~/ohc.network/care && ./scripts/celery-dev.sh`.
  The worker does not reload plug code: `celery-dev.sh` watches only the Care tree, and a worker started
  by hand watches nothing. After a change under `backend/src/abdm/` restart it, or send it
  `kill -HUP <celery main pid>` (Celery re-executes itself in the same terminal with the same
  environment; done on 2026-09-17, restart took 20 s). `runserver` reloads the plug on its own.
- HIP ID is per facility and is read from the gateway, not typed: after "Register HRP service" the
  plug stores the service id the registry issued (`IN1410000232_1` for facility `IN1410000232`) and
  sends it as `X-HIP-ID`. The setup page re-reads it on every load. A call sent with the bare HFR id
  is accepted with 202 but its callback is never delivered (2026-09-17).
- Probes: `GET /api/abdm/health`; `GET /api/abdm/gateway/status`; `GET /api/abdm/bridge` (live gateway view); `GET /api/abdm/admin/overview` (superuser; backs `/admin/abdm`).
- Callback log (superuser): `GET /api/abdm/callbacks?limit=20`; `GET /api/abdm/callbacks/<callback_id>`.
- Encounter link state: `GET /api/abdm/encounters/<encounter_id>/care-context`.
- Outside production the user-initiated link OTP is fixed: `123456` (Care core uses the same rule for login OTPs).

## Frontend

- Plug source: `frontend/`.
  It keeps the reference plug chassis, request helper, plug wrapper, and vendored UI components.
- Container class: `.care-abdm-fe-container`.
- i18n namespace: `care_abdm_fe`.
  It must equal PlugConfig `meta.name`.
- Build and serve:
  `npm run build && npx vite preview --port <port>` (Rithvik serves it through `portless`; observed on 4664 on 2026-09-15).
- The MFE serves `/assets/remoteEntry.js`. Every build changes the chunk hashes: hard-refresh the host after a build, or the console shows 404s for the old `/assets/*.js` names.
- Care DB plug config:
  `PlugConfig(slug="abdm", meta={url, name: "care_abdm_fe", plug: "abdm"})`. `meta.url` must be the port the preview runs on.
- care_fe host:
  `cd ~/ohc.network/care_fe && npx vite --port 4000`.
- Point `REACT_CARE_API_URL` at `http://localhost:8000`.
  You can also use the `care-local.localhost` URL map in `.env.local`.

## Bruno collection

- Collection: `bruno/`.
  It calls the plug routes on Care. It does not call ABDM directly.
- Open it in 1 of 2 ways.
  Use "Open Collection" and select `bruno/`.
  Use "Open Workspace" and select the repository root, which holds `workspace.yml`.
  Bruno 4 shows "Invalid workspace: workspace.yml not found" if you open a folder that has no `workspace.yml`.
- It mirrors `backend/src/abdm/urls.py`.
  Change both files together.
- Folders: `auth`, `probes`, `bridge`, `facility`, `abha-enrol`, `abha-login`,
  `transactions`, `patient`, `encounters`, `callbacks`, `scan-share`.
- Select the `local` environment.
  Set the secret variables `careUsername` and `carePassword`. `careToken` and `careRefreshToken`
  are secret variables too, so a saved token never lands in the file.
- Send `auth > 1. Login` first.
  The script saves `careToken` to the environment.
- The OTP requests save `txnId`.
  The callback list saves `callbackId`.
- The collection pre-request script sets `requestId` and `timestamp`.
  The callback requests send them as `REQUEST-ID` and `TIMESTAMP`.
- The secret variables hold the credentials and the personal data.
  Bruno keeps these values out of the file.
- Run it from a terminal:
  `cd bruno && npx @usebruno/cli run probes --env local`.
- Caution: the callback requests write a row in `AbdmCallback` before the signature check.
  Use a development database only.

## Tunnel (ADR-005)

- Tunnel name: `care-abdm-sbx`.
- Public hostname: `https://care-abdm-sbx.rithviknishad.dev`.
- Target: local Care on `http://localhost:8000`.
- Bridge URL: registered on 2026-09-09 with HTTP 202.
- Run command: `cloudflared tunnel run care-abdm-sbx`.
