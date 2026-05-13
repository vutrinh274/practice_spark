## SQL Solution

```sql
SELECT customer_id, SUM(amount) AS total_amount
FROM data
GROUP BY customer_id
```

**Why it works:**
- `GROUP BY customer_id` collapses all rows with the same `customer_id` into one group
- `SUM(amount)` computes the total amount within each group
- The alias `total_amount` gives the result column a clean name
