---
id: T01
title: "Toolchain configs: every root dotfile and config the render ships"
status: done
depends_on: [T00]
parallel_with: [T02, T03, T04, T05, T06, T07, T08, T09]
branch: ticket/t01-toolchain-configs
estimated_size: M
---

# T01: Toolchain configs: every root dotfile and config the render ships

## Context

This repository is a Copier template; everything under `template/` renders into a new
Biscuit Games game (CONVENTIONS.md §0). The twenty-one files in this ticket are the
root of that render: the formatter, linter, test-runner and hook configuration a game
carries from Poodl, in generic form. Every one of them is **managed** (CONVENTIONS.md
§5): `copier update` re-renders it and merges the game's edits three-way, so what is
written here reaches every game on every update. Nine of them are files a game is
expected to edit as well (`M†`), which is why they follow the bottom-append layout
convention of CONVENTIONS.md §5: the template's own entries sit in the upper blocks, and
a game appends at the end.

Where this ticket sits: T00 merged before it. T00 created `copier.yml`, the harness and
the fast suite, and left every path in the table below as a stub (Poodl's file with the
tokens `test_no_poodl_outside_provenance` forbids scrubbed) so the suite could be green
from the first commit. Treat the stubs as placeholders: overwrite each from the source
the table names rather than editing the stub. T02 to T09 run in parallel and own the
other lanes; T10 (`tests/test_full.py` and the `full` CI job) and T11 (the first
consumer render) wait on this lane, because `just initialize` and `just check` inside a
render read these files first.

Sources, at the commits CONVENTIONS.md §0 pins, and how they are named below:

- `P` = `/Users/scutting/projects/poodl` at `0a46a485`.
- `H` = `/Users/scutting/projects/biscuit_games` at `09b4894a` (four commits after the
  tag `v1.0.0`; the files this lane takes from H are identical at both).

Check `git -C /Users/scutting/projects/poodl rev-parse --short HEAD` prints `0a46a48`
and the same for the hub prints `09b4894`; if either clone has moved, read the pinned
content with `git -C <clone> show <commit>:<path>` instead of the working file. Never
modify either clone.

Read first, in this order: CONVENTIONS.md §4 (the tree; this ticket's rows are the
root-level `M`/`M†` entries), §5 (managed versus seed, the `M†` layout convention), §6
(Jinja rules: `.jinja` only where an answer is substituted), §9 (what the template
repository's own gate lints under `template/` at source), §13 (the
`.copier-answers.yml` risk); then the twenty P root files the table names,
`H/eslint.config.js`, `H/pyproject.toml` (already the generic shape this ticket wants),
and `P/.github/workflows/ci.yml` lines 32, 46 and 49-51 (the pins that
`tests/test_render.py::test_pins_agree` holds equal to `package.json` and
`.python-version`).

What changes against Poodl, and why: everything that exists only because Poodl owns a
domain (`site/`, `site-root/`, the `stage` and `stage-preview` recipes and script) or
ships word lists (`src/lib/data/`) is dropped, because decision 2 in CONVENTIONS.md §1
makes every game a project Pages site with no staging step; Poodl's two ESLint
vocabulary rules go with them (the hub's `eslint.config.js` is the source, minus its
package-only `dist/` ignore); `.copier-answers.yml` joins `.prettierignore` because
Copier rewrites that file on every update and Prettier would rewrite it back
(CONVENTIONS.md §13); and exactly two files carry an answer, `package.json.jinja`
(`game_slug`) and `pyproject.toml.jinja` (`game_slug`, `game_name_escaped`), both
computed or asked in CONVENTIONS.md §3. The hub package version in `package.json.jinja`
stays the literal `1.0.0` Poodl pins: `test_pins_agree` holds it equal to `copier.yml`'s
`hub_package_version`, and there is no `hub_package_version` substitution.

## Goal

Every path in the table below holds its designed content: nine byte-for-byte copies of
Poodl's files, ten Poodl or hub files with the named lines dropped or rewritten, and two
`.jinja` files that substitute an answer and nothing else. A render with the default
answers is byte-identical to the template source for every non-`.jinja` file, carries no
Jinja delimiter in the two rendered files, mentions nothing Poodl-specific, and agrees
with the CI workflows on every tool pin. Inside a render, `just initialize` leaves only
the two lockfiles untracked, and `just lint` and `just frontend-static` pass.

## Non-goals

- No lockfile is shipped, ever (`test_no_lockfiles_shipped`); `just initialize` in the
  render creates both.
- No `{{ hub_package_version }}` substitution in `package.json.jinja`, and no other
  `.jinja` suffix in this ticket than the two named.
