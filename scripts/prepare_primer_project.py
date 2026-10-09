"""Consumer preparation invoked inside primer's isolated consumer environment."""

import argparse
import ast
import os
import shlex
import subprocess
from pathlib import Path


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


def prepare(project: str, install: str) -> None:
    installer = shlex.split(install)
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
                "--output-dir",
                "generated",
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
                "--project",
                "generated/primer_project",
                "--output-file",
                str(requirements.resolve()),
            ],
            check=True,
        )
        subprocess.run([*installer, "-r", str(requirements)], check=True)
    elif project in {"sentry", "lidotiku"}:
        requirements = Path("primer-requirements.txt")
        subprocess.run(
            ["uv", "export", "--frozen", "--no-hashes", "--no-emit-project", "--output-file", str(requirements)],
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
        raise ValueError(f"Unknown consumer: {project}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", choices=["cookiecutter-django", "sentry", "lidotiku"])
    parser.add_argument("--install", required=True)
    args = parser.parse_args()
    prepare(args.project, args.install)
