After a FULL OUTER JOIN, `department_id` may come from either table. Use `COALESCE(e.department_id, d.department_id)` to get a non-NULL value when possible.
