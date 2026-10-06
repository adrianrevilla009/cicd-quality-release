#!/usr/bin/env python3
"""Validate-only check of dependabot.yml against the documented required keys."""
import sys, yaml

ECOSYSTEMS = {"maven", "gradle", "npm", "pip", "docker", "github-actions", "terraform", "gomod"}
errs = []
c = yaml.safe_load(open("dependabot.yml"))
if c.get("version") != 2:
    errs.append("version must be 2")
for i, u in enumerate(c.get("updates", [])):
    if u.get("package-ecosystem") not in ECOSYSTEMS:
        errs.append(f"update {i}: unknown ecosystem")
    if "directory" not in u and "directories" not in u:
        errs.append(f"update {i}: directory required")
    if "interval" not in u.get("schedule", {}):
        errs.append(f"update {i}: schedule.interval required")
print("\n".join(errs) or "ok")
sys.exit(1 if errs else 0)
