Given a table `subscriptions` with columns `sub_id`, `customer_id`, `start_date`, `end_date`, and `plan`, find all subscriptions that were **active on 2024-06-15**.

A subscription is active on a given date if `start_date <= '2024-06-15' AND end_date >= '2024-06-15'`.

Return columns: `sub_id`, `customer_id`, `plan`, `start_date`, `end_date`

Order by `sub_id` ascending.
