#!/usr/bin/env python3
"""Validate-only check: required JReleaser sections present and no inline credentials."""
import re, sys, yaml

errs = []
raw = open("jreleaser.yml").read()
c = yaml.safe_load(raw)
for key in ("project", "release", "signing", "deploy"):
    if key not in c:
        errs.append(f"missing section {key}")
if not c["project"].get("java", {}).get("groupId"):
    errs.append("Maven Central needs project.java.groupId")
for m in re.finditer(r"(token|password|passphrase):[ ]*(.+)", raw):
    if "env." not in m.group(2) and m.group(2) not in ('""', "''"):
        errs.append(f"inline credential for {m.group(1)}")
if c["signing"].get("active") != "ALWAYS":
    errs.append("Central requires signed artifacts")
print("\n".join(errs) or "ok")
sys.exit(1 if errs else 0)
