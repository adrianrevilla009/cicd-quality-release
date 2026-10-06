# cicd-quality-release

Configuration for the quality, dependency, release and publishing steps of a CI/CD pipeline, each with an offline check, around a small Orders service.

## What is inside

| Folder | What it shows | Run |
|---|---|---|
| [`sonarqube-gate`](./sonarqube-gate) | SonarQube on compose, a new-code quality gate and a workflow that fails on a red gate | `python3 validate.py` |
| [`renovate`](./renovate) | Renovate config with grouping, automerge for minor and patch, approval for majors | `python3 validate.py` |
| [`dependabot`](./dependabot) | Dependabot config for Maven, GitHub Actions and Docker | `python3 validate.py` |
| [`semantic-release`](./semantic-release) | Commit-driven versioning and changelog, plus a Python model of the bump rule | `python3 validate.py` |
| [`jreleaser`](./jreleaser) | JReleaser config for a GitHub release and Maven Central deploy with signing | `python3 validate.py` |
| [`nexus-artifactory`](./nexus-artifactory) | Nexus on compose with Maven `settings.xml` and `distributionManagement` | `python3 validate.py` |
| [`multi-registry-push`](./multi-registry-push) | One image pushed to GHCR and Docker Hub, or to two local registries | `python3 validate.py` |
| [`dora-metrics`](./dora-metrics) | The four DORA metrics computed from a CSV, and a Grafana dashboard | `python3 dora.py` |
| [`pre-commit`](./pre-commit) | Pinned hooks for hygiene, secrets and commit messages | `python3 validate.py` |
| [`infracost-in-pr`](./infracost-in-pr) | Infracost cost comment and budget policy on pull requests | `python3 validate.py` |

Run each command from inside its folder.

## Prerequisites

- Python 3.10+ with PyYAML (`pip install pyyaml`)
- Docker with Compose, only to start the Nexus, SonarQube and registry stacks by hand
- Node.js 22 with `npx`, only for the optional `python3 validate.py --online` in `renovate`

## How to read it

Start with `sonarqube-gate`: it shows the usual folder layout of config files, a workflow and a `validate.py` that checks them offline. Nothing here talks to a real SonarQube, registry, GitHub or cloud account, and the Orders service the configs refer to is not part of this repo.
