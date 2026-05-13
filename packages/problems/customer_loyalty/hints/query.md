# Query Hint

## SQL Skeleton

```sql
WITH order_stats AS (
    SELECT
        customer_id,
        COUNT(*)          AS total_orders,
        ROUND(AVG(amount), 2) AS avg_order_value
    FROM orders
    GROUP BY customer_id
),
rating_stats AS (
    SELECT
        customer_id,
        ROUND(AVG(score), 2) AS avg_rating
    FROM ratings
    GROUP BY customer_id
)
SELECT
    o.customer_id,
    o.total_orders,
    o.avg_order_value,
    r.avg_rating,
    ROUND((o.total_orders * 0.3) + (o.avg_order_value * 0.5) + (r.avg_rating * 0.2), 2) AS loyalty_score
FROM order_stats o
JOIN rating_stats r ON o.customer_id = r.customer_id
ORDER BY loyalty_score DESC
```

## DataFrame Skeleton

```python
order_stats = (
    orders.groupBy("customer_id")
          .agg(
              F.count("*").alias("total_orders"),
              F.round(F.avg("amount"), 2).alias("avg_order_value")
          )
)

rating_stats = (
    ratings.groupBy("customer_id")
           .agg(F.round(F.avg("score"), 2).alias("avg_rating"))
)

result = (
    order_stats.join(rating_stats, on="customer_id")
               .withColumn(
                   "loyalty_score",
                   F.round(
                       F.col("total_orders") * 0.3
                       + F.col("avg_order_value") * 0.5
                       + F.col("avg_rating") * 0.2,
                       2
                   )
               )
               .select("customer_id", "total_orders", "avg_order_value", "avg_rating", "loyalty_score")
               .orderBy(F.col("loyalty_score").desc())
)
```
