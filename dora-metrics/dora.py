#!/usr/bin/env python3
"""Compute the four DORA metrics from deployments.csv. Stdlib only."""
import csv, json, os, statistics, sys
from datetime import datetime

def load(path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "deployments.csv")):
    with open(path) as f:
        return list(csv.DictReader(f))

def metrics(rows):
    t = lambda s: datetime.fromisoformat(s)
    days = (max(t(r["deployed_at"]) for r in rows) - min(t(r["deployed_at"]) for r in rows)).days or 1
    lead = [(t(r["deployed_at"]) - t(r["commit_at"])).total_seconds() / 3600 for r in rows]
    failed = [r for r in rows if r["failed"] == "true"]
    mttr = [(t(r["restored_at"]) - t(r["deployed_at"])).total_seconds() / 3600 for r in failed]
    return {
        "deploys_per_week": round(len(rows) / days * 7, 2),
        "lead_time_hours_median": round(statistics.median(lead), 1),
        "change_failure_rate": round(len(failed) / len(rows), 2),
        "mttr_hours": round(statistics.mean(mttr), 1) if mttr else None,
    }

if __name__ == "__main__":
    json.dump(metrics(load(*sys.argv[1:])), sys.stdout, indent=2)
    print()
