## SQL Solution

```sql
SELECT employee_id,
       name,
       department,
       salary,
       ROUND(AVG(salary) OVER (PARTITION BY department), 2) AS dept_avg_salary,
       ROUND(salary - AVG(salary) OVER (PARTITION BY department), 2) AS diff_from_avg
FROM employees
ORDER BY department, employee_id
```

**Why it works:**
- `AVG(salary) OVER (PARTITION BY department)` computes the average within each department without reducing rows
- Each row retains its original salary alongside the department-level average
- Subtracting the two gives the difference; positive means above average, negative means below
