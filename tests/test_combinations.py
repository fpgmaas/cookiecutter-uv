from __future__ import annotations

import pytest

MINIMAL = {
    "include_github_actions": "n",
    "publish_to_pypi": "n",
    "deptry": "n",
    "mkdocs": "n",
    "codecov": "n",
    "dockerfile": "n",
    "devcontainer": "n",
}

COMBINATIONS = [
    pytest.param({}, id="all-defaults"),
    pytest.param(MINIMAL, id="minimal"),
    pytest.param({"layout": "src"}, id="src-layout-defaults"),
    pytest.param({**MINIMAL, "layout": "src"}, id="src-layout-minimal"),
    pytest.param({"publish_to_pypi": "n", "mkdocs": "n"}, id="no-publish-no-mkdocs"),
    pytest.param({"include_github_actions": "n"}, id="no-github-actions"),
    pytest.param({"type_checker": "ty"}, id="ty-type-checker"),
    pytest.param({"mkdocs": "y", "codecov": "n"}, id="mkdocs-no-codecov"),
    pytest.param({"codecov": "n", "include_github_actions": "n"}, id="no-codecov-no-actions"),
    pytest.param({"layout": "src", "type_checker": "ty", "publish_to_pypi": "n"}, id="src-ty-no-publish"),
]

# Defaults from cookiecutter.json (first item in each list)
DEFAULTS = {
    "layout": "flat",
    "include_github_actions": "y",
    "publish_to_pypi": "y",
    "deptry": "y",
    "mkdocs": "y",
    "codecov": "y",
    "dockerfile": "y",
    "devcontainer": "y",
    "type_checker": "mypy",
}


def resolve_options(options: dict[str, str]) -> dict[str, str]:
    """Return the full set of resolved options (defaults merged with overrides)."""
    return {**DEFAULTS, **options}


@pytest.mark.parametrize("options", COMBINATIONS)
class TestStructure:
    """Validate file presence/absence for each option combination."""

    def test_always_present_files(self, bake, options):
        EXPECTED_FILES = [
            ".gitignore",
            ".pre-commit-config.yaml",
            "CONTRIBUTING.md",
            "LICENSE",
            "Makefile",
            "README.md",
            "pyproject.toml",
            "tests",
            "tox.ini",
        ]
        project = bake(**options)
        for rel_path in EXPECTED_FILES:
            assert (project.path / rel_path).exists(), f"Expected {rel_path} to exist"

    def test_conditional_files(self, bake, options):
        project = bake(**options)
        effective = resolve_options(options)

        if effective["dockerfile"] == "y":
            assert project.has_file("Dockerfile")
        else:
            assert not project.has_file("Dockerfile")

        if effective["mkdocs"] == "y":
            assert project.has_dir("docs")
            assert project.has_file("mkdocs.yml")
        else:
            assert not project.has_dir("docs")
            assert not project.has_file("mkdocs.yml")

        if effective["codecov"] == "y":
            assert project.has_file("codecov.yaml")
        else:
            assert not project.has_file("codecov.yaml")

        if effective["devcontainer"] == "y":
            assert project.has_dir(".devcontainer")
        else:
            assert not project.has_dir(".devcontainer")

        if effective["include_github_actions"] == "y":
            assert project.has_dir(".github")
        else:
            assert not project.has_dir(".github")

    def test_layout(self, bake, options):
        effective = resolve_options(options)
        project = bake(**options)
        if effective["layout"] == "src":
            assert project.has_dir("src/example_project")
            assert not project.has_dir("example_project")
        else:
            assert project.has_dir("example_project")
            assert not project.has_dir("src")

    def test_release_workflow(self, bake, options):
        effective = resolve_options(options)
        project = bake(**options)
        if effective["include_github_actions"] != "y":
            return  # no .github at all
        has_release = effective["publish_to_pypi"] == "y" or effective["mkdocs"] == "y"
        workflow = ".github/workflows/on-release-main.yml"
        if has_release:
            assert project.has_file(workflow), "Expected release workflow to exist"
        else:
            assert not project.has_file(workflow), "Expected release workflow to be absent"

    def test_yaml_validity(self, bake, options):
        effective = resolve_options(options)
        project = bake(**options)
        if effective["include_github_actions"] == "y":
            assert project.is_valid_yaml(".github/workflows/main.yml")

    def test_pyproject_type_checker(self, bake, options):
        effective = resolve_options(options)
        project = bake(**options)
        content = project.read_file("pyproject.toml")
        if effective["type_checker"] == "mypy":
            assert '"mypy' in content
            assert '"ty' not in content
        else:
            assert '"ty' in content
            assert '"mypy' not in content

    def test_makefile_targets(self, bake, options):
        effective = resolve_options(options)
        project = bake(**options)
        content = project.read_file("Makefile")

        if effective["publish_to_pypi"] == "y":
            assert "build-and-publish" in content
        else:
            assert "build-and-publish" not in content

        if effective["mkdocs"] == "y":
            assert "docs:" in content
        else:
            assert "docs:" not in content

    def test_codecov_workflow(self, bake, options):
        effective = resolve_options(options)
        project = bake(**options)
        if effective["include_github_actions"] == "y":
            if effective["codecov"] == "y":
                assert project.has_file(".github/workflows/validate-codecov-config.yml")
                assert project.has_file("codecov.yaml")
            else:
                assert not project.has_file(".github/workflows/validate-codecov-config.yml")
                assert not project.has_file("codecov.yaml")


@pytest.mark.slow
@pytest.mark.parametrize("options", COMBINATIONS)
def test_install_and_run_tests(bake, options):
    """Bake, install dependencies, and run the generated project's test suite."""
    project = bake(**options)
    project.install()
    project.run_tests()


@pytest.mark.slow
def test_check_passes_on_default_project(bake):
    """A freshly baked default project should pass its own ``make check``."""
    project = bake()
    project.install()
    project.run_check()
