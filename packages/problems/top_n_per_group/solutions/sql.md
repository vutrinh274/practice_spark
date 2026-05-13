## SQL Solution

```sql
SELECT department, employee, salary, rank
FROM (
  SELECT department, employee, salary,
         RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rank
  FROM employees
)
WHERE rank <= 2
ORDER BY department, rank
```

**Why it works:**
- `RANK() OVER (PARTITION BY department ORDER BY salary DESC)` assigns a rank within each department, highest salary = rank 1
- The outer query filters `rank <= 2` to keep only the top 2
- `ORDER BY department, rank` gives the required sort order
