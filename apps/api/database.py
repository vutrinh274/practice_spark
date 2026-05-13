import os
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, Boolean, DateTime, Text, or_
from sqlalchemy.orm import DeclarativeBase, Session

DB_PATH = os.getenv("DB_PATH", "spark_practice.db")
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})


class Base(DeclarativeBase):
    pass


class StripeSubscriber(Base):
    """Synced automatically from Stripe — managed by stripe_sync.py."""
    __tablename__ = "stripe_subscribers"
    email = Column(String, primary_key=True, index=True)
    synced_at = Column(DateTime, default=datetime.utcnow)


class ManualSubscriber(Base):
    """Manually added via admin endpoints — never touched by Stripe sync."""
    __tablename__ = "manual_subscribers"
    email = Column(String, primary_key=True, index=True)
    added_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(String, nullable=True)


class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, index=True, nullable=False)
    problem_id = Column(String, index=True, nullable=False)
    mode = Column(String, nullable=False)
    code = Column(Text, nullable=False)
    passed = Column(Boolean, nullable=False)
    feedback = Column(Text, nullable=True)
    submitted_at = Column(DateTime, default=datetime.utcnow)


class Progress(Base):
    __tablename__ = "progress"
    user_id = Column(String, primary_key=True)
    problem_id = Column(String, primary_key=True)
    solved = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)
    last_submitted_at = Column(DateTime, nullable=True)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    with Session(engine) as session:
        yield session


def is_subscriber(email: str) -> bool:
    """Check both Stripe and manual subscriber tables."""
    if not email:
        return False
    with Session(engine) as session:
        in_stripe = session.get(StripeSubscriber, email) is not None
        in_manual = session.get(ManualSubscriber, email) is not None
        return in_stripe or in_manual


def list_all_subscribers() -> list[dict]:
    """Return merged list from both tables."""
    with Session(engine) as session:
        stripe_subs = [
            {"email": s.email, "source": "stripe", "since": s.synced_at.isoformat(), "notes": ""}
            for s in session.query(StripeSubscriber).all()
        ]
        manual_subs = [
            {"email": s.email, "source": "manual", "since": s.added_at.isoformat(), "notes": s.notes or ""}
            for s in session.query(ManualSubscriber).all()
        ]
        # Merge, deduplicate by email (manual takes precedence for metadata)
        merged = {s["email"]: s for s in stripe_subs}
        for s in manual_subs:
            merged[s["email"]] = s
        return list(merged.values())


def save_submission(user_id: str, problem_id: str, mode: str, code: str, passed: bool, feedback: str):
    with Session(engine) as session:
        sub = Submission(
            user_id=user_id,
            problem_id=problem_id,
            mode=mode,
            code=code,
            passed=passed,
            feedback=feedback or "",
        )
        session.add(sub)

        prog = session.get(Progress, (user_id, problem_id))
        if prog is None:
            prog = Progress(user_id=user_id, problem_id=problem_id, attempts=0, solved=False)
            session.add(prog)
        prog.attempts += 1
        prog.last_submitted_at = datetime.utcnow()
        if passed:
            prog.solved = True

        session.commit()


def get_user_progress(user_id: str) -> list[dict]:
    with Session(engine) as session:
        rows = session.query(Progress).filter(Progress.user_id == user_id).all()
        return [
            {
                "problem_id": r.problem_id,
                "solved": r.solved,
                "attempts": r.attempts,
                "last_submitted_at": r.last_submitted_at.isoformat() if r.last_submitted_at else None,
            }
            for r in rows
        ]


def get_problem_submissions(user_id: str, problem_id: str) -> list[dict]:
    with Session(engine) as session:
        rows = (
            session.query(Submission)
            .filter(Submission.user_id == user_id, Submission.problem_id == problem_id)
            .order_by(Submission.submitted_at.desc())
            .limit(20)
            .all()
        )
        return [
            {
                "id": r.id,
                "mode": r.mode,
                "passed": r.passed,
                "feedback": r.feedback,
                "submitted_at": r.submitted_at.isoformat(),
            }
            for r in rows
        ]
