## SQL Solution

```sql
SELECT
    DATE_FORMAT(signup_date, 'yyyy-MM') AS cohort_month,
    CAST(MONTHS_BETWEEN(activity_date, signup_date) AS INT) AS months_since_signup,
    COUNT(DISTINCT user_id) AS active_users
FROM user_activity
WHERE CAST(MONTHS_BETWEEN(activity_date, signup_date) AS INT) BETWEEN 0 AND 3
GROUP BY
    DATE_FORMAT(signup_date, 'yyyy-MM'),
    CAST(MONTHS_BETWEEN(activity_date, signup_date) AS INT)
ORDER BY cohort_month, months_since_signup
```

**Why it works:**
- `DATE_FORMAT(signup_date, 'yyyy-MM')` truncates the signup date to month granularity, defining the cohort
- `MONTHS_BETWEEN(activity_date, signup_date)` computes the fractional months elapsed; casting to INT gives whole months
- `WHERE ... BETWEEN 0 AND 3` restricts to the 4-month retention window
- `COUNT(DISTINCT user_id)` ensures each user is counted only once per cohort/month bucket
