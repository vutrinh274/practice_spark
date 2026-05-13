1. Use `DATE_FORMAT(activity_date, 'yyyy-MM')` to extract the year-month string.
2. Group by the resulting `month` column.
3. Use `COUNT(DISTINCT user_id)` (SQL) or `F.countDistinct("user_id")` (DataFrame) to count unique users.
4. Order the result by `month` ascending.
