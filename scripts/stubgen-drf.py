import shutil
from argparse import ArgumentParser

from mypy.stubgen import generate_stubs, parse_options

from scripts.git_helpers import git_checkout_drf
from scripts.paths import DRF_SOURCE_DIRECTORY

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--drf_version", required=False)
    args = parser.parse_args()
    if DRF_SOURCE_DIRECTORY.exists():
        shutil.rmtree(DRF_SOURCE_DIRECTORY)
    git_checkout_drf(args.drf_version)
    stubgen_options = parse_options([f"{DRF_SOURCE_DIRECTORY}", "-o=stubgen"])
    generate_stubs(stubgen_options)
