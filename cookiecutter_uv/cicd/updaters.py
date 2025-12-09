"""File updaters for dependencies."""

from __future__ import annotations

import logging
import re
from pathlib import Path

from cookiecutter_uv.cicd.config import (
    ACTION_YML_FILES,
    PRECOMMIT_CONFIG,
    PRECOMMIT_HOOKS,
    PYPI_PACKAGES,
    PYPROJECT_FILES,
    UV_REPO,
)
from cookiecutter_uv.cicd.fetchers import get_github_release, get_github_tag, get_pypi_version

logger = logging.getLogger(__name__)


class PyprojectTomlUpdater:
    """Updates package versions in pyproject.toml files."""

    def _update_file(self, filepath: Path, package: str, version: str) -> bool:
        """Update a single package in a pyproject.toml file. Returns True if updated."""
        content = filepath.read_text()
        pattern = rf'"{re.escape(package)}(\[[^\]]*\])?>=([^"]+)"'

        def replacement(m: re.Match[str], pkg: str = package, ver: str = version) -> str:
            extras = m.group(1) or ""
            return f'"{pkg}{extras}>={ver}"'

        new_content, count = re.subn(pattern, replacement, content)

        if count > 0 and new_content != content:
            filepath.write_text(new_content)
            return True
        return False

    def update(self, dry_run: bool = False) -> int:
        """Update all pyproject.toml files. Returns count of updates."""
        update_count = 0

        for package in PYPI_PACKAGES:
            version = get_pypi_version(package)
            if not version:
                logger.warning("Failed to fetch version for %s", package)
                continue

            for filepath in PYPROJECT_FILES:
                if not filepath.exists():
                    continue

                if dry_run:
                    content = filepath.read_text()
                    pattern = rf'"{re.escape(package)}(\[[^\]]*\])?>=([^"]+)"'
                    if re.search(pattern, content):
                        logger.info("%s: %s -> %s", filepath.name, package, version)
                        update_count += 1
                elif self._update_file(filepath, package, version):
                    logger.info("%s: %s -> %s", filepath.name, package, version)
                    update_count += 1

        return update_count


class ActionYmlUpdater:
    """Updates uv version in action.yml files."""

    def _update_file(self, filepath: Path, version: str, pattern: str) -> bool:
        """Update uv version in an action.yml file. Returns True if updated."""
        content = filepath.read_text()

        def replacement(m: re.Match[str], ver: str = version) -> str:
            return f"{m.group(1)}{ver}{m.group(2)}"

        new_content, count = re.subn(pattern, replacement, content)

        if count > 0 and new_content != content:
            filepath.write_text(new_content)
            return True
        return False

    def update(self, dry_run: bool = False) -> int:
        """Update all action.yml files. Returns count of updates."""
        version = get_github_release(UV_REPO)
        if not version:
            logger.warning("Failed to fetch uv version")
            return 0

        update_count = 0
        pattern = (
            r'(uv-version:\s*\n\s*description:[^\n]*\n\s*required:[^\n]*\n\s*default:\s*")'
            r'[0-9]+\.[0-9]+\.[0-9]+(")'
        )

        for filepath in ACTION_YML_FILES:
            if not filepath.exists():
                continue

            if dry_run:
                content = filepath.read_text()
                if re.search(pattern, content):
                    logger.info("%s: uv -> %s", filepath.name, version)
                    update_count += 1
            elif self._update_file(filepath, version, pattern):
                logger.info("%s: uv -> %s", filepath.name, version)
                update_count += 1

        return update_count


class PreCommitConfigUpdater:
    """Updates hook revisions in .pre-commit-config.yaml."""

    def _update_hook(self, filepath: Path, content: str, repo_url: str, version: str) -> tuple[str, bool]:
        """Update a single hook in pre-commit config. Returns (new_content, updated)."""
        pattern = rf'(- repo: {re.escape(repo_url)}\s*\n\s*rev:\s*")[^"]+(")'

        def replacement(m: re.Match[str], v: str = version) -> str:
            return f"{m.group(1)}v{v}{m.group(2)}"

        new_content, count = re.subn(pattern, replacement, content)

        if count > 0 and new_content != content:
            filepath.write_text(new_content)
            return new_content, True
        return content, False

    def update(self, dry_run: bool = False) -> int:
        """Update pre-commit config. Returns count of updates."""
        if not PRECOMMIT_CONFIG.exists():
            return 0

        update_count = 0
        content = PRECOMMIT_CONFIG.read_text()

        for repo_url, github_repo in PRECOMMIT_HOOKS:
            version = get_github_tag(github_repo)
            if not version:
                logger.warning("Failed to fetch version for %s", github_repo)
                continue

            hook_name = repo_url.split("/")[-1]

            if dry_run:
                pattern = rf'(- repo: {re.escape(repo_url)}\s*\n\s*rev:\s*")[^"]+(")'
                if re.search(pattern, content):
                    logger.info("%s: %s -> v%s", PRECOMMIT_CONFIG.name, hook_name, version)
                    update_count += 1
            else:
                content, updated = self._update_hook(PRECOMMIT_CONFIG, content, repo_url, version)
                if updated:
                    logger.info("%s: %s -> v%s", PRECOMMIT_CONFIG.name, hook_name, version)
                    update_count += 1

        return update_count
