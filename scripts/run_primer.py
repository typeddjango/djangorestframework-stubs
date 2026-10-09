"""
## Usage

Check how stubs changes affect downstream projects that use them.
The diff shows which mypy errors and notes are added or removed.

Run Python from this repository's root on Linux. uv is required internally;
see README for required system packages. No activated virtualenv is needed.

    python scripts/run_primer.py
    python scripts/run_primer.py --projects=sentry,lidotiku
    python scripts/run_primer.py <branch-name>
    python scripts/run_primer.py <commit>..<commit>

By default, checks your changes against origin, including uncommitted changes.
--projects selects which projects to check; omit it to check all configured projects.

A single REF checks its branch changes if unmerged into origin/HEAD; if already
merged, it checks that commit against its first parent. A..B compares exact endpoints;
A...B compares their common ancestor with B. WORKTREE means your current files.
Local Git refs are used without fetching. --dry-run prints commands without checking projects.

Diffs stream to stdout; [runner] status lines and check timings go to stderr.
Add --verbose for labeled full mypy results and setup commands. Failures always show diagnostics.
Redirect stdout to save the diff. Exit 0: identical results; 1: differences; 70: errors.

## How it works

The upstream mypy_primer tool clones projects, installs their dependencies, runs
mypy, and diffs its output. Our wrapper supplies the project definitions, Python
assignments, and old/new DRF sources, plus hooks for imports and diagnostic logging.
The current checkout supplies the pinned primer dependencies and exact mypy version
from uv.lock; the compared revisions select only the DRF stubs/plugin sources.
CI uses --python=VERSION to select projects assigned to one Python version.

The default baseline is git merge-base HEAD origin/HEAD; the new sources are WORKTREE.
For a single ref, git merge-base --is-ancestor REF origin/HEAD decides the baseline:
exit 0 selects REF's first parent; exit 1 selects the merge base with origin/HEAD.
Other exit codes are errors. Git ancestry cannot identify original branch refs
merged via squash/rebase.

Each project is checked twice against the same latest default-branch checkout and
installed dependencies. Mypy runs in two checker virtualenvs, separate from the
project's dependency virtualenv. Import hooks override the installed DRF stubs/plugin
with the selected old/new checkout. WORKTREE uses live files; committed sources use
temporary Git worktrees. Temporary checkouts and environments are removed afterward;
uv's download cache is retained.

run_primer.py
    |       Resolve old/new sources; group projects by Python.
    v
uv sync --locked --python=VERSION --only-group=primer
    |       Install locked primer deps in a temporary runner venv, once per Python group.
    v
primer_internal.py --run-primer
    |       Run in custom environment; import project definitions and install hooks.
    v
upstream mypy_primer
    |       Clone latest project head; create its dependency venv.
    |
    +--> primer_internal.py --prepare-project=NAME --install=COMMAND
    |       Custom setup only, before checks; installer targets the project's venv.
    |       Python subprocesses use the project's interpreter, not necessarily the helper's.
    |
    v
mypy(old sources) + mypy(new sources)
    |       Separate checker venvs; same locked mypy/project/deps.
    |       Only the selected DRF stubs/plugin sources differ.
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
# Runner choices, not compatibility floors: some projects also have upper bounds.
PYTHON_PROJECTS: dict[str, tuple[str, ...]] = {
    "3.12": ("lidotiku",),
    "3.13": ("sentry", "django-polymorphic", "djangorestframework-dataclasses", "django-seriously"),
    "3.14": ("cookiecutter-django",),
}


def get_projects() -> list[Project]:
    """Define the downstream projects primer checks against our DRF stubs."""
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
    """Resolve a revision or range into baseline and new-source comparison endpoints."""

    def commit(ref: str) -> str:
        return command_output(["git", "rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}"])

    if revision is None or revision == "WORKTREE":
        return command_output(["git", "merge-base", "HEAD", "origin/HEAD"]), "WORKTREE"
    if ".." not in revision:
        new = commit(revision)
        # Git ancestry, not PR status: squash/rebase merges may leave the original ref unreachable.
        ancestry = subprocess.run(
            ["git", "merge-base", "--is-ancestor", new, "origin/HEAD"],
            cwd=ROOT,
            text=True,
            stderr=subprocess.PIPE,
        )
        if ancestry.returncode == 1:
            return command_output(["git", "merge-base", new, "origin/HEAD"]), new
        # Exit 0 means merged; all nonzero statuses except 1 are operational errors.
        ancestry.check_returncode()
        return commit(f"{new}^1"), new
    separator = "..." if "..." in revision else ".."
    parts = revision.split(separator)
    if len(parts) != 2 or parts[0] == "WORKTREE":
        raise ValueError("Expected REF, A..B, or A...B; WORKTREE is only valid as the new endpoint")
    old = commit(parts[0] or "HEAD")
    new = "WORKTREE" if parts[1] == "WORKTREE" else commit(parts[1] or "HEAD")
    if separator == "...":
        old = command_output(["git", "merge-base", old, "HEAD" if new == "WORKTREE" else new])
    return old, new


def select_groups(python: str | None, projects: str | None) -> dict[str, tuple[str, ...]]:
    """Validate project selection and group projects by their assigned Python version."""
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


def log_status(message: str, *, kind: str = "info") -> None:
    """Print runner status separately from mypy output, coloring terminals unless NO_COLOR is set."""
    line = f"[runner] {message}"
    if sys.stderr.isatty() and "NO_COLOR" not in os.environ:
        color = {"info": "36", "success": "32", "warning": "33", "error": "31"}[kind]
        line = f"\033[1;{color}m{line}\033[0m"
    print(line, file=sys.stderr, flush=True)


def locked_mypy_version() -> str:
    """Read and validate the exact mypy version recorded in this repository's uv.lock."""
    version_output = command_output(["uv", "tree", "--locked", "--package=mypy", "--depth=0", "-q"])
    match = re.fullmatch(r"mypy v(\d+\.\d+\.\d+)", version_output)
    if match is None:
        raise ValueError(f"Unexpected locked mypy version: {version_output!r}")
    return match[1]


