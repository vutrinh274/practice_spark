# Concept: ROW_NUMBER for Top-N with Deterministic Tie-Breaking

## Why ROW_NUMBER, not RANK?

| Function | Behaviour on ties | Rows returned per group |
|---|---|---|
| `RANK` | Tied rows share a rank; next rank skips | May exceed N |
| `DENSE_RANK` | Tied rows share a rank; no skip | May exceed N |
| `ROW_NUMBER` | Every row gets a unique number arbitrarily within ties | Exactly N |

When you need **exactly N rows per group** regardless of ties, use `ROW_NUMBER`. To make the result **deterministic**, you must supply a fully-defined `ORDER BY` that resolves all ties — here, `salary DESC, employee_id ASC`.

## Fully-Defined ORDER BY

```sql
ROW_NUMBER() OVER (
    PARTITION BY department
    ORDER BY salary DESC, employee_id ASC
)
```

- Primary sort: `salary DESC` — highest earner first.
- Tiebreaker: `employee_id ASC` — among equal salaries, the employee hired first (lower id) gets the lower row number.

With both criteria, no two rows within a partition share the same `(salary, employee_id)` pair, so `ROW_NUMBER` is completely deterministic.
