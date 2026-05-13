# Solution: DataFrame API

```python
# F (pyspark.sql.functions) and Window are pre-imported

# Rename amount columns before joining so both are accessible after
sys_df  = system_ledger.select(F.col("txn_id"), F.col("amount").alias("system_amount"))
bank_df = bank_ledger.select(F.col("txn_id"), F.col("amount").alias("bank_amount"))

joined = sys_df.join(bank_df, on="txn_id", how="full")

result = (
    joined
    .withColumn("variance", F.col("bank_amount") - F.col("system_amount"))
    .filter(
        (F.col("system_amount") != F.col("bank_amount"))
        | F.col("system_amount").isNull()
        | F.col("bank_amount").isNull()
    )
    .select("txn_id", "system_amount", "bank_amount", "variance")
    .orderBy("txn_id")
)

result.show()
```

## Explanation

- Renaming `amount` in each DataFrame before the join prevents column ambiguity and makes subsequent expressions clear.
- `how="full"` ensures rows missing from either side are preserved with NULL.
- The filter removes perfectly matching rows, leaving only discrepancies.
- `bank_amount - system_amount` naturally yields NULL for one-sided transactions.
