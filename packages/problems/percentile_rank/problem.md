Given a table `sales_reps` with columns `rep_id`, `name`, `region`, and `total_sales`, compute each sales rep's **percent rank** and **quartile (NTILE 4)** within their region, both ranked by `total_sales` descending.

Round `pct_rank` to 2 decimal places.

Return columns: `rep_id`, `name`, `region`, `total_sales`, `pct_rank`, `quartile`

Order by `region` ascending, then `total_sales` descending.
