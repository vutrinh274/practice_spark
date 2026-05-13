Given a table `employees` where each row has an `employee_id`, `name`, `department`, and `manager_id` (which references another `employee_id`), return each employee along with their manager's name.

Employees without a manager (top-level) should have `NULL` for `manager_name`.

Return columns: `employee_id`, `name`, `department`, `manager_name`

Order by `employee_id` ascending.
