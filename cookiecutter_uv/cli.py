from __future__ import annotations

import os
import sys
from pathlib import Path


def main() -> None:
    package_dir = Path(__file__).parent.parent.absolute()
    try:
        os.system(f"cookiecutter {package_dir}")  # noqa: S605 | No injection, retrieving path in OS
    except KeyboardInterrupt:
        sys.exit(0)
