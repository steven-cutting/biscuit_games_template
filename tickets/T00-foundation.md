---
id: T00
title: "Foundation: copier.yml, template-repository tooling, harness core, manifest, map and stubs for every path"
status: done
depends_on: []
parallel_with: []
branch: ticket/t00-foundation
estimated_size: XL
---

# T00: Foundation: copier.yml, template-repository tooling, harness core, manifest, map and stubs for every path

## Context

This repository (`steven-cutting/biscuit_games_template`, branch `init`, one commit holding a
one-line `README.md`) becomes a Copier template that renders a new Biscuit Games game.
`CONVENTIONS.md` is the design; read it in full before anything else, then `README.md` in
this directory for the worktree rules. This is the first ticket: nothing else can start
until it has merged to `main`, because the nine lane tickets T01 to T09 each replace stubs
this ticket creates, and every lane's definition of done is `just check` green in this
repository, which only this ticket can make true.

Why one large ticket rather than several: the fast suite (`tests/test_render.py`,
`tests/test_validators.py`) can only be green if every path in CONVENTIONS.md §4 exists
from the first commit. The inventory test compares the render against
`tests/inventory.py`; the two validators the render ships walk every page and every skill.
So this ticket ships the whole shape: `copier.yml`, the template repository's own tooling
and gate, the harness core, the complete `docs/manifest.yml` and `docs/README.md.jinja`
(which no lane may touch, CONVENTIONS.md §11), the files CONVENTIONS.md §7 gives exactly,
and a stub for everything else. Lanes replace stubs; they never add, rename or reclassify
a path.

Sources, at the commits CONVENTIONS.md §0 pins (read-only, never modified):

- P = `/Users/scutting/projects/poodl` at `0a46a485`. Read first: `.pre-commit-config.yaml`,
  `.pre-commit-fix.yaml`, `.editorconfig`, `.markdownlint-cli2.jsonc`, `lychee.toml`,
  `docs/manifest.yml`, `docs/README.md`, `docs/decisions/README.md`, `tests/platform.ts`,
  `tests/platformSpecs.test.ts`, `AGENTS.md`, `.agents/skills/*/SKILL.md`,
  `.claude/skills/fix-quality/SKILL.md`, `.github/workflows/ci.yml`.
- H = `/Users/scutting/projects/biscuit_games` at `09b4894a`. Read first:
  `scripts/validate_docs.py` (the page rules: `REQUIRED_FIELDS`, `METADATA_FIELDS`,
  `MINIMUM_WORDS = 40`, `BAD_CONTENT`, reachability from `docs/README.md`) and
  `scripts/validate_agents.py` (`REQUIRED_GUIDANCE`, the 300-word floor, `BRIDGE_BODY`,
  `ADAPTERS`, the eight-word description rule and the `just` / `AGENTS.md` body rule).
- foo/www = `/Users/scutting/projects/foo/www` at `42ed403`. Read `Justfile`,
  `pyproject.toml` and `template/{{ _copier_conf.answers_file }}.jinja` for the shape.

Tooling on the machine, verified: uv 0.11.18, just 1.51.0, node 26.5.1, Python 3.14 via
`uv python install 3.14`, copier 9.18.2. `typos`, `lychee` and `prek` are not on the PATH;
the gate installs them through `uv sync` and the hook cache.

## Goal

At the end of this ticket, on branch `ticket/t00-foundation`:

- `just check` is green (`lock-check`, `lint`, `typecheck`, `test`), and `just render`
  writes a complete game into `ai_tmp/render` in which both shipped validators exit 0
  after `git init`.
- `tests/inventory.py` is the single source of the managed/seed classification and
  `test_inventory_matches_classification` proves the render equals it, that every seed
  path matches `_skip_if_exists`, that no managed path does, and that the two seed lists
  in `copier.yml` are identical.
- `docs/manifest.yml` and `docs/README.md.jinja` are complete and final for `v0.1.0`:
  38 entries, Poodl's grouping, the seed block last.
- Every path in CONVENTIONS.md §4 exists under `template/`, either in final form (the
  §7 files, `tests/platform.ts`) or as a stub that passes every check the fast suite
  runs, so each lane starts green.
- The `fast` CI job exists in `.github/workflows/ci.yml`.

## Non-goals

- The designed lane edits. Every verbatim-class file is P's or H's copy with at most the
  smallest edit that removes a forbidden token (Step 10); T01 (configs), T02 (scripts),
  T03 (workflows and the Copilot adapter), T04 (agent contract), T05 (source skeleton),
  T06 (seed specification) make the edits CONVENTIONS.md §4 and §7 describe.
- Real handbook prose: T07, T08 and T09 replace the page stubs. Only the frontmatter, the
  H1 and the 40-word floor are this ticket's.
- `tests/test_questionnaire.py`, `tests/test_update.py`, `tests/test_full.py` and the
  `full` CI job: T10. `tests/test_specs.py`: T02.
- Tagging `v0.1.0`, rendering `tic_tac_toe_beans`: T11. The real template `README.md`,
  `CHANGELOG.md` entry and `AGENTS.md`: T12.
- Repository settings, branch protection, the package read grant: C03, applied after
  this ticket merges.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `copier.yml` | repo | CONVENTIONS.md §3 | new; copied verbatim |
| `pyproject.toml` | repo | Step 2 (embedded) | new |
| `uv.lock` | repo | `uv lock` | new; committed |
| `Justfile` | repo | CONVENTIONS.md §9 | new; copied verbatim |
| `.gitignore` | repo | Step 3 (embedded) | new |
| `.editorconfig` | repo | P `.editorconfig` plus two sections (Step 3) | new |
| `.markdownlint-cli2.jsonc` | repo | P `.markdownlint-cli2.jsonc`, `ignores` replaced (Step 3) | new |
| `lychee.toml` | repo | Step 3 (embedded) | new |
| `.pre-commit-config.yaml` | repo | Step 4 (embedded) | new |
| `.pre-commit-fix.yaml` | repo | Step 4 (embedded) | new |
| `.python-version` | repo | `3.14` | new |
| `AGENTS.md` | repo | Step 5 (embedded) | new |
| `CLAUDE.md` | repo | `@AGENTS.md` | new |
| `CHANGELOG.md` | repo | Step 5 (embedded) | new |
| `README.md` | repo | Step 5 (embedded) | replaces the one-line stub |
| `.github/workflows/ci.yml` | repo | Step 6 (embedded) | new; `fast` job only |
| `tests/__init__.py` | repo | empty file | new |
| `tests/conftest.py` | repo | Step 7 (embedded) | new |
| `tests/helpers.py` | repo | Step 7 (embedded) | new |
| `tests/inventory.py` | repo | Step 7 (embedded) | new |
| `tests/test_render.py` | repo | Step 7 | new |
| `tests/test_validators.py` | repo | Step 7 (embedded) | new |
| `template/{{ _copier_conf.answers_file }}.jinja` | copier-owned | foo/www, same path | new; two lines |
| `template/docs/manifest.yml` | M† | Step 8 (embedded) | new; complete |
| `template/docs/README.md.jinja` | M† | Step 8 (embedded) | new; complete |
| `template/tests/platform.ts` | M | Step 9 (embedded) | new; final form |
| `template/src/lib/brand.ts.jinja` | S | CONVENTIONS.md §7 | new; final form |
| `template/src/lib/config.ts` | M† | CONVENTIONS.md §7 | new; final form |
| `template/src/lib/components/Lockup.svelte` | S | CONVENTIONS.md §7 | new; final form |
| `template/src/routes/+page.svelte` | S | CONVENTIONS.md §7 | new; final form |
| `template/tests/platformSpecs.test.ts` | M | CONVENTIONS.md §7 plus P lines (Step 9) | new; final form |
| `template/tests/restated.ts` | S | CONVENTIONS.md §7 | new; final form |
| `template/tests/lockup.test.ts` | S | CONVENTIONS.md §7 | new; final form |
| `template/tests/route.test.ts` | S | CONVENTIONS.md §7 | new; final form |
| `template/docs/specs/{{ game_slug }}.allium.jinja` | S | CONVENTIONS.md §7 | new; final form |
| `template/AGENTS.md.jinja` | M† | P `AGENTS.md` with every §7 edit applied (Step 10) | stub |
| every other path in CONVENTIONS.md §4 not listed above | M, M† or S as §4 marks it | P or H as §4 names, or fresh prose (Step 10) | stub |

The table is the whole scope. Nothing outside it is edited except the `status:` line of
this ticket.

## Steps

Work from the repository root on branch `ticket/t00-foundation`. Commit as often as you
like on the branch; the order below is the order that lets `just check` be run early.

### Step 1: `copier.yml`

Write CONVENTIONS.md §3 to `copier.yml`, byte for byte, including the comments. It is a
file no lane may touch, so what lands here is final for `v0.1.0`. Check with
`uv run --frozen python -c 'import yaml; yaml.safe_load(open("copier.yml"))'` once the venv
exists (Step 2).

### Step 2: `pyproject.toml`, `uv.lock`, `Justfile`, `.python-version`

Write `.python-version` as `3.14`. Write `Justfile` as CONVENTIONS.md §9 gives it, byte
for byte. Write `pyproject.toml`:

