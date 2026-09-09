---
id: T10
title: Harness completion: update, questionnaire and full-mode tests, the full CI job, the final inventory
status: open
depends_on: [T01, T02, T03, T04, T05, T06, T07, T08, T09]
parallel_with: []
branch: ticket/t10-harness-completion
estimated_size: L
---

# T10: Harness completion: update, questionnaire and full-mode tests, the full CI job, the final inventory

## Context

The template's only product is a render that passes its own `just check` on the first
run and takes later toolchain changes through `copier update` (CONVENTIONS.md §0, §1).
T00 built the harness core (`tests/conftest.py`, `tests/helpers.py`,
`tests/inventory.py`, `tests/test_render.py`, `tests/test_validators.py`) and the `fast`
CI job; T01 to T09 replaced every stub under `template/` with its final content. Three
things are still unproved when this ticket starts: that `copier update` carries a
template change into a game without touching the game's own work, that the
questionnaire refuses what CONVENTIONS.md §3 says it refuses, and that a render passes
its whole gate on a first run. This ticket adds the three test modules that prove them,
the `full` CI job that runs the last one, and reconciles `tests/inventory.py` against the
merged tree so that every rendered path is classified.

Position in the order: every lane (T01 to T09) has merged to `main` before this ticket
starts. T11 (first green render, tag `v0.1.0`, the consumer render) waits for it, and
C06 reads `tests/inventory.py` as the single source of the classification.

Read first, in this order:

1. CONVENTIONS.md §2, §3, §5, §9, §11, §12, §13.
2. The harness as T00 left it, in this repository: `tests/conftest.py` (`TEMPLATE_ROOT`,
   `DEFAULT_ANSWERS`, the `default_render` and `git_render` fixtures, the `network` and
   `full` skip logic), `tests/helpers.py` (`Render`, `render_template`,
   `run_script_in_process`, `git`, `commit_all`), `tests/inventory.py` (`MANAGED`,
   `SEED`, `GAME_EDITED`), `tests/test_render.py` (`test_inventory_matches_classification`),
   `Justfile` (`test`, `test-full`, `render`), `pyproject.toml` (markers, `--timeout`,
   the ruff waivers for `tests/**`), `.github/workflows/ci.yml` (the `fast` job).
3. What the render runs on a first run, at the pinned commits (CONVENTIONS.md §0):
   - `/Users/scutting/projects/biscuit_games/scripts/initialize.sh` line 7 (needs a git
     worktree), 9-13 (writes `uv.lock` and `package-lock.json`, then installs), 19
     (Chromium), 27-30 (Linux needs `just storybook-browsers-deps`, which asks for sudo),
     36 (allium), 40-42 (ruff, ruff format and `npm run lint:fix` rewrite files that are
     not format-clean), 52-57 (hooks installed only from a primary checkout).
   - `/Users/scutting/projects/poodl/scripts/run_project_check.py` lines 18-30
     (`RECIPES`), 53-55 and 72-77 (the snapshot covers untracked files too), 93-119
     (`run`: every recipe must leave the worktree unchanged).
   - `/Users/scutting/projects/poodl/Justfile` lines 14-15 (`initialize`), 55-56
     (`storybook-browsers-deps`), 167-168 (`check`).
   - `/Users/scutting/projects/poodl/.gitignore` lines 2, 7, 12, 16-17, 19-22, 31 and 36:
     what `just initialize` writes that git never sees (the template's copy is P's minus
     lines 24-26). Only `package-lock.json` and `uv.lock` remain visible.
   - `/Users/scutting/projects/poodl/package.json` lines 22-23 (`lint`, `lint:fix`) and
     30-31 (`storybook:browsers`, `storybook:browsers:deps`).
   - `/Users/scutting/projects/poodl/.github/workflows/ci.yml` lines 27, 30, 44 and 150
     (the action SHAs), 148-155 (the Playwright cache step the `full` job mirrors),
     156-161 (the token on the install step, never on the job).
   - `/Users/scutting/projects/biscuit_games/scripts/validate_docs.py` lines 22-32
     (frontmatter fields, kinds, forty-word minimum), 138-164 (the manifest is strict
     JSON), 191-219 (`_check_page`), 252-262 (reachability from `docs/README.md`), and
     `/Users/scutting/projects/poodl/docs/manifest.yml` line 4 (one entry per line, the
     shape the game-page fixture below appends).
