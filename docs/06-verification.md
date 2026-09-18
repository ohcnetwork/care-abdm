# 06 — Verification playbook

The user runs Care (:8000), care_fe (:4000), the MFE preview (:4174) and the cloudflared tunnel in
his own terminals. **Do not start or kill servers.** Hand him commands (`04-dev-setup.md`).
Everything below works without a live server.

## Backend

```sh
cd ~/ohc.network/care && set -a && . ./.env && set +a
.venv/bin/python manage.py check
.venv/bin/python manage.py makemigrations abdm --check --dry-run
(cd ~/ohc.network/care-abdm-sbx/backend && ~/ohc.network/care/.venv/bin/ruff check src tests && ~/ohc.network/care/.venv/bin/ruff format --check src tests)
```

`manage.py check` cannot run on this machine since 2026-09-17: Care imports weasyprint, which needs
`libgobject-2.0-0`, and glib is not installed. This is a Care environment gap, not a plug problem. To
prove the plug's Django modules load, stub weasyprint and import them, then run `makemigrations --check`
in the same process (see the scratch script pattern below).

Ruff reads `backend/pyproject.toml` (line length 120, `abdm` first-party, migrations excluded), so run it
from the `backend` directory; run from the Care directory it silently picks up Care's config instead.

In-process HTTP against real auth and the real DB (the way Phase 2 was proven):

```sh
.venv/bin/python manage.py shell < script.py
```

where `script.py` uses `rest_framework.test.APIClient` with `force_authenticate(superuser)` and
posts to `/api/v1/patient/` / `/api/abdm/...`. Create fixtures (`AbhaTransaction`, `Patient`) in
the script and delete them at the end. Examples of what was checked: create-with-`txn_id` writes
both identifiers and `instance_identifiers`; `PUT` with unrelated change preserves ABHA; duplicate
txn 409; unknown txn 404; card without token 409. Write scratch scripts under the session files directory, not the repo.

M2 uses `m2_smoke.py` in the session files directory (2026-09-15). Run it after `manage.py migrate abdm`:

```sh
.venv/bin/python manage.py shell < ~/.copilot/session-state/<session>/files/m2_smoke.py
```

It patches only `gateway.outbound.requests.request` (records every call, answers 202; answers the
bridge-services read with a bridge id), `gateway.outbound.get_access_token`,
`callbacks.views.verify_callback_signature`, the 2 Celery `.delay` calls (run inline), and
`care.utils.sms.send_text_message`. Everything else is real: Care auth, the DB, the routes, the
FHIR builders and the crypto. It drives 15 stages: facility PUT and bridge GET; HRP registration;
Encounter save → link token → link → notify with the 3 result callbacks; duplicate callback;
discovery (match and no match); link init → wrong OTP → right OTP; consent GRANTED and REVOKED
(both path variants); health-information request → encrypted push → **HIU-side decrypt and MD5
check** → notify TRANSFERRED; a wider date range refused (`ABDM-1063`); SMS deep link; the 403 on
bridge registration; Scan and Share token `OPD1-001`. It snapshots every plug table first and deletes only the rows it created (a 2026-09-15 version
deleted all outbound and callback rows; do not use it), then restores the facility extension. Expected last lines: `M2 SMOKE OK — outbound calls: 31 callbacks: 54`
and `cleanup done`.

FHIR bundles use `fhir_smoke.py` in the same directory. It builds the 3 record types from fixture
CARE data, writes them to files and runs MCP `validate_fhir` on each
(`python3 /tmp/mcp_tool.py validate_fhir '{"record_type":"<type>"}' --file <bundle>`; the helper
script is in the session archive and takes 1 minute to recreate from `docs/01-sources.md`).
Expected: `findings: null` for each type.

Real-sandbox calls (`curl` to `dev.abdm.gov.in` / `abhasbx.abdm.gov.in`) need the session token —
use `abdm.gateway.session.get_access_token()` from a shell, never paste the secret. Anything that
needs a real Aadhaar/mobile OTP is user-driven: ask him to click through the UI and report.

## Backend unit tests

```sh
cd ~/ohc.network/care && set -a && . ./.env && set +a
.venv/bin/python -m unittest discover -s /Users/rithviknishad/ohc.network/care-abdm-sbx/backend/tests -t /Users/rithviknishad/ohc.network/care-abdm-sbx/backend
```

Observed 2026-09-10: 8 tests ran. Result: OK.
Observed 2026-09-14: 14 tests ran. Result: OK (`test_share_rules.py` added).
Observed 2026-09-15: 41 tests ran in 0.4 s. Result: OK (`test_hip_rules.py`, `test_hip_crypto.py`, `test_fhir_bundles.py` added).
Observed 2026-09-15 (later): 46 tests. Result: OK (`test_callback_signature.py` rewritten: RS512, header auto-detect, unknown kid, HS256 refused).
Observed 2026-09-17: 54 tests. Result: OK (`test_callback_paths.py`: the `/api` prefix the gateway really sends; `HipServiceLookupTests` in `test_facility_rules.py`: the registry's `<facilityId>_<n>` service id).
Observed 2026-09-17 (later): 78 tests. Result: OK (`test_errors.py`: the ADR-012 classifier; `test_hip_rules.py` freshness test replaced).

Observed 2026-09-18: 90 tests. Result: OK (`test_sharing_rules.py` added for ADR-013).

The tests run without Django. Pure rules must live in a module with no Django import
(`abha/checksums.py`, `share/rules.py`, `facility/rules.py`, `hip/rules.py`, `hip/crypto.py`, `fhir/bundle.py`,
`callbacks/paths.py`).

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
  Use it to learn the real callback signature header (findings E2) and the real bodies (E8, G1, H1, H3).
- `GET /api/abdm/encounters/<id>/care-context` shows the link state and the last 10 gateway requests with their callbacks.
- `GET /api/abdm/bridge` shows the live gateway view of the bridge; a wrong `ABDM_CALLBACK_BASE_URL` shows as a URL mismatch on the setup page.

## Bruno parse check

```sh
cd /tmp && mkdir -p brucheck && cd brucheck && npm i @usebruno/lang >/dev/null && node -e '
const fs=require("fs"),p=require("path"),{bruToJsonV2}=require("@usebruno/lang");
function w(d){for(const f of fs.readdirSync(d)){const q=p.join(d,f);if(fs.statSync(q).isDirectory()){if(f!=="environments")w(q);continue}
if(f.endsWith(".bru")&&f!=="collection.bru"&&f!=="folder.bru")bruToJsonV2(fs.readFileSync(q,"utf8"))}}w(process.argv[1]);console.log("ok")' ~/ohc.network/care-abdm-sbx/bruno
```

Observed 2026-09-15: 59 files parsed, 47 requests, and the request paths matched `urls.py` both ways.
