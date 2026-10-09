<img src="https://mypy-lang.org/static/mypy_light.svg" alt="mypy logo" width="300px"/>

# pep484 stubs for Django REST framework

[![test](https://github.com/typeddjango/djangorestframework-stubs/actions/workflows/test.yml/badge.svg?branch=master&event=push)](https://github.com/typeddjango/djangorestframework-stubs/actions/workflows/test.yml)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![Gitter](https://badges.gitter.im/mypy-django/Lobby.svg)](https://gitter.im/mypy-django/Lobby)
[![StackOverflow](https://shields.io/badge/ask-stackoverflow-orange?logo=stackoverflow)](https://stackoverflow.com/questions/tagged/django-stubs?tab=Active)


Mypy stubs for [Django REST Framework](https://pypi.org/project/djangorestframework/).
Supports Python 3.11 and up.

## Installation

```bash
pip install djangorestframework-stubs[compatible-mypy]
```

To make mypy aware of the plugin, you need to add

```ini
[mypy]
plugins =
    mypy_drf_plugin.main
```

in your `mypy.ini` file.

## FAQ

### Model instance is inferred as `Any` instead of my `Model` class

When subclassing `ModelSerializer`, add a [type argument](https://peps.python.org/pep-0484/#generics) to type-hint the related model class, for example:

```python
class MyModelSerializer(serializers.ModelSerializer[MyModel]):
    class Meta:
        model = MyModel
        fields = ("id", "example")
```

Which means that methods where the model is being passed around will know the actual type of the model instead of being `Any`. The `instance` attribute on the above serializer will be `MyModel | typing.Sequence[MyModel] | None`.

## To get help

We have Gitter here: <https://gitter.im/mypy-django/Lobby>
If you think you have more generic typing issue, please refer to <https://github.com/python/mypy> and their Gitter.

## Contributing

This project is open source and community driven. As such we encourage contributions big and small. You can contribute by doing any of the following:

1. Contribute code (e.g. improve stubs, add plugin capabilities, write tests etc) - to do so please follow the [contribution guide](./CONTRIBUTING.md).
2. Assist in code reviews and discussions in issues.
3. Identify bugs and issues and report these

You can always also reach out in gitter to discuss your contributions!

### Consumer regression checks

PR CI uses [mypy_primer](https://github.com/hauntsaninja/mypy_primer) to compare the PR merge
commit's stubs **and plugin** with its target-branch merge base. Both runs use the exact mypy
version from the PR's `uv.lock` and share each consumer's installed dependencies.
Diagnostic differences are advisory; setup, plugin-import, and checker-internal failures fail
the job instead of appearing as an empty diff. Full comparisons and diagnostic logs are uploaded
as artifacts. A separate privileged workflow validates the current PR and tested revisions
before updating a comment; it never checks out PR code or extracts artifact archives.
The comment workflow must exist on the default branch before GitHub can trigger it.

Consumers and revisions live in `scripts/primer_projects.py`. They use Linux and three Python
groups because their supported versions do not overlap:

| Python | Consumers |
|---|---|
| 3.12 | Lidotiku |
| 3.13 | Sentry, django-polymorphic, djangorestframework-dataclasses, django-seriously |
| 3.14 | Cookiecutter Django (a generated project with DRF enabled) |

Run from this repository's root on Linux with [uv](https://docs.astral.sh/uv/).
On Debian/Ubuntu, first install the native consumer dependencies:

```bash
sudo apt-get update
sudo apt-get install -y libpq-dev libgdal-dev libgeos-dev
```

Create a baseline worktree at the merge base with the target branch (replace `origin/master`
if targeting another branch). Skip this step when comparing an existing checkout:

```bash
git fetch origin master
git worktree add --detach ../djangorestframework-stubs-base "$(git merge-base HEAD origin/master)"
```

The non-default `primer` dependency group in `pyproject.toml` pins the runner; `uv.lock` also
locks its transitive dependencies. `uv run --only-group primer` installs only this group, not
the package or default development dependencies. Use a separate runner environment per Python
group so concurrent runs cannot overwrite each other's interpreter or the development environment.
Resolve the checker version from this checkout's lockfile, then run the Python 3.13 group:

```bash
MYPY_VERSION=$(uv tree --locked --package=mypy --depth=0 -q)
MYPY_VERSION=${MYPY_VERSION#mypy v}
UV_PROJECT_ENVIRONMENT=_local/primer-runner-313 \
  uv run --locked --only-group primer --python 3.13 python scripts/run_mypy_primer.py \
  --new "$MYPY_VERSION" --old "$MYPY_VERSION" \
  --known-dependency-selector djangorestframework-stubs \
  --project-selector 'sentry|django-polymorphic|djangorestframework-dataclasses|django-seriously' \
  --old-prepend-path ../djangorestframework-stubs-base \
  --new-prepend-path . \
  --base-dir _local/primer-work-313 --output concise --debug -j 2
```

For Lidotiku, use `--python 3.12`, `--project-selector lidotiku`,
`UV_PROJECT_ENVIRONMENT=_local/primer-runner-312`, and `--base-dir _local/primer-work-312`;
for Cookiecutter, use `--python 3.14`, `--project-selector cookiecutter-django`,
`UV_PROJECT_ENVIRONMENT=_local/primer-runner-314`, and `--base-dir _local/primer-work-314`.
For a quick check, select only `djangorestframework-dataclasses` on Python 3.13.
For an identical-checkout smoke run, use `--old-prepend-path . --new-prepend-path .`.
The new path includes uncommitted source changes; package dependency metadata is not compared.

Exit codes: `0` means identical diagnostics, `1` means differences, and `70` means an operational
failure. Use separate work directories for concurrent Python groups. Repeated runs reuse uv's
download cache and refresh consumer clones, but recreate checker/consumer environments and caches.
Primer cleans and resets clones inside its work directory; never store your own edits there.
Prepend paths must point to checkout roots, not directly to `rest_framework-stubs/`.

The wrapper extends pinned upstream internal APIs to select our registry, prepend the matching
checkout in both checker environments, and retain operational failures. When updating
the `primer` dependency group in `pyproject.toml` or consumer revisions, review the
[pinned upstream implementation](https://github.com/hauntsaninja/mypy_primer/tree/0bb419028b53bceb57c136094e7a9df1444e7241/mypy_primer)
and rerun the configured consumers, an identical-checkout comparison, and deliberate stub/plugin
change comparisons. Sentry uses its upstream development configuration; Cookiecutter runs its
normal generation hooks and then normalizes fixture credentials for reproducible generated source.
**Never deploy the generated primer project:** its credentials are deliberately predictable.
Existing consumer diagnostics are expected unless an entry explicitly sets `expected_success`.
After changing the primer dependency, regenerate `uv.lock` with `uv lock` and commit both
`pyproject.toml` and `uv.lock`.
