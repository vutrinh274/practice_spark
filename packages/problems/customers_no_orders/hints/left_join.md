Use a `LEFT JOIN` — it keeps all rows from the left table (customers) even if there's no match in the right table (orders). Unmatched rows get NULL for all order columns.
