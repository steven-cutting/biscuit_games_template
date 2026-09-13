---
id: T02
title: "Scripts: the validators, installers and checkers the render ships"
status: done
depends_on: [T00]
parallel_with: [T01, T03, T04, T05, T06, T07, T08, T09]
branch: ticket/t02-scripts
estimated_size: M
---

# T02: Scripts: the validators, installers and checkers the render ships

## Context

Every rendered game carries eight scripts under `scripts/` and one provider setting,
`.claude/settings.json`. They are the machinery behind the game's gate: `just initialize`
runs `sh scripts/initialize.sh` (P `Justfile` lines 14-15); `just install-allium` runs
`scripts/install_allium.py` (lines 43-44); `just check-specs` and `just analyse-specs` run
`scripts/run_allium.py check` and `analyse` (lines 148-149, 155-156); `just check-clean`
and `just check` run `scripts/run_project_check.py clean` and `run` (lines 163-168); the
hooks `validate-docs`, `validate-agents`, `check-specs`, `analyse-specs` and `ripsecrets`
in P `.pre-commit-config.yaml` (lines 37-49, 58-70, 160-164) run the validators, the
Allium gate and `scripts/run_ripsecrets_redacted.py`; and the `storybook:test` script in
P `package.json` line 29 runs `node scripts/check_playwright_browsers.js` first. The
callers are T01's files (`Justfile`, the prek configs, `package.json.jinja`); this ticket
ships what they call.

CONVENTIONS.md §1 fact 2 decides the sources: the hub's validators are the stricter, newer
ones, and Poodl's bridges, `CLAUDE.md` and copilot adapter already satisfy them byte for
byte. CONVENTIONS.md §4 assigns each file. What P (`/Users/scutting/projects/poodl` at
`0a46a485`) and H (`/Users/scutting/projects/biscuit_games` at `09b4894a`) hold, and which
copy ships, verified by `diff` of every pair:

| File | How H differs from P | Shipped |
| --- | --- | --- |
| `scripts/validate_docs.py` | H rejects a repeated frontmatter key (H 74-78) and a repeated manifest key through `_reject_duplicates` and `object_pairs_hook` (H 122-135, 140-147); the comment at line 26 names the repository | H, with the comment at lines 26-29 rewritten |
| `scripts/validate_agents.py` | H replaces the 40-word bridge budget with an exact `BRIDGE_BODY` (H 19-25, compared at 220), rejects a repeated frontmatter key (H 126-131) and compares the two adapters unstripped (H 169-176) | H verbatim |
| `scripts/initialize.sh` | H adds the Linux system-libraries notice (H 21-30) and installs hooks only from the primary checkout (H 44-57) | H verbatim, mode 100755 |
| `scripts/install_allium.py` | H adds only the comment at lines 29-35 (the tool's version series against the assistant plugin's) | H verbatim |
| `scripts/run_allium.py` | identical | P |
| `scripts/run_project_check.py` | H adds `package-build` and `package-check` to `RECIPES` (H 24-25); both are hub-only recipes | P verbatim |
| `scripts/run_ripsecrets_redacted.py` | identical | P |
| `scripts/check_playwright_browsers.js` | identical | P |
| `.claude/settings.json` | identical | P |

The H commit is the one CONVENTIONS.md §0 pins. `git -C /Users/scutting/projects/biscuit_games describe --tags`
reports `v1.0.0-4-g09b4894`, so the tag sits four commits earlier, at `dfebaf4`; the nine
files above are byte-identical at both commits, so nothing in this ticket depends on which
one is read.

