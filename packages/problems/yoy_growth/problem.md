Given a table `annual_revenue` with columns `year`, `category`, and `revenue`, compute the **year-over-year revenue growth percentage** for each category.

Formula: `(revenue - prev_year_revenue) / prev_year_revenue * 100`

Round `yoy_growth_pct` to 2 decimal places. For the first year of each category, `yoy_growth_pct` should be `NULL`.

Return columns: `category`, `year`, `revenue`, `yoy_growth_pct`

Order by `category` ascending, then `year` ascending.
