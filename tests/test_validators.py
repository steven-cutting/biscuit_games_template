"""The two validators the render pins pass on it, and are proved to be live."""

from __future__ import annotations

from typing import TYPE_CHECKING

from tests.helpers import Render, run_tool_in_process

if TYPE_CHECKING:
    import pytest


def test_validate_docs_passes(git_render: Render) -> None:
    assert run_tool_in_process(git_render, "validate_docs") == 0


def test_validate_agents_passes(git_render: Render) -> None:
    assert run_tool_in_process(git_render, "validate_agents") == 0


def test_validate_docs_is_live(git_render: Render, capsys: pytest.CaptureFixture[str]) -> None:
    page = git_render.path / "docs/reference/commands.md"
    page.write_text(page.read_text(encoding="utf-8") + "\nTODO: prove the gate reads this\n")
    assert run_tool_in_process(git_render, "validate_docs") == 1
    assert "an unfinished marker" in capsys.readouterr().err


def test_validate_agents_is_live(git_render: Render) -> None:
    (git_render.path / ".claude/skills/fix-quality/SKILL.md").unlink()
    assert run_tool_in_process(git_render, "validate_agents") == 1
