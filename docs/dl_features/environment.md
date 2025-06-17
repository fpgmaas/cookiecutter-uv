# Setup Environment

This project uses [uv](https://docs.astral.sh/uv/) for dependency management and provides a streamlined setup process for deep learning development with PyTorch Lightning.

## Installation

### Option 1: Using Make (Recommended)

The project includes a convenient Makefile for setup:

```bash
make install
```

This command will:
- Create a virtual environment using uv
- Install all dependencies from `pyproject.toml`
- Set up pre-commit hooks for code quality

## Verification

To verify your installation is working correctly:

```bash
# Run code quality checks
make check

# Run tests
make test

# Check if PyTorch can detect your GPU (if available)
uv run python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"

# Try your first train with
uv run python -m {{cookiecutter.project_slug}}.scripts.train
```

Since it create the virtual environment using uv, please use uv run for all your python script like `uv run python` or just `source ./.venv/bin/activate` to enter the environment first and then run python command.

## Troubleshooting

### Common Issues

**uv not found**: Install uv using `curl -LsSf https://astral.sh/uv/install.sh | sh` or visit [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)

**CUDA version mismatch**: This should be handled by UV properly. But If you want to specific version, please check [using uv with PyTorch](https://docs.astral.sh/uv/guides/integration/pytorch/)

**Pre-commit hooks failing**: Run `uv run pre-commit install` and `uv run pre-commit run --all-files` to set up and test hooks.

For additional help, see the project's GitHub repository issues section.
