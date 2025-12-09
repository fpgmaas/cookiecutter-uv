"""CLI for dependency updates."""

from __future__ import annotations

import logging
from pathlib import Path

import click

from cookiecutter_uv.cicd.updaters import ActionYmlUpdater, PreCommitConfigUpdater, PyprojectTomlUpdater

logging.basicConfig(level=logging.INFO, format="%(message)s")


@click.group()
def cli() -> None:
    """CI/CD utilities for cookiecutter-uv."""


@cli.command()
@click.option("--dry-run", is_flag=True, help="Print changes without writing")
@click.option(
    "--pyproject",
    "pyproject_files",
    multiple=True,
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="pyproject.toml files to update (can be repeated)",
)
@click.option(
    "--action-yml",
    "action_yml_files",
    multiple=True,
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="action.yml files to update (can be repeated)",
)
@click.option(
    "--precommit-config",
    "precommit_configs",
    multiple=True,
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Pre-commit config files to update (can be repeated)",
)
def update_dependencies(
    dry_run: bool,
    pyproject_files: tuple[Path, ...],
    action_yml_files: tuple[Path, ...],
    precommit_configs: tuple[Path, ...],
) -> None:
    """Update all dependencies to their latest versions."""
    total = 0
    total += PyprojectTomlUpdater(list(pyproject_files)).update(dry_run=dry_run)
    total += ActionYmlUpdater(list(action_yml_files)).update(dry_run=dry_run)
    for config in precommit_configs:
        total += PreCommitConfigUpdater(config).update(dry_run=dry_run)

    if dry_run:
        click.echo(f"\nDry run complete. {total} update(s) would be applied.")
    else:
        click.echo(f"\nDone. {total} update(s) applied.")


if __name__ == "__main__":
    cli()
