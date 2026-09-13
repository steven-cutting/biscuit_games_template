---
id: C04
title: A central dependency-update preset for the games, the hub and the template
status: open
depends_on: [C01]
parallel_with: []
branch: ticket/c04-dependency-updates
estimated_size: M
---

# C04: A central dependency-update preset for the games, the hub and the template

## Context

Every Biscuit Games repository pins every dependency exactly and nothing moves the
pins. Poodl's handbook says so in `docs/how-to/maintain-dependencies.md`
(`/Users/scutting/projects/poodl`, lines 11-13: exact versions in `package.json` and
`pyproject.toml`, lockfiles marked `linguist-generated`, "Nothing updates them for
you"), and again at lines 86-87: nothing proposes a bump, there is no Dependabot, and one
would need the registry credential as a stored secret of its own. The same is true of the
hub (`/Users/scutting/projects/biscuit_games`) and will be true of every game the
template renders, because the template ships Poodl's toolchain verbatim
(CONVENTIONS.md §4).

Four ecosystems are pinned in four different ways, and each needs a different updater:

- npm packages, exact versions in `package.json` with `package-lock.json` (the hub
  package `@steven-cutting/biscuit-games` comes from GitHub Packages, which
  authenticates every read; the committed `.npmrc` names only the registry for the
  `@steven-cutting` scope).
- Python tools, exact versions in `pyproject.toml` `[dependency-groups]` (Poodl's
  `pyproject.toml` lines 8-11: `prek==0.4.12`, `ruff==0.16.2`) with `uv.lock`.
- GitHub Actions, pinned by commit SHA with a version comment (Poodl's
  `.github/workflows/ci.yml` line 27: `actions/checkout@3d3c42e5...` followed by
  `# v7.0.1`), and prek hooks pinned the same way (`.pre-commit-config.yaml` line 99:
  `rev: 675b1261...` followed by `# v3.11.1`).
- The Allium binary, pinned by version and four checksums in
  `scripts/install_allium.py` (the hub's copy, which the template ships: `VERSION` at
  line 29, `CHECKSUMS` at lines 46-50), which no updater can recompute.

The set of repositories is now Poodl, the hub, the template and each new game, so a
per-repository configuration is the wrong unit. This ticket is a recommendation
(CONVENTIONS.md §1, decision 3): it is picked up on its own, after C01 has decided
where shared tooling lives, and every step that installs an app, stores a secret or opens
a pull request in another repository is separately authorised (CONVENTIONS.md §11).

One thing an updater changes that is not a pin: it becomes the first author of a branch
in these repositories who is not a person with write access. `chromatic.yml` decides
whose code may run beside the Chromatic token by asking whether the head is a fork
(Poodl's file, lines 129-135) — a question an updater's in-repo branch passes while
carrying code nobody wrote. Step 5 closes that before the first bump PR is opened, and
the Goal below counts it as part of shipping the updater.

Read first: CONVENTIONS.md §0, §4, §9 (the template repository's own pins), §11, §12
(the Renovate and Dependabot item), §13; Poodl's `docs/how-to/maintain-dependencies.md`
in full; the hub's `scripts/install_allium.py` lines 1-60.

## Goal

One updater configuration, kept centrally, that every repository consumes with a
one-line file, proposing pull requests that move an npm pin, a uv pin, an action SHA
with its comment, and a hook rev, and that pass each repository's own gate. The
recommendation is Renovate with a shared preset; Dependabot is the fallback if the Mend
app is not wanted. The choice is made with evidence, recorded in the ticket's hand-back
notes, and shipped as one managed file in the template.

Shipping it includes the `/chromatic` question step 5 settles: no bump pull request is
opened until an updater's in-repo branch is either refused by `authorize` or ruled out by
the managed dependency page.

## Non-goals

- Changing any pin by hand, or bumping the hub package in any game (that is a game's
  own decision, taken with the hub's `CHANGELOG.md` in hand).
- Automating the Allium checksums. The updater may flag that `VERSION` lags upstream;
  a human recomputes the four checksums, as `install_allium.py`'s comment at lines
  44-45 requires.
- Hosting the preset: C01 decides the host (`steven-cutting/biscuit_games_tooling` or a
  repository of its own); this ticket puts the preset wherever C01 chose.
- Reusable workflows (C01), the validators package (C02), repository settings (C03).

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `biscuit_games_tooling: renovate/default.json` (or `renovate-config: default.json`) | repo | new | The shared preset, per Steps 3 |
| `template/renovate.json` | M | new | `{"extends": ["github>steven-cutting/biscuit_games_tooling//renovate/default"]}` (path per the host chosen in C01) |
| `tests/inventory.py` | repo | T10's file | Add `renovate.json` to `MANAGED` |
| `CHANGELOG.md` | repo | T12's file | Unreleased, under Managed: the new file; MINOR release (CONVENTIONS.md §10) |
| `template/docs/how-to/maintain-dependencies.md` | M | T07's page | Drop the "no Dependabot" sentence; add "What the updater proposes and what stays manual" |
| `poodl: renovate.json` | other repo | new | Same one-line file, in a pull request |
| `biscuit_games: renovate.json` | other repo | new | Same one-line file, in a pull request |
| `template/.github/workflows/chromatic.yml` | M | T03's file | Step 5, guard branch only: one more `deny` in `authorize` for a bot-authored head |
| `poodl: .github/workflows/chromatic.yml` | other repo | its own file | Step 5, guard branch only: the same `deny`, in the step 7 pull request |
| `biscuit_games: .github/workflows/chromatic.yml` | other repo | its own file | Step 5, guard branch only: the same `deny`, in the step 7 pull request |
| `tickets/CONVENTIONS.md` | repo | §7 | Step 5, guard branch only: the `chromatic.yml` paragraph gains the guard |

## Steps

1. **Verify the capabilities the recommendation rests on** (CONVENTIONS.md §12). Read
   the current Renovate documentation and confirm, recording each answer in the
   hand-back notes: (a) `hostRules` can carry a token for `npm.pkg.github.com` so the
   hub package is resolvable; (b) the `pep621` manager updates `pyproject.toml` pins
   and refreshes `uv.lock` (the `lockFileMaintenance` and `postUpdateOptions` uv
   support); (c) `helpers:pinGitHubActionDigests` keeps the `# vX.Y.Z` comment beside
   the SHA in the form Poodl's workflows use; (d) the `pre-commit` manager updates
   `rev:` SHAs in `.pre-commit-config.yaml` and `.pre-commit-fix.yaml` (it is disabled
   by default and must be enabled); (e) a custom regex manager can match `VERSION =
   "3.6.1"` in `scripts/install_allium.py` against the upstream release list. Then read
   the Dependabot documentation and confirm what it cannot do: shared presets across
   repositories, uv lockfile refresh, and SHA-with-comment action pins.
2. **Decide.** Renovate if (a) to (d) hold; Dependabot only if the Mend app is not
   wanted, in which case each repository carries its own `.github/dependabot.yml` with a
   `registries` entry for the hub package and a per-repository `dependabot` secret, and
   the rest of this ticket is adapted to that shape. **Authorisation required:**
   installing the Renovate app on the `steven-cutting` account, and storing the
   `read:packages` token it needs as the app's secret.
3. **Write the preset** at the host C01 chose. Content:

   ```json
   {
     "$schema": "https://docs.renovatebot.com/renovate-schema.json",
     "extends": ["config:recommended", "helpers:pinGitHubActionDigests"],
     "rangeStrategy": "pin",
     "lockFileMaintenance": { "enabled": true, "schedule": ["before 6am on monday"] },
     "pre-commit": { "enabled": true },
     "packageRules": [
       { "groupName": "storybook", "matchPackageNames": ["/^@storybook//", "/^storybook$/"] },
       { "groupName": "vitest", "matchPackageNames": ["/^vitest$/", "/^@vitest//"] },
       { "groupName": "eslint", "matchPackageNames": ["/eslint/"] },
       { "matchPackageNames": ["@steven-cutting/biscuit-games"], "dependencyDashboardApproval": true }
     ],
     "hostRules": [
       { "matchHost": "npm.pkg.github.com", "hostType": "npm", "token": "{{ secrets.GITHUB_PACKAGES_READ_TOKEN }}" }
     ],
     "customManagers": [
       {
         "customType": "regex",
         "managerFilePatterns": ["/^scripts/install_allium\\.py$/"],
         "matchStrings": ["VERSION = \"(?<currentValue>[0-9.]+)\""],
         "depNameTemplate": "allium",
         "datasourceTemplate": "github-releases",
         "packageNameTemplate": "<the allium release repository named in install_allium.py>"
       }
     ]
   }
   ```

   Adjust every key to what step 1 found (the regex manager's field names change
   between Renovate versions; the `packageNameTemplate` is read from the download URL
   in `install_allium.py`). The hub-package rule asks for dashboard approval so a hub
   release is taken deliberately, with its `CHANGELOG.md` read, rather than merged by
   habit. Renovate's `{{ secrets.* }}` placeholder is Renovate's own syntax and never
   reaches a Jinja renderer: the preset lives outside `template/`.
4. **Add the managed file to the template.** `template/renovate.json` holding only the
   `extends` line; add `"renovate.json"` to `MANAGED` in `tests/inventory.py`; run
   `just test` (the inventory test now expects the path). This is a new managed file:
   record it under Managed in the Unreleased section of the template `CHANGELOG.md` and
   note that the next release is MINOR (CONVENTIONS.md §10).
5. **Close the `/chromatic` path this ticket opens.** Until now nothing proposed a bump
   (the fact at the top of Context), so every branch in these repositories was pushed by
   someone with write access and `chromatic.yml`'s fork check was the whole of "whose
   code runs". An updater's pull request is a branch **in the base repository**: it
   passes that check, and `/chromatic` on it checks out the head and runs `just sync`
   — `npm ci --no-audit`, no `--ignore-scripts` — before the publish step that carries
   `CHROMATIC_PROJECT_TOKEN`. A maintainer typing the word on a bump PR would therefore
   run the newly proposed dependency's install scripts beside the token, which is the one
   case the workflow's own reasoning does not cover. Settle it one of two ways and record
   which, with the reason, in the hand-back notes:

   1. **A guard in `authorize`** (preferred). One more `deny` in the gate step of
      `chromatic.yml`, beside the fork check and before the reaction: refuse a head whose
      pull request was opened by a bot (`gh pr view --json author` reports
      `author.is_bot`) or whose branch carries the updater's prefix. It costs visual
      review on bump PRs, which is exactly the case it exists for; a maintainer who wants
      one pushes the branch on by hand under their own name. This edits the workflow in
      three places — `template/.github/workflows/chromatic.yml` here, and Poodl's and the
      hub's in the pull requests step 7 already opens — and `tickets/CONVENTIONS.md` §7's
      `chromatic.yml` paragraph, which is the living description of that file. Files
      touched carries all four rows, marked for this branch only. T03 is `done` by then:
      its composition and
      diff signatures are a record of how the file was first built, not a thing to edit.
      `test_verbatim_files_are_byte_identical` compares `template/` to its own render and
      is unaffected by diverging from Poodl.
   2. **A stated rule** in `template/docs/how-to/maintain-dependencies.md`, the page step
      6 rewrites anyway: `/chromatic` is not typed on an updater's branch until its diff
      has been read. Cheaper, and it relies on a person remembering.

   Take (2) only if (1) proves awkward against the updater actually chosen — a bot whose
   pull requests report no `author.is_bot`, or branch names the guard cannot match.
6. **Update the managed page.** In `template/docs/how-to/maintain-dependencies.md`
   remove the sentence that says there is no Dependabot and add a section
   `## What the updater proposes and what stays manual`: the four ecosystems it moves,
   the hub package (proposed, approved by hand from the dashboard), and the two things
   that stay manual: the Allium checksums, and any pin whose bump the game's gate
   rejects. Run `just test` and, in a render, `just check-docs`.
7. **Consume it in Poodl and the hub.** **Authorisation required:** one pull request in
   each repository adding `renovate.json`; each PR must pass that repository's own
   required checks before merge.
8. **Prove it** on the template repository first: wait for the dependency dashboard
   issue to list the four ecosystems, take one PR per ecosystem through `fast` and
   `full`, and record the outcomes.

## Acceptance criteria

- [ ] The choice (Renovate or Dependabot) is recorded with the step 1 evidence.
- [ ] The preset exists at the host C01 chose and validates against Renovate's schema
      (`npx --yes renovate-config-validator` or the equivalent for the chosen tool).
- [ ] `template/renovate.json` renders, is listed in `tests/inventory.py`, and
      `just test` is green.
- [ ] A preset-driven PR in the template moved one npm pin, one uv pin, one action SHA
      with its comment and one hook rev, and passed `fast` and `full`.
- [ ] A PR in Poodl proposed `@steven-cutting/biscuit-games` when the hub tagged a
      release, proving the registry host rule.
- [ ] `template/docs/how-to/maintain-dependencies.md` no longer says there is no
      updater, and `just check-docs` passes in a render.
- [ ] The `/chromatic` path is closed: either `authorize` refuses a bot-authored head in
      all three repositories' `chromatic.yml` (and CONVENTIONS.md §7 describes it), or
      the managed dependency page states the rule. Which, and why, is in the hand-back
      notes. Proof for the guard: `/chromatic` on an updater's pull request prints the
      refusal notice, leaves the run green, and publishes nothing.
- [ ] The Allium checksums were never touched by an automated PR.

## Verification

From the template repository root:

```sh
just test
npx --yes renovate-config-validator template/renovate.json
```

Expected: the fast suite green with `renovate.json` in the inventory; the validator
reports no errors.

In a render:

```sh
just render ai_tmp/render && cd ai_tmp/render && git init -q -b main && just initialize && just check-docs
```

Expected: `check-docs` green with the rewritten page.

On GitHub, after the app is installed and the preset consumed:

```sh
gh issue list -R steven-cutting/biscuit_games_template --search "Dependency Dashboard" --json title,url
gh pr list -R steven-cutting/biscuit_games_template --author app/renovate --json number,title,statusCheckRollup
```

Expected: one dashboard issue listing npm, uv, GitHub Actions and pre-commit; PRs whose
`fast` and `full` checks are green.

## Hand-back notes

Filled in by the agent that executes this ticket.

- Which updater was chosen, and the step 1 evidence for each of (a) to (e).
- How step 5 was settled: the guard or the stated rule, with the reason, and — for the
  guard — the three workflow diffs and the CONVENTIONS.md §7 wording as merged.
- The exact preset as merged, and the host path the one-line file extends.
- The four proving PRs (one per ecosystem) and their check outcomes.
- What was handed back: to C01 if the host was not yet decided; to T12 if the template
  README's maintenance section needs the updater named.
- Which open points were settled.

## Open points

- Every Renovate and Dependabot capability listed in step 1 is CONVENTIONS.md §12's
  unverified item for this ticket; each is checked against the current documentation
  before the choice is made.
- Whether the Renovate app needs the `read:packages` token as an app secret or as a
  repository secret per consumer; check the app's host-rule documentation.
- Whether the chosen updater opens its pull requests from branches in the base
  repository. Renovate and Dependabot both do, which is what makes step 5 necessary; an
  updater working from a fork would be refused by `chromatic.yml`'s existing fork check
  and would need no guard. Check: the first proving PR's
  `gh pr view --json isCrossRepository,headRefName,author`.
- Whether `lockFileMaintenance` refreshes `uv.lock` without a pin change, or whether a
  separate `uv lock --upgrade` PR is needed; check with one weekly run.
- Whether the hub-package rule should also apply in the template (its pin is a template
  release, CONVENTIONS.md §3: `hub_package_version` moves only with a template release,
  and `test_pins_agree` holds `package.json.jinja` equal to it, so a bot PR that moves
  only one of the two fails `just test`); the likely answer is to exclude the hub package
  from the template's updates and bump it by hand with the CHANGELOG entry.
