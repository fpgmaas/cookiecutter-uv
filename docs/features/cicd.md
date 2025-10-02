# CI/CD with Github actions

when `include_github_actions` is set to `"y"`, a `.github` directory is
added with the following structure:

    .github
    ├── workflows
    ├─── run-checks
    │    └── action.yml
    ├─── setup-python-env
    │    └── action.yml
    ├── on-merge-to-main.yml
    ├── on-pull-request.yml
    └── on-release-main.yml

`on-merge-to-main.yml` and `on-pull-request.yml` are identical except
for their trigger conditions; the first is run whenever a new commit is
made to `main` (which should
[only](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches)
happen through merge requests, hence the name), and the latter is run
whenever a pull request is opened or updated. They call the `action.yml`
files to set-up the environment, run the tests, and check the code
formatting.

`on-release-main.yml` does all of the former whenever a new release is
made on the `main` branch. In addition, `on-release-main.yml` also
publishes the project to PyPI if `publish_to_pypi` is set to
`"y"`, and it builds and deploys the documentation
if `mkdocs` is set to `"y"`. To learn more about these features,
see [Publishing to PyPI](./publishing.md) and [Documentation with MkDocs](./mkdocs.md)

Additionally, all workflows check for compatibility with multiple Python
versions if `tox` is set to `"y"`.

## How to trigger a release?

To trigger a new release, navigate to your repository on GitHub, click `Releases` on the right, and then select `Draft
a new release`. If you fail to find the button, you could also directly visit
`https://github.com/<username>/<repository-name>/releases/new`.

Give your release a title, and add a new tag in the form `*.*.*` where the
`*`'s are alphanumeric. To finish, press `Publish release`.
