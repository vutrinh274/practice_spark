**masked_email:**
1. Take the first 3 characters of the email with `SUBSTRING(email, 1, 3)`.
2. Append the literal `***@`.
3. Extract the domain using `REGEXP_EXTRACT(email, '@(.+)$', 1)`.
4. Concatenate the three parts.

**masked_phone (format: `XXX-XXX-XXXX`):**
1. The last 4 characters of the phone string are the final 4 digits.
2. Use `CONCAT('***-***-', SUBSTRING(phone, LENGTH(phone) - 3, 4))`.
