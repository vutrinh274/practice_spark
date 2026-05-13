# Query Hint

## SQL Skeleton

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

## DataFrame Skeleton

```python
joined = (
    system_ledger.alias("s")
    .join(bank_ledger.alias("b"), on="txn_id", how="full")
    .select(
        F.col("txn_id"),
        F.col("s.amount").alias("system_amount"),
        F.col("b.amount").alias("bank_amount"),
        (F.col("b.amount") - F.col("s.amount")).alias("variance"),
    )
)

result = (
    joined.filter(
        (F.col("system_amount") != F.col("bank_amount"))
        | F.col("system_amount").isNull()
        | F.col("bank_amount").isNull()
    )
    .orderBy("txn_id")
)
```
