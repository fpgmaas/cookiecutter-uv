# Unittesting with Pytest

[pytest](https://docs.pytest.org/en/7.1.x/) is automatically added to
the environment. There will be a template unittest in the `tests`
directory upon creation of the project, which can be run with

```bash
make test
```

If `include_github_actions` is set to `"y"`, the tests are automatically
run for every merge request, every merge to main, and every release.
