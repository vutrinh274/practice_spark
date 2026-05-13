# Solution: SQL

```sql
WITH ranked AS (
    SELECT
        department,
        employee_id,
        name,
        salary,
        ROW_NUMBER() OVER (
            PARTITION BY department
            ORDER BY salary DESC, employee_id ASC
        ) AS row_num
    FROM employees
)
SELECT
    department,
    employee_id,
    name,
    salary,
    row_num
FROM ranked
WHERE row_num <= 2
ORDER BY department, row_num
```

## Explanation

1. **`ranked` CTE** — assigns a unique row number to every employee within their department. The ordering `salary DESC, employee_id ASC` puts the highest earner first and uses the lower employee ID as a deterministic tiebreaker for equal salaries.
2. **`WHERE row_num <= 2`** — retains only the top 2 employees per department. Because `ROW_NUMBER` never produces duplicates, exactly 2 rows per department pass the filter.
3. **`ORDER BY department, row_num`** — presents results department by department, with rank 1 before rank 2.
