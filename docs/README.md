# care-abdm-sbx — knowledge base

This directory is the single source of context for the ABDM plug being built for
CARE. An agent that has never seen this repo should be able to read this folder
top to bottom and start work without asking anyone.

Read in this order:

| File | What it is |
|---|---|
| `00-context.md` | Why this repo exists, the hard rules, who the actors are |
| `01-sources.md` | The ONLY permitted ABDM source, how to read it (llms.txt, `.md` mirrors, MCP, skills) and what is forbidden |
| `02-care-host-contract.md` | What CARE (`care`, `care_fe`) actually exposes to a plug — cited to host files |
| `03-roadmap.md` | Phased plan with definition of done per phase; checkboxes record observed output |
| `04-dev-setup.md` | Local bring-up commands (user runs servers), env, tunnel, known traps |
| `05-codebase-map.md` | What every module does and the invariants to keep |
| `06-verification.md` | How to prove a change without starting servers; Care core traps |
| `findings.md` | Every gap in the ABDM docs, with the URL that should have answered it |
| `adr/` | Architecture decision records. One decision per file, numbered |
| `abdm-docs-mirror/` | Snapshot of the docs site (`llms.txt`, `llms-full.txt`, `sitemap.xml`, `skills-index.json`, `agent-setup-prompt.md`, and `pages/<url path>.md` for every page under `docs/hiecm/v3` and `docs/whats-new`). `MANIFEST.json` records the fetch date. Rebuild with `python3 scripts/refresh-docs-mirror.py` (`--diff` reports changes only). Snapshot only — prefer the live site / MCP |

Repo layout:

```
care-abdm-sbx/
  backend/          Django plug (pip-installable app for ohcnetwork/care)
  frontend/         MFE plug (Vite + module federation remote for ohcnetwork/care_fe)
  bruno/            Bruno collection for every plug route (mirrors backend/src/abdm/urls.py)
  scripts/          refresh-docs-mirror.py — rebuilds docs/abdm-docs-mirror and .agent/skills from the live site
  docs/             this knowledge base
  .agent/skills/    the docs site's own agent skills (abdm-m1 … abdm-fhir), downloaded verbatim
  .env.local        sandbox credentials — gitignored, never copy into docs
```

Conventions for editing docs:
- Every claim about ABDM cites a URL under `https://abdm-docs.dev.eka.care/docs/hiecm/v3/...`.
- Every claim about CARE cites `repo/path:line`.
- Decisions go in `adr/NNN-title.md` with Status / Context / Decision / Consequences.
- Nothing here is "done" without the observed command output that proves it.

Working with Rithvik: bring the seam design (routes, extension shape, care_fe slot needs) before
building; he runs all servers himself; real end-to-end over mocks; minimal-delta edits to care_fe,
PR-able (slot additions only without asking). Corrections he gives are durable — record them in
`findings.md` or an ADR.
