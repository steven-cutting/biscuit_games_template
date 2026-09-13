"""Render the template and run what the render ships."""

from __future__ import annotations

import runpy
import shutil
import subprocess
import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING

import copier
import yaml

if TYPE_CHECKING:
    from pathlib import Path


@dataclass(frozen=True)
class Render:
    path: Path

    def files(self) -> list[Path]:
        """Every file in the render, relative to its root, `.git` excluded."""
        return sorted(
            p.relative_to(self.path)
            for p in self.path.rglob("*")
            if p.is_file() and ".git" not in p.parts
        )

    def text_files(self) -> list[Path]:
        """Every file except the answers file, which carries the local template path."""
        return [p for p in self.files() if p.name != ".copier-answers.yml"]

    def read(self, relative: Path | str) -> str:
        return (self.path / relative).read_text(encoding="utf-8")

    def answers(self) -> dict[str, object]:
        loaded = yaml.safe_load(self.read(".copier-answers.yml"))
        assert isinstance(loaded, dict)
        return loaded

    def copy_to(self, destination: Path) -> Render:
        shutil.copytree(self.path, destination)
        return Render(destination)


def render_template(
    template: Path, destination: Path, data: dict[str, str], vcs_ref: str = "HEAD"
) -> Render:
    """`copier copy` with `data` as answers; a validator failure raises ValueError."""
    copier.run_copy(
        str(template),
        destination,
        data=data,
        defaults=True,
        unsafe=False,
        vcs_ref=vcs_ref,
        quiet=True,
    )
    return Render(destination)


def run_script_in_process(render: Render, script: str) -> int:
    """Run a rendered checker as `python scripts/<script>` would, in this process.

    ROOT in both validators is `Path(__file__).resolve().parents[1]`, so the
    script judges the render it was rendered into. SystemExit carries the code.
    """
    try:
        runpy.run_path(str(render.path / "scripts" / script), run_name="__main__")
    except SystemExit as stop:
        return int(stop.code or 0)
    return 0


def run_script(render: Render, script: str, *args: str) -> subprocess.CompletedProcess[str]:
    """Subprocess form, for scripts that import a sibling (run_allium imports install_allium)."""
    return subprocess.run(
        [sys.executable, f"scripts/{script}", *args],
        cwd=render.path,
        check=False,
        capture_output=True,
        text=True,
    )


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
    ).stdout.strip()


def commit_all(cwd: Path, message: str) -> None:
    git(cwd, "add", "-A")
    git(
        cwd,
        "-c",
        "user.name=template-tests",
        "-c",
        "user.email=tests@example.invalid",
        "commit",
        "-q",
        "-m",
        message,
        "--no-verify",
    )
