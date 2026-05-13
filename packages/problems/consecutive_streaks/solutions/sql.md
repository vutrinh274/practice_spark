# Solution: SQL

```sql
WITH present AS (
    SELECT employee_id, attendance_date
    FROM attendance
    WHERE status = 'Present'
),
numbered AS (
    SELECT
        employee_id,
        attendance_date,
        ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY attendance_date) AS rn
    FROM present
),
islands AS (
    SELECT
        employee_id,
        DATE_SUB(attendance_date, rn) AS grp,
        COUNT(*) AS streak_len
    FROM numbered
    GROUP BY employee_id, DATE_SUB(attendance_date, rn)
)
SELECT
    employee_id,
    MAX(streak_len) AS max_streak
FROM islands
GROUP BY employee_id
ORDER BY employee_id
```

## Explanation

1. **`present` CTE** — restricts the dataset to Present days only.
2. **`numbered` CTE** — assigns a sequential row number per employee ordered by date. This is the "rank within island" counter.
3. **`islands` CTE** — subtracting the integer row number from the date produces the same anchor date for all consecutive days in the same run. Grouping on this anchor and counting gives each island's length.
4. **Final SELECT** — takes the maximum streak per employee.
