# General

Provides Python type stubs for Django REST Framework (DRF)
for type-checkers such as mypy, pyright, ty.
Stubs should model *runtime* behavior of DRF as closely as possible.

- `rest_framework-stubs/**.pyi` - type stub files corresponding to DRF modules
- `mypy_drf_plugin/` - minimal plugin for mypy; adds fallback to `Serializer.Meta` inner class fields.

## Pull requests

Keep descriptions concise.
Link upstream implementation or API documentation supporting the change when possible.

## Finding upstream source

When editing stubs, ALWAYS verify against actual implementation source.
Run `uv sync` and then see sources at `.venv/lib/python*/site-packages/`:

- `rest_framework/` - DRF runtime
- `django/` - Django runtime
- `django-stubs/` - `.pyi` files for Django

## Docs

Consult upstream docs for examples or when intent is not perfectly clear from source.
To access, clone repos into `_local/` if not already present:

- DRF `git clone -q --depth=1 https://github.com/encode/django-rest-framework _local/drf`
- Django `git clone -q --depth=1 https://github.com/django/django _local/django`
- Python type system details - verify for complex typing constructs:
  `git clone -q --depth=1 https://github.com/python/typing _local/typing`

## Tests

For *basic* stubs changes: DO create a test but don't commit it.

ONLY commit tests for complex cases:
- Generics, decorators, protocols, `@overload`
- When fixing nontrivial bugs
- Testing integration with django-stubs

Before adding a test, check if an existing related test can be improved.

Run with: `uv run mypy tests && uv run pytest`

Respectively:
- `tests/assert_type/*.py`: Preferred. Plain Python files scanned with type checker, must produce no type errors.
- `tests/typecheck/*.yml`: Slower mypy-specific pytest tests - ONLY if above is insufficient.
  e.g. ensure specific errors are raised or test plugin logic.

## Validation

Stubtest `uv run scripts/stubtest.sh` compares stubs to symbols available at Python runtime.
ONLY add exclusions when stubtest inference is wrong, with explaining comment: `scripts/stubtest/allowlist.txt`

Pre-commit hooks run Ruff formatter and linter.
Install before committing: `PRE_COMMIT_USE_UV=1 uv run pre-commit install`
