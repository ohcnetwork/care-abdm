#!/usr/bin/env python3
"""
Generate `backend/src/abdm/error_catalogue.py` from the docs mirror.

`/docs/hiecm/v3/getting-started/build-it-well` says: "Every code in the error code reference
carries an action. Key your handling to that column rather than to a list of codes you maintain by
hand." This script does exactly that. It reads
`docs/abdm-docs-mirror/pages/hiecm/v3/reference/error-codes.md` and writes 1 map of code to action.

Run it after `scripts/refresh-docs-mirror.py`:

    python3 scripts/generate-error-catalogue.py

A code can publish more than 1 action (39 of 818 do). The action that does not retry wins, by the
precedence in PRECEDENCE below. Sandbox corrections do not belong here: they go in
`abdm/errors.py::OVERRIDES` with a line in `docs/findings.md`.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "docs/abdm-docs-mirror/pages/hiecm/v3/reference/error-codes.md"
TARGET = ROOT / "backend/src/abdm/error_catalogue.py"

ROW = re.compile(r"\|\s*`([^`]+)`\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$")

# The published "What to do" text, mapped to the action constants in abdm/errors.py.
ACTIONS = {
    "fix request": "fix_request",
    "fix auth": "fix_auth",
    "new request id": "new_request_id",
    "new consent": "new_consent",
    "retry": "retry",
    "back off": "back_off",
    "cannot proceed": "cannot_proceed",
    "ask support": "ask_support",
    "treat as success": "treat_as_success",
    "blocked, no retry": "blocked",
    "unclassified": "unclassified",
}

# Most serious first. The first action a code publishes on this list wins.
PRECEDENCE = (
    "blocked",
    "cannot_proceed",
    "ask_support",
    "fix_auth",
    "new_consent",
    "new_request_id",
    "back_off",
    "fix_request",
    "chase_hip",
    "retry",
    "treat_as_success",
    "unclassified",
)


def action_of(text: str) -> str:
    """The action constant for 1 published cell. `Chase the [HIP](...)` becomes `chase_hip`."""
    plain = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text).strip().lower()
    if plain.startswith("chase the"):
        return "chase_hip"
    return ACTIONS.get(plain, "unclassified")


def read_rows(path: Path) -> list[tuple[str, str]]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = ROW.match(line)
        if match and match.group(1).strip():
            rows.append((match.group(1).strip(), action_of(match.group(3))))
    return rows


def resolve(rows: list[tuple[str, str]]) -> dict[str, str]:
    by_code: dict[str, set] = {}
    for code, action in rows:
        by_code.setdefault(code, set()).add(action)
    catalogue = {}
    for code, actions in by_code.items():
        for candidate in PRECEDENCE:
            if candidate in actions:
                catalogue[code] = candidate
                break
        else:
            catalogue[code] = "unclassified"
    return dict(sorted(catalogue.items()))


def render(catalogue: dict[str, str], row_count: int) -> str:
    lines = [
        '"""',
        "ABDM error codes and the action each one asks for.",
        "",
        "GENERATED FILE. Do not edit it by hand.",
        "Run `python3 scripts/generate-error-catalogue.py` to rebuild it from the docs mirror",
        "(`docs/abdm-docs-mirror/pages/hiecm/v3/reference/error-codes.md`).",
        "",
        f"Rows read: {row_count}. Codes: {len(catalogue)}.",
        "",
        "Sandbox corrections live in `abdm/errors.py::OVERRIDES`, never here.",
        '"""',
        "",
        "ERROR_ACTIONS: dict[str, str] = {",
    ]
    lines += [f'    "{code}": "{action}",' for code, action in catalogue.items()]
    lines += ["}", ""]
    return "\n".join(lines)


def has_action_column(path: Path) -> bool:
    """True when the page carries the `What to do` column this script reads."""
    return any(
        line.startswith("|") and "what to do" in line.lower()
        for line in path.read_text(encoding="utf-8").splitlines()
    )


def main() -> int:
    if not SOURCE.exists():
        print(f"missing {SOURCE}", file=sys.stderr)
        return 1
    if not has_action_column(SOURCE):
        # The 2026-09-16 catalogue replaced the action column with HTTP / Message / Returned by and
        # kept 20 codes of 818. Writing from that page would delete the ADR-012 catalogue. Keep the
        # last good file and record the gap in docs/findings.md.
        print(
            f"{SOURCE.relative_to(ROOT)} has no `What to do` column; "
            f"{TARGET.relative_to(ROOT)} is left as it is",
            file=sys.stderr,
        )
        return 2
    rows = read_rows(SOURCE)
    catalogue = resolve(rows)
    TARGET.write_text(render(catalogue, len(rows)), encoding="utf-8")
    print(f"{TARGET.relative_to(ROOT)}: {len(catalogue)} codes from {len(rows)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
