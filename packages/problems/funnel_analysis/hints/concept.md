# Concept: Funnel Analysis

A funnel measures the count of distinct users who performed each action at least once, regardless of order or repetition. The key insight is:

- **Per-stage aggregation**: for each stage, count `DISTINCT user_id` where that event type appears. No need for ordering within user events for this simpler form of funnel.
- **Stage metadata**: you need to attach the human-readable stage name and its order number — use a lookup table (inline values or a CASE expression).

## Two Common Approaches

### 1. Pivot / CASE aggregation
Compute all four counts in one pass using conditional aggregation:
```sql
COUNT(DISTINCT CASE WHEN event_type = 'view' THEN user_id END) AS view_users
```
Then `UNPIVOT` (or union) to return one row per stage.

### 2. GROUP BY + JOIN to stage map
```sql
SELECT event_type, COUNT(DISTINCT user_id)
FROM user_events
GROUP BY event_type
-- then join to a stage mapping table for stage_order
```

Approach 2 is simpler and easier to extend.
