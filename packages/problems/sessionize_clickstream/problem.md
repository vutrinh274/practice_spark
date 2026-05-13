# Sessionize Clickstream Data

**Difficulty:** Hard
**Tags:** window functions, session, lag

## Background

A clickstream captures every page visit a user makes on a website. For analytics purposes, visits are grouped into *sessions* — contiguous bursts of activity. A new session begins whenever a user is idle for more than 30 minutes.

## Schema

**clickstream** (`fixture.csv`)

| Column | Type | Description |
|---|---|---|
| event_id | INT | Unique event identifier |
| user_id | INT | User who triggered the event |
| page | STRING | Page visited |
| event_time | STRING | Timestamp of the event (YYYY-MM-DD HH:MM:SS) |

## Task

Assign a `session_id` to each event. A new session starts when the gap between consecutive events for the same user exceeds **30 minutes** (1800 seconds). Session IDs are sequential integers starting at 1 per user.

Return: **event_id, user_id, page, event_time, session_id**
Order by: **user_id ASC, event_time ASC**

## Expected Output (first few rows)

| event_id | user_id | page | event_time | session_id |
|---|---|---|---|---|
| 1 | 1 | home | 2024-01-01 10:00:00 | 1 |
| 2 | 1 | products | 2024-01-01 10:10:00 | 1 |
| 3 | 1 | product_detail | 2024-01-01 10:20:00 | 1 |
| 4 | 1 | cart | 2024-01-01 11:05:00 | 2 |
| 5 | 1 | checkout | 2024-01-01 11:15:00 | 2 |
| ... | ... | ... | ... | ... |
