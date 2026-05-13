Given a table `user_activity` with columns `user_id`, `signup_date`, and `activity_date`, perform a **cohort retention analysis**.

Group users into cohorts based on their signup month. For each cohort, count how many distinct users were active in month 0 (signup month), month 1, month 2, and month 3 after signup.

Return columns: `cohort_month` (format `yyyy-MM`), `months_since_signup` (INT), `active_users` (INT).

Only include rows where `months_since_signup` is between 0 and 3 (inclusive).

Order by `cohort_month` ascending, then `months_since_signup` ascending.
