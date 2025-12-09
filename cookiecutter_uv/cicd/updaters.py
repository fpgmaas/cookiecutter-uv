"""File updaters for dependencies."""

from __future__ import annotations

import logging
import re

from cookiecutter_uv.cicd.config import (
    ACTION_YML_FILES,
    PRECOMMIT_CONFIG,
    PRECOMMIT_HOOKS,
    PYPI_PACKAGES,
    PYPROJECT_FILES,
)
from cookiecutter_uv.cicd.fetchers import VersionFetcher

logger = logging.getLogger(__name__)


class PyprojectTomlUpdater:
    """Updates package versions in pyproject.toml files."""

    def __init__(self, fetcher: VersionFetcher | None = None) -> None:
        self.fetcher = fetcher or VersionFetcher()
        self.files = PYPROJECT_FILES
        self.packages = PYPI_PACKAGES

    def update(self, dry_run: bool = False) -> int:
        """Update all pyproject.toml files. Returns count of updates."""
        update_count = 0

        for package in self.packages:
            version = self.fetcher.get_pypi_version(package)
            if not version:
                logger.warning("Failed to fetch version for %s", package)
                continue

            for filepath in self.files:
                if not filepath.exists():
                    continue

                content = filepath.read_text()
                pattern = rf'"{re.escape(package)}(\[[^\]]*\])?>=([^"]+)"'

                def replacement(m: re.Match) -> str:
                    extras = m.group(1) or ""
                    return f'"{package}{extras}>={version}"'

                new_content, count = re.subn(pattern, replacement, content)

                if count > 0 and new_content != content:
                    logger.info("%s: %s -> %s", filepath.name, package, version)
                    if not dry_run:
                        filepath.write_text(new_content)
                    update_count += 1

        return update_count


class ActionYmlUpdater:
    """Updates uv version in action.yml files."""

    def __init__(self, fetcher: VersionFetcher | None = None) -> None:
        self.fetcher = fetcher or VersionFetcher()
        self.files = ACTION_YML_FILES

    def update(self, dry_run: bool = False) -> int:
        """Update all action.yml files. Returns count of updates."""
        version = self.fetcher.get_github_release("astral-sh/uv")
        if not version:
            logger.warning("Failed to fetch uv version")
            return 0

        update_count = 0
        pattern = (
            r'(uv-version:\s*\n\s*description:[^\n]*\n\s*required:[^\n]*\n\s*default:\s*")'
            r'[0-9]+\.[0-9]+\.[0-9]+(")'
        )

        for filepath in self.files:
            if not filepath.exists():
                continue

            content = filepath.read_text()

            def replacement(m: re.Match) -> str:
                return f"{m.group(1)}{version}{m.group(2)}"

            new_content, count = re.subn(pattern, replacement, content)

            if count > 0 and new_content != content:
                logger.info("%s: uv -> %s", filepath.name, version)
                if not dry_run:
                    filepath.write_text(new_content)
                update_count += 1

        return update_count


class PreCommitConfigUpdater:
    """Updates hook revisions in .pre-commit-config.yaml."""

    def __init__(self, fetcher: VersionFetcher | None = None) -> None:
        self.fetcher = fetcher or VersionFetcher()
        self.file = PRECOMMIT_CONFIG
        self.hooks = PRECOMMIT_HOOKS

    def update(self, dry_run: bool = False) -> int:
        """Update pre-commit config. Returns count of updates."""
        if not self.file.exists():
            return 0

        update_count = 0
        content = self.file.read_text()

        for repo_url, owner_repo in self.hooks:
            version = self.fetcher.get_github_tag(owner_repo)
            if not version:
                logger.warning("Failed to fetch version for %s", owner_repo)
                continue

            hook_name = repo_url.split("/")[-1]
            pattern = rf'(- repo: {re.escape(repo_url)}\s*\n\s*rev:\s*")[^"]+(")'

            def replacement(m: re.Match, v: str = version) -> str:
                return f"{m.group(1)}v{v}{m.group(2)}"

            new_content, count = re.subn(pattern, replacement, content)

            if count > 0 and new_content != content:
                logger.info("%s: %s -> v%s", self.file.name, hook_name, version)
                if not dry_run:
                    self.file.write_text(new_content)
                content = new_content  # Update for next iteration
                update_count += 1

        return update_count