- No `stage`, `stage-preview`, `site/` or `site-root/` anywhere: the render is a project
  Pages site (CONVENTIONS.md §1 decision 2), and `pages.yml` (T03) uploads `build/`.
- Poodl's two ESLint rules (`no-misused-spread`, `restrict-template-expressions`) are
  not carried; a game that needs one appends it (CONVENTIONS.md §5).
- No `import? 'Justfile.local'` or other extension point; that is C07's question.
- Nothing under `template/scripts/` or `template/.claude/` (T02), no workflow or the
  copilot adapter (T03), no `AGENTS.md.jinja`, `CLAUDE.md` or skill (T04), nothing under
  `template/src/`, `template/tests/`, `template/.storybook/` or `template/static/`
  (T05), no specification (T06), no handbook page (T07 to T09).
- No edit to `copier.yml`, `tests/inventory.py`, `tests/test_render.py` or any harness
  file (T00; a needed change is handed back as a T00 follow-up on `main`), and no
  `tests/test_full.py` (T10).
- No token written into any file, and no repository setting touched (CONVENTIONS.md
  §11).

## Files touched

Class follows CONVENTIONS.md §5, which lists nine of these as files the game is expected
to edit (`M†`); the tree in §4 marks six of those nine as plain `M` (see Open points).
Line numbers are the source file's at the pinned commit and were verified.

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `template/.editorconfig` | M | `P/.editorconfig` | verbatim (29 lines) |
| `template/.gitattributes` | M | `P/.gitattributes` | drop lines 5-6: the blank line and `src/lib/data/*.txt linguist-generated=true` |
| `template/.gitignore` | M† | `P/.gitignore` | drop lines 24-27: the `just stage` comment, `site/`, and the blank line after |
| `template/.markdownlint-cli2.jsonc` | M | `P/.markdownlint-cli2.jsonc` | drop line 21 (`"site",`) |
| `template/.npmrc` | M | `P/.npmrc` | verbatim (one line naming the registry; no token) |
| `template/.pre-commit-config.yaml` | M† | `P/.pre-commit-config.yaml` | drop line 10, the `src/lib/data/` alternative in `exclude` |
| `template/.pre-commit-fix.yaml` | M† | `P/.pre-commit-fix.yaml` | drop line 12, the `src/lib/data/` alternative in `exclude` |
| `template/.prettierignore` | M† | `P/.prettierignore` | drop line 6 (`site`) and lines 14-16 (word-list comment, `src/lib/data`, blank); append the `.copier-answers.yml` block; exact content in step 4 |
| `template/.prettierrc.json` | M | `P/.prettierrc.json` | verbatim |
| `template/.python-version` | M | `P/.python-version` | verbatim (`3.14`) |
| `template/chromatic.config.json` | M | `P/chromatic.config.json` | verbatim (`autoAcceptChanges` is `main`) |
| `template/eslint.config.js` | M† | `H/eslint.config.js` | remove `'dist/',` and the space after it from the `ignores` list on line 11; nothing else |
| `template/lychee.toml` | M† | `P/lychee.toml` | drop line 14 (`"site",`) |
| `template/package.json.jinja` | M† | `P/package.json` | line 2 becomes `"name": "{{ game_slug }}",`; drop line 20 (the `stage` script) |
| `template/pyproject.toml.jinja` | M† | `P/pyproject.toml` | name, description, the `[tool.uv]` comment and the typos block change; exact content in step 8 |
| `template/svelte.config.js` | M | `P/svelte.config.js` | replace the comment block at lines 4-15; code unchanged; exact content in step 6 |
| `template/tsconfig.json` | M | `P/tsconfig.json` | verbatim |
| `template/vite.config.ts` | M | `P/vite.config.ts` | verbatim (coverage thresholds stay 90) |
| `template/vitest.config.ts` | M | `P/vitest.config.ts` | verbatim |
| `template/vitest.storybook.config.ts` | M | `P/vitest.storybook.config.ts` | verbatim (keeps `optimizeDeps.include`, line 47) |
| `template/Justfile` | M† | `P/Justfile` | drop lines 68-80: `stage`, `stage-preview`, their comments, and the blank line after |

Where CONVENTIONS.md §4 says "minus line 6", "minus lines 24-26", "minus lines 14-15"
and "minus lines 68-79", the ranges above add the adjoining blank line so that no file
ends in a blank line or carries two blank lines in a row; the content is otherwise the
same.

## Steps

