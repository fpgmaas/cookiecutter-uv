# Linting and code quality

Code can be linted and quality-checked with the command

```bash
make check
```

Note that this requires the pre-commit hooks to be installed.

This command will run the following tools:

## ruff

[ruff](https://github.com/charliermarsh/ruff) is used to lint and format the code, and it is configured through `pyproject.toml`:

```
[tool.ruff]
target-version = "py39"
line-length = 120
fix = true
select = [
    # flake8-2020
    "YTT",
    # flake8-bandit
    "S",
    # flake8-bugbear
    "B",
    # flake8-builtins
    "A",
    # flake8-comprehensions
    "C4",
    # flake8-debugger
    "T10",
    # flake8-simplify
    "SIM",
    # isort
    "I",
    # mccabe
    "C90",
    # pycodestyle
    "E", "W",
    # pyflakes
    "F",
    # pygrep-hooks
    "PGH",
    # pyupgrade
    "UP",
    # ruff
    "RUF",
    # tryceratops
    "TRY",
]
ignore = [
    # LineTooLong
    "E501",
    # DoNotAssignLambda
    "E731",
]

[tool.ruff.format]
preview = true

[tool.ruff.per-file-ignores]
"tests/*" = ["S101"]
```

## mypy

[mypy](https://mypy.readthedocs.io/en/stable/) is used for static type checking, and it's configuration can be edited in `pyproject.toml`.

```toml
[tool.mypy]
disallow_untyped_defs = true
disallow_any_unimported = true
no_implicit_optional = true
check_untyped_defs = true
warn_return_any = true
warn_unused_ignores = true
show_error_codes = true
exclude = [
    '\.venv',
    '{{cookiecutter.project_name}}',
    'tests'
]
```

## ty

[ty](https://docs.astral.sh/ty/) is an extremely fast type checker (and language server) that can be used instead of mypy, and it's configuration can be edited in `pyproject.toml`.

```toml
[tool.ty.environment]
python = "./.venv"
python-version = "3.9"
```

## deptry

[deptry](https://github.com/fpgmaas/deptry) is used to check the code for dependency issues, and it can be configured by adding a `[tool.deptry]` section in `pyproject.toml`. For more information, see [this section](https://deptry.com/usage/#configuration) documentation of deptry.

## Github Actions

If `include_github_actions` is set to `"y"`, code formatting is checked
for every merge request, every merge to main, and every release.
