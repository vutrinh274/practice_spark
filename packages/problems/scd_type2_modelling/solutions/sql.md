## SQL Solution

```sql
WITH changes AS (
    SELECT
        player_name,
        scoring_class,
        is_active,
        season,
        CASE
            WHEN LAG(scoring_class) OVER w IS NULL
              OR scoring_class <> LAG(scoring_class) OVER w
              OR is_active     <> LAG(is_active) OVER w
            THEN 1 ELSE 0
        END AS is_change
    FROM players
    WINDOW w AS (PARTITION BY player_name ORDER BY season)
),
runs AS (
    SELECT
        *,
        SUM(is_change) OVER (PARTITION BY player_name ORDER BY season) AS streak_id,
        MAX(season)   OVER (PARTITION BY player_name)                  AS current_season
    FROM changes
)
SELECT
    player_name,
    scoring_class,
    is_active,
    current_season,
    MIN(season) AS start_season,
    MAX(season) AS end_season
FROM runs
GROUP BY player_name, streak_id, scoring_class, is_active, current_season
ORDER BY player_name, start_season
```

**Why it works:**
- `LAG` over `(PARTITION BY player_name ORDER BY season)` gives each row a peek at the immediately preceding season's attributes for the same player.
- The `CASE` flags any row that starts a new run — first season for the player, or a change in either `scoring_class` or `is_active`.
- A cumulative `SUM` of that 0/1 flag over the same window produces a stable `streak_id` that increments only at transitions, so all rows in the same run share one id.
- Grouping by `(player_name, streak_id, scoring_class, is_active)` collapses each run to one row, with `MIN/MAX(season)` becoming the run's bounds.
- `MAX(season) OVER (PARTITION BY player_name)` is included in the grouping (it is constant within a player) so it survives the aggregation and lands on every row as `current_season`.
