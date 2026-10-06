#!/usr/bin/env python3
"""Validate-only check, plus a pure-python model of the commit -> bump rule."""
import json, re, sys, yaml

def bump(msgs):
    """Mirror of the default commit-analyzer (angular preset): breaking > feat > fix."""
    level = None
    for m in msgs:
        if "BREAKING CHANGE" in m or re.match(r"^\w+(\(.+\))?!:", m):
            return "major"
        if m.startswith("feat"):
            level = "minor"
        elif m.startswith("fix") and level is None:
            level = "patch"
    return level

errs = []
rc = json.load(open(".releaserc.json"))
names = [p if isinstance(p, str) else p[0] for p in rc["plugins"]]
if names.index("@semantic-release/commit-analyzer") > names.index("@semantic-release/github"):
    errs.append("analyzer must run before publish")
pkg = json.load(open("package.json"))
for dep in [n for n in names if n in pkg["devDependencies"]]:
    if not pkg["devDependencies"][dep][0].isdigit():
        errs.append(f"{dep} not pinned")
if "fetch-depth: 0" not in open("release.workflow.yml").read():
    errs.append("release needs full git history")
yaml.safe_load(open("release.workflow.yml"))
cases = [(["fix: x"], "patch"), (["fix: x", "feat: y"], "minor"), (["feat!: z"], "major"), (["docs: a"], None)]
for msgs, want in cases:
    if bump(msgs) != want:
        errs.append(f"bump({msgs}) != {want}")
print("\n".join(errs) or "ok")
sys.exit(1 if errs else 0)
