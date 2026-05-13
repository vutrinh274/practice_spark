Apply both `RANK()` and `DENSE_RANK()` over the same window: `ORDER BY score DESC`. Since there is no partitioning here (all students are in one group), the window spec has only an ORDER BY clause.
