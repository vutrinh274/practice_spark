## SQL Solution

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

**Why it works:**
- The inner query selects only the columns needed for the pivot
- `PIVOT` rotates distinct values of `status` into columns
- `COUNT(*)` aggregates occurrences of each status per employee
- Missing combinations default to `NULL` (no days with that status)
