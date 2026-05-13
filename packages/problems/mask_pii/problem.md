Given a table `customers` with columns `customer_id`, `name`, `email`, and `phone`, mask the PII fields as follows:

- `masked_email`: keep the first 3 characters of the local part, replace the rest with `***`, and keep the `@domain` part intact. Example: `alice@gmail.com` → `ali***@gmail.com`
- `masked_phone`: replace all but the last 4 digits with `*`. Example: `5551234567` → `******4567`

Return columns: `customer_id`, `name`, `masked_email`, `masked_phone`

Order by `customer_id` ascending.
