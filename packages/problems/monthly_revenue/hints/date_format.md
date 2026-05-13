Use `DATE_FORMAT(order_date, 'yyyy-MM')` in Spark SQL to extract the year-month string.

In DataFrame API: `F.date_format(F.col("order_date"), "yyyy-MM")`
