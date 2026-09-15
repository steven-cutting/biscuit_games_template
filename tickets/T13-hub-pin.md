---
id: T13
title: "Hub pin: move hub_package_version to 1.1.0, so a render passes its own gate"
status: done
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

### Outcome

- Carried out on `T10-harness-completion`, the branch of the template's pull request 12,
  at the maintainer's direction (Deviations).
- The pin reads `1.1.0` in `copier.yml`, `template/package.json.jinja`,
  `tests/test_render.py` and CONVENTIONS.md §3. §0's H row names `v1.1.0` and its
  commit, and `CHANGELOG.md` carries the Managed bullet.
- `just check` is green: 44 passed, 4 skipped.
- `just test-full` is green, and `test_render_passes_its_own_gate` passed. The render's
  whole gate ran for the first time: `just initialize`, all eleven recipes, then
  `check-clean`.
- On pull request 12, CI run `34931522393` on `32ca849` passed both jobs:
  - `fast` in 1m18s, with pytest reporting `46 passed, 2 skipped in 10.29s`.
  - `full` in 3m00s, with the `just test-full` step's pytest reporting
    `47 passed, 1 skipped in 156.89s (0:02:36)`. The one skip is
    `test_update.py`'s latest-tag case, so `test_render_passes_its_own_gate` passed.
- No tag was created and no repository setting was changed.

### What was verified, and how

Step 1, before any edit:

```text
$ grep -c '^//npm.pkg.github.com/:_authToken=' ~/.npmrc
1
$ npm view @steven-cutting/biscuit-games versions dist-tags time --registry=https://npm.pkg.github.com --json
[...] "versions": ["1.0.0", "1.1.0"], "dist-tags": {"latest": "1.1.0"} [...] "1.1.0": "2026-09-15T04:55:28Z"
$ npm pack @steven-cutting/biscuit-games@1.1.0 --registry=https://npm.pkg.github.com --pack-destination ai_tmp/hub-1.1.0
[...]
steven-cutting-biscuit-games-1.1.0.tgz
$ tar -xOzf ai_tmp/hub-1.1.0/steven-cutting-biscuit-games-1.1.0.tgz package/dist/components/Wordmark.svelte | grep -c product
3
$ git ls-remote --tags https://github.com/steven-cutting/biscuit_games.git
dfebaf41b101c36a134a1373ac82e1944bbd324a refs/tags/v1.0.0
2a51533a61d79df0b627ebdc510536333d01d89f refs/tags/v1.1.0
ca0ca0a0e88795c737c04e0eb74fce91b870dcd2 refs/tags/v1.1.0^{}
```

`3` is the count T05 printed for its package built from hub `main`. The hub's Release
run on `v1.1.0` is `34930610026`, which succeeded. Comparing `09b4894a...ca0ca0a` on
GitHub lists two commits: `cda64f9` ("Cut 1.1.0, so a game can name itself in the
Wordmark") and the merge `ca0ca0a`. They touch five files: `CHANGELOG.md`,
`docs/how-to/consume-the-hub.md`, `docs/operations/poodl-handover.md`, `package.json` and
`package-lock.json`.

Step 2's starting point, on the branch at `341c303`: `git grep -n '1\.0\.0' -- copier.yml
template tests` printed `copier.yml:283`, `template/package.json.jinja:34` and
`tests/test_render.py:259`. `just check` printed `44 passed, 4 skipped in 47.10s`.

Steps 3 to 5. The edits were applied, and then the three commands ran as one chain on the
uncommitted tree, logged to `ai_tmp/`:

```text
$ git grep -n '1\.0\.0' -- copier.yml template tests
[nothing; exit 1]
$ just test tests/test_render.py
[...] 23 passed, 16 warnings in 12.90s [...]
$ just check
[every hook line ending Passed; mypy: Success: no issues found in 10 source files]
[...] 44 passed, 4 skipped, 31 warnings in 45.28s [...]
$ just test-full -v -s --durations=5
tests/test_full.py::test_render_passes_its_own_gate sh scripts/initialize.sh
[...]
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
[...]
Storybook build completed successfully
==> just storybook-test
 Test Files  1 passed (1)
      Tests  3 passed (3)
==> just check-docs
==> just check-agents
==> just check-specs
==> just analyse-specs
allium analyse: 1 specifications, no diagnostics and no findings.
==> just check-clean
The worktree matches the check baseline.

All checks passed and the worktree is unchanged.
PASSED
[...]
45.37s call     tests/test_full.py::test_render_passes_its_own_gate
11.19s call     tests/test_update.py::test_update_keeps_game_work
11.02s call     tests/test_update.py::test_pristine_update_equals_fresh_render[HEAD~2]
2.28s call     tests/test_questionnaire.py::test_computed_defaults
2.27s call     tests/test_render.py::test_markdown_punctuation_inside_an_answer_is_accepted
SKIPPED [1] tests/test_update.py:84: no v* tag yet; T11 makes the first
[...] 47 passed, 1 skipped, 31 warnings in 92.54s (0:01:32) [...]
```

The chain's own timer put `just test-full` at 93 s on a warm machine, where Chromium and
allium were already downloaded.

After the edits, `git status --porcelain` printed exactly the five paths in Files touched.

### Deviations, and why

- **Branch.** The hub published `1.1.0` while pull request 12 was still open, and the
  maintainer asked for the failing `full` job to be tried again on that branch. So this
  ticket was carried out on `T10-harness-completion`, not on `ticket/t13-hub-pin` from
  `main`. Step 2's worktree was never created, and its baseline is that branch at
  `341c303`.
- **Uncommitted run.** Steps 4 and 5 ran before the commit, so copier raised its
  `DirtyLocalWarning`. The rendered bytes are the committed ones.
- **§0's wording.** The H row says `v1.1.0` sits "two commits after `09b4894a` at
  `ca0ca0a`" and differs from it "only in the release cut". The comparison above is the
  evidence for both claims.

### Handed back

- **T11.** Its step 2 needs a render whose `just check` is green, and one now is. T11
  still starts from `main` after pull request 12 merges.
- **Noise, not a defect.** `storybook-build` prints Node's `DEP0205` deprecation warning
  for `module.register()`, and Vite's advice to adjust `build.chunkSizeWarningLimit`.
  Neither fails the recipe.

### Open points settled

1. **`storybook-build` and the final worktree check: hold.** Both passed in step 5
   ("Storybook build completed successfully" and "The worktree matches the check
   baseline.").
2. **What else `1.1.0` carries: nothing that changes a render.** The published tree
   differs from the hub `main` T05 built only in the release cut. Step 5's
   `frontend-coverage` ran 30 tests, `tests/platformSpecs.test.ts` among them, and all
   30 passed.

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
