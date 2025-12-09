"""File updaters for dependencies."""

from __future__ import annotations

import logging
import re
from pathlib import Path

from cookiecutter_uv.cicd.config import (
    PRECOMMIT_HOOKS,
    PYPI_PACKAGES,
    UV_REPO,
)
from cookiecutter_uv.cicd.fetchers import get_github_release, get_github_tag, get_pypi_version

logger = logging.getLogger(__name__)


class PyprojectTomlUpdater:
    """Updates package versions in pyproject.toml files."""

    def __init__(self, files: list[Path]) -> None:
        self.files = files

    @staticmethod
    def _build_pattern(package: str) -> str:
        return rf'("{re.escape(package)}(?:\[[^\]]*\])?)>=([^"]+)"'

    @staticmethod
    def _build_replacement(version: str) -> str:
        return f'\\g<1>>={version}"'

    def _update_file(self, filepath: Path, package: str, version: str) -> bool:
        """Update a single package in a pyproject.toml file. Returns True if updated."""
        content = filepath.read_text()
        pattern = self._build_pattern(package)
        replacement = self._build_replacement(version)
        new_content, count = re.subn(pattern, replacement, content)

        if count > 0 and new_content != content:
            filepath.write_text(new_content)
            return True
        return False

    def _matches(self, filepath: Path, package: str) -> bool:
        """Check if file contains the package pattern."""
        content = filepath.read_text()
        return bool(re.search(self._build_pattern(package), content))

    def update(self, dry_run: bool = False) -> int:
        """Update all pyproject.toml files. Returns count of updates."""
        update_count = 0

        for package in PYPI_PACKAGES:
            version = get_pypi_version(package)
            if not version:
                logger.warning("Failed to fetch version for %s", package)
                continue

            for filepath in self.files:
                if not filepath.exists():
                    continue

                if dry_run:
                    if self._matches(filepath, package):
                        logger.info("%s: %s -> %s", filepath, package, version)
                        update_count += 1
                elif self._update_file(filepath, package, version):
                    logger.info("%s: %s -> %s", filepath, package, version)
                    update_count += 1

        return update_count


class ActionYmlUpdater:
    """Updates uv version in action.yml files."""

    PATTERN = (
        r'(uv-version:\s*\n\s*description:[^\n]*\n\s*required:[^\n]*\n\s*default:\s*")'
        r'[0-9]+\.[0-9]+\.[0-9]+(")'
    )

    def __init__(self, files: list[Path]) -> None:
        self.files = files

    @staticmethod
    def _build_replacement(version: str) -> str:
        return rf"\g<1>{version}\2"

    def _update_file(self, filepath: Path, version: str) -> bool:
        """Update uv version in an action.yml file. Returns True if updated."""
        content = filepath.read_text()
        replacement = self._build_replacement(version)
        new_content, count = re.subn(self.PATTERN, replacement, content)

        if count > 0 and new_content != content:
            filepath.write_text(new_content)
            return True
        return False

    def _matches(self, filepath: Path) -> bool:
        """Check if file contains the uv version pattern."""
        content = filepath.read_text()
        return bool(re.search(self.PATTERN, content))

    def update(self, dry_run: bool = False) -> int:
        """Update all action.yml files. Returns count of updates."""
        version = get_github_release(UV_REPO)
        if not version:
            logger.warning("Failed to fetch uv version")
            return 0

        update_count = 0

        for filepath in self.files:
            if not filepath.exists():
                continue

            if dry_run:
                if self._matches(filepath):
                    logger.info("%s: uv -> %s", filepath, version)
                    update_count += 1
            elif self._update_file(filepath, version):
                logger.info("%s: uv -> %s", filepath, version)
                update_count += 1

        return update_count


class PreCommitConfigUpdater:
    """Updates hook revisions in .pre-commit-config.yaml."""

    def __init__(self, config_file: Path) -> None:
        self.config_file = config_file

    @staticmethod
    def _build_pattern(repo_url: str) -> str:
        return rf'(- repo: {re.escape(repo_url)}\s*\n\s*rev:\s*")[^"]+(")'

    @staticmethod
    def _build_replacement(version: str) -> str:
        return rf"\g<1>v{version}\2"

    @staticmethod
    def _extract_hook_name(repo_url: str) -> str:
        return repo_url.split("/")[-1]

    def _update_hook(self, content: str, repo_url: str, version: str) -> tuple[str, bool]:
        """Update a single hook in pre-commit config. Returns (new_content, updated)."""
        pattern = self._build_pattern(repo_url)
        replacement = self._build_replacement(version)
        new_content, count = re.subn(pattern, replacement, content)

        if count > 0 and new_content != content:
            return new_content, True
        return content, False

    def _matches(self, content: str, repo_url: str) -> bool:
        """Check if content contains the hook pattern."""
        return bool(re.search(self._build_pattern(repo_url), content))

    def update(self, dry_run: bool = False) -> int:
        """Update pre-commit config. Returns count of updates."""
        if not self.config_file.exists():
            return 0

        update_count = 0
        content = self.config_file.read_text()

        for repo_url, github_repo in PRECOMMIT_HOOKS:
            version = get_github_tag(github_repo)
            if not version:
                logger.warning("Failed to fetch version for %s", github_repo)
                continue

            hook_name = self._extract_hook_name(repo_url)

            if dry_run:
                if self._matches(content, repo_url):
                    logger.info("%s: %s -> v%s", self.config_file, hook_name, version)
                    update_count += 1
            else:
                new_content, updated = self._update_hook(content, repo_url, version)
                if updated:
                    content = new_content
                    logger.info("%s: %s -> v%s", self.config_file, hook_name, version)
                    update_count += 1

        if not dry_run and update_count > 0:
            self.config_file.write_text(content)

        return update_count
