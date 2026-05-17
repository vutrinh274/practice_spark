from dotenv import load_dotenv
load_dotenv()

import csv
import os
from typing import Literal
from fastapi import FastAPI, HTTPException, Request, Security, UploadFile
from fastapi.security import APIKeyHeader
from auth import get_current_user, get_user_id, require_auth, get_user_email
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sandbox import check_ast
from errors import friendly_error
from executor import execute_submission, validate_sql
from loader import get_problem, get_dataset_local_path, list_problems, load_registry
from database import init_db, is_subscriber, save_submission, get_user_progress, get_problem_submissions, get_github_activation, save_github_activation, GithubActivation, ManualSubscriber, StripeSubscriber, list_all_subscribers, Session, engine
from stripe_sync import start_sync_loop
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

def _get_rate_limit_key(request: Request) -> str:
    """Use user_id for authenticated users, IP for anonymous."""
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        try:
            from auth import verify_token, get_user_id
            token = auth_header.split(" ", 1)[1]
            user = verify_token(token)
            uid = get_user_id(user)
            if uid:
                return f"user:{uid}"
        except Exception:
            pass
    return f"ip:{get_remote_address(request)}"


limiter = Limiter(key_func=_get_rate_limit_key)

_CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")]

app = FastAPI(
    title="spark.practice API",
    description="Backend API for spark.practice — Spark SQL & DataFrame practice platform",
    version="1.0.0",
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

_admin_key_header = APIKeyHeader(name="X-Admin-Key", auto_error=False)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    import asyncio
    load_registry()
    init_db()
    asyncio.create_task(start_sync_loop())

    async def evict_sessions():
        from executor import _evict_idle_sessions
        while True:
            await asyncio.sleep(5 * 60)  # every 5 minutes
            _evict_idle_sessions()

    asyncio.create_task(evict_sessions())



class SubmissionRequest(BaseModel):
    problem_id: str
    mode: Literal["sql", "dataframe"]
    code: str


@app.get("/problems")
def get_problems():
    problems = list_problems()
    return [
        {
            "id": p.id,
            "title": p.title,
            "difficulty": p.difficulty,
            "tags": p.tags,
        }
        for p in problems
    ]


@app.get("/problems/{problem_id}")
def get_problem_by_id(problem_id: str):
    try:
        p = get_problem(problem_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Problem not found")
    return {
        "id": p.id,
        "title": p.title,
        "difficulty": p.difficulty,
        "tags": p.tags,
        "description": p.description,
        "schema": p.schema,
        "hint_count": len(p.hint_paths),
        "solution_modes": list(p.solution_paths.keys()),
    }


@app.get("/problems/{problem_id}/preview")
def get_problem_preview(problem_id: str):
    try:
        p = get_problem(problem_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Problem not found")

    preview = {}
    for ds in p.datasets:
        csv_path = get_dataset_local_path(p, ds.name)
        if not csv_path.exists():
            continue
        with open(csv_path) as f:
            rows = list(csv.DictReader(f))[:5]
        preview[ds.name] = rows
    return preview


@app.get("/problems/{problem_id}/hints/{index}")
def get_hint(problem_id: str, index: int):
    try:
        p = get_problem(problem_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Problem not found")
    if not p.hint_paths or index >= len(p.hint_paths):
        raise HTTPException(status_code=404, detail="Hint not found")
    return {
        "content": p.hint_paths[index].read_text(),
        "index": index,
        "total": len(p.hint_paths),
    }


@app.get("/problems/{problem_id}/solution/{mode}")
def get_solution(problem_id: str, mode: str):
    try:
        p = get_problem(problem_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Problem not found")
    if mode not in p.solution_paths:
        raise HTTPException(status_code=404, detail=f"No {mode} solution registered")
    return {
        "content": p.solution_paths[mode].read_text(),
        "available_modes": list(p.solution_paths.keys()),
    }



class ValidatePythonRequest(BaseModel):
    code: str


@app.post("/validate/python")
def validate_python(req: ValidatePythonRequest):
    import ast as pyast
    try:
        pyast.parse(req.code)
        return {"valid": True, "error": None, "line": None}
    except SyntaxError as e:
        return {"valid": False, "error": e.msg, "line": e.lineno}


class ValidateRequest(BaseModel):
    problem_id: str
    code: str


@app.post("/validate")
@limiter.limit("30/minute")
async def validate(req: ValidateRequest, request: Request):
    try:
        get_problem(req.problem_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Problem not found")
    try:
        return await validate_sql(req.problem_id, req.code)
    except TimeoutError:
        return {"valid": False, "error": "Validation timed out."}
    except Exception as e:
        return {"valid": False, "error": friendly_error(e)}


@app.post("/submit")
@limiter.limit("20/minute")
async def submit(req: SubmissionRequest, request: Request):
    user = await get_current_user(request)
    user_id = get_user_id(user) if user else None

    try:
        get_problem(req.problem_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Problem not found")

    if req.mode == "dataframe":
        error = check_ast(req.code)
        if error:
            return {"passed": False, "feedback": error}

    # Check problem access: problems 6+ require paid subscription
    FREE_LIMIT = 5
    all_problems = list_problems()
    problem_index = next((i for i, p in enumerate(all_problems) if p.id == req.problem_id), None)
    if problem_index is not None and problem_index >= FREE_LIMIT:
        user_email = get_user_email(get_user_id(user)) if user_id else ""
        if not user_email or not is_subscriber(user_email):
            return {"passed": False, "feedback": "This problem requires a paid subscription. Subscribe to my newsletter to unlock all 64 problems."}

    try:
        result = await execute_submission(req.problem_id, req.mode, req.code, user_id=user_id)
        # Save submission only for paid subscribers
        user_email = get_user_email(user_id) if user_id else ""
        if user_id and user_email and is_subscriber(user_email):
            save_submission(
                user_id=user_id,
                problem_id=req.problem_id,
                mode=req.mode,
                code=req.code,
                passed=result.get("passed", False),
                feedback=result.get("feedback", ""),
            )
        return result
    except TimeoutError:
        return {"passed": False, "feedback": "Query timed out (60s). Check for cartesian joins or infinite loops."}
    except Exception as e:
        return {"passed": False, "feedback": friendly_error(e)}


# ── Admin endpoints (protected by ADMIN_SECRET_KEY) ──────────────────────────

ADMIN_SECRET = os.getenv("ADMIN_SECRET_KEY", "")


def _check_admin(api_key: str = Security(_admin_key_header)):
    if not api_key or api_key != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Invalid admin key")


class SubscriberRequest(BaseModel):
    email: str
    notes: str = ""


@app.post("/admin/subscribers")
async def add_subscriber(req: SubscriberRequest, api_key: str = Security(_admin_key_header)):
    _check_admin(api_key)
    from datetime import datetime
    with Session(engine) as session:
        existing = session.get(ManualSubscriber, req.email)
        if existing:
            return {"status": "already exists", "email": req.email}
        sub = ManualSubscriber(email=req.email, notes=req.notes, added_at=datetime.utcnow())
        session.add(sub)
        session.commit()
    return {"status": "added", "email": req.email}


@app.post("/admin/subscribers/bulk")
async def add_subscribers_bulk(file: UploadFile, api_key: str = Security(_admin_key_header)):
    _check_admin(api_key)
    import csv as csv_module
    from io import StringIO
    from database import ManualSubscriber
    from datetime import datetime, timezone
    body = await file.read()
    reader = csv_module.DictReader(StringIO(body.decode()))
    csv_emails: set[str] = set()
    rows = []
    for row in reader:
        email = (row.get("email") or row.get("Email") or "").strip()
        if email:
            csv_emails.add(email)
            rows.append(row)

    added, removed = 0, 0
    with Session(engine) as session:
        existing = {s.email: s for s in session.query(ManualSubscriber).all()}
        existing_emails = set(existing.keys())

        to_remove = existing_emails - csv_emails
        to_add = csv_emails - existing_emails

        for email in to_remove:
            session.delete(existing[email])
            removed += 1

        csv_rows = {(row.get("email") or row.get("Email") or "").strip(): row for row in rows}
        for email in to_add:
            row = csv_rows[email]
            notes = row.get("notes") or row.get("Type") or ""
            session.add(ManualSubscriber(email=email, notes=notes, added_at=datetime.now(timezone.utc)))
            added += 1

        session.commit()
    return {"added": added, "removed": removed}


@app.delete("/admin/subscribers/{email}")
async def remove_subscriber(email: str, api_key: str = Security(_admin_key_header)):
    _check_admin(api_key)
    with Session(engine) as session:
        sub = session.get(ManualSubscriber, email)
        if not sub:
            raise HTTPException(status_code=404, detail="Subscriber not found in manual list")
        session.delete(sub)
        session.commit()
    return {"status": "removed", "email": email}


@app.get("/admin/subscribers")
async def list_subscribers(api_key: str = Security(_admin_key_header), source: str = "all"):
    _check_admin(api_key)
    if source not in ("all", "stripe", "manual"):
        raise HTTPException(status_code=400, detail="source must be 'all', 'stripe', or 'manual'")
    subs = list_all_subscribers()
    if source != "all":
        subs = [s for s in subs if s["source"] == source]
    return subs


# ── User endpoints ────────────────────────────────────────────────────────────

@app.get("/me/progress")
async def me_progress(request: Request):
    user = await require_auth(request)
    return get_user_progress(get_user_id(user))


@app.get("/me/access")
async def me_access(request: Request):
    user = await get_current_user(request)
    if not user:
        return {"authenticated": False, "subscriber": False}
    uid = get_user_id(user)
    email = get_user_email(uid)
    return {
        "authenticated": True,
        "subscriber": is_subscriber(email),
        "user_id": uid,
        "email": email,
    }


@app.get("/me/submissions/{problem_id}")
async def me_submissions(problem_id: str, request: Request):
    user = await require_auth(request)
    return get_problem_submissions(get_user_id(user), problem_id)


@app.post("/admin/github-activations/bulk")
async def bulk_github_activations(file: UploadFile, api_key: str = Security(_admin_key_header)):
    """Migrate existing activations. CSV must have headers: email,github_username"""
    _check_admin(api_key)
    import csv as csv_module
    from io import StringIO
    from datetime import datetime
    body = await file.read()
    reader = csv_module.DictReader(StringIO(body.decode()))
    added, skipped = 0, 0
    with Session(engine) as session:
        for row in reader:
            email = row.get("email", "").strip().lower()
            github_username = row.get("github_username", "").strip().lower()
            if not email or not github_username:
                continue
            if session.get(GithubActivation, email):
                skipped += 1
                continue
            session.add(GithubActivation(email=email, github_username=github_username))
            added += 1
        session.commit()
    return {"added": added, "skipped": skipped}


# ── GitHub activation ─────────────────────────────────────────────────────────

class GithubActivateRequest(BaseModel):
    email: str
    github_username: str


@app.post("/github/activate")
@limiter.limit("5/minute")
async def github_activate(req: GithubActivateRequest, request: Request):
    from github import github_user_exists, add_to_github_team

    email = req.email.strip().lower()
    username = req.github_username.strip().lower()

    if not email or not username:
        raise HTTPException(status_code=400, detail="Both email and github_username are required.")

    if not is_subscriber(email):
        raise HTTPException(status_code=403, detail="No active paid subscription found for that email.")

    if get_github_activation(email):
        raise HTTPException(status_code=409, detail="This email is already linked to a GitHub account.")

    if not await github_user_exists(username):
        raise HTTPException(status_code=400, detail=f'GitHub user "{username}" not found.')

    try:
        await add_to_github_team(username)
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e))

    save_github_activation(email, username)
    return {"status": "invited", "github_username": username}


@app.post("/admin/sync-subscribers")
async def trigger_sync(request: Request, api_key: str = Security(_admin_key_header)):
    _check_admin(api_key)
    from stripe_sync import sync_subscribers
    import asyncio
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, sync_subscribers)
    return {"status": "sync complete"}


