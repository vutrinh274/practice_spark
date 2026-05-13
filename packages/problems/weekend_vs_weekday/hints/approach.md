1. Use `DAYOFWEEK(sale_date)` to get the numeric day of the week.
2. Wrap it in a `CASE WHEN` to produce `'Weekend'` when the result is `1` (Sunday) or `7` (Saturday), and `'Weekday'` otherwise.
3. Group by the resulting `day_type` column.
4. Aggregate with `SUM(amount)` and `COUNT(*)`.
5. Order by `day_type` ascending.
