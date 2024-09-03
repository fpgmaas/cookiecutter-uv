from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path

import yaml


def is_valid_yaml(path: str | Path):
    path = Path(path)

    if not path.is_file():
        print(f"File does not exist: {path}")
        return False

    try:
        with path.open("r") as file:
            yaml.safe_load(file)
    except yaml.YAMLError as e:
        print(f"Invalid YAML file: {path} - Error: {e}")
        return False
    except OSError as e:
        print(f"Error reading file: {path} - Error: {e}")
        return False

    return True


@contextmanager
def run_within_dir(path: str):
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)


def file_contains_text(file: str, text: str) -> bool:
    with open(file) as f:
        return f.read().find(text) != -1
