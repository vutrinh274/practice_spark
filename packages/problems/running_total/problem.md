Given a table `orders` with columns `order_date`, `customer_id`, and `amount`, compute the **running total of amount per customer**, ordered by `order_date`.

Return columns: `customer_id`, `order_date`, `amount`, `running_total`

Order the result by `customer_id` ascending, then `order_date` ascending.

**Hint:** Use `SUM() OVER (PARTITION BY ... ORDER BY ... ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`.
