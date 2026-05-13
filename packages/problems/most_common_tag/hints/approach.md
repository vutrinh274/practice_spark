1. Use a subquery to `EXPLODE(SPLIT(tags, ','))` to get one row per tag per article.
2. In an intermediate layer, `GROUP BY category, tag` and `COUNT(*)` to get `tag_count`.
3. Apply `RANK() OVER (PARTITION BY category ORDER BY tag_count DESC)` to rank tags within each category.
4. Filter to `rnk = 1` and order by `category`.
