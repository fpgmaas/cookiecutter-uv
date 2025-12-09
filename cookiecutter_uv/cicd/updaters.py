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
    UV_REPO,
)
from cookiecutter_uv.cicd.fetchers import get_github_release, get_github_tag, get_pypi_version

logger = logging.getLogger(__name__)


class PyprojectTomlUpdater:
    """Updates package versions in pyproject.toml files."""

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
            pattern = rf'(- repo: {re.escape(repo_url)}\s*\n\s*rev:\s*")[^"]+(")'

            def replacement(m: re.Match, v: str = version) -> str:
                return f"{m.group(1)}v{v}{m.group(2)}"

            new_content, count = re.subn(pattern, replacement, content)

            if count > 0 and new_content != content:
                logger.info("%s: %s -> v%s", PRECOMMIT_CONFIG.name, hook_name, version)
                if not dry_run:
                    PRECOMMIT_CONFIG.write_text(new_content)
                content = new_content
                update_count += 1

        return update_count
