```sql
SELECT
    record_id,
    employee_id,
    name,
    department,
    salary,
    effective_date,
    LEAD(effective_date) OVER (PARTITION BY employee_id ORDER BY effective_date) AS end_date,
    CASE WHEN LEAD(effective_date) OVER (PARTITION BY employee_id ORDER BY effective_date) IS NULL
         THEN 1 ELSE 0 END AS is_current
FROM employee_history
ORDER BY employee_id, effective_date
```
