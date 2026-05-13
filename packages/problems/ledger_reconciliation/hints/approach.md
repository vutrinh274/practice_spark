# Approach

## Step-by-Step Plan

1. **FULL OUTER JOIN** `system_ledger` and `bank_ledger` on `txn_id`.
2. **Select columns**:
   - `COALESCE(s.txn_id, b.txn_id)` → `txn_id`
   - `s.amount` → `system_amount`
   - `b.amount` → `bank_amount`
   - `b.amount - s.amount` → `variance` (NULL when either is NULL — that's correct)
3. **Filter** to rows where amounts differ or one side is missing:
   - `s.amount != b.amount OR s.txn_id IS NULL OR b.txn_id IS NULL`
4. **Order** by `txn_id ASC`.

## DataFrame Tip

In Spark's DataFrame API, after a full outer join both `txn_id` columns exist. Use `COALESCE` or alias them carefully before the join:

```python
system_ledger.alias("s").join(bank_ledger.alias("b"), on="txn_id", how="full")
```

When joining `on="txn_id"` Spark automatically coalesces the join key into a single column.