1. Create the worktree on `ticket/t01-toolchain-configs` from `main` (README.md "How to
   pick up a ticket"), run `just sync`, and confirm `just test` is green before touching
   anything: the suite must be green on the stubs, or the failure is not yours.

2. The nine verbatim files. From the repository root, in bash or zsh:

   ```sh
   P=/Users/scutting/projects/poodl
   for f in .editorconfig .npmrc .prettierrc.json .python-version \
     chromatic.config.json tsconfig.json vite.config.ts vitest.config.ts \
     vitest.storybook.config.ts; do cp "$P/$f" "template/$f"; done
   ```

   Check: `cmp "$P/$f" "template/$f"` prints nothing for each. Do not "improve" a
   comment in any of them; `vite.config.ts` keeps the four `90` thresholds and
   `vitest.storybook.config.ts` keeps `optimizeDeps: { include: [...] }` (P line 47).

3. The seven line drops. `sed 'A,Bd' <source> > <destination>` is the same on BSD and
   GNU sed, which is why no `-i` is used:

   ```sh
   sed '5,6d' "$P/.gitattributes" > template/.gitattributes
   sed '24,27d' "$P/.gitignore" > template/.gitignore
   sed '21d' "$P/.markdownlint-cli2.jsonc" > template/.markdownlint-cli2.jsonc
   sed '10d' "$P/.pre-commit-config.yaml" > template/.pre-commit-config.yaml
   sed '12d' "$P/.pre-commit-fix.yaml" > template/.pre-commit-fix.yaml
   sed '14d' "$P/lychee.toml" > template/lychee.toml
   sed '68,80d' "$P/Justfile" > template/Justfile
   ```

   Before running each, confirm the range holds what the table says (`sed -n 'A,Bp'`):
   `.gitignore` 24-26 open with `` # What `just stage` assembles `` and end with `site/`;
   `Justfile` 68-79 run from `# Assembles what Pages serves` through the `stage-preview`
   recipe body. After the drops, `template/.gitattributes` is four lines ending
   `uv.lock linguist-generated=true`; `template/Justfile` is 164 lines, its `preview`
   recipe followed by one blank line and `# The component workshop on port 6006`, and
   every other recipe, `initialize` through `chromatic`, byte-identical to Poodl's (the
   render's `ci.yml`, T03, calls `just lock-check`, which stays Poodl's two lines).

4. `template/.prettierignore`, written whole (P minus line 6 and lines 14-16, plus the
   final block):

   ```text
   .svelte-kit
   build
   coverage
   node_modules
   package-lock.json
   storybook-static

   # Markdown belongs to markdownlint-cli2. Two formatters over the same files
   # disagree eventually, and `just fix` runs markdownlint before Prettier, so the
   # disagreement would surface as a gate that never converges.
   *.md

   # The manifest is strict JSON despite the extension, because validate_docs.py
   # parses it with json.loads. Prettier reads the .yml and rewrites it as YAML
   # with single quotes, which is no longer JSON and fails the contract outright.
   docs/manifest.yml

   # Copier owns the answers file and rewrites it on every `copier update`.
   # Prettier would reformat YAML it does not own, so without this line
   # `prettier --check` and the regenerated file fight after every update.
   .copier-answers.yml
   ```

   Check: `diff "$P/.prettierignore" template/.prettierignore` reports line 6 and lines
   14-16 removed and the last five lines added, nothing else.

5. `template/eslint.config.js` from the hub, minus the package-only ignore:

   ```sh
   H=/Users/scutting/projects/biscuit_games
   sed "11s|'dist/', ||" "$H/eslint.config.js" > template/eslint.config.js
   ```

   Check: `diff "$H/eslint.config.js" template/eslint.config.js` prints exactly

   ```diff
   11c11
   <     ignores: ['.svelte-kit/', 'build/', 'coverage/', 'dist/', 'node_modules/', 'storybook-static/']
   ---
   >     ignores: ['.svelte-kit/', 'build/', 'coverage/', 'node_modules/', 'storybook-static/']
   ```

   The result is 46 lines and has no `rules:` block: Poodl's two vocabulary rules
   (`P/eslint.config.js` lines 42-57) are deliberately absent.

6. `template/svelte.config.js`: copy `P/svelte.config.js`, then replace lines 4-15 (the
   `/** ... */` block that opens `Poodl is a static site` and names `/poodl` and
   `pnut.fans`) with this block, leaving lines 1-3 and 16-46 untouched:

   ```js
   /**
    * This game is a static site with no server, so every route is prerendered and
    * the build output is a directory of files a host can serve as-is.
    *
    * `paths.base` is empty by default, which is what `just dev`, the unit tests
    * and a local `just preview` see. GitHub Pages serves a project site beneath
    * the repository's name, so `pages.yml` sets BASE_PATH to `/<repository name>`
    * from the workflow event and the build lands under that path. Nothing here
    * names the repository, so this file is the same in every game and a template
    * update carries it unchanged. See decision 0010.
    */
   ```

   Check: `diff "$P/svelte.config.js" template/svelte.config.js` reports one hunk,
   `4,15c4,14`, and `grep -n 'process.env.BASE_PATH' template/svelte.config.js` still
   finds the `paths` line.

