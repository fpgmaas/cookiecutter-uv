from __future__ import annotations


def test_bake_project(bake):
    project = bake(project_name="my-project")
    assert project.path.name == "my-project"
    assert project.path.is_dir()


def test_cicd_contains_pypi_secrets(bake):
    project = bake(publish_to_pypi="y")
    assert project.is_valid_yaml(".github/workflows/on-release-main.yml")
    assert project.file_contains(".github/workflows/on-release-main.yml", "PYPI_TOKEN")
    assert project.file_contains("Makefile", "build-and-publish")


def test_dont_publish(bake):
    project = bake(publish_to_pypi="n")
    assert project.is_valid_yaml(".github/workflows/on-release-main.yml")
    assert not project.file_contains(".github/workflows/on-release-main.yml", "make build-and-publish")


def test_mkdocs(bake):
    project = bake(mkdocs="y")
    assert project.is_valid_yaml(".github/workflows/on-release-main.yml")
    assert project.file_contains(".github/workflows/on-release-main.yml", "mkdocs gh-deploy")
    assert project.file_contains("Makefile", "docs:")
    assert project.has_dir("docs")


def test_not_mkdocs(bake):
    project = bake(mkdocs="n")
    assert project.is_valid_yaml(".github/workflows/on-release-main.yml")
    assert not project.file_contains(".github/workflows/on-release-main.yml", "mkdocs gh-deploy")
    assert not project.file_contains("Makefile", "docs:")
    assert not project.has_dir("docs")


def test_tox(bake):
    project = bake()
    assert project.has_file("tox.ini")
    assert project.file_contains("tox.ini", "[tox]")


def test_license_mit(bake):
    project = bake(open_source_license="MIT license")
    assert project.file_contains("LICENSE", "MIT License")


def test_license_bsd(bake):
    project = bake(open_source_license="BSD license")
    assert project.file_contains("LICENSE", "Redistributions of source code")


def test_license_isc(bake):
    project = bake(open_source_license="ISC license")
    assert project.file_contains("LICENSE", "ISC License")


def test_license_apache(bake):
    project = bake(open_source_license="Apache Software License 2.0")
    assert project.file_contains("LICENSE", "Apache License")


def test_license_gplv3(bake):
    project = bake(open_source_license="GNU General Public License v3")
    assert project.file_contains("LICENSE", "GNU GENERAL PUBLIC LICENSE")


def test_license_no_license(bake):
    project = bake(open_source_license="Not open source")
    assert not project.has_file("LICENSE")
