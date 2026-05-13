Use `UNION ALL` to combine both tables — `UNION ALL` keeps all rows including duplicates (which is correct here since each order is unique).

In DataFrame API: `.union()` or `.unionByName()` — prefer `unionByName` when column order might differ.
