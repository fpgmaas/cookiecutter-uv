# Makefile

The generated repository will have a `Makefile` available. A list of all
available commands that are available can be obtained by running
`make help` in the terminal. Initially, if all features are selected, the following commands are
available:

```
install              Install the uv environment and install the pre-commit hooks
check                Lint and check code by running ruff, mypy and deptry.
test                 Test the code with pytest
build                Build wheel file using uv
clean-build          clean build artifacts
publish              publish a release to pypi.
build-and-publish    Build and publish.
docs-test            Test if documentation can be built without warnings or errors
docs                 Build and serve the documentation
```