Where this ticket sits: T00 has merged, so `copier.yml`, the harness core (`tests/conftest.py`
with the `network` gate and the `git_render` fixture, `tests/helpers.py` with `run_script`,
`tests/inventory.py`), `tests/test_render.py`, `tests/test_validators.py` and the `fast` CI
job exist, and a stub stands at every path below. T00 may already have shipped working
copies of some of these scripts to keep its own `test_validators.py` green; this ticket's
outcome is that each file equals its source (with the one comment edit) whatever T00 left.
T01 and T03 to T09 run in parallel: T01 owns the callers, T04 owns what
`validate_agents.py` inspects, T06 owns the seed module `test_specs.py` parses, T07 to T09
own what `validate_docs.py` inspects. T10 waits for this lane: its `test_full.py` runs
`just initialize` and `just check` inside a render, which is these scripts end to end.

Read first: the nine source files named above in P and H; `tests/helpers.py`,
`tests/conftest.py` and `tests/test_validators.py` in this repository (the harness API
CONVENTIONS.md §9 describes, as T00 actually wrote it); CONVENTIONS.md §4 (the `scripts/`
rows), §9 (harness and tests), §11 (lane rules), §13 (the `initialize.sh` risk).

## Goal

- `template/scripts/` holds the eight scripts of the table, each byte-identical to its
  named source except `validate_docs.py`, whose lines 26-29 carry the comment in step 5.
- `template/scripts/initialize.sh` is tracked as mode `100755`, and a render carries the
  bit (copier 9.18.2 reads it from the template's git index: `_template.py` 600-625,
  `_main.py` 880-897).
- `template/.claude/settings.json` is P's, verbatim.
- `tests/test_specs.py` exists, carries the `network` marker, and proves in a `git_render`
  that `install_allium.py` installs the pinned binary and that `run_allium.py check` and
  `analyse` exit 0 over the seed module, with a negative control that an empty
  `docs/specs/` is refused.
- `just check` (lock-check, lint, typecheck, the fast suite) is green, and
  `BISCUIT_TEMPLATE_NETWORK=1 just test tests/test_specs.py` has been run and its outcome
  recorded.

## Non-goals

- Editing any caller of these scripts: `template/Justfile`, the two prek configs,
  `template/package.json.jinja` are T01's.
- Fixing the seed module `docs/specs/{{ game_slug }}.allium.jinja` or
  `template/tests/platformSpecs.test.ts`. If the binary rejects the module, the failure
  is recorded in the hand-back notes for T06 and nothing is changed here.
- Writing or editing `tests/test_validators.py`, `tests/conftest.py`, `tests/helpers.py`
  or `tests/inventory.py`: T00's. A helper this ticket needs and cannot find is handed
  back as a T00 follow-up on `main` (CONVENTIONS.md §11).
- Touching `AGENTS.md.jinja`, the skills or bridges (T04), the workflows or the copilot
  adapter (T03), or any handbook page (T07 to T09), even where a validator shipped here
  reports on them.
- Packaging the scripts as a dependency: ticket C02.
- Running `just initialize` or `just check` inside a render: T10's `test_full.py`.
- Pushing, opening a pull request, tagging.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `template/scripts/check_playwright_browsers.js` | M | P `scripts/check_playwright_browsers.js` | replace the stub with the verbatim copy |
| `template/scripts/initialize.sh` | M | H `scripts/initialize.sh` | verbatim copy; tracked as `100755` |
| `template/scripts/install_allium.py` | M | H `scripts/install_allium.py` | verbatim copy |
| `template/scripts/run_allium.py` | M | P `scripts/run_allium.py` | verbatim copy |
| `template/scripts/run_project_check.py` | M | P `scripts/run_project_check.py` | verbatim copy |
| `template/scripts/run_ripsecrets_redacted.py` | M | P `scripts/run_ripsecrets_redacted.py` | verbatim copy |
| `template/scripts/validate_docs.py` | M | H `scripts/validate_docs.py` | verbatim copy, then lines 26-29 rewritten (step 5) |
| `template/scripts/validate_agents.py` | M | H `scripts/validate_agents.py` | verbatim copy |
| `template/.claude/settings.json` | M | P `.claude/settings.json` | verbatim copy |
| `tests/test_specs.py` | repo | new | the `network` test of step 7 |

