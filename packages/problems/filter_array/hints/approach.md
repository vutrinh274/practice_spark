1. In the `WHERE` clause, apply `SPLIT(interests, ',')` to get an array.
2. Wrap it in `ARRAY_CONTAINS(..., 'Technology')`.
3. Select `user_id` and `name`.
4. Order by `user_id` ascending.
