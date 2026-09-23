---
id: C08
title: Move the workflow pin to the release that skips the Chromatic publish on a single-commit history
status: done
depends_on: [C01]
parallel_with: []
branch: chromatic-fix
estimated_size: S
---

# C08: Take the tooling release that keeps a game's first push green

## Context

Chromatic refuses a repository whose history is one commit and fails the build with
`Found only one commit`: it has no ancestor to take a baseline from. A game rendered from
this template commits everything once (README, "Render a game") and pushes that single
commit to `main`, which runs `.github/workflows/chromatic.yml` — so the first push fails as
soon as `CHROMATIC_PROJECT_TOKEN` is set on the repository, on a publish nobody asked for.
The workflow already survives the other reason a publish cannot happen, an unset token, by
noting it and skipping while the run stays green (decision `0006`, "A missing token is not
a failure either").

The fix is not in this repository. Since `v1.0.0` the three workflows are thin callers
(`CHANGELOG.md`, `1.0.0` Managed), and the jobs live in
`steven-cutting/biscuit_games_tooling` as `game-chromatic.yml`, pinned here by commit. The
fix and its release were handed off to that repository as a self-contained prompt on
2026-09-22 (`ai_tmp/chromatic-one-commit-prompt.md` in the `chromatic-fix` worktree, which
is gitignored; the hand-off is summarised under "Upstream half" below). This ticket is this
repository's half: take the release.

Read first: `CONVENTIONS.md` §11 (separately authorised steps), `AGENTS.md`,
`template/docs/how-to/maintain-dependencies.md` "Actions in the workflows", and
`CHANGELOG.md`'s `1.0.0` Managed entry as the model for the wording.

**Upstream half, for reference.** In `biscuit_games_tooling`, the token check in
`game-chromatic.yml`'s `chromatic` job becomes one step, `Decide whether a build can be
published`, that also runs `git rev-list --count HEAD` (the checkout takes
`fetch-depth: 0`, so the count is the whole history). Its `publish` and `reason` outputs
gate the publish step and word the reply on a pull request, so a skipped publish always
says which of the two skipped it. Released as `v0.3.0`: the jobs change and no caller needs
an edit.

## Goal

The three rendered workflows call `biscuit_games_tooling` at `v0.3.0`, so a game rendered
after the next template release publishes nothing on its first push, says so in a notice,
and stays green — with or without the token — and publishes normally from the second commit
onward.

## Non-goals

- Editing `biscuit_games_tooling`. That is the hand-off above; this ticket starts after
  `v0.3.0` is tagged there.
- Moving the package pin `biscuit-games-tooling @ …@v0.2.0` in `template/pyproject.toml`.
  The package is unchanged by that release, and `tests/test_render.py` does not couple the
  package pin to the workflow pin. Moving it would force every game to relock for nothing.
- `template/docs/decisions/0006-visual-review-in-chromatic.md`. It is seed
  (`tests/inventory.py`), so a change reaches no game that already exists, and its claim —
  that a game does not fail its first push for a secret it has not created — stays true.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `template/.github/workflows/chromatic.yml` | M | T03's workflow | Line 46: the pinned commit and its `# v0.1.0` comment; lines 47-48: the comment on the optional secret gains the one-commit skip |
| `template/.github/workflows/ci.yml` | M | T03's workflow | Line 28: the same pin, moved with it |
| `template/.github/workflows/pages.yml` | M | T03's workflow | Line 31: the same pin, moved with it |
| `template/docs/reference/quality-gates.md` | M | T08's page | The middle of the three shellchecked `run:` blocks is no longer "the token check"; it is the publish decision. The count of three stays right |
| `CHANGELOG.md` | repo | this repository | One bullet under Unreleased, Managed |
| `tickets/C08-chromatic-single-commit.md` | repo | this ticket | `status:` |
| `tickets/README.md` | repo | index | The C08 row's status |

## Steps

1. Confirm the release exists and resolve its commit. The tags there are annotated, so a
   tag reference answers the tag object, which no `uses:` line accepts:

   ```sh
   gh api repos/steven-cutting/biscuit_games_tooling/commits/v0.3.0 --jq .sha
   ```

2. Replace the forty-character commit and the `# v0.1.0` comment with that commit and
   `# v0.3.0` in **all three** callers. `tests/test_render.py::test_pins_agree` collects the
   `(sha, tag)` pairs from the render and asserts there is exactly one, and
   `template/docs/how-to/maintain-dependencies.md` tells a game the same thing, so the three
   move together even though only `game-chromatic.yml` changed.
3. In `template/.github/workflows/chromatic.yml`, the comment above `secrets:` says the
   called workflow notes an absent token and skips the publish. Add the second skip in the
   same voice: a history of one commit, which Chromatic refuses, is skipped the same way, so
   a game's first push to `main` is green whether or not the secret exists.
4. In `template/docs/reference/quality-gates.md`, reword the few words that name the second
   of the three multi-line `run:` blocks "the token check". It decides the publish now. Do
   not change the count: the release keeps that workflow at three blocks deliberately.
5. `CHANGELOG.md`, under Unreleased → Managed, in the shape of the `1.0.0` entry: the three
   callers move to `v0.3.0`, which skips the publish with a notice when the checkout is a
   single commit, so a game's first push to `main` no longer fails once
   `CHROMATIC_PROJECT_TOKEN` is set, and the reply on a `/chromatic` comment names which
   skip happened. A pin bump is MINOR (README, "Versions"). Nothing goes under Update notes:
   a game resolves the markers `copier update` writes in the three workflows and does
   nothing else.
6. `git add` the changed files before trusting the gate — `just lint` runs
   `prek run --all-files`, which lists files through git — then `just test` and `just check`
   (AGENTS.md: never change `template/` without `just test`, never commit without
   `just check`).
7. Flip this ticket's `status:` to `done` and the row in `tickets/README.md` with it.
8. **Authorisation required:** pushing the branch, opening the pull request (with Copilot
   and Codex requested on it) and any tag. `CONVENTIONS.md` §11.

## Acceptance criteria

- [x] `grep` over `template/.github/workflows/*.yml` shows one commit and `# v0.3.0` in all
      three files, and that commit is what `gh api …/commits/v0.3.0 --jq .sha` answers.
- [x] `just test` is green, `test_pins_agree` included.
- [x] `just check` is green.
- [x] `CHANGELOG.md` carries the Managed bullet and no Update-notes entry.
- [x] `template/docs/reference/quality-gates.md` no longer calls the publish decision "the
      token check", and still says three blocks.
- [x] Nothing under `template/pyproject.toml`, `template/uv.lock` or
      `docs/decisions/0006-*` changed.

## Verification

On the branch, in this repository:

```sh
gh api repos/steven-cutting/biscuit_games_tooling/commits/v0.3.0 --jq .sha
grep -n 'biscuit_games_tooling/.github/workflows/' template/.github/workflows/*.yml
just test
just check
```

Expected: one SHA, three matching `uses:` lines carrying it with `# v0.3.0`, and two green
runs. Record the SHA, the three lines and the tail of each run in the hand-back.

The behaviour itself cannot be exercised from here: it runs in a game's repository on a
push to `main`. The first render made from the next template release is the real check —
its first push should show `::notice::` on the Chromatic run, no published build, and a
green run — and whoever makes it reports back on this ticket.

## Hand-back notes

Executed on 2026-09-22 on `chromatic-fix`, the branch the ticket names.

- Upstream: the hand-off merged as `biscuit_games_tooling` PR 4 (`6c5c07f`, CI `check`
  green on `main`), carrying `version = "0.3.0"` and `## [0.3.0]` in its changelog.
  `v0.3.0` was not tagged by that session; it was tagged from here with the maintainer's
  authorisation, annotated, on `6c5c07f`, and pushed. `git show v0.3.0:` of
  `game-chromatic.yml` has three `run: |` blocks (lines 61, 203, 246), so
  `quality-gates.md`'s count stands.
- The release and the three moved lines:

  ```text
  $ gh api repos/steven-cutting/biscuit_games_tooling/commits/v0.3.0 --jq .sha
  6c5c07f6bec86e86b3930dfa41392e4b440e8c85
  $ grep -n 'biscuit_games_tooling/.github/workflows/' template/.github/workflows/*.yml
  template/.github/workflows/pages.yml:31:    uses: steven-cutting/biscuit_games_tooling/.github/workflows/game-pages.yml@6c5c07f6bec86e86b3930dfa41392e4b440e8c85 # v0.3.0
  template/.github/workflows/chromatic.yml:46:    uses: steven-cutting/biscuit_games_tooling/.github/workflows/game-chromatic.yml@6c5c07f6bec86e86b3930dfa41392e4b440e8c85 # v0.3.0
  template/.github/workflows/ci.yml:28:    uses: steven-cutting/biscuit_games_tooling/.github/workflows/game-ci.yml@6c5c07f6bec86e86b3930dfa41392e4b440e8c85 # v0.3.0
  ```

- `just check`, with every changed file staged: all 18 hooks Passed, actionlint among
  them; mypy "Success: no issues found in 10 source files"; pytest `45 passed, 3 skipped`
  in 61 s, `test_pins_agree` included. `just check` runs `just test`, so that is the
  `just test` result too. The three skips are the `full` and network cases, which need
  `BISCUIT_TEMPLATE_FULL=1` and `BISCUIT_TEMPLATE_NETWORK=1`.
- Not yet confirmed in a real run: no game has been rendered from a template release that
  carries this pin. The first one's first push is the check.
- Open point on the branch: settled by doing it here — the ticket and the pin move are one
  pull request.

## Open points

- The template release that carries this pin. A pin bump is MINOR, but it may ride with
  other Unreleased work rather than being cut on its own; whoever cuts the release decides.
- Whether the pull request here waits for `v0.3.0` (this ticket's `branch:` field is
  `chromatic-fix`, the worktree the hand-off was written in, so the ticket and the pin move
  can be one pull request). If the ticket is merged on its own first, execute the steps
  above on `ticket/c08-chromatic-single-commit` from `main`, per `CONVENTIONS.md` §11.
