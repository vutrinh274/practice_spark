1. Use `DATE_FORMAT(signup_date, 'yyyy-MM')` to extract the cohort month for each user.
2. Use `MONTHS_BETWEEN(activity_date, signup_date)` to compute how many months after signup each activity occurred. Cast to INT to get whole months.
3. Filter to keep only rows where `months_since_signup` is between 0 and 3.
4. Group by `cohort_month` and `months_since_signup`, then count distinct users with `COUNT(DISTINCT user_id)`.
5. Order the final result by `cohort_month`, then `months_since_signup`.
