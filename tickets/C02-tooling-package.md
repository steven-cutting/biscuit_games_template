---
id: C02
title: Validators, installers and checkers as an installable dev dependency
status: done
depends_on: [C01]
parallel_with: []
branch: ticket/c02-tooling-package
estimated_size: L
---

# C02: Validators, installers and checkers as an installable dev dependency

## Context

Six Python files exist three times over: in Poodl's `scripts/` (P), in the hub's
`scripts/` (H), and in this template's `template/scripts/` (CONVENTIONS.md §4, the
`scripts/` rows). Verified by diffing P against H at the commits CONVENTIONS.md §0 pins:
`run_allium.py` and `run_ripsecrets_redacted.py` are byte-identical; `install_allium.py`
differs only by H's comment at lines 29-35; `run_project_check.py` differs by the two
entries `"package-build"` and `"package-check"` at H lines 24-25 of `RECIPES`;
`validate_docs.py` differs by H's duplicate-key rejection (H lines 74-78, 122-135 and
142-145); `validate_agents.py` differs by H's exact `BRIDGE_BODY` (H lines 22-25), its
duplicate-key rejection (H lines 127-132) and its unstripped adapter comparison (H line
175). The template ships H's validators and P's runner (CONVENTIONS.md §1, fact 2, and
§4), so a fix to any of them reaches a game only through `copier update`, as a 3-way
merge the game may have edited (CONVENTIONS.md §5). A package pinned in `uv.lock`
reaches a game by a one-line pin bump instead, and `just lock-check` proves the pin.

Two contracts bind the files to their location, and both have to move with them:

- `H/scripts/validate_agents.py` names itself in its own inventory: line 62
  `expected = {Path("AGENTS.md"), Path("scripts/validate_agents.py")}` and line 100
  `named = (*ADAPTERS, "AGENTS.md", "scripts/validate_agents.py")`.
- The hook gate and the recipes name the paths: `P/.pre-commit-config.yaml` entries at
  lines 39, 46, 60, 67 and 164 and `files:` triggers at lines 42, 49, 63 and 70;
  `P/Justfile` lines 44, 133, 136, 149, 156, 164 and 168; `H/scripts/initialize.sh`
  line 36.

Every script derives the repository root from its own location
(`Path(__file__).resolve().parents[1]`: `validate_docs.py:18`, `validate_agents.py:16`,
`install_allium.py:25`, `run_allium.py:32`, `run_project_check.py:17`), and
`run_allium.py:30` imports `install_allium` as a sibling module. An installed package
sits in a virtual environment, nowhere near the repository it checks, so the root has to
come from Git instead.

Where this sits: after T12 and the `v0.1.0` tag, and after C01 has chosen the host
repository. C04 later proposes bumps of the pin this ticket introduces. If C07 has
merged, the Poodl change below arrives as part of Poodl's next `copier update`; if not,
it is a stand-alone pull request. The template releases this as a MAJOR (CONVENTIONS.md
§10): six managed files stop being rendered, and copier removes a managed file from every
game on update, edited or not (CONVENTIONS.md §5 and §13).

The H commit is `09b4894a`, four commits after the tag `v1.0.0` (`dfebaf4`), as
CONVENTIONS.md §0 records. Every H line number here is at `09b4894a`.

Read first: the six files under `H/scripts/`, `P/scripts/run_project_check.py`,
`P/.pre-commit-config.yaml`, `P/Justfile`, `H/docs/reference/published-artefacts.md`
lines 80-98 (the version table this ticket mirrors), and CONVENTIONS.md §4, §5, §9, §10
and §11.

## Goal

