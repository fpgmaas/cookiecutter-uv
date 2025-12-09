"""Version fetchers for PyPI and GitHub."""

from __future__ import annotations

import json
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


class VersionFetcher:
    """Fetches latest versions from package registries."""

    TIMEOUT = 30

    def _fetch_json(self, url: str) -> dict | None:
        """Fetch JSON from a URL."""
        try:
            with urlopen(url, timeout=self.TIMEOUT) as response:
                return json.loads(response.read().decode())
        except (HTTPError, URLError, json.JSONDecodeError):
            return None

    def get_pypi_version(self, package: str) -> str | None:
        """Get the latest version of a package from PyPI."""
        data = self._fetch_json(f"https://pypi.org/pypi/{package}/json")
        if data:
            return data.get("info", {}).get("version")
        return None

    def get_github_release(self, owner_repo: str) -> str | None:
        """Get the latest release tag from GitHub."""
        data = self._fetch_json(f"https://api.github.com/repos/{owner_repo}/releases/latest")
        if data:
            tag = data.get("tag_name", "")
            return tag.lstrip("v") if tag else None
        return None

    def get_github_tag(self, owner_repo: str) -> str | None:
        """Get the latest tag from GitHub (for repos without releases)."""
        data = self._fetch_json(f"https://api.github.com/repos/{owner_repo}/tags")
        if data and len(data) > 0:
            tag = data[0].get("name", "")
            return tag.lstrip("v") if tag else None
        return None
