## SQL Solution

```sql
SELECT e.employee_id, e.name, e.department, m.name AS manager_name
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id
ORDER BY e.employee_id
```

**Why it works:**
- The same table is joined to itself with two aliases: `e` (employee) and `m` (manager)
- `LEFT JOIN` ensures employees without a manager (NULL `manager_id`) still appear
- `m.name AS manager_name` picks the manager's name from the second copy
