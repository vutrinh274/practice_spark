Use `SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END)` to sum only matching rows.

In DataFrame API: `F.sum(F.when(F.col("status") == "completed", F.col("amount")).otherwise(0))`
