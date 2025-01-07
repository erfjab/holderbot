import json
import httpx
from packaging import version


async def check_github_version(current_version: str) -> tuple[bool, str]:
    """
    Check if there's a newer version available on GitHub
    Returns: (has_update, latest_version)
    """
    current = version.parse(current_version.lstrip("v"))

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.github.com/repos/erfjab/holderbot/releases/latest",
                headers={"Accept": "application/vnd.github.v3+json"},
                timeout=10.0,
            )

            if response.status_code != 200:
                return False, current_version

            data = response.json()
            latest_version = data["tag_name"].lstrip("v")
            latest = version.parse(latest_version)

            return latest > current, data["tag_name"]

    except (httpx.RequestError, json.JSONDecodeError, KeyError):
        return False, current_version