7. `template/package.json.jinja`:

   ```sh
   sed -e '2s/"poodl"/"{{ game_slug }}"/' -e '20d' "$P/package.json" > template/package.json.jinja
   ```

   Check: `diff "$P/package.json" template/package.json.jinja` prints exactly

   ```diff
   2c2
   <   "name": "poodl",
   ---
   >   "name": "{{ game_slug }}",
   20d19
   <     "stage": "sh scripts/stage_site.sh",
   ```

   `"version": "0.1.0"`, `"packageManager": "npm@11.17.0"`, the `engines` and `volta`
   blocks, and `"@steven-cutting/biscuit-games": "1.0.0"` stay literal; `test_pins_agree`
   reads them. `game_slug` matches `^[a-z][a-z0-9]*(_[a-z0-9]+)*$` (CONVENTIONS.md §3),
   which is always a legal unscoped npm name.

8. `template/pyproject.toml.jinja`, written whole. It is `P/pyproject.toml` with lines 2
   and 4 carrying the answers, the `[tool.uv]` comment made generic (P line 15 says
   "Poodl ships no Python package", which `test_no_poodl_outside_provenance` rejects, and
   line 17 names a decision file that does not exist in the render; the template's is
   `docs/decisions/0004-python-toolchain.md`, T09), and the typos block reduced to the
   hub's (P lines 57-58 and 62 dropped):

   ```toml
   [project]
   name = "{{ game_slug }}-tooling"
   version = "0.1.0"
   description = "Repository tooling for {{ game_name_escaped }}. Not the application; see package.json for that."
   requires-python = ">=3.14"
   dependencies = []

   [dependency-groups]
   dev = [
     "prek==0.4.12",
     "ruff==0.16.2",
   ]

   [tool.uv]
   # This game ships no Python package. This project exists so `uv run --frozen`
   # can provide a pinned prek and ruff to the hooks; see
   # docs/decisions/0004-python-toolchain.md.
   package = false
   default-groups = ["dev"]

   [tool.ruff]
   line-length = 99
   target-version = "py314"
   unsafe-fixes = false
   src = ["scripts"]

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
   # These are single-file command-line checkers: they print, they take no
   # annotations beyond their own signatures, and they shell out to git by design.
   "scripts/**" = [
     "ANN", "BLE001", "EM101", "EM102", "INP001", "PLR0912", "PLR0915",
     "PLR2004", "S404", "S603", "S607", "T201", "TRY003",
   ]

   [tool.ruff.format]
   quote-style = "double"
   indent-style = "space"
   line-ending = "lf"

   [tool.typos.files]
   # Lockfiles carry hashes that look like typos.
   extend-exclude = [
     "package-lock.json",
     "uv.lock",
   ]
   ```

   Check: `diff "$H/pyproject.toml" template/pyproject.toml.jinja` reports changes on
   lines 2, 4, 15 and 17 only. `game_name_escaped` (CONVENTIONS.md §3) already escapes
   the backslash and the double quote for a TOML basic string, and the questionnaire
   refuses control characters, so the description is always a legal string.

9. Residue check at source, from the repository root: `grep -n -i -E
   'poodl|pnut|site-root|stage_site|stage-preview|word list|word-list|dist/'` over
   the twenty-one files must print nothing. Then `grep -l -s '{{' template/*.jinja
   template/.[a-z]*` must list only `package.json.jinja` and `pyproject.toml.jinja`
   among this ticket's files (CONVENTIONS.md §6 rule 1; `-s` silences the directory
   entries the second glob matches).

10. `just check` from the repository root (the template repository's gate: lock check,
    prek over `template/` at source, mypy, the fast suite). The four tests the brief
    names must pass: `test_verbatim_files_are_byte_identical`,
    `test_rendered_jinja_files_carry_no_delimiter`, `test_no_poodl_outside_provenance`,
    `test_pins_agree`. A prek finding on one of this ticket's files (editorconfig,
    typos, check-json, check-toml, check-yaml, ripsecrets) is fixed at source; one on
    another lane's file is recorded, not fixed.

