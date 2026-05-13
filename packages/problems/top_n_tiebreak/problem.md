# Top N with Tie-Breaking

**Difficulty:** Medium
**Tags:** window functions, row_number, tie-breaking

## Background

HR wants the top 2 earners from each department for the annual bonus review. When two employees earn the same salary, the one with the lower `employee_id` gets the higher rank (seniority tie-break).

## Schema

**employees** (`fixture.csv`)

| Column | Type | Description |
|---|---|---|
| employee_id | INT | Unique employee identifier |
| name | STRING | Employee name |
| department | STRING | Department |
| salary | INT | Annual salary in USD |

## Task

Get the **top 2 earners per department**, breaking ties by `employee_id ASC`. Use `ROW_NUMBER` (not `RANK`) so exactly 2 rows are returned per department regardless of ties.

Return: **department, employee_id, name, salary, row_num**
Order by: **department ASC, row_num ASC**

## Expected Output

| department | employee_id | name | salary | row_num |
|---|---|---|---|---|
| Engineering | 1 | Alice | 95000 | 1 |
| Engineering | 3 | Carol | 95000 | 2 |
| Finance | 9 | Iris | 110000 | 1 |
| Finance | 10 | Jack | 98000 | 2 |
| Marketing | 5 | Eve | 70000 | 1 |
| Marketing | 6 | Frank | 70000 | 2 |

## Notes

- Engineering: Alice (id=1, 95k) and Carol (id=3, 95k) are tied — Alice wins on lower id.
- Finance: Iris (110k) first, then Jack (id=10, 98k) before Karen (id=11, 98k).
- Marketing: Eve (id=5, 70k) and Frank (id=6, 70k) both at 70k — Eve wins.
