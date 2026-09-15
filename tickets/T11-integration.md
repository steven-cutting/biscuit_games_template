---
id: T11
title: Integration: first green render, tag v0.1.0, render tic_tac_toe_beans
status: open
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

Filled in by the agent that executes this ticket.

- What was verified and how: the `origin/main` SHA the green scratch render came from;
  the `just test-full` or hand-render output tail; the tag commands and their output;
  the `just test` result after the tag; the `_message_after_copy` text; the
  `.copier-answers.yml` lines; the `just initialize` and `just check` tails in the
  clone; the non-`??` `git status` lines.
- The answers used, and the maintainer's confirmation of the description.
- Whether the render used `gh:` or a local path, and whether the `_src_path` hand edit
  was made.
- What deviated from the ticket and why.
- What was handed back: each rendered path a scratch render proved wrong, its owning
  lane, the failing recipe and the fix that landed on `main` (with its pull request).
- Whether a commit or push in `tic_tac_toe_beans` was authorised and made.
- What the first push needs (C03 items) and the private-repository Pages question.
- Which open points were settled, with the command output.

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
