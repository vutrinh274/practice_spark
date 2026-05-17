import os
import asyncio
import requests
from datetime import datetime
from sqlalchemy.orm import Session
from database import engine, StripeSubscriber

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
SYNC_INTERVAL_MINUTES = int(os.getenv("STRIPE_SYNC_INTERVAL_MINUTES", "5"))


def _stripe_get(path: str, params: dict = None) -> dict:
    resp = requests.get(
        f"https://api.stripe.com/v1/{path}",
        auth=(STRIPE_SECRET_KEY, ""),
        params=params or {},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()


def _paginate(path: str, params: dict = None) -> list:
    results = []
    params = {**(params or {}), "limit": 100}
    while True:
        data = _stripe_get(path, params)
        results.extend(data["data"])
        if not data.get("has_more"):
            break
        params["starting_after"] = data["data"][-1]["id"]
    return results


def sync_subscribers():
    """
    Sync paid Stripe subscribers to stripe_subscribers table only.
    Never touches manual_subscribers.
    """
    if not STRIPE_SECRET_KEY:
        print("[stripe_sync] STRIPE_SECRET_KEY not set — skipping sync")
        return

    print("[stripe_sync] Starting subscriber sync...")

    # Fetch all customers → {customer_id: email}
    customers = _paginate("customers")
    customer_email_map = {c["id"]: c["email"] for c in customers if c.get("email")}
    print(f"[stripe_sync] Found {len(customer_email_map)} customers")

    # Fetch all active subscriptions → set of paying customer IDs
    active_subs = _paginate("subscriptions", {"status": "active"})
    paying_customer_ids = {sub["customer"] for sub in active_subs}
    print(f"[stripe_sync] Found {len(paying_customer_ids)} active subscriptions")

    # Cross-reference locally
    paid_emails = {
        customer_email_map[cid]
        for cid in paying_customer_ids
        if cid in customer_email_map
    }
    print(f"[stripe_sync] {len(paid_emails)} paid subscribers")

    # Atomic upsert into stripe_subscribers only
    with Session(engine) as session:
        existing = {s.email for s in session.query(StripeSubscriber.email).all()}

        # Add new
        for email in paid_emails - existing:
            session.add(StripeSubscriber(email=email, synced_at=datetime.utcnow()))

        # Remove cancelled (only from stripe table)
        to_remove = existing - paid_emails
        if to_remove:
            session.query(StripeSubscriber).filter(
                StripeSubscriber.email.in_(to_remove)
            ).delete(synchronize_session=False)

        # Update sync timestamp for existing
        session.query(StripeSubscriber).filter(
            StripeSubscriber.email.in_(paid_emails & existing)
        ).update({"synced_at": datetime.utcnow()}, synchronize_session=False)

        session.commit()

    print(f"[stripe_sync] Sync complete — {len(paid_emails)} stripe subscribers")


def has_active_stripe_subscription(email: str) -> bool:
    """Live Stripe API check — bypasses local cache. Used as fallback in is_subscriber."""
    if not STRIPE_SECRET_KEY:
        return False
    try:
        customers = _stripe_get("customers", {"email": email, "limit": 1})
        if not customers["data"]:
            return False
        customer_id = customers["data"][0]["id"]
        subs = _stripe_get("subscriptions", {"customer": customer_id, "status": "active", "limit": 1})
        return len(subs["data"]) > 0
    except Exception as e:
        print(f"[stripe_sync] Live check failed for {email}: {e}")
        return False


async def start_sync_loop():
    loop = asyncio.get_event_loop()
    while True:
        try:
            await loop.run_in_executor(None, sync_subscribers)
        except Exception as e:
            print(f"[stripe_sync] Sync failed: {e}")
        await asyncio.sleep(SYNC_INTERVAL_MINUTES * 60)
