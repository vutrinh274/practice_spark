Given a table `scores` with columns `student_id`, `name`, `subject`, and `score`, compute both `RANK()` and `DENSE_RANK()` for each student ordered by `score` descending.

Return columns: `student_id`, `name`, `score`, `rank`, `dense_rank`

Order by `score` descending, then `student_id` ascending.

**Key learning:** When scores are tied, `RANK()` skips subsequent rank numbers (e.g., two students at rank 1 means the next rank is 3), while `DENSE_RANK()` assigns the next consecutive number (rank 2).
