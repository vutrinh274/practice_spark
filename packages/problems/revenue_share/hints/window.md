Use `SUM(amount) OVER ()` — a window function with no partition — to get the grand total alongside each row's group sum:

```sql
SUM(SUM(amount)) OVER () AS grand_total
```

Or use a subquery / CTE to compute total separately.
