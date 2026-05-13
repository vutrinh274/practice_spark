```sql
SELECT word, COUNT(*) AS count
FROM (
  SELECT LOWER(EXPLODE(SPLIT(review_text, ' '))) AS word
  FROM reviews
)
WHERE LENGTH(word) >= 3
  AND word NOT IN ('the', 'and', 'for', 'this', 'was', 'very', 'are', 'with', 'that')
GROUP BY word
ORDER BY count DESC, word ASC
LIMIT 5
```