4. Copier 9.18.2 and dunamai, in the template venv (locate them with
   `uv run --frozen python -c 'import copier, dunamai, pathlib; print(pathlib.Path(copier.__file__).parent, dunamai.__file__)'`):
   `copier/_main.py` lines 650-651 (answers passed as `data=` are parsed and validated),
   1337-1381 (`run_update` guards: git-tracked, clean, versions detectable, no downgrade,
   `overwrite`), 1645-1646 (the marker bytes), 1838-1860 (the `run_update` signature);
   `copier/_user_data.py` 458-466 (`validate_answer` raises `ValueError` with the
   message the questionnaire tests match); `copier/_vcs.py` 39-46 (copier's git calls
   carry their own identity, so CI needs none), 401-420 (a dirty local template rendered
   at `HEAD` is folded into a draft commit in copier's clone), 428 (`checkout -f <ref>`,
   which is why `HEAD~1` works as a `vcs_ref`); `copier/_subproject.py` 39-49
   (`is_dirty`); `copier/_template.py` 649-670 (version detection through dunamai);
   `dunamai/__init__.py` 42-47 (`VERSION_SOURCE_PATTERN`), 113-135 (`Pattern`), 1236 and
   1265 (with no tag, the distance is `git rev-list --count HEAD`, so `HEAD~1` and
   `HEAD` sort correctly without a tag).

## Goal

- `tests/test_questionnaire.py`, `tests/test_update.py` and `tests/test_full.py` exist,
  pass `just lint` and `just typecheck`, and are green: the first two inside `just test`
  (offline), the third under `just test-full` with a `read:packages` token in `~/.npmrc`.
- `tests/inventory.py` classifies every path the merged template renders, no more and
  no fewer, with `GAME_EDITED` equal to the fourteen `M†` paths CONVENTIONS.md §4 marks
  and §5 lists.
- `.github/workflows/ci.yml` carries the `full` job after the unchanged `fast` job, and
  actionlint passes on it.
- The three CONVENTIONS.md §12 claims assigned to T10 are checked and their outcomes
  recorded in the hand-back notes.

## Non-goals

- Making `full` a required check, granting the hub package read access to this
  repository, or changing any repository setting. C03 owns branch protection and the
  order in which the package grant and the required checks are applied
  (CONVENTIONS.md §11). Until that grant exists the `full` job is expected to fail at
  the render's `npm ci`; this ticket states that and does nothing about it.
- Editing `copier.yml`, `template/docs/manifest.yml`, `template/docs/README.md.jinja`,
  `tests/conftest.py`, `tests/helpers.py`, `tests/test_render.py` or `pyproject.toml`.
  A change one of the new tests needs there is handed back as a T00 follow-up on
  `main` (CONVENTIONS.md §11).
