"""Command-line interface."""

import fire

from {{cookiecutter.project_slug}}.base import Base


def main():
    """Main entry point for the {{cookiecutter.project_name}} command line."""
    fire.Fire(Base)


if __name__ == "__main__":
    main()
