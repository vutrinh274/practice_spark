Given a table `orders` with columns `order_id`, `customer_id`, `status`, and `amount`, compute per customer:

- `completed_revenue` — total amount of completed orders
- `cancelled_revenue` — total amount of cancelled orders
- `total_orders` — total number of orders (all statuses)

Return columns: `customer_id`, `completed_revenue`, `cancelled_revenue`, `total_orders`

Order by `customer_id` ascending.