## Steps

1. Create the worktree from `main` after T00 has merged (`tickets/README.md`, "How to
   pick up a ticket"). Confirm the sources are at the pinned commits:

   ```sh
   git -C /Users/scutting/projects/poodl rev-parse --short HEAD
   git -C /Users/scutting/projects/biscuit_games rev-parse --short HEAD
   ```

   Expected `0a46a48` and `09b4894`. Then run `just test` once, before changing anything,
   to see T00's baseline green.

2. Read `tests/helpers.py` and `tests/conftest.py`. Confirm `run_script(render, script,
   *args)` runs `sys.executable scripts/<script>` with `cwd=render.path`,
   `capture_output=True, text=True` and returns the `CompletedProcess`; confirm the
   `git_render` fixture and that `pytest_collection_modifyitems` skips `network` unless
   `BISCUIT_TEMPLATE_NETWORK=1`; note how `tests/test_validators.py` imports the helpers
   (`from tests.helpers import ...` with a `tests/__init__.py`, or `from helpers import
   ...` without one). Step 7 follows that style.

3. Copy the five files whose P and H copies are identical, plus P's
   `run_project_check.py`:

   ```sh
   P=/Users/scutting/projects/poodl
   cp "$P/scripts/run_allium.py" "$P/scripts/run_project_check.py" \
      "$P/scripts/run_ripsecrets_redacted.py" "$P/scripts/check_playwright_browsers.js" \
      template/scripts/
   cp "$P/.claude/settings.json" template/.claude/settings.json
   ```

   Why P's `run_project_check.py`: its `RECIPES` tuple (P lines 18-30: `lock-check`,
   `lint`, `frontend-static`, `frontend-coverage`, `frontend-build`, `storybook-build`,
   `storybook-test`, `check-docs`, `check-agents`, `check-specs`, `analyse-specs`) is the
   `just check` order, and every name in it is a recipe of the template's `Justfile` (P's
   minus `stage` and `stage-preview`, which the tuple never named). H's adds
   `package-build` and `package-check`, which no game has. The tuple is unchanged so that
   the gate numbering in `.agents/skills/project-check/SKILL.md` (T04) stays true.
   `.claude/settings.json` is the five-line `enabledPlugins` object for
   `allium@juxt-plugins`; `validate_agents.py` tolerates it by name (H line 31) rather
   than requiring it.

4. Copy H's `validate_agents.py` and `install_allium.py` verbatim:

   ```sh
   H=/Users/scutting/projects/biscuit_games
   cp "$H/scripts/validate_agents.py" "$H/scripts/install_allium.py" template/scripts/
   cmp template/scripts/validate_agents.py "$H/scripts/validate_agents.py"
   cmp template/scripts/install_allium.py "$H/scripts/install_allium.py"
   ```

   Both `cmp` calls print nothing. `install_allium.py` pins `VERSION = "3.6.1"` (H line
   36) with four checksums (lines 53-58); `run_allium.py` calls its `check()` (P line 161)
   before every run, which is why the two ship together and why step 7 installs first.

5. Copy H's `validate_docs.py` and rewrite the comment at lines 26-29, the only edit in
   this ticket. H's line 26 reads
   `# Biscuit Games is generated from no template and has no feature toggles, so no page is`;
   replace the four-line comment so that the file differs from H by exactly this hunk:

   ```diff
   -# Biscuit Games is generated from no template and has no feature toggles, so no page is
   -# conditional on one. The machinery is kept rather than deleted: `requires` is
   -# still parsed and compared, so adding a predicate later is a one-line change
   -# here rather than a reshaping of the manifest.
   +# This game is generated from the Biscuit Games template and has no feature
   +# toggles, so no page is conditional on one. The machinery is kept rather than
   +# deleted: `requires` is still parsed and compared, so adding a predicate later
   +# is a one-line change here rather than a reshaping of the manifest.
   ```

   Check with `diff "$H/scripts/validate_docs.py" template/scripts/validate_docs.py`: one
   hunk, `26,29c26,29`. Everything the validator enforces (CONVENTIONS.md §6 rule 4, §11)
   is unchanged: the render is what it inspects, because `ROOT` is
   `Path(__file__).resolve().parents[1]` (H line 18).

