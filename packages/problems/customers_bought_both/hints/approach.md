Two approaches work:

1. **INTERSECT**: Find customers who bought Laptop, then INTERSECT with customers who bought Phone
2. **GROUP BY + HAVING**: Group by customer, count distinct products matching either Laptop or Phone, keep those with count = 2
