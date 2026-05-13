# Concept: Full Outer Join for Reconciliation

A **FULL OUTER JOIN** returns all rows from both tables, filling in NULL for columns from the side that has no matching row. This is the natural tool for reconciliation tasks where you need to surface:

- Rows present in **both** sources (for comparison)
- Rows present in **only the left** source (missing from the right)
- Rows present in **only the right** source (missing from the left)

## Filtering to Discrepancies Only

After the full outer join, filter out exactly-matching rows:
```sql
WHERE s.amount != b.amount
   OR s.txn_id IS NULL
   OR b.txn_id IS NULL
```

An easier way: keep any row where the amounts are NOT equal or either side is NULL.

## NULL Arithmetic

In SQL and Spark, any arithmetic involving NULL produces NULL:
```
bank_amount - system_amount = NULL  (if either is NULL)
```

This is the desired behaviour for `variance` — you naturally get NULL when a transaction is one-sided.
