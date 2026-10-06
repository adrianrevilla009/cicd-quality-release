#!/usr/bin/env python3
"""Validate-only check of renovate.json (also runs renovate-config-validator with --online)."""
import json, shutil, subprocess, sys, yaml

errs = []
cfg = json.load(open("renovate.json"))
if "extends" not in cfg:
    errs.append("missing extends")
for i, r in enumerate(cfg.get("packageRules", [])):
    if not any(k.startswith("match") for k in r):
        errs.append(f"rule {i} has no matcher")
    if r.get("automerge") and "major" in r.get("matchUpdateTypes", []):
        errs.append(f"rule {i} automerges majors")
yaml.safe_load(open("renovate.workflow.yml"))
if shutil.which("npx") and "--online" in sys.argv:
    p = subprocess.run(["npx", "--yes", "--package=renovate@39.60.0", "renovate-config-validator", "renovate.json"])
    errs += ["renovate-config-validator failed"] * (p.returncode != 0)
print("\n".join(errs) or "ok")
sys.exit(1 if errs else 0)
