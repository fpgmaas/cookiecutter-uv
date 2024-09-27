# Tutorial

This page contains a complete tutorial on how to create your project.

## Step 1: Install uv

To start, we will need to install `uv`. The instructions to install uv can be found
[here](https://docs.astral.sh/uv/#getting-started). For MacOS or Linux;

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Step 2: Generate your project

On your local machine, navigate to the directory in which you want to
create a project directory, and run the following command:

```bash
uvx cookiecutter https://github.com/fpgmaas/cookiecutter-uv.git
```

For an explanation of the prompt arguments, see
[Prompt Arguments](../prompt_arguments).

## Step 3: Set up your Github repository

Create an empty [new repository](https://github.com/new) on Github. Give
it a name that only contains alphanumeric characters and optionally `-`.
DO NOT check any boxes under the option `Initialize this repository
with`.

## Step 4: Upload your project to Github

Run the following commands, replacing `<project-name>` with the name
that you also gave the Github repository and `<github_author_handle>`
with your Github username.

```bash
cd <project_name>
git init -b main
git add .
git commit -m "Init commit"
git remote add origin git@github.com:<github_author_handle>/<project_name>.git
git push -u origin main
```

### Step 5: Set Up Your Development Environment

Initially, the CI/CD pipeline will fail for two reasons:

- The project does not yet contain a `uv.lock` file
- There are a few formatting issues in the project

To fix that, we first install the environment and the pre-commit hooks with:

```bash
make install
```

This will generate the `uv.lock` file

### Step 6: Run the pre-commit hooks

Now, to resolve the formatting issues, let's run the pre-commit hooks:

```bash
uv run pre-commit run -a
```

### 7. Commit the changes

Now we commit the changes made by the two steps above to the repository:

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

## Step 8: Sign up to codecov.io

If you enabled code coverage with codecov for your project, you should sign up with your GitHub account at [codecov.io](https://about.codecov.io/language/python/)

## Step 9: Configure your repository secrets

If you want to deploy your project to PyPI using the
Github Actions, you will have to set some repository secrets. For
instructions on how to do that, see [here](./features/publishing.md#set-up-for-pypi).

## Step 10: Enable your documentation

To enable your documentation on GitHub, first navigate to `Settings > Actions > General` in your repository, and under `Workflow permissions` select `Read and write permissions`.

## Step 11: Create a new release

To trigger a new release, navigate to your repository on GitHub, click `Releases` on the right, and then select `Draft
a new release`. If you fail to find the button, you could also directly visit
`https://github.com/<username>/<repository-name>/releases/new`.

Give your release a title, and add a new tag in the form `*.*.*` where the
`*`'s are alphanumeric. To finish, press `Publish release`.

## Step 12: Enable your documentation ct'd

Then navigate to `Settings > Code and Automation > Pages`. If you succesfully created a new release,
you should see a notification saying ` Your site is ready to be published at https://<author_github_handle>.github.io/<project_name>/`.

To finalize deploying your documentation, under `Source`, select the branch `gh-pages`.

## Step 12: You're all set!

That's it! I hope this repository saved you a lot of manual configuration. If you have any improvement suggestions, feel
free to raise an issue or open a PR on Github!
