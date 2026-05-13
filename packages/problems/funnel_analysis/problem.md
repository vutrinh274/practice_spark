# Funnel Analysis

**Difficulty:** Hard
**Tags:** window functions, ordered events, aggregation

## Background

A conversion funnel tracks how many users progress through each stage of an e-commerce journey: view a product → add to cart → checkout → purchase. Marketing wants to see where users drop off.

## Schema

**user_events** (`fixture.csv`)

| Column | Type | Description |
|---|---|---|
| event_id | INT | Unique event identifier |
| user_id | INT | User who triggered the event |
| event_type | STRING | One of: view, cart, checkout, purchase |
| event_date | STRING | Date of the event (YYYY-MM-DD) |

## Task

Count how many **distinct users** reached each funnel stage (i.e., performed at least one event of that type).

Return: **stage, stage_order, users_reached**
Order by: **stage_order ASC**

Stages and their order:

| stage | stage_order |
|---|---|
| view | 1 |
| cart | 2 |
| checkout | 3 |
| purchase | 4 |

## Expected Output

| stage | stage_order | users_reached |
|---|---|---|
| view | 1 | 6 |
| cart | 2 | 5 |
| checkout | 3 | 4 |
| purchase | 4 | 3 |
