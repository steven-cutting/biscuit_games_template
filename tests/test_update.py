"""`copier update` round trips: a pristine game equals a fresh render; game work survives."""

from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING

import copier
import pytest

from tests.conftest import DEFAULT_ANSWERS, TEMPLATE_ROOT
from tests.helpers import Render, commit_all, git, render_template, run_tool_in_process
from tests.inventory import GAME_EDITED, MANAGED, SEED

if TYPE_CHECKING:
    from pathlib import Path

MARKERS = (b"<<<<<<< before updating", b">>>>>>> after updating")
SLUG = DEFAULT_ANSWERS["game_slug"]
IDENTITY = ("-c", "user.name=template-tests", "-c", "user.email=tests@example.invalid")
TEMPLATE_CHANGE = "A template release changed this page after the game was rendered."
MAP_CHANGE = "A template release changed this map after the game was rendered."
SYNTHETIC = (("docs/reference/testing.md", TEMPLATE_CHANGE), ("docs/README.md", MAP_CHANGE))

BEANS_PAGE = """---
title: "Beans"
kind: "project"
audience: [contributor, agent]
canonical_for: [beans]
requires: []
---

# Beans

The beans are the marks this game is played with. A page the game added after it was
rendered, registered at the end of the manifest and linked from the end of the map, so
that a template update and this addition land in different hunks and both survive the
three-way merge that copier update performs on every managed file.
"""
BEANS_ENTRY = (
    '    {"path": "project/beans.md", "title": "Beans", "kind": "project", '
    '"audience": ["contributor", "agent"], "canonical_for": ["beans"], "requires": []}'
)
BEANS_LINK = "- [Beans](project/beans.md)"
GAME_README = "# Beans\n\nThe game's own words.\n"
BOARD = '<script lang="ts">\n  // The board goes here.\n</script>\n\n<div class="board"></div>\n'
BOARD_TEST = (
    "import { describe, expect, it } from 'vitest';\n\n"
    "describe('board', () => {\n  it('exists', () => {\n    expect(true).toBe(true);\n  });\n});\n"
)


