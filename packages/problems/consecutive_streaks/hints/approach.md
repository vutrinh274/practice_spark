# Approach

## Step-by-Step Plan

1. **Filter** rows where `status = 'Present'`.
2. **Assign a row number** per employee ordered by `attendance_date`:
   `ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY attendance_date) AS rn`
3. **Compute the group key**:
   `DATE_SUB(attendance_date, rn)` — same value for all consecutive dates in the same island.
4. **Count** rows per `(employee_id, group_key)` → streak length.
5. **Aggregate** `MAX(streak_length)` per employee.

## Pseudocode

```
present = attendance WHERE status = 'Present'

rn = ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY attendance_date)
grp = DATE_SUB(attendance_date, rn)   -- island anchor

streaks = GROUP BY employee_id, grp → COUNT(*) AS streak_len

result = GROUP BY employee_id → MAX(streak_len) AS max_streak
```

## Tips

- In Spark SQL use `DATE_SUB(attendance_date, rn)` or `attendance_date - INTERVAL rn DAYS`.
- In the DataFrame API use `F.date_sub(F.col("attendance_date"), F.col("rn"))`.