11. The render check (Verification, second block). It needs the network and a
    `read:packages` token in `~/.npmrc` as `//npm.pkg.github.com/:_authToken=<your token>`
    so `npm` can read `@steven-cutting/biscuit-games`. Never create, paste or commit a
    token: if `~/.npmrc` carries none, `just initialize` fails at
    `npm install --package-lock-only` with an npm authentication error against
    `npm.pkg.github.com`; record that in the hand-back notes and carry the render check
    to T10's `test_full` and T11. Commit inside the render before `just initialize` (no
    hook exists yet) so `git status --porcelain` afterwards shows what the first run
    wrote: exactly `package-lock.json` and `uv.lock` untracked. A modified (`M`) line
    means `initialize.sh` reformatted a shipped file with ruff, ESLint or Prettier; for a
    file in the table above, fix it at source so the file ships already formatted; for
    any other file, record it with the owning lane. `just lint` in the render also runs
    the validators and the spec hooks over other lanes' stubs; a failure there on a file
    outside the table is recorded with its lane, never fixed here. Chromium is not
    needed for `lint` or `frontend-static`, so do not run `storybook-browsers-deps`.

12. Fill in the hand-back notes with the outputs quoted, set `status: done` in this
    file, and commit on the ticket branch. **Authorisation required:** pushing the
    branch and opening the pull request are separately authorised (CONVENTIONS.md §11);
    stop and ask the maintainer.

## Acceptance criteria

- [ ] Every path in the Files touched table exists with the content the Steps specify,
      and nothing outside the table changed except this ticket's `status:` line.
- [ ] The nine verbatim files are byte-identical to Poodl's (`cmp` prints nothing).
- [ ] The seven `sed` results and the two embedded-diff results match the source with
      exactly the lines the table names dropped or changed.
- [ ] `template/.prettierignore` ends with the `.copier-answers.yml` block and no longer
      lists `site` or `src/lib/data`.
- [ ] `template/eslint.config.js` has no `rules:` block and its `ignores` list carries
      neither `dist/` nor `site/`.
- [ ] `template/svelte.config.js` differs from Poodl's only at lines 4-15, and the new
      comment names neither Poodl nor a domain.
- [ ] `template/package.json.jinja` and `template/pyproject.toml.jinja` are the only
      `.jinja` files in the table; the first substitutes `game_slug` once, the second
      `game_slug` and `game_name_escaped` once each; the hub package pin is the literal
      `1.0.0`.
- [ ] None of the twenty-one files matches, case-insensitively, `poodl`, `pnut`,
      `site-root`, `stage_site`, `stage-preview`, `word list`, `word-list` or `dist/`.
- [ ] `just check` is green in the template repository, including
      `test_verbatim_files_are_byte_identical`, `test_rendered_jinja_files_carry_no_delimiter`,
      `test_no_poodl_outside_provenance` and `test_pins_agree`.
- [ ] In a render with `git init -b main`: `just initialize` exits 0 and leaves exactly
      `package-lock.json` and `uv.lock` untracked and nothing modified; `just lint` and
      `just frontend-static` exit 0. Or, with no `read:packages` token available, the
      hand-back notes say so and name T10's `test_full` as the check that runs it.
- [ ] Hand-back notes filled in with the outputs quoted; `status: done`.

## Verification

Template repository, from its root:

```sh
just check
just test tests/test_render.py -v
```

Expected: both exit 0; the second lists `test_verbatim_files_are_byte_identical`,
`test_rendered_jinja_files_carry_no_delimiter`, `test_no_poodl_outside_provenance` and
`test_pins_agree` as `PASSED`.

Source equality, from the repository root in bash or zsh (each `cmp` prints nothing; the
three `diff`s report only the hunks named in Steps 4, 6 and 8):

```sh
P=/Users/scutting/projects/poodl
H=/Users/scutting/projects/biscuit_games
for f in .editorconfig .npmrc .prettierrc.json .python-version \
  chromatic.config.json tsconfig.json vite.config.ts vitest.config.ts \
  vitest.storybook.config.ts; do cmp "$P/$f" "template/$f"; done
cmp <(sed '5,6d' "$P/.gitattributes") template/.gitattributes
cmp <(sed '24,27d' "$P/.gitignore") template/.gitignore
cmp <(sed '21d' "$P/.markdownlint-cli2.jsonc") template/.markdownlint-cli2.jsonc
cmp <(sed '10d' "$P/.pre-commit-config.yaml") template/.pre-commit-config.yaml
cmp <(sed '12d' "$P/.pre-commit-fix.yaml") template/.pre-commit-fix.yaml
cmp <(sed '14d' "$P/lychee.toml") template/lychee.toml
cmp <(sed '68,80d' "$P/Justfile") template/Justfile
cmp <(sed -e '2s/"poodl"/"{{ game_slug }}"/' -e '20d' "$P/package.json") template/package.json.jinja
cmp <(sed "11s|'dist/', ||" "$H/eslint.config.js") template/eslint.config.js
diff "$P/.prettierignore" template/.prettierignore
diff "$P/svelte.config.js" template/svelte.config.js
diff "$H/pyproject.toml" template/pyproject.toml.jinja
```

