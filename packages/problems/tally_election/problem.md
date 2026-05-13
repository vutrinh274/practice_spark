# Tally Election Results

**Difficulty:** Hard
**Tags:** aggregation, ranking, dense_rank

## Background

Three candidates (Alice, Bob, Charlie) contested an election across three districts (North, South, East). Each row in the votes table represents one ballot cast. Determine the winner in each district.

## Schema

**votes** (`fixture.csv`)

| Column | Type | Description |
|---|---|---|
| vote_id | INT | Unique ballot identifier |
| voter_id | INT | Unique voter identifier |
| candidate | STRING | Candidate name |
| district | STRING | District where the vote was cast |

## Task

Find the **winning candidate** (most votes) in each district. Return one row per district.

Return: **district, candidate, votes**
Order by: **district ASC**

## Expected Output

| district | candidate | votes |
|---|---|---|
| East | Charlie | 3 |
| North | Alice | 3 |
| South | Bob | 4 |

## Notes

- North: Alice 3, Bob 2, Charlie 1 → Alice wins
- South: Bob 4, Charlie 2, Alice 1 → Bob wins
- East: Charlie 3, Alice 2, Bob 2 → Charlie wins
