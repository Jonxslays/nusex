import os
import shutil
import zipfile
from pathlib import Path

import nox

from nusex import CONFIG_DIR

if os.environ.get("CI", False):
    import sys

    PY_VERSIONS = [".".join(f"{v}" for v in sys.version_info[:2])]

else:
    PY_VERSIONS = [f"3.{v}" for v in range(6, 11)]  # 3.6 - 3.10

PROJECT_NAME = "nusex"
LIB_DIR = Path(__file__).parent / PROJECT_NAME
TEST_DIR = Path(__file__).parent / "tests"


def parse_requirements(path):
    with open(path, mode="r", encoding="utf-8") as f:
        deps = (d.strip() for d in f.readlines())
        return [d for d in deps if not d.startswith(("#", "-r"))]


DEPS = {
    name: install
    for name, install in (
        r.split("~=")
        for r in parse_requirements("./requirements-dev.txt")
        if not r.startswith(("#", "-r"))
    )
}


@nox.session(python=PY_VERSIONS, reuse_venv=True)
def tests(session):
    test_config_dir = CONFIG_DIR.parent / "nusex-test"

    with zipfile.ZipFile(Path(__file__).parent / "tests/nusex-test.zip") as z:
        z.extractall(test_config_dir)

    deps = parse_requirements("./requirements-test.txt")
    session.install(*deps)
    session.run("pytest", "--verbose", "--log-level=INFO")

    if os.path.isdir(test_config_dir):
        shutil.rmtree(test_config_dir)


@nox.session(reuse_venv=True)
def check_formatting(session):
    session.install(f"black~={DEPS['black']}")
    session.run("black", ".", "--check")


@nox.session(reuse_venv=True)
def check_imports(session):
    session.install(f"flake8~={DEPS['flake8']}", f"isort~={DEPS['isort']}")
    # flake8 doesn't use the gitignore so we have to be explicit.
    session.run(
        "flake8",
        PROJECT_NAME,
        "tests",
        "--select",
        "F4",
        "--extend-ignore",
        "E,F,W",
        "--extend-exclude",
        "__init__.py",
    )
    session.run("isort", ".", "-cq", "--profile", "black")


@nox.session(reuse_venv=True)
def check_line_lengths(session):
    session.install(f"len8~={DEPS['len8']}")
    session.run("len8", PROJECT_NAME, "tests")


@nox.session(reuse_venv=True)
def check_licensing(session):
    missing = []

    for p in [*LIB_DIR.rglob("*.py"), *TEST_DIR.rglob("*.py")]:
        with open(p) as f:
            if not f.read().startswith("# Copyright (c)"):
                missing.append(p)

    if missing:
        session.error(
            f"\n{len(missing):,} file(s) are missing their licenses:\n"
            + "\n".join(f" - {file}" for file in missing)
        )