6. Copy H's `initialize.sh` and commit the mode. `cp` onto an existing stub keeps the
   stub's mode, so set it explicitly:

   ```sh
   cp "$H/scripts/initialize.sh" template/scripts/initialize.sh
   chmod +x template/scripts/initialize.sh
   git add template/scripts/initialize.sh
   git ls-files -s template/scripts/initialize.sh
   ```

   The last line must begin `100755`. If it shows `100644`, `git config core.fileMode`
   is `false` on this checkout: run `git update-index --chmod=+x template/scripts/initialize.sh`
   and look again. The bit is load-bearing three times: the builtin hooks
   `check-executables-have-shebangs` and `check-shebang-scripts-are-executable` run in
   this repository's own gate (`just lint`, T00) and in every render's (P
   `.pre-commit-config.yaml` lines 77 and 80), and copier carries the bit from the
   template's git index into the render (`git ls-files --stage`, copier `_template.py`
   600-625; applied in `_main.py` 880-897), so the index, not the working tree, is what a
   game receives. The render never depends on it to run: `just initialize` invokes
   `sh scripts/initialize.sh`. Read H lines 44-57 before moving on: the script skips
   `just install-hooks` in a secondary worktree and says so on stderr, which is what a
   `.supacode` worktree is; and it runs `npm run lint:fix` under `set -eu` (lines 40-42),
   the CONVENTIONS.md §13 risk that T05's lint-clean seeds guard.

7. Write `tests/test_specs.py`. Match the import style step 2 found; the body is:

   ```python
   """The specification gate the render ships, run inside a render.

   `scripts/run_allium.py` refuses an empty `docs/specs/` (its `NO_INPUTS`), so a
   green `check` and `analyse` is also the proof that the seed module exists and
   parses. Subprocess rather than `runpy`, because `run_allium.py` imports
   `install_allium` as a sibling and needs an interpreter started in the render.

   Network: `install_allium.py` downloads the pinned binary, about 1.6 MB and
   checksummed, into `<render>/.tools/bin`, once per render. The `network` marker
   is enabled by `BISCUIT_TEMPLATE_NETWORK=1`; without it every test here is
   skipped.
   """

   from __future__ import annotations

   import pytest

   from tests.helpers import Render, run_script


   def _install(render: Render) -> None:
       install = run_script(render, "install_allium.py")
       assert install.returncode == 0, install.stdout + install.stderr


   @pytest.mark.network
   def test_seed_module_is_clean(git_render: Render) -> None:
       _install(git_render)
       for command in ("check", "analyse"):
           result = run_script(git_render, "run_allium.py", command)
           assert result.returncode == 0, result.stdout + result.stderr


   @pytest.mark.network
   def test_gate_refuses_an_empty_specs_directory(git_render: Render) -> None:
       # The negative control: a gate that read nothing must not pass, or a
       # render whose seed module went missing would still be green above.
       _install(git_render)
       for module in (git_render.path / "docs" / "specs").glob("*.allium"):
           module.unlink()
       result = run_script(git_render, "run_allium.py", "check")
       assert result.returncode == 1, result.stdout + result.stderr
       assert "resolved no specification under docs/specs/" in result.stderr
   ```

   The second test is the counterpart of `test_validators.py`'s negative controls: with
   no `.allium` file, `allium check` exits `NO_INPUTS` (2), `_read` raises, and `main`
   prints `run_allium: allium check resolved no specification under docs/specs/` to
   stderr and returns 1 (P `run_allium.py` lines 42, 132-133, 203-210). The file passes
   ruff with CONVENTIONS.md §9's configuration (`from __future__ import annotations` plus a
   runtime import from the same module keeps `TC001` quiet) and `mypy --strict`; every
   function is annotated because the template repository's mypy runs strict over
   `tests/`.

