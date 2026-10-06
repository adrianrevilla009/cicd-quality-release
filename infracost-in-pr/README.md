# infracost-in-pr

An Infracost project config, a usage file, a Rego budget policy and a workflow that comments the cost change on pull requests.

## Goal
Show how a pull request that changes Terraform gets a cost estimate and a budget limit before merge.

## Run it
```bash
pip install pyyaml
python3 validate.py
```
Expected: `ok`. The script reads the files only and never calls the Infracost API.

## What it proves
- `infracost.workflow.yml` runs on `pull_request` for `terraform/**`, takes `INFRACOST_API_KEY` from secrets, and updates one comment.
- `infracost.yml` points at the project `terraform/orders` and `infracost-usage.yml`, which assumes 1,000,000 Lambda requests a month at 120 ms.
- `cost-policy.rego` denies when the monthly increase is above 100 USD; `validate.py` checks that a `deny[msg]` rule exists.

## Trade-offs
- The `terraform/orders` directory is not in this repo, so a real run fails until it exists.
- The Rego policy is not evaluated here and the workflow does not apply it.
- Usage values are assumptions; the estimate is only as good as they are.

## When not to use it
- Not for infrastructure without Terraform.
- Not as a hard cost control: it estimates and does not stop spending.

Not run end to end: the Infracost CLI, the policy and the workflow were not run.
