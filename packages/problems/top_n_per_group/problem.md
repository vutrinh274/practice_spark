Given a table `employees` with columns `department`, `employee`, and `salary`, return the **top 2 highest-paid employees per department**.

Return columns: `department`, `employee`, `salary`, `rank`

Order the result by `department` ascending, then `rank` ascending.

**Hint:** Use a window function with `RANK()` or `ROW_NUMBER()` partitioned by `department`.
