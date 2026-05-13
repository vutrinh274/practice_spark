Given tables `employees` and `departments`, produce a **full report** showing:
- All employees (even those in departments not in the `departments` table)
- All departments (even those with no employees)

Return columns: `employee_id`, `name`, `department_id`, `department_name`, `budget`

Use `COALESCE` to fill NULL `department_id` from either table. Order by `department_id` ascending (NULLs last), then `employee_id` ascending.
