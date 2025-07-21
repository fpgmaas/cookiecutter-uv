# Publishing to PyPI

## Releasing from Github

Depending on `publish_python_package` value, `on-release-main.yml` workflow publishes the code to different locations whenever a [new release](./cicd.md#how-to-trigger-a-release) is made.
- pypi
  - [PyPI](https://pypi.org) 
- azure_artifacts
  - [Azure Artifacts](https://azure.microsoft.com/en-us/products/devops/artifacts)
- None
  - Doesn't publish

Before you can succesfully publish your project from the release workflow, you need to add some secrets to your github repository so
they can be used as environment variables.

## Set-up for PyPI

In order to publish to PyPI, the secret `PYPI_TOKEN` should be set in
your repository. In your Github repository, navigate to
`Settings > Secrets > Actions` and press `New repository secret`. As the
name of the secret, set `PYPI_TOKEN`. Then, in a new tab go to your
[PyPI Account settings](https://pypi.org/manage/account/) and select
`Add API token`. Copy and paste the token in the `Value`
field for the Github secret in your first tab, and you're all set!

## Publishing from your local machine

It is also possible to release locally, although it is not recommended.
To do so, run:

```bash
make build-and-publish
```
