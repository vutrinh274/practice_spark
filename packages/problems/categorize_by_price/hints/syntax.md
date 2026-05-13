Use `CASE WHEN ... THEN ... ELSE ... END` in SQL, or `F.when(...).when(...).otherwise(...)` in DataFrame API.

```sql
CASE
  WHEN price < 50 THEN 'Budget'
  WHEN price < 500 THEN 'Mid-range'
  ELSE 'Premium'
END AS price_tier
```
