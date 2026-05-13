```sql
SELECT employee_id, Present, Absent, Late
FROM (
    SELECT employee_id, status FROM attendance
)
PIVOT (
    COUNT(*) FOR status IN ('Present' AS Present, 'Absent' AS Absent, 'Late' AS Late)
)
ORDER BY employee_id
```
