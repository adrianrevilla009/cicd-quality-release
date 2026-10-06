# dependabot

A `dependabot.yml` covering Maven, GitHub Actions and Docker.

## Goal
Show Dependabot version updates with grouping and a rule that leaves major upgrades to a human.

## Run it
```bash
pip install pyyaml
python3 validate.py
```
Expected: `ok`. In a real repository the file belongs at `.github/dependabot.yml`.

## What it proves
- Maven is checked weekly on Monday, limited to 5 open pull requests, with a `spring-boot` group and a `minor-and-patch` group.
- All major bumps are ignored for Maven (`version-update:semver-major`).
- GitHub Actions are checked monthly with the labels `ci` and `dependencies`; Docker weekly.
- `validate.py` checks `version: 2`, a known ecosystem, a directory and a schedule interval for each entry.

## Trade-offs
- The check covers only those keys, not the full GitHub schema.
- Ignoring majors means they are never proposed, so they need another process.
- Dependabot has no automerge; that needs a separate workflow.

## When not to use it
- Not when you already run Renovate (see `renovate`) on the same repository.
- Not for ecosystems it does not support or for custom version files.

Not run end to end: GitHub never read this file; only `validate.py` was run.
