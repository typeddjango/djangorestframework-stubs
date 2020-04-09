import os
import shutil
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Pattern

from mypy import build
from mypy.main import process_options

from scripts.ignored import IGNORED_ERRORS


@contextmanager
def cd(path):
    """Context manager to temporarily change working directories"""
    if not path:
        return
    prev_cwd = Path.cwd().as_posix()
    if isinstance(path, Path):
        path = path.as_posix()
    os.chdir(str(path))
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def is_ignored(line: str) -> bool:
    for pattern in IGNORED_ERRORS:
        if isinstance(pattern, Pattern):
            if pattern.search(line):
                return True
        else:
            if pattern in line:
                return True
    return False


def replace_with_clickable_location(error: str, abs_test_folder: Path) -> str:
    raw_path, _, error_line = error.partition(": ")
    fname, _, line_number = raw_path.partition(":")

    try:
        path = abs_test_folder.joinpath(fname).relative_to(PROJECT_DIRECTORY)
    except ValueError:
        # fail on travis, just show an error
        return error

    clickable_location = f"./{path}:{line_number or 1}"
    return error.replace(raw_path, clickable_location)


def check_with_mypy(abs_path: Path) -> int:
    error_happened = False
    with cd(abs_path):
        sources, options = process_options(
            [
                "--cache-dir",
                str(MYPY_CONFIG_FILE.parent / ".mypy_cache"),
                "--config-file",
                str(MYPY_CONFIG_FILE),
                str(abs_path),
            ]
        )
        res = build.build(sources, options)
        for error_line in res.errors:
            if not error_line.startswith("tests/"):
                # only leave errors for tests/ directory
                continue
            if not is_ignored(error_line):
                print(replace_with_clickable_location(error_line, abs_test_folder=abs_path))
    return int(error_happened)


if __name__ == "__main__":
    PROJECT_DIRECTORY = Path(__file__).parent.parent

    MYPY_CONFIG_FILE = (PROJECT_DIRECTORY / "scripts" / "mypy.ini").absolute()
    REPO_DIRECTORY = PROJECT_DIRECTORY / "drf-sources" / "tests"

    global_rc = 0
    tests_root = REPO_DIRECTORY
    mypy_cache_dir = Path(__file__).parent / ".mypy_cache"

    # copy django settings to the tests_root directory
    shutil.copy(PROJECT_DIRECTORY / "scripts" / "drf_tests_settings.py", tests_root)

    try:
        mypy_options = [
            "--cache-dir",
            str(MYPY_CONFIG_FILE.parent / ".mypy_cache"),
            "--config-file",
            str(MYPY_CONFIG_FILE),
        ]
        mypy_options += [str(tests_root)]

        import distutils.spawn

        mypy_executable = distutils.spawn.find_executable("mypy")
        command = [mypy_executable, *mypy_options]
        print(" ".join(command))
        completed = subprocess.run(
            command, env={"PYTHONPATH": str(tests_root)}, stdout=subprocess.PIPE, cwd=str(tests_root)
        )
        sorted_lines = sorted(completed.stdout.decode().splitlines())
        for line in sorted_lines:
            try:
                module_name = line.split("/")[0]
            except IndexError:
                module_name = "unknown"

            if not is_ignored(line):
                print(replace_with_clickable_location(line, abs_test_folder=tests_root))

        sys.exit(global_rc)

    except BaseException as exc:
        shutil.rmtree(mypy_cache_dir, ignore_errors=True)
        raise exc
