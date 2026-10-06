# renovate

A `renovate.json` plus a scheduled GitHub workflow that runs Renovate with a token.

## Goal
Show a conservative Renovate setup: weekly batches, automerge only for safe updates, and a human gate on major versions.

## Run it
```bash
pip install pyyaml
python3 validate.py
python3 validate.py --online
```
Expected: `ok`. The `--online` form also runs `renovate-config-validator` from `renovate@39.60.0` through `npx`, which needs network; only the offline form was run.

## What it proves
- Minor and patch updates of versions not starting with `0` are grouped as `non-major` and automerged; majors wait for approval on the dependency dashboard.
- `org.springframework.boot:*` Maven packages go into one `spring-boot` group.
- `vulnerabilityAlerts` runs at any time with a `security` label, outside the Monday-before-6am schedule.
- `validate.py` fails if a rule has no matcher or automerges majors.

## Trade-offs
- Automerge relies on good tests and a required status check; without them it merges breakage.
- The workflow needs a `RENOVATE_TOKEN` secret that is not provided here.
- Self-hosting costs runner minutes; the hosted Renovate app avoids that.

## When not to use it
- Not alongside Dependabot version updates on the same repository: they open duplicate pull requests.
- Not for a repo with no automated tests.

Not run end to end: the workflow was not executed against GitHub.
