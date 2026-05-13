Given a table `product_sales` with columns `product_id`, `product_name`, `year`, and `total_sales`, find all products that had **consistently increasing sales every year** from 2021 to 2024.

A product qualifies if its sales increased in every single year-over-year comparison (2021→2022, 2022→2023, and 2023→2024 must all be positive growth).

Return columns: `product_id`, `product_name`.

Order by `product_id` ascending.
