import os
import httpx

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_ORG = os.getenv("GITHUB_ORG", "")
GITHUB_TEAM_SLUG = os.getenv("GITHUB_TEAM_SLUG", "")

_HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "spark-practice-api",
}


async def github_user_exists(username: str) -> bool:
    async with httpx.AsyncClient(timeout=10) as client:
        res = await client.get(
            f"https://api.github.com/users/{username}",
            headers={**_HEADERS, "Authorization": f"Bearer {GITHUB_TOKEN}"},
        )
        return res.status_code == 200


async def add_to_github_team(username: str) -> None:
    async with httpx.AsyncClient(timeout=10) as client:
        res = await client.put(
            f"https://api.github.com/orgs/{GITHUB_ORG}/teams/{GITHUB_TEAM_SLUG}/memberships/{username}",
            headers={**_HEADERS, "Authorization": f"Bearer {GITHUB_TOKEN}"},
        )
        if not res.is_success:
            raise RuntimeError(f"GitHub API error {res.status_code}: {res.text}")


async def remove_from_github_team(username: str) -> None:
    async with httpx.AsyncClient(timeout=10) as client:
        res = await client.delete(
            f"https://api.github.com/orgs/{GITHUB_ORG}/teams/{GITHUB_TEAM_SLUG}/memberships/{username}",
            headers={**_HEADERS, "Authorization": f"Bearer {GITHUB_TOKEN}"},
        )
        if not res.is_success and res.status_code != 404:
            raise RuntimeError(f"GitHub API error {res.status_code}: {res.text}")
