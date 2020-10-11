from pathlib import Path

PROJECT_DIRECTORY = Path(__file__).parent.parent
STUBS_DIRECTORY = PROJECT_DIRECTORY / "rest_framework-stubs"  # type: Path
DRF_SOURCE_DIRECTORY = PROJECT_DIRECTORY / "drf_source"  # type: Path
STUBGEN_TARGET_DIRECTORY = PROJECT_DIRECTORY / "stubgen"  # type: Path
