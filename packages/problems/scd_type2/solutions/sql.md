## SQL Solution

```sql
SELECT
    record_id,
    employee_id,
    name,
    department,
    salary,
    effective_date,
    LEAD(effective_date) OVER (PARTITION BY employee_id ORDER BY effective_date) AS end_date,
    CASE
        WHEN LEAD(effective_date) OVER (PARTITION BY employee_id ORDER BY effective_date) IS NULL
        THEN 1
        ELSE 0
    END AS is_current
FROM employee_history
ORDER BY employee_id, effective_date
```

**Why it works:**
- `LEAD(effective_date) OVER (PARTITION BY employee_id ORDER BY effective_date)` peeks at the next row's start date within each employee group — this becomes the current row's `end_date`
- When there is no next row (the most recent record), `LEAD` returns NULL, indicating the record is still active
- The `CASE WHEN` translates the NULL into the `is_current = 1` flag
- No self-join is needed — the entire logic is expressed with a single window function pass
