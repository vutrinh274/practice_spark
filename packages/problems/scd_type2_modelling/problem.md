Given a table `players` with one snapshot row per player per season — columns `player_name`, `scoring_class`, `is_active`, `season` — model it as a **Slowly Changing Dimension Type 2** table.

For each player, collapse consecutive seasons where both `scoring_class` and `is_active` stayed the same into a single row, and emit:

- `start_season` — first season in the run
- `end_season` — last season in the run
- `current_season` — the most recent season observed for that player (i.e. `MAX(season)` per player)

A new row should start whenever `scoring_class` changes, `is_active` changes, or it is the player's first season.

Return columns in this order: `player_name`, `scoring_class`, `is_active`, `current_season`, `start_season`, `end_season`.

Order the result by `player_name` ascending, then `start_season` ascending.
