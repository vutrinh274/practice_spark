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
