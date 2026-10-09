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

Consumer definitions and the Python-to-project mapping live in `scripts/run_primer.py`.
Each run checks the latest consumer default-branch heads, recording their resolved SHAs.
Both mypy checks share each consumer's checkout and installed dependencies; only the DRF
stubs/plugin source changes. Consumers use Linux and separate Python groups because their
supported versions do not overlap.

The public CLI starts `scripts/primer_internal.py --run-primer` in each selected Python's
primer environment. That subprocess imports the public project definitions, installs our
hooks, and runs upstream primer. For custom setup, primer invokes
`primer_internal.py --prepare-project=NAME --install=COMMAND` from the project checkout,
before either mypy check. The supplied installer targets the project's virtualenv;
the helper itself need not run in that environment. Exactly one internal mode is required;
preparation does not require primer to be installed.

Cookiecutter uses an in-memory SQLite database URL for Django settings initialization.
Lidotiku keeps its PostGIS URL because its settings explicitly force that backend.

Run from this repository's root on Linux with [uv](https://docs.astral.sh/uv/).
On Debian/Ubuntu, first install the native consumer dependencies:

```bash
sudo apt-get update
sudo apt-get install -y libpq-dev libgdal-dev libgeos-dev
```

Use the same entry point locally and in CI:

```bash
# Compare with the default branch, including uncommitted changes
uv run --no-project python scripts/run_primer.py

# Focus on selected projects; their Python versions are chosen automatically
uv run --no-project python scripts/run_primer.py --projects=sentry,lidotiku

# Explicit baseline, with either live or committed new sources
uv run --no-project python scripts/run_primer.py A..WORKTREE
uv run --no-project python scripts/run_primer.py A..HEAD
```

With no revision argument, the baseline is `git merge-base HEAD origin/HEAD` and the new
source is the current working tree. Local refs are used without automatically fetching.
`COMMIT` compares its first parent to that commit; `A..B` compares exact endpoints;
`A...B` compares their merge base to B. `WORKTREE` may replace the new endpoint and includes
uncommitted changes. Add `--dry-run` to resolve/check out sources and print commands without
running consumer comparisons. Package dependency metadata is not compared.

The current checkout supplies the consumer registry and exact mypy version from `uv.lock`.
The non-default `primer` dependency group pins primer and locks its dependencies.
The launcher uses uv to select each project's Python and install only this group in isolated
runner environments, without installing primer into the default development environment.
Temporary worktrees, environments, and consumer clones under `_local/` are removed afterward;
uv's package-download cache remains reusable.

Colored diagnostic diffs stream to stdout as each consumer comparison completes.
Commands, progress, full checker diagnostics, and consumer SHAs go to stderr. No result
files are written automatically; redirect stdout to save the diff:

```bash
mkdir -p _local
uv run --no-project python scripts/run_primer.py A..WORKTREE > _local/primer.diff
```

Exit codes: `0` means identical diagnostics, `1` means differences, and `70` means an
operational failure. Existing consumer errors are fine: the comparison reports changes,
not whether either checker run was error-free.

CI derives its matrix from `scripts/run_primer.py` and selects projects assigned to one Python version per job:

```bash
uv run --no-project python scripts/run_primer.py \
  "$TESTED_BASE..WORKTREE" --python="$PYTHON_VERSION"
```

The checked-out PR sources serve as the new side; only the baseline needs a worktree.
`--python` only checks projects assigned to that Python version, and is not needed locally.
Explicitly selected projects assigned to another version are rejected rather than silently skipped.

The runner extends pinned upstream internal APIs to select our registry, prepend the matching
checkout in both checker environments, log consumer SHAs, and retain operational failures.
When updating the `primer` dependency group or consumer definitions, review the
[pinned upstream implementation](https://github.com/hauntsaninja/mypy_primer/tree/0bb419028b53bceb57c136094e7a9df1444e7241/mypy_primer)
and rerun the configured consumers, an identical-checkout comparison, and deliberate stub/plugin
change comparisons. Sentry uses its upstream development configuration; Cookiecutter runs its
normal generation hooks and then normalizes fixture credentials for reproducible generated source.
**Never deploy the generated primer project:** its credentials are deliberately predictable.
Existing consumer diagnostics are expected unless an entry explicitly sets `expected_success`.
After changing the primer dependency, regenerate `uv.lock` with `uv lock` and commit both
`pyproject.toml` and `uv.lock`.