- Fixing a render defect that `just test-full` exposes (a file `initialize.sh`'s fixers
  rewrite, a failing gate inside the render, a validator error). The failure is recorded
  with the owning lane named (T01 to T09 by the file's row in CONVENTIONS.md §4) and
  handed back; T11 collects what is left.
- `tests/test_specs.py` (T02), tagging `v0.1.0` and rendering `tic_tac_toe_beans` (T11),
  the template README, CHANGELOG and AGENTS.md (T12), the impact check that reads the
  inventory (C06).

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `tests/test_update.py` | repo | new; CONVENTIONS.md §9 "Tests", exact content in step 4 | Create: the `template_clone` fixture and the two update round trips. |
| `tests/test_questionnaire.py` | repo | new; CONVENTIONS.md §9 "Tests", exact content in step 3 | Create: fourteen refusals and the computed defaults. |
| `tests/test_full.py` | repo | new; CONVENTIONS.md §9 "Tests", exact content in step 5 | Create: `just initialize` then `just check` inside a render, marker `full`. |
| `tests/inventory.py` | repo | T00's file; CONVENTIONS.md §4, §5, §9 | Reconcile against the merged tree: every rendered path classified, `GAME_EDITED` the fourteen `M†` paths, no placeholder left. |
| `.github/workflows/ci.yml` | repo | T00's `fast` job; the `full` job embedded in step 6 | Append the `full` job; `fast` byte-unchanged. |

## Steps

### 1. Baseline and names

1. Create the worktree from `main` (README.md "How to pick up a ticket"), run `just sync`
   and then `just check`. It must be green before anything is written; if it is not, the
   failure belongs to the lane that merged last and is handed back, not fixed here.
2. Read the T00 files listed under Context. The code below uses the CONVENTIONS.md §9
   names (`TEMPLATE_ROOT`, `DEFAULT_ANSWERS`, `Render`, `render_template`,
   `run_script_in_process`, `git`, `commit_all`, `MANAGED`, `SEED`, `GAME_EDITED`) and
   imports `DEFAULT_ANSWERS` and `TEMPLATE_ROOT` from `tests.conftest`. If T00 placed them
   elsewhere (for instance in `tests/helpers.py`, because `tests/inventory.py` needs the
   slug at import time), or spelt the inventory sets as `Path` rather than `str`, use
   T00's names and types and record the substitution in the hand-back notes. Do the same
   for whatever `tests/helpers.py` does to satisfy ruff about `import subprocess`
   (`tests/test_full.py` needs it too; `pyproject.toml` is not this ticket's file).
3. After writing each module run `just format`: the code below is written to ruff's
   settings, but ruff's own layout wins where they differ, and `just lint` checks it.

### 2. `tests/inventory.py`: reconcile against the merged tree

1. Render the merged template and list what is classified against what is rendered:

   ```sh
   rm -rf ai_tmp/render && just render
   uv run --frozen python - <<'EOF'
   from pathlib import Path

   from tests.helpers import Render
   from tests.inventory import GAME_EDITED, MANAGED, SEED

   rendered = {str(path) for path in Render(Path("ai_tmp/render")).files()}
   classified = {str(path) for path in MANAGED} | {str(path) for path in SEED} | {".copier-answers.yml"}
   print("rendered but unclassified:", sorted(rendered - classified))
   print("classified but not rendered:", sorted(classified - rendered))
   print("in both sets:", sorted({str(p) for p in MANAGED} & {str(p) for p in SEED}))
   print("game-edited outside managed:", sorted({str(p) for p in GAME_EDITED} - {str(p) for p in MANAGED}))
   EOF
   ```

   All four lists must be empty when this step is done.
2. A rendered path that is unclassified is added with the class CONVENTIONS.md §4 gives
   its row (S when its rendered path matches one of the fourteen `_skip_if_exists`
   patterns of CONVENTIONS.md §3, M otherwise). A rendered path that §4 does not list at
   all is not added silently: it is a design change, handed back as a CONVENTIONS.md pull
   request on `main`, and named in the hand-back notes. A classified path the render
   lacks means a lane dropped a file: hand it back to that lane.
3. `GAME_EDITED` is exactly the fourteen paths §4 marks `M†`, which are the ones §5
   lists under "Managed files the game is expected to edit": `docs/manifest.yml`,
   `docs/README.md`, `AGENTS.md`, `Justfile`, `package.json`, `eslint.config.js`,
   `.gitignore`, `.prettierignore`, `lychee.toml`, `.pre-commit-config.yaml`,
   `.pre-commit-fix.yaml`, `pyproject.toml`, `src/lib/config.ts`, `tests/ports.test.ts`.
4. Remove any placeholder T00 left in the module (a comment deferring to this ticket, a
   commented-out entry). The module's docstring says what the three sets are and that
   `tests/test_render.py` and C06 read them; nothing else.
5. `just test` must pass `test_inventory_matches_classification` afterwards.

### 3. `tests/test_questionnaire.py`

Write the module below. Each case renders into a fresh directory, so the file takes
about fifteen seconds; each bad value trips exactly one validator branch of
CONVENTIONS.md §3, and the `match=` string is the prefix `copier/_user_data.py` line
466 formats.

```python
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
```

Check: `just test tests/test_questionnaire.py -v` reports 15 passed. A refusal that
does not raise, or raises something other than `ValueError` with that prefix, settles
the third open point negatively: record the actual exception and message, adapt the
`match=` (never weaken it to a bare `Exception`), and say so in the hand-back notes.

### 4. `tests/test_update.py`

Write the module below. It proves CONVENTIONS.md §5: a template change reaches a game's
managed files by three-way merge, a seed is never touched, a game-added file is never
touched, and the game's own entries at the end of `docs/manifest.yml` and
`docs/README.md` survive because they sit in a different hunk from the template's.

Two mechanics the code depends on:

- Both refs must live in one `_src_path` (`copier/_subproject.py` 73-81 rebuilds the old
  template from the answers file), and no test may commit to or tag the real repository.
  So the fixture clones the repository into a temporary directory and, when the worktree
  is dirty, folds the uncommitted tree into a draft commit in the clone only, which is
  copier's own trick (`copier/_vcs.py` 401-420). `HEAD~1` in CI is `main` on a pull
  request (HEAD is the merge commit) and the previous `main` on a push; locally with a
  dirty tree it is the committed HEAD, so the test reads "does my uncommitted change
  update cleanly from what is committed".
- The clone must end with a populated, clean working tree. A `--no-checkout` clone has an
  empty one, and after the draft commit its index already matches HEAD, so a plain
  `git checkout HEAD` writes nothing and `git status` then reports every file deleted.
  Copier reads that status before rendering `HEAD` (`copier/_subproject.py` 39-49,
  `copier/_vcs.py` 401-420) and would fold "everything deleted" into a draft commit of
  its own. `git checkout -q -f HEAD` is what writes the tree out.

```python
"""`copier update` round trips: a pristine game equals a fresh render; game work survives."""

from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING

import copier
import pytest

from tests.conftest import DEFAULT_ANSWERS, TEMPLATE_ROOT
from tests.helpers import Render, commit_all, git, render_template, run_script_in_process
from tests.inventory import MANAGED, SEED

if TYPE_CHECKING:
    from pathlib import Path

MARKERS = (b"<<<<<<< before updating", b">>>>>>> after updating")
SLUG = DEFAULT_ANSWERS["game_slug"]
IDENTITY = ("-c", "user.name=template-tests", "-c", "user.email=tests@example.invalid")

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
        pytest.skip("the update round trip needs two commits")
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
    for path in render.files():
        assert path.suffix != ".rej", f"{path} was rejected by git apply"
        content = (render.path / path).read_bytes()
        assert not any(marker in content for marker in MARKERS), f"{path} carries markers"


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


@pytest.mark.parametrize("old_ref", ["HEAD~1", "latest-tag"])
def test_pristine_update_equals_fresh_render(
    template_clone: Path, tmp_path: Path, old_ref: str
) -> None:
    game = start_game(template_clone, tmp_path / "game", resolve_ref(template_clone, old_ref))
    before = tree(game)
    update(game)
    assert_no_conflicts(game)
    after = tree(game)
    fresh = tree(render_template(template_clone, tmp_path / "fresh", DEFAULT_ANSWERS, vcs_ref="HEAD"))
    assert set(after) == set(fresh)
    stale = sorted(str(path) for path in MANAGED if after[str(path)] != fresh[str(path)])
    assert stale == [], "managed files the update did not bring to HEAD"
    touched = sorted(str(path) for path in SEED if after[str(path)] != before[str(path)])
    assert touched == [], "seed files an update must never touch"
    assert run_script_in_process(game, "validate_docs.py") == 0
    assert run_script_in_process(game, "validate_agents.py") == 0
    commit_all(game.path, "update")
    assert git(game.path, "status", "--porcelain") == ""


def test_update_keeps_game_work(template_clone: Path, tmp_path: Path) -> None:
    game = start_game(template_clone, tmp_path / "game", "HEAD~1")
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
            assert game.read(path) == fresh.read(path), f"{path} did not take the template's change"
    assert run_script_in_process(game, "validate_docs.py") == 0
```

What a failure means, for the hand-back notes: a marker or a `.rej` file is a same-hunk
collision; a `stale` entry is a managed file the update did not deliver; a `touched`
entry is an update reaching a seed; a path in one of the two sets only is a seed added
or removed between the refs, which the frozen inventory of CONVENTIONS.md §5 forbids
after `v0.1.0`; a mismatch on `docs/manifest.yml` after `test_update_keeps_game_work`
means a template change touched the last decision line, which is the collision the
bottom-append convention exists to avoid.

Check: `just test tests/test_update.py -v` reports
`test_pristine_update_equals_fresh_render[HEAD~1] PASSED`,
`test_pristine_update_equals_fresh_render[latest-tag] SKIPPED` (no tag exists before
T11) and `test_update_keeps_game_work PASSED`, in well under a minute.

### 5. `tests/test_full.py`

Write the module below. The render is committed before `just initialize` runs, because
"the untracked set is exactly the two lockfiles" is only defined against a commit, and
because a tracked file that `initialize.sh` lines 40-42 rewrite then shows as modified
(an `M` in the second column of `git status --porcelain`), which is the loud failure
wanted: the template must ship format-clean files. `just check` is `run_project_check.py run`, which snapshots tracked and untracked
files before the first recipe and fails if any recipe changes one, so the final status
assertion is the same claim from outside.

```python
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
```

Notes:

- The `timeout` marker is pytest-timeout's; it overrides the `--timeout=1800` in
  `pyproject.toml` for this one test, which needs ten to twenty minutes on a warm
  machine and longer on a cold one.
- `just storybook-browsers-deps` runs `playwright install-deps`, which uses sudo, so
  the test runs it only where `CI` is `true` on Linux (GitHub runners have passwordless
  sudo). **Authorisation required:** if the executing machine is Linux, do not run that
  recipe by hand without asking the maintainer; on macOS there is nothing to install.
- Locally the render's `npm ci` reads the token from `~/.npmrc`, where the line
  `//npm.pkg.github.com/:_authToken=<your token>` must exist (CONVENTIONS.md §11:
  never write the token anywhere else, and never quote it in the hand-back notes). In CI
  it reads `NODE_AUTH_TOKEN` through the user-level config that setup-node writes.
- Run it as `just test-full tests/test_full.py -v -s` so the recipes' output is visible;
  `just test-full` alone runs the whole suite, `network` and `full` included, and is the
  acceptance command.

### 6. `.github/workflows/ci.yml`: the `full` job

Append the job below after `fast`, under the existing `jobs:` key. Nothing above `jobs:`
and nothing in `fast` changes. The action SHAs are Poodl's (P `ci.yml` lines 27, 30, 44,
150); the `NODE_AUTH_TOKEN` sits on the one step that installs, as P lines 156-161 do;
there is no `cache: npm` because the lockfile it would key on is created inside the
render, in a temporary directory; the Playwright cache is keyed on the shipped manifest
for the same reason.

```yaml
  full:
    runs-on: ubuntu-latest
    timeout-minutes: 60
    permissions:
      contents: read
      # The render installs @steven-cutting/biscuit-games with the run's own
      # token. That works only once the package grants this repository read
      # access, a per-package setting; see README "Bootstrap of this repository".
      packages: read
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
          fetch-depth: 0
      - uses: actions/setup-node@820762786026740c76f36085b0efc47a31fe5020 # v7.0.0
        with:
          node-version: '26'
          # No `cache: npm`: the lockfile it would key on is created inside the
          # render, in a temporary directory, and setup-node fails when the
          # dependency path it is given does not exist.
          registry-url: 'https://npm.pkg.github.com'
          scope: '@steven-cutting'
      - uses: astral-sh/setup-uv@c771a70e6277c0a99b617c7a806ffedaca235ff9 # v9.0.0
        with:
          version: 0.11.18
          enable-cache: true
          cache-dependency-glob: uv.lock
      - run: uv python install 3.14
      - run: uv tool install rust-just==1.51.0
      - run: npm install --global npm@11.17.0
      # Restored before the render's install, as Poodl's stories job does.
      - uses: actions/cache@0057852bfaa89a56745cba8c7296529d2fc39830 # v4.3.0
        with:
          path: ~/.cache/ms-playwright
          # Keyed on the shipped manifest, because the lockfile that would
          # normally key this does not exist until `just initialize` runs.
          key: ${{ runner.os }}-playwright-${{ hashFiles('template/package.json.jinja') }}
          restore-keys: |
            ${{ runner.os }}-playwright-
      - run: just sync
      - run: just test-full
        env:
          # On the step that installs, never on the job. setup-node wrote the
          # registry into a user config under RUNNER_TEMP; the render's npm
          # inherits it and reads the token from here.
          NODE_AUTH_TOKEN: ${{ github.token }}
```

State plainly, in the pull request description and the hand-back notes: this ticket
does not make `full` a required check and changes no repository setting. Until the hub
package grants `steven-cutting/biscuit_games_template` read access (a per-package
setting in the GitHub UI, applied by C03 in the order C03 states), the job fails at the
render's `npm ci` with a 401 or 403 from `npm.pkg.github.com`; that is expected and is
not a defect in this ticket. `fast` stays the one required check.

Check: `uv run --frozen prek run --all-files actionlint check-yaml` passes;
`grep -n '^  full:' .github/workflows/ci.yml` prints one line.

### 7. The open-point checks

Run the commands under Open points, in the template worktree, and record each outcome
verbatim in the hand-back notes before the final `just check`.

### 8. Commit

Commit on `ticket/t10-harness-completion` with the ticket's `status:` set to `done` in
the same commit. **Authorisation required:** pushing the branch and opening the pull
request are separately authorised (CONVENTIONS.md §11); stop and ask. No other
authorised action occurs in this ticket.

## Acceptance criteria

- [ ] `just check` is green on the ticket branch: `lock-check`, `lint` (actionlint over
      the new job included), `typecheck` (mypy strict over the three new modules) and
      `test`.
- [ ] `tests/test_questionnaire.py`: 15 passed; the fourteen refusals are the values in
      step 3, each matched on `Validation error for question '<name>'`.
- [ ] `tests/test_update.py`: `test_pristine_update_equals_fresh_render[HEAD~1]` and
      `test_update_keeps_game_work` passed; `[latest-tag]` skipped with the reason
      "no v* tag yet"; no tag or commit was made in the real repository (`git tag` in
      the worktree lists nothing new; `git log` shows only the ticket's commits).
- [ ] `tests/test_full.py`: `test_render_passes_its_own_gate` passed under
      `just test-full` with a `read:packages` token in `~/.npmrc`, and the whole
      `just test-full` run (which includes `tests/test_specs.py`) is green.
- [ ] `tests/inventory.py`: the four lists in step 2 are empty; `GAME_EDITED` is the fourteen
      paths; no placeholder comment or entry remains.
- [ ] `.github/workflows/ci.yml`: `fast` is byte-identical to `main`'s; `full` is exactly
      the yaml in step 6; `fetch-depth: 0` in both jobs.
- [ ] Nothing outside the Files touched table changed, other than this ticket's
      `status:` line.
- [ ] Every open point below has its outcome recorded in the hand-back notes.
- [ ] No repository setting was changed; `full` is not a required check.

## Verification

From the repository root, on the ticket branch.

```sh
just check
```

Expected: exit 0. The pytest summary shows `tests/test_questionnaire.py` with 15 passed,
`tests/test_update.py` with 2 passed and 1 skipped, `tests/test_full.py` with 1 skipped
(reason `set BISCUIT_TEMPLATE_FULL=1`) and `tests/test_specs.py` skipped unless
`BISCUIT_TEMPLATE_NETWORK=1` is set.

```sh
just test tests/test_update.py tests/test_questionnaire.py -v
```

Expected: the per-test lines named under steps 3 and 4, nothing failed, total under
ninety seconds.

```sh
grep -c '^//npm.pkg.github.com/:_authToken=' ~/.npmrc
just test-full -v
```

Expected: `1` (never print the line itself), then the whole suite green:
`tests/test_specs.py::test_seed_module_is_clean PASSED` and
`tests/test_full.py::test_render_passes_its_own_gate PASSED`, the latter in ten to
twenty minutes. Quote the elapsed time and the render's final line
`All checks passed and the worktree is unchanged.` in the hand-back notes.

```sh
uv run --frozen prek run --all-files actionlint check-yaml
grep -n '^  full:\|^  fast:\|fetch-depth: 0' .github/workflows/ci.yml
git diff main -- .github/workflows/ci.yml | grep -c '^-[^-]'
```

Expected: both hooks report `Passed`; the grep prints `fast:`, `full:` and two
`fetch-depth: 0` lines; the diff removes no line (`0`), so `fast` is unchanged.

```sh
git status --porcelain
git tag --list 'v*'
```

Expected: nothing untracked or modified after the commit; no tag (T11 makes the first).

## Hand-back notes

Filled in by the agent that executes this ticket.

- What was verified and how: the output of every Verification command, quoted,
  including the elapsed time of `just test-full` and the last line of the render's
  `just check`.
- What deviated from the ticket and why: T00 names or types substituted in step 1; any
  questionnaire value whose refusal message differed and how `match=` was adapted; any
  change to the test code above that a lint or type rule forced.
- What was handed back to another ticket: render defects `just test-full` exposed (the
  file, the gate, the owning lane per CONVENTIONS.md §4); any modified-file line after
  `just initialize`; any rendered path CONVENTIONS.md §4 does not list; anything the
  new tests needed in a T00 file.
- Which open points were settled, with each command's output; which are carried
  forward, and to whom.
- The `full` job's first run in CI, if a pull request was opened: which step failed and
  with what status from `npm.pkg.github.com`, so C03 can confirm the grant fixes it.

## Open points

1. CONVENTIONS.md §12: `git clone --no-checkout` of a linked worktree path yields a clone
   whose HEAD is the worktree's HEAD, not the primary checkout's. Check, in the
   `.supacode` worktree, before the first `just test`:

   ```sh
   git rev-parse HEAD
   rm -rf ai_tmp/clone-check && git clone -q --no-checkout "$PWD" ai_tmp/clone-check
   git -C ai_tmp/clone-check rev-parse HEAD && git -C ai_tmp/clone-check branch --show-current
   rm -rf ai_tmp/clone-check
   ```

   Expected: the two SHAs are equal and the branch is `ticket/t10-harness-completion`.
   Then `just test tests/test_update.py -v` on its first run in that worktree passes.
2. CONVENTIONS.md §12: dunamai's `Pattern.DefaultUnprefixed` accepts both `v0.1.0` and
   `0.1.0` tags, and the prerelease form CONVENTIONS.md §10 prescribes. Check:

   ```sh
   uv run --frozen python -c 'import re, dunamai; p = dunamai.Pattern.DefaultUnprefixed.regex(); print(p); print([bool(re.match(p, t)) for t in ("v0.1.0", "0.1.0", "v0.2.0rc1")])'
   ```

   Expected: the printed pattern begins its anchored group with `^v?`, and the list is
   `[True, True, True]`.
3. CONVENTIONS.md §12: `copier.run_copy(..., data=...)` raises
   `ValueError("Validation error for question '<name>': ...")` when a validator fails.
   Check: `just test tests/test_questionnaire.py -v`; expected 15 passed. If a case
   raises a different type or message, record it and adapt as step 3 says.
4. The `template_clone` fixture leaves the clone clean when the worktree is dirty, so
   copier never folds a spurious draft commit. Check, with at least one uncommitted
   change present in the worktree (this ticket's `status:` edit qualifies):

   ```sh
   just test tests/test_update.py -v -W error::copier.errors.DirtyLocalWarning
   ```

   Expected: the same two passes and one skip as without the flag. A
   `DirtyLocalWarning` turned error means copier saw the clone as dirty; the fixture's
   `git checkout -q -f HEAD` is the line to look at.
5. The `full` job cannot go green before C03 applies the package grant. Check: the first
   CI run of the pull request, once pushing is authorised. Expected: `fast` green,
   `full` failing inside `just test-full` at the render's `npm ci` with a 401 or 403;
   record the step and status, and carry the point to C03.
6. The elapsed time of `test_render_passes_its_own_gate` against the job's 60-minute
   limit and the test's own 3600-second timeout. Check: the timing from the local
   `just test-full` run. Expected: under thirty minutes; if it is over forty, say so in
   the hand-back notes so T11 and C03 can raise the limits before `full` is required.
