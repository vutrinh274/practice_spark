1. Use `REGEXP_EXTRACT` with the pattern `@(.+)$` to capture the domain part of the email.
2. The capture group index is `1` — this returns everything after the `@`.
3. Alias the result as `domain` and select all required columns.
4. Order by `user_id`.
