1. Use a subquery (or CTE) to `EXPLODE(SPLIT(tags, ','))` so each tag becomes a separate row.
2. In the outer query, `GROUP BY product_id, product_name` and `COUNT(*)` to get `tag_count`.
3. Order by `tag_count DESC`, then `product_id ASC` to break ties.
