# Contribution Guide

This project is open source and community driven. As such we encourage code contributions of all kinds. Some areas you can contribute in:

1. Improve the stubs
2. Sync stubs with the latest version of the DRF
3. Improve plugin code and extend its capabilities
4. Write tests
5. Update dependencies
6. Fix and remove things from our `scripts/stubtest/allowlist_todo.txt`

Type stubs in `.pyi` files should follow
[coding conventions from typeshed project](https://github.com/python/typeshed/blob/main/CONTRIBUTING.md#conventions).

## Tutorials

If you want to start working on this project, you will need to get familiar with python typings.
The Mypy documentation offers an excellent resource for this, as well as the python official documentation:

- [Mypy typing documentation](https://mypy.readthedocs.io/en/stable/#overview-type-system-reference)
- [Python official typing documentation](https://docs.python.org/3/library/typing.html)
- [Typing in Python](https://inventwithpython.com/blog/2019/11/24/type-hints-for-busy-python-programmers/) article

Additionally, the following resources might be useful:

- [How to write custom mypy plugins](https://mypy.readthedocs.io/en/stable/extending_mypy.html)
- [Typechecking Django and DRF](https://sobolevn.me/2019/08/typechecking-django-and-drf) guide
- [Testing mypy stubs, plugins, and types](https://sobolevn.me/2019/08/testing-mypy-types) guide
- [Awesome Python Typing](https://github.com/typeddjango/awesome-python-typing) list

## Dev setup

### Repository Setup

As a first step you will need to fork this repository and clone your fork locally.
In order to be able to continously sync your fork with the origin repository's master branch, you will need to set up an upstream master.
To do so follow this [official github guide](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/syncing-a-fork).

### Dependency Setup

We use [uv](https://github.com/astral-sh/uv) to manage our dev dependencies.
To install it, see their [installation guide](https://docs.astral.sh/uv/getting-started/installation/)

Once it's done, simply run the following command to automatically setup a virtual environment and install dev dependencies:

```bash
uv sync
source .venv/bin/activate
```

Finally, install the pre-commit hooks:

```bash
pre-commit install
```

### Testing and Linting

We use `mypy`, `pytest`, `ruff`, and `black` for quality control. All tools except pytest are executed using pre-commit when you make a commit.
To ensure there are not formatting or typing issues in the entire repository you can run:

```bash
pre-commit run --all-files
```

NOTE: This command will not only lint but also modify files - so make sure to commit whatever changes you've made before hand.
You can also run pre-commit per file or for a specific path, simply replace "--all-files" with a target (see [this guide](https://codeburst.io/tool-your-django-project-pre-commit-hooks-e1799d84551f) for more info).

To execute the unit tests, simply run:

```bash
pytest
```

### Testing stubs with `stubtest`

Run `bash ./scripts/stubtest.sh` to test that stubs and sources are in-line.

We have two special files to allow errors:

1. `scripts/stubtest/allowlist.txt` where we store things that we really don't care about: hacks, DRF internal utility modules, things that are handled by our plugin, things that are not representable by type system, etc
2. `scripts/stubtest/allowlist_todo.txt` where we store all errors there are right now. Basically, this is a TODO list: we need to work through this list and fix things (or move entries to real `allowlist.txt`). In the end, ideally we can remove this file

You might also want to disable `incremental` mode while working on `stubtest` changes.
This mode leads to several known problems (stubs do not show up or have strange errors).

## Submission Guidelines

The workflow for contributions is fairly simple:

1. fork and setup the repository as in the previous step.
2. create a local branch.
3. make whatever changes you want to contribute.
4. ensure your contribution does not introduce linting issues or breaks the tests by linting and testing the code.
5. make a pull request with an adequate description.

## Releasing `djangorestframework-stubs`

1. Open a pull request that updates `pyproject.toml` (anyone can open this PR, not just maintainers):

   - Increase `version =` value within `[project]` section. Version number `major.minor.patch` is formed as follows:

     `major.minor` version must match newest supported `djangorestframework` release.

     `patch` is sequentially increasing for each stubs release. Reset to `0` if `major.minor` was updated.

   - Under `dependencies =`, update the `django-stubs>=` version to point to latest `django-stubs` release.
   - Update lockfile, run: `uv lock`
   - Use pull request title "Version x.y.z release" by convention.

2. Ensure the CI succeeds. A maintainer must merge this PR. If it's just a verison bump, no need
   to wait for a second maintainer's approval.

3. Maintainers need to [сreate a new GitHub release](https://github.com/typeddjango/djangorestframework-stubs/releases/new):

   - Under "Choose a tag" enter the new version number. Do NOT use `v` prefix.
   - Click "Generate release notes".
   - Delete all release notes lines containing `by @pre-commit-ci` or `by @renovate`, as these
     are irrelevant for our users.

4. Once you feel brave enough, click "Publish release".

5. Check that the [release workflow](https://github.com/typeddjango/djangorestframework-stubs/actions/workflows/release.yml) succeeds.