@pytest.fixture(scope="module")
def template_clone(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A throwaway clone holding every ref the tests render, never the real repository."""
    clone = tmp_path_factory.mktemp("template") / "clone"
    git(TEMPLATE_ROOT, "clone", "-q", "--no-checkout", str(TEMPLATE_ROOT), str(clone))
    if git(TEMPLATE_ROOT, "status", "--porcelain"):
        tree_of = ("--git-dir=.git", f"--work-tree={TEMPLATE_ROOT}")
        git(clone, *tree_of, "add", "-A")
        git(clone, *tree_of, *IDENTITY, "commit", "-q", "-m", "wip", "--no-verify")
    git(clone, "checkout", "-q", "-f", "HEAD")
    if int(git(clone, "rev-list", "--count", "HEAD")) < 2:
        pytest.skip("the update round trip needs two real commits")
    assert "docs/README.md" in {str(path) for path in GAME_EDITED}
    assert "docs/reference/testing.md" in {str(path) for path in MANAGED - GAME_EDITED}
    page = clone / "template" / "docs" / "reference" / "testing.md"
    text = page.read_text(encoding="utf-8").rstrip("\n") + "\n\n" + TEMPLATE_CHANGE + "\n"
    page.write_text(text, encoding="utf-8")
    docs_map = clone / "template" / "docs" / "README.md.jinja"
    lines = docs_map.read_text(encoding="utf-8").splitlines(keepends=True)
    heading = next(index for index, line in enumerate(lines) if line.startswith("# "))
    lines.insert(heading + 2, MAP_CHANGE + "\n\n")
    docs_map.write_text("".join(lines), encoding="utf-8")
    git(clone, *IDENTITY, "commit", "-q", "-a", "-m", "synthetic template change", "--no-verify")
    return clone


def resolve_ref(clone: Path, old_ref: str) -> str:
    if old_ref != "latest-tag":
        return old_ref
    tags = git(clone, "tag", "--list", "v*", "--sort=-version:refname").splitlines()
    if not tags:
        pytest.skip("no v* tag yet; T11 makes the first")
    return tags[0]


def tree(render: Render) -> dict[str, str]:
    """Relative path to content digest, `.git/` and the answers file aside."""
    return {
        str(path): hashlib.sha256((render.path / path).read_bytes()).hexdigest()
        for path in render.files()
        if str(path) != ".copier-answers.yml"
    }


def assert_no_conflicts(render: Render) -> None:
    """A marker is a whole line, as copier's own conflict scan reads it (`_apply_update`).

    Two shipped pages quote both markers inside a sentence; that is prose, not a conflict.
    """
    for path in render.files():
        assert path.suffix != ".rej", f"{path} was rejected by git apply"
        lines = (render.path / path).read_bytes().splitlines()
        assert not any(line.rstrip() in MARKERS for line in lines), f"{path} carries markers"


def assert_template_change(game: Render, *, arrived: bool) -> None:
    """The synthetic commit's strings: absent at the old ref, present after the update."""
    for path, sentence in SYNTHETIC:
        assert (sentence in game.read(path)) is arrived, (
            f"{path}: template change arrived is not {arrived}"
        )


def start_game(clone: Path, dest: Path, old_ref: str) -> Render:
    game = render_template(clone, dest, DEFAULT_ANSWERS, vcs_ref=old_ref)
    git(game.path, "init", "-q", "-b", "main")
    commit_all(game.path, f"render at {old_ref}")
    return game


def update(game: Render) -> None:
    copier.run_update(
        game.path,
        defaults=True,
        overwrite=True,
        skip_answered=True,
        unsafe=False,
        vcs_ref="HEAD",
        conflict="inline",
        quiet=True,
    )


def add_game_page(game: Render) -> None:
    """Register a page the way CONVENTIONS §5 tells a game to: after the last decision."""
    (game.path / "docs" / "project" / "beans.md").write_text(BEANS_PAGE, encoding="utf-8")
    manifest = game.path / "docs" / "manifest.yml"
    lines = manifest.read_text(encoding="utf-8").splitlines(keepends=True)
    last = max(index for index, line in enumerate(lines) if '"path": "decisions/' in line)
    lines[last] = lines[last].rstrip("\n") + ",\n"
    lines.insert(last + 1, BEANS_ENTRY + "\n")
    manifest.write_text("".join(lines), encoding="utf-8")
    readme = game.path / "docs" / "README.md"
    text = readme.read_text(encoding="utf-8")
    assert "## This game" in text
    readme.write_text(text.rstrip("\n") + "\n\n" + BEANS_LINK + "\n", encoding="utf-8")


@pytest.mark.parametrize("old_ref", ["HEAD~2", "latest-tag"])
def test_pristine_update_equals_fresh_render(
    template_clone: Path, tmp_path: Path, old_ref: str
) -> None:
    game = start_game(template_clone, tmp_path / "game", resolve_ref(template_clone, old_ref))
    assert_template_change(game, arrived=False)
    before = tree(game)
    update(game)
    assert_no_conflicts(game)
    assert_template_change(game, arrived=True)
    after = tree(game)
    fresh = tree(
        render_template(template_clone, tmp_path / "fresh", DEFAULT_ANSWERS, vcs_ref="HEAD")
    )
    assert set(after) == set(fresh)
    stale = sorted(str(path) for path in MANAGED if after[str(path)] != fresh[str(path)])
    assert stale == [], "managed files the update did not bring to HEAD"
    touched = sorted(str(path) for path in SEED if after[str(path)] != before[str(path)])
    assert touched == [], "seed files an update must never touch"
    assert run_tool_in_process(game, "validate_docs") == 0
    assert run_tool_in_process(game, "validate_agents") == 0
    commit_all(game.path, "update")
    assert git(game.path, "status", "--porcelain") == ""


def test_update_keeps_game_work(template_clone: Path, tmp_path: Path) -> None:
    game = start_game(template_clone, tmp_path / "game", "HEAD~2")
    assert_template_change(game, arrived=False)
    add_game_page(game)
    (game.path / "README.md").write_text(GAME_README, encoding="utf-8")
    module = game.path / "docs" / "specs" / f"{SLUG}.allium"
    spec = "-- Rewritten by the game.\n" + module.read_text(encoding="utf-8")
    module.write_text(spec, encoding="utf-8")
    (game.path / "src" / "lib" / "components" / "Board.svelte").write_text(BOARD, encoding="utf-8")
    (game.path / "tests" / "board.test.ts").write_text(BOARD_TEST, encoding="utf-8")
    commit_all(game.path, "game work")
    update(game)
    assert_no_conflicts(game)
    assert_template_change(game, arrived=True)
    fresh = render_template(template_clone, tmp_path / "fresh", DEFAULT_ANSWERS, vcs_ref="HEAD")
    assert game.read("docs/project/beans.md") == BEANS_PAGE
    assert game.read("README.md") == GAME_README
    assert game.read(f"docs/specs/{SLUG}.allium") == spec
    assert game.read("src/lib/components/Board.svelte") == BOARD
    assert game.read("tests/board.test.ts") == BOARD_TEST
    manifest = game.read("docs/manifest.yml")
    assert manifest.replace(",\n" + BEANS_ENTRY + "\n", "\n") == fresh.read("docs/manifest.yml")
    expected_map = fresh.read("docs/README.md").rstrip("\n") + "\n\n" + BEANS_LINK + "\n"
    assert game.read("docs/README.md") == expected_map
    for path in sorted(str(path) for path in MANAGED):
        if path not in {"docs/manifest.yml", "docs/README.md"}:
            assert game.read(path) == fresh.read(path), (
                f"{path} did not take the template's change"
            )
    assert run_tool_in_process(game, "validate_docs") == 0
