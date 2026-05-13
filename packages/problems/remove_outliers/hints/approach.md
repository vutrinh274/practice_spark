Use `percentile_approx(amount, 0.25)` for Q1 and `percentile_approx(amount, 0.75)` for Q3 in a CTE or subquery to get the bounds, then join or cross join back to the original table to filter rows.