```toml
[project]
name = "biscuit-games-template"
version = "0.1.0"
description = "Maintainer tooling for the Biscuit Games copier template. The template is under template/; this project only tests it."
requires-python = ">=3.14"
dependencies = [
  "copier==9.18.2",
  "pathspec==0.12.1",
  "PyYAML==6.0.3",
]

[dependency-groups]
dev = [
  "mypy==2.3.0",
  "prek==0.4.12",
  "pytest==9.1.1",
  "pytest-timeout==2.4.0",
  "ruff==0.16.2",
  "types-PyYAML==6.0.12.20250915",
]

[tool.uv]
# No wheel is ever built. This project exists so `uv run --frozen` provides a
# pinned copier, pytest and the hook runner; see README "Maintaining".
package = false
default-groups = ["dev"]

[tool.pytest.ini_options]
addopts = ["-ra", "--strict-config", "--strict-markers", "--timeout=1800"]
testpaths = ["tests"]
xfail_strict = true
markers = [
  "network: downloads the pinned allium binary into the render (BISCUIT_TEMPLATE_NETWORK=1)",
  "full: runs `just initialize` and `just check` inside the render (BISCUIT_TEMPLATE_FULL=1)",
]

[tool.mypy]
python_version = "3.14"
strict = true
files = ["tests"]

[tool.ruff]
line-length = 99
target-version = "py314"
unsafe-fixes = false
src = ["tests", "template/scripts"]

[tool.ruff.lint]
select = [
  "A", "ANN", "ARG", "B", "BLE", "C4", "COM", "DTZ", "E",
  "EM", "EXE", "F", "FA", "FLY", "FURB", "G", "I", "INP", "INT",
  "ISC", "LOG", "N", "PERF", "PGH", "PIE", "PL", "PTH", "PYI",
  "Q", "RET", "RSE", "RUF", "S", "SIM", "SLF", "T10", "TC",
  "TID", "TRY", "UP", "W",
]
ignore = ["COM812", "E501", "ISC001"]
fixable = ["ALL"]
unfixable = []

[tool.ruff.lint.flake8-tidy-imports]
ban-relative-imports = "all"

[tool.ruff.lint.per-file-ignores]
# The harness asserts, shells out to git and to the rendered scripts by design.
"tests/**" = ["PLR2004", "S101", "S404", "S603", "S607"]
# The shipped checkers, linted at source. Same waivers Poodl grants them.
"template/scripts/**" = [
  "ANN", "BLE001", "EM101", "EM102", "INP001", "PLR0912", "PLR0915",
  "PLR2004", "S404", "S603", "S607", "T201", "TRY003",
]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "lf"

[tool.typos.files]
extend-exclude = ["uv.lock"]
```

The `select`, `ignore`, `flake8-tidy-imports` and `template/scripts/**` waivers are P's
`pyproject.toml` lines 27-48 verbatim (P's `scripts/**` block applied to
`template/scripts/**`). The pins `mypy`, `pytest`, `pytest-timeout`, `types-PyYAML` are
foo/www's and `pathspec==0.12.1` is a guess; none has been confirmed on PyPI
(CONVENTIONS.md §12, assigned to this ticket). Confirm them: temporarily write those five
as `>=` constraints, run `uv lock`, read the resolved versions out of `uv.lock`, write
them back as exact `==` pins, run `uv lock` again and then `uv lock --check`. Record the
confirmed pins in the hand-back notes. `copier`, `PyYAML`, `prek` and `ruff` stay as
written; `uv sync` after locking. Commit `uv.lock`.

If `mypy --strict` reports `copier` as untyped, add
`[[tool.mypy.overrides]] module = ["copier", "copier.*"] ignore_missing_imports = true`
and say so in the hand-back notes.

### Step 3: `.gitignore`, `.editorconfig`, `.markdownlint-cli2.jsonc`, `lychee.toml`

`.gitignore`:

```gitignore
.DS_Store
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
.cache/
.lycheecache

# Scratch, and where `just render` lands by default.
ai_tmp/

# Assistant state written on first use.
.claude/settings.local.json
.codex/settings.local.json
```

`.editorconfig`: P's `.editorconfig` (29 lines) verbatim, then append after the `[*.md]`
section:

```ini
# Shipped pages that carry an answer follow the rules of the page they render.
[*.md.jinja]
indent_size = unset
trim_trailing_whitespace = false

# The seed specification module, which renders to an .allium file.
[*.allium.jinja]
indent_size = 4
```

`.markdownlint-cli2.jsonc`: P's file verbatim with the `ignores` array replaced by
`[".venv", "ai_tmp"]`. Shipped `.md` pages under `template/` are linted at source;
`.md.jinja` files never match the `**/*.md` glob and are linted by the render's own gate.

`lychee.toml`: P's with `exclude_path` reduced, because shipped pages link to
`.jinja`-suffixed neighbours the offline checker cannot resolve:

```toml
cache = true
max_retries = 2
max_concurrency = 8
timeout = 20
accept = [200, 204, 206, 429]
exclude_path = [
  ".git",
  ".venv",
  "ai_tmp",
  "template",
]
```

### Step 4: the hook gate

`.pre-commit-config.yaml` is P's reduced to what makes sense at source (no ESLint, no
validator or specification hooks; those run inside pytest against the render). Every
`rev` below is the SHA P's file carries at the same hook; copy them from P's
`.pre-commit-config.yaml` (lines 99, 108, 114, 119, 150, 155, 161) and check they agree.

```yaml
exclude: >-
  (?x)^(
    \.git/|
    \.venv/|
    ai_tmp/|
    uv\.lock$
  )
repos:
  - repo: local
    hooks:
      - id: ruff-check
        name: Ruff lint
        entry: uv run --frozen ruff check --force-exclude
        language: system
        types_or: [python, pyi]

      - id: ruff-format-check
        name: Ruff format check
        entry: uv run --frozen ruff format --check --force-exclude
        language: system
        types_or: [python, pyi]

  - repo: builtin
    hooks:
      - id: check-added-large-files
        args: [--maxkb=768]
      - id: check-case-conflict
      - id: check-executables-have-shebangs
      - id: check-json
      - id: check-merge-conflict
      - id: check-shebang-scripts-are-executable
      - id: check-toml
      - id: check-yaml
      - id: detect-private-key
      # end-of-file-fixer and trailing-whitespace live in .pre-commit-fix.yaml.
      # This config is the read-only gate, so it may report but never repair.

  # The checker's own repository, pinned, for the reason P's file records.
  - repo: https://github.com/editorconfig-checker/editorconfig-checker
    rev: 675b1261a4d9668c357fcd67deb87aed8b881b94 # v3.11.1
    hooks:
      - id: editorconfig-checker
        name: EditorConfig
        types: [text]

  # Root pages, tickets/ and every shipped .md file. Shipped pages that carry an
  # answer are .md.jinja, which this never matches; the render's gate reads those.
  - repo: https://github.com/DavidAnson/markdownlint-cli2
    rev: b82a6c8896e491b9cb377a99ff3412131920681b # v0.23.2
    hooks:
      - id: markdownlint-cli2
        name: markdownlint

  - repo: https://github.com/crate-ci/typos
    rev: bee27e3a4fd1ea2111cf90ab89cd076c870fce14 # v1.48.0
    hooks:
      - id: typos

  # LYCHEE_VERSION leads the arguments and matches the rev comment, for the
  # reason P's file records: without it the hook derives its version from a
  # `git describe` that Git's exported GIT_DIR points at this repository.
  - repo: https://github.com/lycheeverse/lychee
    rev: 2bba271688c1abb1503097a064e6c3bc1d1b6a9b # lychee-v0.24.2
    hooks:
      - id: lychee
        args:
          [
            LYCHEE_VERSION=0.24.2,
            --offline,
            --cache,
            --config,
            lychee.toml,
            --no-progress,
            --root-dir,
            .
          ]
        types: [markdown]

  - repo: https://github.com/shellcheck-py/shellcheck-py
    rev: 745eface02aef23e168a8afb6b5737818efbea95 # v0.11.0.1
    hooks:
      - id: shellcheck

  - repo: https://github.com/rhysd/actionlint
    rev: 914e7df21a07ef503a81201c76d2b11c789d3fca # v1.7.12
    hooks:
      - id: actionlint
        # This repository's own workflows, and the three shipped workflows,
        # which carry no answer and so ship unsuffixed.
        files: ^(\.github|template/\.github)/workflows/.*\.ya?ml$

  - repo: https://github.com/sirwart/ripsecrets
    rev: 7d94620933e79b8acaa0cd9e60e9864b07673d86 # v0.1.11
    hooks:
      - id: ripsecrets
```

`.pre-commit-fix.yaml` mirrors P's `.pre-commit-fix.yaml` with the same reduced
`exclude`:

```yaml
# Mutating counterpart to .pre-commit-config.yaml. Never installed as a hook;
# run it explicitly with `just fix`.
exclude: >-
  (?x)^(
    \.git/|
    \.venv/|
    ai_tmp/|
    uv\.lock$
  )
repos:
  - repo: local
    hooks:
      - id: ruff-fix
        name: Ruff autofix
        entry: uv run --frozen ruff check --fix-only --force-exclude
        language: system
        types_or: [python, pyi]

      - id: ruff-format
        name: Ruff format
        entry: uv run --frozen ruff format --force-exclude
        language: system
        types_or: [python, pyi]

  - repo: builtin
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace

  - repo: https://github.com/DavidAnson/markdownlint-cli2
    rev: b82a6c8896e491b9cb377a99ff3412131920681b # v0.23.2
    hooks:
      - id: markdownlint-cli2
        name: markdownlint fix
        args: [--fix]
```

