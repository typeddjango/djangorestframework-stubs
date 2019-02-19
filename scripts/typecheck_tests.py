import os
import re
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Pattern

from git import Repo
from mypy import build
from mypy.main import process_options

PROJECT_DIRECTORY = Path(__file__).parent.parent

# DRF branch to typecheck against
DRF_BRANCH = 'drf-plugin-tests'

# Some errors occur for the test suite itself, and cannot be addressed via djangorestframework-stubs. They should be ignored
# using this constant.
IGNORED_ERRORS = [
    'Need type annotation for',
    'URLPattern',  # moved in django 2.0+
    'URLResolver',  # moved in django 2.0+
    'Invalid signature "def (self: Any) -> Any"',
    'already defined on line',
    'already defined (possibly by an import)',
    'variable has type Module',
    'Invalid base class',
    'MockRequest',
    'MockView',
    'MockTimezone',
    'MockLazyStr',
    'Invalid type "self"',
    re.compile(r'Item "None" of "Optional\[[a-zA-Z0-9]+\]" has no attribute'),
    'Optional[List[_Record]]',
    '"Callable[..., Any]" has no attribute "initkwargs"',
    'Cannot assign to a type',
    'Cannot assign to a method',
    '"Type[NonTimeThrottle]" has no attribute "called"',
    'BaseTokenAuthTests',
    re.compile(r'Dict entry [0-9] has incompatible type "[a-zA-Z]+": "None"; expected "object": "bool"')
]

MYPY_CONFIG_FILE = (PROJECT_DIRECTORY / 'scripts' / 'mypy.ini').absolute()
REPO_DIRECTORY = PROJECT_DIRECTORY / 'drf-sources'


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
    raw_path, _, error_line = error.partition(': ')
    fname, _, line_number = raw_path.partition(':')

    try:
        path = abs_test_folder.joinpath(fname).relative_to(PROJECT_DIRECTORY)
    except ValueError:
        # fail on travis, just show an error
        return error

    clickable_location = f'./{path}:{line_number or 1}'
    return error.replace(raw_path, clickable_location)


def check_with_mypy(abs_path: Path) -> int:
    error_happened = False
    with cd(abs_path):
        sources, options = process_options(['--cache-dir', str(MYPY_CONFIG_FILE.parent / '.mypy_cache'),
                                            '--config-file', str(MYPY_CONFIG_FILE),
                                            str(abs_path)])
        res = build.build(sources, options)
        for error_line in res.errors:
            if not error_line.startswith('tests/'):
                # only leave errors for tests/ directory
                continue
            if not is_ignored(error_line):
                print(replace_with_clickable_location(error_line, abs_test_folder=abs_path))
    return int(error_happened)


if __name__ == '__main__':
    # clone Django repository, if it does not exist
    if not REPO_DIRECTORY.exists():
        repo = Repo.clone_from('https://github.com/mkurnikov/django-rest-framework.git', REPO_DIRECTORY)
    else:
        repo = Repo(REPO_DIRECTORY)
        repo.remotes['origin'].pull(DRF_BRANCH)

    repo.git.checkout(DRF_BRANCH)

    global_rc = check_with_mypy(REPO_DIRECTORY.absolute())
    sys.exit(global_rc)
