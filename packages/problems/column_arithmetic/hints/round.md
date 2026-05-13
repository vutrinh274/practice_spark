Use `ROUND(expression, 2)` in SQL or `F.round(F.col(...), 2)` in DataFrame API to round to 2 decimal places.

Watch out for integer division — `discount_pct / 100` with integer columns may truncate. Cast to float: `discount_pct / 100.0`.
