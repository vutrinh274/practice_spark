# Concept: Ranking Aggregated Groups

Finding the winner per group is a two-step pattern:

1. **Aggregate** to get the count per group (here: votes per district–candidate pair).
2. **Rank within groups** to find the top entry per group and filter to rank = 1.

## Why Not Just MAX?

A plain `MAX(count) GROUP BY district` gives you the vote total for the winner but loses the candidate name. Ranking preserves the full row so you can return both.

## RANK vs DENSE_RANK vs ROW_NUMBER

| Function | Ties |
|---|---|
| `RANK` | Tied rows get same rank; next rank skips |
| `DENSE_RANK` | Tied rows get same rank; next rank does not skip |
| `ROW_NUMBER` | Tied rows get arbitrary distinct ranks |

For this problem `RANK` and `DENSE_RANK` both work when there are no ties. If there were ties and you wanted to surface all co-winners, use `RANK` or `DENSE_RANK` and filter `rank = 1` — multiple rows would pass the filter.