Run `just install-hooks` once the venv exists. The first `just lint` clones and builds
every hook (about a minute; needs the network).

### Step 5: `AGENTS.md`, `CLAUDE.md`, `CHANGELOG.md`, `README.md`

`CLAUDE.md` is exactly `@AGENTS.md` followed by one newline. `AGENTS.md` (the template
repository does not run `validate_agents.py` on itself; T12 rewrites it):

```markdown
# Instructions for agents working in this repository

This repository is a Copier template, not a game. `template/` is what `copier copy`
renders into a new Biscuit Games game; `tests/` renders it and inspects the result;
`tickets/` is the work breakdown, and `tickets/CONVENTIONS.md` is the design every change
obeys.

Three classes of file live under `template/`, and `tests/inventory.py` records which is
which: managed files are re-rendered into every game on `copier update` and merged with
the game's edits, seed files are rendered once and never touched again, and
`.copier-answers.yml` belongs to Copier. A change to a seed file reaches no existing
game; say so in `CHANGELOG.md` when you make one.

Never edit `template/` without running `just test`, and run `just check` before handing
back. Scratch work goes in `ai_tmp/`, which is gitignored and is where `just render`
writes by default. Pushing, tagging, opening pull requests, filing issues and touching any
other repository are separately authorised actions: stop and ask before each one.
```

`CHANGELOG.md` (Keep a Changelog; the four headings are the ones every release uses):

```markdown
# Changelog

All notable changes to this template are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions
are tags on `main`, and what each level means for a rendered game is stated in
`tickets/CONVENTIONS.md` §10.

## [Unreleased]

### Managed

- The complete template tree, as a shape: every managed file is rendered from Poodl's
  copy or a stub, and the lane tickets under `tickets/` replace each one.

### Seed

- Every seed file, in the form CONVENTIONS §7 gives it or as a stub.

### Questionnaire

- Four questions: `game_name`, `game_slug`, `description`, `repository`.

### Update notes

- Nothing yet; no game has been rendered from this template.

[Unreleased]: https://github.com/steven-cutting/biscuit_games_template/commits/main/
```

`README.md` (minimal; T12 writes the real one):

````markdown
# biscuit_games_template

