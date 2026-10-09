"""Run the pinned primer with our registry and checkout-isolated DRF plugins."""

import importlib
import sys
import traceback
from pathlib import Path
from typing import Any

PREPEND_PTH = (
    "import os; import sys; exec('''env = os.environ.get(\"MYPY_PRIMER_PREPEND_PATH\")"
    "\\nif env: sys.path = env.split(os.pathsep) + sys.path''')"
)


def get_projects() -> list[Any]:
    registry: Any = importlib.import_module(f"{__package__}.primer_projects" if __package__ else "primer_projects")
    projects: list[Any] = registry.get_projects()
    return projects


def configure() -> Any:
    primer: Any = importlib.import_module("mypy_primer.main")
    model: Any = importlib.import_module("mypy_primer.model")
    utils: Any = importlib.import_module("mypy_primer.utils")
    upstream_setup = primer.setup_mypy
    upstream_run = model.run

    async def setup_mypy(mypy_dir: Path, **kwargs: Any) -> Path:
        executable: Path = await upstream_setup(mypy_dir, **kwargs)
        site_packages = utils.Venv(mypy_dir / "venv").site_packages
        (site_packages / "primer_prepend.pth").write_text(PREPEND_PTH, encoding="utf-8")
        return executable

    async def run(cmd: str | list[str], **kwargs: Any) -> Any:
        proc, runtime = await upstream_run(cmd, **kwargs)
        if isinstance(cmd, str) and "--python-executable=" in cmd:
            print(f"Consumer check ({runtime:.2f}s): {cmd}", file=sys.stderr)
            print(proc.stderr + proc.stdout, file=sys.stderr)
            # Upstream only retains success/failure, which can otherwise hide equal
            # configuration failures or internal errors behind an empty diff.
            if proc.returncode not in (0, 1) or "INTERNAL ERROR" in proc.stderr + proc.stdout:
                raise RuntimeError(f"Consumer checker failed operationally (exit {proc.returncode}): {cmd}")
        return proc, runtime

    primer.get_projects = get_projects
    primer.setup_mypy = setup_mypy
    model.run = run
    return primer


if __name__ == "__main__":
    try:
        for project in get_projects():
            print(f"Consumer pin: {project.name} {project.revision}", file=sys.stderr)
        configure().main()
    except Exception:
        # Startup failures happen before upstream's own exception boundary.
        traceback.print_exc()
        sys.exit(70)
