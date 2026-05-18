1. For each player, use `LAG(scoring_class)` and `LAG(is_active)` over `(PARTITION BY player_name ORDER BY season)` to compare each row to its predecessor.
2. Mark a row as the start of a new run when the previous value is NULL (first season) or when either attribute differs from the previous row.
3. Take a cumulative `SUM` of that "is_change" flag over the same window — the running total is a stable id for each run of unchanged attributes.
4. Group by `(player_name, run_id, scoring_class, is_active)` and aggregate `MIN(season)` as `start_season`, `MAX(season)` as `end_season`.
5. Use `MAX(season) OVER (PARTITION BY player_name)` to attach `current_season` to each row.
6. Order by `player_name`, then `start_season`.
