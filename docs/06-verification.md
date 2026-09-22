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

`manage.py check` could not run on this machine on 2026-09-17 (Care imports weasyprint, which needs
`libgobject-2.0-0`). On 2026-09-19 it ran again: `System check identified no issues (0 silenced).` If it
fails on weasyprint again, stub weasyprint and import the plug modules, then run `makemigrations --check`
in the same process.

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

`abha_link_conflict_smoke.py` (session files directory, 2026-09-19) proves the 4 link rules over
real auth, the real DB and the real routes: a second patient for an ABHA another patient holds is
refused with HTTP 400 and rolled back; the link API refuses the same ABHA with the same sentence;
an incomplete ABHA and a used request answer 400 too; a re-link of the same patient still answers
200. Expected last line: `LINK CONFLICT SMOKE OK — 14 checks passed, 0 failed`.

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

M3 uses `m3_smoke.py` (session `f18b6f36…`, 2026-09-19). Run it after `manage.py migrate abdm`:

```sh
.venv/bin/python manage.py shell < ~/.copilot/session-state/f18b6f36-94a4-4be3-968f-8a0ed28422c9/files/m3_smoke.py
```

It patches only `gateway.outbound.requests.request`, `gateway.outbound.get_access_token`,
`callbacks.views.verify_callback_signature` and `dispatch_callback.delay`. The script plays the HIP: it
reads the key material the plug sent in the health-information request, encrypts 2 bundles with
`abdm.hip.crypto` and posts them to the data push URL. It drives 17 stages: init body and headers; on-init;
refresh and on-status; GRANTED notify (ack, fetch); on-fetch (HI request); on-request; the push (decrypt,
MD5, records, notify RECEIVED, scrub); state and record detail; duplicate push; fetch again; housekeeping
on a stale request; REVOKED (erase, 410); DENIED; a refused init; erase-at housekeeping; validation and
the providers proxy; 403 without `can_view_clinical_data`. It snapshots every plug table first and
deletes only what it created. Expected last lines: `M3 SMOKE OK — outbound calls: 16 callbacks: 11` and
`cleanup done`.

M4 uses `m4_smoke.py` (session `3c44300c…`, 2026-09-21; the 2026-09-19 copy in session `f18b6f36…` is
older). Run it after `manage.py migrate abdm`; it needs a superuser without an HPR profile and 2 more
active users:

```sh
.venv/bin/python manage.py shell < ~/.copilot/session-state/3c44300c-ac9c-475c-9a40-53adc8e4055f/files/m4_smoke.py
```

It patches only `gateway.outbound.requests.request` and `gateway.outbound.get_access_token`. The script
is the NHPR: it generates an RSA key, serves it on `/api/v1/auth/cert`, and decrypts the mobile number,
the OTP and the password the plug sends, which proves the RSA/ECB/PKCS1 path. Since 2026-09-21 its fake
registry answers with the sandbox's own refusal shapes (HTTP 422 `HIS-1070` for a name search without
state or ownership, 422 `HIS-3008` for an unknown HPR ID, 422 `HIS-3028` for categories without `role`)
and it checks that a refused call's outbound row survives the request (J9). It drives the 4 tiers
(`03-roadmap.md` Phase 5) and the masters cache, then deletes what it created and restores the facility
extension. Expected last lines: `M4 SMOKE OK — NHPR calls: 58 total calls: 64` and `cleanup done`.

Since the afternoon of 2026-09-21 the script creates its own superuser (`abdm_m4_smoke_admin`) and
deletes it at the end: the real superuser holds a real HPR profile now, and the smoke must never touch it.

**Caution:** if the script dies inside its `finally` block, the cleanup is partial: the smoke superuser
stays, and facility 9 keeps the smoke's extension. Read `Facility.extensions["abdm"]` before a run and
restore it by hand after a crash (done once on 2026-09-21).

Read-only probes against the real registry (the way the 2026-09-21 facts were found) need no fixture:
`abdm.nhpr.client.search_facilities(facility_id="IN1410000232")`, `client.masters("lgd-states")`,
`client.call("m4-probe", "/v1.5/facility/get-master-data?type=OWNER", None, method="GET")` from
`manage.py shell`. Each leaves 1 `AbdmOutboundRequest` row, which is the evidence. Do not call a write
(`authPassword`, the HFR steps, `createHprIdWithPreVerified`) without the user.

The developer explorer (ADR-018) uses `dev_smoke.py` (session `3c44300c…`, 2026-09-21). Run it after
`manage.py migrate abdm`; it needs 1 superuser and 1 active non-superuser:

```sh
.venv/bin/python manage.py shell < ~/.copilot/session-state/3c44300c-ac9c-475c-9a40-53adc8e4055f/files/dev_smoke.py
```

