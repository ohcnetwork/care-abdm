#!/usr/bin/env python3
"""Call one tool on the ABDM docs MCP server from a shell (docs/01-sources.md, way in #1).

Usage:
  python3 scripts/abdm-docs-mcp.py search_docs '{"query": "link token"}'
  python3 scripts/abdm-docs-mcp.py get_operation '{"operation_id": "m2_hip_link_care_context"}'
  python3 scripts/abdm-docs-mcp.py validate_fhir '{"record_type": "OPConsultation", "bundle_json": "..."}'

Streamable HTTP, no auth, no third-party dependency. Operation ids use underscores on the MCP
server (`m2_hip_link_care_context`) and hyphens in page URLs (findings A4).
"""
import json, sys, urllib.request
URL = "https://abdm-docs-mcp.dev.eka.care/mcp"
def post(payload, sid=None):
    h = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    if sid: h["Mcp-Session-Id"] = sid
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(), headers=h)
    with urllib.request.urlopen(req, timeout=60) as r:
        sid = r.headers.get("Mcp-Session-Id", sid)
        body = r.read().decode()
    out = []
    for line in body.splitlines():
        if line.startswith("data:"):
            out.append(json.loads(line[5:].strip()))
    if not out and body.strip():
        try: out.append(json.loads(body))
        except Exception: pass
    return sid, out
sid, _ = post({"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"care-abdm-sbx","version":"0"}}})
post({"jsonrpc":"2.0","method":"notifications/initialized"}, sid)
tool = sys.argv[1]; args = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
_, res = post({"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":tool,"arguments":args}}, sid)
for r in res:
    result = r.get("result", r)
    for c in result.get("content", []):
        if c.get("type") == "text":
            print(c["text"])
        else:
            print(json.dumps(c)[:2000])
    if "error" in r: print("ERROR", r["error"])
