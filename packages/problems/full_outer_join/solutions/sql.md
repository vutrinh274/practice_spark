## SQL Solution

```sql
SELECT e.employee_id, e.name,
       COALESCE(e.department_id, d.department_id) AS department_id,
       d.department_name, d.budget
FROM employees e
FULL OUTER JOIN departments d ON e.department_id = d.department_id
ORDER BY department_id ASC NULLS LAST, e.employee_id ASC
```

**Why it works:**
- `FULL OUTER JOIN` returns all rows from both tables
- `COALESCE(e.department_id, d.department_id)` handles the case where one side is NULL
- Employees in dept 30 and 40 have no matching department — `department_name` and `budget` are NULL
- Departments 50 and 60 have no employees — `employee_id` and `name` are NULL
