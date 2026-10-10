"""
Internal entry point; invoked by `run_primer.py` or upstream mypy_primer.

--run-primer: the launcher starts this mode in its selected Python/primer environment.
It imports the public script's project definitions, installs our hooks, and runs primer.

--prepare-project=NAME --install=COMMAND: primer invokes this mode from the project's
checkout during dependency installation, before either mypy check. Preparation uses
the supplied installer and its target Python, not necessarily this script's interpreter.
Exactly one mode is required; project preparation needs only the standard library.
"""

import argparse
import ast
import os
import shlex
import subprocess
import sys
import traceback
from collections.abc import Callable
from pathlib import Path
from typing import Any

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


def install_checker_path_hook(primer: Any, utils: Any) -> None:
    """Hook mypy setup so each checker can import the selected checkout's DRF plugin."""
    upstream_setup = primer.setup_mypy

    async def setup_mypy(mypy_dir: Path, **kwargs: Any) -> Path:
        """Set up mypy and add the startup hook for the selected stubs/plugin checkout."""
        executable: Path = await upstream_setup(mypy_dir, **kwargs)
        site_packages = utils.Venv(mypy_dir / "venv").site_packages
        # .pth files execute only import-prefixed lines; encode the multiline script as one.
        (site_packages / "primer_prepend.pth").write_text(f"import sys; exec({PREPEND_PTH!r})\n", encoding="utf-8")
        return executable

    primer.setup_mypy = setup_mypy


def install_checkout_logging(model: Any, status: Callable[..., None]) -> None:
    """Hook project checkout to show preparation progress and optionally its revision."""
    upstream_checkout = model.ensure_repo_at_revision
    upstream_run = model.run

    async def checkout(*args: Any, **kwargs: Any) -> Path:
        """Return the checked-out project path after logging preparation progress."""
        path: Path = await upstream_checkout(*args, **kwargs)
        status(f"Preparing {path.name}")
        if model.ctx.get().debug:
            revision, _ = await upstream_run(["git", "rev-parse", "HEAD"], cwd=path, output=True)
            status(f"Project revision: {path.name} {revision.stdout.strip()}")
        return path

    model.ensure_repo_at_revision = checkout


def install_checker_diagnostics(model: Any, status: Callable[..., None]) -> None:
    """Hook commands to report check timings, optional output, and operational failures."""
    upstream_run = model.run

    async def run(cmd: str | list[str], **kwargs: Any) -> Any:
        """Run a command, showing concise checker progress or full failure diagnostics."""
        if not isinstance(cmd, str) or "--python-executable=" not in cmd:
            return await upstream_run(cmd, **kwargs)
        project = Path(kwargs["cwd"]).name
        sources = kwargs["env"]["MYPY_PRIMER_PREPEND_PATH"]
        label = "old" if sources == str(model.ctx.get().old_prepend_path) else "new"
        status(f"Checking {project} ({label})")
        proc, runtime = await upstream_run(cmd, **kwargs)
        output = proc.stderr + proc.stdout
        # Equal configuration/internal failures must not become an empty diff.
        failed = proc.returncode not in (0, 1) or "INTERNAL ERROR" in output
        status(f"Finished {project} ({label}) in {runtime:.2f}s", kind="error" if failed else "info")
        if model.ctx.get().debug or failed:
            print(
                f"\n--- mypy: {project} ({label}) ---\n{output.rstrip()}\n--- end mypy ---\n",
                file=sys.stderr,
                flush=True,
            )
        if failed:
            raise RuntimeError(f"Project checker failed operationally (exit {proc.returncode}): {cmd}")
        return proc, runtime

    model.run = run


def install_project_status(model: Any, status: Callable[..., None]) -> None:
    """Hook completed project comparisons to report their diff status."""
    upstream_result = model.Project.primer_result

    async def primer_result(self: Any, *args: Any, **kwargs: Any) -> Any:
        """Report each project's outcome after both checks, preserving failures."""
        try:
            result = await upstream_result(self, *args, **kwargs)
        except Exception:
            status(f"Failed {self.name}: comparison incomplete", kind="error")
            raise
        summary = "diagnostic differences" if result.diff else "no diagnostic differences"
        status(f"Finished {self.name}: {summary}", kind="warning" if result.diff else "success")
        return result

    model.Project.primer_result = primer_result


def configure_primer() -> Any:
    """Select our projects and install hooks on the upstream functions primer calls."""
    # Optional primer imports belong only to --run-primer, never project preparation.
    import mypy_primer.main as primer  # type: ignore[import-not-found]
    import mypy_primer.model as model  # type: ignore[import-not-found]
    import mypy_primer.utils as utils  # type: ignore[import-not-found]

    if __package__:
        from . import run_primer as package_runner

        runner = package_runner
    else:
        import run_primer  # type: ignore[import-not-found]

        runner = run_primer

    primer.get_projects = runner.get_projects
    install_checker_path_hook(primer, utils)
    install_checkout_logging(model, runner.log_status)
    install_checker_diagnostics(model, runner.log_status)
    install_project_status(model, runner.log_status)
    return primer


