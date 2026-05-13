Given a table `purchases` with columns `purchase_id`, `customer_id`, `purchase_date`, and `amount`, find the **next purchase date** for each purchase by the same customer.

If there is no subsequent purchase by the customer, `next_purchase_date` should be `NULL`.

Return columns: `purchase_id`, `customer_id`, `purchase_date`, `next_purchase_date`

Order by `customer_id` ascending, then `purchase_date` ascending.