A [Copier](https://copier.readthedocs.io/en/stable/) template that renders a new Biscuit
Games game: a static SvelteKit site consuming `@steven-cutting/biscuit-games`, carrying
Poodl's toolchain, handbook, agent contract and quality gate in generic form.

The template is under `template/`; `tests/` renders it and inspects the render. The design
is `tickets/CONVENTIONS.md`, and the work breakdown is `tickets/README.md`.

## Maintaining

```sh
just sync          # the pinned toolchain
just check         # lock-check, lint, typecheck, test
just render        # a render with default answers, in ai_tmp/render
just new-game DIR  # ask the questionnaire and render a game into DIR
```

A render has nothing run in it: `git init -b main`, `just initialize` and `just check`
inside it come next, as the message after copy says.
````

### Step 6: `.github/workflows/ci.yml` (the `fast` job only)

Action SHAs are P's `.github/workflows/ci.yml` lines 27 (checkout) and 44 (setup-uv);
check them against P before committing. T10 adds the `full` job.

```yaml
name: CI

on:
  pull_request:
  push:
    # Quoted because a branch named `true`, `false`, `null`, `on`, or `1.0` is
    # valid to Git but is not a string to a YAML 1.1 parser.
    branches: ['main']
  schedule:
    # Weekly. A render's first run depends on a registry, a browser download
    # and a hub package none of which this repository controls, so a green
    # main is re-proved without a change here.
    - cron: '17 6 * * 1'
  workflow_dispatch:

permissions:
  contents: read

concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  # Supersede a pull request's run; never a main or scheduled one.
  cancel-in-progress: ${{ github.event_name == 'pull_request' }}

jobs:
  fast:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
          # The update round trip renders HEAD~1 and the latest tag, and copier
          # reads `git describe`; a shallow clone has none of that.
          fetch-depth: 0
      - uses: astral-sh/setup-uv@c771a70e6277c0a99b617c7a806ffedaca235ff9 # v9.0.0
        with:
          version: 0.11.18
          enable-cache: true
          cache-dependency-glob: uv.lock
      - run: uv python install 3.14
      - run: uv tool install rust-just==1.51.0
      - run: just sync
      - run: just lock-check
      - run: just lint
      - run: just typecheck
      - run: just test
        env:
          # The one download in the fast suite: the pinned allium, checksummed.
          BISCUIT_TEMPLATE_NETWORK: '1'
```

### Step 7: the harness core under `tests/`

`tests/__init__.py` is empty (the `tests.` imports below and ruff's `INP` rules need it).
The API is CONVENTIONS.md §9 "Harness API"; the answer names are §3's.

`tests/conftest.py`:

```python
"""Fixtures shared by the harness: one default render, and a git-initialised copy."""

from __future__ import annotations

import os
import subprocess
from collections.abc import Iterator
from pathlib import Path

import pytest

from tests.helpers import Render, render_template

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

    validate_agents.py lists files with `git ls-files --others`, so `git init`
    is enough for it; the update tests (T10) additionally commit, because
    copier treats untracked files as dirty.
    """
    copy = default_render.copy_to(tmp_path / "game")
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=copy.path, check=True)
    yield copy
```

`tests/helpers.py`:

```python
"""Render the template and run what the render ships."""

from __future__ import annotations

import runpy
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

import copier
import yaml


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
        str(template), destination, data=data, defaults=True, unsafe=False,
        vcs_ref=vcs_ref, quiet=True,
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
        cwd=render.path, check=False, capture_output=True, text=True,
    )


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True
    ).stdout.strip()


def commit_all(cwd: Path, message: str) -> None:
    git(cwd, "add", "-A")
    git(
        cwd, "-c", "user.name=template-tests", "-c", "user.email=tests@example.invalid",
        "commit", "-q", "-m", message, "--no-verify",
    )
```

`tests/inventory.py` is CONVENTIONS.md §4 transcribed to rendered paths, `<slug>` taken
from `DEFAULT_ANSWERS`. `GAME_EDITED` is the fourteen files §5 names under "Managed
files the game is expected to edit", which are exactly the paths §4's tree marks `M†`.

```python
"""The managed/seed classification of every rendered path: the single source."""

from __future__ import annotations

from tests.conftest import DEFAULT_ANSWERS

SLUG = DEFAULT_ANSWERS["game_slug"]

SKILLS = (
    "accessibility-review", "code-review", "fix-quality", "plan-change",
    "project-check", "review-docs", "spec-change", "svelte-change",
)
DECISIONS = (
    "0001-static-site-no-backend", "0002-ports-and-fakes",
    "0003-specs-are-the-source-of-truth", "0004-python-toolchain",
    "0005-component-workshop", "0006-visual-review-in-chromatic",
    "0007-project-managed-allium-cli", "0008-design-system-as-a-package",
    "0009-rendered-from-the-template", "0010-a-project-pages-site",
)
MANAGED_PAGES = (
    "project/repository-map", "project/platform", "tutorials/first-change",
    "how-to/develop-locally", "how-to/test-and-debug",
    "how-to/work-in-the-component-workshop", "how-to/work-with-the-specs",
    "how-to/maintain-dependencies", "how-to/deploy-to-github-pages",
    "how-to/update-from-template",
    "explanation/architecture", "explanation/layering", "explanation/specifications",
    "explanation/accessibility", "explanation/security-model",
    "explanation/quality-philosophy",
    "reference/commands", "reference/configuration", "reference/testing",
    "reference/quality-gates", "reference/documentation-contract",
    "reference/agent-contract",
    "operations/maintenance", "operations/troubleshooting",
)

MANAGED: frozenset[str] = frozenset({
    ".editorconfig", ".gitattributes", ".gitignore", ".markdownlint-cli2.jsonc", ".npmrc",
    ".pre-commit-config.yaml", ".pre-commit-fix.yaml", ".prettierignore",
    ".prettierrc.json", ".python-version", "AGENTS.md", "CLAUDE.md",
    "chromatic.config.json", "eslint.config.js", "lychee.toml", "package.json",
    "pyproject.toml", "svelte.config.js", "tsconfig.json", "vite.config.ts",
    "vitest.config.ts", "vitest.storybook.config.ts", "Justfile",
    ".claude/settings.json", ".github/copilot-instructions.md",
    ".github/workflows/ci.yml", ".github/workflows/chromatic.yml",
    ".github/workflows/pages.yml", ".storybook/main.ts", ".storybook/preview.ts",
    "scripts/check_playwright_browsers.js", "scripts/initialize.sh",
    "scripts/install_allium.py", "scripts/run_allium.py", "scripts/run_project_check.py",
    "scripts/run_ripsecrets_redacted.py", "scripts/validate_docs.py",
    "scripts/validate_agents.py", "static/.nojekyll",
    "src/app.html", "src/app.d.ts", "src/routes/+layout.svelte", "src/routes/+layout.ts",
    "src/lib/config.ts", "src/lib/ports/storage.ts", "src/lib/ports/clock.ts",
    "src/lib/ports/random.ts",
    "tests/setup.ts", "tests/platform.ts", "tests/platformSpecs.test.ts",
    "tests/ports.test.ts", "docs/manifest.yml", "docs/README.md",
    *(f".{provider}/skills/{name}/SKILL.md"
      for provider in ("agents", "claude", "codex") for name in SKILLS),
    *(f"docs/{page}.md" for page in MANAGED_PAGES),
})

SEED: frozenset[str] = frozenset({
    "README.md", "CHANGELOG.md", "SECURITY.md",
    "docs/project/purpose-and-scope.md", "docs/project/terminology.md",
    "docs/decisions/README.md", *(f"docs/decisions/{name}.md" for name in DECISIONS),
    f"docs/specs/{SLUG}.allium",
    "src/lib/brand.ts", "src/lib/components/Lockup.svelte", "src/routes/+page.svelte",
    "stories/Lockup.stories.svelte",
    "tests/restated.ts", "tests/lockup.test.ts", "tests/route.test.ts",
})

# Managed, and expected to be edited by the game (CONVENTIONS §5).
GAME_EDITED: frozenset[str] = frozenset({
    "docs/manifest.yml", "docs/README.md", "AGENTS.md", "Justfile", "package.json",
    "eslint.config.js", ".gitignore", ".prettierignore", "lychee.toml",
    ".pre-commit-config.yaml", ".pre-commit-fix.yaml", "pyproject.toml",
    "src/lib/config.ts", "tests/ports.test.ts",
})
```

Check the transcription: `len(MANAGED) == 101`, `len(SEED) == 24`, `GAME_EDITED <= MANAGED`,
and the render holds 126 files including `.copier-answers.yml`.

`tests/test_render.py` holds the eight offline tests CONVENTIONS.md §9 lists, each over the
session `default_render`; write them from that list, with these specifics:

- `test_inventory_matches_classification`: rendered paths (as POSIX strings) equal
  `MANAGED | SEED | {".copier-answers.yml"}`; parse `copier.yml` with `yaml.safe_load`;
  the `_exclude` entry containing `_copier_operation`, split on line breaks, stripped,
  the `{%` lines dropped, must equal `_skip_if_exists` exactly; build
  `pathspec.PathSpec.from_lines("gitwildmatch", skip)` and assert every `SEED` path
  matches and no `MANAGED` path does. Assert the fourteen patterns are, in order,
  `/README.md`, `/CHANGELOG.md`, `/SECURITY.md`, `/docs/project/purpose-and-scope.md`,
  `/docs/project/terminology.md`, `/docs/decisions/`, `/docs/specs/`, `/src/lib/brand.ts`,
  `/src/lib/components/`, `/src/routes/+page.svelte`, `/stories/`, `/tests/restated.ts`,
  `/tests/lockup.test.ts`, `/tests/route.test.ts`. This test is the check for the
  pathspec claim in CONVENTIONS.md §12 (a leading-and-trailing-slash pattern matches every
  file beneath the directory; an empty rendered `_exclude` line is ignored).
- `test_verbatim_files_are_byte_identical`: for every file under `template/` whose name
  does not end in `.jinja`, the file at the same relative path in the render has the same
  bytes.
- `test_rendered_jinja_files_carry_no_delimiter`: for every `*.jinja` under `template/`,
  the rendered path is the source path minus the suffix with `{{ game_slug }}` replaced by
  `DEFAULT_ANSWERS["game_slug"]` and `{{ _copier_conf.answers_file }}` by
  `.copier-answers.yml`; its text contains none of the three delimiters.
- `test_no_poodl_outside_provenance`: over `text_files()` (which excludes
  `.copier-answers.yml`: a local render writes the template's absolute path there as
  `_src_path`, and that path starts with `/Users/`), decode as UTF-8, lowercase;
  `poodl` only in `AGENTS.md`, `docs/project/platform.md`, `docs/decisions/*.md`,
  `tests/restated.ts`, `tests/platform.ts`; the twelve tokens §9 lists nowhere.
- `test_answers_file_and_provenance`, `test_no_lockfiles_shipped`: as §9.
- `test_pins_agree`: in the three rendered workflows every `node-version:` is `'26'`,
  every setup-uv `version:` is `0.11.18`, `rust-just==1.51.0`, `npm@11.17.0` and
  `uv python install 3.14` appear where the workflow installs the tool; `package.json`
  `volta.node` starts with `26.`, `volta.npm` and `packageManager` carry `11.17.0`;
  `.python-version` is `3.14`; `package.json` `dependencies["@steven-cutting/biscuit-games"]`
  equals `copier.yml`'s `hub_package_version.default` (`1.0.0`, a string).
- `test_managed_pages_link_only_to_stable_pages`: for every `MANAGED` page under `docs/`,
  every relative link target (the validator's `LINK` regex, fragment and title stripped,
  resolved against the page's directory) is a `MANAGED` page or a `docs/decisions/*.md`
  page. The stubs carry no links, so it is trivially green now; it exists so T07 and T08
  are held to it.

`tests/test_validators.py`:

```python
"""The two validators the render ships pass on it, and are proved to be live."""

from __future__ import annotations

import pytest

from tests.helpers import Render, run_script_in_process


def test_validate_docs_passes(git_render: Render) -> None:
    assert run_script_in_process(git_render, "validate_docs.py") == 0


def test_validate_agents_passes(git_render: Render) -> None:
    assert run_script_in_process(git_render, "validate_agents.py") == 0


def test_validate_docs_is_live(git_render: Render, capsys: pytest.CaptureFixture[str]) -> None:
    page = git_render.path / "docs/reference/commands.md"
    page.write_text(page.read_text(encoding="utf-8") + "\nTODO: prove the gate reads this\n")
    assert run_script_in_process(git_render, "validate_docs.py") == 1
    assert "an unfinished marker" in capsys.readouterr().err


def test_validate_agents_is_live(git_render: Render) -> None:
    (git_render.path / ".claude/skills/fix-quality/SKILL.md").unlink()
    assert run_script_in_process(git_render, "validate_agents.py") == 1
```

### Step 8: the answers file, the manifest and the map

`template/{{ _copier_conf.answers_file }}.jinja` is foo/www's file of the same name,
verbatim (two lines):

```yaml
# Managed by Copier. Do not edit by hand; run `copier update` instead.
{{ _copier_answers | to_nice_yaml -}}
```

`template/docs/manifest.yml` is strict JSON in P's layout (one entry per line, a blank line
between groups; `validate_docs.py` parses it with `json.loads`, so no comment can mark the
seed block). Managed entries first in P's grouping, `update-from-template` after
`deploy-to-github-pages`, then the seed block. Titles, kinds, audiences and slugs are P's
`docs/manifest.yml` for every page P has; the six carried decisions keep P's title text
under the new number; 0009 and 0010 are new. Frozen at `v0.1.0`: no lane changes a line.

```json
{
  "schema_version": 1,
  "pages": [
    {"path": "README.md", "title": "Documentation map", "kind": "project", "audience": ["user", "contributor", "maintainer", "operator", "agent"], "canonical_for": ["documentation_navigation"], "requires": []},

    {"path": "project/repository-map.md", "title": "Repository map", "kind": "project", "audience": ["contributor", "maintainer", "agent"], "canonical_for": ["repository_layout"], "requires": []},
    {"path": "project/platform.md", "title": "The platform upstream", "kind": "project", "audience": ["contributor", "maintainer", "agent"], "canonical_for": ["platform_upstream"], "requires": []},

    {"path": "tutorials/first-change.md", "title": "Make your first change", "kind": "tutorial", "audience": ["contributor", "agent"], "canonical_for": ["first_change_tutorial"], "requires": []},

    {"path": "how-to/develop-locally.md", "title": "Develop locally", "kind": "how-to", "audience": ["contributor", "maintainer", "agent"], "canonical_for": ["local_development"], "requires": []},
    {"path": "how-to/test-and-debug.md", "title": "Test and debug", "kind": "how-to", "audience": ["contributor", "maintainer", "agent"], "canonical_for": ["test_workflow"], "requires": []},
    {"path": "how-to/work-in-the-component-workshop.md", "title": "Work in the component workshop", "kind": "how-to", "audience": ["contributor", "maintainer", "agent"], "canonical_for": ["component_workshop"], "requires": []},
    {"path": "how-to/maintain-dependencies.md", "title": "Maintain dependencies", "kind": "how-to", "audience": ["maintainer", "agent"], "canonical_for": ["dependency_maintenance"], "requires": []},
    {"path": "how-to/deploy-to-github-pages.md", "title": "Deploy to GitHub Pages", "kind": "how-to", "audience": ["maintainer", "operator", "agent"], "canonical_for": ["deployment_procedure"], "requires": []},
    {"path": "how-to/update-from-template.md", "title": "Update from the template", "kind": "how-to", "audience": ["maintainer", "agent"], "canonical_for": ["template_update_procedure"], "requires": []},
    {"path": "how-to/work-with-the-specs.md", "title": "Work with the specifications", "kind": "how-to", "audience": ["contributor", "maintainer", "agent"], "canonical_for": ["specification_workflow"], "requires": []},

    {"path": "explanation/architecture.md", "title": "Architecture", "kind": "explanation", "audience": ["contributor", "maintainer", "operator", "agent"], "canonical_for": ["system_architecture"], "requires": []},
    {"path": "explanation/layering.md", "title": "Layering and dependency direction", "kind": "explanation", "audience": ["contributor", "maintainer", "agent"], "canonical_for": ["dependency_boundaries"], "requires": []},
    {"path": "explanation/specifications.md", "title": "Specifications", "kind": "explanation", "audience": ["contributor", "maintainer", "agent"], "canonical_for": ["specification_model"], "requires": []},
    {"path": "explanation/accessibility.md", "title": "Accessibility", "kind": "explanation", "audience": ["user", "contributor", "maintainer", "agent"], "canonical_for": ["accessibility_model"], "requires": []},
    {"path": "explanation/security-model.md", "title": "Security model", "kind": "explanation", "audience": ["user", "contributor", "maintainer", "operator", "agent"], "canonical_for": ["security_model"], "requires": []},
    {"path": "explanation/quality-philosophy.md", "title": "Quality philosophy", "kind": "explanation", "audience": ["contributor", "maintainer", "agent"], "canonical_for": ["quality_philosophy"], "requires": []},

    {"path": "reference/commands.md", "title": "Commands", "kind": "reference", "audience": ["contributor", "maintainer", "operator", "agent"], "canonical_for": ["command_reference"], "requires": []},
    {"path": "reference/configuration.md", "title": "Configuration", "kind": "reference", "audience": ["contributor", "maintainer", "operator", "agent"], "canonical_for": ["configuration_reference"], "requires": []},
    {"path": "reference/testing.md", "title": "Testing", "kind": "reference", "audience": ["contributor", "maintainer", "agent"], "canonical_for": ["testing_reference"], "requires": []},
    {"path": "reference/quality-gates.md", "title": "Quality gates", "kind": "reference", "audience": ["contributor", "maintainer", "agent"], "canonical_for": ["quality_gate_reference"], "requires": []},
    {"path": "reference/documentation-contract.md", "title": "Documentation contract", "kind": "reference", "audience": ["contributor", "maintainer", "agent"], "canonical_for": ["documentation_contract"], "requires": []},
    {"path": "reference/agent-contract.md", "title": "Agent contract", "kind": "reference", "audience": ["contributor", "maintainer", "agent"], "canonical_for": ["agent_contract"], "requires": []},

    {"path": "operations/maintenance.md", "title": "Maintenance", "kind": "operations", "audience": ["maintainer", "operator", "agent"], "canonical_for": ["maintenance_routine"], "requires": []},
    {"path": "operations/troubleshooting.md", "title": "Troubleshooting", "kind": "operations", "audience": ["contributor", "maintainer", "operator", "agent"], "canonical_for": ["troubleshooting"], "requires": []},

    {"path": "project/purpose-and-scope.md", "title": "Purpose and scope", "kind": "project", "audience": ["user", "contributor", "maintainer", "agent"], "canonical_for": ["project_purpose", "project_non_goals"], "requires": []},
    {"path": "project/terminology.md", "title": "Terminology", "kind": "project", "audience": ["contributor", "maintainer", "operator", "agent"], "canonical_for": ["project_terminology"], "requires": []},
    {"path": "decisions/README.md", "title": "Architecture decisions", "kind": "decision", "audience": ["contributor", "maintainer", "agent"], "canonical_for": ["decision_index"], "requires": []},
    {"path": "decisions/0001-static-site-no-backend.md", "title": "Decision 0001: A static site with no backend", "kind": "decision", "audience": ["maintainer", "agent"], "canonical_for": ["decision_no_backend"], "requires": []},
    {"path": "decisions/0002-ports-and-fakes.md", "title": "Decision 0002: Side effects behind ports", "kind": "decision", "audience": ["contributor", "maintainer", "agent"], "canonical_for": ["decision_ports_and_fakes"], "requires": []},
    {"path": "decisions/0003-specs-are-the-source-of-truth.md", "title": "Decision 0003: Specifications decide behaviour", "kind": "decision", "audience": ["contributor", "maintainer", "agent"], "canonical_for": ["decision_spec_first"], "requires": []},
    {"path": "decisions/0004-python-toolchain.md", "title": "Decision 0004: A Python toolchain in a frontend repository", "kind": "decision", "audience": ["maintainer", "agent"], "canonical_for": ["decision_python_toolchain"], "requires": []},
    {"path": "decisions/0005-component-workshop.md", "title": "Decision 0005: A component workshop", "kind": "decision", "audience": ["contributor", "maintainer", "agent"], "canonical_for": ["decision_component_workshop"], "requires": []},
    {"path": "decisions/0006-visual-review-in-chromatic.md", "title": "Decision 0006: Visual review in Chromatic", "kind": "decision", "audience": ["contributor", "maintainer", "agent"], "canonical_for": ["decision_visual_review"], "requires": []},
    {"path": "decisions/0007-project-managed-allium-cli.md", "title": "Decision 0007: A project-managed Allium binary", "kind": "decision", "audience": ["maintainer", "agent"], "canonical_for": ["decision_allium_cli"], "requires": []},
    {"path": "decisions/0008-design-system-as-a-package.md", "title": "Decision 0008: The design system arrives as a package", "kind": "decision", "audience": ["contributor", "maintainer", "agent"], "canonical_for": ["decision_design_system_as_a_package"], "requires": []},
    {"path": "decisions/0009-rendered-from-the-template.md", "title": "Decision 0009: Rendered from the template", "kind": "decision", "audience": ["contributor", "maintainer", "agent"], "canonical_for": ["decision_rendered_from_template"], "requires": []},
    {"path": "decisions/0010-a-project-pages-site.md", "title": "Decision 0010: A project Pages site", "kind": "decision", "audience": ["contributor", "maintainer", "agent"], "canonical_for": ["decision_project_pages_site"], "requires": []}
  ]
}
```

`template/docs/README.md.jinja` is P's `docs/README.md` in P's order with the §8 changes.
It links every managed page and the two seed project pages directly and the ten decisions
through `decisions/README.md`, which is what makes every page reachable:

```markdown
---
title: "Documentation map"
kind: "project"
audience: [user, contributor, maintainer, operator, agent]
canonical_for: [documentation_navigation]
requires: []
---

# Documentation map

Every page below is registered in `manifest.yml`, owns at least one topic, and is
reachable from here. That is the whole of the arrangement; the rules behind it are in
[Documentation contract](reference/documentation-contract.md).

Behaviour is specified separately, in Allium, under `docs/specs/`, rooted at
[`{{ game_slug }}.allium`](specs/{{ game_slug }}.allium). Three more modules are the
platform's, arrive inside `@steven-cutting/biscuit-games`, and are compared against this
game's restatements rather than edited here; see
[The platform upstream](project/platform.md). Those files are not part of this handbook;
they are its subject. Start at [Specifications](explanation/specifications.md) to
understand how the two relate.

## Start here

- [Purpose and scope](project/purpose-and-scope.md) — what {{ game_name }} is for, and what it is not.
- [Repository map](project/repository-map.md) — where everything lives.
- [Terminology](project/terminology.md) — the words this repository uses precisely.
- [Make your first change](tutorials/first-change.md) — clone to green gate, once through every layer.

## How to

- [Develop locally](how-to/develop-locally.md)
- [Test and debug](how-to/test-and-debug.md)
- [Work in the component workshop](how-to/work-in-the-component-workshop.md)
- [Work with the specifications](how-to/work-with-the-specs.md)
- [Maintain dependencies](how-to/maintain-dependencies.md)
- [Deploy to GitHub Pages](how-to/deploy-to-github-pages.md)
- [Update from the template](how-to/update-from-template.md)

## Platform

- [The platform upstream](project/platform.md) — what Biscuit Games decides for this game,
  which version of it is installed, and where to read the rest.

## Understand

- [Architecture](explanation/architecture.md) — how a static site with no server is put together.
- [Layering and dependency direction](explanation/layering.md) — which module may import which.
- [Specifications](explanation/specifications.md) — why behaviour is written down before it is built.
- [Accessibility](explanation/accessibility.md) — the obligations the specifications state.
- [Security model](explanation/security-model.md) — what a site with no backend does and does not defend.
- [Quality philosophy](explanation/quality-philosophy.md) — why each gate exists.

## Look up

- [Commands](reference/commands.md)
- [Configuration](reference/configuration.md)
- [Testing](reference/testing.md)
- [Quality gates](reference/quality-gates.md)
- [Documentation contract](reference/documentation-contract.md)
- [Agent contract](reference/agent-contract.md)

## Run it

- [Maintenance](operations/maintenance.md)
- [Troubleshooting](operations/troubleshooting.md)

## Decisions

- [Architecture decisions](decisions/README.md) — the record of what was chosen and why.

## This game

Pages this game adds are listed here, after everything the template manages, so an
update from the template and an addition here land in different places.
```

### Step 9: the files written in final form

`template/tests/platform.ts` is P's `tests/platform.ts` with the comment at lines 12-13
made self-contained and line 19 made generic, plus the `Restatement` addition
CONVENTIONS.md §7 gives after `platformFile`. The whole file (T05 and T06 read it; neither
edits it):

```ts
import { readFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { resolve, sep } from 'node:path';

/**
 * The files `@steven-cutting/biscuit-games` ships, resolved the way a consumer
 * resolves them.
 *
 * Through the package's own `exports` subpaths rather than a path into
 * `node_modules`, so a file the package renames fails here rather than reading
 * as nothing. And through `createRequire` anchored at the project root rather
 * than at `import.meta.url`: under Vitest's SSR transform `import.meta.url` is
 * a served path rooted at `/`, and a resolver anchored there walks a
 * `node_modules` that does not exist.
 *
 * The `node_modules` assertion is the point of the file. A resolve that fell
 * back to a copy inside this repository would stay green while proving nothing
 * about the package this game actually installs, which is the one failure that
 * would make every test below meaningless without saying so.
 */
const PACKAGE = '@steven-cutting/biscuit-games';
const resolver = createRequire(resolve(process.cwd(), 'package.json'));

/** Where the package ships `subpath`, refusing anything outside `node_modules`. */
export function platformPath(subpath: string): string {
  const path = resolver.resolve(`${PACKAGE}/${subpath}`);

  if (!path.split(sep).includes('node_modules')) {
    throw new Error(`${PACKAGE}/${subpath} resolved outside node_modules: ${path}`);
  }

  return path;
}

/** What the package ships at `subpath`, as text. */
export function platformFile(subpath: string): string {
  return readFileSync(platformPath(subpath), 'utf8');
}

/** The three modules the package ships under `specs/`. */
export type PlatformModule = 'appearance.allium' | 'operation.allium' | 'play-surfaces.allium';

/**
 * A run of clauses this game restates from one platform module, word for word.
 *
 * `alias` is the `use` alias `file` reaches its config through when it reaches
 * another module's rather than its own — Poodl's `settings.allium` wrote
 * `game/config.` where the platform wrote `config.` — or null when no
 * normalisation is needed. `tests/restated.ts` holds the game's table.
 */
export interface Restatement {
  module: PlatformModule;
  theirs: string;
  file: string;
  ours: string;
  alias: string | null;
  clauses: readonly string[];
}
```

The nine §7 files are copied from CONVENTIONS.md §7 verbatim: `src/lib/brand.ts.jinja`,
`src/lib/config.ts`, `src/lib/components/Lockup.svelte`, `src/routes/+page.svelte`,
`tests/restated.ts`, `tests/lockup.test.ts`, `tests/route.test.ts`,
`docs/specs/{{ game_slug }}.allium.jinja` (the source file name carries the literal
`{{ game_slug }}`, and the fenced text in §7 is the whole file), and
`tests/platformSpecs.test.ts`, whose §7 text has two splice points: replace the line
`// ... flatten, clauses, figures: Poodl lines 37-100 verbatim ...` with P's
`tests/platformSpecs.test.ts` lines 37-100 (`flatten`, `clauses`, `figures`, with their
comments), and replace the three-line `it('reads the version package.json pins', ...)`
stub with P's lines 181-194 (the comment and the case). T05 and T06 own these files
afterwards and verify them in a render; nothing here runs them.

### Step 10: a stub for every other path in CONVENTIONS.md §4

Rules every stub obeys: no `{{`, `{%` or `{#` after rendering unless the file is
`.svelte`; `.jinja` only on the paths §4 marks `.jinja`, and each such stub uses the answer
§4 names for it, so the suffix is earned; none of the twelve forbidden tokens anywhere,
and `poodl` (any case) only in the five allowed files; no file under `template/` may be
byte-different from its P or H source unless this step says so, because
`test_verbatim_files_are_byte_identical` compares them.

1. **Handbook pages (37 stubs; `docs/README.md` is complete from Step 8).** Each page's
   frontmatter is the six-key block P's pages carry, in P's key order and quoting, equal
   to the page's manifest entry: `title: "..."`, `kind: "..."`,
   `audience: [a, b]`, `canonical_for: [slug]`, `requires: []`. The H1 equals the title.
   The body is 40 or more words of real prose (the validator counts words after
   stripping punctuation; write 50 to be safe) saying what the page will say, taken from
   the page's row in CONVENTIONS.md §8. No unfinished marker the validator's
   `BAD_CONTENT` names, no "insert ... here", no links except in
   `docs/decisions/README.md.jinja`, which must carry the ten-row table linking
   `0001-static-site-no-backend.md` through `0010-a-project-pages-site.md` (P's
   `docs/decisions/README.md` shape) or the ten decisions are unreachable and
   `validate_docs.py` fails. Write fresh prose; do not copy P's pages, which carry Poodl's
   words. A worked example, `docs/reference/commands.md`:

   ```markdown
   ---
   title: "Commands"
   kind: "reference"
   audience: [contributor, maintainer, operator, agent]
   canonical_for: [command_reference]
   requires: []
   ---

   # Commands

   Every recipe the `Justfile` offers, what it runs and what it must not change. The
   `Justfile` is the only supported interface to the checks, so this page is the
   reference for the whole gate: the setup recipes, the formatting recipes, each check
   `just check` runs in order, and the recipes that serve the site or the workshop. It
   is a managed page: the template rewrites it, and a game appends its own recipes below.
   ```

   The `.jinja` pages: `project/purpose-and-scope.md.jinja` and
   `project/terminology.md.jinja` use `{{ game_name }}`; `decisions/README.md.jinja` says
   "how {{ game_name }} is built"; `how-to/deploy-to-github-pages.md.jinja` names
   `{{ pages_url }}` and `{{ base_path }}`; `how-to/update-from-template.md.jinja` names
   `{{ template_url }}`; `decisions/0010-a-project-pages-site.md.jinja` names
   `{{ pages_url }}`. A decision stub may open "Carried from Poodl's decision NNNN"
   (`docs/decisions/*.md` is on the allowlist).
2. **`template/AGENTS.md.jinja`.** P's `AGENTS.md` with every edit CONVENTIONS.md §7
   lists under `AGENTS.md.jinja` applied: lines 10-12, invariant 3 (lines 36-41),
   invariant 6 (lines 50-52), the stack bullet (lines 68-71), and the whole `## Provenance`
   section (lines 145-189) replaced by §7's. Those regions hold every forbidden token P's
   file carries (`word lists` at 37 and 161, `/Users/` at 148, `site-root` at 155, `pnut`
   at 157), so the result is token-free, keeps the six `REQUIRED_GUIDANCE` phrases and the
   300-word floor, and renders `_copier_answers._commit`, which
   `test_answers_file_and_provenance` looks for. T04 verifies it.
3. **Skills, bridges, adapters.** Copy P's `.agents/skills/<name>/SKILL.md`,
   `.claude/skills/<name>/SKILL.md` and `.codex/skills/<name>/SKILL.md` for the eight
   names in `tests/inventory.py` (not `word-list-change`), byte for byte; P's
   `.claude/settings.json`, `CLAUDE.md` and `.github/copilot-instructions.md` byte for
   byte (the validator pins the last two to `ADAPTERS`). T04 applies the §7 skill edits.
4. **Every verbatim-class file.** Copy P's file (H's for `eslint.config.js`,
   `scripts/initialize.sh`, `scripts/install_allium.py`, `scripts/validate_docs.py`,
   `scripts/validate_agents.py`) to the §4 path. `static/.nojekyll` is empty.
   `scripts/initialize.sh` is committed with mode 100755 (`chmod +x` before `git add`;
   `git ls-files -s` shows `100755`). These P files carry a forbidden token and get the
   smallest edit that removes it; every other copy is untouched, and the lane named in
   §4 makes the designed edit later:

   | P file | Token lines | Edit made here |
   | --- | --- | --- |
   | `.gitignore` | 25 (`site-root/`) | delete lines 24-26 |
   | `.prettierignore` | 14 (`Word lists`) | delete line 14 |
   | `package.json` | 2 (`"poodl"`), 20 (`stage_site`) | becomes `package.json.jinja`: `"name": "{{ game_slug }}"`, line 20 deleted |
   | `pyproject.toml` | 2, 4, 15, 56 | becomes `pyproject.toml.jinja`: `name = "{{ game_slug }}-tooling"`; description `"Repository tooling for {{ game_name_escaped }}. Not the application; see package.json for that."`; line 15 `Poodl ships` to `This game ships`; lines 56-58 replaced by `# Lockfiles carry hashes that look like typos.` and line 62 deleted |
   | `svelte.config.js` | 5, 9, 10 | comment lines 4-15 replaced by the §4 sentence, as a comment of the same shape |
   | `Justfile` | 68, 78 | delete lines 68-79 |
   | `.github/workflows/pages.yml` | 16-17, 22 | write CONVENTIONS.md §7's `pages.yml` verbatim (the token-free form is the designed file) |
   | `.storybook/main.ts` | 39, 44, 45 | `Poodl` to `this game`, `Poodl's` to `this game's` |
   | `.storybook/preview.ts` | 46 | `'poodl-simulated-reduced-motion'` to `'game-simulated-reduced-motion'` |
   | `src/routes/+layout.svelte` | 7 | `Poodl's own styles` to `the game's own styles` |
   | `src/routes/+layout.ts` | 1 | `Poodl is served` to `The game is served` |
   | `src/lib/ports/random.ts` | 4 (`statistics.allium`) | write §7's replacement for line 2 and lines 4-8 |
   | `tests/ports.test.ts` | 75-135 (`'poodl:...'`), 218-251 (`Poodl`) | every `'poodl:` to `'game:`; every `Poodl` to `Game` |
   | `stories/Lockup.stories.svelte` | 14, 54, 57, 108 | add `import { GAME_NAME } from '../src/lib/brand';` after line 6 and ``const LOCKUP = `biscuit games / ${GAME_NAME}`;`` after line 11; line 14 to `'This game’s own lockup: the platform’s words and then its own, always lowercase,'`; line 54 to `// The mark's "b" is hidden, so nothing reads "b" before the words.`; line 57 to `await expect(words.textContent).toBe(LOCKUP);`; line 108 to `name: LOCKUP` |

   Confirm with `grep -r -i -E 'poodl|pnut|site-root|stage_site|stage-preview|word list|word-list|words\.allium|daily\.allium|sharing\.allium|statistics\.allium|foo/www|/Users/' template/`
   that only the five allowed files and `tests/platform.ts`'s `Poodl's settings.allium`
   comment remain (that phrase is a forbidden-token false positive only if the checker is
   run over `settings.allium`; it is not one of the twelve).
5. **Seed root files.** `template/SECURITY.md` is P's `SECURITY.md` with lines 28-32
   deleted (the two out-of-scope bullets that name Poodl's answer and its custom links,
   including the decision link) and one paragraph added after P line 7, because GitHub
   offers private vulnerability reporting on public repositories and a game may be
   rendered into a private one (T07 §2 gives the wording, which this step copies):

   ````markdown
   GitHub offers that form on public repositories. While this repository is private, only
   people its owner has added can see it at all, so report to the owner directly instead —
   the account named in this repository's address. Do not open an issue.
   ````

   `template/README.md.jinja`:

   ```markdown
   # {{ game_name }}

   {{ description }}

   A Biscuit Games game: a single-page static site with no backend, no accounts and no
   telemetry, published to GitHub Pages at <{{ pages_url }}> beneath `{{ base_path }}/`.
   This file is the game's own; a template update never touches it.

   ## Quick start

   Put a token carrying `read:packages` in `~/.npmrc`, then `just initialize` and
   `just check`. `just dev` serves the game locally.
   ```

   `template/CHANGELOG.md.jinja`:

   ```markdown
   # Changelog

   All notable changes to {{ game_name }} are documented here.

   The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
   project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

   ## [Unreleased]

   ### Added

   - The repository, rendered from the Biscuit Games template.

   [Unreleased]: {{ repository_url }}/commits/main/
   ```

   T07 writes the real three.

### Step 11: green, then commit

1. `just check`. Fix what fails at its root: a missing path in the render is an
   inventory or stub error, a validator failure names the page or skill, a lint failure
   under `template/` is a copy that drifted from P or H.
2. `just lint` also runs markdownlint, typos and lychee (offline) over `tickets/`. If
   typos flags a word in a ticket, add it under
   `[tool.typos.default.extend-words]` in `pyproject.toml` (a new table below
   `[tool.typos.files]`) and record the entry in the hand-back notes. Lychee needs every
   file `tickets/README.md` links to exist; if one does not, report it rather than
   editing the index.
3. `just render`, then run both validators in `ai_tmp/render` as the Verification
   section shows; delete `ai_tmp/render` afterwards.
4. Set this ticket's `status:` to `done`, commit on `ticket/t00-foundation`.
5. **Authorisation required:** pushing the branch and opening the pull request to
   `main` are separately authorised actions (CONVENTIONS.md §11). Stop and ask; do not
   push. Nothing else in this ticket needs authorisation.

## Acceptance criteria

- [ ] `copier.yml` equals CONVENTIONS.md §3; `Justfile` equals CONVENTIONS.md §9.
- [ ] `uv.lock` is committed; `just lock-check` passes; every Python pin was confirmed
      against PyPI and the confirmed set is in the hand-back notes.
- [ ] `just check` exits 0: `lock-check`, `lint`, `typecheck`, `test` (fast suite:
      `tests/test_render.py`, `tests/test_validators.py`, all passing, none skipped).
- [ ] `test_inventory_matches_classification` passes, which proves the render equals
      `MANAGED | SEED | {".copier-answers.yml"}`, every seed path matches
      `_skip_if_exists`, no managed path does, and the two seed lists are identical.
- [ ] `len(MANAGED) == 101`, `len(SEED) == 24`; `find template -type f | wc -l` prints 126.
- [ ] `just render` writes `ai_tmp/render`; after `git init -q -b main` there, both
      validators exit 0 and print their "Validated" line.
- [ ] `template/docs/manifest.yml` has 38 entries in the Step 8 order;
      `template/docs/README.md.jinja` is the Step 8 file.
- [ ] `template/tests/platform.ts` and the nine §7 files are in final form.
- [ ] `git ls-files -s template/scripts/initialize.sh` shows mode `100755`.
- [ ] No forbidden token under `template/` outside the allowed files (Step 10, item 4).
- [ ] `.github/workflows/ci.yml` defines the `fast` job and no other; `actionlint` passes
      on it and on the three shipped workflows (part of `just lint`).
- [ ] `just lint` is clean over `tickets/`.
- [ ] Nothing outside the Files touched table changed; this ticket's `status:` is `done`.

## Verification

From the repository root, after Step 11:

```sh
just sync && just check
```

Expected: every recipe exits 0; pytest reports the fast suite passed with no failures and
no skips (there are no `network` or `full` tests yet).

```sh
uv run --frozen python -c 'from tests.inventory import MANAGED, SEED, GAME_EDITED; print(len(MANAGED), len(SEED), GAME_EDITED <= MANAGED)'
find template -type f | wc -l
```

Expected: `101 24 True`, then `126`.

```sh
rm -rf ai_tmp/render && just render
git -C ai_tmp/render init -q -b main
uv run --frozen python ai_tmp/render/scripts/validate_docs.py
uv run --frozen python ai_tmp/render/scripts/validate_agents.py
```

Expected: `Rendered into ai_tmp/render`, then `Validated 38 pages and 40 canonical topics.`
and `Validated AGENTS.md, 2 adapters, and 8 skills.` (the topic count is 39 slugs plus
`project_non_goals`; if the number differs, count the `canonical_for` entries and say why).

```sh
grep -r -i -l -E 'poodl' template/ | sort
grep -r -i -E 'pnut|site-root|stage_site|stage-preview|word list|word-list|words\.allium|daily\.allium|sharing\.allium|statistics\.allium|foo/www|/Users/' template/ ; echo "exit=$?"
```

Expected: the first lists only `template/AGENTS.md.jinja`, `template/docs/project/platform.md`
(if its stub mentions Poodl; it need not), `template/docs/decisions/*.md*`,
`template/tests/restated.ts`, `template/tests/platform.ts`; the second prints nothing and
`exit=1`.

```sh
git ls-files -s template/scripts/initialize.sh
uv run --frozen prek run --all-files actionlint
```

Expected: `100755 ...`, and actionlint `Passed`.

## Hand-back notes

### What was verified, and how

Every Verification command, run on the committed tree (`45ce0b7`). Output is quoted; the
one elision is marked.

```text
$ just sync && just check
uv sync --frozen
Checked 32 packages in 0.63ms
uv lock --check
Resolved 33 packages in 3ms
uv run --frozen prek run --all-files
[18 hook lines, every one ending Passed]
uv run --frozen mypy
Success: no issues found in 6 source files
uv run --frozen pytest "$@"
collected 12 items

tests/test_render.py ........                                            [ 66%]
tests/test_validators.py ....                                            [100%]

============================== 12 passed in 2.36s ==============================

$ uv run --frozen python -c 'from tests.inventory import MANAGED, SEED, GAME_EDITED; print(len(MANAGED), len(SEED), GAME_EDITED <= MANAGED)'
101 24 True
$ find template -type f | wc -l
     126

$ rm -rf ai_tmp/render && just render
Rendered into ai_tmp/render
$ git -C ai_tmp/render init -q -b main
$ uv run --frozen python ai_tmp/render/scripts/validate_docs.py
Validated 38 pages and 39 canonical topics.
$ uv run --frozen python ai_tmp/render/scripts/validate_agents.py
Validated AGENTS.md, 2 adapters, and 8 skills.

$ grep -r -i -l -E 'poodl' template/ | sort
template/AGENTS.md.jinja
template/docs/decisions/0001-static-site-no-backend.md
template/docs/decisions/0002-ports-and-fakes.md
template/docs/decisions/0003-specs-are-the-source-of-truth.md
template/docs/decisions/0004-python-toolchain.md
template/docs/decisions/0005-component-workshop.md
template/docs/decisions/0006-visual-review-in-chromatic.md
template/docs/decisions/0007-project-managed-allium-cli.md
template/docs/decisions/0008-design-system-as-a-package.md
template/tests/platform.ts
template/tests/restated.ts
$ grep -r -i -E 'pnut|site-root|stage_site|stage-preview|word list|word-list|words\.allium|daily\.allium|sharing\.allium|statistics\.allium|foo/www|/Users/' template/ ; echo "exit=$?"
exit=1

$ git ls-files -s template/scripts/initialize.sh
100755 4449c7b09c7ee93f5a8110f249d2977f0910183d 0 template/scripts/initialize.sh
$ uv run --frozen prek run --all-files actionlint
Lint GitHub Actions workflow files.......................................Passed
```

Also checked: the 57 verbatim-class copies under `template/` are byte-identical to P
(`0a46a485`) and H (`09b4894a`) by `cmp` against `git show`; `copier.yml`, the §7 files,
`tests/platform.ts`, the manifest and the map were extracted from their fences, not
retyped; the rendered tree holds 126 files and its `.copier-answers.yml` carries the four
default answers plus `_commit` and `_src_path`.

### Python pins

Confirmed with the Step 2 procedure (`>=`, `uv lock`, read `uv.lock`, pin, `uv lock`,
`uv lock --check`):

- `mypy==2.3.1` (the ticket's guess was 2.3.0)
- `pytest==9.1.1`
- `pytest-timeout==2.4.0`
- `types-PyYAML==6.0.12.20260906` (the guess was 6.0.12.20250915)
- `pathspec==1.1.1` (the guess was 0.12.1)

`copier==9.18.2`, `PyYAML==6.0.3`, `prek==0.4.12` and `ruff==0.16.2` stay as written. No
mypy override for `copier` was needed: `mypy --strict` reported nothing.

### typos

No `[tool.typos.default.extend-words]` entry was needed; typos passes over `tickets/` and
`template/`.

### Deviations, and why

- **`just render`, in `Justfile` and CONVENTIONS.md §9, approved by the maintainer.** The
  recipe as §9 gave it failed with `ValueError: Question "game_name" is required`:
  `--defaults` cannot answer `game_name` or `description`, which carry a placeholder and
  no default. The recipe now passes both with `--data`, spelt as `DEFAULT_ANSWERS` spells
  them, and the slug and repository derive. §9's block changed in the same commit, so
  `Justfile` still equals §9.
- **`.prekignore`, new, outside the Files touched table.** Without it prek's workspace
  mode discovers `template/.pre-commit-config.yaml` as a nested project and runs the
  game's own hooks (ESLint, both validators, the allium gates) inside `template/`, where
  none can pass. The file removes `template/` from project discovery only; the root hooks
  still read every file under `template/`.
- **EditorConfig.** `copier.yml`, which is frozen, indents its messages and wrapped Jinja
  lines to odd columns, so `.editorconfig` gains a third section,
  `[copier.yml] indent_size = unset`. And `template/.editorconfig`, Poodl's verbatim, says
  `root = true`, so this repository's `[*.md.jinja]` and `[*.allium.jinja]` sections never
  reach a file under `template/`: `template/AGENTS.md.jinja`'s list continuations failed.
  The editorconfig-checker hook now excludes `^template/.*\.md\.jinja$`, and the render's
  own gate checks those pages as the `.md` files they become. Confirmed with the hook's
  binary: the same file passes beside the root `.editorconfig` alone and fails once
  `template/.editorconfig` sits next to it.
- **pathspec factory.** `test_inventory_matches_classification` builds its `PathSpec` with
  `"gitignore"`, not `"gitwildmatch"`. pathspec 1.1.1 deprecates `gitwildmatch`, and copier
  9.18.2 itself picks `"gitignore"` for pathspec 1.x (`copier/_main.py`,
  `_pathspec_pattern`), so the test matches exactly what copier matches.
- **The Step 7 code is not byte-identical to the ticket.** Ruff flagged three
  annotation-only imports (TC003 `Iterator` in `tests/conftest.py`, TC003 `Path` in
  `tests/helpers.py`, TC002 `pytest` in `tests/test_validators.py`), now under
  `if TYPE_CHECKING:`. `ruff format` then reflowed `tests/helpers.py`,
  `tests/inventory.py` and `tests/test_render.py` to one item per line; no value changed.
- **`test_managed_pages_link_only_to_stable_pages` exempts `docs/README.md`.** The map is
  managed but has to link the two seed project pages and `specs/<slug>.allium` to make
  them reachable, so as Step 7 words it the test fails on the map. Every other managed page
  is held to the rule.
- **The two residue tests list sources with Git.** `git ls-files --cached --others
  --exclude-standard template`, not a filesystem walk, because copier renders what Git
  would add: a gitignored `__pycache__` is neither a source nor rendered.
- **Small choices inside Step 10.** The two `.editorconfig` sections sit after `[*.md]`
  and before `[Makefile]`. `svelte.config.js` lines 4-15 became two comment paragraphs: the
  static-site sentence with "The game", then the §4 sentence. `tests/lockup.test.ts` and
  `tests/route.test.ts` keep the `// tests/...` first line, because each §7 fence holds it
  and T05 checks against exactly §7's text. The stub prose is fresh; decisions 0001 to 0008
  open "Carried from Poodl's decision NNNN" with Poodl's own numbers (0006, 0008, 0011 and
  0013 for 0005 to 0008).
- **`just install-hooks` was not run.** In a linked worktree `prek install` writes to the
  shared `.git/hooks`, which would give the main checkout and every other worktree a hook
  bound to this worktree's virtual environment. Run it once T00 is on `main`.

### Handed back

- **T06 and T07.** The direct copier commands in `T06-seed-specification.md` (open points,
  `--data 'game_name=Tic Tac Toe Beans '`) and `T07-handbook-a.md` (open points,
  `-d 'description=A *marked* game.'`) each pass one of the two required answers, so each
  stops with `Question "..." is required` until it passes the other.
- **T10.** Ruff 0.16.2 formats Python blocks inside Markdown, so `ruff format --check .`
  reports `tickets/T00-foundation.md` and `tickets/T10-harness-completion.md`, and
  `just format` would rewrite them. `just lint` is unaffected: its hooks pass only Python
  files. T10's embedded test code is not ruff-format clean and will need `just format`
  when it lands in `tests/`.
- **T01.** The root `[*.md.jinja]` and `[*.allium.jinja]` sections are inert under
  `template/` (see EditorConfig above); a designed edit to `template/.editorconfig` should
  not assume otherwise.
- **CONVENTIONS.md §9, `pyproject.toml` paragraph.** It lists `tests/**` waivers as
  `["PLR2004", "S101", "S603", "S607"]`; this ticket and the committed file add `S404`.
  Harmless, but the two disagree.
- **This ticket's Step 10 table.** Its ranges for `.gitignore` (delete 24-26) and
  `Justfile` (delete 68-79) each stop one line short of CONVENTIONS.md §4 (24-27 and
  68-80): the blank line after each removed block. §4 wins, so both stubs follow it and
  neither keeps a double blank line.

### Open points settled

- **Python pins.** Confirmed, as above.
- **pathspec matching.** `test_inventory_matches_classification` passes: every seed path
  matches its pattern, `/docs/decisions/`, `/docs/specs/`, `/src/lib/components/` and
  `/stories/` included, and no managed path matches any. `just render` produces all 24 seed
  paths, so the empty rendered `_exclude` block is ignored on a copy.
- **Cloning a linked worktree.** Copier clones this `.supacode` worktree without error. On
  a clean tree the render's `_commit` is the worktree's HEAD (`45ce0b7`), not `main`'s
  (`6ab0b13`); on a dirty tree copier commits the working tree into its clone and warns
  `DirtyLocalWarning: Dirty template changes included automatically.` Copier's own
  `clone` runs `git clone --no-checkout` and then `git checkout -f` (`copier/_vcs.py`),
  the mechanism T10's `template_clone` fixture uses.
- **`just lint` over `tickets/`.** typos flags nothing, and lychee resolves every link
  `tickets/README.md` carries.
- **The topic count.** The validator reports 39, not 40.
  `grep -o 'canonical_for' template/docs/manifest.yml | wc -l` prints 38, and only
  `project/purpose-and-scope.md` carries two slugs, so 38 + 1 = 39; the Verification
  section's "39 slugs plus `project_non_goals`" counts that slug twice. The manifest is
  right.

## Open points

- **Python pins (CONVENTIONS.md §12, this ticket).** `mypy==2.3.0`, `pytest==9.1.1`,
  `pytest-timeout==2.4.0`, `types-PyYAML==6.0.12.20250915`, `pathspec==0.12.1` are
  unconfirmed. Check: the Step 2 procedure (`>=` constraints, `uv lock`, read the
  resolved versions, pin exactly, `uv lock --check`). Record the outcome.
- **pathspec matching (CONVENTIONS.md §12, this ticket).** A gitwildmatch pattern with a
  leading and a trailing slash (`/docs/decisions/`) matches every file beneath the
  directory, and an empty rendered `_exclude` line is ignored. Check:
  `uv run --frozen pytest tests/test_render.py::test_inventory_matches_classification -q`
  and, for the second half, `just render` producing every seed path (a `copy` renders the
  update block empty). If the directory patterns do not match, the seed lists in
  `copier.yml` §3 must change to enumerate files, which is a CONVENTIONS change on `main`:
  stop and report rather than editing.
- **Cloning a linked worktree (CONVENTIONS.md §12 assigns it to T10, but this ticket hits
  it first).** `default_render` renders with `vcs_ref="HEAD"`, so copier clones this
  repository, which in a `.supacode` worktree is a linked worktree whose `.git` is a file.
  Check: the first `just test` run; the failure would be a clone error or a render of the
  wrong commit. Record what happened for T10.
- **`just lint` over `tickets/`.** Whether typos flags any word in `tickets/CONVENTIONS.md`
  or the ticket files, and whether lychee resolves every link `tickets/README.md` carries.
  Check: `just lint`; the remedies are Step 11, item 2.
- **The topic count.** The Verification section expects 40 canonical topics; if the render
  reports another number, the manifest embedded in Step 8 and the count disagree and the
  manifest is right. Check: `grep -o 'canonical_for' template/docs/manifest.yml | wc -l`
  is 38 and one entry carries two slugs.
