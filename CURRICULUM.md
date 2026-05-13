# spark.practice — Problem Curriculum (64 Problems)

## Status Legend
- ✅ Implemented
- 🔲 Pending

---

## Track 1: Foundations (10 problems, Easy)

| # | Status | Problem | Key Concept |
|---|---|---|---|
| 1 | ✅ | Group By Basics | GROUP BY + SUM |
| 2 | ✅ | Find Duplicate Emails | GROUP BY + HAVING |
| 3 | 🔲 | Handling NULLs | COALESCE, dropna, fillna |
| 4 | 🔲 | Filter and Count | WHERE + COUNT DISTINCT |
| 5 | 🔲 | Categorize by Price | CASE WHEN / F.when() |
| 6 | 🔲 | Combine Two Tables | UNION ALL / unionByName |
| 7 | 🔲 | Column Arithmetic | Derived columns, casting |
| 8 | 🔲 | Top N Overall | ORDER BY + LIMIT |
| 9 | 🔲 | String Basics | CONCAT, UPPER, LOWER, TRIM |
| 10 | 🔲 | Daily Sales Total | Date grouping, DATE_FORMAT |

---

## Track 2: Joins (8 problems, Easy → Medium)

| # | Status | Problem | Key Concept |
|---|---|---|---|
| 11 | ✅ | Multi-Table Join | 3-way JOIN + aggregation |
| 12 | 🔲 | Simple Inner Join | JOIN basics |
| 13 | 🔲 | Customers with No Orders | Anti-join (LEFT JOIN + IS NULL) |
| 14 | 🔲 | Self Join — Find Manager | Self-join pattern |
| 15 | 🔲 | Full Outer Join | FULL OUTER JOIN + NULL handling |
| 16 | 🔲 | Customers Who Bought Both | INTERSECT / double join |
| 17 | 🔲 | Unsold Products | Anti-join, NOT EXISTS |
| 18 | 🔲 | Most Popular Product per Category | JOIN + RANK |

---

## Track 3: Aggregation Deep Dive (8 problems, Medium)

| # | Status | Problem | Key Concept |
|---|---|---|---|
| 19 | 🔲 | Monthly Revenue Summary | DATE_TRUNC + GROUP BY |
| 20 | 🔲 | Revenue Share per Category | Percentage over total |
| 21 | 🔲 | Conditional Aggregation | SUM(CASE WHEN ...) |
| 22 | 🔲 | Count Distinct per Day | COUNT DISTINCT |
| 23 | 🔲 | First and Last Event per User | MIN/MAX per group |
| 24 | 🔲 | Pivot Attendance by Status | PIVOT / crosstab |
| 25 | 🔲 | Customers Above Average Spend | HAVING + subquery |
| 26 | 🔲 | Remove Statistical Outliers | IQR filtering, percentile_approx |

---

## Track 4: Window Functions (10 problems, Medium → Hard)

| # | Status | Problem | Key Concept |
|---|---|---|---|
| 27 | ✅ | Top N per Group | RANK() OVER PARTITION BY |
| 28 | ✅ | Running Total | SUM() cumulative window |
| 29 | 🔲 | Stock Price Daily Change | LAG() |
| 30 | 🔲 | Next Purchase Date | LEAD() |
| 31 | 🔲 | 7-Day Rolling Average | ROWS BETWEEN frame |
| 32 | 🔲 | Employee Salary vs Dept Average | AVG() OVER PARTITION BY |
| 33 | 🔲 | Percentile Rank of Sales | PERCENT_RANK / NTILE |
| 34 | 🔲 | Dense Rank vs Rank | DENSE_RANK vs RANK distinction |
| 35 | 🔲 | Year-over-Year Growth | LAG by year partition |
| 36 | 🔲 | Top Customers by Region | Nested PARTITION BY |

---

## Track 5: Date & Time (6 problems, Medium)

| # | Status | Problem | Key Concept |
|---|---|---|---|
| 37 | 🔲 | Monthly Active Users | DATE_TRUNC + COUNT DISTINCT |
| 38 | 🔲 | Weekend vs Weekday Sales | DAYOFWEEK + CASE WHEN |
| 39 | 🔲 | Days Between Events | DATEDIFF, date arithmetic |
| 40 | 🔲 | Cohort Retention | months_between + window |
| 41 | 🔲 | Active Subscriptions on Date | Date range overlap |
| 42 | 🔲 | Late Deliveries | Date comparison + SLA |

---

## Track 6: Arrays & Structs — Spark Specific (8 problems, Medium → Hard)

| # | Status | Problem | Key Concept |
|---|---|---|---|
| 43 | 🔲 | Aggregate Tags into List | COLLECT_LIST |
| 44 | 🔲 | Explode Product Tags | EXPLODE — array to rows |
| 45 | 🔲 | Count Tags per Product | EXPLODE + GROUP BY |
| 46 | 🔲 | Parse JSON Column | from_json + schema |
| 47 | 🔲 | Flatten Nested Structs | getField, struct operations |
| 48 | 🔲 | Filter by Array Contents | array_contains() |
| 49 | 🔲 | Most Common Tag per Category | EXPLODE + RANK |
| 50 | 🔲 | Merge Arrays Across Rows | collect_list + flatten |

---

## Track 7: String & Regex (4 problems, Medium)

| # | Status | Problem | Key Concept |
|---|---|---|---|
| 51 | 🔲 | Extract Email Domain | regexp_extract |
| 52 | 🔲 | Mask PII Data | regexp_replace |
| 53 | 🔲 | Split and Count Words | split + explode + count |
| 54 | 🔲 | Standardize Phone Numbers | regexp_replace + format |

---

## Track 8: Advanced Patterns (10 problems, Hard)

| # | Status | Problem | Key Concept |
|---|---|---|---|
| 55 | 🔲 | Sessionize Clickstream | Session windows, LAG + cumsum |
| 56 | 🔲 | Consecutive Attendance Streaks | Islands & gaps problem |
| 57 | 🔲 | Funnel Analysis | Ordered event sequences |
| 58 | 🔲 | ETL Job Statistics | Window on execution metadata |
| 59 | 🔲 | Products with Increasing YoY Sales | Multi-year LAG + filter |
| 60 | 🔲 | Customer Loyalty Score | Multi-step composite scoring |
| 61 | 🔲 | Tallying Election Results | Seat allocation via ranking |
| 62 | 🔲 | Ledger Reconciliation | Full outer join + variance |
| 63 | 🔲 | Slowly Changing Dimension | SCD Type 2 pattern |
| 64 | 🔲 | Top N with Tie-Breaking | RANK vs ROW_NUMBER in depth |

---

## Currently Implemented (5/64)
- Track 1: #1 Group By Basics, #2 Find Duplicate Emails
- Track 2: #11 Multi-Table Join
- Track 4: #27 Top N per Group, #28 Running Total

## Notes
- Sources: SparkPlayground, TPC-H benchmark, Apache Spark docs, LeetCode SQL (concept inspiration only)
- Each problem has SQL mode + DataFrame API mode
- All problems authored in-house — original datasets, descriptions, hints, solutions
