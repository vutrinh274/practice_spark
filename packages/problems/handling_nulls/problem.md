Given a table `employees` with columns `employee_id`, `name`, `department`, and `salary`, return all employees with their details where:

- Replace NULL `department` with `'Unknown'`
- Replace NULL `salary` with `0`
- Only return employees whose `salary` (after replacement) is greater than `0`

Return columns: `employee_id`, `name`, `department`, `salary`

Order by `employee_id` ascending.
