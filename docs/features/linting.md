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

# Pyright

[Pyright](https://microsoft.github.io/pyright/) is used for static type checking. It's a fast, modern type checker created by Microsoft. Its configuration is in `pyproject.toml`:

```toml
[tool.pyright]
include = ["src"]
exclude = ["**/__pycache__", "build", "dist"]
defineConstant = {}
typeCheckingMode = "strict"
useLibraryCodeForTypes = true
reportMissingTypeStubs = "warning"
reportUnknownMemberType = "warning"
reportUnknownParameterType = "warning"
reportUnknownVariableType = "warning"
reportUnknownArgumentType = "warning"
reportPrivateUsage = "warning"
reportUntypedFunctionDecorator = "warning"
```

The configuration above enables strict type checking with helpful warnings for missing type information. You can customize these settings based on your project's needs. For more information about configuration options, see [Pyright's configuration documentation](https://microsoft.github.io/pyright/#/configuration).

# deptry

[deptry](https://github.com/fpgmaas/deptry) is used to check the code for dependency issues, and it can be configured by adding a `[tool.deptry]` section in `pyproject.toml`. For more information, see [this section](https://deptry.com/usage/#configuration) documentation of deptry.

# Black

[Black](https://black.readthedocs.io/) is used to format Python code files.
Its options can be configured in `pyproject.toml`:

```toml
[tool.black]
line-length = 120
target-version = ["py39"]
include = '\.pyi?$'
```

## Github Actions

If `include_github_actions` is set to `"y"`, code formatting is checked
for every merge request, every merge to main, and every release.
