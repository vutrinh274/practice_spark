Use `RANK()` or `ROW_NUMBER()` over the window, assign it as `rank`, then wrap in a subquery and filter `WHERE rank <= 2`.

```sql
SELECT * FROM (
  SELECT *, RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rank
  FROM employees
) WHERE rank <= 2
```
