Given a table `customers` with columns `customer_id`, `first_name`, `last_name`, `email`, and `city`, clean and format the data:

- `full_name` = trimmed first name + `' '` + trimmed last name, in **Title Case**
- `email` = lowercased and trimmed
- `city` = **Title Case** (e.g. `new york` → `New York`)

Return columns: `customer_id`, `full_name`, `email`, `city`

Order by `customer_id` ascending.
