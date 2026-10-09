"""
This tool extends upstream mypy_primer to check downstream projects: code that uses
our DRF stubs, such as Sentry. A worker subprocess runs mypy twice on each project,
using the baseline (old stubs/plugin) and the new sources. WORKTREE selects local
files, including uncommitted changes; a Git revision selects committed sources.

Mypy runs in checker virtualenvs, separate from the project's own virtualenv of
installed dependencies. Both checks use the same mypy version, latest project
checkout, and project dependencies. We diff their diagnostics (reported errors and
notes) to show which were added or removed by changing our stubs/plugin.

## Comparison

Default: merge-base(HEAD, origin/HEAD) -> WORKTREE, including uncommitted changes.
COMMIT: first parent -> COMMIT. A..B: A -> B. A...B: merge-base(A, B) -> B.
WORKTREE may replace the new endpoint; committed endpoints use detached worktrees.

## Execution

--projects=NAME,... selects consumers and infers Python; omitted means all consumers.
--python=VERSION restricts the group for CI matrix jobs.
uv uses pinned primer, locked mypy, and isolated temporary environments under _local/.

## Output

Colored diffs stream to stdout; diagnostics and resolved revisions go to stderr.
Exit 0: identical diagnostics; 1: differences; 70: operational failure.
"""

import argparse
import importlib
import os
import re
import shlex
import subprocess
import sys
import tempfile
import traceback
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
registry: Any = importlib.import_module(f"{__package__}.primer_projects" if __package__ else "primer_projects")
# Prepend the old/new checkout root to sys.path so mypy imports its DRF plugin,
# not the copy installed in the downstream project's virtualenv.
# language=python
PREPEND_PTH = """\
import os
import sys

prepend_path = os.environ.get("MYPY_PRIMER_PREPEND_PATH")
if prepend_path:
    sys.path[:0] = prepend_path.split(os.pathsep)
"""


def configure() -> Any:
    # The launcher is stdlib-only; optional primer dependencies are installed in the worker.
    import mypy_primer.main as primer  # type: ignore[import-not-found]
    import mypy_primer.model as model  # type: ignore[import-not-found]
    import mypy_primer.utils as utils  # type: ignore[import-not-found]

    upstream_setup = primer.setup_mypy
    upstream_run = model.run
    upstream_checkout = model.ensure_repo_at_revision

    async def setup_mypy(mypy_dir: Path, **kwargs: Any) -> Path:
        executable: Path = await upstream_setup(mypy_dir, **kwargs)
        site_packages = utils.Venv(mypy_dir / "venv").site_packages
        # .pth files execute only import-prefixed lines; encode the multiline script as one.
        (site_packages / "primer_prepend.pth").write_text(f"import sys; exec({PREPEND_PTH!r})\n", encoding="utf-8")
        return executable

    async def checkout(*args: Any, **kwargs: Any) -> Path:
        path: Path = await upstream_checkout(*args, **kwargs)
        revision, _ = await upstream_run(["git", "rev-parse", "HEAD"], cwd=path, output=True)
        print(f"Consumer revision: {path.name} {revision.stdout.strip()}", file=sys.stderr)
        return path

    async def run(cmd: str | list[str], **kwargs: Any) -> Any:
        proc, runtime = await upstream_run(cmd, **kwargs)
        if isinstance(cmd, str) and "--python-executable=" in cmd:
            print(f"Consumer check ({runtime:.2f}s): {cmd}", file=sys.stderr)
            print(proc.stderr + proc.stdout, file=sys.stderr)
            # Equal configuration/internal failures must not become an empty diff.
            if proc.returncode not in (0, 1) or "INTERNAL ERROR" in proc.stderr + proc.stdout:
                raise RuntimeError(f"Consumer checker failed operationally (exit {proc.returncode}): {cmd}")
        return proc, runtime

    primer.get_projects = registry.get_projects
    primer.setup_mypy = setup_mypy
    model.ensure_repo_at_revision = checkout
    model.run = run
    return primer


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
    available: dict[str, tuple[str, ...]] = registry.PYTHON_PROJECTS
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


def compare(old: str, new: str, *, groups: dict[str, tuple[str, ...]], dry_run: bool) -> int:
    version_output = command_output(["uv", "tree", "--locked", "--package=mypy", "--depth=0", "-q"])
    match = re.fullmatch(r"mypy v(\d+\.\d+\.\d+)", version_output)
    if match is None:
        raise ValueError(f"Unexpected locked mypy version: {version_output!r}")
    version = match[1]
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
                str(Path(__file__).resolve()),
                "--worker",
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("revision", nargs="?", help="COMMIT, A..B, or A...B; B may be WORKTREE")
    parser.add_argument(
        "--projects", metavar="NAME,...", help="Comma-separated consumer names; Python versions are automatic"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Resolve/check out sources and print commands without running primer"
    )
    parser.add_argument_group("CI").add_argument(
        "--python", choices=registry.PYTHON_PROJECTS, help="Restrict the consumer group for a CI matrix job"
    )
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


def primer_main() -> None:
    """Run upstream primer in the worker's selected Python environment."""
    try:
        configure().main()
    except Exception:
        traceback.print_exc()
        sys.exit(70)


if __name__ == "__main__":
    # Internal subprocess entry point: the launcher re-runs this script in the selected
    # Python environment with primer installed. Skip orchestration and run primer directly.
    if sys.argv[1:2] == ["--worker"]:
        del sys.argv[1]
        primer_main()
    else:
        sys.exit(main())
