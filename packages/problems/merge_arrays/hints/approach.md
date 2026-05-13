1. Use a subquery to `EXPLODE(SPLIT(items, ','))` so each item is its own row.
2. In the outer query, `GROUP BY user_id` and use `COLLECT_LIST(DISTINCT item)` to gather unique items.
3. To sort the resulting array alphabetically, wrap with `ARRAY_SORT(...)`.
4. Order the final result by `user_id`.
