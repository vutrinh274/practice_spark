# Customer Loyalty Score

**Difficulty:** Hard
**Tags:** aggregation, joins, composite scoring

## Background

The marketing team wants to rank customers by a composite loyalty score that balances purchase frequency, average spend, and customer satisfaction ratings.

## Schema

**orders** (`orders.csv`)

| Column | Type | Description |
|---|---|---|
| order_id | INT | Unique order identifier |
| customer_id | INT | Customer who placed the order |
| amount | INT | Order value in USD |
| order_date | STRING | Date the order was placed |

**ratings** (`ratings.csv`)

| Column | Type | Description |
|---|---|---|
| rating_id | INT | Unique rating identifier |
| customer_id | INT | Customer who left the rating |
| score | INT | Satisfaction score (1–5) |

## Task

Compute a loyalty score for each customer:

```
loyalty_score = ROUND(
    (total_orders * 0.3) + (avg_order_value * 0.5) + (avg_rating * 0.2),
    2
)
```

Return: **customer_id, total_orders, avg_order_value, avg_rating, loyalty_score**

- `avg_order_value` rounded to 2 decimal places
- `avg_rating` rounded to 2 decimal places
- `loyalty_score` rounded to 2 decimal places

Order by: **loyalty_score DESC**
