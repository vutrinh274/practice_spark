**Option A (no explode):** Use `SIZE(SPLIT(tags, ','))` to directly compute the number of elements in each tags string — no grouping needed.

**Option B (explode then group):**
1. Explode the tags into individual rows.
2. Group by `product_id` and `product_name`.
3. Use `COUNT(*)` to count the tags per product.
