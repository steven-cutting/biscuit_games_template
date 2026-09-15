"""The default render, inspected offline: inventory, residue, provenance and pins.

Also the answers the questionnaire refuses because the render's Markdown would read
them as syntax.
"""

from __future__ import annotations

import json
import re
from fnmatch import fnmatchcase
from posixpath import normpath
from typing import TYPE_CHECKING, Any
from urllib.parse import unquote

import pathspec
import pytest
import yaml

from tests.conftest import DEFAULT_ANSWERS, TEMPLATE_ROOT
from tests.helpers import Render, git, render_template
from tests.inventory import MANAGED, SEED

if TYPE_CHECKING:
    from pathlib import Path

TEMPLATE = TEMPLATE_ROOT / "template"
ANSWERS_FILE = ".copier-answers.yml"
DELIMITERS = ("{{", "{%", "{#")

# copier.yml's seed list, in copier.yml's order. `_skip_if_exists` and the
# update-only `_exclude` block must both equal it.
SEED_PATTERNS = (
    "/README.md",
    "/CHANGELOG.md",
    "/SECURITY.md",
    "/docs/project/purpose-and-scope.md",
    "/docs/project/terminology.md",
    "/docs/decisions/",
    "/docs/specs/",
    "/src/lib/brand.ts",
    "/src/lib/components/",
    "/src/routes/+page.svelte",
    "/stories/",
    "/tests/restated.ts",
    "/tests/lockup.test.ts",
    "/tests/route.test.ts",
)

# The only rendered files that may name the game the template was distilled
# from: the provenance each states on purpose.
POODL_ALLOWED = (
    "AGENTS.md",
    "docs/project/platform.md",
    "docs/decisions/*.md",
    "tests/restated.ts",
    "tests/platform.ts",
)
# That game's own vocabulary, which no render carries anywhere. Lowercase,
# because the text is lowercased before the search.
FORBIDDEN = (
    "pnut",
    "site-root",
    "stage_site",
    "stage-preview",
    "word list",
    "word-list",
    "words.allium",
    "daily.allium",
    "sharing.allium",
    "statistics.allium",
    "foo/www",
    "/users/",
)
LOCKFILES = frozenset(
    {
        "bun.lock",
        "bun.lockb",
        "npm-shrinkwrap.json",
        "package-lock.json",
        "pnpm-lock.yaml",
        "uv.lock",
        "yarn.lock",
    }
)
WORKFLOWS = (
    ".github/workflows/ci.yml",
    ".github/workflows/chromatic.yml",
    ".github/workflows/pages.yml",
)
# The one line through which each workflow calls its shared counterpart: the
# reusable workflow pinned to a forty-character commit, with the tag as a comment.
CALLER = re.compile(
    r"^\s*uses: steven-cutting/biscuit_games_tooling/\.github/workflows/"
    r"game-(ci|chromatic|pages)\.yml@([0-9a-f]{40}) # (v\d+\.\d+\.\d+)$",
    re.MULTILINE,
)
# scripts/validate_docs.py `LINK`: an inline link that is not an image.
LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
# One answer per rule the `game_name` and `description` validators hold against
# Markdown (CONVENTIONS §3). Each passes every earlier check, and each made the
# render's markdownlint fail or turned the answer into a heading, list or code block.
MARKDOWN_ANSWERS = (
    ("game_name", "Beans "),
    ("game_name", "- Beans"),
    ("game_name", "Tic <b>Beans</b>"),
    ("game_name", "Tic [Beans][ref]"),
    ("game_name", "Beans at www.example.com"),
    ("game_name", "Beans!"),
    ("game_name", "Beans C#"),
    ("description", "    A three-in-a-row game played with beans."),
    ("description", "# A puzzle game"),
    ("description", "1. A three-in-a-row game"),
    ("description", "A <b>bold</b> three-in-a-row game."),
    ("description", "A [beans][ref] game played with beans."),
    ("description", "A game at https://example.com for beans."),
    ("description", "A beans game, mail beans@example.com today."),
)


