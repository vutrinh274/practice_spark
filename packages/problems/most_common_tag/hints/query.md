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