Residue at source (expected: no output, exit status 1):

```sh
grep -n -i -E 'poodl|pnut|site-root|stage_site|stage-preview|word list|word-list|dist/' \
  template/.editorconfig template/.gitattributes template/.gitignore \
  template/.markdownlint-cli2.jsonc template/.npmrc template/.pre-commit-config.yaml \
  template/.pre-commit-fix.yaml template/.prettierignore template/.prettierrc.json \
  template/.python-version template/chromatic.config.json template/eslint.config.js \
  template/lychee.toml template/package.json.jinja template/pyproject.toml.jinja \
  template/svelte.config.js template/tsconfig.json template/vite.config.ts \
  template/vitest.config.ts template/vitest.storybook.config.ts template/Justfile
```

The render (needs the network and a `read:packages` token in `~/.npmrc`; `ai_tmp/` is
gitignored in the template repository):

```sh
rm -rf ai_tmp/t01-render
just render ai_tmp/t01-render
cd ai_tmp/t01-render
git init -q -b main
git add -A
git -c user.name=render -c user.email=render@example.invalid commit -q -m 'Rendered from the template'
just initialize
git status --porcelain
just lint
just frontend-static
```

Expected: `just render` prints `Rendered into ai_tmp/t01-render`; `just initialize`
exits 0 with `Ready. Next: just check.` on its penultimate line (the last line is
`Nothing has been staged, committed, tagged, or pushed.`); `git status --porcelain`
prints exactly

```text
?? package-lock.json
?? uv.lock
```

and `just lint` and `just frontend-static` each exit 0. Without a token, `just initialize`
fails at `npm install --package-lock-only`; quote that error in the hand-back notes.

## Hand-back notes

### What was verified, and how

Both clones were at their pinned commits (`git rev-parse --short HEAD` printed `0a46a48`
and `09b4894`). Before any edit, `just sync && just test` printed `27 passed`. Every
command below ran on the edited working tree; output is quoted, and each elision is
marked with square brackets.

```text
$ just check
uv lock --check
Resolved 33 packages in 3ms
uv run --frozen prek run --all-files
[18 hook lines, every one ending Passed]
uv run --frozen mypy
Success: no issues found in 6 source files
uv run --frozen pytest "$@"
collected 27 items

tests/test_render.py .......................                             [ 85%]
tests/test_validators.py ....                                            [100%]

======================= 27 passed, 16 warnings in 10.66s =======================

$ just test tests/test_render.py -v
tests/test_render.py::test_inventory_matches_classification PASSED       [  4%]
tests/test_render.py::test_verbatim_files_are_byte_identical PASSED      [  8%]
tests/test_render.py::test_rendered_jinja_files_carry_no_delimiter PASSED [ 13%]
tests/test_render.py::test_no_poodl_outside_provenance PASSED            [ 17%]
tests/test_render.py::test_answers_file_and_provenance PASSED            [ 21%]
tests/test_render.py::test_no_lockfiles_shipped PASSED                   [ 26%]
tests/test_render.py::test_pins_agree PASSED                             [ 30%]
tests/test_render.py::test_managed_pages_link_only_to_stable_pages PASSED [ 34%]
[the fourteen refused-answer cases and the accepted-punctuation case, every one PASSED]
======================= 23 passed, 16 warnings in 10.43s =======================
```

