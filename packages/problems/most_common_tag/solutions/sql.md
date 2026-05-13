## SQL Solution

```sql
SELECT category, tag, tag_count
FROM (
  SELECT category, tag, COUNT(*) AS tag_count,
         RANK() OVER (PARTITION BY category ORDER BY COUNT(*) DESC) AS rnk
  FROM (
    SELECT category, EXPLODE(SPLIT(tags, ',')) AS tag
    FROM articles
  )
  GROUP BY category, tag
)
WHERE rnk = 1
ORDER BY category
```

**Why it works:**
- The innermost subquery explodes the comma-separated `tags` string into individual rows per category.
- The middle layer counts occurrences of each tag within each category.
- `RANK() OVER (PARTITION BY category ORDER BY COUNT(*) DESC)` ranks tags from most to least frequent within each category; ties both receive rank 1.
- The outer filter `WHERE rnk = 1` keeps only the top tag(s) per category.
