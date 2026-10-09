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

To compare two local checkout roots, install the native dependencies (`libpq-dev`, `libgdal-dev`,
and `libgeos-dev` on Debian/Ubuntu), then run the appropriate group. For example:

```bash
uv venv --python 3.13 _local/primer-venv
uv pip install --python _local/primer-venv/bin/python -r scripts/mypy_primer_requirements.txt
uv tree --locked --package=mypy --depth=0 -q
# Use the exact version printed above for both --new and --old (currently 2.4.0).
_local/primer-venv/bin/python scripts/run_mypy_primer.py \
  --new 2.4.0 --old 2.4.0 \
  --known-dependency-selector djangorestframework-stubs \
  --project-selector 'sentry|django-polymorphic|djangorestframework-dataclasses|django-seriously' \
  --old-prepend-path ../djangorestframework-stubs-base \
  --new-prepend-path . \
  --base-dir _local/primer-work --output concise --debug
```

Exit codes: `0` means identical diagnostics, `1` means differences, and `70` means an operational
failure. Use separate work directories for concurrent Python groups. Prepend paths must point
to checkout roots, not directly to `rest_framework-stubs/`.

The wrapper extends pinned upstream internal APIs to select our registry, prepend the matching
checkout in both checker environments, and retain operational failures. When updating
`scripts/mypy_primer_requirements.txt` or consumer revisions, review the
[pinned upstream implementation](https://github.com/hauntsaninja/mypy_primer/tree/0bb419028b53bceb57c136094e7a9df1444e7241/mypy_primer)
and rerun the configured consumers, an identical-checkout comparison, and deliberate stub/plugin
change comparisons. Sentry uses its upstream development configuration; Cookiecutter runs its
normal generation hooks and then normalizes fixture credentials for reproducible generated source.
**Never deploy the generated primer project:** its credentials are deliberately predictable.
Existing consumer diagnostics are expected unless an entry explicitly sets `expected_success`.
