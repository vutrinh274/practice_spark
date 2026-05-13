Given a table `orders` with columns `order_id`, `customer_id`, `order_date`, `delivery_date`, and `promised_days`, find all orders that were **delivered late**.

An order is late when the actual delivery took more days than promised:
- `actual_days = DATEDIFF(delivery_date, order_date)`
- `days_late = actual_days - promised_days`
- Late means `actual_days > promised_days`

Return columns: `order_id`, `customer_id`, `promised_days`, `actual_days`, `days_late`

Order by `days_late` descending.
