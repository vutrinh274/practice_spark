Use `SUM() OVER (PARTITION BY customer_id ORDER BY order_date)` — the window orders rows by date so the sum accumulates chronologically per customer.
