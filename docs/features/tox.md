# Compatibility testing with Tox

If `tox` is set to `"y"` project uses [tox-uv](https://github.com/tox-dev/tox-uv)
to test compatibility with multiple Python versions. You can run `tox` locally:

```sh
uv run tox
```

By default, the project is tested with Python `3.9`, `3.10`, `3.11`, `3.12` and `3.13`.

Testing for compatibility with different Python versions is also done automatically in the CI/CD pipeline on every pull request, merge
to main, and on each release.

If you want to test for compatbility with more Python versions you can simply add them to `tox.ini` and to the separate workflows in `.github`.