A Python package `biscuit_games_tooling` in the repository C01 chose (recommended:
`steven-cutting/biscuit_games_tooling`, public), distributed as a git dependency and
exposing six console scripts: `bg-validate-docs`, `bg-validate-agents`,
`bg-install-allium`, `bg-run-allium`, `bg-project-check` and `bg-ripsecrets`. Every
consumer (the template's render, Poodl, the hub) pins it as one line in
`[dependency-groups].dev`, `uv.lock` records the commit, hooks and recipes call the
console scripts, and the render's `scripts/` holds only `initialize.sh` and
`check_playwright_browsers.js`. The root is `git rev-parse --show-toplevel`; the two
things that differ between consumers, the recipe list and the documentation predicates,
are configuration in `[tool.biscuit-games-tooling]`. A golden test proves the console
scripts say exactly what the scripts they replace said, on a checkout of P at
`0a46a485` and of H at `09b4894a`: byte-identical stdout, stderr and exit status.

The alternative, prek remote hooks (`repo: https://github.com/steven-cutting/biscuit_games_tooling`
with a `rev:` SHA and `language: python`), covers the hook path only: `just check-docs`,
`just check-agents`, `just check-specs`, `just analyse-specs`, `just install-allium`
and `just check` all run the scripts outside prek, so the hooks would need the package
as well, which means two pins for one thing. The uv dependency covers both paths with
one pin. Its cost is that the first `just lock` in a render needs GitHub reachable, which
`npm ci` against GitHub Packages already needs.

## Non-goals

- Changing what any validator checks. The hub's rules move into the package unchanged;
  a rule change is a package release under the version table below, not this ticket.
- Packaging `initialize.sh`, `check_playwright_browsers.js`, the hub's
  `check_release.py` or `smoke_package.sh`. The first two stay in the render; the
  other two are the hub's alone.
- The reusable workflows and the composite action: C01. Proposing pin bumps: C04.
  Classifying the six removals for the template CHANGELOG: C06's check does that; this
  ticket writes the entry by hand.
- Editing decision records that name `scripts/install_allium.py` or `run_allium.py`
  (Poodl's 0004 and 0011, the hub's 0006 and 0007, the template's seed decisions 0004 and
  0007). They record what was true when they were written.
- Touching `docs/manifest.yml` or `docs/README.md.jinja` in the template: no page is
  added, renamed or retitled.

## Files touched

Template files carry `template/`; template-repository files are bare; files in other
repositories are written as `<repository>: <path>` in the Path column, with the
brace idiom of CONVENTIONS.md §4 for groups of files that change the same way.

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `template/pyproject.toml.jinja` | M | P `pyproject.toml` | Pin the package in `dev`; append `[tool.biscuit-games-tooling]` |
| `template/.pre-commit-config.yaml` | M | P | Five entries call console scripts; four triggers rewritten |
| `template/Justfile` | M† | P | Seven recipe lines call console scripts; one comment |
| `template/scripts/initialize.sh` | M | H | Line 36 calls `bg-install-allium`; comment at 32-35 |
| `template/scripts/validate_docs.py` | M | H | Delete: moved into the package |
| `template/scripts/validate_agents.py` | M | H | Delete: moved into the package |
| `template/scripts/install_allium.py` | M | H | Delete: moved into the package |
| `template/scripts/run_allium.py` | M | P | Delete: moved into the package |
| `template/scripts/run_project_check.py` | M | P | Delete: moved into the package |
| `template/scripts/run_ripsecrets_redacted.py` | M | P | Delete: moved into the package |
| `template/AGENTS.md.jinja` | M† | P | Stack bullet (P 176-178) and the Provenance bullet naming the pin |
| `template/.agents/skills/review-docs/SKILL.md` | M | P | Step 1 names `bg-validate-docs` |
| `template/docs/project/repository-map.md` | M | P | Tree line 35 and table row 54 |
| `template/docs/how-to/work-with-the-specs.md` | M | P | Line 87 |
| `template/docs/how-to/maintain-dependencies.md` | M | P | Lines 92 and 130; the checksum block 99-107 moves out; new section |
| `template/docs/how-to/update-from-template.md.jinja` | M | new | One "Steps by version" line |
| `template/docs/reference/commands.md` | M | P | Line 73 |
| `template/docs/reference/quality-gates.md` | M | P | Lines 41 and 82 |
| `template/docs/reference/documentation-contract.md` | M | P | Line 11 |
| `template/docs/reference/agent-contract.md` | M | P | Line 11 |
| `template/docs/explanation/quality-philosophy.md` | M | P | Line 18 |
| `tests/inventory.py` | repo | — | `MANAGED` loses the six script paths |
| `tests/helpers.py` | repo | — | `run_script_in_process` becomes an in-process package runner |
| `tests/test_validators.py` | repo | — | Calls the package, not `scripts/` |
| `tests/test_specs.py` | repo | — | `python -m biscuit_games_tooling.run_allium` |
| `tests/test_render.py` | repo | — | `test_pins_agree` holds the two package pins equal |
| `pyproject.toml` | repo | — | The package in `dev`; `template/scripts` leaves the ruff config |
| `uv.lock` | repo | — | `just lock` |
| `CHANGELOG.md` | repo | — | "Update notes": six managed files removed |
| `biscuit_games_tooling: pyproject.toml` | repo | new | Package metadata, console scripts, ruff |
| `biscuit_games_tooling: src/biscuit_games_tooling/_project.py` | repo | new | `root()`, `settings()`, `recipes()`, `predicates()` |
| `biscuit_games_tooling: src/biscuit_games_tooling/{__init__,validate_docs,validate_agents,install_allium,run_allium,run_project_check,run_ripsecrets_redacted}.py` | repo | H and P scripts | The six modules, ported |
| `biscuit_games_tooling: src/biscuit_games_tooling/py.typed` | repo | new | Empty marker; the template's `mypy --strict` imports the package |
| `biscuit_games_tooling: tests/golden/scripts/*.py` | repo | H `scripts/` | H's six files at `09b4894a`, byte-identical: the baseline |
| `biscuit_games_tooling: tests/test_golden.py` | repo | new | The golden test |
| `biscuit_games_tooling: {README,CHANGELOG}.md` | repo | new | Consumption, version table, `0.1.0` entry |
| `biscuit_games_tooling: {Justfile,.pre-commit-config.yaml,.github/workflows/ci.yml}` | repo | template repository's | `lock-check`, `lint`, `test`, `check` |
| `poodl: {pyproject.toml,uv.lock,.pre-commit-config.yaml,Justfile,scripts/initialize.sh}` | repo | — | As the template rows above |
| `poodl: scripts/{validate_docs,validate_agents,install_allium,run_allium,run_project_check,run_ripsecrets_redacted}.py` | repo | — | Delete |
| `poodl: {AGENTS.md,.agents/skills/review-docs/SKILL.md}` | repo | — | As the template rows above |
| `poodl: docs/{project/repository-map,how-to/work-with-the-specs,how-to/maintain-dependencies,reference/commands,reference/quality-gates,reference/documentation-contract,reference/agent-contract,explanation/quality-philosophy}.md` | repo | — | The same lines as the template rows |
| `biscuit_games: {pyproject.toml,uv.lock,.pre-commit-config.yaml,Justfile,scripts/initialize.sh}` | repo | — | As the template rows; `recipes` lists `package-build` and `package-check` |
| `biscuit_games: scripts/{validate_docs,validate_agents,install_allium,run_allium,run_project_check,run_ripsecrets_redacted}.py` | repo | — | Delete |
| `biscuit_games: .agents/skills/review-docs/SKILL.md` | repo | — | Line 8 |
| `biscuit_games: docs/{project/repository-map,how-to/work-with-the-specs,how-to/maintain-dependencies,reference/commands,reference/quality-gates,reference/documentation-contract,reference/agent-contract,reference/configuration,explanation/quality-philosophy,operations/maintenance,operations/poodl-handover}.md` | repo | — | Lines 74; 120; 93, 102, 148; 73, 101; 43; 11; 11; 142; 17; 46; 700 |

## Steps

1. Settle the host. Read C01's hand-back notes. If `steven-cutting/biscuit_games_tooling`
   exists, the package lives at its root (`pyproject.toml` beside `.github/`; a shared
   tag series, so a workflow release and a package release share a number, which the
   README states). If it does not exist: **Authorisation required:** creating the
   repository, and making it public. Stop and ask. Public is the recommendation: with a
   private repository every `uv lock` and `uv sync` needs a credential for the clone
   (uv reads a token from the URL, `git+https://<token>@github.com/...`, or from the Git
   credential helper, which `gh auth login` or `gh auth setup-git` configures), and a
   consumer's CI would need that token as a stored secret, which no game has today.

2. Write the package's `pyproject.toml`. Shape from `H/pyproject.toml` lines 21-53 for
   ruff (same `select`, `ignore`, format), with the per-file waivers keyed
   `"src/biscuit_games_tooling/**"` and `INP001` dropped from them. The rest:

   ```toml
   [project]
   name = "biscuit-games-tooling"
   version = "0.1.0"
   description = "The checkers, validators and installers every Biscuit Games repository runs."
   requires-python = ">=3.14"
   dependencies = []

   [project.scripts]
   bg-validate-docs = "biscuit_games_tooling.validate_docs:main"
   bg-validate-agents = "biscuit_games_tooling.validate_agents:main"
   bg-install-allium = "biscuit_games_tooling.install_allium:main"
   bg-run-allium = "biscuit_games_tooling.run_allium:main"
   bg-project-check = "biscuit_games_tooling.run_project_check:main"
   bg-ripsecrets = "biscuit_games_tooling.run_ripsecrets_redacted:main"

   [build-system]
   requires = ["uv_build>=0.11,<0.12"]
   build-backend = "uv_build"

   [dependency-groups]
   dev = ["prek==0.4.12", "pytest==9.1.1", "ruff==0.16.2"]
   ```

   `pytest` at the pin the template repository's `pyproject.toml` carries.

3. Write `src/biscuit_games_tooling/_project.py`. Every console script resolves the root
   once, inside `main()`, and passes it down; no module reads the root at import time
   (`install_allium.py` lines 25-27 and `run_project_check.py` line 17 do today, and
   `run_allium.py` line 165 reads `install_allium.BINARY`). Never assign a module global
   from `main()`: `PLW0603` is selected.

   ```python
   """Where the consuming repository is, and what its pyproject.toml asks of the tools.

   Every console script runs from inside a consumer's worktree and takes the
   repository root from Git rather than from its own location, because the
   package is installed into a virtual environment, nowhere near the files it checks.
   """

   from __future__ import annotations

   import subprocess
   import sys
   import tomllib
   from pathlib import Path
   from typing import Any

   # Poodl's `RECIPES` tuple: what `bg-project-check run` executes, in order, before
   # `check-clean`. A consumer with more gates lists them in its pyproject.toml.
   DEFAULT_RECIPES = (
       "lock-check",
       "lint",
       "frontend-static",
       "frontend-coverage",
       "frontend-build",
       "storybook-build",
       "storybook-test",
       "check-docs",
       "check-agents",
       "check-specs",
       "analyse-specs",
   )


   def root() -> Path:
       """The top level of the Git worktree the current directory is inside."""
       result = subprocess.run(
           ["git", "rev-parse", "--show-toplevel"], check=False, capture_output=True, text=True
       )
       if result.returncode != 0:
           print("biscuit-games-tooling: run this from inside a Git worktree", file=sys.stderr)
           raise SystemExit(2)
       return Path(result.stdout.strip())


   def settings(project_root: Path) -> dict[str, Any]:
       """The `[tool.biscuit-games-tooling]` table of the consumer's pyproject.toml, or {}."""
       manifest = project_root / "pyproject.toml"
       if not manifest.is_file():
           return {}
       with manifest.open("rb") as stream:
           return tomllib.load(stream).get("tool", {}).get("biscuit-games-tooling", {})


   def recipes(project_root: Path) -> tuple[str, ...]:
       return tuple(settings(project_root).get("recipes", DEFAULT_RECIPES))


   def predicates(project_root: Path) -> tuple[set[str], set[str]]:
       """Every predicate the consumer declares, and the subset it enables."""
       declared: dict[str, bool] = settings(project_root).get("predicates", {})
       return set(declared), {name for name, enabled in declared.items() if enabled}
   ```

   A render that has not run `git init` resolves to whatever repository encloses it:
   `just render` writes into `ai_tmp/render` inside this worktree, so a console script
   run there before `git init` would read the template repository. `git init -b main`
   is step 2 of `_message_after_copy` (CONVENTIONS.md §3), and the harness's
   `git_render` fixture does it (CONVENTIONS.md §9); verified that a nested `git init`
   makes `--show-toplevel` stop at the render.

4. Port the six modules, each keeping its `if __name__ == "__main__": raise SystemExit(main())`
   so `python -m biscuit_games_tooling.<module>` works (the template harness uses it):
   - `validate_docs.py` from H: `ROOT`, `DOCS`, `MANIFEST` (lines 18-20) and
     `PREDICATES`, `ENABLED` (30-31) become values computed in `main()` from `root()`
     and `predicates()` and passed to the functions that use them; the comment at 26-29
     says the predicates come from the consumer's `pyproject.toml`. Messages unchanged.
   - `validate_agents.py` from H: `ROOT` and `CANONICAL_SKILLS` (16-17) likewise;
     line 62 becomes `expected = {Path("AGENTS.md")}` and line 100
     `named = (*ADAPTERS, "AGENTS.md")`, so a consumer that still carries the old file
     is neither missing nor unexpected. `cwd=ROOT` at line 88 keeps the resolved root.
   - `install_allium.py` from H: `INSTALL_DIRECTORY` and `BINARY` (26-27) become
     `binary(project_root)`; `check(project_root)` stays public for `run_allium`;
     everything printed stays word for word.
   - `run_allium.py`: line 30 becomes `from biscuit_games_tooling import install_allium`
     (`ban-relative-imports = "all"`); `PROJECT_ROOT` (32) is a parameter; lines 161
     and 165 call `install_allium.check(project_root)` and
     `install_allium.binary(project_root)`. The `run_allium:` message prefix at line 209
     stays: the hub's `docs/operations/troubleshooting.md` line 82 quotes it.
   - `run_project_check.py` from P: `PROJECT_ROOT` (17) and `RECIPES` (18-30) become
     `root()` and `recipes()` read once in `main()`; the usage line at 157 says
     `bg-project-check`.
   - `run_ripsecrets_redacted.py`: verbatim; it has no root.
   - Add an empty `py.typed` beside `__init__.py`.

5. Write the golden test. The baseline is H's six scripts at `09b4894a`, copied
   byte-identical into `tests/golden/scripts/`. For each checkout, the fixture clones
   the repository into a temporary directory (`BG_GOLDEN_POODL` and
   `BG_GOLDEN_BISCUIT_GAMES` name local clones; the GitHub URLs are the fallback),
   checks out the pinned commit, copies the baseline scripts over its `scripts/` (they
   derive the root from `__file__`, so they must run from there; for H the copy is a
   no-op) and commits, so `clean` has a clean tree to report on. Then, for each case,
   `sys.executable scripts/<name>.py <args>` and `bg-<name> <args>` run with the same
   `cwd` and the same environment, and `(stdout, stderr, returncode)` must be equal:

   ```python
   CHECKOUTS = {
       "poodl": ("https://github.com/steven-cutting/poodl", "0a46a485"),
       "biscuit_games": ("https://github.com/steven-cutting/biscuit_games", "09b4894a"),
   }
   CASES = [
       ("validate_docs.py", "bg-validate-docs", ()),
       ("validate_agents.py", "bg-validate-agents", ()),
       ("install_allium.py", "bg-install-allium", ("--check",)),
       ("run_project_check.py", "bg-project-check", ("clean",)),
       ("run_ripsecrets_redacted.py", "bg-ripsecrets", ()),
       pytest.param("run_allium.py", "bg-run-allium", ("check",), marks=pytest.mark.network),
       pytest.param("run_allium.py", "bg-run-allium", ("analyse",), marks=pytest.mark.network),
   ]
   ```

   The two `network` cases run `bg-install-allium` in the checkout first (`.tools/` is
   ignored by both repositories: `P/.gitignore` line 31, `H/.gitignore` line 28). The
   `run` subcommand is out of scope: it needs `npm ci` and a browser. The same run
   records `(stdout, stderr, returncode)` per checkout and case under
   `tests/golden/expected/`; later releases compare against the recordings, and a
   deliberate change re-records in the same commit as the version bump that names it.

6. Write the tooling repository's `Justfile` (`sync`, `lock`, `lock-check`, `lint`,
   `test`, `test-network` with `BG_TOOLING_NETWORK=1`, `check: lock-check lint test`),
   its `.pre-commit-config.yaml` (the template repository's reduced gate, CONVENTIONS.md
   §9, without lychee) and a `ci.yml` running `just check` on the template's `fast`
   shape (CONVENTIONS.md §9), plus `just test-network`. Write `README.md`: what the six
   scripts are, the consumption snippet of step 8, the configuration table, the
   checksum recomputation block moved from `P/docs/how-to/maintain-dependencies.md`
   lines 99-107, and the version table in the shape of
   `H/docs/reference/published-artefacts.md` lines 85-98:

   | Change | Level |
   | --- | --- |
   | A tree that passed now fails: an error added, a rule tightened, a phrase added to `REQUIRED_GUIDANCE`, an inventory rule changed | Major |
   | A console script, a configuration key or a recipe name the runner expects removed or renamed | Major |
   | The allium `VERSION` moved: what the checker reports can move in both directions | Major |
   | A check added behind a configuration key whose default keeps today's verdicts | Minor |
   | A console script or a configuration key added, with today's behaviour as the default | Minor |
   | A message reworded with the verdict and the exit status kept, or a comment | Patch |

   `CHANGELOG.md` opens with `0.1.0`: "the six scripts of Poodl and the hub, unchanged
   in what they say". **Authorisation required:** pushing the tooling repository and
   tagging `v0.1.0` (annotated; a tag is never moved, because a consumer's `uv.lock`
   pins the commit behind it and only `uv lock --upgrade-package` re-resolves a tag).

