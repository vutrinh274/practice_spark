Given a table `transactions` with columns `transaction_id` and `amount`, remove statistical outliers using the **IQR method**.

Compute Q1 = `percentile_approx(amount, 0.25)` and Q3 = `percentile_approx(amount, 0.75)`. Then IQR = Q3 - Q1. Keep only transactions where:

```
amount BETWEEN (Q1 - 1.5 * IQR) AND (Q3 + 1.5 * IQR)
```

Return columns: `transaction_id`, `amount`

Order by `transaction_id` ascending.
