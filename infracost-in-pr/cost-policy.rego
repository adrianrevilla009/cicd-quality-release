package infracost

# Fail the PR when the monthly cost increase is more than 100 USD.
deny[msg] {
  to_number(input.diffTotalMonthlyCost) > 100
  msg := sprintf("Monthly cost increase %s USD exceeds budget of 100", [input.diffTotalMonthlyCost])
}
