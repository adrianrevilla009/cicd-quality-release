#!/usr/bin/env python3
"""Validate-only check: Maven server ids line up and credentials come from the environment."""
import sys, yaml
import xml.etree.ElementTree as ET

errs = []
ns = {"m": "http://maven.apache.org/SETTINGS/1.2.0"}
s = ET.parse("settings.xml").getroot()
server_ids = {e.text for e in s.findall("m:servers/m:server/m:id", ns)}
mirror_ids = {e.text for e in s.findall("m:mirrors/m:mirror/m:id", ns)}
pw = s.find("m:servers/m:server/m:password", ns).text
if not pw.startswith("${env."):
    errs.append("password must come from env")
dm = ET.fromstring("<r>" + open("pom-snippet.xml").read() + "</r>")
for repo in list(dm.iter("repository")) + list(dm.iter("snapshotRepository")):
    rid = repo.findtext("id")
    if rid not in server_ids:
        errs.append(f"distributionManagement id {rid} has no <server> credentials")
if not mirror_ids <= server_ids:
    errs.append("mirror id has no matching server")
for svc in yaml.safe_load(open("compose.yaml"))["services"].values():
    if svc["image"].endswith(":latest") or ":" not in svc["image"]:
        errs.append("unpinned image")
print("\n".join(errs) or "ok")
sys.exit(1 if errs else 0)
