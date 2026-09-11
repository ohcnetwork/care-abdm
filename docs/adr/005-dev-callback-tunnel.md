# ADR-005 — Dev callback ingress: a stable tunnel to local Care

Status: Accepted (Rithvik, 2026-09-09: "ngrok or cloudflared as long as the URL doesn't change")
Date: 2026-09-09

## Context
M2/M3 answers arrive as POSTs to a registered public URL that must be reachable
and listening whether or not we are ready (`/getting-started/sandbox` §3). The
docs warn ad-hoc tunnels change URL per restart and must be re-registered each
time. Both `ngrok` and `cloudflared` are installed at `/opt/homebrew/bin`; as of
2026-09-09 neither is authenticated (`ngrok config check` → no ngrok.yml;
`cloudflared tunnel list` → no origin cert).

## Decision
Use a **named/static** tunnel so the URL is fixed:
- ngrok: `ngrok config add-authtoken <tok>` then claim the free static domain in
  the dashboard and run `ngrok http --url=<name>.ngrok-free.app 9000`.
- cloudflared: `cloudflared tunnel login`, `cloudflared tunnel create care-abdm`,
  route a DNS name on a zone Rithvik owns, `cloudflared tunnel run care-abdm`
  with ingress → `http://localhost:9000`.
Chosen 2026-09-09: cloudflared. Tunnel `care-abdm-sbx` (id 5cd26138-…), CNAME `care-abdm-sbx.rithviknishad.dev`, config `~/.cloudflared/config.yml` → `http://localhost:8000`. Run: `cloudflared tunnel run care-abdm-sbx`. The resulting
URL goes in `.env.local` as `ABDM_CALLBACK_BASE_URL` and is registered once via
`gateway_update_bridge_url` (PATCH `/api/hiecm/gateway/v3/bridge/url`).
Local Care runs `manage.py runserver 0.0.0.0:8000`.

Callbacks land under `${ABDM_CALLBACK_BASE_URL}/api/abdm/...` because Care mounts
plug URLs at `api/<plug>/` (`care/config/urls.py:111-112`).

## Consequences
- One-time manual auth step by Rithvik (I cannot log in on his behalf).
- No re-registration churn; the bridge URL stays valid across restarts.
