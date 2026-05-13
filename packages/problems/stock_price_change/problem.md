Given a table `stock_prices` with columns `price_date`, `stock`, and `close_price`, compute the **daily price change** for each stock. The price change is `close_price - previous_day_close_price`.

For the first trading day of each stock, `price_change` should be `NULL`.

Return columns: `stock`, `price_date`, `close_price`, `price_change`

Order by `stock` ascending, then `price_date` ascending.
