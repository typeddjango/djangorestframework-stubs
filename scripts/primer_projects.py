"""Real DRF consumers; revisions and Python groups are deliberately explicit."""

import shlex
from pathlib import Path

from mypy_primer.model import Project  # type: ignore[import-not-found]


def get_projects() -> list[Project]:
    helper = shlex.quote(str(Path(__file__).with_name("prepare_primer_project.py").resolve()))

    def preparation(name: str) -> str:
        return f'python {helper} {name} --install "{{install}}"'

    common = {"pyright_cmd": None, "needs_mypy_plugins": True, "supported_platforms": ["linux"]}
    return [
        Project(
            location="https://github.com/getsentry/sentry",
            revision="1930a929e210b123a4cc8d4e2558d7e71885f938",
            mypy_cmd="SENTRY_CONF=primer-config PYTHONPATH=src:. {mypy} src/sentry/api --num-workers=0",
            install_cmd=preparation("sentry"),
            deps=["djangorestframework-stubs"],
            min_python_version=(3, 13),
            cost={"mypy": 74},
            **common,
        ),
        Project(
            location="https://github.com/cookiecutter/cookiecutter-django",
            revision="4b9d477a18d507d6e51bb083b14bbfe585fde922",
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
            revision="324e755b8ff216b6c3bdc9c0c247cfeb387fce5c",
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
            revision="8371be49f16c884f073e1b8d61cd95bb97f4b781",
            mypy_cmd="{mypy} -p rest_framework_dataclasses",
            install_cmd="{install} -e . django-stubs",
            deps=["djangorestframework-stubs"],
            cost={"mypy": 5},
            **common,
        ),
        Project(
            location="https://github.com/tfranzel/django-seriously",
            revision="74ad70d58c3fe6646cca93d93ceafb6bb813d3b2",
            mypy_cmd="{mypy} django_seriously",
            install_cmd="{install} -e '.[schema]' django-stubs",
            deps=["djangorestframework-stubs"],
            min_python_version=(3, 12),
            cost={"mypy": 6},
            **common,
        ),
        Project(
            location="https://github.com/City-of-Helsinki/lidotiku",
            revision="e606999d18a2cf7bbe3b9f9e0b421f5e17dbc47f",
            mypy_cmd="DATABASE_URL=postgis://primer:primer@localhost/primer SECRET_KEY=primer {mypy} api lidotiku",
            install_cmd=preparation("lidotiku"),
            deps=["djangorestframework-stubs"],
            min_python_version=(3, 12),
            cost={"mypy": 19},
            **common,
        ),
    ]
