"""A render passes its own gate on the first run and leaves only the lockfiles behind."""

from __future__ import annotations

import os
import platform
import subprocess
from typing import TYPE_CHECKING

import pytest

from tests.helpers import commit_all, git

if TYPE_CHECKING:
    from pathlib import Path

    from tests.helpers import Render

LOCKFILES = {"?? package-lock.json", "?? uv.lock"}


def just(cwd: Path, recipe: str) -> int:
    return subprocess.run(["just", recipe], cwd=cwd, check=False).returncode


def status(cwd: Path) -> set[str]:
    return set(git(cwd, "status", "--porcelain").splitlines())


@pytest.mark.full
@pytest.mark.timeout(3600)
def test_render_passes_its_own_gate(default_render: Render, tmp_path: Path) -> None:
    game = default_render.copy_to(tmp_path / "game")
    git(game.path, "init", "-q", "-b", "main")
    commit_all(game.path, "render")
    assert just(game.path, "initialize") == 0
    assert status(game.path) == LOCKFILES, "initialize touched a file the render ships"
    if os.environ.get("CI") == "true" and platform.system() == "Linux":
        assert just(game.path, "storybook-browsers-deps") == 0
    assert just(game.path, "check") == 0
    assert status(game.path) == LOCKFILES, "a gate wrote into the worktree"
