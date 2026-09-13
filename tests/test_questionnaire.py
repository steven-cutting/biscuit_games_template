"""The questionnaire refuses what copier.yml's validators refuse, and computes the rest."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.conftest import DEFAULT_ANSWERS, TEMPLATE_ROOT
from tests.helpers import render_template

if TYPE_CHECKING:
    from pathlib import Path

BAD_GAME_NAMES = ["", "x", "Bad{Name}", "a" * 41, "tab\there", "123"]
BAD_GAME_SLUGS = ["Tic Tac", "_leading", "UPPER", "a-b", "a__b"]
BAD_REPOSITORIES = ["nogroup", "-x/y", "a/.git"]


@pytest.mark.parametrize("value", BAD_GAME_NAMES)
def test_bad_game_name_is_refused(tmp_path: Path, value: str) -> None:
    with pytest.raises(ValueError, match="Validation error for question 'game_name'"):
        render_template(TEMPLATE_ROOT, tmp_path / "r", {**DEFAULT_ANSWERS, "game_name": value})


@pytest.mark.parametrize("value", BAD_GAME_SLUGS)
def test_bad_game_slug_is_refused(tmp_path: Path, value: str) -> None:
    with pytest.raises(ValueError, match="Validation error for question 'game_slug'"):
        render_template(TEMPLATE_ROOT, tmp_path / "r", {**DEFAULT_ANSWERS, "game_slug": value})


@pytest.mark.parametrize("value", BAD_REPOSITORIES)
def test_bad_repository_is_refused(tmp_path: Path, value: str) -> None:
    with pytest.raises(ValueError, match="Validation error for question 'repository'"):
        render_template(TEMPLATE_ROOT, tmp_path / "r", {**DEFAULT_ANSWERS, "repository": value})


def test_computed_defaults(tmp_path: Path) -> None:
    render = render_template(
        TEMPLATE_ROOT,
        tmp_path / "r",
        {"game_name": "Tic Tac Toe Beans", "description": DEFAULT_ANSWERS["description"]},
    )
    answers = render.answers()
    assert answers["game_slug"] == "tic_tac_toe_beans"
    assert answers["repository"] == "steven-cutting/tic_tac_toe_beans"
    assert (render.path / "docs" / "specs" / "tic_tac_toe_beans.allium").is_file()
    brand = render.read("src/lib/brand.ts")
    assert "GAME_NAME = 'tic tac toe beans'" in brand
    assert "GAME_TITLE = 'Tic Tac Toe Beans'" in brand
    deploy = render.read("docs/how-to/deploy-to-github-pages.md")
    assert "https://steven-cutting.github.io/tic_tac_toe_beans/" in deploy