def _copier_config() -> dict[str, Any]:
    loaded = yaml.safe_load((TEMPLATE_ROOT / "copier.yml").read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def _template_sources() -> list[str]:
    """Every file under `template/` a render is made from, relative to `template/`.

    Copier clones this repository and commits dirty changes with `git add -A`, so
    what Git would add is what copier sees; a gitignored `__pycache__` is neither.
    """
    listed = git(
        TEMPLATE_ROOT,
        "ls-files",
        "-z",
        "--cached",
        "--others",
        "--exclude-standard",
        "--",
        "template",
    )
    return sorted(
        name.removeprefix("template/")
        for name in listed.split("\0")
        if name and (TEMPLATE_ROOT / name).is_file()
    )


def _rendered_path(source: str) -> str:
    """Where copier writes `source`: the suffix removed and the path's own answers filled in."""
    return (
        source.removesuffix(".jinja")
        .replace("{{ game_slug }}", DEFAULT_ANSWERS["game_slug"])
        .replace("{{ _copier_conf.answers_file }}", ANSWERS_FILE)
    )


def test_inventory_matches_classification(default_render: Render) -> None:
    rendered = {path.as_posix() for path in default_render.files()}
    classified = MANAGED | SEED | {ANSWERS_FILE}
    assert not MANAGED & SEED
    assert sorted(rendered - classified) == []
    assert sorted(classified - rendered) == []

    config = _copier_config()
    skip = config["_skip_if_exists"]
    assert tuple(skip) == SEED_PATTERNS
    [update_block] = [entry for entry in config["_exclude"] if "_copier_operation" in entry]
    update_only = [
        line.strip() for line in update_block.splitlines() if not line.strip().startswith("{%")
    ]
    assert update_only == skip

    # A leading-and-trailing-slash pattern must match every file beneath the
    # directory it names (CONVENTIONS §12). The factory is the one copier itself
    # picks for pathspec 1.x (copier/_main.py, `_pathspec_pattern`).
    spec = pathspec.PathSpec.from_lines("gitignore", skip)
    assert sorted(path for path in SEED if not spec.match_file(path)) == []
    assert sorted(path for path in MANAGED if spec.match_file(path)) == []


def test_verbatim_files_are_byte_identical(default_render: Render) -> None:
    verbatim = [source for source in _template_sources() if not source.endswith(".jinja")]
    assert verbatim
    differing = [
        source
        for source in verbatim
        if not (default_render.path / source).is_file()
        or (default_render.path / source).read_bytes() != (TEMPLATE / source).read_bytes()
    ]
    assert differing == []


def test_rendered_jinja_files_carry_no_delimiter(default_render: Render) -> None:
    templated = [
        _rendered_path(source) for source in _template_sources() if source.endswith(".jinja")
    ]
    assert templated
    residue = {
        rendered: [
            delimiter for delimiter in DELIMITERS if delimiter in default_render.read(rendered)
        ]
        for rendered in templated
    }
    assert {rendered: found for rendered, found in residue.items() if found} == {}


def test_no_poodl_outside_provenance(default_render: Render) -> None:
    mentions: list[str] = []
    tokens: dict[str, list[str]] = {}
    for path in default_render.text_files():
        name = path.as_posix()
        text = (default_render.path / path).read_bytes().decode("utf-8").lower()
        if "poodl" in text and not any(fnmatchcase(name, allowed) for allowed in POODL_ALLOWED):
            mentions.append(name)
        if found := [token for token in FORBIDDEN if token in text]:
            tokens[name] = found
    assert mentions == []
    assert tokens == {}


def test_answers_file_and_provenance(default_render: Render) -> None:
    answers = default_render.answers()
    assert {"_commit", "_src_path", *DEFAULT_ANSWERS} <= answers.keys()
    assert {name: answers[name] for name in DEFAULT_ANSWERS} == DEFAULT_ANSWERS
    commit = answers["_commit"]
    assert isinstance(commit, str)
    assert commit
    assert commit in default_render.read("AGENTS.md")


def test_no_lockfiles_shipped(default_render: Render) -> None:
    assert [path.as_posix() for path in default_render.files() if path.name in LOCKFILES] == []


def test_pins_agree(default_render: Render) -> None:
    # The workflows install no toolchain of their own: each calls a shared workflow in
    # biscuit_games_tooling, whose setup-toolchain action holds the node, npm, uv,
    # Python and just pins. Its README pairs a changed default with a template release
    # moving the same pins below; nothing compares the two here.
    pins: set[tuple[str, str]] = set()
    for name in WORKFLOWS:
        calls = CALLER.findall(default_render.read(name))
        assert [workflow for workflow, _, _ in calls] == [
            name.rpartition("/")[2].removesuffix(".yml")
        ]
        pins |= {(sha, tag) for _, sha, tag in calls}
    # One release of the shared repository, moved in all three at once.
    assert len(pins) == 1

    package = json.loads(default_render.read("package.json"))
    assert package["volta"]["node"].startswith("26.")
    assert package["volta"]["npm"] == "11.17.0"
    assert package["packageManager"] == "npm@11.17.0"
    assert default_render.read(".python-version").strip() == "3.14"
    hub_version = _copier_config()["hub_package_version"]["default"]
    assert hub_version == "1.1.0"
    assert package["dependencies"]["@steven-cutting/biscuit-games"] == hub_version


def test_managed_pages_link_only_to_stable_pages(default_render: Render) -> None:
    managed_pages = {path for path in MANAGED if path.startswith("docs/") and path.endswith(".md")}
    unstable: dict[str, list[str]] = {}
    # The map is exempt: it reaches the seed pages only by linking them, and the
    # seed inventory it links is frozen (CONVENTIONS §5).
    for page in sorted(managed_pages - {"docs/README.md"}):
        for raw in LINK.findall(default_render.read(page)):
            target = raw.strip().split(maxsplit=1)[0].strip("<>")
            path_text = target.partition("#")[0]
            if not path_text or target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = normpath(f"{page.rpartition('/')[0]}/{unquote(path_text)}")
            if resolved not in managed_pages and not fnmatchcase(resolved, "docs/decisions/*.md"):
                unstable.setdefault(page, []).append(raw)
    assert unstable == {}


@pytest.mark.parametrize(("question", "value"), MARKDOWN_ANSWERS)
def test_markdown_syntax_in_an_answer_is_refused(
    tmp_path: Path, question: str, value: str
) -> None:
    with pytest.raises(ValueError, match=f"Validation error for question '{question}'"):
        render_template(TEMPLATE_ROOT, tmp_path / "r", {**DEFAULT_ANSWERS, question: value})


def test_markdown_punctuation_inside_an_answer_is_accepted(tmp_path: Path) -> None:
    answers = {
        **DEFAULT_ANSWERS,
        "game_name": "C# Beans?",
        "description": "A tic_tac_toe game on a 3*3 grid, the #1 pick for `beans`.",
    }
    render = render_template(TEMPLATE_ROOT, tmp_path / "r", answers)
    heading = f"# {answers['game_name']}\n\n{answers['description']}\n"
    assert render.read("README.md").startswith(heading)
