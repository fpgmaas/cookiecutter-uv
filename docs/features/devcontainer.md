# Reproducible development environments with VSCode devcontainers

If `devcontainer` is set to `"y"` project uses the VSCode [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers)
specification to create a reproducible development environment. The devcontainer
is defined in the `.devcontainer` directory and pre-installs all dependencies
from uv required to develop, test and build the project.

The devcontainer also installs the pre-commit hooks and configures the VSCode python
extension to use the appropriate python interpretor and pytest paths.
