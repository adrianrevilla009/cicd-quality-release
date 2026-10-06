#!/usr/bin/env python3
"""Validate-only check: workflow logs in to every registry it pushes to; script is strict."""
import re, subprocess, sys, yaml

errs = []
w = yaml.safe_load(open("push.workflow.yml"))
steps = w["jobs"]["push"]["steps"]
logins = {s["with"].get("registry", "docker.io") for s in steps if s["uses"].startswith("docker/login-action")}
meta = next(s for s in steps if s["uses"].startswith("docker/metadata-action"))
targets = {re.sub(r"/.*", "", i.strip()) for i in meta["with"]["images"].splitlines() if i.strip()}
if targets - logins:
    errs.append(f"no login for {sorted(targets - logins)}")
if "secrets." not in str(steps):
    errs.append("expected secrets-based auth")
if "set -euo pipefail" not in open("push-local.sh").read():
    errs.append("push-local.sh must be strict")
if subprocess.run(["bash", "-n", "push-local.sh"]).returncode:
    errs.append("push-local.sh syntax error")
for svc in yaml.safe_load(open("compose.yaml"))["services"].values():
    if ":" not in svc["image"]:
        errs.append("unpinned image")
print("\n".join(errs) or "ok")
sys.exit(1 if errs else 0)
