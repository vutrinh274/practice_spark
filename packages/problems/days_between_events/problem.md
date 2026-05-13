Given a table `user_events` with columns `event_id`, `user_id`, `event_type`, and `event_date`, compute the **number of days between each user's signup and their first purchase**.

Each user has exactly one row with `event_type = 'signup'` and one row with `event_type = 'first_purchase'`.

Return columns: `user_id`, `signup_date`, `first_purchase_date`, `days_to_purchase`

Order by `user_id` ascending.

> Hint: Use `DATEDIFF(first_purchase_date, signup_date)` or pivot both events onto the same row first, then subtract.
