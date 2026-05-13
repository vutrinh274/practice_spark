Use `COALESCE(column, default_value)` to replace NULLs — it returns the first non-NULL value in the list.

```sql
COALESCE(department, 'Unknown')
COALESCE(salary, 0)
```

In DataFrame API: `F.coalesce(F.col("department"), F.lit("Unknown"))`
