```sql
SELECT employee_id, name, department, salary,
       ROUND(AVG(salary) OVER (PARTITION BY department), 2) AS dept_avg_salary,
       ROUND(salary - AVG(salary) OVER (PARTITION BY department), 2) AS diff_from_avg
FROM employees
ORDER BY department, employee_id
```
