Phone numbers often arrive in inconsistent formats. Standardizing them requires:
1. Stripping non-digit characters to isolate the raw digits.
2. Reassembling the digits into the target format using string slicing.

Key functions:
- `REGEXP_REPLACE(str, pattern, replacement)` — replace all matches of a regex
- `SUBSTRING(str, pos, len)` — extract a substring (1-indexed)
- `CONCAT(...)` — join multiple strings
