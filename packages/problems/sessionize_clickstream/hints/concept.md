# Concept: Session Windows with Window Functions

A **session** is a sequence of events where no two consecutive events are separated by more than a threshold gap (here, 30 minutes).

## Key Idea: Cumulative Sum of Boundary Flags

The trick to sessionizing without a loop is:

1. **Detect boundaries** — for each event, check if the gap from the *previous* event (by the same user) exceeds the threshold. If so, this event starts a new session.
2. **Assign session IDs** — a running `SUM` of boundary flags gives each event a monotonically increasing group number. Add 1 to start at session 1.

```
event_time    prev_time    gap(min)    new_flag    cumsum    session_id
10:00         NULL         NULL        1           1         2  ← add 1
10:10         10:00        10          0           1         2
10:20         10:10        10          0           1         2
11:05         10:20        45          1           2         3
11:15         11:05        10          0           2         3
```

Wait — the first event always gets flag=1 (no previous event). After the cumulative sum + 1 the session IDs will be correct relative to each other per user, as long as you consistently treat NULL gaps as new sessions.

## Window Functions Used

- `LAG(col, 1)` — retrieve the previous row's value within the partition
- `SUM(...) OVER (... ROWS UNBOUNDED PRECEDING)` — running total
