#!/usr/bin/env python3
"""Verify dora.py against hand-computed values and the dashboard panel set."""
import json, sys
from dora import load, metrics

m = metrics(load())
want = {"deploys_per_week": 2.8, "change_failure_rate": 0.25, "mttr_hours": 1.2, "lead_time_hours_median": 24.0}
errs = [f"{k}: got {m[k]}, want {v}" for k, v in want.items() if m[k] != v]
titles = {p["title"] for p in json.load(open("dashboard.json"))["panels"]}
if len(titles) != 4:
    errs.append("dashboard must have the four DORA panels")
print("\n".join(errs) or "ok")
sys.exit(1 if errs else 0)