def compare(old: str, new: str, *, groups: dict[str, tuple[str, ...]], dry_run: bool, verbose: bool) -> int:
    """Compare selected projects in temporary environments, or print commands for a dry run."""
    version = locked_mypy_version()
    local = ROOT / "_local"
    local.mkdir(exist_ok=True)
    log_status(f"Comparing {old}..{new} with mypy {version}")
    if new == "WORKTREE":
        log_status(f"Working tree HEAD: {command_output(['git', 'rev-parse', 'HEAD'])}")
    status = 0
    with (
        tempfile.TemporaryDirectory(prefix="primer-work-", dir=local) as temporary,
        source_path(old, Path(temporary) / "old") as old_path,
        source_path(new, Path(temporary) / "new") as new_path,
    ):
        workspace = Path(temporary)
        for group_python, projects in groups.items():
            runner = workspace / f"runner-{group_python}"
            setup = ["uv", "sync", "--locked", "--only-group=primer", f"--python={group_python}"]
            selector = "|".join(re.escape(project) for project in projects)
            command = [
                str(runner / "bin" / "python"),
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
                "--concurrency=2",
            ]
            if verbose:
                command.append("--debug")
            else:
                setup.insert(1, "--quiet")
            environment = {**os.environ, "UV_PROJECT_ENVIRONMENT": str(runner)}
            log_status(f"Checking with Python {group_python}: {', '.join(projects)}")
            if verbose or dry_run:
                log_status(f"Command: {shlex.join(setup)}")
                log_status(f"Command: {shlex.join(command)}")
            if dry_run:
                continue
            # Sync separately: uv setup failures may exit 1, also primer's status for a diff.
            preparation = subprocess.run(setup, cwd=ROOT, env=environment)
            if preparation.returncode:
                status = 70
                log_status(
                    f"Python {group_python}: environment setup failed (exit {preparation.returncode})", kind="error"
                )
                continue
            result = subprocess.run(command, cwd=ROOT, env=environment)
            status = 70 if result.returncode not in (0, 1) else max(status, result.returncode)
            if result.returncode in (0, 1):
                summary = "diagnostic differences" if result.returncode else "no diagnostic differences"
                log_status(f"Python {group_python}: {summary}")
            else:
                log_status(f"Python {group_python}: comparison failed (exit {result.returncode})", kind="error")
    if dry_run:
        log_status("Dry run complete: no project comparisons were run.")
    elif status == 70:
        log_status("Comparison incomplete; see diagnostics above.", kind="error")
    else:
        log_status(
            "Diagnostic differences." if status else "No diagnostic differences.",
            kind="warning" if status else "success",
        )
    return status


def build_parser() -> argparse.ArgumentParser:
    """Build the public CLI using the user-facing section of the module docstring."""
    description = __doc__.split("\n## How it works\n", 1)[0] if __doc__ else None
    if description is not None:
        description = description.strip().removeprefix("## Usage").lstrip()
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    known_projects = ", ".join(sorted(name for names in PYTHON_PROJECTS.values() for name in names))
    parser.add_argument("revision", nargs="?", help="REF, A..B, or A...B; B may be WORKTREE")
    parser.add_argument(
        "--projects",
        metavar="NAME,...",
        help=f"Comma-separated names; Python versions are automatic. Known projects: {known_projects}",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Resolve/check out sources and print commands without running primer"
    )
    parser.add_argument("--verbose", action="store_true", help="Show setup commands and full old/new mypy output")
    parser.add_argument_group("CI").add_argument(
        "--python", choices=PYTHON_PROJECTS, help="Only check projects assigned to this Python version (for CI)"
    )
    return parser


def main() -> int:
    """Parse CLI args, run the comparison, and return its exit status."""
    parser = build_parser()
    args = parser.parse_args()
    try:
        groups = select_groups(args.python, args.projects)
    except ValueError as error:
        parser.error(str(error))
    try:
        old, new = resolve_comparison(args.revision)
        return compare(old, new, groups=groups, dry_run=args.dry_run, verbose=args.verbose)
    except subprocess.CalledProcessError as error:
        log_status(f"Command failed: {shlex.join(error.cmd)}", kind="error")
        if error.stderr:
            print(error.stderr, file=sys.stderr)
        return 70
    except (OSError, ValueError) as error:
        log_status(str(error), kind="error")
        return 70


if __name__ == "__main__":
    sys.exit(main())
