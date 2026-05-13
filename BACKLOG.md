# Backlog

## Infrastructure

### Object Storage (Cloudflare R2) — Future Scaling Only
- **Current architecture:** SQLite + Docker volumes on a single machine. No object storage needed.
- **When to revisit:** moving Spark to a separate machine, multiple API instances, or SQLite becomes a bottleneck (thousands of concurrent users)
- **If/when migrating:** R2 over GCS for free egress. Spark reads via `s3a://`. Per-user prefix not needed — SQLite user_id column is sufficient for data isolation on single machine.

### Infra Scaling Principle
- Spark Connect runs as a single Docker container on one machine (`local[*]` mode)
- Scale vertically (bigger VM) when traffic spikes — `local[*]` uses all available cores automatically
- Fair Scheduler handles concurrent user sessions on the same machine
- Horizontal scaling is a future concern — not needed until a single large VM is insufficient

## Features

### Problem List Page
- `/problems` route listing all problems with title, difficulty, tags, solved status
- Requires user identity (auth) to track solved status

### Submission History
- Per-problem submission history: timestamp, mode (SQL/DataFrame), pass/fail
- Requires database to persist submissions

### User Accounts & Auth
- Login/signup before any public release
- Submission history and progress tied to user identity
- Subscription gating for premium problems

### Spark-Specific Editor Autocomplete
- DataFrame API mode: Spark-specific method completions (`.groupBy()`, `.withColumn()`, etc.)
- Currently deferred — SQL mode has keyword + schema completions

### Result Feedback UX
- Row-level diff display (expected vs actual rows side by side)
- Cancel button mid-execution

### Problem UX
- Show reference solution after solving
- Progress tracking (solved/attempted/failed per user)
- Problem list with difficulty and topic filters

### Problem Versioning
- Lock problems on rollout — once live, fixture + expected output is immutable
- Version field in problem.yaml for future reference

## Auth & User System

### Auth Implementation (Clerk + SQLite)
- Clerk for sign-up/sign-in (email + password only for now, no social login)
- SQLite + SQLAlchemy for submissions and progress
- FastAPI middleware to validate Clerk JWT, inject user_id
- Per-user Spark sessions (keyed by user_id, evict after 30min inactivity)
- Phase-separated timeouts: session creation 15s, job execution 45s

### Access Control Model
- Anonymous: can see problems 1-10, description + fixture visible, Run shows "Sign in to submit"
- Logged in (free): can submit problems 1-10
- Subscriber: full access to all problems
- Problems 11+ blurred on list for anonymous/free users (Option A — blur row)

### Subscriber Management
- subscribers table: (email, subscribed_at, notes)
- Admin endpoints protected by secret key (env var):
  - POST /admin/subscribers — add single subscriber
  - POST /admin/subscribers/bulk — upload CSV
  - DELETE /admin/subscribers/{email} — remove subscriber
- Check email against subscribers table on login
- Decoupled from payment — managed manually, automate with Stripe later

### Journey Mode (requires auth)
- Two modes: Explore (open) and Journey (structured, must pass first attempt to unlock next)
- Journey mode is the subscription product
- Explore mode works without auth (localStorage)

## Missing Curriculum Problems (implement and validate)
- #40 Cohort Retention — months_between + window
- #46 Parse JSON Column — from_json + schema inference
- #47 Flatten Nested Structs — getField, struct operations
- #58 ETL Job Statistics — window on execution metadata
- #59 Products with Increasing YoY Sales — multi-year LAG + filter
- #63 Slowly Changing Dimension — SCD Type 2 pattern

## Editor
- Cmd+Enter keyboard shortcut to run (with rate limiting)
- Parameter hints/signature help for Spark DataFrame methods

## Rate Limiting
- Per-user + per-problem on /submit after auth
- Never apply to syntax check endpoints (/validate/python)

## Security

### Full Endpoint Authentication (Future)
- Gate all non-public endpoints behind Clerk JWT
- Current state: hints, solutions, preview endpoints are public
- Future: require valid Clerk token for any action (submit, hints, solutions, validate)
- This means all users must be signed in to take any action
- Implementation: add `require_auth` dependency to all non-public endpoints
- Public endpoints to remain open: `GET /problems`, `GET /problems/:id` (description only)
- Impacts: frontend must pass token on all API calls
