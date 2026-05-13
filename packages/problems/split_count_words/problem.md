Given a table `reviews` with columns `review_id`, `product_id`, and `review_text`, find the top 5 most common words across all reviews.

Rules:
- Convert all words to lowercase before counting.
- Exclude words shorter than 3 characters.
- Exclude these stop words: `the`, `and`, `for`, `this`, `was`, `very`, `are`, `with`, `that`.
- Words are separated by spaces.

Return columns: `word`, `count`

Order by `count` DESC, then `word` ASC. Limit to 5 rows.
