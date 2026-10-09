"""
This tool extends upstream mypy_primer to check downstream projects: code that uses
our DRF stubs, such as Sentry. A worker subprocess runs mypy twice on each project,
using the baseline (old stubs/plugin) and the new sources. WORKTREE selects local
files, including uncommitted changes; a Git revision selects committed sources.

Mypy runs in checker virtualenvs, separate from the project's own virtualenv of
installed dependencies. Both checks use the same mypy version, latest project
checkout, and project dependencies. We diff their diagnostics (reported errors and
notes) to show which were added or removed by changing our stubs/plugin.

--projects=NAME,... selects consumers and infers Python; omitted means all consumers.
--python=VERSION selects projects assigned to that Python version (CI).

## Comparison

Default: merge-base(HEAD, origin/HEAD) -> WORKTREE, including uncommitted changes.
COMMIT: first parent -> COMMIT. A..B: A -> B. A...B: merge-base(A, B) -> B.
WORKTREE may replace the new endpoint; committed endpoints use detached worktrees.

## Output

Diff of mypy results to stdout; diagnostics and resolved revisions go to stderr.
Exit 0: identical mypy results; 1: mypy differences; 70: errors.

## Execution
run_primer.py
    |       Resolve old/new sources; group projects by Python.
    v
uv run --locked --python=VERSION --only-group=primer
    |       Install locked primer deps in a temporary runner venv, once per Python group.
    v
primer_internal.py --run-primer
    |       Import project definitions; install checker hooks.
    v
upstream mypy_primer
    |       Clone latest project head; create its dependency venv.
    +--> primer_internal.py --prepare-project=NAME --install=COMMAND
    |       Custom setup only, before checks; installer targets the project's venv.
    |       Python subprocesses use the project's interpreter, not necessarily the helper's.
    |
    v
mypy(old sources) + mypy(new sources)
    |       Separate checker venvs; same locked mypy/project/deps.
    |       Only the selected DRF stubs/plugin sources differ.
    v
diagnostic diff -> stdout
    |       Progress, full diagnostics, and project SHAs -> stderr.
    v
cleanup

"""

from __future__ import annotations

import argparse
import os
import re
import shlex
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator

    from mypy_primer.model import Project  # type: ignore[import-not-found]

ROOT = Path(__file__).resolve().parent.parent
# Runner choices, not compatibility floors: some consumers also have upper bounds.
PYTHON_PROJECTS: dict[str, tuple[str, ...]] = {
    "3.12": ("lidotiku",),
    "3.13": ("sentry", "django-polymorphic", "djangorestframework-dataclasses", "django-seriously"),
    "3.14": ("cookiecutter-django",),
}


def get_projects() -> list[Project]:
    from mypy_primer.model import Project

    helper = shlex.quote(str(Path(__file__).with_name("primer_internal.py").resolve()))

    def preparation(name: str) -> str:
        return f'python {helper} --prepare-project={name} --install="{{install}}"'

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
            mypy_cmd=("cd generated/primer_project && DATABASE_URL=sqlite:///:memory: {mypy} primer_project"),
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
        # Settings force the PostGIS backend; a SQLite URL would not switch engines.
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


def command_output(command: list[str]) -> str:
    return subprocess.check_output(command, cwd=ROOT, text=True, stderr=subprocess.PIPE).strip()


@contextmanager
def source_path(revision: str, path: Path) -> Iterator[Path]:
    """Use live sources or a temporary checkout removed when leaving the scope."""
    if revision == "WORKTREE":
        yield ROOT
        return
    command_output(["git", "worktree", "add", "--detach", str(path), revision])
    try:
        yield path
    finally:
        command_output(["git", "worktree", "remove", "--force", str(path)])


def resolve_comparison(revision: str | None) -> tuple[str, str]:
    def commit(ref: str) -> str:
        return command_output(["git", "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}"])

    if revision is None or revision == "WORKTREE":
        return command_output(["git", "merge-base", "HEAD", "origin/HEAD"]), "WORKTREE"
    if ".." not in revision:
        new = commit(revision)
        return commit(f"{new}^1"), new
    separator = "..." if "..." in revision else ".."
    parts = revision.split(separator)
    if len(parts) != 2 or parts[0] == "WORKTREE":
        raise ValueError("Expected COMMIT, A..B, or A...B; WORKTREE is only valid as the new endpoint")
    old = commit(parts[0] or "HEAD")
    new = "WORKTREE" if parts[1] == "WORKTREE" else commit(parts[1] or "HEAD")
    if separator == "...":
        old = command_output(["git", "merge-base", old, "HEAD" if new == "WORKTREE" else new])
    return old, new


