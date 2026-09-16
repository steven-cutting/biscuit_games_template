"""Fixtures shared by the harness: one default render, and a git-initialised copy."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from tests.helpers import Render, render_template

if TYPE_CHECKING:
    from collections.abc import Iterator

TEMPLATE_ROOT = Path(__file__).resolve().parents[1]

# The answer names are copier.yml's. This dict is the one place the harness
# spells them; tests/inventory.py reads the slug from here.
DEFAULT_ANSWERS: dict[str, str] = {
    "game_name": "Tic Tac Toe Beans",
    "game_slug": "tic_tac_toe_beans",
    "description": "A three-in-a-row game played with beans.",
    "repository": "steven-cutting/tic_tac_toe_beans",
}

NETWORK = os.environ.get("BISCUIT_TEMPLATE_NETWORK") == "1"
FULL = os.environ.get("BISCUIT_TEMPLATE_FULL") == "1"


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    skip_network = pytest.mark.skip(reason="set BISCUIT_TEMPLATE_NETWORK=1")
    skip_full = pytest.mark.skip(reason="set BISCUIT_TEMPLATE_FULL=1")
    for item in items:
        if "network" in item.keywords and not NETWORK:
            item.add_marker(skip_network)
        if "full" in item.keywords and not FULL:
            item.add_marker(skip_full)


@pytest.fixture(scope="session")
def default_render(tmp_path_factory: pytest.TempPathFactory) -> Render:
    """One render with the default answers, shared by the read-only tests."""
    return render_template(TEMPLATE_ROOT, tmp_path_factory.mktemp("render"), DEFAULT_ANSWERS)


@pytest.fixture
def git_render(default_render: Render, tmp_path: Path) -> Iterator[Render]:
    """A private copy of the default render inside an initialised git repository.

    The package's scripts take the root from `git rev-parse --show-toplevel`, and
    `bg-validate-agents` lists files with `git ls-files --others`, so `git init` is
    enough for both; the update tests (T10) additionally commit, because copier
    treats untracked files as dirty.
    """
    copy = default_render.copy_to(tmp_path / "game")
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=copy.path, check=True)
    yield copy
