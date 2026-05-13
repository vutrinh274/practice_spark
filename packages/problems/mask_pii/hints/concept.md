Masking PII means replacing sensitive characters with a placeholder (like `*`) while keeping enough context for identification purposes (e.g., last 4 digits of a phone).

Key functions:
- `SUBSTRING(str, pos, len)` — extract part of a string (1-indexed)
- `CONCAT(...)` — join strings together
- `REGEXP_EXTRACT(str, pattern, group)` — extract a regex capture group
- `LENGTH(str)` — length of a string
