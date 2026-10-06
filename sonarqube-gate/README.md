# sonarqube-gate

SonarQube with Postgres on compose, a quality gate definition, scanner properties and a GitHub workflow that calls a reusable Sonar job.

## Goal
Show how a CI build is failed by a quality gate that only looks at new code, so legacy issues do not block unrelated changes.

## Run it
```bash
pip install pyyaml
python3 validate.py
cp .env.example .env && docker compose up -d   # optional, SonarQube at http://localhost:9000
```
Expected: `validate.py` prints `ok`. Create the gate from `quality-gate.json` in the web UI or through the `api/qualitygates` endpoints, then store a token as the `SONAR_TOKEN` secret.

## What it proves
- `quality-gate.json` has four conditions, all on `new_` metrics: coverage below 80, duplication above 3, and security and maintainability rating worse than A.
- `sonar-project.properties` sets `sonar.qualitygate.wait=true` with a 300 s timeout, so the scanner step fails when the gate is red.
- `compose.yaml` pins `sonarqube:10.7.0-community` and `postgres:16.4`; `validate.py` rejects unpinned images.

## Trade-offs
- The gate is a JSON description and is not applied to a server by anything here.
- Community edition has no pull request analysis, so the gate is meaningful on `main` pushes.
- `sonar.workflow.yml` calls `maven-sonar.yml` in a separate `lab-workflows` repo, which is not included.
- The compose database password defaults to `change-me`; set `SONAR_DB_PASSWORD`.

## When not to use it
- Not for a project with no tests: an 80% new-code coverage condition fails every build.
- Not when a hosted service such as SonarCloud is acceptable and you do not want to run Postgres yourself.

Not run end to end: the compose stack was not started and the workflow was not executed; only `validate.py` was run.
