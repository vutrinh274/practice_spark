## SQL Solution

```sql
SELECT word, COUNT(*) AS count
FROM (
  SELECT LOWER(TRIM(word_raw)) AS word
  FROM reviews
  LATERAL VIEW EXPLODE(SPLIT(review_text, ' ')) t AS word_raw
)
WHERE LENGTH(word) >= 3
  AND word NOT IN ('the', 'and', 'for', 'this', 'was', 'very', 'are', 'with', 'that')
GROUP BY word
ORDER BY count DESC, word ASC
LIMIT 5
```

**Why it works:**
- `LATERAL VIEW EXPLODE(SPLIT(...))` is the Spark SQL way to unnest arrays
- `LOWER(TRIM(...))` normalizes the word after exploding (not nested inside EXPLODE)
- `WHERE LENGTH(word) >= 3` filters short words
- `NOT IN (...)` removes common stop words
