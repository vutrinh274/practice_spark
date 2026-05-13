## SQL Solution

```sql
SELECT employee_id, name,
       COALESCE(department, 'Unknown') AS department,
       COALESCE(salary, 0) AS salary
FROM employees
WHERE COALESCE(salary, 0) > 0
ORDER BY employee_id
```

**Why it works:**
- `COALESCE(department, 'Unknown')` replaces NULL department with 'Unknown'
- `COALESCE(salary, 0)` replaces NULL salary with 0
- `WHERE COALESCE(salary, 0) > 0` filters out rows with no salary
