<div align="center">

# Cookiecutter-Pytorch-Lightning <img width="50" src="https://raw.githubusercontent.com/foreverYoungGitHub/cookiecutter-pytorch-lightning/main/docs/static/cookiecutter.svg">

[![Build status](https://img.shields.io/github/actions/workflow/status/foreverYoungGitHub/cookiecutter-pytorch-lightning/main.yml?branch=main)](https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning/actions/workflows/main.yml?query=branch%3Amain)
[![Supported Python versions](https://img.shields.io/badge/python-3.9_%7C_3.10_%7C_3.11_%7C_3.12_%7C_3.13-blue?labelColor=grey&color=blue)](https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning/blob/main/pyproject.toml)
[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://foreveryounggithub.github.io/cookiecutter-pytorch-lightning/)
[![License](https://img.shields.io/github/license/foreverYoungGitHub/cookiecutter-pytorch-lightning)](https://img.shields.io/github/license/foreverYoungGitHub/cookiecutter-pytorch-lightning)

[![pytorch](https://img.shields.io/badge/PyTorch_2.6+-ee4c2c?logo=pytorch&logoColor=white)](https://pytorch.org/get-started/locally/)
[![lightning](https://img.shields.io/badge/-Lightning_2.4+-792ee5?logo=pytorchlightning&logoColor=white)](https://pytorchlightning.ai/)
[![hydra](https://img.shields.io/badge/Config-Hydra_1.3-89b8cd)](https://hydra.cc/)

</div>


---


This modern Cookiecutter template provides all the necessary tools for deep learning development, training, testing, and deployment. It supports the following features:

[Deep Learning related](https://foreveryounggithub.github.io/cookiecutter-pytorch-lightning/features/train/)
- [PyTorch](https://pytorch.org/) and [PyTorch Lightning](https://pytorchlightning.ai/) for deep learning framework
- [Hydra](https://hydra.cc/) for modular experiment configuration
- Optional experiment trackers: Tensorboard, W&B, Neptune, Comet, MLFlow and CSVLogger

[Python related](https://foreveryounggithub.github.io/cookiecutter-pytorch-lightning/features/cicd/)
- [uv](https://docs.astral.sh/uv/) for dependency management
- Supports both [src and flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/).
- CI/CD with [GitHub Actions](https://github.com/features/actions)
- Pre-commit hooks with [pre-commit](https://pre-commit.com/)
- Code quality with [ruff](https://github.com/charliermarsh/ruff), [mypy](https://mypy.readthedocs.io/en/stable/) and [deptry](https://github.com/fpgmaas/deptry/).
- Publishing to [PyPI](https://pypi.org) by creating a new release on GitHub
- Testing and coverage with [pytest](https://docs.pytest.org/en/7.1.x/) and [codecov](https://about.codecov.io/)
- Documentation with [MkDocs](https://www.mkdocs.org/)
- Compatibility testing for multiple versions of Python with [tox-uv](https://github.com/tox-dev/tox-uv)
- Containerization with [Docker](https://www.docker.com/) or [Podman](https://podman.io/)
- Development environment with [VSCode devcontainers](https://code.visualstudio.com/docs/devcontainers/containers)

---

<p align="center">
  <a href="https://foreveryounggithub.github.io/cookiecutter-pytorch-lightning/">Documentation</a> - <a href="https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning-example">Example</a>
</p>

---

## Quickstart

On your local machine, navigate to the directory in which you want to
create a project directory, and run the following command:

```bash
uvx cookiecutter https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning.git
```

or if you don't have `uv` installed yet:

```bash
pip install cookiecutter
cookiecutter https://github.com/foreverYoungGitHub/cookiecutter-pytorch-lightning.git
```

Follow the prompts to configure your project. Once completed, a new directory containing your project will be created. Then navigate into your newly created project directory and follow the instructions in the `README.md` to complete the setup of your project.

## Acknowledgements

This project is partially based on [Florian Maas](https://github.com/fpgmaas)\'s great
[cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv) and [Lukas](https://github.com/ashleve)\'s great [lightning-hydra-template](https://github.com/ashleve/lightning-hydra-template) repository.
