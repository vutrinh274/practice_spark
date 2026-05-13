```sql
FROM employees e
FULL OUTER JOIN departments d ON e.department_id = d.department_id
```

In DataFrame API: `how="outer"` or `how="full"` — both work in Spark.
