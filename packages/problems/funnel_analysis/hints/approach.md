# Approach

## Step-by-Step Plan

1. **Aggregate** `COUNT(DISTINCT user_id)` grouped by `event_type` from `user_events`.
2. **Map** each `event_type` to a `stage_order` integer using a CASE expression or by joining to an inline stage-mapping table.
3. **Rename** `event_type` → `stage` and select `stage, stage_order, users_reached`.
4. **Order** by `stage_order ASC`.

## Stage Mapping

```
view      → 1
cart      → 2
checkout  → 3
purchase  → 4
```

## Pseudocode

```
counts = GROUP BY event_type → COUNT(DISTINCT user_id) AS users_reached

result = counts
    .withColumn("stage", event_type)
    .withColumn("stage_order", CASE event_type WHEN 'view' THEN 1 ...)
    .select("stage", "stage_order", "users_reached")
    .orderBy("stage_order")
```
