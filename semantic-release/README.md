# semantic-release

semantic-release configuration with pinned plugins, a release workflow, and a Python model of the commit-to-version rule.

## Goal
Show versions and changelogs derived from conventional commit messages, with the Maven version updated before the release commit.

## Run it
```bash
pip install pyyaml
python3 validate.py
```
Expected: `ok`.

## What it proves
- `.releaserc.json` runs the commit analyzer first, then release notes, changelog, `mvn versions:set`, a git commit of `CHANGELOG.md` and `pom.xml` with `[skip ci]`, and the GitHub release.
- `package.json` pins semantic-release 24.2.0 and its plugins to exact versions.
- `release.workflow.yml` checks out with `fetch-depth: 0`; without full history the tool cannot find the last tag.
- `validate.py` models the rule on four cases: `fix` gives patch, `fix` plus `feat` gives minor, `feat!` gives major, `docs` gives no release.

## Trade-offs
- The Python `bump` function is a simplified copy, not the real analyzer.
- Pushing the release commit needs `contents: write` and a branch that allows it.
- There is no `pom.xml` here, so `mvn versions:set` is never exercised.

## When not to use it
- Not when the team does not write conventional commits.
- Not for releases that need a manual go/no-go.

Not run end to end: `npx semantic-release` was not run and the plugins were not installed.
