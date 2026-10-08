# General

Python type stubs for Django REST Framework (DRF) for mypy, pyright, ty, etc.
Match DRF runtime behavior.

- `rest_framework-stubs/**.pyi` stubs
- `mypy_drf_plugin/`: plugin for mypy that affects `Serializer.Meta`

## Pull requests

Keep descriptions concise.
Link supporting upstream code or API docs when possible.

## Finding upstream source

ALWAYS VERIFY changes against upstream implementation source.
Run `uv sync`, then sources are in `.venv/lib/python*/site-packages/{rest_framework,django,django-stubs}`

## Docs

Consult upstream docs for examples or when intent is not perfectly clear.
Clone missing repositories into `_local/`:

- DRF `git clone -q --depth=1 https://github.com/encode/django-rest-framework _local/drf`
- Django `git clone -q --depth=1 https://github.com/django/django _local/django`
- Typing specification - for complex type constructs:
  `git clone -q --depth=1 https://github.com/python/typing _local/typing`

## Tests

Prefer extending existing tests.
Create temporary tests for basic stub changes.
Commit tests only for complex typing:
- Generics, decorators, protocols, overloads
- Fixing nontrivial bugs
- django-stubs integration

Run `uv run mypy tests && uv run pytest`

- `tests/assert_type/*.py`: Preferred; must type-check without errors.
- `tests/typecheck/*.yml`: Use only when plain Python tests are insufficient,
  e.g. expected diagnostics or plugin behavior.

## Validation

`uv run scripts/stubtest.sh` compares stubs with runtime symbols.
When stubtest is wrong, allowlist with a comment explaining why:
`scripts/stubtest/allowlist.txt`

Before committing, install Ruff format/lint hooks:
`PRE_COMMIT_USE_UV=1 uv run pre-commit install`
