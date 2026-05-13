1. Use `LEAD(effective_date) OVER (PARTITION BY employee_id ORDER BY effective_date)` to look ahead to the next record's start date — this becomes the current record's `end_date`.
2. When `LEAD` returns NULL (no next row), the record is the most recent one for that employee.
3. Derive `is_current` with `CASE WHEN end_date IS NULL THEN 1 ELSE 0 END`.
4. Order the result by `employee_id`, then `effective_date`.
