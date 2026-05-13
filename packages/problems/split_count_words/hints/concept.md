To count word frequencies you need to first "explode" each review into individual words, then aggregate by word.

Key functions:
- `SPLIT(str, delimiter)` — splits a string into an array of strings
- `EXPLODE(array)` — turns each array element into a separate row
- `LOWER(str)` — converts string to lowercase
- `LENGTH(str)` — number of characters in a string
- `GROUP BY` + `COUNT(*)` — count occurrences of each word
