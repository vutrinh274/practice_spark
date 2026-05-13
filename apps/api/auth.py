import os
from dotenv import load_dotenv
load_dotenv()
import httpx
import jwt
from jwt.algorithms import RSAAlgorithm
from functools import lru_cache
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

def _clerk_secret() -> str:
    return os.getenv("CLERK_SECRET_KEY", "")
_bearer = HTTPBearer(auto_error=False)


@lru_cache(maxsize=1)
def _get_jwks() -> dict:
    """Fetch Clerk's public JWKS for JWT verification."""
    # Extract the JWT issuer from the publishable key
    # pk_test_BASE64 → decode → issuer URL
    import base64
    pub_key = os.getenv("NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY", "")
    if not pub_key:
        return {}
    try:
        # The publishable key encodes the frontend API URL
        payload = pub_key.split("_")[2]
        # Add padding
        payload += "=" * (4 - len(payload) % 4)
        decoded = base64.b64decode(payload).decode()
        issuer = f"https://{decoded.rstrip('$')}"
        resp = httpx.get(f"{issuer}/.well-known/jwks.json", timeout=5)
        return resp.json()
    except Exception:
        return {}


def verify_token(token: str) -> dict:
    """Verify a Clerk JWT and return the payload."""
    try:
        jwks = _get_jwks()
        if not jwks:
            raise HTTPException(status_code=401, detail="Auth service unavailable")

        header = jwt.get_unverified_header(token)
        kid = header.get("kid")

        key = None
        for k in jwks.get("keys", []):
            if k.get("kid") == kid:
                key = RSAAlgorithm.from_jwk(k)
                break

        if not key:
            raise HTTPException(status_code=401, detail="Invalid token key")

        payload = jwt.decode(token, key, algorithms=["RS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")


async def get_current_user(request: Request) -> dict | None:
    """Extract user from JWT if present. Returns None if not authenticated."""
    credentials: HTTPAuthorizationCredentials | None = await _bearer(request)
    if not credentials:
        return None
    return verify_token(credentials.credentials)


async def require_auth(request: Request) -> dict:
    """Require a valid JWT. Raises 401 if not authenticated."""
    user = await get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user


def get_user_id(user: dict) -> str:
    """Extract user_id from Clerk JWT payload."""
    return user.get("sub", "")


@lru_cache(maxsize=512)
def get_user_email(user_id: str) -> str:
    """Fetch user email from Clerk API using user_id. Cached per user_id."""
    key = _clerk_secret()
    if not key or not user_id:
        return ""
    try:
        resp = httpx.get(
            f"https://api.clerk.com/v1/users/{user_id}",
            headers={"Authorization": f"Bearer {key}"},
            timeout=5,
        )
        data = resp.json()
        emails = data.get("email_addresses", [])
        primary_id = data.get("primary_email_address_id", "")
        for e in emails:
            if e.get("id") == primary_id:
                return e.get("email_address", "")
        if emails:
            return emails[0].get("email_address", "")
        return ""
    except Exception:
        return ""
