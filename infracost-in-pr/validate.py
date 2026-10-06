#!/usr/bin/env python3
"""Validate-only check. Never calls the Infracost API or any cloud account."""
import re, sys, yaml

errs = []
w = yaml.safe_load(open("infracost.workflow.yml"))
text = open("infracost.workflow.yml").read()
if "INFRACOST_API_KEY" not in text or "secrets." not in text:
    errs.append("API key must be a secret")
if "pull_request" not in w.get(True, w.get("on", {})):
    errs.append("must trigger on pull_request")
cfg = yaml.safe_load(open("infracost.yml"))
if not cfg["projects"]:
    errs.append("no projects")
yaml.safe_load(open("infracost-usage.yml"))
if not re.search(r"deny\[msg\]", open("cost-policy.rego").read()):
    errs.append("policy has no deny rule")
print("\n".join(errs) or "ok")
sys.exit(1 if errs else 0)