7. Template `pyproject.toml.jinja` (CONVENTIONS.md §4 gives its base). In `dev`, first
   line, then the table appended at the end of the file (CONVENTIONS.md §5):

   ```toml
   [dependency-groups]
   dev = [
     "biscuit-games-tooling @ git+https://github.com/steven-cutting/biscuit_games_tooling@v0.1.0",
     "prek==0.4.12",
     "ruff==0.16.2",
   ]

   [tool.biscuit-games-tooling]
   # What `just check` runs, in order, before `check-clean`. This is the package's
   # default; it is written out so a game that adds a gate appends to it.
   recipes = [
     "lock-check", "lint", "frontend-static", "frontend-coverage", "frontend-build",
     "storybook-build", "storybook-test", "check-docs", "check-agents", "check-specs",
     "analyse-specs",
   ]
   # Predicates a page's `requires` may name, true when enabled. None yet.
   predicates = {}
   ```

   Verified with uv 0.11.18 against a `git+file://` repository: a git URL in `dev` under
   `[tool.uv] package = false` locks, `uv.lock` records `?rev=v0.1.0#<commit>`,
   `uv sync --frozen` installs that commit, `uv run --frozen bg-<name>` works from a
   subdirectory, and `uv lock --check` fails when the tag in `pyproject.toml` changes.
   It passes when the tag moves upstream, which is why tags never move.

