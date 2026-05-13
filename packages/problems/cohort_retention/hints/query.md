```sql
SELECT
    DATE_FORMAT(signup_date, 'yyyy-MM') AS cohort_month,
    CAST(MONTHS_BETWEEN(activity_date, signup_date) AS INT) AS months_since_signup,
    COUNT(DISTINCT user_id) AS active_users
FROM user_activity
WHERE CAST(MONTHS_BETWEEN(activity_date, signup_date) AS INT) BETWEEN 0 AND 3
GROUP BY cohort_month, months_since_signup
ORDER BY cohort_month, months_since_signup
```
