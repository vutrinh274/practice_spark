1. Use `LOWER(review_text)` to normalize case.
2. Use `SPLIT(text, ' ')` to split each review into an array of words.
3. Use `EXPLODE(...)` to turn each word into its own row.
4. Filter out words shorter than 3 characters with `LENGTH(word) >= 3`.
5. Filter out stop words with `word NOT IN ('the', 'and', ...)`.
6. `GROUP BY word` and `COUNT(*)` to get frequencies.
7. Order by `count DESC`, then `word ASC`, and `LIMIT 5`.
