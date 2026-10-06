# jreleaser

A `jreleaser.yml` for a GitHub release with a conventional-commits changelog, GPG signing and a Maven Central deploy.

## Goal
Show how JReleaser describes a Java release in one file, with all secrets read from the environment.

## Run it
```bash
pip install pyyaml
python3 validate.py
```
Expected: `ok`.

## What it proves
- `jreleaser.yml` has `project`, `release`, `signing` and `deploy` sections, and `project.java.groupId` is `com.example.orders`.
- The GitHub token is `{{ env.JRELEASER_GITHUB_TOKEN }}`; `validate.py` rejects any inline token, password or passphrase.
- `signing.active` is `ALWAYS`, since Maven Central requires signed artifacts.
- `.env.example` lists the four variables to export, all empty.

## Trade-offs
- JReleaser can also build distributions and announce releases; this file only does GitHub and Central.
- The version is a fixed input (`project.version`), not computed as in `semantic-release`.
- The staging directory `target/staging-deploy` must be filled by a Maven build that is not included.
- The GitHub owner and project name are fixed in the file and need changing for a fork.

## When not to use it
- Not for non-Java projects, where semantic-release is simpler.
- Not if you publish only to an internal repository such as Nexus.

Not run end to end: the `jreleaser` CLI was not installed or run, and nothing was released.