8. Run the gate, then the network test:

   ```sh
   just check
   BISCUIT_TEMPLATE_NETWORK=1 just test tests/test_specs.py
   ```

   `just check` is `lock-check`, `lint`, `typecheck` and the fast suite; `test_specs.py`
   is skipped there and run by the second line, which downloads the binary once per
   `git_render` (two downloads). Both are expected green. If the second is red, read the
   assertion message: a line starting `install_allium:` is the download or the checksum
   (network; retry, and record it); a diagnostic naming `docs/specs/tic_tac_toe_beans.allium`
   is the seed module, which belongs to T06: quote the diagnostics in the hand-back notes
   and change nothing. `.github/workflows/ci.yml`'s `fast` job runs `just test` with
   `BISCUIT_TEMPLATE_NETWORK=1`, so the pull request will run this test too.

9. Prove the scripts pass the template repository's Python gate on their own, whether or
   not T00's `[tool.mypy] files` names `template/scripts` (`just typecheck` runs bare
   `mypy`, so it checks only what `pyproject.toml` lists):

   ```sh
   uv run --frozen ruff check template/scripts tests
   uv run --frozen ruff format --check template/scripts tests
   uv run --frozen mypy --strict template/scripts
   ```

   All three exit 0 (the six Python scripts are clean under both tools as shipped). If
   `pyproject.toml` does not list `template/scripts` under `[tool.mypy] files`, say so in
   the hand-back notes as a T00 follow-up on `main`; do not edit `pyproject.toml`.

10. Render once and check the bit reached the render, then remove the render:

    ```sh
    rm -rf ai_tmp/t02-render
    just render ai_tmp/t02-render
    test -x ai_tmp/t02-render/scripts/initialize.sh && echo executable
    cmp ai_tmp/t02-render/scripts/run_allium.py template/scripts/run_allium.py && echo verbatim
    rm -rf ai_tmp/t02-render
    ```

    Expected `executable` and `verbatim`. `just render` includes uncommitted changes
    (copier stages a dirty template into a throwaway commit), so this works before the
    commit in step 11.

11. Fill in the hand-back notes, set `status: done` in this file, and commit on
    `ticket/t02-scripts`. **Authorisation required:** pushing the branch and opening the
    pull request are separately authorised (CONVENTIONS.md §11); stop and ask.

## Acceptance criteria

- [ ] `cmp` reports no difference between each of `template/scripts/validate_agents.py`,
      `install_allium.py`, `initialize.sh` and H's copy, and between each of
      `run_allium.py`, `run_project_check.py`, `run_ripsecrets_redacted.py`,
      `check_playwright_browsers.js`, `template/.claude/settings.json` and P's copy.
- [ ] `diff` between H's `validate_docs.py` and `template/scripts/validate_docs.py` is
      exactly the `26,29c26,29` hunk of step 5.
- [ ] `git ls-files -s template/scripts/initialize.sh` begins `100755`; a fresh render's
      `scripts/initialize.sh` is executable.
- [ ] `tests/test_specs.py` exists with both tests under `@pytest.mark.network`, is
      skipped by plain `just test`, and is collected under `BISCUIT_TEMPLATE_NETWORK=1`.
- [ ] `just check` is green: `lock-check`, `lint` (ruff, shellcheck over
      `template/scripts/initialize.sh`, the shebang hooks, editorconfig, ripsecrets),
      `typecheck`, and `just test` including `tests/test_validators.py` with its negative
      controls.
- [ ] `BISCUIT_TEMPLATE_NETWORK=1 just test tests/test_specs.py` was run and its outcome,
      green or the quoted failure, is in the hand-back notes.
