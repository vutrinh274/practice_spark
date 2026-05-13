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
