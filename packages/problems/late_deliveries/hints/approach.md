1. Compute `actual_days = DATEDIFF(delivery_date, order_date)`.
2. Compute `days_late = actual_days - promised_days`.
3. Filter rows where `actual_days > promised_days` (equivalently, `days_late > 0`).
4. Select `order_id`, `customer_id`, `promised_days`, `actual_days`, `days_late`.
5. Order by `days_late` descending.

You can do steps 1–3 in a subquery or CTE, then filter in the outer query.
