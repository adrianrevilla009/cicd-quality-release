#!/usr/bin/env bash
# Tag one image for several registries and push; REGISTRIES defaults to a local registry:2.
set -euo pipefail
IMAGE="${1:?usage: push-local.sh <local-image:tag>}"
REGISTRIES="${REGISTRIES:-localhost:5000 localhost:5001}"
for r in $REGISTRIES; do
  docker tag "$IMAGE" "$r/$IMAGE"
  docker push "$r/$IMAGE"
done
