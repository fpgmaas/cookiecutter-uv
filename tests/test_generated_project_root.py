from __future__ import annotations

from tests.utils import run_within_dir


def test_full_structure(cookies, tmp_path):
    """
    Test to verify the correct structure of a generated project.

    The test checks that all expected files and directories exist in the
    generated project directory and that the project creation process
    completes without errors.
    """

    expected_files = [
        ".devcontainer",
        ".github",
        ".gitignore",
        ".pre-commit-config.yaml",
        "CONTRIBUTING.md",
        "Dockerfile",
        "LICENSE",
        "Makefile",
        "README.md",
        "codecov.yaml",
        "docs",
        "example_project",
        "mkdocs.yml",
        "pyproject.toml",
        "tests",
        "tox.ini",
    ]

    with run_within_dir(tmp_path):
        result = cookies.bake()

        # Check that all expected files and folders are present
        for file in expected_files:
            file_path = result.project_path / file
            assert file_path.exists(), f"Missing file or folder: {file_path}"

        # Final assertions
        assert result.exit_code == 0
        assert result.exception is None
