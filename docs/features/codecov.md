# Test coverage with codecov

If `codecov` is set to `"y"`, `pytest-cov` is added as a development dependency,
and `make test` will run the tests and output a coverage report as `coverage.xml`.
If `include_github_actions` is set to `"y"`, coverage tests with [codecov](https://about.codecov.io/) are added to the CI/CD pipeline. To enable this, sign up at [codecov.io](https://about.codecov.io/) with your GitHub account.
If codecov is configured to require token authentication for the upload, then follow the [instructions](https://docs.codecov.com/docs/codecov-tokens#types-of-tokens) for token generation and how to add it on your GitHub repository.
Additionally, a `codecov.yaml` file is created, with the following defaults:

```yaml
# Badge color changes from red to green between 70% and 100%
# PR pipeline fails if codecov falls with 1%

coverage:
  range: 70..100
  round: down
  precision: 1
  status:
    project:
      default:
        target: auto
        threshold: 1%

# Ignoring Paths
# --------------
# which folders/files to ignore
ignore:
  - "foo/bar.py"
```

If `codecov` is set to `"n"`, `pytest-cov` is not added to the development dependencies and the github actions won't produce a coverage report.
