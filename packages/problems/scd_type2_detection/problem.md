Given a table `employee_history` with columns `record_id`, `employee_id`, `name`, `department`, `salary`, and `effective_date`, implement a **Slowly Changing Dimension Type 2** transformation.

For each record add:
- `end_date` — the `effective_date` of the next record for that employee (ordered by `effective_date`), or `NULL` if it is the most recent record
- `is_current` — `1` if `end_date` is NULL (the current active record), `0` otherwise

Return columns: `record_id`, `employee_id`, `name`, `department`, `salary`, `effective_date`, `end_date`, `is_current`.

Order by `employee_id` ascending, then `effective_date` ascending.
