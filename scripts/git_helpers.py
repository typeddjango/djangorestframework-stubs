from typing import Optional, Union

from git.remote import RemoteProgress
from git.repo import Repo

from scripts.paths import DRF_SOURCE_DIRECTORY


class ProgressPrinter(RemoteProgress):
    def line_dropped(self, line: str) -> None:
        print(line)

    def update(
        self, op_code: int, cur_count: Union[str, float], max_count: Union[str, float, None] = None, message: str = ""
    ) -> None:
        print(self._cur_line)


def git_checkout_drf(commit_ref: Optional[str] = None) -> None:
    if not DRF_SOURCE_DIRECTORY.exists():
        DRF_SOURCE_DIRECTORY.mkdir(exist_ok=True, parents=False)
        repository = Repo.clone_from(
            "https://github.com/encode/django-rest-framework.git",
            DRF_SOURCE_DIRECTORY,
            progress=ProgressPrinter(),  # type: ignore
            branch="master",
            depth=100,
        )
    else:
        repository = Repo(DRF_SOURCE_DIRECTORY)
        repository.remote("origin").pull("master", progress=ProgressPrinter(), depth=100)
    repository.git.checkout(commit_ref or "master")
