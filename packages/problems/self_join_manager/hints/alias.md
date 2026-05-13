Use table aliases to distinguish the two copies of the table:

```sql
FROM employees e        -- the employee
LEFT JOIN employees m   -- the manager
ON e.manager_id = m.employee_id
```
