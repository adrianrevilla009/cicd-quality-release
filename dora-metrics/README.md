# dora-metrics

A stdlib Python script that computes the four DORA metrics from `deployments.csv`, and a Grafana `dashboard.json` with four panels.

## Goal
Show how deployment frequency, lead time, change failure rate and time to restore come from plain deployment records.

## Run it
```bash
python3 dora.py
python3 validate.py
```
Expected from `dora.py`: `deploys_per_week` 2.8, `lead_time_hours_median` 24.0, `change_failure_rate` 0.25, `mttr_hours` 1.2. `validate.py` prints `ok`.

## What it proves
- The sample has 8 deployments over 20 days (2.8 per week) and 2 failures (0.25), restored after 2 h and 0.5 h (mean 1.2 h).
- `dora.py` takes lead time as commit to deploy and reports the median; `validate.py` compares all four values with hand-computed ones.
- `dashboard.json` has four stat panels with PromQL expressions for the same four numbers.

## Trade-offs
- The panels assume metrics such as `deployments_total` that something must export; nothing here does.
- With few rows the numbers are noisy, and the day span is rounded down to whole days.
- Mean time to restore is dominated by a single long incident.

## When not to use it
- Not as a replacement for a platform that already tracks deployments.
- Not for measuring individual developers; the metrics describe a team.

Not run end to end: the dashboard was never loaded into Grafana.
