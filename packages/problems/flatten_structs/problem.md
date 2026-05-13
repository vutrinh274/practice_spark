Given a table `orders` with columns `order_id`, `customer_name`, `address`, and `items_count`, where `address` is a JSON string containing the keys `street`, `city`, and `zip`:

Extract the address fields into separate columns.

Return columns: `order_id`, `customer_name`, `street`, `city`, `zip`, `items_count`.

Order by `order_id` ascending.
