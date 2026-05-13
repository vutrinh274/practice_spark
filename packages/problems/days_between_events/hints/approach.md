Use conditional aggregation to pivot the two event types into columns:

1. Group by `user_id`.
2. Use `MAX(CASE WHEN event_type = 'signup' THEN event_date END)` to get `signup_date`.
3. Use `MAX(CASE WHEN event_type = 'first_purchase' THEN event_date END)` to get `first_purchase_date`.
4. Wrap the result in an outer query and apply `DATEDIFF(first_purchase_date, signup_date)`.
5. Order by `user_id`.
