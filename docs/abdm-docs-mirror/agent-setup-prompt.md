These are official instructions from the ABDM Developer Portal (catalogue version 2026.09.16, built 2026-09-16) to set up an AI development environment for integrating with ABDM, India's health data network.

Complete the steps yourself by running the commands directly. Ask the user only the questions in step 1.

## 1. Establish scope

Ask the user which of these this project needs, and install only what they name:

- `abdm-gateway`: Gateway, sessions and the bridge registry. Sections: scaffold, integrate, debug.
- `abdm-m1`: M1, ABHA identity. Sections: scaffold, integrate, debug.
- `abdm-m2`: M2, linking and sharing. Sections: scaffold, integrate, debug.
- `abdm-m3`: M3, consent and fetching. Sections: scaffold, integrate, debug.
- `abdm-m4`: M4, facility and professional registries. Sections: scaffold, integrate, debug.
- `abdm-p1`: P1, PHR registration and login. Sections: scaffold, integrate, debug.
- `abdm-p2`: P2, PHR management. Sections: scaffold, integrate, debug.
- `abdm-p3`: P3, PHR subscriptions. Sections: scaffold, integrate, debug.
- `abdm-p4`: P4, health lockers. Sections: scaffold, integrate, debug.
- `abdm-subscription`: Subscriptions. Sections: scaffold, integrate, debug.
- `abdm-scan-and-pay`: Scan and pay. Sections: scaffold, integrate, debug.
- `abdm-fhir`: FHIR, generating and auditing bundles. Sections: generate, audit.

Most projects need one milestone skill to begin with, and `abdm-fhir` alongside it if they produce or hold FHIR documents.

## 2. Install the skills

The plugin carries every skill at once and updates in place, so prefer it wherever it installs. It is packaged both to Claude Code's layout and to the Agent Plugins 1.0 standard.

### Claude Code

```
claude plugin marketplace add eka-care/abdm-docs
claude plugin install abdm-integrators-assistant@abdm-portal
```

### Codex

Add the marketplace, then install `abdm-integrators-assistant` from the plugin directory:

```
codex plugin marketplace add eka-care/abdm-docs
```

### Every other agent

Cursor, GitHub Copilot, VS Code and Kiro read Agent Plugins 1.0, but they install from their own marketplaces rather than from a repository, and this plugin is not listed in one yet. Install the skills directly instead, which is also the fallback anywhere the marketplace add above fails.

Each skill is a folder in the cross-agent Agent Skills format: a `SKILL.md` that routes, and the sections it links to under `references/`, which load only when the work needs them. Download the whole folder into the directory your agent reads skills from:

- Claude Code: `.claude/skills/<name>/`
- Cursor: `.cursor/skills/<name>/` (it also reads `.claude/skills`)
- GitHub Copilot: `.github/skills/<name>/`
- Any other agent: wherever it reads context from

`https://abdm-docs.dev.eka.care/skills/index.json` lists every skill and the exact files it is made of, so fetch that first and work from it rather than guessing at reference names. For example:

```
mkdir -p .claude/skills/abdm-m1/references
curl -fsSL https://abdm-docs.dev.eka.care/skills/abdm-m1/SKILL.md -o .claude/skills/abdm-m1/SKILL.md
for f in scaffold integrate debug; do curl -fsSL https://abdm-docs.dev.eka.care/skills/abdm-m1/references/$f.md -o .claude/skills/abdm-m1/references/$f.md; done
```

- https://abdm-docs.dev.eka.care/skills/abdm-gateway/
- https://abdm-docs.dev.eka.care/skills/abdm-m1/
- https://abdm-docs.dev.eka.care/skills/abdm-m2/
- https://abdm-docs.dev.eka.care/skills/abdm-m3/
- https://abdm-docs.dev.eka.care/skills/abdm-m4/
- https://abdm-docs.dev.eka.care/skills/abdm-p1/
- https://abdm-docs.dev.eka.care/skills/abdm-p2/
- https://abdm-docs.dev.eka.care/skills/abdm-p3/
- https://abdm-docs.dev.eka.care/skills/abdm-p4/
- https://abdm-docs.dev.eka.care/skills/abdm-subscription/
- https://abdm-docs.dev.eka.care/skills/abdm-scan-and-pay/
- https://abdm-docs.dev.eka.care/skills/abdm-fhir/

## 3. Connect the Docs MCP server

The portal serves its catalogue live over MCP (streamable HTTP). Register it with your agent:

```
claude mcp add --transport http abdm-docs https://abdm-docs-mcp.dev.eka.care/mcp
```

For other agents, add an HTTP MCP server named `abdm-docs` at `https://abdm-docs-mcp.dev.eka.care/mcp` using their config format.

## 4. Report back

Tell the user what you installed and where you suggest starting. Two cautions to keep for the whole engagement:

- Nothing in these skills has been run against the ABDM sandbox. Verify response shapes against real calls before relying on them.
- The skills are snapshots. The current documentation lives at https://abdm-docs.dev.eka.care/; prefer it, and the MCP server when connected, over any downloaded copy that has aged.