- [ ] `uv run --frozen ruff check template/scripts tests` and
      `uv run --frozen mypy --strict template/scripts` exit 0.
- [ ] No file outside the Files touched table changed, other than this ticket's `status:`.

## Verification

From the repository root. Byte identity with the sources:

```sh
H=/Users/scutting/projects/biscuit_games
P=/Users/scutting/projects/poodl
for f in validate_agents.py initialize.sh install_allium.py; do
  cmp "template/scripts/$f" "$H/scripts/$f" && echo "same as H: $f"
done
for f in run_allium.py run_project_check.py run_ripsecrets_redacted.py check_playwright_browsers.js; do
  cmp "template/scripts/$f" "$P/scripts/$f" && echo "same as P: $f"
done
cmp template/.claude/settings.json "$P/.claude/settings.json" && echo "same as P: settings.json"
diff "$H/scripts/validate_docs.py" template/scripts/validate_docs.py
```

Expected: eight `same as` lines, then a single `26,29c26,29` hunk whose eight lines are
the ones in step 5.

The mode, in git and in a render:

```sh
git ls-files -s template/scripts/initialize.sh
rm -rf ai_tmp/t02-render && just render ai_tmp/t02-render
test -x ai_tmp/t02-render/scripts/initialize.sh && echo executable
rm -rf ai_tmp/t02-render
```

Expected: a line beginning `100755`, then `executable`.

The gate and the network test:

```sh
just check
BISCUIT_TEMPLATE_NETWORK=1 just test tests/test_specs.py
uv run --frozen ruff check template/scripts tests
uv run --frozen mypy --strict template/scripts
```

Expected: `just check` ends with pytest reporting every test passed and
`tests/test_specs.py`'s two tests skipped with reason `set BISCUIT_TEMPLATE_NETWORK=1`; the
second command reports `2 passed`; the last two exit 0 (`All checks passed!` and
`Success: no issues found in 6 source files`).

## Hand-back notes

### What was verified, and how

Every command ran in this worktree, from `main` at `3db0adb`, on the tree this ticket's
commit records (the notes and the `status:` line excepted). Output is quoted; elisions
are marked, and the tab `git ls-files -s` prints before the path is written as a space
because markdownlint refuses hard tabs.

T00 had already shipped eight of the nine files in final form and `initialize.sh` at
`100755`, so steps 3, 4 and 6 had nothing to change and were not run; the `cmp` calls
below are the proof. The ticket's two edits are the comment in `validate_docs.py` and
the new `tests/test_specs.py`.

Sources at the pinned commits, and T00's baseline (step 1), before any change:

```text
$ git -C /Users/scutting/projects/poodl rev-parse --short HEAD
0a46a48
$ git -C /Users/scutting/projects/biscuit_games rev-parse --short HEAD
09b4894
$ just test
[... session header elided ...]
tests/test_render.py .......................                             [ 85%]
tests/test_validators.py ....                                            [100%]

============================== 27 passed in 9.70s ==============================
```

Byte identity with the sources:

```text
same as H: validate_agents.py
same as H: initialize.sh
same as H: install_allium.py
same as P: run_allium.py
same as P: run_project_check.py
same as P: run_ripsecrets_redacted.py
same as P: check_playwright_browsers.js
same as P: settings.json
26,29c26,29
< # Biscuit Games is generated from no template and has no feature toggles, so no page is
< # conditional on one. The machinery is kept rather than deleted: `requires` is
< # still parsed and compared, so adding a predicate later is a one-line change
< # here rather than a reshaping of the manifest.
---
> # This game is generated from the Biscuit Games template and has no feature
> # toggles, so no page is conditional on one. The machinery is kept rather than
> # deleted: `requires` is still parsed and compared, so adding a predicate later
> # is a one-line change here rather than a reshaping of the manifest.
```

