Given a table `etl_jobs` with columns `job_id`, `job_name`, `pipeline`, `start_time`, `end_time`, `status`, and `rows_processed`, compute summary statistics for each pipeline.

For each pipeline calculate:
- `total_runs` — total number of job runs
- `success_rate` — percentage of successful runs, rounded to 2 decimal places
- `avg_duration_seconds` — average job duration in seconds, rounded to 2 decimal places
- `avg_rows_processed` — average rows processed per run, rounded to 2 decimal places
- `rank` — pipeline ranked by `success_rate` descending (use DENSE_RANK)

Return columns: `pipeline`, `total_runs`, `success_rate`, `avg_duration_seconds`, `avg_rows_processed`, `rank`.

Order by `rank` ascending.
