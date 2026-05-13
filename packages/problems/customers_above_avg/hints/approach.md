In SQL: use a subquery or CTE to compute `total_spend` per customer, then wrap it with `HAVING total_spend > (SELECT AVG(total_spend) FROM ...)`.

In the DataFrame API: compute the per-customer totals first, then derive the average of those totals and filter.
