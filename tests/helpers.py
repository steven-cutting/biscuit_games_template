"""Render the template and run what the render ships."""

from __future__ import annotations

import contextlib
import importlib
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


def run_tool_in_process(render: Render, module: str) -> int:
    """Run a `biscuit_games_tooling` console script's `main()` in this process, inside the render.

    The render ships no checker of its own: its `pyproject.toml` pins the package, which
    this repository's environment also installs at the same pin (`test_pins_agree`). Each
    script takes its root from `git rev-parse --show-toplevel` in the working directory,
    so the render must be a Git worktree. SystemExit carries the code where one is raised.
    """
    tool = importlib.import_module(f"biscuit_games_tooling.{module}")
    with contextlib.chdir(render.path):
        try:
            return int(tool.main())
        except SystemExit as stop:
            return stop.code if isinstance(stop.code, int) else 1


def run_tool(render: Render, module: str, *args: str) -> subprocess.CompletedProcess[str]:
    """Subprocess form, for a script that takes arguments or downloads (install_allium, run_allium).

    `python -m` from this repository's environment, never `uv run` inside the render:
    uv would adopt the render's `pyproject.toml` as the project and sync the render.
    """
    return subprocess.run(
        [sys.executable, "-m", f"biscuit_games_tooling.{module}", *args],
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
