Given a table `products_with_arrays` with columns `product_id`, `product_name`, and `tags` (a comma-separated string of tags), **split and explode** the tags so that each tag gets its own row.

Return columns: `product_id`, `product_name`, `tag`

Order by `product_id` ascending, then `tag` ascending.

> Hint: Use `SPLIT(tags, ',')` to turn the string into an array, then `EXPLODE(...)` to expand the array into rows.
