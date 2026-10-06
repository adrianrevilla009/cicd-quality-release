#!/usr/bin/env python3
"""Validate-only check: compose, workflow, gate definition and scanner properties."""
import json, sys, yaml

errs = []
c = yaml.safe_load(open("compose.yaml"))
for name, svc in c["services"].items():
    if ":" not in svc["image"] or svc["image"].endswith(":latest"):
        errs.append(f"{name}: image not pinned")
w = yaml.safe_load(open("sonar.workflow.yml"))
if "uses" not in w["jobs"]["sonar"]:
    errs.append("workflow must call a reusable workflow")
props = dict(l.split("=", 1) for l in open("sonar-project.properties") if "=" in l and not l.startswith("#"))
if props.get("sonar.qualitygate.wait", "").strip() != "true":
    errs.append("sonar.qualitygate.wait must be true")
g = json.load(open("quality-gate.json"))
if not g["conditions"] or any(not x["metric"].startswith("new_") for x in g["conditions"]):
    errs.append("gate must only use new-code metrics")
print("\n".join(errs) or "ok")
sys.exit(1 if errs else 0)
