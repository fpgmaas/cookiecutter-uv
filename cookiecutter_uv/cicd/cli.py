"""CLI for dependency updates."""

from __future__ import annotations

import logging

import click

from cookiecutter_uv.cicd.updaters import ActionYmlUpdater, PreCommitConfigUpdater, PyprojectTomlUpdater

logging.basicConfig(level=logging.INFO, format="%(message)s")


@click.group()
def cli() -> None:
    """CI/CD utilities for cookiecutter-uv."""


@cli.command()
@click.option("--dry-run", is_flag=True, help="Print changes without writing")
def update_dependencies(dry_run: bool) -> None:
    """Update all dependencies to their latest versions."""
    total = 0
    total += PyprojectTomlUpdater().update(dry_run=dry_run)
    total += ActionYmlUpdater().update(dry_run=dry_run)
    total += PreCommitConfigUpdater().update(dry_run=dry_run)

    if dry_run:
        click.echo(f"\nDry run complete. {total} update(s) would be applied.")
    else:
        click.echo(f"\nDone. {total} update(s) applied.")


if __name__ == "__main__":
    cli()
