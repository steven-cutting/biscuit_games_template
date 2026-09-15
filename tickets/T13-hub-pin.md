---
id: T13
title: "Hub pin: move hub_package_version to 1.1.0, so a render passes its own gate"
status: open
depends_on: [T10]
parallel_with: []
branch: ticket/t13-hub-pin
estimated_size: S
---

# T13: Hub pin: move `hub_package_version` to 1.1.0, so a render passes its own gate

## Context

Every render of this template fails its own gate at the same line, and has done since
T00:

```text
src/lib/components/Lockup.svelte:20:11
Error: Type 'string' is not assignable to type 'never'. (ts)
<Wordmark product={GAME_NAME} />
```

`Lockup.svelte` (CONVENTIONS.md §7) passes the game's name to the platform's `Wordmark`
through its `product` prop. `product` arrived in hub commit `41c430b`, after the tag
`v1.0.0` (`dfebaf4`). When this ticket was written, the only published version of
`@steven-cutting/biscuit-games` was `1.0.0`, whose `Wordmark` takes no props, and
`copier.yml` pins every render to it.

T00, T01 and T05 each handed this back. T05 built a package from hub `main` and ran the
render against it, changing no template file. `frontend-static`, `frontend-unit`,
`frontend-coverage`, `frontend-build` and `storybook-test` all exited 0. T10 added
`tests/test_full.py` and the `full` CI job, and recorded that the job's first runs
failed on this error alone (its open point 5).

The remedy those notes name has two halves:

- **The hub releases `1.1.0`.** This work is in `steven-cutting/biscuit_games`, done by
  the maintainer outside this repository. The level is Minor: components and an optional
  prop are added and nothing is removed. The hub's `docs/operations/poodl-handover.md`
  argues the level.
- **This ticket moves the template's pin to that release.** The pin lives in
  `copier.yml`, which CONVENTIONS.md §11 says no lane touches. So this ticket is the
  "T00 follow-up on `main`" that §11 calls for.

Position: after T10 has merged and after the hub has published `1.1.0`. T11 waits for
this ticket, because its step 2 needs a render whose `just check` is green.

The pin bump alone cannot prove the whole gate green in advance. The render's gate runs
eleven recipes (`template/scripts/run_project_check.py` lines 18-30), then checks that
the worktree is unchanged. What is already known about each:

- `lock-check` and `lint` already pass in CI.
- `frontend-static`, `frontend-coverage`, `frontend-build` and `storybook-test` passed
  in T05's run against hub `main`.
- `check-docs`, `check-agents`, `check-specs` and `analyse-specs` run the same commands
  as hooks the render's `lint` already passed. Compare `template/Justfile` lines 118-143
  with `template/.pre-commit-config.yaml`.
- `storybook-build` has never run in a render, and neither has the final worktree check.
  This ticket's `just test-full` is their first run.

Read first, in this order:

- CONVENTIONS.md:
  - §0, the H row
  - §3, `hub_package_version`
  - §10, where a pin bump is Minor
  - §11, the files no lane touches and the separately authorised actions
- `tickets/T05-source-skeleton.md` hand-back notes: "Which CONVENTIONS.md §7 files
  changed" and the hub-HEAD run just above it.
- `tickets/T10-harness-completion.md` hand-back notes: open points 5 and 6.
- In this repository:
  - `copier.yml` (`hub_package_version`)
  - `template/package.json.jinja` (the dependency line)
  - `tests/test_render.py` (`test_pins_agree`)
  - `.github/workflows/ci.yml` (the `full` job)
  - `CHANGELOG.md`

## Goal

- `@steven-cutting/biscuit-games` is pinned at `1.1.0` everywhere the template writes the
  pin:
  - `copier.yml`
  - `template/package.json.jinja`
  - the assertion in `tests/test_render.py`
  - the §3 copy in CONVENTIONS.md
- `just test-full` is green locally:
  `tests/test_full.py::test_render_passes_its_own_gate` passes, and the render prints
  `All checks passed and the worktree is unchanged.`
- `CHANGELOG.md` records the bump under Managed.
- The `full` job passes on this ticket's pull request.

## Non-goals

- Anything in the hub. The maintainer cuts the release there. If `1.1.0` is not
  published, this ticket stops at step 1.
- Any other change under `template/`:
  - `Lockup.svelte`, its test and its story stay as T05 wrote them.
  - No `xfail`, `skip` or `continue-on-error` stands in for a green gate.
- Fixing a failure the gate reports past `frontend-static`:
  - Diagnose it to a rendered path and its owning lane (CONVENTIONS.md §4).
  - Record it in the hand-back notes, then stop.
  - The fix lands on `main` through that lane or a follow-up.
- Tags and repository settings. `full` stays a non-required check (C03), and `v0.1.0`
  is T11's.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `copier.yml` | repo | CONVENTIONS.md §3 | `hub_package_version` default `1.0.0` → `1.1.0`. |
| `template/package.json.jinja` | M† | CONVENTIONS.md §3; §9 `test_pins_agree` | `"@steven-cutting/biscuit-games": "1.1.0"`. |
| `tests/test_render.py` | repo | T00's `test_pins_agree` | `assert hub_version == "1.1.0"`. |
| `tickets/CONVENTIONS.md` | repo | §0, §3 | §3's copy of `hub_package_version` reads `1.1.0`; §0's H row names the tag `v1.1.0` and the commit it tags. |
| `CHANGELOG.md` | repo | Keep a Changelog; CONVENTIONS.md §10 | One bullet under `[Unreleased]` → `### Managed` (step 3). |

Plus the `status:` line and the hand-back notes of this file.

## Steps

