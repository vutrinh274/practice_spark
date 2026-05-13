Given a table `sales` with columns `sale_id`, `sale_date`, and `amount`, compare total revenue on **weekends vs weekdays**.

A day is a **Weekend** if it falls on Saturday or Sunday, otherwise it is a **Weekday**.

Return columns: `day_type` (either `'Weekend'` or `'Weekday'`), `total_revenue`, `num_sales`

Order by `day_type` ascending (alphabetical).

> Hint: In Spark, `DAYOFWEEK` returns `1` for Sunday and `7` for Saturday.
