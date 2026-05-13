Use `LEFT JOIN` products to sales, then filter where `sale_id IS NULL`. Or use `NOT IN` / `NOT EXISTS` subquery approach.

In DataFrame API, Spark's `left_anti` join is the most elegant solution.
