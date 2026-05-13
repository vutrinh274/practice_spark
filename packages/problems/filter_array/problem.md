Given a table `user_interests` with columns `user_id`, `name`, and `interests` (a comma-separated string), find all users who are interested in **'Technology'**.

Return columns: `user_id`, `name`

Order by `user_id` ascending.

> Hint: Use `ARRAY_CONTAINS(SPLIT(interests, ','), 'Technology')` to check for membership after splitting.
