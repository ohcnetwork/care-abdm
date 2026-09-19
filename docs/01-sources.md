# 01 — Sources: how to read the ABDM docs as an agent

Base: `https://abdm-docs.dev.eka.care`. Catalogue version 2026.09.16; skills built
2026-09-16 (from `/skills/index.json`). Mirror rebuilt 2026-09-19 (`docs/abdm-docs-mirror/MANIFEST.json`).

## What changed on 2026-09-19 (mirror rebuild; the site republished on 2026-09-16)

- The API reference is rebuilt from the specification set of 16 September 2026. Every endpoint page
  now sits under a flow folder with a step number:
  `api/<module>/endpoints/<flow>/<nn>-<method>-<path>` (for example
  `api/m3/endpoints/m3-consent-management-data-flow-hiu/01-m3-post-consent-v3-request-init`). The old
  flat pages (`api/m2/endpoints/m2-hip-link-care-context`) still serve the old text, but they left the
  sitemap, so treat them as orphans and cite the flow pages.
- 450 pages (was 382): 11 gateway, 109 M1, 21 M2, 12 M3, 100 M4, 48 P1, 47 P2, 8 P3, 4 P4, 18 Scan and
  Pay, 6 subscription endpoint pages. New modules: `api/p4`, `api/scan-and-pay`, `api/subscription`.
  Withdrawn: `api/m1/apis`, `api/m4/undocumented`, `api/phr-services`, `resources/testing/*`, the
  `whats-new` pages before 2026-09-15.
- 12 skills (was 9): `abdm-gateway`, `abdm-p4`, `abdm-subscription`, `abdm-scan-and-pay` are new;
  `abdm-phr-services` is withdrawn; every `references/test.md` is withdrawn (scaffold, integrate,
  debug remain). `scripts/refresh-docs-mirror.py` now removes stale skill files.
- `reference/error-codes` shrank from 818 codes with a "What to do" column to 20 codes with
  HTTP / Message / Returned by columns. `build-it-well` still tells you to key handling to the
  action column. `scripts/generate-error-catalogue.py` refuses the new page, so
  `backend/src/abdm/error_catalogue.py` keeps the 818-code catalogue (findings A10).
- Facts that settle earlier findings: callbacks declare bearer auth in `Authorization`
  (`concepts/callback-authenticity`); the certs call needs the bearer token and `X-CM-ID`; the M2
  page writes the callback path with the `/api` prefix; the 4 HIP-inbound bodies (discover, link init,
  link confirm, consent notify) are published; `hiTypes` is 8 values with `Invoice`
  (`concepts/fhir`); the sandbox has 2 gateway hosts, not 4 (`concepts/gateway`).
- New: `troubleshooting/*` (5 symptom pages) and per-module `errors` pages.
- MCP: `catalogue_info` reports `catalogue_version 2026.09.16`, 305 operations; `list_operations`
  with `module: "m3"` lists the 7 HIU calls.

## Ways in, in order of preference

1. **MCP server (live)** — `https://abdm-docs-mcp.dev.eka.care/mcp`, streamable
   HTTP, no auth. Registered in the kiran Hermes profile as `mcp_servers.abdm-docs`
   (tools appear as `mcp_abdm-docs_*` after a Hermes restart). Tools observed
   on 2026-09-09 via `tools/list`:
   `catalogue_info`, `search_docs`, `get_atom`, `list_atoms`, `related_atoms`,
   `list_operations`, `get_operation` (exact OpenAPI fragment per operation),
   `validate_request` (local schema check before hitting sandbox),
   `decode_error`, `list_fhir_profiles`, `get_fhir_profile`, `get_fhir_example`,
   `validate_fhir`.
   Use `get_operation` for every request body we write, and `validate_request`
   before the first real call. From a shell without an MCP client, `scripts/abdm-docs-mcp.py <tool> '<json args>'` calls
   the server (`POST /mcp` with `initialize`, then `tools/call`; `Accept: application/json,
   text/event-stream`; the `Mcp-Session-Id` header echoed back; answers arrive as SSE `data:` lines). `validate_fhir` takes `bundle_json` as a string and returns
   `findings: null` for a clean bundle.
2. **Per-page markdown** — append `/index.md` to any docs URL
   (`…/docs/hiecm/v3/milestones/m2/index.md`). `.md` without `/index` 404s.
3. **`/llms.txt`** (page map) and **`/llms-full.txt`** (everything, 4 MB since 2026-09-16; it now
   carries NHCX too).
   Mirrored in `docs/abdm-docs-mirror/`, with every page as `pages/<url path>.md`
   (`pages/hiecm/v3/api/m2/endpoints/m2-abdm-hip-initiated-linking-hip/01-m2-post-hip-v3-link-carecontext.md`
   ↔ `/docs/hiecm/v3/api/m2/endpoints/m2-abdm-hip-initiated-linking-hip/01-m2-post-hip-v3-link-carecontext`).
   The `whats-new/` pages list the site's own change log; only 2026-09-15 and 2026-09-16 are in the
   sitemap now. The 2026-09-10 page ("linked on callback" rule) still serves at its old URL.
4. **Skills** — `/skills/index.json` lists 12 skills; each has `SKILL.md` +
   `references/{scaffold,integrate,debug}.md` (`abdm-fhir`: `generate.md`, `audit.md`). Downloaded
   verbatim to `.agent/skills/abdm-*/`. `integrate.md` = endpoint tables with hosts and
   headers; `debug.md` = error codes; `scaffold.md` = build-it-flow-by-flow loop that ends on an
   observed result. The `test.md` certification matrices were withdrawn on 2026-09-16.
5. **Per-endpoint pages** — `/docs/hiecm/v3/api/<module>/endpoints/<flow>/<nn>-<operation>`.
   The sitemap lists 11 gateway, 109 M1, 21 M2, 12 M3, 100 M4 operation pages
   (`docs/abdm-docs-mirror/sitemap.xml`). The HIP-facing bodies that once lived only on HIU-side
   pages are now on the M2 flow pages (`m2-consent-management-data-flow-hip/01`, `03`, `05`).
6. **Interactive API reference** — `/reference/hiecm-{gateway,m1,m2,m3,m4}`.
   These are JS-rendered; use MCP `get_operation` instead.

## Sandbox facts (from `/getting-started/sandbox`, `/concepts/hip-hiu`)

| What | Sandbox | Header |
|---|---|---|
| Gateway incl. session | `https://dev.abdm.gov.in` | `X-CM-ID: sbx` |
| ABHA service (M1) | `https://abhasbx.abdm.gov.in/abha/api/v3/` | |
| Production gateway | `https://apis.abdm.gov.in` | `X-CM-ID: abdm` (`troubleshooting/everything-returns-401`; `concepts/gateway` and `going-live` dropped the value on 2026-09-16) |
| Production ABHA | `https://abha.abdm.gov.in/api/abha/v3/` (`registries/abha`; `going-live` dropped it on 2026-09-16) | |

Since 2026-09-16 the docs list 2 gateway hosts only (`concepts/gateway`); the `apissbx` and `live`
hosts and the fingerprint/IRIS `v3.1` host were withdrawn. Credentials (`clientId`, `clientSecret`)
and the callback base URL are issued on the sandbox portal. Confirm a host on the first call.

## Forbidden

See `00-context.md` §Hard rules. If a question cannot be answered from the
sources above, the answer is "the docs do not say" — record it in
`docs/findings.md` and ask Rithvik. Do not fill the gap from memory or from
another source.
