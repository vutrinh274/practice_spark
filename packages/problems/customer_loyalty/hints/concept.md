# Concept: Composite Scoring via Aggregation and Join

This problem combines data from two separate tables using a join, then applies multi-column aggregation followed by a weighted formula.

## Pattern: Aggregate–Join–Compute

1. **Aggregate each table independently** to produce one row per customer.
2. **Join** the two aggregated results on `customer_id`.
3. **Apply the formula** to produce the composite score.

This is more efficient than joining the raw tables first and then aggregating, because each aggregation reduces the row count before the join.

## Rounding

Use `ROUND(expression, 2)` in SQL or `F.round(col, 2)` in the DataFrame API. Apply rounding to each intermediate metric as well as the final score, as specified in the problem.

## Weighted Formula

```
loyalty_score = (total_orders × 0.3) + (avg_order_value × 0.5) + (avg_rating × 0.2)
```

The weights reflect business priorities: average spend is the strongest driver, followed by frequency, then satisfaction.
