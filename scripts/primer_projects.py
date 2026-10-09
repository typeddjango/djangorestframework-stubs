"""Latest DRF consumer default branches and their explicit runner Python groups."""

from __future__ import annotations

import json
import shlex
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mypy_primer.model import Project  # type: ignore[import-not-found]

# Runner choices, not compatibility floors: some consumers also have upper bounds.
PYTHON_PROJECTS: dict[str, tuple[str, ...]] = {
    "3.12": ("lidotiku",),
    "3.13": ("sentry", "django-polymorphic", "djangorestframework-dataclasses", "django-seriously"),
    "3.14": ("cookiecutter-django",),
}


def get_projects() -> list[Project]:
    from mypy_primer.model import Project

    helper = shlex.quote(str(Path(__file__).with_name("prepare_primer_project.py").resolve()))

    def preparation(name: str) -> str:
        return f'python {helper} {name} --install "{{install}}"'

    common = {"pyright_cmd": None, "needs_mypy_plugins": True, "supported_platforms": ["linux"]}
    return [
        Project(
            location="https://github.com/getsentry/sentry",
            mypy_cmd="SENTRY_CONF=primer-config PYTHONPATH=src:. {mypy} src/sentry/api --num-workers=0",
            install_cmd=preparation("sentry"),
            deps=["djangorestframework-stubs"],
            min_python_version=(3, 13),
            cost={"mypy": 74},
            **common,
        ),
        Project(
            location="https://github.com/cookiecutter/cookiecutter-django",
            mypy_cmd=(
                "cd generated/primer_project && DATABASE_URL=postgres://primer:primer@localhost/primer "
                "{mypy} primer_project"
            ),
            install_cmd=preparation("cookiecutter-django"),
            deps=["djangorestframework-stubs"],
            min_python_version=(3, 14),
            expected_success=("mypy",),
            cost={"mypy": 13},
            **common,
        ),
        Project(
            location="https://github.com/django-commons/django-polymorphic",
            mypy_cmd="PYTHONPATH=src:. {mypy} src/polymorphic",
            install_cmd=(
                "{install} -e . djangorestframework django-stubs django-stubs-ext django-filter django-extra-views"
            ),
            deps=["djangorestframework-stubs"],
            min_python_version=(3, 11),
            cost={"mypy": 8},
            **common,
        ),
        Project(
            location="https://github.com/oxan/djangorestframework-dataclasses",
            mypy_cmd="{mypy} -p rest_framework_dataclasses",
            install_cmd="{install} -e . django-stubs",
            deps=["djangorestframework-stubs"],
            cost={"mypy": 5},
            **common,
        ),
        Project(
            location="https://github.com/tfranzel/django-seriously",
            mypy_cmd="{mypy} django_seriously",
            install_cmd="{install} -e '.[schema]' django-stubs",
            deps=["djangorestframework-stubs"],
            min_python_version=(3, 12),
            cost={"mypy": 6},
            **common,
        ),
        Project(
            location="https://github.com/City-of-Helsinki/lidotiku",
            mypy_cmd="DATABASE_URL=postgis://primer:primer@localhost/primer SECRET_KEY=primer {mypy} api lidotiku",
            install_cmd=preparation("lidotiku"),
            deps=["djangorestframework-stubs"],
            min_python_version=(3, 12),
            cost={"mypy": 19},
            **common,
        ),
    ]


if __name__ == "__main__":
    print(json.dumps({"include": [{"python": version} for version in PYTHON_PROJECTS]}))
