---
id: C09
title: Gate the Pages deploy on CI
status: done
depends_on: [C01]
parallel_with: []
branch: fix-template-pages-gate
estimated_size: S
---

# C09: Deploy only what CI has passed

## Context

`template/.github/workflows/pages.yml` deployed on every push to `main`, plus
`workflow_dispatch`, and nothing tied it to `ci.yml`. Any commit that reached `main` was
published whether or not CI passed on it: a direct push by an administrator, whom the
protection `scripts/bootstrap_repo.sh` applies does not bind; the repository's first push,
which comes before any protection exists; and a merge whose result nobody tested, because
the branch is not required to be up to date first. Every rendered game inherits the file.

`steven-cutting/biscuit_studio` found the gap in a Codex adversarial review of its ticket
S04 and closed it for itself: its `pages.yml` is this template's file with one deviation, a
`workflow_run` gate on `CI` (S04, Step 2 "The gate" and the hand-back's "Adversarial
review, and the gate"). S04 left the template and `biscuit_games_tooling` to take the same
gate. This ticket is the template's half.

Read first: `AGENTS.md`, `CONVENTIONS.md` §5 (managed and seed, and the silent merge of an
identical change), `T03-workflows.md`, `C01-reusable-workflows.md`, and the studio's
`.github/workflows/pages.yml`, which is the reference implementation.

## Goal

A game's `pages.yml` runs when the workflow named `CI` completes on `main`, and its one job
deploys only a successful CI run of a push whose `head_sha` was `main`'s head when that run
finished. The file is the studio's, so the two copies of the gate cannot drift apart, but
for the job's comment: review of the pull request corrected it here, and the studio is owed
the same correction.

## Non-goals

- A manual deploy. `workflow_dispatch` on `pages.yml` would skip the gate, and accepting a
  dispatched CI run would make the file differ from the studio's for a path nobody has
  asked for. A redeploy is a re-run of a gated Pages run: a re-run keeps the original
  `GITHUB_SHA` and is allowed for 30 days, after which a redeploy takes a push.
- Gating `chromatic.yml`. It is not a required check, and its push to `main` sets the
  baseline whether or not CI is green, as decision `0006` intends.
- `steven-cutting/biscuit_games_tooling`. Its README's "Calling it" shows the caller's
  triggers as the template ships them and is owed a follow-up, after this merges.
- Existing games. `copier update` carries the file and the pages to the two rendered from
  the template, `pawdoku` and `tic_tac_toe_beans`. Poodl and the studio carry no
  `.copier-answers.yml`, so no update reaches them: the studio has the gate already, and
  Poodl's `pages.yml` still deploys on push. None is edited from here.
- Seed pages. Decision `0010` describes `BASE_PATH` and the event, not the trigger, and
  `SECURITY.md`'s "a fix lands on `main` and deploys" stays true. `CONVENTIONS.md` §7's
  `pages.yml` block has recorded T03's file, not the current one, since C01.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `template/.github/workflows/pages.yml` | M | the studio's file | Copied: `push` and `workflow_dispatch` replaced by `workflow_run` on `CI`, the `if:` on job `pages`, and the comments saying why |
| `template/docs/how-to/deploy-to-github-pages.md.jinja` | M | T07's page | The opening sentence; "When it deploys", new; the setup paragraph on the two 404s; "Rolling back" |
| `template/docs/reference/quality-gates.md` | M | T08's page | The paragraph on what protection on `main` buys |
| `template/docs/operations/maintenance.md` | M | T08's page | "Deploying" and "Rolling back" |
| `tests/test_render.py` | repo | this repository | `test_pages_deploys_only_what_ci_passed`, `test_pages_names_ci_by_its_name` |
| `CHANGELOG.md` | repo | this repository | Unreleased: a Managed bullet and an Update notes bullet |
| `README.md` | repo | this repository | The `pages.yml` item in what a render carries |
| `tickets/C09-pages-gate.md`, `tickets/README.md` | repo | index | This ticket and its row |

## Steps

1. `cp` the studio's `.github/workflows/pages.yml` over `template/.github/workflows/pages.yml`
   and `diff` the two: nothing may differ.
2. Confirm the gate means what it says for a game. `ci.yml` has one job, `ci`, which calls
   `game-ci.yml`; its `frontend`, `documents` and `stories` jobs carry no `if:` and no
   `continue-on-error`, so CI's conclusion is `success` only when all three passed. CI's
   `cancel-in-progress` on `main` cancels a run a newer push overtakes, which the gate
   skips as it skips a failure.
3. Rewrite every managed page that describes the trigger, and leave the seed pages alone.
4. Add the two render tests. PyYAML reads the bare key `on` as `True`.
5. `CHANGELOG.md` and `README.md`. Stage everything, then `just test` and `just check`.
6. **Authorisation required:** pushing, the pull request, and any tag.

## Acceptance criteria

- [x] The render's `.github/workflows/pages.yml` is byte-identical to the studio's file, but
  for the job's comment, corrected after review of the pull request.
- [x] No managed page says the site deploys on every push to `main`.
- [x] `just test` and `just check` are green, the two new tests included.
- [x] `CHANGELOG.md` carries the Managed bullet and the Update notes bullet.

## Verification

```sh
diff /Users/scutting/projects/biscuit_studio/.github/workflows/pages.yml template/.github/workflows/pages.yml
just render
diff /Users/scutting/projects/biscuit_studio/.github/workflows/pages.yml ai_tmp/render/.github/workflows/pages.yml
just test
just check
```

Since review of the pull request, both `diff`s print one hunk, the job's comment above
`if:`, until the studio takes the same correction.

The gate itself cannot be exercised from here: `workflow_run` fires only from the default
branch's copy of `pages.yml`, so the first proof is a game that merges the update and then
pushes to `main`, and whoever does it reports back on this ticket.

## Hand-back notes

Executed on 2026-09-24 on `fix-template-pages-gate`.

- Release: MINOR. It changes what a managed workflow does in every game, which is not
  prose, and asks nothing of a game beyond resolving markers: no check is renamed and no
  file removed. The C08 pin bump already under Unreleased is MINOR too.
- Both `diff`s against the studio's file print nothing: the template's source and the
  default render's `.github/workflows/pages.yml` are byte-identical to it.
- With every change staged, `just test`: `47 passed, 3 skipped`. `just check`: exit 0, all
  18 hooks Passed ("Lint GitHub Actions workflow files" among them, which covers
  `template/.github/workflows/`), mypy "Success: no issues found in 10 source files", and
  `47 passed, 3 skipped`. The skips are the `full` and network cases.
- `copier update` reaches the two games whose `.copier-answers.yml` names this template,
  read from GitHub on 2026-09-24: `pawdoku` (`_commit: v2.0.0`) and `tic_tac_toe_beans`
  (`_commit: v1.0.0`). Both still carry the ungated `push` and `workflow_dispatch`
  triggers. Poodl and `biscuit_studio` have no answers file, locally or on GitHub, so no
  update reaches them. The studio has the gate already. Poodl's `pages.yml` still deploys
  on push, with its own `base_path: /poodl` and `stage: true`, and needs the gate by hand
  until C07 makes it a render.
- Owed: `biscuit_games_tooling`'s README "Calling it" still shows `push` and
  `workflow_dispatch` for `pages.yml`.
- Not yet confirmed in a real run: nothing here is proved until a game merges the update
  and pushes to `main`.
- After review of the pull request (Codex and Copilot, the same finding): `github.sha` on a
  `workflow_run` event is `main`'s head when the event fired, so the equality is checked
  when CI finishes, not when the deploy starts. A Pages run waiting behind a deployment in
  progress still deploys its own commit after a newer push lands. That commit passed CI,
  and the `pages` group's default `queue: single` cancels an older waiting run when a newer
  one queues, so nothing unvalidated or out of order is published; "still `main`'s head"
  claimed more than that. The job's comment in `pages.yml`, "When it deploys" (a new
  bullet for the waiting run), `quality-gates.md`, the Managed bullet and the Goal now say
  "was `main`'s head when that run finished". No live check of `refs/heads/main` was added:
  it would refuse every re-run of an older Pages run, which is the documented rollback; job
  `pages` calls a reusable workflow, so the check would be a job of its own; and the build
  checks out `github.sha` minutes later, so the race would be shorter, not gone. The
  template's `pages.yml` now differs from the studio's by that comment only.
- Owed: `biscuit_studio`'s `pages.yml` takes the same comment, and the file is byte-identical
  again.
