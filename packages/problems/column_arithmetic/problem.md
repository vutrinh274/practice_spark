Given a table `products` with columns `product_id`, `product_name`, `price`, `quantity`, and `discount_pct`, compute the following for each product:

- `discounted_price` = `price * (1 - discount_pct / 100)`  (rounded to 2 decimal places)
- `total_revenue` = `discounted_price * quantity`  (rounded to 2 decimal places)

Return columns: `product_id`, `product_name`, `discounted_price`, `total_revenue`

Order by `total_revenue` descending.
