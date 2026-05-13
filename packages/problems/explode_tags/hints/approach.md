1. Use `SPLIT(tags, ',')` to convert the comma-separated string into an array.
2. Wrap it in `EXPLODE(...)` to produce one row per tag.
3. Select `product_id`, `product_name`, and the exploded value aliased as `tag`.
4. Order by `product_id`, then `tag`.
