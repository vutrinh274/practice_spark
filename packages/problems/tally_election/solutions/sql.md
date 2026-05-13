# Solution: SQL

```sql
WITH vote_counts AS (
    SELECT
        district,
        candidate,
        COUNT(*) AS votes
    FROM votes
    GROUP BY district, candidate
),
ranked AS (
    SELECT
        district,
        candidate,
        votes,
        RANK() OVER (PARTITION BY district ORDER BY votes DESC) AS rnk
    FROM vote_counts
)
SELECT
    district,
    candidate,
    votes
FROM ranked
WHERE rnk = 1
ORDER BY district
```

## Explanation

1. **`vote_counts` CTE** — aggregates the ballot table to get the total votes per district–candidate pair.
2. **`ranked` CTE** — applies `RANK()` within each district ordered by votes descending. The candidate with the most votes gets `rnk = 1`.
3. **Final SELECT** — filters to only the top-ranked candidate per district and orders alphabetically by district.
