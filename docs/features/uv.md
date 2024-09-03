# Dependency management with uv

The generated repository will uses [uv](https://docs.astral.sh/uv/)
for its dependency management. When you have created your repository
using this cookiecutter template, a uv environment is pre-configured
in `pyproject.toml`. All you need to do is add your
project-specific dependencies with

```bash
uv add <package>
```

and then install the environment with

```bash
uv sync
```

You can then run commands within your virtual environment, for example:

```bash
uv run python -m pytest
```
