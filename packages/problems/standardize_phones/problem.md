Given a table `contacts` with columns `contact_id`, `name`, and `phone`, standardize all phone numbers to the format `XXX-XXX-XXXX`.

Phone numbers may appear in any of these formats:
- `(555) 123-4567`
- `555-123-4567`
- `5551234567`
- `555.123.4567`

All source phones contain exactly 10 digits.

Steps:
1. Strip all non-digit characters to get a 10-digit string.
2. Format as `XXX-XXX-XXXX` using the first 3, next 3, and last 4 digits.

Return columns: `contact_id`, `name`, `original_phone`, `standardized_phone`

Order by `contact_id` ascending.
