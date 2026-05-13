In Spark SQL use `PIVOT` inside a subquery. In the DataFrame API use `.groupBy(...).pivot(...).agg(...)`.

SQL pattern:
```sql
SELECT * FROM (SELECT employee_id, status FROM attendance)
PIVOT (COUNT(*) FOR status IN ('Present', 'Absent', 'Late'))
```

DataFrame pattern:
```python
df.groupBy("employee_id").pivot("status", ["Present", "Absent", "Late"]).count()
```
