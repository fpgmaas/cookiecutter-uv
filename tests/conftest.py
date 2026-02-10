from __future__ import annotations

import os
import shlex
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import pytest
import yaml


@dataclass
class BakedProject:
    """Wrapper around a baked cookiecutter project with convenience methods for testing."""

    project_path: Path
    exit_code: int
    exception: Exception | None
    options: dict[str, str] = field(default_factory=dict)

    @property
    def path(self) -> Path:
        return self.project_path

    def has_file(self, rel_path: str) -> bool:
        return (self.path / rel_path).is_file()

    def has_dir(self, rel_path: str) -> bool:
        return (self.path / rel_path).is_dir()

    def read_file(self, rel_path: str) -> str:
        return (self.path / rel_path).read_text()

    def file_contains(self, rel_path: str, text: str) -> bool:
        return text in self.read_file(rel_path)

    def is_valid_yaml(self, rel_path: str) -> bool:
        path = self.path / rel_path
        if not path.is_file():
            return False
        try:
            with path.open() as f:
                yaml.safe_load(f)
        except (yaml.YAMLError, OSError):
            return False
        return True

    def run(self, command: str, check: bool = False) -> subprocess.CompletedProcess:
        # Strip VIRTUAL_ENV so the outer test environment doesn't leak
        # into the baked project's subprocess.
        env = {k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}
        return subprocess.run(
            shlex.split(command),
            cwd=self.path,
            capture_output=True,
            text=True,
            check=check,
            env=env,
        )

    def git_init(self) -> None:
        """Initialize a git repo and stage all files (needed for pre-commit)."""
        self.run("git init", check=True)
        self.run("git add .", check=True)

    def install(self) -> None:
        self.git_init()
        result = self.run("uv sync")
        assert result.returncode == 0, f"uv sync failed:\n{result.stderr}"

    def run_tests(self) -> None:
        result = self.run("uv run make test")
        assert result.returncode == 0, f"make test failed:\n{result.stderr}"

    def run_check(self) -> None:
        # Run pre-commit once to auto-fix formatting issues from Jinja2 rendering
        # (e.g. end-of-file-fixer), then re-stage and run the real check.
        self.run("uv run pre-commit run -a")
        self.run("git add .", check=True)
        result = self.run("uv run make check")
        assert result.returncode == 0, f"make check failed:\n{result.stdout}\n{result.stderr}"


@pytest.fixture
def bake(cookies):
    """Fixture factory that bakes a cookiecutter project and returns a BakedProject.

    Usage:
        def test_something(bake):
            project = bake(mkdocs="n", codecov="y")
            assert project.has_file("pyproject.toml")
    """

    def _bake(**options) -> BakedProject:
        result = cookies.bake(extra_context=options)
        project = BakedProject(
            project_path=result.project_path,
            exit_code=result.exit_code,
            exception=result.exception,
            options=options,
        )
        assert project.exit_code == 0, f"Bake failed with options {options}: {project.exception}"
        assert project.exception is None
        return project

    return _bake
