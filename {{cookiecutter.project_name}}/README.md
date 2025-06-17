# {{cookiecutter.project_name}}

[![Release](https://img.shields.io/github/v/release/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}})](https://img.shields.io/github/v/release/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}})
[![Build status](https://img.shields.io/github/actions/workflow/status/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/main.yml?branch=main)](https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/branch/main/graph/badge.svg)](https://codecov.io/gh/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}})
[![Commit activity](https://img.shields.io/github/commit-activity/m/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}})](https://img.shields.io/github/commit-activity/m/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}})
[![License](https://img.shields.io/github/license/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}})](https://img.shields.io/github/license/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}})

{{cookiecutter.project_description}}

- **Github repository**: <https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/>
- **Documentation** <https://{{cookiecutter.author_github_handle}}.github.io/{{cookiecutter.project_name}}/>

## Getting started with your project

### 1. Create a New Repository

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}.git
git push -u origin main
```

### 2. Set Up Your Development Environment

Then, install the environment and the pre-commit hooks with

```bash
make install
```

This will also generate your `uv.lock` file

### 3. Verification

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

### 4. Run the pre-commit hooks

Initially, the CI/CD pipeline might be failing due to formatting issues. To resolve those run:

```bash
uv run pre-commit run -a
```

### 5. Commit the changes

Lastly, commit the changes made by the two steps above to your repository.

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

To finalize the set-up for publishing to PyPI, see [here](https://foreveryounggithub.github.io/cookiecutter-pytorch-lightning/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see [here](https://foreveryounggithub.github.io/cookiecutter-pytorch-lightning/features/mkdocs/#enabling-the-documentation-on-github).
To enable the code coverage reports, see [here](https://foreveryounggithub.github.io/cookiecutter-pytorch-lightning/features/codecov/).

## Releasing a new version

{% if cookiecutter.publish_to_pypi == "y" -%}

- Create an API Token on [PyPI](https://pypi.org/).
- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting [this page](https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/settings/secrets/actions/new).
- Create a [new release](https://github.com/{{cookiecutter.author_github_handle}}/{{cookiecutter.project_name}}/releases/new) on Github.
- Create a new tag in the form `*.*.*`.

For more details, see [here](https://foreveryounggithub.github.io/cookiecutter-pytorch-lightning/features/cicd/#how-to-trigger-a-release).
{%- endif %}

---

Repository initiated with [foreverYoungGitHub/cookiecutter-pytorch-lightning](https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning).