8. Template `.pre-commit-config.yaml` (P numbering; the template is one line lower after
   the dropped `src/lib/data/|`). Entries at 39, 46, 60, 67 become
   `uv run --frozen bg-validate-docs`, `uv run --frozen bg-validate-agents`,
   `uv run --frozen bg-run-allium check`, `uv run --frozen bg-run-allium analyse`; line
   164 becomes `entry: uv run --frozen bg-ripsecrets` (the wrapper now needs the
   project environment, so `--no-project` goes). Triggers: 42 becomes
   `files: ^(README\.md|SECURITY\.md|docs/|pyproject\.toml$)`, 49 ends
   `\.github/copilot-instructions\.md|pyproject\.toml$)`, 63 and 70 become
   `files: ^(docs/specs/|pyproject\.toml$)`. `uv.lock` is in the global `exclude` (line
   12), so naming it in a trigger would match nothing; the pin bump edits
   `pyproject.toml`, which is enough. The comment at 55-57 says "the pin" is the
   package version in `pyproject.toml`.

9. Template `Justfile` (P numbering; the template is twelve lines lower after line 67).
   Line 44 `uv run --frozen bg-install-allium`; 133 `uv run --frozen bg-validate-docs`;
   136 `uv run --frozen bg-validate-agents`; 149 `uv run --frozen bg-run-allium check`;
   156 `uv run --frozen bg-run-allium analyse`; 164
   `uv run --frozen bg-project-check clean "$1"`; 168 `uv run --frozen bg-project-check run`.
   Comment line 39: "pinned and checksummed in the tooling package". Template
   `scripts/initialize.sh` line 36: `uv run --frozen bg-install-allium`; the comment at
   32-35 says the package pins it. Delete the six `template/scripts/*.py`.

10. Template prose, "this game" wording throughout (CONVENTIONS.md §4 rule):
    - `AGENTS.md.jinja`: P 176-178 "pinned by version and SHA-256 in
      `scripts/install_allium.py`" becomes "pinned by version and SHA-256 inside the
      `biscuit-games-tooling` package that `pyproject.toml` pins"; the Provenance bullet
      of CONVENTIONS.md §7 ends "checked by a project-managed binary the
      `biscuit-games-tooling` package pins and installs", and the toolchain bullet
      there names the package beside `uv`, `prek` and `ruff`. The six required phrases
      are untouched.
    - `.agents/skills/review-docs/SKILL.md` step 1: "enforced by `bg-validate-docs`,
      which `just check-docs` runs and which reports every violation at once". The
      frontmatter is unchanged, so the sixteen bridges are unchanged.
    - `repository-map.md` line 35: "The first-run script and the browser preflight";
      row 54: "`initialize.sh` and `check_playwright_browsers.js`. The two validators,
      the allium installer and runner, the gate runner and the ripsecrets wrapper are
      console scripts of `biscuit-games-tooling`, pinned in `pyproject.toml`."
    - `commands.md` 73, `quality-gates.md` 41, `work-with-the-specs.md` 87:
      `scripts/run_allium.py` becomes `bg-run-allium`; `quality-gates.md` 82: "Any
      Python file the game adds; none ships." `documentation-contract.md` 11 and
      `agent-contract.md` 11: "Enforced by `bg-validate-docs`" and "by
      `bg-validate-agents`", each "a console script of the `biscuit-games-tooling`
      package". `quality-philosophy.md` 18: "`bg-project-check`, the runner behind
      `just check`, enforces this".
    - `maintain-dependencies.md` 92: the package holds the version and the checksums,
      so moving the allium pin is a package release taken here by moving the package
      pin; 99-107 removed (the block now lives in the package README); 130: "Moving the
      package pin in `pyproject.toml` is itself a trigger for both specification hooks".
      New section "Moving the tooling package": edit the tag, run
      `uv lock --upgrade-package biscuit-games-tooling`, read the package CHANGELOG for
      the level, and on a Major run `just check` before committing.
    - `update-from-template.md.jinja`, "Steps by version": for this release, "the six
      checkers left `scripts/` and the update removed them; run `just lock` before
      `just fix && just check` so `uv.lock` learns the package pin".

