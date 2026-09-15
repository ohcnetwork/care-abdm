# 01 — Sources: how to read the ABDM docs as an agent

Base: `https://abdm-docs.dev.eka.care`. Catalogue version 2026.08.24; skills built
2026-09-14 (from `/skills/index.json`). Mirror rebuilt 2026-09-15 (`docs/abdm-docs-mirror/MANIFEST.json`).

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
   before the first real call. From a shell without an MCP client, a 30-line Python script can call
   the server: `POST /mcp` with `initialize`, then `tools/call`; send
   `Accept: application/json, text/event-stream` and echo the `Mcp-Session-Id` header. Responses
   arrive as SSE `data:` lines. `validate_fhir` takes `bundle_json` as a string and returns
   `findings: null` for a clean bundle.
2. **Per-page markdown** — append `/index.md` to any docs URL
   (`…/docs/hiecm/v3/milestones/m2/index.md`). `.md` without `/index` 404s.
3. **`/llms.txt`** (page map, 21 KB) and **`/llms-full.txt`** (everything, 1.3 MB).
   Mirrored in `docs/abdm-docs-mirror/`, with every page as `pages/<url path>.md`
   (`pages/hiecm/v3/api/m2/endpoints/m2-hip-link-care-context.md` ↔ `/docs/hiecm/v3/api/m2/endpoints/m2-hip-link-care-context`).
   The `whats-new/` pages list the site's own change log; `2026-09-10` carries the "linked on callback" rule.
4. **Skills** — `/skills/index.json` lists nine skills; each has `SKILL.md` +
   `references/{scaffold,integrate,debug,test}.md`. Downloaded verbatim to
   `.agent/skills/abdm-*/`. `integrate.md` = endpoint tables with hosts and
   headers; `debug.md` = error codes; `test.md` = certification test matrix;
   `scaffold.md` = build-it-flow-by-flow loop that ends on an observed result.
5. **Per-endpoint pages** — `/docs/hiecm/v3/api/<module>/endpoints/<operation-id>`.
   The sitemap lists 11 gateway, 44 M1, 20 M2, 14 M3, 2 M4 operations
   (`docs/abdm-docs-mirror/sitemap.xml`). Some HIP-facing bodies live only on HIU-side pages:
   the consent notification on `m3-on-consent-request-notify-hip`, the data-push body on
   `m3-on-health-information-transfer`, the health-information request on
   `m3-hiu-health-information-request` and `p2-as-record-on-share` (findings H1, H3, H4).
6. **Interactive API reference** — `/reference/hiecm-{gateway,m1,m2,m3,m4}`.
   These are JS-rendered; use MCP `get_operation` instead.

## Sandbox facts (from `/getting-started/sandbox`, `/concepts/hip-hiu`)

| What | Sandbox | Header |
|---|---|---|
| Gateway incl. session | `https://dev.abdm.gov.in` | `X-CM-ID: sbx` |
| ABHA service (M1) | `https://abhasbx.abdm.gov.in/abha/api/v3/` | |
| Fingerprint/IRIS (M1) | `https://abhasbx.abdm.gov.in/abha/api/v3.1/` | |
| Production gateway | `https://apis.abdm.gov.in` | `X-CM-ID: abdm` |
| Production ABHA | `https://abha.abdm.gov.in/api/abha/v3/` | |

Credentials (`clientId`, `clientSecret`) and the callback base URL are issued
on the sandbox portal; the docs say "more than one sandbox host appears across
our published documents" — treat hosts as something to confirm on first call.

## Forbidden

See `00-context.md` §Hard rules. If a question cannot be answered from the
sources above, the answer is "the docs do not say" — record it in
`docs/findings.md` and ask Rithvik. Do not fill the gap from memory or from
another source.