def select_groups(python: str | None, projects: str | None) -> dict[str, tuple[str, ...]]:
    available = PYTHON_PROJECTS
    requested = None if projects is None else {name.strip() for name in projects.split(",")}
    if requested is not None:
        if "" in requested:
            raise ValueError("--projects requires comma-separated project names")
        unknown = requested - {name for names in available.values() for name in names}
        if unknown:
            raise ValueError(f"Unknown projects: {', '.join(sorted(unknown))}")
    groups = {}
    for version, names in available.items():
        if python is not None and python != version:
            continue
        selected = names if requested is None else tuple(name for name in names if name in requested)
        if selected:
            groups[version] = selected
    if requested is not None:
        excluded = requested - {name for names in groups.values() for name in names}
        if excluded:
            raise ValueError(f"Projects unavailable with --python={python}: {', '.join(sorted(excluded))}")
    return groups


def locked_mypy_version() -> str:
    version_output = command_output(["uv", "tree", "--locked", "--package=mypy", "--depth=0", "-q"])
    match = re.fullmatch(r"mypy v(\d+\.\d+\.\d+)", version_output)
    if match is None:
        raise ValueError(f"Unexpected locked mypy version: {version_output!r}")
    return match[1]


def compare(old: str, new: str, *, groups: dict[str, tuple[str, ...]], dry_run: bool) -> int:
    version = locked_mypy_version()
    local = ROOT / "_local"
    local.mkdir(exist_ok=True)
    print(f"Comparing {old}..{new} with mypy {version}", file=sys.stderr, flush=True)
    if new == "WORKTREE":
        print(f"Working tree HEAD: {command_output(['git', 'rev-parse', 'HEAD'])}", file=sys.stderr)
    status = 0
    with (
        tempfile.TemporaryDirectory(prefix="primer-work-", dir=local) as temporary,
        source_path(old, Path(temporary) / "old") as old_path,
        source_path(new, Path(temporary) / "new") as new_path,
    ):
        workspace = Path(temporary)
        for group_python, projects in groups.items():
            selector = "|".join(re.escape(project) for project in projects)
            command = [
                "uv",
                "run",
                "--locked",
                "--only-group=primer",
                f"--python={group_python}",
                "python",
                "-u",
                str(Path(__file__).with_name("primer_internal.py").resolve()),
                "--run-primer",
                f"--new={version}",
                f"--old={version}",
                "--known-dependency-selector=djangorestframework-stubs",
                f"--project-selector={selector}",
                f"--old-prepend-path={old_path}",
                f"--new-prepend-path={new_path}",
                f"--base-dir={workspace}/work-{group_python}",
                "--output=concise",
                "--debug",
                "--concurrency=2",
            ]
            environment = {**os.environ, "UV_PROJECT_ENVIRONMENT": str(workspace / f"runner-{group_python}")}
            print(f"Python {group_python}: {shlex.join(command)}", file=sys.stderr, flush=True)
            if dry_run:
                continue
            result = subprocess.run(command, cwd=ROOT, env=environment)
            status = 70 if result.returncode not in (0, 1) else max(status, result.returncode)
            print(f"Python {group_python}: exit {result.returncode}", file=sys.stderr, flush=True)
    if dry_run:
        print("Dry run complete: no consumer comparisons were run.", file=sys.stderr)
    elif status == 70:
        print("Comparison incomplete; see diagnostics above.", file=sys.stderr)
    else:
        print("Diagnostic differences." if status else "No diagnostic differences.", file=sys.stderr)
    return status


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    known_projects = ", ".join(sorted(name for names in PYTHON_PROJECTS.values() for name in names))
    parser.add_argument("revision", nargs="?", help="COMMIT, A..B, or A...B; B may be WORKTREE")
    parser.add_argument(
        "--projects",
        metavar="NAME,...",
        help=f"Comma-separated names; Python versions are automatic. Known projects: {known_projects}",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Resolve/check out sources and print commands without running primer"
    )
    parser.add_argument_group("CI").add_argument(
        "--python", choices=PYTHON_PROJECTS, help="Only check projects assigned to this Python version (for CI)"
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        groups = select_groups(args.python, args.projects)
    except ValueError as error:
        parser.error(str(error))
    try:
        old, new = resolve_comparison(args.revision)
        return compare(old, new, groups=groups, dry_run=args.dry_run)
    except subprocess.CalledProcessError as error:
        print(f"Command failed: {shlex.join(error.cmd)}", file=sys.stderr)
        if error.stderr:
            print(error.stderr, file=sys.stderr)
        return 70
    except (OSError, ValueError) as error:
        print(error, file=sys.stderr)
        return 70


if __name__ == "__main__":
    sys.exit(main())