11. Template repository: `pyproject.toml` `dev` gains the same package line (the harness
    imports it); `[tool.ruff] src` drops `template/scripts` and the
    `"template/scripts/**"` waivers go. `just lock`. `tests/inventory.py` drops the six
    paths from `MANAGED`. `tests/helpers.py` replaces `run_script_in_process` with
    `run_tool_in_process(render, module)`: `importlib.import_module(f"biscuit_games_tooling.{module}").main()`
    under `contextlib.chdir(render.path)`, `SystemExit` caught. `tests/test_validators.py`
    calls it with `"validate_docs"` and `"validate_agents"` on `git_render`; the negative
    controls of CONVENTIONS.md §9 are unchanged. `tests/test_specs.py` runs
    `[sys.executable, "-m", "biscuit_games_tooling.install_allium"]` then
    `[..., "run_allium", "check"]` and `"analyse"` with `cwd=render`: never `uv run` from
    inside a render, because uv would adopt the render's `pyproject.toml` as the
    project. `tests/test_render.py::test_pins_agree` asserts the package line in
    `template/pyproject.toml.jinja` equals the one in the root `pyproject.toml`.
    `CHANGELOG.md` "Update notes": the six paths removed on update, `just lock` first.

12. `just check` and `just test-full` green (`~/.npmrc` carries the read token). Commit
    on the ticket branch. **Authorisation required:** pushing, opening the pull request
    and tagging the MAJOR release. Stop and ask.

13. **Authorisation required:** a pull request on Poodl (steps 7 to 10 applied to P's
    files, `just lock && just fix && just check` green, `.tools/` untouched). If C07 has
    merged, this is Poodl's `copier update` to the new tag instead. Stop and ask.

14. **Authorisation required:** a pull request on the hub (the same, with `recipes`
    listing `package-build` and `package-check` after `frontend-build`, and the eleven
    handbook lines in the Files touched row). Stop and ask.

## Acceptance criteria

- [ ] The tooling repository's `just check` is green and `just test-network` passes
      every golden case on both checkouts: byte-identical stdout, stderr and status.
- [ ] `bg-validate-agents` on a checkout that still carries `scripts/validate_agents.py`
      reports neither a missing nor an unexpected managed file.
- [ ] `ls scripts/` in a fresh render prints exactly `check_playwright_browsers.js` and
      `initialize.sh`; the six deletions are named in the template `CHANGELOG.md`
      "Update notes" and the release is a MAJOR tag.
- [ ] In a render after `git init -b main && just initialize`: `just check` green;
      `uv.lock` names `biscuit_games_tooling` with a `#<commit>` suffix; editing the tag
      in `pyproject.toml` makes `just lock-check` exit non-zero.
- [ ] A deliberate regression in the package (a branch where `bg-validate-docs` returns
      1 unconditionally) fails a render's `just check-docs` once the render's pin names
      that branch and `just lock` has run.
- [ ] The template repository's `just check` and `just test-full` are green; the fast
      suite runs the package from the template repository's own environment and never
      syncs a render.
- [ ] No template page, `AGENTS.md.jinja` or skill names a `scripts/*.py` path;
      `test_no_poodl_outside_provenance` and `validate_docs` pass on the render.
- [ ] The package README carries the version table and the checksum recomputation
      block; every action marked **Authorisation required** was authorised before it
      was taken.

## Verification

In the tooling repository:

```sh
just check
BG_GOLDEN_POODL=/Users/scutting/projects/poodl BG_GOLDEN_BISCUIT_GAMES=/Users/scutting/projects/biscuit_games just test-network
```

Both exit 0; the second reports fourteen golden cases passed (seven per checkout).

In the template repository, from the root:

```sh
just check
just test-full
just render ai_tmp/render && cd ai_tmp/render && git init -q -b main && just initialize && just check
```

All green. Then, still inside the render:

```sh
ls scripts
uv run --frozen bg-validate-docs
grep -n 'biscuit_games_tooling' uv.lock
sed -i '' 's/@v0.1.0/@v0.1.1/' pyproject.toml && just lock-check; git checkout -- pyproject.toml
```

Expected: `check_playwright_browsers.js` and `initialize.sh` only; a line beginning
`Validated 38 pages and` with exit 0; a `source = { git = "...?rev=v0.1.0#` line
carrying a full commit; `uv lock --check` exits non-zero (a missing tag or a lockfile
that needs updating).

Regression proof, on a throwaway branch `always-fail` of the tooling repository whose
`validate_docs.main` returns 1 before validating: in the render, point the pin at
`@always-fail`, then:

```sh
just lock && just check-docs
```

Expected: `just check-docs` exits 1. Delete the branch afterwards.

## Hand-back notes

### Outcome

- `steven-cutting/biscuit_games_tooling` carries the package `biscuit-games-tooling`
  `0.2.0`: the six console scripts, `_project.py`, the golden test and its recordings, and
  `tests/test_project.py`. Pull request 3 was merged as `c0a76b6`, and the annotated tag
  `v0.2.0` points there. Both were authorised by the maintainer; the maintainer did the
  merge, because `main` requires an approving review.
- In this repository, the template renders `scripts/` as `initialize.sh` and
  `check_playwright_browsers.js` alone. The hooks, recipes and `initialize.sh` call
  `uv run --frozen bg-…`, and `pyproject.toml` pins `@v0.2.0` in both the template and the
  root. The harness runs the package from this repository's environment, and
  `CHANGELOG.md` records the change under Unreleased as a MAJOR release. All of it is
  committed on the ticket branch.
- Still to come, each separately authorised: the pull request on `main` and the `v2.0.0`
  tag; the Poodl and hub changes, handed to the maintainer as two Claude Code prompts.

### What was verified, and how

Output is quoted. Elisions are in square brackets, and so is the `=` padding of pytest's
summary lines.

The tooling repository, on the branch before the merge:

