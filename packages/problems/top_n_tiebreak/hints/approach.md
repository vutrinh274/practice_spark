# Approach

## Step-by-Step Plan

1. **Define the window**: partition by `department`, order by `salary DESC, employee_id ASC`.
2. **Apply `ROW_NUMBER()`** over the window → `row_num`.
3. **Filter** to `row_num <= 2`.
4. **Select** `department, employee_id, name, salary, row_num`.
5. **Order** by `department ASC, row_num ASC`.

## Pseudocode

```
w = PARTITION BY department ORDER BY salary DESC, employee_id ASC

df = employees
    .withColumn("row_num", ROW_NUMBER().over(w))
    .filter(row_num <= 2)
    .select(department, employee_id, name, salary, row_num)
    .orderBy(department, row_num)
```

## Common Mistakes

- Using `RANK` or `DENSE_RANK` — these can return more than 2 rows per department when there are ties.
- Forgetting `employee_id` in the `ORDER BY` — without it, results are non-deterministic for tied salaries.
