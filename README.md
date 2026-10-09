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

### Downstream checks with mypy_primer

PR CI uses [mypy_primer](https://github.com/hauntsaninja/mypy_primer) to check how DRF
stub and plugin changes affect downstream projects. Diagnostic differences are advisory:
a separate workflow updates a PR comment with the diff, and full logs are available
in workflow artifacts. Commenting requires that workflow to be on the default branch.

Run manually from the repository root on Linux with [uv](https://docs.astral.sh/uv/)
installed. Native dependencies are also required: `libpq-dev`, `libgdal-dev`, and
`libgeos-dev` on Debian/Ubuntu.

```bash
python scripts/run_primer.py
python scripts/run_primer.py --projects=sentry,lidotiku
python scripts/run_primer.py --help
```

The default run compares your changes against origin, including uncommitted files.
See `--help` for revision ranges, project selection, and output options.
