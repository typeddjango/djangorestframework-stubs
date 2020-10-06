import itertools
import shutil
import subprocess
import sys
from argparse import ArgumentParser
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Pattern, Union, Optional

from git import RemoteProgress, Repo

from scripts.enabled_test_modules import EXTERNAL_MODULES, IGNORED_ERRORS, IGNORED_MODULES, MOCK_OBJECTS

PROJECT_DIRECTORY = Path(__file__).parent.parent
STUBS_DIRECTORY = PROJECT_DIRECTORY / "rest_framework-stubs"  # type: Path
DRF_DIRECTORY = PROJECT_DIRECTORY / "drf_source"  # type: Path


def get_unused_ignores(ignored_message_freq: Dict[str, Dict[Union[str, Pattern], int]]) -> List[str]:
    unused_ignores = []
    for root_key, patterns in IGNORED_ERRORS.items():
        for pattern in patterns:
            if ignored_message_freq[root_key][pattern] == 0 and pattern not in itertools.chain(
                EXTERNAL_MODULES, MOCK_OBJECTS
            ):
                unused_ignores.append(f"{root_key}: {pattern}")
    return unused_ignores


def is_pattern_fits(pattern: Union[Pattern, str], line: str):
    if isinstance(pattern, Pattern):
        if pattern.search(line):
            return True
    else:
        if pattern in line:
            return True
    return False


def is_ignored(line: str, filename: str, ignored_message_dict: Dict[str, Dict[str, int]]) -> bool:
    if "runtests" in line or filename in IGNORED_MODULES:
        return True
    for pattern in IGNORED_ERRORS["__common__"]:
        if pattern in line:
            return True
    for pattern in IGNORED_ERRORS.get(filename, []):
        if is_pattern_fits(pattern, line):
            ignored_message_dict[test_filename][pattern] += 1
            return True
    for mock_object in MOCK_OBJECTS:
        if mock_object in line:
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


class ProgressPrinter(RemoteProgress):
    def line_dropped(self, line: str) -> None:
        print(line)

    def update(self, op_code, cur_count, max_count=None, message=""):
        print(self._cur_line)


def checkout_target_tag(drf_version: Optional[str]) -> Path:
    if not DRF_DIRECTORY.exists():
        DRF_DIRECTORY.mkdir(exist_ok=True, parents=False)
        repository = Repo.clone_from(
            "https://github.com/encode/django-rest-framework.git",
            DRF_DIRECTORY,
            progress=ProgressPrinter(),
            branch="master",
            depth=100,
        )
    else:
        repository = Repo(DRF_DIRECTORY)
        repository.remote("origin").pull("master", progress=ProgressPrinter(), depth=100)
    repository.git.checkout(drf_version or "master")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--drf_version", required=False)
    args = parser.parse_args()
    checkout_target_tag(args.drf_version)
    shutil.copytree(STUBS_DIRECTORY, DRF_DIRECTORY / "rest_framework", dirs_exist_ok=True)
    mypy_config_file = (PROJECT_DIRECTORY / "scripts" / "mypy.ini").absolute()
    mypy_cache_dir = Path(__file__).parent / ".mypy_cache"
    tests_root = DRF_DIRECTORY / "tests"
    global_rc = 0

    try:
        mypy_options = [
            "--cache-dir",
            str(mypy_cache_dir),
            "--config-file",
            str(mypy_config_file),
            "--show-traceback",
            "--no-error-summary",
            "--hide-error-context",
        ]
        mypy_options += [str(tests_root)]

        import distutils.spawn

        mypy_executable = distutils.spawn.find_executable("mypy")
        mypy_argv = [mypy_executable, *mypy_options]
        completed = subprocess.run(
            mypy_argv,
            env={"PYTHONPATH": str(PROJECT_DIRECTORY)},
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        output = completed.stdout.decode()

        ignored_message_freqs = defaultdict(lambda: defaultdict(int))

        sorted_lines = sorted(output.splitlines())
        for line in sorted_lines:
            try:
                path_to_error = line.split(":")[0]
                test_filename = path_to_error.split("/")[2]
            except IndexError:
                test_filename = "unknown"

            if not is_ignored(line, test_filename, ignored_message_dict=ignored_message_freqs):
                global_rc = 1
                print(line)

        unused_ignores = get_unused_ignores(ignored_message_freqs)
        if unused_ignores:
            print("UNUSED IGNORES ------------------------------------------------")
            print("\n".join(unused_ignores))

        sys.exit(global_rc)

    except BaseException as exc:
        shutil.rmtree(mypy_cache_dir, ignore_errors=True)
        raise exc
