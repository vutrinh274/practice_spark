Given a table `products` with columns `product_id`, `product_name`, and `tag` (one tag per row), aggregate all tags for each product into an **array**.

Return columns: `product_id`, `product_name`, `tags` (array of strings collected with `COLLECT_LIST`)

Order by `product_id` ascending.
