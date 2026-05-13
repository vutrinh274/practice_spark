# Approach

## Step-by-Step Plan

1. **Aggregate** — `GROUP BY district, candidate` and `COUNT(*)` → `votes`.
2. **Rank** — `RANK() OVER (PARTITION BY district ORDER BY votes DESC)` → `rnk`.
3. **Filter** — keep only rows where `rnk = 1`.
4. **Select** — `district, candidate, votes`.
5. **Order** — by `district ASC`.

## Pseudocode

```
vote_counts = GROUP BY district, candidate → COUNT(*) AS votes

ranked = vote_counts
    .withColumn("rnk", RANK() OVER (PARTITION BY district ORDER BY votes DESC))

result = ranked
    .filter(rnk == 1)
    .select("district", "candidate", "votes")
    .orderBy("district")
```

## Alternative: Subquery / CTE

Use a CTE to compute counts first, then add the rank in the outer query. This is cleaner in SQL.
