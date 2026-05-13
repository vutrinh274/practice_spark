1. Use `REGEXP_REPLACE(phone, '[^0-9]', '')` to strip everything except digits. Store the result as `digits`.
2. All phones have exactly 10 digits, so:
   - Area code: `SUBSTRING(digits, 1, 3)`
   - Exchange: `SUBSTRING(digits, 4, 3)`
   - Number: `SUBSTRING(digits, 7, 4)`
3. `CONCAT(area, '-', exchange, '-', number)` produces `XXX-XXX-XXXX`.
4. Keep the original `phone` column aliased as `original_phone`.
