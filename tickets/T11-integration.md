---
id: T11
title: Integration: first green render, tag v0.1.0, render tic_tac_toe_beans
status: done
depends_on: [T10, T13]
parallel_with: []
branch: ticket/t11-integration
estimated_size: M
---

# T11: Integration: first green render, tag v0.1.0, render tic_tac_toe_beans

## Context

Every build ticket before this one changed the template. This one changes nothing in
it: it proves the merged template on `main` renders a game that passes its own gate,
puts the first tag on that commit, and renders the first real consumer,
`steven-cutting/tic_tac_toe_beans`, from the tag. CONVENTIONS.md §1 decision 4 names
that repository as the end-to-end verification.

Order: T00 and the nine lanes T01 to T09 have merged, then T10 (which added
`tests/test_full.py` and the `full` CI job), then T13 (which moves the hub pin to the
release whose `Wordmark` takes `product`: that `Wordmark` error was the one failure T10
recorded in a render's gate). T12
(template `README.md`, `CHANGELOG.md`, `AGENTS.md`) waits for this ticket, and so does
C07 (Poodl adopts the template), which needs `v0.1.0` to exist. T12 writes the
`CHANGELOG.md` entry for `v0.1.0` after the tag; that file is a template-repository
file, not a rendered one, so the tag does not have to wait for it.

Why the tag comes before the consumer render (CONVENTIONS.md §10 and §13): the answers
file records `_commit` from `git describe --tags --always`, so an untagged render
records a bare SHA, and every later `copier update` then leans on dunamai's
`0.0.0.postN` fallback to order versions. Why the stub `README.md` is deleted first
(CONVENTIONS.md §3, the comment above `_skip_if_exists`, and §13): `_skip_if_exists`
lists `/README.md` and is consulted before overwrite, so `copier copy` into a directory
that already holds a `README.md` keeps the stub, and `_message_after_copy` prints too
late to warn.

State of the consumer clone at `/Users/scutting/projects/tic_tac_toe_beans` when this
ticket was written: branch `main` tracking `origin/main`
(`git@github.com:steven-cutting/tic_tac_toe_beans.git`), one commit `4f84e9d`
("first commit"), one tracked file `README.md` (20 bytes, `# tic_tac_toe_beans`),
worktree clean. The GitHub repository is private. The template repository
`steven-cutting/biscuit_games_template` is public, default branch `main`, no tags yet.

Read first, in this order:

- CONVENTIONS.md §0 (sources and tooling versions), §3 (`copier.yml`: the seed lists,
  `_message_after_copy`, the four questions and their defaults), §5 (the answers file
  and its one sanctioned hand edit), §9 (`just render`, `just test-full`), §10 (tags
  and versions), §11 (separately authorised actions), §12 (the two claims assigned
  here) and §13 (the risks this ticket meets: tag first, delete the stub, the first
  `just check` needs the network).
- P `Justfile` lines 13-15 (`initialize` runs `scripts/initialize.sh`), 131-133
  (`check-docs` runs markdownlint, typos and lychee, then the docs validator) and
  166-168 (`check` runs `scripts/run_project_check.py run`). The rendered `Justfile`
  is this file minus lines 68-79.
- H `scripts/initialize.sh` (the rendered `scripts/initialize.sh`): line 7 needs a
  Git worktree; lines 9-13 write `uv.lock` and `package-lock.json` and install both
  trees (`npm install` and `npm ci` read `@steven-cutting/biscuit-games` from GitHub
  Packages, so the token must be in `~/.npmrc` before this runs); line 19 downloads
  Chromium; line 36 installs the allium binary; lines 40-42 run the formatters; lines
  52-57 install hooks only from a primary checkout (the consumer clone is one); lines
  59-60 print "Ready. Next: just check." and that nothing was staged, committed,
  tagged or pushed.
- P `scripts/run_project_check.py` (rendered verbatim): lines 18-30 name the eleven
  `RECIPES`, and line 106 runs `check-clean` after them, so `just check` runs twelve
  gates; lines 53-55 and 72-77 show the worktree snapshot includes
  untracked, non-ignored files, so the two lockfiles are in it and must not change
  during a check; lines 106-108 pass the baseline to `check-clean`, so a dirty tree
  with untracked files passes as long as nothing changes; line 118 prints "All checks
  passed and the worktree is unchanged."
- P `docs/how-to/deploy-to-github-pages.md` lines 22-25 (Pages source must be GitHub
  Actions; the `github-pages` environment is created on the first run) and 29-31 (until
  then the deploy job fails with `Failed to create deployment (status: 404)`).
- P `docs/reference/quality-gates.md` lines 141-142 (the required checks are the three
  CI job names `frontend`, `documents`, `stories`) and P `.github/workflows/ci.yml`
  lines 16 (`packages: read`), 42-43 (registry and scope) and 57 (`NODE_AUTH_TOKEN`
  from `github.token`): the first push installs the hub package with the run's own
  token, which works only once the package grants the repository read access.

## Goal

- The merged `main` renders a game in which `just initialize` and then `just check`
  pass, first as a scratch render (`just test-full` green, or `just render` plus the
  two commands by hand).
- Annotated tag `v0.1.0` on that `main` commit, pushed to `origin`, so that
  `git describe --tags origin/main` prints `v0.1.0` and `copier` picks it as the
  latest PEP 440 tag.
- `/Users/scutting/projects/tic_tac_toe_beans` holds a render from `v0.1.0` with the
  answers `game_name` "Tic Tac Toe Beans", `game_slug` `tic_tac_toe_beans`,
  `description` "A tic-tac-toe game played with beans." (or the sentence the
  maintainer confirms instead) and `repository` `steven-cutting/tic_tac_toe_beans`;
  `.copier-answers.yml` names `_commit: v0.1.0` and
  `_src_path: gh:steven-cutting/biscuit_games_template`; the rendered `AGENTS.md`
  provenance names the template and `v0.1.0`; `just initialize` and `just check` pass
  there; nothing is committed or pushed in that clone without the maintainer's word.
- The hand-back notes record what the first push will need (C03) and which open
  points were settled.

## Non-goals

- Editing any file under `template/`, `copier.yml` or `tests/` on this branch. A fix a
  scratch render reveals goes back to the lane that owns the file (the index in
  [README.md](README.md) and the tree in CONVENTIONS.md §4 say which) or lands as a
  small follow-up pull request on `main`; this branch carries only its own ticket file.
- Repository settings on either repository: Pages source, required checks, the package
  read grant, the Chromatic secret. That is C03, applied by the maintainer.
- The template `README.md`, `CHANGELOG.md` entry for `v0.1.0` and `AGENTS.md`: T12.
- Rendering Poodl or converging Poodl's drift: C07.
- Adding game content to `tic_tac_toe_beans` beyond what the template renders: the
  render is the deliverable; the game is the maintainer's.
- Committing, pushing or deploying in `tic_tac_toe_beans`, unless separately
  authorised in step 8.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `/Users/scutting/projects/tic_tac_toe_beans/README.md` | S | the consumer's stub (20 bytes) | Deleted before the render so `_skip_if_exists` does not keep it; replaced by the render of `README.md.jinja` |
| the rendered tree under `/Users/scutting/projects/tic_tac_toe_beans/` (every path in CONVENTIONS.md §4 plus `.copier-answers.yml`, then `package-lock.json` and `uv.lock` from `just initialize`) | M, M†, S | `copier copy --vcs-ref v0.1.0` | Created; `_src_path` in `.copier-answers.yml` hand-edited to the GitHub URL only if the render used a local path; nothing else edited by hand |
| template repository: tag `v0.1.0` | repo | the merged `main` commit the green scratch render came from | Annotated tag created and pushed (authorisation required) |
| template repository: any file a scratch render proves wrong | as CONVENTIONS.md §4 classes it | the lane that owns it | Not edited on this branch; diagnosed in the hand-back notes and fixed on `main` through that lane or a follow-up (authorisation required to push or open the pull request) |

Plus the `status:` line and the hand-back notes of `tickets/T11-integration.md`.

## Steps

1. Create the worktree from `main` after T10 has merged (README.md "How to pick up a
   ticket"), then confirm the starting point:

   ```sh
   git fetch origin main
   git log --oneline -1 origin/main
   just sync && just check
   grep -c '_authToken' ~/.npmrc
   uvx copier --version
   ```

   `just check` is green (the fast suite); `grep` prints at least `1` (the token line
   `//npm.pkg.github.com/:_authToken=<your token>` from CONVENTIONS.md §11 and
   `_message_after_copy`); copier prints `9.18.2`. If `~/.npmrc` has no token, stop:
   every step from 2 onward reads the hub package.

2. Scratch render until the gate is green. The automated form is the `full` test, which
   copies a default render, runs `git init -q -b main`, `just initialize`, `just check`
   and asserts the untracked set is exactly `package-lock.json` and `uv.lock`
   (CONVENTIONS.md §9, `test_full.py`; 10 to 20 minutes, network, Chromium):

   ```sh
   just test-full tests/test_full.py
   ```

   When it fails, or to look at the tree, render by hand and run the same two
   commands; `ai_tmp/` is gitignored and `just render` refuses to overwrite:

   ```sh
   rm -rf ai_tmp/render
   just render ai_tmp/render
   cd ai_tmp/render && git init -q -b main && just initialize && just check
   ```

   Diagnose a failure to a rendered path and its owning lane (CONVENTIONS.md §4).
   Write the path, the failing recipe, the output and the proposed change into the
   hand-back notes, then stop. **Authorisation required:** the fix lands on `main`
   through the owning lane or a follow-up pull request; pushing that branch and opening
   the pull request are the maintainer's to authorise, and this branch never carries
   the fix. Once it has merged, `git fetch origin main && git merge --no-edit
   origin/main` here and repeat this step from the top. Record in the hand-back notes
   the `origin/main` SHA the green run came from.

3. Tag that commit. **Authorisation required:** creating and pushing the tag
   (CONVENTIONS.md §11); stop and ask, quoting the SHA from step 2. When authorised:

   ```sh
   git fetch origin main
   git rev-parse origin/main
   git tag -a v0.1.0 -m 'biscuit_games_template v0.1.0' origin/main
   git describe --tags origin/main
   git push origin v0.1.0
   git ls-remote --tags origin v0.1.0
   ```

   `rev-parse` prints the SHA step 2 recorded (if it does not, `main` moved: go back to
   step 2); `describe` prints `v0.1.0`; `ls-remote` prints one line. The tag is
   annotated `vMAJOR.MINOR.PATCH` on `main` exactly as CONVENTIONS.md §10 requires;
   copier parses the leading `v`. Then run `just test` here once more:
   `tests/test_update.py` now finds `v0.1.0` as the latest tag and runs the pristine
   update from it as well as from `HEAD~2`; both pass.

4. Prepare the consumer clone and settle the answers. Check the clone is as the
   Context describes (anything else is a question for the maintainer, not a thing to
   tidy):

   ```sh
   cd /Users/scutting/projects/tic_tac_toe_beans
   git status --porcelain --branch
   git log --oneline
   git ls-files
   ```

   Expected: `## main...origin/main` and nothing else; one commit; `README.md` only.
   The answers: `game_name` is `Tic Tac Toe Beans`; `game_slug` takes its default,
   which CONVENTIONS.md §3 derives as `tic_tac_toe_beans` (T10's
   `test_computed_defaults` proves it); `repository` takes its default
   `steven-cutting/tic_tac_toe_beans`, which is the real repository name, so
   `pages_url` renders as `https://steven-cutting.github.io/tic_tac_toe_beans/`;
   `description` is proposed as `A tic-tac-toe game played with beans.`
   **Authorisation required:** the maintainer confirms or replaces the description
   before the render (10 to 200 characters, no braces). Then delete the stub, which
   the maintainer authorised as part of rendering into the clone:

   ```sh
   rm README.md
   git status --porcelain
   ```

   Expected: one line, `D README.md` after porcelain's leading space (deleted, unstaged).

5. Render from the tag. Once step 3 has pushed the tag, use the GitHub shorthand, which
   records the wanted `_src_path` directly (copier expands `gh:` to
   `https://github.com/steven-cutting/biscuit_games_template.git`, and the repository
   is public, so no credential is needed):

   ```sh
   cd /Users/scutting/projects/tic_tac_toe_beans
   uvx copier copy --vcs-ref v0.1.0 --defaults \
     -d 'game_name=Tic Tac Toe Beans' \
     -d 'description=A tic-tac-toe game played with beans.' \
     gh:steven-cutting/biscuit_games_template .
   ```

   `--defaults` takes the derived `game_slug` and `repository`; the two `-d` values are
   the answers step 4 settled (substitute the confirmed description). Never pass
   `--trust`: the template has no tasks (CONVENTIONS.md §2). Quote the
   `_message_after_copy` text that prints at the end in the hand-back notes. If the tag
   exists locally but its push is not yet authorised, render from the local checkout
   instead: replace the `gh:` argument with the absolute path of this ticket's worktree
   (`git rev-parse --show-toplevel` there; the tag is a shared ref, visible from every
   worktree, and with a ref other than `HEAD` copier clones the tagged commit, not the
   working tree). Then make the one sanctioned hand edit (CONVENTIONS.md §5): in
   `.copier-answers.yml` change the `_src_path:` value to
   `gh:steven-cutting/biscuit_games_template` and nothing else.

6. Inspect the render before anything runs:

   ```sh
   grep -n '^_commit\|^_src_path' .copier-answers.yml
   grep -n 'v0.1.0' AGENTS.md docs/how-to/update-from-template.md
   find . -name '*.jinja' -not -path './node_modules/*'
   ls docs/specs
   grep -n 'GAME_' src/lib/brand.ts
   git status --porcelain | grep -v '^?? '
   ```

   Expected: `_commit: v0.1.0` and `_src_path: gh:steven-cutting/biscuit_games_template`;
   `AGENTS.md` carries the Provenance sentence from CONVENTIONS.md §7 ("Rendered by
   Copier from the `biscuit_games_template` template ... at `v0.1.0`") and the how-to
   page states the same version; `find` prints nothing; `ls` prints
   `tic_tac_toe_beans.allium`; `brand.ts` reads `GAME_NAME = 'tic tac toe beans'`,
   `GAME_TITLE = 'Tic Tac Toe Beans'` and `GAME_DESCRIPTION` with the confirmed
   sentence; the last command prints one line, `M README.md` after porcelain's leading
   space (the stub's path, now the rendered seed), because every other rendered path is
   untracked.

7. Initialise and check, in the clone, on this machine (macOS: `initialize.sh` prints
   the Linux notice only on Linux, so no `just storybook-browsers-deps` here):

   ```sh
   just initialize
   git status --porcelain | grep -v '^?? '
   git status --porcelain --ignored | grep '^!! '
   just check
   ```

   `initialize` ends with "Ready. Next: just check." and installs the hooks (primary
   checkout). After it, the only non-untracked line is still the `M README.md` one; the
   untracked set gained exactly `package-lock.json` and `uv.lock`; the ignored set is
   what the rendered `.gitignore` names (`.venv/`, `node_modules/`, `.svelte-kit/`,
   `.tools/`; P `.gitignore` lines 2, 19-22, 31, 36 in the rendered copy) and, after
   `check`, `build/`, `coverage/` and `storybook-static/`. `just check` ends with "All
   checks passed and the worktree is unchanged." Its `check-docs` recipe is the first
   run of typos over this slug and name (CONVENTIONS.md §12): if typos flags
   `tic_tac_toe_beans`, `beans` or the description, record the word; the remedy is an
   `extend-words` entry under `[tool.typos]` in the game's `pyproject.toml`, which is
   the game's edit and needs the maintainer's word, so stop and ask rather than edit.
   The first `lint` clones every hook repository (CONVENTIONS.md §13), so an offline
   failure there is not a template failure: reconnect and rerun `just check`.

8. Record and hand back. Write the `_message_after_copy` text, the tail of `just check`,
   the `git status --porcelain` lines that are not `??`, and the answers used into the
   hand-back notes. **Authorisation required:** committing and pushing in
   `tic_tac_toe_beans`. The maintainer authorised rendering into the clone as
   verification and nothing more, so the ticket ends with the render uncommitted; if the
   maintainer then authorises it, one commit of everything (the answers file and both
   lockfiles included, as `_message_after_copy` says) on `main`, and a push only on a
   second explicit word. Set this ticket's `status:` to `done` and commit that on the
   ticket branch.

9. State in the hand-back notes what the consumer's first push needs, so the maintainer
   applies C03 to `steven-cutting/tic_tac_toe_beans` first: the Pages source set to
   GitHub Actions (otherwise `pages.yml`'s deploy job fails with `Failed to create
   deployment (status: 404)`, P `docs/how-to/deploy-to-github-pages.md` 29-31), and the
   `@steven-cutting/biscuit-games` package granting the repository read access (a
   setting on the package, CONVENTIONS.md §11) so `ci.yml`'s `npm ci` with
   `github.token` succeeds. With both in place, `frontend`, `documents` and `stories`
   are expected green on the first push, and the first `pages.yml` run is the check for
   `github.event.repository.name` (CONVENTIONS.md §12). Note that the repository is
   private: GitHub Pages from a private repository needs a paid plan, which is a
   maintainer decision, not a template concern.

## Acceptance criteria

- [ ] `just test-full tests/test_full.py` passed on the commit that became `v0.1.0`, or
      a hand render of that commit passed `just initialize` and `just check`; the SHA
      is quoted in the hand-back notes.
- [ ] `git describe --tags origin/main` prints `v0.1.0`; the tag is annotated and
      pushed (`git ls-remote --tags origin v0.1.0` prints one line); its creation and
      push were authorised.
- [ ] `just test` is green in the template worktree after the tag, including
      `tests/test_update.py` from `v0.1.0`.
- [ ] In `/Users/scutting/projects/tic_tac_toe_beans`: `.copier-answers.yml` names
      `_commit: v0.1.0` and `_src_path: gh:steven-cutting/biscuit_games_template`;
      `AGENTS.md` provenance names `biscuit_games_template` and `v0.1.0`; no `.jinja`
      path exists; `docs/specs/tic_tac_toe_beans.allium` exists.
- [ ] The answers are `Tic Tac Toe Beans`, `tic_tac_toe_beans`, the confirmed
      description and `steven-cutting/tic_tac_toe_beans`; the description was confirmed
      by the maintainer.
- [ ] `just initialize` then `just check` are green in the clone; `just check` printed
      "All checks passed and the worktree is unchanged."
- [ ] `git status --porcelain` in the clone shows `README.md` as modified and unstaged
      plus untracked lines for the rendered tree and the two lockfiles, nothing staged,
      `git log` still one commit; or the maintainer authorised a commit and the notes
      say so.
- [ ] No file under `template/`, `copier.yml` or `tests/` changed on this branch;
      any fix a render revealed is recorded as handed back.
- [ ] The hand-back notes carry the C03 needs for the first push and the outcome of the
      two open points below.

## Verification

From the template worktree, before and after the tag:

```sh
just check
just test-full tests/test_full.py
git describe --tags origin/main
git ls-remote --tags origin v0.1.0
just test
```

Expected: the fast gate green; the `full` test passes (10 to 20 minutes); `v0.1.0`;
one `refs/tags/v0.1.0` line; the fast suite green with the `v0.1.0` update case
collected and passed.

From `/Users/scutting/projects/tic_tac_toe_beans`, after the render:

```sh
grep -n '^_commit\|^_src_path' .copier-answers.yml
grep -c 'v0.1.0' AGENTS.md
find . -name '*.jinja' -not -path './node_modules/*' | wc -l
ls docs/specs
just initialize
just check
git status --porcelain | grep -v '^?? '
git status --porcelain | grep -c '^?? '
git log --oneline | wc -l
```

Expected: `_commit: v0.1.0` and `_src_path: gh:steven-cutting/biscuit_games_template`;
a count of at least `1`; `0`; `tic_tac_toe_beans.allium`; "Ready. Next: just check.";
"All checks passed and the worktree is unchanged."; one line, `M README.md` after
porcelain's leading space; a count equal to the number of rendered paths minus one (the
README) plus two (the lockfiles); `1`.

## Hand-back notes

### Outcome

- `just test-full tests/test_full.py` passed on `origin/main` at
  `6612b7e470b5b9e41d1086cc58d540404c476fbf`, which merged pull request 12, and
  `test_render_passes_its_own_gate` passed with it.
- Annotated tag `v0.1.0` points at that commit and is pushed; the tag object is
  `f3636e8`, and `git describe --tags origin/main` prints `v0.1.0`.
  - The maintainer authorised creating and pushing it on two conditions: the full test
    had to be green, and `main` must not have moved. Both held.
- `just test` after the tag: 45 passed, 3 skipped. The update case from the latest tag
  ran from `v0.1.0` and passed, next to the `HEAD~2` case.
- `/Users/scutting/projects/tic_tac_toe_beans` holds a render from `v0.1.0`.
  - It was rendered through `gh:`, so `_src_path` needed no hand edit.
  - `just initialize` and `just check` passed there.
- The answers:
  - `game_name`: `Tic Tac Toe Beans`
  - `game_slug`: `tic_tac_toe_beans`
  - `description`: `A three-in-a-row game played with beans.`, the maintainer's choice
  - `repository`: `steven-cutting/tic_tac_toe_beans`
- **No commit or push in the clone.** The maintainer chose to leave the render
  uncommitted, so nothing there is staged and `git log` still shows one commit.
- **A committed copy passed as well.** The same bytes, committed in a scratch
  repository, passed `just initialize` and `just check` with every hook run over the
  whole tree. Deviations explains why that copy was needed.
- **No template change.** This branch carries only this ticket file: nothing under
  `template/`, `copier.yml` or `tests/` changed, and no repository setting changed on
  either repository.

### What was verified, and how

Output is quoted. Elisions are in square brackets, and so is the `=` padding of pytest's
summary lines.

Step 1, in this worktree:

```text
$ git log --oneline -1 origin/main
6612b7e Merge pull request #12 from steven-cutting/T10-harness-completion
$ just sync && just check
[18 hook lines, every one ending Passed; mypy: Success: no issues found in 10 source files]
SKIPPED [1] tests/test_update.py:84: no v* tag yet; T11 makes the first
[...] 44 passed, 4 skipped in 46.33s [...]
$ grep -c '^//npm.pkg.github.com/:_authToken=' ~/.npmrc
1
$ uvx copier --version
copier 9.18.2
$ git diff --stat 32ca849 6612b7e -- template copier.yml tests
[nothing]
```

`32ca849` is the commit on which T13's `just test-full` was green. The empty diff means
`main` renders the same tree.

Step 2:

```text
$ just test-full tests/test_full.py -v -s --durations=5
[...]
collecting ... collected 1 item
[just initialize]
prek installed at `.git/hooks/pre-commit`

Ready. Next: just check.
Nothing has been staged, committed, tagged, or pushed.
uv run --frozen python scripts/run_project_check.py run
==> just lock-check
==> just lint
==> just frontend-static
[...] COMPLETED 816 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS
==> just frontend-coverage
 Test Files  4 passed (4)
      Tests  30 passed (30)
Statements   : 100% ( 54/54 )
Branches     : 100% ( 15/15 )
Functions    : 100% ( 23/23 )
Lines        : 100% ( 52/52 )
==> just frontend-build
==> just storybook-build
==> just storybook-test
 Test Files  1 passed (1)
      Tests  3 passed (3)
==> just check-docs
uv run --frozen prek run --all-files markdownlint-cli2 typos lychee
markdownlint.............................................................Passed
typos....................................................................Passed
lychee...................................................................Passed
uv run --frozen python scripts/validate_docs.py
Validated 38 pages and 39 canonical topics.
==> just check-agents
Validated AGENTS.md, 2 adapters, and 8 skills.
==> just check-specs
allium check: 1 specifications, no diagnostics and no findings.
==> just analyse-specs
allium analyse: 1 specifications, no diagnostics and no findings.
==> just check-clean
The worktree matches the check baseline.

All checks passed and the worktree is unchanged.
PASSED
[...]
42.48s call     tests/test_full.py::test_render_passes_its_own_gate
[...] 1 passed in 44.86s [...]
```

Step 3:

```text
$ git fetch origin main && git rev-parse origin/main
6612b7e470b5b9e41d1086cc58d540404c476fbf
$ git tag -a v0.1.0 -m 'biscuit_games_template v0.1.0' origin/main
$ git describe --tags origin/main
v0.1.0
$ git push origin v0.1.0
To github.com:steven-cutting/biscuit_games_template.git
 * [new tag]         v0.1.0 -> v0.1.0
$ git ls-remote --tags origin v0.1.0
f3636e873cdf84c6606f8315b487d521be490ce0 refs/tags/v0.1.0
$ git cat-file -t v0.1.0
tag
$ just test -v
[...]
tests/test_update.py::test_pristine_update_equals_fresh_render[HEAD~2] PASSED [ 87%]
tests/test_update.py::test_pristine_update_equals_fresh_render[latest-tag] PASSED [ 89%]
tests/test_update.py::test_update_keeps_game_work PASSED                 [ 91%]
[...]
SKIPPED [1] tests/test_full.py:30: set BISCUIT_TEMPLATE_FULL=1
SKIPPED [1] tests/test_specs.py:26: set BISCUIT_TEMPLATE_NETWORK=1
SKIPPED [1] tests/test_specs.py:34: set BISCUIT_TEMPLATE_NETWORK=1
[...] 45 passed, 3 skipped in 55.78s [...]
```

`ls-remote` separates the SHA from the ref name with a tab; it is quoted here with a
space.

Step 4, in `/Users/scutting/projects/tic_tac_toe_beans`:

```text
$ git status --porcelain --branch
## main...origin/main
$ git log --oneline
4f84e9d first commit
$ git ls-files
README.md
$ rm README.md
$ git status --porcelain
 D README.md
```

Step 5:

```text
$ uvx copier copy --vcs-ref v0.1.0 --defaults \
    -d 'game_name=Tic Tac Toe Beans' \
    -d 'description=A three-in-a-row game played with beans.' \
    gh:steven-cutting/biscuit_games_template .
Copying from template version 0.1.0
    create  lychee.toml
[177 create lines in all, and no identical, skip, overwrite or conflict line]
Tic Tac Toe Beans is rendered. Nothing ran, no lockfile exists and Git is
untouched. In order:

  1. Put a GitHub token carrying read:packages in ~/.npmrc as
       //npm.pkg.github.com/:_authToken=<your token>
     @steven-cutting/biscuit-games is read from GitHub Packages, which refuses an
     anonymous read.
  2. git init -b main                   (skip inside an existing clone)
  3. just initialize                    (lockfiles, npm ci, Chromium, allium, hooks)
  4. just check
  5. Commit everything, .copier-answers.yml and both lockfiles included:
     copier update reads the answers file.

Before the first push: grant steven-cutting/tic_tac_toe_beans read access on the
@steven-cutting/biscuit-games package (a setting on the package, not on either
repository) so CI's own token can install it, and set the Pages source to
GitHub Actions so pages.yml can publish to https://steven-cutting.github.io/tic_tac_toe_beans/.
```

`--trust` was not passed, and copier printed no warning.

Step 6:

```text
$ cat .copier-answers.yml
# Managed by Copier. Do not edit by hand; run `copier update` instead.
_commit: v0.1.0
_src_path: gh:steven-cutting/biscuit_games_template
description: A three-in-a-row game played with beans.
game_name: Tic Tac Toe Beans
game_slug: tic_tac_toe_beans
repository: steven-cutting/tic_tac_toe_beans
$ grep -n 'v0.1.0' AGENTS.md docs/how-to/update-from-template.md
docs/how-to/update-from-template.md:13:`v0.1.0`. The answers the
AGENTS.md:149:(<https://github.com/steven-cutting/biscuit_games_template>) at `v0.1.0`.
$ find . -name '*.jinja' -not -path './node_modules/*'
[nothing]
$ ls docs/specs
tic_tac_toe_beans.allium
$ grep -n 'GAME_' src/lib/brand.ts
[lines 4 to 7: the module's doc comment]
14:export const GAME_NAME = 'tic tac toe beans';
15:export const GAME_TITLE = 'Tic Tac Toe Beans';
16:export const GAME_DESCRIPTION = 'A three-in-a-row game played with beans.';
$ git status --porcelain | grep -v '^?? '
 M README.md
```

`AGENTS.md` line 148 opens the provenance sentence: "Rendered by Copier from the
`biscuit_games_template` template".

The render was also compared with a local render of the tag. It used the same two
answers, from this worktree into `ai_tmp/tag-render`:

```text
$ diff -rq -x .git -x .copier-answers.yml /Users/scutting/projects/tic_tac_toe_beans ai_tmp/tag-render
[nothing; exit 0]
$ diff /Users/scutting/projects/tic_tac_toe_beans/.copier-answers.yml ai_tmp/tag-render/.copier-answers.yml
3c3
< _src_path: gh:steven-cutting/biscuit_games_template
---
> _src_path: /Users/scutting/.supacode/repos/biscuit_games_template/T11-integration
```

So the `gh:` render is byte for byte the local render of `v0.1.0`, 126 files including
the answers file. Its answers are the `DEFAULT_ANSWERS` that the `full` test renders
with.

Step 7, in the clone:

```text
$ just initialize
[...]
prek installed at `.git/hooks/pre-commit`

Ready. Next: just check.
Nothing has been staged, committed, tagged, or pushed.
$ git status --porcelain | grep -v '^?? '
 M README.md
$ git status --porcelain --ignored | grep '^!! '
!! .ruff_cache/
!! .svelte-kit/
!! .tools/
!! .venv/
!! node_modules/
$ diff -rq -x .git -x .copier-answers.yml -x node_modules -x .venv -x .svelte-kit -x .tools -x package-lock.json -x uv.lock . [this worktree]/ai_tmp/tag-render
Only in .: .ruff_cache
$ just check
==> just lock-check
==> just lint
Ruff lint............................................(no files to check)Skipped
[23 hook lines: 11 Passed and 12 "(no files to check)" Skipped, typos among the Passed]
==> just frontend-static
[...] COMPLETED 816 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS
==> just frontend-coverage
      Tests  30 passed (30)
[...]
==> just storybook-test
      Tests  3 passed (3)
==> just check-docs
markdownlint.............................................................Passed
typos....................................................................Passed
lychee...................................................................Passed
Validated 38 pages and 39 canonical topics.
==> just check-agents
Validated AGENTS.md, 2 adapters, and 8 skills.
==> just check-specs
allium check: 1 specifications, no diagnostics and no findings.
==> just analyse-specs
allium analyse: 1 specifications, no diagnostics and no findings.
==> just check-clean
The worktree matches the check baseline.

All checks passed and the worktree is unchanged.
```

The `diff` above shows `initialize` changed no rendered file: its only addition beside
the lockfiles and the ignored trees is `.ruff_cache`. Its untracked set gained exactly
`package-lock.json` and `uv.lock`.

The committed copy took the local render in `ai_tmp/tag-render` and set its `_src_path`
to the `gh:` value. It then ran `git init -q -b main` and committed everything with a
throwaway identity and `--no-verify`, in `ai_tmp/consumer-committed`:

```text
$ cmp .copier-answers.yml /Users/scutting/projects/tic_tac_toe_beans/.copier-answers.yml
[identical]
$ git ls-files | wc -l
     126
$ just initialize
[...]
Ready. Next: just check.
$ git status --porcelain
?? package-lock.json
?? uv.lock
$ just check
==> just lock-check
==> just lint
Ruff lint................................................................Passed
[all 23 hook lines Passed, none Skipped]
[...]
==> just check-docs
markdownlint.............................................................Passed
typos....................................................................Passed
lychee...................................................................Passed
Validated 38 pages and 39 canonical topics.
[...]
==> just check-clean
The worktree matches the check baseline.

All checks passed and the worktree is unchanged.
$ git status --porcelain
?? package-lock.json
?? uv.lock
```

Step 8, the clone's final state:

```text
$ git status --porcelain | grep -v '^?? '
 M README.md
$ git status --porcelain | grep -c '^?? '
39
$ git status --porcelain --untracked-files=all | grep -c '^?? '
127
$ git diff --cached --name-only
[nothing]
$ git log --oneline | wc -l
       1
$ git status --porcelain --ignored | grep '^!! '
!! .lycheecache
!! .ruff_cache/
!! .svelte-kit/
!! .tools/
!! .venv/
!! build/
!! coverage/
!! node_modules/
!! scripts/__pycache__/
!! storybook-static/
```

### Deviations, and why

- **Branch.** The branch is `T11-integration`, which Supacode created, not
  `ticket/t11-integration`. T10 and T13 ran on branches of the same shape.
- **Description.** The maintainer chose `A three-in-a-row game played with beans.` over
  the ticket's proposal. It is the sentence in `tests/conftest.py` `DEFAULT_ANSWERS` and
  in `just render`, so the consumer's answers are exactly the ones the `full` test
  renders.
- **An extra committed run.** `prek run --all-files` lists files through Git, and in the
  uncommitted clone the only tracked file is `README.md`.
  - The clone's `lint` skipped twelve hooks with "(no files to check)", and its
    `check-docs` ran markdownlint, typos and lychee over `README.md` alone.
  - The recipes that walk the filesystem did cover the whole tree: `frontend-static`
    read 816 files, and both validators and allium ran.
  - To give step 7 and the typos open point their intended reach, the same bytes were
    committed in `ai_tmp/consumer-committed`. There every hook ran over all 126 files
    and both commands passed. Nothing in the clone was staged for this.
- **Hooks in the clone.** `just initialize` installed prek's `pre-commit` hook into the
  clone's `.git/hooks`, as step 7 expects of a primary checkout.
- **Ignored set.** Three ignored paths appeared beyond those step 7 names:
  `.ruff_cache/` after `initialize`, and `.lycheecache` and `scripts/__pycache__/` after
  `check`. Git ignores all three, and none shows in `git status --porcelain`.
- **Untracked count.** Plain `git status --porcelain` folds each untracked directory into
  one line, so the Verification section's count prints `39`. With
  `--untracked-files=all` it prints `127`: the 126 rendered paths, minus `README.md`,
  plus the two lockfiles. That is the figure the Verification section describes.
- **`test-full` time.** The full test took 44.86 s, because T13's runs had already
  downloaded Chromium, allium and the hook repositories on this machine.

### Handed back

- **No template fixes.** No scratch render failed, so no rendered path was proved wrong
  and no fix is owed to a lane.
- **T12 and C07.** T12 can write the `CHANGELOG.md` entry for `v0.1.0`, and C07 has the
  tag it needs.
- **The clone is left uncommitted.** To commit it, make one commit of everything on
  `main`, `.copier-answers.yml` and both lockfiles included, as `_message_after_copy`
  says. A push needs its own authorisation and, first, the C03 items below.

### What the consumer's first push needs (C03)

The maintainer applies these to `steven-cutting/tic_tac_toe_beans` before its first
push:

1. **Set the Pages source to GitHub Actions.**
   - Today `gh api repos/steven-cutting/tic_tac_toe_beans/pages` answers
     `"status":"404"` (Not Found).
   - Without it, `pages.yml` builds its artefact but the deploy job fails with
     `Failed to create deployment (status: 404)`. See the rendered
     `docs/how-to/deploy-to-github-pages.md`, "One-time setup", lines 23 and 36.
   - The first run that reaches the deploy job creates the `github-pages` environment
     itself.
2. **Grant the repository read access on the `@steven-cutting/biscuit-games` package.**
   - Where: the package's Package settings, then Manage Actions access, then Add
     repository, with the Read role.
   - Why: the rendered `ci.yml` grants `packages: read` (line 16). Each job points
     `setup-node` at `https://npm.pkg.github.com` for `@steven-cutting` (lines 42-43,
     85-86, 138-139) and installs with `NODE_AUTH_TOKEN: ${{ github.token }}` (lines 57,
     103, 161).
   - Until the grant exists, that token cannot read the package and `npm ci` fails with
     `404 Not Found`.
3. **With both in place,** `frontend`, `documents` and `stories` are expected green on
   the first push. Those are the three required checks in the rendered
   `docs/reference/quality-gates.md`, "On `main`".
4. **The repository is private.** `gh repo view steven-cutting/tic_tac_toe_beans --json
   isPrivate,visibility` prints `{"isPrivate":true,"visibility":"PRIVATE"}`.
   - Pages from a private repository needs a paid GitHub plan, so the first `pages.yml`
     deploy may fail for that reason alone.
   - Making the repository public, or accepting no deployment for now, is the
     maintainer's decision.

### Open points settled

1. **typos and the slug or game name: settled, no finding.** In the committed copy,
   `just check-docs` ran typos over all 126 rendered files, and it passed. Those files
   carry the slug, the game name and the description. No `extend-words` entry is needed.
2. **`github.event.repository.name`: carried forward.** The rendered `pages.yml` sets
   `BASE_PATH: /${{ github.event.repository.name }}` at line 22.
   - No push in the clone was authorised, so no run has yet shown
     `BASE_PATH=/tic_tac_toe_beans`.
   - The check moves to the consumer's first push after C03.
3. **The description: settled.** The maintainer chose
   `A three-in-a-row game played with beans.` (Deviations).
4. **The private repository and Pages: carried forward to C03.** The Pages endpoint
   answers 404 today because Pages is not configured. Whether to go public is the
   maintainer's decision.

## Open points

- typos never flags the slug or the game name (CONVENTIONS.md §12, assigned here).
  Check: `just check-docs` inside the clone after `just initialize`; expected exit 0
  with no typos finding. If it fails, quote the word; the remedy is an `extend-words`
  entry under `[tool.typos]` in the game's `pyproject.toml`, applied only with the
  maintainer's word.
- `github.event.repository.name` is populated in a workflow-level `env` on `push` and
  `workflow_dispatch` (CONVENTIONS.md §12, assigned to T03 at source and here on the
  first push). Check: after C03 and the authorised first push, the first `pages.yml`
  run's build log shows `BASE_PATH=/tic_tac_toe_beans` and the site answers at
  `https://steven-cutting.github.io/tic_tac_toe_beans/`. This cannot be checked inside
  this ticket unless the push is authorised; carry it forward otherwise.
- The description sentence. Proposed: `A tic-tac-toe game played with beans.`; the
  maintainer confirms or replaces it in step 4.
- `steven-cutting/tic_tac_toe_beans` is private (`gh repo view
  steven-cutting/tic_tac_toe_beans --json isPrivate` printed `true`). Pages from a
  private repository needs a paid GitHub plan; the deploy job of the first `pages.yml`
  run may fail for that reason alone. Check: `gh api
  repos/steven-cutting/tic_tac_toe_beans/pages` after C03; the decision (make it
  public, or accept no deployment for now) is the maintainer's.
