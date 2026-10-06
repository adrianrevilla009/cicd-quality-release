#!/usr/bin/env python3
"""Validate-only check: every remote repo is pinned to a version tag and hooks are well formed."""
import re, sys, yaml

errs = []
c = yaml.safe_load(open(".pre-commit-config.yaml"))
ids = []
for r in c["repos"]:
    if r["repo"] != "local" and not re.match(r"^v?\d+\.\d+\.\d+$", r.get("rev", "")):
        errs.append(f"{r['repo']}: rev must be a pinned version, not a branch")
    for h in r["hooks"]:
        ids.append(h["id"])
        if r["repo"] == "local" and not {"name", "entry", "language"} <= h.keys():
            errs.append(f"local hook {h['id']} incomplete")
for needed in ("detect-private-key", "gitleaks", "conventional-pre-commit"):
    if needed not in ids:
        errs.append(f"missing {needed}")
print("\n".join(errs) or "ok")
sys.exit(1 if errs else 0)
