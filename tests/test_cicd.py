"""Tests for cookiecutter_uv.cicd module."""

from __future__ import annotations

import shutil
from pathlib import Path
from unittest.mock import patch

import pytest

from cookiecutter_uv.cicd.fetchers import GitHubRepo, get_github_release, get_github_tag, get_pypi_version
from cookiecutter_uv.cicd.updaters import ActionYmlUpdater, PreCommitConfigUpdater, PyprojectTomlUpdater

DATA_DIR = Path(__file__).parent / "data" / "cicd"


@pytest.fixture
def temp_pyproject(tmp_path: Path) -> Path:
    """Copy sample pyproject.toml to temp directory."""
    dest = tmp_path / "pyproject.toml"
    shutil.copy(DATA_DIR / "sample_pyproject.toml", dest)
    return dest


@pytest.fixture
def temp_action_yml(tmp_path: Path) -> Path:
    """Copy sample action.yml to temp directory."""
    dest = tmp_path / "action.yml"
    shutil.copy(DATA_DIR / "sample_action.yml", dest)
    return dest


@pytest.fixture
def temp_precommit(tmp_path: Path) -> Path:
    """Copy sample pre-commit config to temp directory."""
    dest = tmp_path / ".pre-commit-config.yaml"
    shutil.copy(DATA_DIR / "sample_precommit.yaml", dest)
    return dest


class TestGitHubRepo:
    def test_str(self) -> None:
        repo = GitHubRepo(owner="astral-sh", repo="uv")
        assert str(repo) == "astral-sh/uv"


class TestFetchers:
    def test_get_pypi_version_returns_version(self) -> None:
        mock_response = {"info": {"version": "1.2.3"}}
        with patch("cookiecutter_uv.cicd.fetchers._fetch_json", return_value=mock_response):
            assert get_pypi_version("pytest") == "1.2.3"

    def test_get_pypi_version_returns_none_on_failure(self) -> None:
        with patch("cookiecutter_uv.cicd.fetchers._fetch_json", return_value=None):
            assert get_pypi_version("nonexistent") is None

    def test_get_github_release_strips_v_prefix(self) -> None:
        mock_response = {"tag_name": "v0.9.0"}
        with patch("cookiecutter_uv.cicd.fetchers._fetch_json", return_value=mock_response):
            assert get_github_release(GitHubRepo("astral-sh", "uv")) == "0.9.0"

    def test_get_github_tag_strips_v_prefix(self) -> None:
        mock_response = [{"name": "v5.0.0"}]
        with patch("cookiecutter_uv.cicd.fetchers._fetch_json", return_value=mock_response):
            assert get_github_tag(GitHubRepo("pre-commit", "pre-commit-hooks")) == "5.0.0"


class TestPyprojectTomlUpdater:
    def test_updates_package_version(self, temp_pyproject: Path) -> None:
        with (
            patch("cookiecutter_uv.cicd.updaters.PYPROJECT_FILES", [temp_pyproject]),
            patch("cookiecutter_uv.cicd.updaters.PYPI_PACKAGES", ["pytest"]),
            patch("cookiecutter_uv.cicd.updaters.get_pypi_version", return_value="8.0.0"),
        ):
            count = PyprojectTomlUpdater().update()

        assert count == 1
        content = temp_pyproject.read_text()
        assert '"pytest>=8.0.0"' in content

    def test_updates_package_with_extras(self, temp_pyproject: Path) -> None:
        with (
            patch("cookiecutter_uv.cicd.updaters.PYPROJECT_FILES", [temp_pyproject]),
            patch("cookiecutter_uv.cicd.updaters.PYPI_PACKAGES", ["mkdocstrings"]),
            patch("cookiecutter_uv.cicd.updaters.get_pypi_version", return_value="0.30.0"),
        ):
            count = PyprojectTomlUpdater().update()

        assert count == 1
        content = temp_pyproject.read_text()
        assert '"mkdocstrings[python]>=0.30.0"' in content

    def test_dry_run_does_not_modify(self, temp_pyproject: Path) -> None:
        original = temp_pyproject.read_text()
        with (
            patch("cookiecutter_uv.cicd.updaters.PYPROJECT_FILES", [temp_pyproject]),
            patch("cookiecutter_uv.cicd.updaters.PYPI_PACKAGES", ["pytest"]),
            patch("cookiecutter_uv.cicd.updaters.get_pypi_version", return_value="8.0.0"),
        ):
            PyprojectTomlUpdater().update(dry_run=True)

        assert temp_pyproject.read_text() == original


class TestActionYmlUpdater:
    def test_updates_uv_version(self, temp_action_yml: Path) -> None:
        with (
            patch("cookiecutter_uv.cicd.updaters.ACTION_YML_FILES", [temp_action_yml]),
            patch("cookiecutter_uv.cicd.updaters.get_github_release", return_value="0.9.7"),
        ):
            count = ActionYmlUpdater().update()

        assert count == 1
        content = temp_action_yml.read_text()
        assert 'default: "0.9.7"' in content


class TestPreCommitConfigUpdater:
    def test_updates_hook_revision(self, temp_precommit: Path) -> None:
        hooks = [
            ("https://github.com/pre-commit/pre-commit-hooks", GitHubRepo("pre-commit", "pre-commit-hooks")),
        ]
        with (
            patch("cookiecutter_uv.cicd.updaters.PRECOMMIT_CONFIG", temp_precommit),
            patch("cookiecutter_uv.cicd.updaters.PRECOMMIT_HOOKS", hooks),
            patch("cookiecutter_uv.cicd.updaters.get_github_tag", return_value="5.0.0"),
        ):
            count = PreCommitConfigUpdater().update()

        assert count == 1
        content = temp_precommit.read_text()
        assert 'rev: "v5.0.0"' in content
