# Concept: Islands and Gaps

The **islands and gaps** pattern identifies contiguous groups ("islands") of rows that satisfy a condition, separated by gaps that do not.

## The Classic Trick

For a set of consecutive dates, if you subtract a sequential row number from each date, the result is the **same constant date** for all rows within the same island.

```
date        rn    date - rn (days)
2024-01-03   1    2024-01-02        ← island A
2024-01-04   2    2024-01-02        ← island A
2024-01-05   3    2024-01-02        ← island A (streak = 3)
-- gap --
2024-01-07   4    2024-01-03        ← island B
2024-01-08   5    2024-01-03        ← island B (streak = 2)
```

Any break in consecutive dates shifts the subtracted value, creating a new group key. You can then `COUNT(*)` per group to get streak length, and `MAX` across groups per employee.

## Why it Works

`ROW_NUMBER()` increments by 1 for each row. Consecutive dates also increment by 1 day. So `date - rn` cancels out both increments, leaving a stable anchor.
