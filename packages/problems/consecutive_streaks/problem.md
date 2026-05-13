# Consecutive Attendance Streaks

**Difficulty:** Hard
**Tags:** window functions, islands and gaps

## Background

HR wants to reward employees with the longest unbroken run of attendance. Given a daily attendance log, find each employee's **longest consecutive "Present" streak**.

## Schema

**attendance** (`fixture.csv`)

| Column | Type | Description |
|---|---|---|
| employee_id | INT | Employee identifier |
| attendance_date | STRING | Date (YYYY-MM-DD) |
| status | STRING | `Present` or `Absent` |

## Task

For each employee, find their **maximum consecutive Present streak length**.

Return: **employee_id, max_streak**
Order by: **employee_id ASC**

## Expected Output

| employee_id | max_streak |
|---|---|
| 1 | 3 |
| 2 | 4 |
| 3 | 2 |

## Notes

- Employee 1: Present Jan 1–3 (streak 3), Absent Jan 4, Present Jan 5–7 (streak 3) → max = 3
- Employee 2: Present Jan 1 (streak 1), Absent Jan 2, Present Jan 3–6 (streak 4) → max = 4
- Employee 3: Present Jan 2–3 (streak 2), Present Jan 6–7 (streak 2) → max = 2
