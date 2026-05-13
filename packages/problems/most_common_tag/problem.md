Given a table `articles` with columns `article_id`, `title`, `category`, and `tags` (a comma-separated string of tags), find the **most frequently used tag within each category**.

Return columns: `category`, `tag`, `tag_count`

Only return the top-ranked tag per category (rank = 1). If there is a tie for top tag within a category, return all tied tags.

Order by `category` ASC.
