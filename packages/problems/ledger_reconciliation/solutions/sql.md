# Solution: SQL

```sql
SELECT
    COALESCE(s.txn_id, b.txn_id) AS txn_id,
    s.amount                      AS system_amount,
    b.amount                      AS bank_amount,
    b.amount - s.amount           AS variance
FROM system_ledger s
FULL OUTER JOIN bank_ledger b ON s.txn_id = b.txn_id
WHERE s.amount != b.amount
   OR s.txn_id IS NULL
   OR b.txn_id IS NULL
ORDER BY txn_id
```

## Explanation

1. **`FULL OUTER JOIN`** — produces all combinations: matching rows, system-only rows (bank side is NULL), and bank-only rows (system side is NULL).
2. **`COALESCE(s.txn_id, b.txn_id)`** — ensures `txn_id` is non-NULL regardless of which side the row came from.
3. **`b.amount - s.amount`** — computes variance; NULL arithmetic naturally yields NULL when either operand is missing.
4. **`WHERE` clause** — excludes transactions that match exactly on both sides.
5. **`ORDER BY txn_id`** — consistent, predictable ordering.
