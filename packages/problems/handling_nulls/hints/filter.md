After replacing NULLs, filter out rows where salary is 0. Apply `COALESCE` in the `SELECT` first, then filter in `WHERE` or use a subquery.

```sql
SELECT employee_id, name, COALESCE(department, 'Unknown') AS department,
       COALESCE(salary, 0) AS salary
FROM employees
WHERE COALESCE(salary, 0) > 0
ORDER BY employee_id
```
