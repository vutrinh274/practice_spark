## SQL Solution

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

**Why it works:**
- `UNIX_TIMESTAMP(end_time) - UNIX_TIMESTAMP(start_time)` converts timestamp strings to seconds and takes the difference
- The `CASE WHEN` expression turns status into a 0/1 flag; multiplying by 100.0 and dividing by COUNT gives the percentage
- `DENSE_RANK() OVER (ORDER BY success_rate DESC)` assigns rank 1 to the pipeline with the highest success rate; ties get the same rank
- The CTE separates aggregation from ranking, keeping the query readable
