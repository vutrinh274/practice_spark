Use `LEFT JOIN` so employees without a manager still appear (with NULL for manager_name):

```sql
SELECT e.employee_id, e.name, e.department, m.name AS manager_name
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id
ORDER BY e.employee_id
```
