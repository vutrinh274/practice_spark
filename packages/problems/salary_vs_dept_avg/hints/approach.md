Use `AVG(salary) OVER (PARTITION BY department)` to compute the department average on each row without collapsing rows. Then subtract the average from the individual salary to get the difference.
