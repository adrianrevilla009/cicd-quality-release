# multi-registry-push

A GitHub workflow that publishes one image to GHCR and Docker Hub, and a shell script plus compose file that do the same against two local registries.

## Goal
Show one build tagged and pushed to several registries, with a login for each.

## Run it
```bash
pip install pyyaml
python3 validate.py
docker compose up -d && bash push-local.sh orders-service:1.0   # optional local push
```
Expected: `validate.py` prints `ok`. The script tags the local image and pushes it to `localhost:5000` and `localhost:5001`.

## What it proves
- `push.workflow.yml` triggers on `v*` tags, logs in to `ghcr.io` with `GITHUB_TOKEN` and to Docker Hub with secrets, then lets `docker/metadata-action` generate tags for both images.
- `validate.py` fails if an image in the metadata step has no matching login.
- `push-local.sh` uses `set -euo pipefail` and loops over `REGISTRIES`; `validate.py` also runs `bash -n` on it.
- `compose.yaml` runs two `registry:2.8.3` containers on ports 5000 and 5001.

## Trade-offs
- Pushes are not atomic; one registry can succeed while another fails and they drift.
- The workflow builds from `context: .`, so it needs a Dockerfile that is not in this repo.
- Docker Hub adds a second secret to rotate and its own rate limits.
- The image names point to a specific GitHub account and need changing for a fork.

## When not to use it
- Not when one registry is enough; each extra one adds a secret and a failure point.
- Not when registry-side replication can mirror the image for you.

Not run end to end: the push script and compose stack were not run and the workflow was not executed.