def primer_main() -> None:
    """Run upstream primer in the launcher's selected Python environment."""
    configure_primer().main()


def normalize_generated_secrets(project: Path) -> None:
    """Make disposable primer fixtures reproducible; never deploy this project."""
    secret = "primer-only-secret-never-deploy-this-generated-project"
    for filename in ("local.py", "test.py"):
        path = project / "config" / "settings" / filename
        source = path.read_text(encoding="utf-8")
        assignments = [
            node
            for node in ast.parse(source).body
            if isinstance(node, ast.Assign)
            and any(isinstance(target, ast.Name) and target.id == "SECRET_KEY" for target in node.targets)
        ]
        if len(assignments) != 1 or not isinstance(assignments[0].value, ast.Call):
            raise ValueError(f"Unexpected generated SECRET_KEY assignment in {path}")
        default = next(keyword.value for keyword in assignments[0].value.keywords if keyword.arg == "default")
        literal = ast.get_source_segment(source, default)
        if not isinstance(default, ast.Constant) or not isinstance(default.value, str) or literal is None:
            raise ValueError(f"Unexpected generated SECRET_KEY default in {path}")
        path.write_text(source.replace(literal, repr(secret), 1), encoding="utf-8")
    values = {
        "DJANGO_SECRET_KEY": secret,
        "DJANGO_ADMIN_URL": "primer-admin/",
        "POSTGRES_USER": "primer",
        "POSTGRES_PASSWORD": "primer-only-do-not-deploy",
        "CELERY_FLOWER_USER": "primer",
        "CELERY_FLOWER_PASSWORD": "primer-only-do-not-deploy",
    }
    for path in (project / ".envs").rglob("*"):
        if path.is_file():
            rewritten = []
            for line in path.read_text(encoding="utf-8").splitlines(keepends=True):
                key = line.partition("=")[0]
                rewritten.append(f"{key}={values[key]}\n" if key in values else line)
            path.write_text("".join(rewritten), encoding="utf-8")


def prepare_primer_project(project: str, install: str) -> None:
    """Install project dependencies and generate configuration using primer's supplied installer."""
    installer = shlex.split(install)
    # The helper may run in the runner environment; project subprocesses need its target Python.
    python = installer[installer.index("--python") + 1] if "--python" in installer else installer[0]
    if project == "cookiecutter-django":
        subprocess.run([*installer, "cookiecutter==2.6.0"], check=True)
        subprocess.run(
            [
                python,
                "-m",
                "cookiecutter",
                ".",
                "--no-input",
                "--output-dir=generated",
                "project_name=Primer Project",
                "project_slug=primer_project",
                "rest_api=DRF",
                "cloud_provider=None",
                "mail_service=Other SMTP",
                "use_docker=n",
                "use_celery=n",
                "use_sentry=n",
                "frontend_pipeline=None",
                "keep_local_envs_in_vcs=y",
                "use_whitenoise=y",
            ],
            check=True,
        )
        normalize_generated_secrets(Path("generated/primer_project"))
        requirements = Path("generated/primer_project/primer-requirements.txt")
        subprocess.run(
            [
                "uv",
                "export",
                "--frozen",
                "--no-hashes",
                "--no-emit-project",
                "--project=generated/primer_project",
                f"--output-file={requirements.resolve()}",
            ],
            check=True,
        )
        subprocess.run([*installer, "-r", str(requirements)], check=True)
    elif project in {"sentry", "lidotiku"}:
        requirements = Path("primer-requirements.txt")
        subprocess.run(
            ["uv", "export", "--frozen", "--no-hashes", "--no-emit-project", f"--output-file={requirements}"],
            check=True,
        )
        subprocess.run([*installer, "-r", str(requirements)], check=True)
        if project == "sentry":
            subprocess.run(
                [python, "-m", "sentry", "init", "--dev", "--no-clobber", "primer-config"],
                env={**os.environ, "PYTHONPATH": "src:."},
                check=True,
            )
    else:
        raise ValueError(f"Unknown project: {project}")


def main() -> int:
    """Dispatch exactly one internal mode, forwarding remaining arguments to primer."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter, allow_abbrev=False
    )
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--run-primer", action="store_true", help="Run primer with its remaining CLI arguments")
    modes.add_argument("--prepare-project", choices=["cookiecutter-django", "sentry", "lidotiku"])
    parser.add_argument("--install", help="Primer's installer command; required with --prepare-project")
    args, primer_args = parser.parse_known_args()
    if args.run_primer:
        if args.install is not None:
            parser.error("--install is only valid with --prepare-project")
        sys.argv[1:] = primer_args
        primer_main()
    else:
        if primer_args:
            parser.error(f"unrecognized arguments: {' '.join(primer_args)}")
        if args.install is None:
            parser.error("--prepare-project requires --install")
        prepare_primer_project(args.prepare_project, args.install)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        traceback.print_exc()
        sys.exit(70)