```text
$ just check
uv lock --check
Resolved 9 packages in 3ms
[ruff lint, ruff format, builtin checks, markdownlint, typos, actionlint, ripsecrets: Passed]
tests/test_golden.py .....ss.....ss
tests/test_project.py ......
[...] 16 passed, 4 skipped in 3.47s [...]
$ BG_GOLDEN_POODL=/Users/scutting/projects/poodl BG_GOLDEN_BISCUIT_GAMES=/Users/scutting/projects/biscuit_games just test-network -v
tests/test_golden.py::test_console_script_matches_the_baseline[biscuit_games-validate_docs] PASSED
[... the other five biscuit_games cases, run_allium-check and run_allium-analyse among them: PASSED]
tests/test_golden.py::test_console_script_matches_the_baseline[poodl-validate_docs] PASSED
[... the other six poodl cases: PASSED]
[...] 14 passed in 4.23s [...]
$ gh run view 35074504188 -R steven-cutting/biscuit_games_tooling [the pull request's head, 04cb6a0]
Run just sync: success
Run just check: success
Run just test-network: success
$ gh run list -R steven-cutting/biscuit_games_tooling [push to main]
35075293305 push c0a76b6 completed/success Merge pull request #3 from steven-cutting/C02-tooling-package
$ git ls-remote --tags origin 'v0.2.0*'
3610736cc22430494a0b4d2994747585de40e388  refs/tags/v0.2.0
c0a76b6d155064bb229d2974ee068841fee05b69  refs/tags/v0.2.0^{}
```

The test-network run had 14 cases then; `tests/test_project.py`, added later, makes the
full run 20. What the recordings hold, with the exit status and the last line printed:

```text
poodl/validate_docs                   0  Validated 41 pages and 42 canonical topics.
poodl/validate_agents                 0  Validated AGENTS.md, 2 adapters, and 9 skills.
poodl/install_allium-check            1  allium is not installed; this project pins 3.6.1. Run just install-allium
poodl/run_project_check-clean         0  The Git worktree is clean.
poodl/run_ripsecrets_redacted         1  ripsecrets is unavailable; run just install-hooks
poodl/run_allium-check                0  allium check: 6 specifications, no diagnostics and no findings.
poodl/run_allium-analyse              0  allium analyse: 6 specifications, no diagnostics and no findings.
biscuit_games/validate_docs           0  Validated 52 pages and 56 canonical topics.
biscuit_games/validate_agents         0  Validated AGENTS.md, 2 adapters, and 10 skills.
biscuit_games/install_allium-check    1  allium is not installed; this project pins 3.6.1. Run just install-allium
biscuit_games/run_project_check-clean 0  The Git worktree is clean.
biscuit_games/run_ripsecrets_redacted 1  ripsecrets is unavailable; run just install-hooks
biscuit_games/run_allium-check        0  allium check: 3 specifications, no diagnostics and no findings.
biscuit_games/run_allium-analyse      0  allium analyse: 3 specifications, no diagnostics and no findings.
```

The golden cases also prove acceptance criterion 2. The fixture commits the hub's
`scripts/validate_agents.py` over each checkout's `scripts/`, so both trees still carry
that file, and `bg-validate-agents` exits 0 on both with neither a missing nor an
unexpected managed file reported.

The golden test is live: changing `Validated` to `Checked` in the package's
`validate_docs` failed both `validate_docs` cases with `stdout: 'Checked 52 pages and 56
canonical topics.\n' != 'Validated 52 pages and 56 canonical topics.\n'`.

The six baselines are byte-identical to the hub's: `git hash-object` of each equals
`git rev-parse 09b4894a:scripts/<name>.py`, for example `validate_docs.py e7a0456…` on
both sides.

This repository, with both pins at `@v0.2.0`:

```text
$ just check
uv lock --check
Resolved 34 packages in 3ms
[every hook: Passed]
Success: no issues found in 10 source files
tests/test_full.py s
tests/test_questionnaire.py ...............
tests/test_render.py .......................
tests/test_specs.py ss
tests/test_update.py ...
tests/test_validators.py ....
[...] 45 passed, 3 skipped, 31 warnings in 58.08s [...]
$ grep -n 'biscuit_games_tooling' uv.lock
112:    { name = "biscuit-games-tooling", git = "https://github.com/steven-cutting/biscuit_games_tooling?rev=v0.2.0" },
124:source = { git = "https://github.com/steven-cutting/biscuit_games_tooling?rev=v0.2.0#c0a76b6d155064bb229d2974ee068841fee05b69" }
$ just test-full -p no:warnings
tests/test_full.py .
tests/test_questionnaire.py ...............
tests/test_render.py .......................
tests/test_specs.py ..
tests/test_update.py ...
tests/test_validators.py ....
[...] 48 passed in 89.96s (0:01:29) [...]
```

The render, from the working tree with both pins at `@v0.2.0`:

```text
$ just render ai_tmp/render && cd ai_tmp/render && git init -q -b main && just initialize && just check
[...]
 + biscuit-games-tooling==0.2.0 (from git+https://github.com/steven-cutting/biscuit_games_tooling@c0a76b6d155064bb229d2974ee068841fee05b69)
[...]
installed allium 3.6.1 at [...]/ai_tmp/render/.tools/bin/allium
[...]
Ready. Next: just check.
==> just lock-check
==> just lint
==> just frontend-static
==> just frontend-coverage
      Tests  30 passed (30)
==> just frontend-build
==> just storybook-build
==> just storybook-test
      Tests  3 passed (3)
==> just check-docs
Validated 38 pages and 39 canonical topics.
==> just check-agents
Validated AGENTS.md, 2 adapters, and 8 skills.
==> just check-specs
allium check: 1 specifications, no diagnostics and no findings.
==> just analyse-specs
allium analyse: 1 specifications, no diagnostics and no findings.
==> just check-clean
All checks passed and the worktree is unchanged.
$ ls scripts
check_playwright_browsers.js
initialize.sh
$ uv run --frozen bg-validate-docs
Validated 38 pages and 39 canonical topics.
$ grep -n biscuit_games_tooling uv.lock
8:source = { git = "https://github.com/steven-cutting/biscuit_games_tooling?rev=v0.2.0#c0a76b6d155064bb229d2974ee068841fee05b69" }
75:    { name = "biscuit-games-tooling", git = "https://github.com/steven-cutting/biscuit_games_tooling?rev=v0.2.0" },
$ sed -i '' 's/@v0.2.0/@v0.2.1/' pyproject.toml && just lock-check
uv lock --check
   Updating https://github.com/steven-cutting/biscuit_games_tooling (v0.2.1)
  × Failed to download and build `biscuit-games-tooling @
  │ git+https://github.com/steven-cutting/biscuit_games_tooling@v0.2.1`
[...]
      fatal: couldn't find remote ref refs/tags/v0.2.1
