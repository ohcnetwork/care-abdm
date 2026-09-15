#!/usr/bin/env python3
"""Refresh the ABDM docs mirror from the single permitted source.

Source: https://abdm-docs.dev.eka.care (see docs/01-sources.md).

The script writes:
- docs/abdm-docs-mirror/llms.txt, llms-full.txt, sitemap.xml
- docs/abdm-docs-mirror/skills-index.json, agent-setup-prompt.md
- docs/abdm-docs-mirror/pages/<url path without /docs/>.md, 1 file per page
  in the sitemap under /docs/hiecm/v3/ and /docs/whats-new/
- .agent/skills/<name>/... for each skill in skills/index.json
- docs/abdm-docs-mirror/MANIFEST.json with the fetch date and the counts

Usage:
  python3 scripts/refresh-docs-mirror.py            # refresh all
  python3 scripts/refresh-docs-mirror.py --diff     # report changes, write nothing

The script has no third-party dependency.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://abdm-docs.dev.eka.care"
REPO = Path(__file__).resolve().parent.parent
MIRROR = REPO / "docs" / "abdm-docs-mirror"
PAGES = MIRROR / "pages"
SKILLS = REPO / ".agent" / "skills"
PAGE_PREFIXES = ("/docs/hiecm/v3", "/docs/whats-new")
WORKERS = 8


def fetch(path: str) -> bytes:
    req = urllib.request.Request(BASE + path, headers={"User-Agent": "care-abdm-sbx-mirror"})
    with urllib.request.urlopen(req, timeout=60) as res:
        return res.read()


def page_paths(sitemap: str) -> list[str]:
    out: list[str] = []
    for loc in re.findall(r"<loc>(.*?)</loc>", sitemap):
        path = loc.replace(BASE, "").rstrip("/")
        if path.startswith(PAGE_PREFIXES) and path not in out:
            out.append(path)
    return sorted(out)


def page_file(path: str) -> Path:
    return PAGES / (path.removeprefix("/docs/").strip("/") + ".md")


def fetch_one(path: str) -> tuple[str, bytes | None, str]:
    try:
        return path, fetch(path), ""
    except urllib.error.HTTPError as err:
        return path, None, f"HTTP {err.code}"
    except Exception as err:  # noqa: BLE001
        return path, None, repr(err)


def refresh_tree(
    jobs: list[tuple[str, Path]], diff_only: bool
) -> tuple[int, list[str], list[str]]:
    """Fetch each (url path, target file). Return (written, changed, failed)."""
    targets = dict(jobs)
    changed: list[str] = []
    failed: list[str] = []
    written = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for path, body, error in pool.map(fetch_one, [p for p, _ in jobs]):
            if body is None:
                failed.append(f"{path}: {error}")
                continue
            target = targets[path]
            old = target.read_bytes() if target.exists() else None
            if old != body:
                changed.append(path)
            if not diff_only:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(body)
                written += 1
    return written, changed, failed


def main() -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--diff", action="store_true", help="report changes, write nothing")
    diff_only = parser.parse_args().diff

    top = {
        "llms.txt": "/llms.txt",
        "llms-full.txt": "/llms-full.txt",
        "sitemap.xml": "/sitemap.xml",
        "skills-index.json": "/skills/index.json",
        "agent-setup-prompt.md": "/agent-setup/prompt.md",
    }
    bodies = {name: fetch(path) for name, path in top.items()}
    changed_top = [
        name
        for name, body in bodies.items()
        if not (MIRROR / name).exists() or (MIRROR / name).read_bytes() != body
    ]

    paths = page_paths(bodies["sitemap.xml"].decode())
    index = json.loads(bodies["skills-index.json"])
    page_jobs = [(p + "/index.md", page_file(p)) for p in paths]
    skill_jobs = [
        (f"/skills/{s['name']}/{rel}", SKILLS / s["name"] / rel)
        for s in index["skills"]
        for rel in s["files"]
    ]

    if not diff_only:
        MIRROR.mkdir(parents=True, exist_ok=True)
        for name, body in bodies.items():
            (MIRROR / name).write_bytes(body)
        # Rebuild the page tree from the sitemap so that stale files go away.
        if PAGES.exists():
            shutil.rmtree(PAGES)
        PAGES.mkdir(parents=True)

    written, changed_pages, failed_pages = refresh_tree(page_jobs, diff_only)
    skills_written, changed_skills, failed_skills = refresh_tree(skill_jobs, diff_only)

    if not diff_only:
        manifest = {
            "source": BASE,
            "fetched_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "catalogue_version": index.get("catalogue_version"),
            "skills_built": index.get("built"),
            "page_prefixes": list(PAGE_PREFIXES),
            "pages": len(paths),
            "pages_written": written,
            "pages_failed": failed_pages,
            "skills": [s["name"] for s in index["skills"]],
            "skill_files_written": skills_written,
            "skill_files_failed": failed_skills,
        }
        (MIRROR / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")

    print(f"pages in sitemap: {len(paths)}")
    print(f"top-level changed: {changed_top or 'none'}")
    print(f"pages changed or new: {len(changed_pages)}")
    for path in changed_pages:
        print(f"  {path}")
    print(f"skill files changed or new: {len(changed_skills)}")
    for path in changed_skills:
        print(f"  {path}")
    if failed_pages or failed_skills:
        print("failed:")
        for line in failed_pages + failed_skills:
            print(f"  {line}")
    return 1 if (failed_pages or failed_skills) else 0


if __name__ == "__main__":
    sys.exit(main())
