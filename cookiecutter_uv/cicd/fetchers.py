"""Version fetchers for PyPI and GitHub."""

from __future__ import annotations

import json
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

TIMEOUT = 30


@dataclass
class GitHubRepo:
    """A GitHub repository reference."""

    owner: str
    repo: str

    def __str__(self) -> str:
        return f"{self.owner}/{self.repo}"
    

def get_pypi_version(package: str) -> str | None:
    """Get the latest version of a package from PyPI."""
    data = _fetch_json(f"https://pypi.org/pypi/{package}/json")
    if data:
        return data.get("info", {}).get("version")
    return None


def get_github_release(repo: GitHubRepo) -> str | None:
    """Get the latest release tag from GitHub."""
    data = _fetch_json(f"https://api.github.com/repos/{repo}/releases/latest")
    if data:
        tag = data.get("tag_name", "")
        return tag.lstrip("v") if tag else None
    return None


def get_github_tag(repo: GitHubRepo) -> str | None:
    """Get the latest tag from GitHub (for repos without releases)."""
    data = _fetch_json(f"https://api.github.com/repos/{repo}/tags")
    if data and len(data) > 0:
        tag = data[0].get("name", "")
        return tag.lstrip("v") if tag else None
    return None

def _fetch_json(url: str) -> dict | None:
    """Fetch JSON from a URL."""
    try:
        with urlopen(url, timeout=TIMEOUT) as response:
            return json.loads(response.read().decode())
    except (HTTPError, URLError, json.JSONDecodeError):
        return None