error: recipe `lock-check` failed on line 31 with exit code 1
[then the pin was put back, and `uv lock --check` passed again]
```

prek lists only the files Git tracks, and a fresh render has none staged, so the `lint`
step above ran almost every hook against no files. The hook gate was run again with the
render's files staged:

```text
$ git add -A && just lint
uv run --frozen prek run --all-files
Ruff lint............................................(no files to check)Skipped
Ruff format check....................................(no files to check)Skipped
ESLint and Prettier......................................................Passed
Documentation contract...................................................Passed
Agent instruction contract...............................................Passed
Specification diagnostics................................................Passed
Specification analysis...................................................Passed
[the nine builtin checks: Passed]
EditorConfig.............................................................Passed
markdownlint.............................................................Passed
typos....................................................................Passed
lychee...................................................................Passed
shellcheck...............................................................Passed
Lint GitHub Actions workflow files.......................................Passed
ripsecrets...............................................................Passed
exit=0
```

Ruff has nothing to check, because no Python ships in a render now.

The regression proof. A local branch `always-fail` in the tooling repository had
`validate_docs.main` return 1 before validating (commit `88cbf12`, never pushed). The
render's pin pointed at it:

```text
$ grep -n 'biscuit-games-tooling @' pyproject.toml
10:  "biscuit-games-tooling @ git+file:///Users/scutting/.supacode/repos/biscuit_games_tooling/C02-tooling-package@always-fail",
$ just lock && just check-docs
Updated biscuit-games-tooling v0.2.0 (04cb6a0b) -> v0.2.0 (88cbf120)
[...]
markdownlint.............................................................Passed
typos....................................................................Passed
lychee...................................................................Passed
uv run --frozen bg-validate-docs
error: recipe `check-docs` failed on line 120 with exit code 1
exit=1
```

This ran on the branch-pinned render before the tag existed, hence `04cb6a0b` as the
starting commit. The render's pin and lock were restored afterwards, and the branch and
its worktree were deleted.

The Update notes say a stale `uv.lock` breaks the console scripts. To test that, a fresh
`.venv` in the render was given `pyproject.toml` with the pin and `uv.lock` from before
it:

```text
$ uv run --frozen bg-validate-docs
Creating virtual environment at: .venv
Installed 2 packages in 2ms
error: Failed to spawn: `bg-validate-docs`
  Caused by: No such file or directory (os error 2)
```

With the package still installed in an existing `.venv`, the same command passed, because
`uv run` does not remove what the lock no longer names. A game updating from `1.0.0` has
never installed the package, so the fresh environment is the case the note describes, and
`just lock-check` fails either way.

### Deviations

- **Version `0.2.0` and tag `v0.2.0`, not `v0.1.0`.** The host already carried `v0.1.0`
  for the workflows, so the package took the next MINOR of the shared series, as the last
  open point says. The tooling README states the shared series. Every `@v0.1.0` in steps
  7 and 11 is `@v0.2.0`, and the verification's `sed` moves `@v0.2.0` to `@v0.2.1`. The
  tooling `CHANGELOG.md` opens with `[0.2.0]`. The template release is `2.0.0`, the
  maintainer's choice, so `update-from-template.md` gains `### 2.0.0`.
- **The regression proof used a local branch and a `git+file://` pin.** The maintainer
  chose this to avoid pushing a throwaway branch. It exercises the same `uv lock` and
  `uv sync` path.
- **Files this ticket does not list:**
  - `tests/test_update.py` called `run_script_in_process` three times and now calls
    `run_tool_in_process`.
  - `tests/conftest.py`'s `git_render` docstring named `validate_agents.py`.
  - Root `README.md` named `scripts/validate_docs.py` and `scripts/validate_agents.py` in
    "What every rendered game gets" and in the harness list, and gains one bullet for the
    pinned package.
  - The `[tool.uv]` comments in `template/pyproject.toml.jinja` and the root
    `pyproject.toml` said the project exists for prek and ruff (or copier, pytest and the
    hook runner); both now name the package.
  - In the tooling repository, `.gitignore` gained the Python caches and
    `.markdownlint-cli2.jsonc` gained `MD024` `siblings_only`, which a changelog with a
    second release needs.
- **Harness helpers.** `run_script` became `run_tool(render, module, *args)`, running
  `python -m biscuit_games_tooling.<module>` beside `run_tool_in_process`.
  `run_tool_in_process` returns `int(main())` and treats a non-integer `SystemExit` code as
  1, for mypy `--strict`. `test_pins_agree` reads both pins with `tomllib`.
- **Golden test details the ticket left open:**
  - The checkouts are fetched one commit deep (`git fetch --depth 1 <clone or URL> <sha>`),
    because Poodl's `.git` is 346 MB.
  - Both sides run with `PATH` limited to the virtual environment, `/usr/bin` and `/bin`,
    so a `ripsecrets` installed elsewhere cannot make a recording machine-dependent. The
    ripsecrets case therefore compares two "unavailable" exits. The hook path is proved in
    the render instead (open points, below).
  - The two network cases run in a copy of the checkout, so the installed binary never
    reaches the `install_allium --check` case.
  - `BG_GOLDEN_RECORD=1` writes the recordings.
- **After review of the tooling pull request** (commits `86b04e4` and `04cb6a0`):
  - CI's first run failed four recordings. allium walks `docs/specs/` in filesystem order,
    which differs between macOS and Linux. The recordings now sort allium's blocks by
    module. The baseline and the package still compare raw.
  - Codex found that `predicates = { x = "false" }` enabled `x`. Only the boolean `true`
    enables a predicate now, and a test holds that.
  - Copilot asked `bg-ripsecrets` to resolve the root and run there. Declined: prek's file
    arguments are relative to the hook's directory, and the script it replaces had no root
    either. The README's claim that every script resolves the root was corrected instead.
  - Copilot's two grammar nits are in comments verbatim from the hub, which read correctly
    with an omitted "that". They were left.
  - `tests/test_project.py` was added before the pull request, because the golden
    checkouts carry no `[tool.biscuit-games-tooling]` table.
- **`validate_agents` keeps `CANONICAL_SKILLS` as the relative `Path(".agents/skills")`,
  joined to the root where it is used,** rather than a value computed in `main()`.
- **`install_allium`'s `CHECKSUMS` comment** now points at the package README rather than
  `docs/how-to/maintain-dependencies.md`, which no longer holds the recomputation block.
- **`maintain-dependencies.md`** also lost the "Replace `VERSION` and all four entries in
  `CHECKSUMS`" sentence, since a game no longer edits those. It keeps the reinstall block
  under "After taking a release that moves it". The new section sits before "Moving the
  Allium binary", which refers to it.
