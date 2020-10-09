# How to contribute

## Tutorials

If you want to start working on this project,
you will need to get familiar with these projects:

- [Django docs](https://docs.djangoproject.com/en/dev/)
- [Typing in Python](https://inventwithpython.com/blog/2019/11/24/type-hints-for-busy-python-programmers/)

It is also recommended to take a look at these resources:

- [How to write custom mypy plugins](https://mypy.readthedocs.io/en/stable/extending_mypy.html)
- [Typechecking Django and DRF](https://sobolevn.me/2019/08/typechecking-django-and-drf) guide
- [Testing mypy stubs, plugins, and types](https://sobolevn.me/2019/08/testing-mypy-types) guide
- [Awesome Python Typing](https://github.com/typeddjango/awesome-python-typing)

## Dev setup

As a first step you will need to install pre-commit globally (see [this guide](https://codeburst.io/tool-your-django-project-pre-commit-hooks-e1799d84551f) for more info), and then run in the repos root the command:

```bash
pre-commit install
```

You will then need to create and activate a git ignored virtual env, e.g.:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

After doing this you can install the dev requirements:

```bash
pip install -r ./dev-requirements.txt
```

## Tests and linters

We use `mypy`, `pytest`, `flake8`, and `black` for quality control.
Here's [how we run our CI](https://github.com/typeddjango/django-stubs/blob/master/.travis.yml).

### Typechecking

To run typechecking use:

```bash
mypy ./mypy_drf_plugin
```

### Testing

To run unit tests:

```bash
pytest
```

To ensure there are not formatting or typing issues in the entire repository you can afterwards run:

```bash
pre-commit run --all-files
```

This command will not only lint but also modify files - so make sure to commit whatever changes you've made before hand.

## Submitting your code

We use [trunk based](https://trunkbaseddevelopment.com/)
development (we also sometimes call it `wemake-git-flow`).

What the point of this method?

1. We use protected `master` branch,
   so the only way to push your code is via pull request
2. We use issue branches: to implement a new feature or to fix a bug
   create a new branch named `issue-$TASKNUMBER`
3. Then create a pull request to `master` branch
4. We use `git tag`s to make releases, so we can track what has changed
   since the latest release

So, this way we achieve an easy and scalable development process
which frees us from merging hell and long-living branches.

In this method, the latest version of the app is always in the `master` branch.

## Other help

You can contribute by spreading a word about this library.
It would also be a huge contribution to write
a short article on how you are using this project.
You can also share your best practices with us.

