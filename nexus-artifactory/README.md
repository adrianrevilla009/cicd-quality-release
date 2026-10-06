# nexus-artifactory

Nexus 3 on compose, a Maven `settings.xml` that mirrors through it, and a `distributionManagement` snippet for deploys.

## Goal
Show how Maven resolves from and publishes to a private repository manager, with credentials taken from the environment.

## Run it
```bash
pip install pyyaml
python3 validate.py
cp .env.example .env && docker compose up -d   # optional, first start takes minutes
```
Expected: `validate.py` prints `ok`. Compose starts Nexus on port 8081; read the first admin password with `docker compose exec nexus cat /nexus-data/admin.password`.

## What it proves
- `settings.xml` has one server and one mirror, both with id `nexus`; the mirror serves `maven-public` for all repositories.
- `pom-snippet.xml` sends releases to `maven-releases` and snapshots to `maven-snapshots` using the same id, so the credentials match.
- The password is `${env.NEXUS_PASSWORD}`, never a literal.
- `compose.yaml` pins `sonatype/nexus3:3.70.1`.

## Trade-offs
- Only Nexus is configured; despite the folder name there is no Artifactory service.
- With `mirrorOf *`, a Nexus outage stops every build that uses these settings.
- The URLs are plain HTTP on localhost, fine for a lab only.

## When not to use it
- Not when Maven Central or a hosted registry such as GitHub Packages is enough.
- Not for production without TLS and a backed-up data volume.

Not run end to end: Nexus was not started and no build was deployed.