The mode, in git and in a render (steps 6 and 10, with step 10's `cmp`):

```text
$ git ls-files -s template/scripts/initialize.sh
100755 4449c7b09c7ee93f5a8110f249d2977f0910183d 0 template/scripts/initialize.sh
$ rm -rf ai_tmp/t02-render && just render ai_tmp/t02-render
[... copier's DirtyLocalWarning elided ...]
Rendered into ai_tmp/t02-render
$ test -x ai_tmp/t02-render/scripts/initialize.sh && echo executable
executable
$ cmp ai_tmp/t02-render/scripts/run_allium.py template/scripts/run_allium.py && echo verbatim
verbatim
```

The gate:

```text
$ just check
uv lock --check
Resolved 33 packages in 3ms
uv run --frozen prek run --all-files
Ruff lint................................................................Passed
Ruff format check........................................................Passed
check for added large files..............................................Passed
check for case conflicts.................................................Passed
check that executables have shebangs.....................................Passed
check json...............................................................Passed
check for merge conflicts................................................Passed
check that scripts with shebangs are executable..........................Passed
check toml...............................................................Passed
check yaml...............................................................Passed
detect private key.......................................................Passed
EditorConfig.............................................................Passed
markdownlint.............................................................Passed
typos....................................................................Passed
lychee...................................................................Passed
shellcheck...............................................................Passed
Lint GitHub Actions workflow files.......................................Passed
ripsecrets...............................................................Passed
uv run --frozen mypy
Success: no issues found in 7 source files
uv run --frozen pytest "$@"
[... session header elided ...]
collected 29 items

tests/test_render.py .......................                             [ 79%]
tests/test_specs.py ss                                                   [ 86%]
tests/test_validators.py ....                                            [100%]
[... copier's DirtyLocalWarning, 16 times, elided ...]
=========================== short test summary info ============================
SKIPPED [1] tests/test_specs.py:26: set BISCUIT_TEMPLATE_NETWORK=1
SKIPPED [1] tests/test_specs.py:34: set BISCUIT_TEMPLATE_NETWORK=1
================= 27 passed, 2 skipped, 16 warnings in 10.80s ==================
```

The scripts on their own (step 9):

```text
$ uv run --frozen ruff check template/scripts tests
All checks passed!
$ uv run --frozen ruff format --check template/scripts tests
13 files already formatted
$ uv run --frozen mypy --strict template/scripts
Success: no issues found in 6 source files
```

And the whole suite as CI's `fast` job runs it, with the network gate on:

```text
$ BISCUIT_TEMPLATE_NETWORK=1 just test
tests/test_render.py .......................                             [ 79%]
tests/test_specs.py ..                                                   [ 86%]
tests/test_validators.py ....                                            [100%]
======================= 29 passed, 16 warnings in 11.79s =======================
```

### The network test

Green. Both downloads verified their checksums, `check` and `analyse` reported the seed
module clean, and the negative control exited 1 with the refusal on stderr:

```text
$ BISCUIT_TEMPLATE_NETWORK=1 just test tests/test_specs.py
uv run --frozen pytest "$@"
[... session header elided ...]
collected 2 items

tests/test_specs.py ..                                                   [100%]
[... copier's DirtyLocalWarning elided ...]
========================= 2 passed, 1 warning in 3.62s =========================
```

### Deviations

- The work is on branch `T02-scripts`, the branch the Supacode worktree was created on,
  not `ticket/t02-scripts` as the frontmatter says. The T01 and T09 worktrees are named
  the same way. Rename the branch before pushing if it must match the field.
- T00's copies were already final; see above. No `cp` was run.
- One in step 7. `tests/__init__.py` exists and `test_validators.py` imports
  `from tests.helpers import ...`, so the imports are the ticket's. The negative control
  empties `docs/specs/` with `.rglob("*.allium")`, not the step's `.glob`, after review on
  pull request 4: `run_allium.py`'s `_modules()` and allium itself walk the directory
  recursively. With a copy of the seed module in `docs/specs/sub/`, `.glob` leaves that
  copy behind and `run_allium.py check` exits 0 on it; `.rglob` removes both, and the
  gate exits 1 with `resolved no specification under docs/specs/`.
- `CHANGELOG.md` is not in the Files touched table and was not edited. The comment edit
  is to a managed file and reaches games on update; no seed file changed.

### Handed back

- T00 follow-up on `main`: `pyproject.toml` lines 37-40 set `[tool.mypy] files = ["tests"]`,
  so `just typecheck` checks the seven files under `tests/` and none of the scripts.
  Adding `"template/scripts"` to that list is enough: `mypy --strict template/scripts`
  already passes.
- T06: nothing. The seed module is clean under allium 3.6.1.
- T01: nothing. Every `scripts/` path in `template/Justfile`,
  `template/.pre-commit-config.yaml` and `template/package.json.jinja` names a shipped
  script, and every name in `run_project_check.py`'s `RECIPES` is a recipe in
  `template/Justfile` (checked by parsing both; none missing).
- `tickets/README.md`'s index still shows T02 as `open`. That file says the frontmatter
  is authoritative and the table a snapshot, and it is outside this ticket's files, so
  the table was not edited.

### Open points

- The seed module parses: settled. `test_seed_module_is_clean` passed (above).
- `[tool.mypy] files` covers `template/scripts`: settled, it does not. Carried forward
  as the T00 follow-up above; step 9's explicit strict run is green.
- `run_script` returns `CompletedProcess[str]` with `text=True`: settled, yes
  (`tests/helpers.py`, `run_script`), so step 7's assertions are unchanged.
- GitHub Releases reachable from the `fast` job: not settled. It was reachable from this
  machine; the first pull request run of `ci.yml`, after an authorised push, settles it.
- `core.fileMode`: settled, `git config core.fileMode` prints `true`, and the index
  already recorded `100755` from T00, so `update-index --chmod=+x` was not needed.

## Open points

- The seed module parses (CONVENTIONS.md §12, first claim, assigned to T06;
  `tests/test_specs.py` is its check). Under allium 3.6.1, the version
  `install_allium.py` pins and the binary at H `.tools/bin/allium`, the CONVENTIONS.md §7
  module text with `Tic Tac Toe Beans` in place of the name reports no diagnostics and
  no findings for both `check` and `analyse` through `run_allium.py`, and an empty
  `docs/specs/` exits 1 with `resolved no specification under docs/specs/`. So a red
  test points at the download or at T00's rendered module differing from §7. Check: step
  8; to reproduce offline, copy H's `.tools/bin/allium` into a render's `.tools/bin/` and
  run `python3 scripts/run_allium.py check` there. Record the outcome; do not edit the
  module.
- Whether T00's `pyproject.toml` lists `template/scripts` under `[tool.mypy] files`, so
  that `just typecheck` covers the scripts. Check: `grep -n -A3 'tool.mypy' pyproject.toml`
  and step 9. If not, hand back to a T00 follow-up; the explicit
  `uv run --frozen mypy --strict template/scripts` in step 9 is the acceptance meanwhile.
- Whether `tests/helpers.py`'s `run_script` returns `CompletedProcess[str]` with
  `text=True` as CONVENTIONS.md §9 says. Check: read it in step 2. If it returns bytes or
  an exit code, adapt step 7's assertions to what it returns and note the deviation.
- Whether GitHub Releases is reachable from the `fast` job for the two `install_allium.py`
  downloads. Check: the first pull request run of `ci.yml`, which is after the
  authorised push. A refusal there is a network fact for the maintainer, not a template
  defect.
- Whether `git config core.fileMode` is `true` in the worktree so `git add` records the
  bit. Check: step 6's `git ls-files -s`; the `update-index --chmod=+x` fallback settles
  it either way.
