"""Configuration for dependency updates."""

from __future__ import annotations

from pathlib import Path

# Repository root (relative to this file)
REPO_ROOT = Path(__file__).parent.parent.parent

# Files to update
PYPROJECT_FILES = [
    REPO_ROOT / "pyproject.toml",
    REPO_ROOT / "{{cookiecutter.project_name}}" / "pyproject.toml",
]

ACTION_YML_FILES = [
    REPO_ROOT / ".github" / "actions" / "setup-python-env" / "action.yml",
    REPO_ROOT / "{{cookiecutter.project_name}}" / ".github" / "actions" / "setup-python-env" / "action.yml",
]

PRECOMMIT_CONFIG = REPO_ROOT / ".pre-commit-config.yaml"

# PyPI packages to track
PYPI_PACKAGES = [
    "pytest",
    "pre-commit",
    "tox-uv",
    "deptry",
    "mypy",
    "ty",
    "pytest-cov",
    "ruff",
    "mkdocs",
    "mkdocs-material",
    "mkdocstrings",
    "cookiecutter",
    "pytest-cookies",
    "hatchling",
]

# Pre-commit hooks: (repo_url, github_owner_repo)
PRECOMMIT_HOOKS = [
    ("https://github.com/pre-commit/pre-commit-hooks", "pre-commit/pre-commit-hooks"),
    ("https://github.com/astral-sh/ruff-pre-commit", "astral-sh/ruff-pre-commit"),
]
