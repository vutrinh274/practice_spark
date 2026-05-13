# Approach

## Step-by-Step Plan

1. **Aggregate orders** per customer:
   - `COUNT(*)` → `total_orders`
   - `ROUND(AVG(amount), 2)` → `avg_order_value`
2. **Aggregate ratings** per customer:
   - `ROUND(AVG(score), 2)` → `avg_rating`
3. **Join** the two aggregated DataFrames on `customer_id`.
4. **Compute loyalty score**:
   ```
   ROUND((total_orders * 0.3) + (avg_order_value * 0.5) + (avg_rating * 0.2), 2)
   ```
5. **Select** `customer_id, total_orders, avg_order_value, avg_rating, loyalty_score`.
6. **Order** by `loyalty_score DESC`.

## Tips

- Use an inner join — every customer has both orders and ratings in this dataset.
- Cast the weights to `DOUBLE` or use decimal literals (`0.3`, `0.5`, `0.2`) to avoid integer arithmetic truncation.
