Given a table `user_purchases` with columns `user_id`, `purchase_date`, and `items` (a comma-separated list of purchased items per transaction), collect all items a user has ever purchased into a **single deduplicated array**.

Return columns: `user_id`, `all_items` (array of unique items, sorted alphabetically)

Order by `user_id` ascending.