The sixteen warnings are copier's `DirtyLocalWarning: Dirty template changes included
automatically.`, raised because the edits were not yet committed.

Source equality, the Verification block run in bash: all nine verbatim `cmp` lines, the
seven `sed` drops, `package.json.jinja` and `eslint.config.js` printed nothing. The
three `diff`s:

```text
$ diff "$P/.prettierignore" template/.prettierignore
6d5
< site
14,16d12
< # Word lists are data, one word per line.
< src/lib/data
<
20a17,21
>
> # Copier owns the answers file and rewrites it on every `copier update`.
> # Prettier would reformat YAML it does not own, so without this line
> # `prettier --check` and the regenerated file fight after every update.
> .copier-answers.yml
$ diff "$P/svelte.config.js" template/svelte.config.js
5,6c5,6
[Poodl's two lines, then step 6's first sentence]
8,14c8,13
[Poodl's seven lines naming /poodl and the domain, then step 6's second paragraph]
$ diff "$H/pyproject.toml" template/pyproject.toml.jinja
2c2
< name = "biscuit-games-tooling"
---
> name = "{{ game_slug }}-tooling"
4c4
< description = "Repository tooling for Biscuit Games. Not the site; see package.json for that."
---
> description = "Repository tooling for {{ game_name_escaped }}. Not the application; see package.json for that."
15c15
< # Biscuit Games ships no Python package. This project exists so `uv run --frozen`
---
> # This game ships no Python package. This project exists so `uv run --frozen`
17c17
< # docs/decisions/0006-python-toolchain.md.
---
> # docs/decisions/0004-python-toolchain.md.
```

`wc -l` gives `template/.gitattributes` 4, `template/Justfile` 164 and
`template/eslint.config.js` 46; `eslint.config.js` has no `rules:`. The residue grep
printed nothing and exited 1. `grep -l -s '{{' template/*.jinja template/.[a-z]*` lists
`package.json.jinja` and `pyproject.toml.jinja` and, outside this ticket, the answers
file template, `AGENTS.md.jinja`, `CHANGELOG.md.jinja` and `README.md.jinja`.
`package.json.jinja` carries `{{ game_slug }}` once; `pyproject.toml.jinja` carries
`{{ game_slug }}` and `{{ game_name_escaped }}` once each; the hub pin is
`"@steven-cutting/biscuit-games": "1.0.0"`.

The render, with a `read:packages` token in `~/.npmrc`:

```text
$ just render ai_tmp/t01-render
Rendered into ai_tmp/t01-render
$ git init -q -b main && git add -A && git -c user.name=render -c user.email=render@example.invalid commit -q -m 'Rendered from the template'
$ just initialize
[uv lock, uv sync, npm install --package-lock-only, npm ci: added 377 packages, playwright install chromium]
installed allium 3.6.1 at [ai_tmp/t01-render]/.tools/bin/allium
74 files left unchanged

> tic_tac_toe_beans@0.1.0 lint:fix
> svelte-kit sync && eslint . --fix && prettier --write .

[ai_tmp/t01-render]/stories/Lockup.stories.svelte
  83:31  error  Invalid type "320" of template literal expression  @typescript-eslint/restrict-template-expressions

✖ 1 problem (1 error, 0 warnings)

error: recipe `initialize` failed on line 15 with exit code 1
$ git status --porcelain
?? package-lock.json
?? uv.lock
$ just lint
uv run --frozen prek run --all-files
Ruff lint................................................................Passed
Ruff format check........................................................Passed
ESLint and Prettier......................................................Failed
- hook id: eslint
- exit code: 1
[the same Lockup.stories.svelte 83:31 error]
Documentation contract...................................................Passed
Agent instruction contract...............................................Passed
Specification diagnostics................................................Passed
Specification analysis...................................................Passed
[the sixteen builtin and remote hooks, every one ending Passed]
error: recipe `lint` failed on line 89 with exit code 1
$ just frontend-static
npm run lint
[the same Lockup.stories.svelte 83:31 error]
error: recipe `frontend-static` failed on line 92 with exit code 1
```

`initialize.sh` stopped at ESLint, so its `prettier --write .` and `install-hooks` never
ran, and the `git status` above proves only that ruff and `eslint --fix` rewrote nothing.
Run in the render afterwards to cover the rest:

```text
$ npx eslint .
[only the Lockup.stories.svelte 83:31 error]
$ npx prettier --list-different .
tests/platformSpecs.test.ts
$ npm run check
[...] ERROR "src/lib/components/Lockup.svelte" 20:11 "Type 'string' is not assignable to type 'never'."
[...] COMPLETED 806 FILES 1 ERRORS 0 WARNINGS 1 FILES_WITH_PROBLEMS
```

No file in the table is flagged by ESLint, would be rewritten by Prettier, or fails any
hook in the render. The render half of the acceptance criteria is nonetheless not met as
written: `just initialize`, `just lint` and `just frontend-static` each exit 1, on three
files other lanes own (Handed back, below). T10's `test_full` and T11 run the same check
once those land.

### Deviations, and why

- **Branch.** The work is on `T01-toolchain-configs`, the Supacode worktree's branch, as
  T00's was `T00-foundation`, not on `ticket/t01-toolchain-configs`.
- **Fifteen of the twenty-one stubs were already the designed files.** Every path was
  still rewritten from its source with this ticket's commands, and those fifteen came
  out byte-identical to T00's stubs. Six changed: `.markdownlint-cli2.jsonc`,
  `lychee.toml` and `.prettierignore` still listed `site`; `eslint.config.js` still
  ignored `dist/`; `svelte.config.js` carried T00's shorter comment; and
  `pyproject.toml.jinja` wrapped line 15 differently and cited
  `docs/decisions/0004-python-toolchain-in-a-frontend-repo.md`.
- **`svelte.config.js` diffs as two hunks, not `4,15c4,14`.** `diff` keeps the unchanged
  comment opener, bare-asterisk line and closer as context. The content is what step 6 says: `cmp <(sed -n
  '1,3p;16,$p' "$P/svelte.config.js") <(sed -n '1,3p;15,$p' template/svelte.config.js)`
  and `cmp` of template lines 4-14 against step 6's block both printed nothing.
- **Steps 4, 6 and 8** were extracted from this file's fences by a script, not retyped.
- **Step 3 under zsh with `noclobber`.** Each `sed ... > template/<file>` refused to
  overwrite its stub (`file exists: template/.gitattributes`) and was rerun with `>|`.
  The Verification block, run in bash, is unaffected.
- **Files touched preamble.** It says §4 marks six of the nine `M†` files as plain `M`;
  §4 as committed marks all nine `M†`, as Open points says. Nothing needed changing.

### Handed back

- **T05.** `stories/Lockup.stories.svelte` line 83 interpolates the number
  `NARROWEST_SUPPORTED_WIDTH` into a template literal, which the hub's
  `strictTypeChecked` refuses now that Poodl's `allowNumber` override is not carried (a
  Non-goal of this ticket). T05 step 9's `FRAME_WIDTH` through `String()` removes it.
  Until then `initialize.sh` aborts at `npm run lint:fix` in every render
  (CONVENTIONS.md §13), and `just lint` and `just frontend-static` fail on it.
- **T06.** `tests/platformSpecs.test.ts` is not Prettier-formatted: Prettier breaks the
  `readdirSync(SPECS).filter(...).sort()` chain on line 85 and the three figure rows on
  lines 95 and 97-99, which pass `printWidth` 100. `npm run lint` fails on it once the
  ESLint error is gone, and `initialize.sh`'s `prettier --write .` would modify it.
- **CONVENTIONS.md §0 and the hub, as T00 handed back.** `svelte-check` still reports
  `src/lib/components/Lockup.svelte:20:11` against the published 1.0.0, so `npm run
  check`, the second half of `just frontend-static`, fails until that is resolved.
- **T00.** No follow-up: `GAME_EDITED` matches §5.

### Open points settled

- **`M†` in the inventory.** `GAME_EDITED` in `tests/inventory.py` equals the fourteen
  paths §5 lists (a set comparison printed `14 14 True`).
- **`just lint` inside a render.** With allium 3.6.1 installed by `just initialize`,
  Documentation contract, Agent instruction contract, Specification diagnostics and
  Specification analysis all pass on the other lanes' stubs. The one failing hook is
  ESLint and Prettier, on T05's story.
- **Prettier and Copier's answers file.** With the default answers, `npx prettier
  --check --ignore-path /dev/null .copier-answers.yml` (both ignore files disabled, rather
  than editing `.prettierignore`) printed `All matched files use Prettier code style!`.
  T00's review showed that a description PyYAML quotes and folds is rewritten, so the
  entry stays required.

## Open points

CONVENTIONS.md §12 assigns no claim to this ticket. These arose while writing it:

- **`M†` in the inventory.** CONVENTIONS.md §4 and §5 both mark `eslint.config.js`,
  `.gitignore`, `.prettierignore`, `lychee.toml`, both prek configs and
  `pyproject.toml.jinja` as `M†`, and this ticket's table follows them.
  `tests/inventory.py` (T00) records the same set in `GAME_EDITED`. Check:
  `grep -n -A 20 'GAME_EDITED' tests/inventory.py` and compare with §5's list. If the two
  differ, do not edit the file; hand back a T00 follow-up on `main` naming the paths and
  citing §5.
- **`just lint` inside a render at this lane's point in time.** The render's prek gate
  runs `validate-docs`, `validate-agents`, `check-specs` and `analyse-specs` over the
  other lanes' stubs and needs the allium binary `just initialize` installs. Check: the
  render block in Verification. A failure on a file outside the table is recorded with
  its lane in the hand-back notes; only this ticket's files are fixed.
- **Whether Prettier would in fact rewrite Copier's answers file.** The `.prettierignore`
  entry is required by CONVENTIONS.md §4 and §13 regardless. Check, optional, inside the
  render after `just initialize`: remove the `.copier-answers.yml` line, run
  `npx prettier --check .copier-answers.yml`, restore the line; record whether Prettier
  reported the file as needing formatting.
