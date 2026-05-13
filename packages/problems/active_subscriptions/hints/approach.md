1. Filter the `subscriptions` table with two conditions joined by `AND`:
   - `start_date <= '2024-06-15'`
   - `end_date >= '2024-06-15'`
2. Select only the required columns: `sub_id`, `customer_id`, `plan`, `start_date`, `end_date`.
3. Order by `sub_id` ascending.