It patches `requests.request` once (1 fake routed by host: the ABHA host answers the M1 paths, the
gateway host the rest), `get_access_token` on both transports, the callback signature check and
`dispatch_callback.delay` (inline; a handler that raises is recorded on the row, as the worker would).
It flips `ABDM_DEVELOPER_MODE` through `override_settings(PLUGIN_CONFIGS=…)` and `plugin_settings.reload()`.
9 stages: off (403 with the setting named); on (status); an M1 login leaves redacted rows; an M2
exchange through the 5 states; a handler traceback; an inbound with its ack; the 17 tables; readiness
and the worker heartbeat; a leak count over every answer. Expected last lines: `DEV SMOKE OK — checks: 44`
and `cleanup done`. It deletes only the rows it created and restores the heartbeat.

The M3 smoke of this session (`m3_smoke.py`, same directory) creates its own superuser like the M4
one: the real superuser holds a real HPR profile, and the requester-identifier check expects the medical
council registration.

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
Observed 2026-09-19: 118 tests in 0.8 s. Result: OK (`test_hiu_rules.py` added for ADR-014: every M3 parser is run on the example body of its docs page; the 6 M3 paths in `test_callback_paths.py`).
Observed 2026-09-19 (later): 149 tests in 0.9 s. Result: OK (`test_nhpr_rules.py` and `test_nhpr_crypto.py` added for ADR-015).
Observed 2026-09-19 (later): 152 tests in 1.3 s. Result: OK (`CarePrefillTests` in `test_nhpr_rules.py` for ADR-016).
Observed 2026-09-19 (later): 153 tests in 1.4 s. Result: OK (`test_validate_clamps_the_range_end_to_now` in `test_hiu_rules.py`, findings L9).
Observed 2026-09-21: 157 tests in 1.3 s. Result: OK (`MastersTests.test_sandbox_shapes_of_2026_09_21`, `test_owner_subtype_codes`, `test_parse_facility_search_keeps_the_sandbox_codes` in `test_nhpr_rules.py`; `RedactHeadersTests` in `test_callback_signature.py`).
Observed 2026-09-21 (later): 178 tests in 0.8 s. Result: OK (ADR-018: `test_dev_redact.py`, `test_dev_exchange.py`, `test_dev_tables.py`, `test_abha_audit.py`; the other session's 3 coordinate tests).

The tests run without Django. Pure rules must live in a module with no Django import
(`abha/checksums.py`, `share/rules.py`, `facility/rules.py`, `hip/rules.py`, `hip/crypto.py`, `hiu/rules.py`,
`nhpr/rules.py`, `nhpr/crypto.py`, `fhir/bundle.py`, `callbacks/paths.py`).

## Frontend

```sh
cd ~/ohc.network/care-abdm-sbx/frontend
npx tsc --noEmit -p tsconfig.app.json   # 0 errors
npm run build          # tsc -b && vite build; must produce dist/assets/remoteEntry.js
npx eslint src         # 0 errors (10 pre-existing fast-refresh warnings in ui/*)
grep -oh 't("abdm_[a-z_0-9]*"' -r src | sort -u   # every key must exist in public/locale/en.json
```

A key with a `{{placeholder}}` must be called with options (findings J10). Check:
`python3 -c 'import json,re,pathlib;d=json.load(open("public/locale/en.json"));src="\n".join(p.read_text() for p in pathlib.Path("src").rglob("*.tsx"));print([k for k,v in d.items() if "{{" in v and re.search(r"t\(\s*\""+re.escape(k)+r"\"\s*\)",src)])'`
must print `[]`.

URL query state (findings J11): every `?key=` write goes through `src/lib/query-params.ts`. Check the rule
without a browser (the URL below is the one a tab change wrote before the fix):
```sh
mkdir -p .tmp-check && npx esbuild src/lib/query-params.ts --bundle --platform=node --format=esm --outfile=.tmp-check/qp.mjs --log-level=warning \
&& node --input-type=module -e 'import {cleanQuery} from "./.tmp-check/qp.mjs"; const q=cleanQuery(Object.fromEntries(new URLSearchParams("tab=tables&exchange=undefined&row=undefined"))); console.log(JSON.stringify(q)); if ("exchange" in q || "row" in q) process.exit(1)'; rm -rf .tmp-check
```
must print `{"tab":"tables"}` and exit 0.

Field help (ADR-016) is keyed by label: `abdm_nhpr_help_<label key without abdm_>_{title,what,how,example}`.
A field whose 4 keys are missing renders without the icon, so the grep above does not cover them; check
with `python3 -c 'import json;d=json.load(open("public/locale/en.json"));print(len([k for k in d if k.startswith("abdm_nhpr_help_") and k.endswith("_what")]))'`
(125 on 2026-09-19).

Smokes (session files; real Care auth and DB; the network mocked): `m2_smoke.py` prints
`M2 SMOKE OK — outbound calls: 33`, `m3_smoke.py` prints `M3 SMOKE OK — outbound calls: 18 callbacks: 11`,
`m4_smoke.py` prints `M4 SMOKE OK — NHPR calls: 58 total calls: 64` (2026-09-21 run of the updated script;
ADR-016: every smoke links the facility through the registry mock; `m4_smoke.py` section G runs the
"Add a facility" create path and reads the admin overview rows).

Definition of done for the MFE is `remoteEntry.js` fetchable over HTTP with
`Access-Control-Allow-Origin: *` from the preview the user runs — a build alone is not proof.
Since 2026-09-22 the stylesheet and the Geist Mono woff2 are 2 more assets that must answer the same
way (the console skin, ADR-018 amendment). With the preview on `<port>`:
```sh
cd ~/ohc.network/care-abdm-sbx/frontend
css=$(ls dist/assets/*.css | xargs -n1 basename); font=$(ls dist/assets | grep geist-mono-latin-wght-normal)
for a in assets/remoteEntry.js assets/$css assets/$font; do curl -s -o /dev/null -H "Origin: https://care.localhost" -w "$a %{http_code} %{content_type} ACAO=%header{access-control-allow-origin}\n" http://localhost:<port>/$a; done
```
must print 3 lines with `200` and `ACAO=*`; the CSS must reference the font as `url(./geist-mono-…woff2)`
(relative), never `/assets/…`: `grep -o 'url([^)]*woff2)' dist/assets/*.css`.
The agent cannot see the UI; ask the user for a screenshot and record what it showed in
`03-roadmap.md`.

## Care core traps found so far (details in `findings.md` and the kiran skill caveats)

- `PatientIdentifier` rows are invisible until `patient.build_instance_identifiers()` is persisted.
- An exception from a plug's `post_save` receiver reaches Care's patient viewset. Only a DRF
  `ValidationError` whose `detail` dict holds `errors` becomes HTTP 400; anything else is HTTP 500
  and the desk reads "Something went wrong" (`02-care-host-contract.md`, "Errors from a plug signal").
- A plug view that raises a DRF `APIException` after an outbound call loses the `AbdmOutboundRequest`
  row: DRF's exception handler calls `set_rollback()` under `ATOMIC_REQUESTS` (findings J9). After a
  call, return the failure as a `Response`; never raise it. The M3 and M4 views do this.
- `auto_maintained` identifiers are dropped from create payloads.
- Extension schema fields need `x-ui.render_blacklist` or the host renders them as form inputs.
- `care/plug_config.py` local modifications can duplicate the `abdm` app label with `.env`
  `ADDITIONAL_PLUGS` (`04-dev-setup.md`).
- The host renders `FacilityHomeActions` inside a dropdown popup. The popup is a transformed
  ancestor, so a `position: fixed` panel in that subtree anchors to the popup. Do not open a
  dialog from that slot. Link to a plug page instead (ADR-009).
- raviger's `useQueryParams` setter writes a key set to `undefined` as the string "undefined"
  (findings J11). Write every `?key=` through `src/lib/query-params.ts`; never call the raviger
  setter with a spread that can hold `undefined`.
- A token-scope class (`.dark`, `.dark.abdm-console`) redefines variables, but `color` is inherited
  as a computed value: a descendant with no `text-*` class inherits the colour computed on
  `.care-abdm-fe-container` (the light theme's black), not the redefined variable. A scope class
  must set `color` (and `background-color`) on the element that carries it (ADR-018 corrections).
- `SheetBody` puts `className` on its scroller and the children in an inner `div`: a `grid gap-*`
  on it has 1 child. Put the grid on your own wrapper inside.

## Developer explorer (ADR-018)

With `ABDM_DEVELOPER_MODE=true`, the explorer is the first place to read after any run: `/abdm/developer`
→ Exchanges (filter by module, state, operation or REQUEST-ID; the REQUEST-ID of a runserver log line
opens the exchange) → the sheet shows the request, the answer, every callback and a traceback. The
Readiness tab names a blocker before a flow runs. The API behind it: `GET /api/abdm/dev/exchanges?request_id=<id>`,
`GET /api/abdm/dev/exchanges/<request_id>`, `GET /api/abdm/dev/inbound`, `GET /api/abdm/dev/tables/<name>`,
`GET /api/abdm/dev/readiness` (Bruno `dev/`). Every value is redacted by name and length, so a body may be
pasted into a finding as it came from the API.

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
Observed 2026-09-19: 60 requests parsed (`hiu/` folder and 6 M3 callbacks added); the route diff against `urls.py` is empty both ways.
Observed 2026-09-19 (later): 77 requests parsed (`nhpr/` folder added); the route diff against `urls.py` is empty both ways.
Observed 2026-09-19 (later): 82 requests parsed (`organizations/` folder, 5 requests, ADR-016); the 5 new paths match `urls.py`.
Observed 2026-09-19 (later): 81 requests parsed (`organizations/` renamed `add-facility/`, 4 requests on the organization-less routes; the list request folded into `admin/overview`).
