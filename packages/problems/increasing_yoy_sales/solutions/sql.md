## SQL Solution

```sql
WITH yoy AS (
    SELECT
        product_id,
        product_name,
        total_sales - LAG(total_sales) OVER (PARTITION BY product_id ORDER BY year) AS yoy_growth
    FROM product_sales
)
SELECT product_id, product_name
FROM yoy
WHERE yoy_growth IS NOT NULL
GROUP BY product_id, product_name
HAVING MIN(yoy_growth) > 0
ORDER BY product_id
```

**Why it works:**
- `LAG(total_sales) OVER (PARTITION BY product_id ORDER BY year)` returns the previous year's sales within each product group
- Subtracting it from the current year's sales gives the raw growth; NULL for the first year (no prior row)
- `WHERE yoy_growth IS NOT NULL` excludes the first year row which has no comparison
- `HAVING MIN(yoy_growth) > 0` ensures every single YoY comparison was strictly positive — one flat or down year disqualifies the product
