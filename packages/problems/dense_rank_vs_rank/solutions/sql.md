## SQL Solution

```sql
SELECT student_id,
       name,
       score,
       RANK() OVER (ORDER BY score DESC) AS rank,
       DENSE_RANK() OVER (ORDER BY score DESC) AS dense_rank
FROM scores
ORDER BY score DESC, student_id
```

**Why it works:**
- No `PARTITION BY` means all students are ranked together
- `RANK()` leaves gaps after ties: if two students tie for rank 1, the next student gets rank 3
- `DENSE_RANK()` never leaves gaps: the student after the two-way tie at 1 gets rank 2
- `ORDER BY score DESC, student_id` ensures a deterministic output order for tied scores
