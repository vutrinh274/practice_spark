1. Compute duration in seconds: `UNIX_TIMESTAMP(end_time) - UNIX_TIMESTAMP(start_time)`.
2. Compute `success_rate` as `ROUND(SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2)`.
3. Use `ROUND(AVG(duration_seconds), 2)` and `ROUND(AVG(rows_processed), 2)` for the average metrics.
4. Apply `DENSE_RANK() OVER (ORDER BY success_rate DESC)` to rank pipelines.
5. Order the final result by `rank` ascending.
