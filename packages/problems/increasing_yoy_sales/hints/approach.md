1. Use `LAG(total_sales) OVER (PARTITION BY product_id ORDER BY year)` to get the previous year's sales.
2. Compute `yoy_growth = total_sales - prev_sales` for each row.
3. Filter out the first year (where `prev_sales` is NULL — no prior year to compare).
4. Group by `product_id` and `product_name`, then take `MIN(yoy_growth)`.
5. Keep only products where `MIN(yoy_growth) > 0` — this guarantees all YoY comparisons were positive.
6. Order by `product_id`.
