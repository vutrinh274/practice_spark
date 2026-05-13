Given a table `products` with columns `product_id`, `product_name`, `category`, and `price`, add a `price_tier` column based on the following rules:

- `price < 50` → `'Budget'`
- `price >= 50` AND `price < 500` → `'Mid-range'`
- `price >= 500` → `'Premium'`

Return columns: `product_id`, `product_name`, `price`, `price_tier`

Order by `price` ascending.