- **Line numbers.** The template's lines differ from the ticket's P numbering, as expected:
  - `.pre-commit-config.yaml` 38, 45, 59, 66 and 163;
  - `Justfile` 44, 120, 123, 136, 143, 151 and 155;
  - `repository-map.md` 33 and 50;
  - `commands.md` 71, `quality-gates.md` 42 and 83, `work-with-the-specs.md` 84 and
    `quality-philosophy.md` 19.
  The template's `AGENTS.md.jinja` has no "pinned by version and SHA-256" stack bullet
  (P 176-178), so only the two Provenance bullets changed.
- **The template's ruff config for `scripts/**` stays** in `pyproject.toml.jinja`. No
  Python ships under `scripts/` now, but a game may add some, and `quality-gates.md` says
  the ruff hooks lint "Any Python file the game adds; none ships."
- **Branch name.** The branch is the Supacode worktree's `C02-tooling-package`, in both
  repositories, as C01's was.
- **The two seed decisions were edited after review of the pull request, against this
  ticket's Non-goals.** Both bots found that a render from this branch contradicts its own
  records on the day it is made: `0004-python-toolchain.md` said the project's only
  dependencies were `prek` and `ruff` and that ruff existed for the Python under
  `scripts/`, and `0007-project-managed-allium-cli.md` said `scripts/install_allium.py`
  held the allium pin and `scripts/run_allium.py` ran the subcommand. The Non-goals rule
  protects a record of what was true when it was written, which is why Poodl's and the
  hub's decisions were left alone; a new game's records are not history, so the maintainer
  chose to reconcile these two. The numbers, titles and `canonical_for` slugs are
  untouched, so the frozen seed inventory holds, and `CHANGELOG.md` records it under Seed.
  `docs/project/repository-map.md`'s tree line, which said `pyproject.toml` holds "prek and
  ruff", was corrected in the same pass.
- **Copilot also asked for this ticket's `## Open points` section to be closed or removed,
  now that the hand-back answers each one.** Left as it is: CONVENTIONS.md §11 fixes the
  ticket's sections, the Open points section is what the ticket asked before the work, and
  "Open points, settled" above is the answer to it. C01 closed the same way.
- **A consequence for a game whose only Python was these scripts.** Poodl's CodeQL, which
  runs from GitHub's default setup rather than a workflow file, began failing on `main`
  with `CodeQL detected code written in JavaScript/TypeScript, GitHub Actions and HTML, but
  not any written in Python` after it adopted the package. The fix is a repository setting,
  dropping Python from the language list, and the maintainer took it. Nothing in the
  template ships a CodeQL workflow, and a render has no Python at all, so any game that
  turns default setup on should leave Python out of it.

### Handed back

- **To a pull request on `main` for `CONVENTIONS.md`:**
  - §4's six `scripts/*.py` rows no longer describe the template.
  - §9's harness API names `run_script_in_process` and `run_script`, and its
    `test_validators.py` and `test_specs.py` descriptions name the scripts.
  - §9's `pyproject.toml` paragraph lists `template/scripts` in ruff's `src` and the
    `template/scripts/**` waivers.
- **To C04:** the pin to propose bumping is the `biscuit-games-tooling @ git+…@vX.Y.Z` line
  in a game's `pyproject.toml` `dev` group. `uv lock --upgrade-package
  biscuit-games-tooling` relocks it, and the package's README gives the level of each
  release in its version table.
- **To C06:** this release removes six managed files, which its check should classify as
  MAJOR. The entry here was written by hand, as the ticket says.
- **To the maintainer, as prompts:** one Claude Code prompt to run in Poodl and one to run
  in the hub, neither committed. Each carries the golden verdict for its
  tree, the exact edits (the hub's `recipes` adds `package-build` and `package-check`
  after `frontend-build`), `just lock && just sync && just fix && just check`, and a stop
  before each push, pull request and merge. If C07 lands first, Poodl takes this through
  `copier update` to `2.0.0`, and its prompt is not needed.

### Open points, settled

- **Poodl at `0a46a485` passes the hub's `validate_docs`:** yes. The golden case exits 0
  with `Validated 41 pages and 42 canonical topics.`, so the duplicate-key rule finds
  nothing in Poodl.
- **`github.token` cloning a private sibling:** not checked, because the repository stayed
  public.
- **`uv run --frozen bg-ripsecrets` finds prek's `ripsecrets`:** yes. In the render with its
  files staged (prek lists tracked files only), `uv run --frozen prek run --all-files
  ripsecrets` printed `Passed` and exited 0. With `planted.txt` staged, holding a
  36-character `ghp_` token, it printed `Failed`, exit code 1,
  `ripsecrets found credential material; the matched values are suppressed`.
- **The first `just lock` over `https://`:** `uv.lock` carries the `#<commit>` suffix, as the
  `file://` probe did: `?rev=v0.2.0#c0a76b6d155064bb229d2974ee068841fee05b69`. uv 0.11.18
  printed no `Updated https://…` line, because the output was not a terminal. A lock with an
  empty `UV_CACHE_DIR` printed `Resolved 4 packages in 413ms` and wrote the same `source`
  line.
- **One tag series or a subdirectory:** one series, at the repository root. The workflows
  carried `v0.1.0`, so the package is `0.2.0`, and the tooling README says so under
  "Versions".

## Open points

CONVENTIONS.md §12 assigns no claim to this ticket. Settled while writing: the git
dependency mechanism (step 7) and the nested `git init` behaviour (step 3), both on
this machine with uv 0.11.18. Still open:

- Poodl at `0a46a485` passes the hub's `validate_docs` (duplicate-key rejection is the
  one rule CONVENTIONS.md §1 fact 2 did not cover). Check: the `validate_docs.py` golden
  case on the Poodl checkout exits 0; if it exits 1, Poodl's pull request fixes the
  duplicate before adopting the package, and the golden test still holds.
- Whether a workflow's `github.token` can clone a private sibling repository for
  `uv sync`. Not verified; the documented uv paths are a token in the URL or the Git
  credential helper (`gh auth setup-git`). Check only if the repository is made private:
  run the template's `fast` job and read the `just sync` step. The recommendation
  stands: public.
- `uv run --frozen bg-ripsecrets` finds the `ripsecrets` binary prek puts on `PATH` for
  a `language: rust` hook, as `uv run --no-project` did. Check: in a render after
  `just install-hooks`, `uv run --frozen prek run --all-files ripsecrets` exits 0.
- The first `just lock` in a render over `https://` behaves as the `file://` probe did.
  Check: it prints `Updated https://github.com/steven-cutting/biscuit_games_tooling (<commit>)`
  and `uv.lock` carries the `#<commit>` suffix.
- Whether C01's host shares one tag series with the package or the package takes a
  `subdirectory` and its own series. Check: read C01's hand-back notes; if the
  workflows already carry `v0.1.0`, the package starts at the next MINOR of that series
  and the README says so.
