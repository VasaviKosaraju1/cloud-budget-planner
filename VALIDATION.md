# Validation

Local validation on Python 3.9.6.

## Unit tests

```text
test_duplicate_service (test_budget.BudgetTests) ... ok
test_exact_budget (test_budget.BudgetTests) ... ok
test_nan_rejected (test_budget.BudgetTests) ... ok
test_negative_quantity (test_budget.BudgetTests) ... ok
test_over_budget (test_budget.BudgetTests) ... ok
test_rounding_only_at_reporting_boundary (test_budget.BudgetTests) ... ok
test_sample_total (test_budget.BudgetTests) ... ok
test_unknown_unit (test_budget.BudgetTests) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.001s

OK
```

## python3 budget.py scenario.json

Exit status: 0

```json
{
  "currency": "USD",
  "line_items": [
    {
      "name": "app-compute",
      "monthly_cost": "36.50"
    },
    {
      "name": "storage",
      "monthly_cost": "10.00"
    },
    {
      "name": "monitoring",
      "monthly_cost": "8.00"
    }
  ],
  "subtotal": "54.50",
  "headroom": "8.18",
  "projected_total": "62.68",
  "monthly_budget": "100.00",
  "remaining_budget": "37.33",
  "over_budget": false
}
```

These checks use small synthetic fixtures. They do not establish production readiness or cloud deployment results.
