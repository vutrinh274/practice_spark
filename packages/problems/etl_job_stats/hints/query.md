```sql
WITH pipeline_stats AS (
    SELECT
        pipeline,
        COUNT(*) AS total_runs,
        ROUND(SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS success_rate,
        ROUND(AVG(UNIX_TIMESTAMP(end_time) - UNIX_TIMESTAMP(start_time)), 2) AS avg_duration_seconds,
        ROUND(AVG(rows_processed), 2) AS avg_rows_processed
    FROM etl_jobs
    GROUP BY pipeline
)
SELECT
    pipeline,
    total_runs,
    success_rate,
    avg_duration_seconds,
    avg_rows_processed,
    DENSE_RANK() OVER (ORDER BY success_rate DESC) AS rank
FROM pipeline_stats
ORDER BY rank
```
