# 06 — Verification playbook

The user runs Care (:8000), care_fe (:4000), the MFE preview (:4174) and the cloudflared tunnel in
his own terminals. **Do not start or kill servers.** Hand him commands (`04-dev-setup.md`).
Everything below works without a live server.

## Backend

```sh
cd ~/ohc.network/care && set -a && . ./.env && set +a
.venv/bin/python manage.py check
.venv/bin/python manage.py makemigrations abdm --check --dry-run
.venv/bin/ruff check ~/ohc.network/care-abdm-sbx/backend/src --exclude '*/migrations/*'
.venv/bin/ruff format ~/ohc.network/care-abdm-sbx/backend/src
```

In-process HTTP against real auth and the real DB (the way Phase 2 was proven):

```sh
.venv/bin/python manage.py shell < script.py
```

where `script.py` uses `rest_framework.test.APIClient` with `force_authenticate(superuser)` and
posts to `/api/v1/patient/` / `/api/abdm/...`. Create fixtures (`AbhaTransaction`, `Patient`) in
the script and delete them at the end. Examples of what was checked: create-with-`txn_id` writes
both identifiers and `instance_identifiers`; `PUT` with unrelated change preserves ABHA; duplicate
txn 409; unknown txn 404; card without token 409. Write scratch scripts under the session files directory, not the repo.

M2 steps 1-2 use `/tmp/abdm_m2_smoke.py`.
Run it after `manage.py migrate abdm`.
It checks facility setup round-trip, callback fail-closed behavior, callback idempotency, local RS256 JWKS verification, and bridge action rows.

Real-sandbox calls (`curl` to `dev.abdm.gov.in` / `abhasbx.abdm.gov.in`) need the session token —
use `abdm.gateway.session.get_access_token()` from a shell, never paste the secret. Anything that
needs a real Aadhaar/mobile OTP is user-driven: ask him to click through the UI and report.

## Backend unit tests

```sh
cd ~/ohc.network/care && set -a && . ./.env && set +a
.venv/bin/python -m unittest discover -s /Users/rithviknishad/ohc.network/care-abdm-sbx/backend/tests -t /Users/rithviknishad/ohc.network/care-abdm-sbx/backend
```

Observed 2026-09-10: 8 tests ran in 0.228 s. Result: OK.

## Frontend

```sh
cd ~/ohc.network/care-abdm-sbx/frontend
npm run build          # tsc -b && vite build; must produce dist/assets/remoteEntry.js
npx eslint src         # 0 errors
grep -oh 't("abdm_[a-z_]*"' -r src | sort -u   # every key must exist in public/locale/en.json
```

Definition of done for the MFE is `remoteEntry.js` fetchable over HTTP with
`Access-Control-Allow-Origin: *` from the preview the user runs — a build alone is not proof.
The agent cannot see the UI; ask the user for a screenshot and record what it showed in
`03-roadmap.md`.

## Care core traps found so far (details in `findings.md` and the kiran skill caveats)

- `PatientIdentifier` rows are invisible until `patient.build_instance_identifiers()` is persisted.
- `auto_maintained` identifiers are dropped from create payloads.
- Extension schema fields need `x-ui.render_blacklist` or the host renders them as form inputs.
- `care/plug_config.py` local modifications can duplicate the `abdm` app label with `.env`
  `ADDITIONAL_PLUGS` (`04-dev-setup.md`).
- The host renders `FacilityHomeActions` inside a dropdown popup. The popup is a transformed
  ancestor, so a `position: fixed` panel in that subtree anchors to the popup. Do not open a
  dialog from that slot. Link to a plug page instead (ADR-009).

## M2 ops probes

- `GET /api/abdm/callbacks?limit=20` shows recent callback rows without raw body or headers.
- `GET /api/abdm/callbacks/<callback_id>` shows the full callback row. Only a superuser can use it.
- Use the detail probe to learn the real callback signature header.