1. Before creating anything, confirm the release exists and carries `product`:

   ```sh
   grep -c '^//npm.pkg.github.com/:_authToken=' ~/.npmrc
   npm view @steven-cutting/biscuit-games versions --registry=https://npm.pkg.github.com
   mkdir -p ai_tmp/hub-1.1.0
   npm pack @steven-cutting/biscuit-games@1.1.0 --registry=https://npm.pkg.github.com --pack-destination ai_tmp/hub-1.1.0
   tar -xOzf ai_tmp/hub-1.1.0/steven-cutting-biscuit-games-1.1.0.tgz package/dist/components/Wordmark.svelte | grep -c product
   ```

   Expected:
   - The first `grep` prints `1`.
   - The version list includes `1.1.0`.
   - The last `grep` prints at least `1`.

   If `1.1.0` is missing, stop: the hub has not released. If the hub released under
   another number, use that number everywhere below and say so in the hand-back notes.

2. Create the worktree from `main` after T10 has merged (README.md, "How to pick up a
   ticket"). Then confirm the starting point:

   ```sh
   git log --oneline -1 origin/main
   just sync && just check
   git grep -n '1\.0\.0' -- copier.yml template tests
   ```

   Expected: `just check` is green, and `git grep` prints exactly three lines:
   `copier.yml:283`, `template/package.json.jinja:34` and `tests/test_render.py:259`.

3. Make the edits in the Files touched table:
   - `copier.yml`: `default: 1.1.0` under `hub_package_version`.
   - `template/package.json.jinja`: `"@steven-cutting/biscuit-games": "1.1.0",`.
   - `tests/test_render.py`: `assert hub_version == "1.1.0"`.
   - `tickets/CONVENTIONS.md`:
     - In §3's copy of `copier.yml`, set `default: 1.1.0`.
     - In §0's H row, after the sentence about the tag `v1.0.0`, name the tag `v1.1.0`
       and its commit. The commit is the line ending `^{}` in
       `git ls-remote --tags https://github.com/steven-cutting/biscuit_games.git v1.1.0`.
   - `CHANGELOG.md`, under `[Unreleased]` → `### Managed`, append:

     ```markdown
     - `package.json` pins `@steven-cutting/biscuit-games` at `1.1.0`, the first release
       whose `Wordmark` takes `product`. Before it, every render's `svelte-check` failed
       at `src/lib/components/Lockup.svelte`, and the lockup read "biscuit games" without
       the game's name.
     ```

4. Run the focused check, then the broad one:

   ```sh
   just test tests/test_render.py
   just check
   ```

   Expected: `test_pins_agree` passes and `just check` is green.

5. Run the whole gate in a render:

   ```sh
   just test-full -v -s --durations=5
   ```

   Expected: `tests/test_full.py::test_render_passes_its_own_gate PASSED`, the render's
   line `All checks passed and the worktree is unchanged.`, and a green run. Quote the
   elapsed time and the durations. If a recipe fails, follow Non-goals: record the
   failure and stop.

6. Set `status: done`, fill in the hand-back notes, and commit on the ticket branch.
   **Authorisation required** (CONVENTIONS.md §11): pushing the branch, and opening the
   pull request. Once both are authorised and done, record the pull request's `fast` and
   `full` results. That `full` run is the first CI run of a render's whole gate.

## Acceptance criteria

- [ ] Step 1 showed `1.1.0` published, with its `Wordmark` carrying `product`.
- [ ] `git grep -n '1\.0\.0' -- copier.yml template tests` prints nothing.
- [ ] `just check` is green on the ticket branch.
- [ ] Under `just test-full`, `test_render_passes_its_own_gate` passed and the whole run
      is green.
- [ ] The pull request's `full` job passed, or the hand-back notes say the push was not
      authorised.
- [ ] `CHANGELOG.md` carries the Managed bullet from step 3.
- [ ] Nothing outside the Files touched table changed, other than this ticket's
      `status:` line and hand-back notes.
- [ ] No tag was created and no repository setting was changed.

## Verification

```sh
git grep -n '1\.0\.0' -- copier.yml template tests
git grep -n '1\.1\.0' -- copier.yml template/package.json.jinja tests tickets/CONVENTIONS.md
just check
just test-full -v -s --durations=5
git status --porcelain
git tag --list 'v*'
```

Expected:

- The first `git grep` prints nothing.
- The second prints the lines in `copier.yml`, `template/package.json.jinja` and
  `tests/test_render.py`, and at least the §3 line of CONVENTIONS.md.
- `just check` is green.
- `test_render_passes_its_own_gate PASSED`, with the render's closing line.
- `git status --porcelain` prints nothing after the commit.
- No tag.

## Hand-back notes

Filled in by the agent that executes this ticket.

- The published versions and the `grep -c product` count from step 1, and the hub
  commit written into §0.
- The tails of `just check` and `just test-full`, with the elapsed time and the five
  slowest durations.
- Whether each recipe of the render's gate passed. For any that failed: the rendered
  path, its owning lane, the output and the proposed fix.
- The pull request's `fast` and `full` results, if the push was authorised.
- What deviated from the ticket, and why.

## Open points

1. `storybook-build` and the render gate's final worktree check have never run in a
   render (see Context).
   - Check: step 5.
   - Expected: both pass. A failure is handed back, as Non-goals says.
2. `1.1.0` carries more than `product`:
   - ten components
   - `Monogram`, extracted from `Wordmark`
   - new clauses in the specification modules the package ships, which the render's
     `tests/platformSpecs.test.ts` resolves from `node_modules`

   Check: step 5's `frontend-coverage`, which runs that file. T05's run against a
   package built from hub `main` passed its ten cases. A failure here means the
   published tree differs from what T05 built.
