# pre-commit

A `.pre-commit-config.yaml` with file hygiene, secret scanning, conventional commit checks and a Maven pre-push hook.

## Goal
Show cheap local checks that stop bad files, leaked secrets and unclear commit messages before they reach CI.

## Run it
```bash
pip install pyyaml
python3 validate.py
```
Expected: `ok`. In a real repository, copy the file to the root and run `pre-commit install --install-hooks -t pre-commit -t commit-msg -t pre-push`.

## What it proves
- Remote hook repositories are pinned to tags: pre-commit-hooks v5.0.0, gitleaks v8.21.2 and conventional-pre-commit v3.6.0. `validate.py` rejects anything else.
- `detect-private-key`, `gitleaks` and `conventional-pre-commit` must be present; the last runs on `commit-msg`.
- The local hook runs `mvn -B -q -o verify -DskipITs` on `pre-push`, so commits stay fast.

## Trade-offs
- Hooks can be skipped with `--no-verify`, so CI must repeat them.
- The Maven hook runs offline and needs a `pom.xml` and a warm local cache.
- The first run downloads each hook environment.

## When not to use it
- Not as the only enforcement point; local hooks are advisory.
- Not for a team that cannot install pre-commit on every machine.

Not run end to end: `pre-commit` is not installed here and no hook was run.
