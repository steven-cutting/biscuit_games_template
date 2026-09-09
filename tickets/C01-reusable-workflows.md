---
id: C01
title: Reusable workflows and a composite toolchain action for every game
status: open
depends_on: [C03]
parallel_with: []
branch: ticket/c01-reusable-workflows
estimated_size: L
---

# C01: Reusable workflows and a composite toolchain action for every game

## Context

Every Biscuit Games repository carries three workflows, and every job in them repeats
the same setup block: checkout, `setup-node` with the GitHub Packages registry and the
`@steven-cutting` scope, `setup-uv` 0.11.18, `uv python install 3.14`,
`uv tool install rust-just==1.51.0`, `npm install --global npm@11.17.0`, then
`just sync` with `NODE_AUTH_TOKEN` on that one step. In Poodl (P =
`/Users/scutting/projects/poodl` at `0a46a485`) the block appears three times in
`.github/workflows/ci.yml` (lines 27-57, 70-103, 123-161), once in
`.github/workflows/chromatic.yml` (180-220) and, without uv and just, once in
`.github/workflows/pages.yml` (41-63). The hub (H =
`/Users/scutting/projects/biscuit_games` at `09b4894a`) repeats it in its own
`ci.yml`, `chromatic.yml` and `release.yml`.

Ticket T03 ships Poodl's three files into the template as managed, verbatim `.yml`
files (CONVENTIONS.md §4, §6 rule 2, §7), so every rendered game holds a fourth copy.
A fix to the setup block then reaches games only through `copier update`, as a
three-way merge in each game, and a toolchain bump is a template release. This ticket
recommends moving the jobs into reusable `workflow_call` workflows and the setup block
into a composite action, both hosted in one new repository, so a game keeps only three
thin callers.

Why a new repository rather than the template or the hub: GitHub runs a reusable
workflow only from `.github/workflows/` at the root of its hosting repository, and the
template's tree lives under `template/` (`_subdirectory: template`, CONVENTIONS.md §3),
so the template cannot host one; a composite action can live at any path
(`uses: owner/repo/path@sha`), but a workflow cannot. The hub declares in
`H/AGENTS.md:171-173` that "It has two artefacts and no more: the
`@steven-cutting/biscuit-games` package ... and the component workshop", and its
`H/.github/workflows/ci.yml:11-12` grants `contents: read` only, with no
`packages: read`, because the hub does not consume the package. A third artefact that
consumes the package does not belong there.

Where this sits: it is a recommendation, outside the build order T00 to T12. Pick it up
after T11 has tagged `v0.1.0` (so a rendered game exists to test against) and after C03
has merged, because C03's `scripts/bootstrap_repo.sh` encodes the required-check
contexts this ticket renames. C02 and C04 wait for this ticket's host decision. Read
first: `P/.github/workflows/ci.yml`, `P/.github/workflows/chromatic.yml`,
`P/.github/workflows/pages.yml`, `H/.github/workflows/chromatic.yml` (lines 201-217 and
230-265, the token guard the template's copy already carries), `P/Justfile` (the
recipes the jobs call), `P/.pre-commit-config.yaml` (hook revisions), the template's
`template/.github/workflows/` as T03 left it, and CONVENTIONS.md §7, §9, §10 and §11.

## Goal

- A public repository `steven-cutting/biscuit_games_tooling` hosting
  `.github/workflows/game-ci.yml`, `.github/workflows/game-chromatic.yml` and
  `.github/workflows/game-pages.yml` (all `on: workflow_call`) and
  `actions/setup-toolchain/action.yml` (composite; inputs default to node 26, npm
  11.17.0, uv 0.11.18, Python 3.14, just 1.51.0 and the `@steven-cutting` scope; every
  `uses:` pinned by SHA), with its own `just check` and actionlint gate.
- The template's three managed workflows become thin callers, still verbatim `.yml`,
  with the same triggers, the same workflow-level `permissions` blocks, the same
  `concurrency` groups and the same effective per-job token scopes as today.
- Required-check contexts change from `frontend`, `documents`, `stories` to
  `ci / frontend`, `ci / documents`, `ci / stories`; C03's bootstrap script and every
  protected branch move in the same change.
- Poodl adopts the three callers through a separately authorised pull request.

## Non-goals

- Packaging the Python validators and installers as a dependency: C02 (it may share
  this repository, and waits for this ticket's host decision).
- A dependency-update preset that bumps the pinned SHAs: C04.
- Changing what the jobs run. Every job runs the same `just` recipes in the same order
  as today; a recipe change belongs to the template's workflows, not to this ticket.
- The hub's own three workflows and the template repository's own `ci.yml` (`fast` and
  `full`, CONVENTIONS.md §9), which run no game recipes and stay as they are.
- Poodl's other template drift, `.copier-answers.yml` and whether Poodl keeps its own
  `pages.yml`: C07.

## Files touched

| Repository | Path | Class | Source | Change |
| --- | --- | --- | --- | --- |
| `biscuit_games_tooling` (new) | `.github/workflows/game-ci.yml` | repo | P `ci.yml` jobs | New; `workflow_call`, three jobs |
| `biscuit_games_tooling` (new) | `.github/workflows/game-chromatic.yml` | repo | template `chromatic.yml` jobs | New; `workflow_call`, optional secret |
| `biscuit_games_tooling` (new) | `.github/workflows/game-pages.yml` | repo | template `pages.yml` jobs | New; `workflow_call`, `base_path` input |
| `biscuit_games_tooling` (new) | `actions/setup-toolchain/action.yml` | repo | P `ci.yml:30-51` | New; composite action, exact below |
| `biscuit_games_tooling` (new) | `.github/workflows/ci.yml` | repo | this ticket | New; the repository's own gate |
| `biscuit_games_tooling` (new) | `.pre-commit-config.yaml` | repo | P `.pre-commit-config.yaml` | New; reduced gate |
| `biscuit_games_tooling` (new) | `Justfile` | repo | CONVENTIONS.md §9 | New; six recipes |
| `biscuit_games_tooling` (new) | `pyproject.toml` | repo | this ticket | New; `prek` only |
| `biscuit_games_tooling` (new) | `uv.lock` | repo | `uv lock` | New; committed |
| `biscuit_games_tooling` (new) | `.python-version` | repo | P | New; `3.14` |
| `biscuit_games_tooling` (new) | `.gitignore` | repo | this ticket | New |
| `biscuit_games_tooling` (new) | `README.md` | repo | this ticket | New; callers, version policy |
| `biscuit_games_tooling` (new) | `CHANGELOG.md` | repo | this ticket | New; Keep a Changelog |
| `biscuit_games_template` | `template/.github/workflows/ci.yml` | M | T03 | Becomes the caller below |
| `biscuit_games_template` | `template/.github/workflows/chromatic.yml` | M | T03 | Becomes the caller below |
| `biscuit_games_template` | `template/.github/workflows/pages.yml` | M | T03 | Becomes the caller below |
| `biscuit_games_template` | `template/docs/reference/quality-gates.md` | M | T08 | Check names and the calling shape |
| `biscuit_games_template` | `scripts/bootstrap_repo.sh` | repo | C03 | Required-check contexts |
| `biscuit_games_template` | `tests/test_render.py` | repo | T00, T10 | `test_pins_agree` loses its workflow half |
| `biscuit_games_template` | `CHANGELOG.md` | repo | T12 | Release entry with "Update notes" |
| `poodl` | `.github/workflows/ci.yml` | repo | P | Becomes a caller (pull request) |
| `poodl` | `.github/workflows/chromatic.yml` | repo | P | Becomes a caller (pull request) |
| `poodl` | `.github/workflows/pages.yml` | repo | P | Becomes a caller (pull request) |
| `poodl` | `docs/reference/quality-gates.md` | repo | P lines 141-142 | Check names (same pull request) |

## Steps

### The tooling repository

1. **Authorisation required:** creating the repository. Stop and ask, then
   `gh repo create steven-cutting/biscuit_games_tooling --public --clone`. Public,
   because a reusable workflow in a private repository is callable only where that
   repository's Actions access setting allows it, and nothing here is secret: the
   registry token is the caller's `github.token` and is never stored.
2. Root files. `.python-version` is `3.14`. `.gitignore` holds `.DS_Store`, `.venv/`,
   `ai_tmp/`. `pyproject.toml`:

   ```toml
   [project]
   name = "biscuit-games-tooling"
   version = "0.0.0"
   description = "Reusable workflows and a composite toolchain action for Biscuit Games games."
   requires-python = ">=3.14"
   dependencies = []

   [dependency-groups]
   dev = ["prek==0.4.12"]

   [tool.uv]
   package = false
   ```

   `Justfile` is CONVENTIONS.md §9's shape reduced to `default`, `sync`, `lock`,
   `lock-check`, `install-hooks`, `lint` and `check: lock-check lint`, with the same
   `set` lines. Run `uv lock` and commit `uv.lock`.
3. `.pre-commit-config.yaml`: `exclude` of `.git/|.venv/|ai_tmp/|uv\.lock$`; the
   `builtin` hooks `P/.pre-commit-config.yaml:74-83` verbatim; `markdownlint-cli2`,
   `typos`, `actionlint` (with `files: ^\.github/workflows/.*\.ya?ml$`) and
   `ripsecrets` (bare `id`, no custom `entry`) at the `rev` SHAs on P lines 108, 114,
   155 and 161. actionlint reads only the `files:` glob, so `action.yml` is covered by
   `check-yaml` and by the repository's own CI run, not by actionlint.
4. `actions/setup-toolchain/action.yml`, exact:

   ```yaml
   name: Set up the Biscuit Games toolchain
   description: >-
     Node with the GitHub Packages registry for the platform scope, uv with its
     cache, and the pinned Python, just and npm. Runs after the checkout and
     installs nothing from the lockfiles: `just sync` stays in the workflow, on
     the one step that carries NODE_AUTH_TOKEN.

   inputs:
     node-version:
       description: Node release line, as setup-node reads it.
       default: '26'
     npm-version:
       description: npm installed globally over the one Node ships.
       default: '11.17.0'
     uv-version:
       description: uv release for setup-uv.
       default: '0.11.18'
     python-version:
       description: Python for uv python install.
       default: '3.14'
     just-version:
       description: rust-just release installed as a uv tool.
       default: '1.51.0'
     registry-scope:
       description: The npm scope served from GitHub Packages.
       default: '@steven-cutting'
     npm-cache:
       description: >-
         Whether setup-node caches npm keyed on package-lock.json. 'false' where
         no lockfile exists, as in this repository's own gate.
       default: 'true'

   runs:
     using: composite
     steps:
       - uses: actions/setup-node@820762786026740c76f36085b0efc47a31fe5020 # v7.0.0
         with:
           node-version: ${{ inputs.node-version }}
           cache: ${{ inputs.npm-cache == 'true' && 'npm' || '' }}
           cache-dependency-path: package-lock.json
           # A user-level .npmrc under RUNNER_TEMP names the registry for the
           # scope and reads the token from NODE_AUTH_TOKEN on each step that
           # installs, so the committed .npmrc holds nothing.
           registry-url: 'https://npm.pkg.github.com'
           scope: ${{ inputs.registry-scope }}
       - uses: astral-sh/setup-uv@c771a70e6277c0a99b617c7a806ffedaca235ff9 # v9.0.0
         with:
           version: ${{ inputs.uv-version }}
           enable-cache: true
           cache-dependency-glob: uv.lock
       # Inputs arrive through env rather than inside the command, so a value is
       # never substituted as text into a shell line.
       - run: uv python install "$PYTHON_VERSION"
         shell: bash
         env:
           PYTHON_VERSION: ${{ inputs.python-version }}
       - run: uv tool install "rust-just==$JUST_VERSION"
         shell: bash
         env:
           JUST_VERSION: ${{ inputs.just-version }}
       - run: npm install --global "npm@$NPM_VERSION"
         shell: bash
         env:
           NPM_VERSION: ${{ inputs.npm-version }}
   ```

   Commit this first, on its own. The workflows in the next step reference the action
   by the SHA of this commit, and a reference must name a commit that exists. Every
   later change to the action is the same two commits: the action, then the workflows
   moving their pin. The alternative, checking the tooling repository out inside the
   game's workspace at `github.job_workflow_sha` and using a relative path, avoids the
   second commit but leaves an untracked tree that the game's `validate_agents.py`
   inventory (`git ls-files --others`, CONVENTIONS.md §9) can see; it is the fallback,
   not the recommendation.
5. `.github/workflows/game-ci.yml`. Header:

   ```yaml
   name: Game CI

   # Called by every game's ci.yml. Triggers, permissions and concurrency are the
   # caller's; the jobs are the same three every game has always run.

   on:
     workflow_call:
   ```

   Then the `jobs:` block of the template's `template/.github/workflows/ci.yml`
   (Poodl's `ci.yml:22-167` with lines 58-61 replaced by `- run: just lock-check`),
   with one edit per job: the block from `- uses: actions/setup-node` through
   `- run: npm install --global npm@11.17.0` (P lines 30-51, 73-94, 126-147) becomes
   the single step
   `- uses: steven-cutting/biscuit_games_tooling/actions/setup-toolchain@<sha> # v0.1.0`
   where `<sha>` is step 4's commit. Checkout, `just sync` with its `NODE_AUTH_TOKEN`
   step, the Playwright cache step (P 150-155) and every recipe step stay. No
   `permissions:` on these jobs: the caller's workflow-level block already carries
   `contents: read` and `packages: read`.
6. `.github/workflows/game-chromatic.yml`. Header:

   ```yaml
   name: Game Chromatic

   on:
     workflow_call:
       secrets:
         CHROMATIC_PROJECT_TOKEN:
           description: Optional. Absent, the publish is skipped with a notice.
           required: false
   ```

   Then the `jobs:` block of the template's `chromatic.yml` (Poodl's
   `chromatic.yml:37-249` plus the hub guard T03 added from `H:201-217` and
   `H:230-265`), with: the setup
   block P 190-214 (comment 204-206 kept above it) replaced by the same action step;
   an explicit `permissions:` on `authorize` of `contents: read`, `issues: write`,
   `pull-requests: write`, so it holds no package scope, as today; `chromatic` keeps
   its four-scope block (P 174-178). `github.event`, `github.token` and
   `github.repository` inside a called workflow are the caller's, so the `/chromatic`
   gate, the reaction and the reply address the game's pull request unchanged. No
   `concurrency:` here; the caller's applies to the whole run.
7. `.github/workflows/game-pages.yml`. Header and env:

   ```yaml
   name: Game Pages

   on:
     workflow_call:
       inputs:
         base_path:
           description: The path Pages serves the site beneath, with a leading slash.
           type: string
           required: true
         artifact_path:
           description: The directory uploaded to Pages.
           type: string
           default: build
         stage:
           description: Run `npm run stage` after the build (a domain-root layout).
           type: boolean
           default: false

   # A caller's workflow-level env is not passed to a called workflow, which is
   # why the path arrives as an input.
   env:
     BASE_PATH: ${{ inputs.base_path }}
   ```

   Then the template's `pages.yml` jobs (CONVENTIONS.md §7, exact), with: `build` keeps
   its `setup-node` step as is (it runs no recipe, so the action buys it nothing);
   a step `- run: npm run stage` with `if: inputs.stage` between the build and the
   upload, and `path: ${{ inputs.artifact_path }}` on the upload; `deploy` gains an
   explicit `permissions:` of `contents: read`, `pages: write`, `id-token: write`.
   The two inputs beyond `base_path` exist so Poodl (`P/pages.yml:16-22`, `66-72`)
   can call this file with `stage: true` and `artifact_path: site`.
8. `.github/workflows/ci.yml`, the repository's own gate: Poodl's triggers and
   `concurrency` (P `ci.yml:3-9`, `18-20`), `permissions: contents: read`, one job
   `check` (timeout 10) with checkout (`persist-credentials: false`),
   `- uses: ./actions/setup-toolchain` with `npm-cache: 'false'` (a smoke test of the
   action on every push, in the one repository where a relative path is right), then
   `just sync` and `just check`.
9. `README.md`: what the repository hosts; the three callers under "The template",
   step 1, verbatim as the way in; the two-commit rule from step 4; the version policy:
   annotated `vMAJOR.MINOR.PATCH` tags, callers pin the SHA with a `# vX.Y.Z` comment
   exactly as actions are pinned; MAJOR when a caller must change (a check renamed, an
   input made required), MINOR when jobs or the action change without a caller edit,
   PATCH for prose; and the pairing rule: a toolchain default changed in `action.yml`
   ships together with a template release moving the same pin in
   `template/package.json.jinja` and `template/.python-version`, because nothing
   checks the two against each other any more. `CHANGELOG.md` opens with `[Unreleased]`
   and a `v0.1.0` entry.
10. Run `just install-hooks && just check` until clean, commit, then
    **Authorisation required:** pushing, tagging `v0.1.0`, and applying C03's
    `scripts/bootstrap_repo.sh steven-cutting/biscuit_games_tooling --apply` with the
    single required check `check`. Record the SHA of the tagged commit: the callers
    pin it.

### The template

1. Replace the three managed workflows with callers. They stay `.yml`, never
   `.jinja` (CONVENTIONS.md §6 rule 2); nothing in them names the game. Keep the
   comments Poodl attaches to the blocks that survive (`P/ci.yml:6-7`, `13-15`;
   `P/chromatic.yml:3-5`, `8-16`, `21-27`, `33-34`; `P/pages.yml:3-4`, `24-25`).
   Workflow-level `permissions` blocks are byte-identical to today's; where a called
   job holds a scope the workflow block lacks, the caller job carries the union,
   because a called workflow can narrow the caller's token and never widen it. The
   three fences below omit those comments for brevity; restore them from the lines
   cited, so the surviving blocks compare byte for byte.

   `template/.github/workflows/ci.yml`:

   ```yaml
   name: CI

   on:
     pull_request:
     push:
       branches: ['main']
     workflow_dispatch:

   permissions:
     contents: read
     packages: read

   concurrency:
     group: ci-${{ github.workflow }}-${{ github.ref }}
     cancel-in-progress: true

   jobs:
     ci:
       uses: steven-cutting/biscuit_games_tooling/.github/workflows/game-ci.yml@<sha> # v0.1.0
   ```

   `template/.github/workflows/chromatic.yml`:

   ```yaml
   name: Chromatic

   on:
     push:
       branches: ['main']
     issue_comment:
       types: [created]
     workflow_dispatch:

   permissions:
     contents: read
     issues: write
     pull-requests: write

   concurrency:
     group: chromatic-${{ github.event.issue.number || github.ref }}
     cancel-in-progress: ${{ github.event_name == 'issue_comment' }}

   jobs:
     chromatic:
       # The union of what the called jobs hold: the publish job also reads
       # the platform package.
       permissions:
         contents: read
         issues: write
         pull-requests: write
         packages: read
       uses: steven-cutting/biscuit_games_tooling/.github/workflows/game-chromatic.yml@<sha> # v0.1.0
       secrets:
         CHROMATIC_PROJECT_TOKEN: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
   ```

   `template/.github/workflows/pages.yml`:

   ```yaml
   name: Deploy to GitHub Pages

   on:
     push:
       branches: ['main']
     workflow_dispatch:

   permissions:
     contents: read
     pages: write
     id-token: write

   concurrency:
     group: pages
     cancel-in-progress: false

   jobs:
     pages:
       # The union of what the called jobs hold: the build reads the platform
       # package, the deploy publishes.
       permissions:
         contents: read
         pages: write
         id-token: write
         packages: read
       uses: steven-cutting/biscuit_games_tooling/.github/workflows/game-pages.yml@<sha> # v0.1.0
       with:
         # A project site, built to live under the repository's name.
         base_path: /${{ github.event.repository.name }}
   ```

2. `tests/test_render.py::test_pins_agree` (CONVENTIONS.md §9) reads
   `node-version: '26'`, `version: 0.11.18`, `rust-just==1.51.0`, `npm@11.17.0` and
   `uv python install 3.14` from the rendered workflows; none of those strings
   remains. Reduce the test to what the render still carries (`package.json`
   volta/engines against `.python-version`, and the `hub_package_version` pin) and
   add one assertion that each rendered workflow's `uses:` line names
   `steven-cutting/biscuit_games_tooling/.github/workflows/` with a forty-character
   SHA and a `# v` comment. The README rule in the tooling repository's step 9 is what
   replaces the lost comparison.
3. `scripts/bootstrap_repo.sh`: the `contexts` list becomes `ci / frontend`,
   `ci / documents`, `ci / stories`. `template/docs/reference/quality-gates.md`: the
   "In continuous integration" paragraph (P lines 114-120) says the three jobs run
   from the shared workflow and names the repository; the "On `main`" paragraph
   (P 141-142) names the three new contexts. Run `just check`.
4. `CHANGELOG.md` (template repository): an entry under the four headings of
   CONVENTIONS.md §9 whose "Update notes" say: after `copier update`, run C03's script
   (or edit branch protection by hand) because the required-check contexts changed; no
   file is removed. This is a MAJOR release by CONVENTIONS.md §10 (a game must do work
   beyond resolving markers). **Authorisation required:** the pull request to `main`
   and the tag.

### A throwaway game, then Poodl

1. `just render ai_tmp/c01-game` from this branch, `git init -b main`,
   `just initialize`, `just check`, commit. **Authorisation required:** creating a
   throwaway repository (`gh repo create steven-cutting/c01-throwaway --public`),
   granting it read access on the hub package (the package's "Manage Actions access"
   setting, UI only, CONVENTIONS.md §11), pushing `main`, and running C03's script
   against it (Pages source and the three new contexts). The pushing token needs the
   `workflow` scope, or the push is refused for carrying workflow files.
2. Watch the first `main` run: `ci / frontend`, `ci / documents`, `ci / stories`
   green, and `pages / build` and `pages / deploy` green with the site answering at
   `https://steven-cutting.github.io/c01-throwaway/`. **Authorisation required:** a
   pull request from a branch in the same repository, then the comment `/chromatic`
   on it. Without `CHROMATIC_PROJECT_TOKEN` the run must finish green and reply "No
   Chromatic build was published"; with one supplied for the test, it must publish and
   reply "Chromatic run finished". Delete the throwaway repository afterwards
   (**Authorisation required**).
3. **Authorisation required:** a pull request on Poodl replacing its three workflows
   with the callers under "The template", step 1, with `pages.yml` passing
   `base_path: /poodl`, `stage: true` and `artifact_path: site`, editing
   `docs/reference/quality-gates.md` lines 141-142 to the new contexts, and updating
   Poodl's branch protection to the new contexts before the merge. Poodl's `ci.yml`
   gains `uv lock --check` through
   `just lock-check` (`P/Justfile:30-32`), a superset of its current dry run.

## Acceptance criteria

- [ ] `steven-cutting/biscuit_games_tooling` is public, tagged `v0.1.0`, and holds the
      three `workflow_call` workflows, `actions/setup-toolchain/action.yml` with the
      inputs and defaults above, and every `uses:` pinned to a forty-character SHA with
      a version comment.
- [ ] `just check` in the tooling repository is green and its own CI job `check` passes
      using `./actions/setup-toolchain`.
- [ ] A rendered game's three workflows are callers only; their triggers,
      workflow-level `permissions` blocks and `concurrency` groups are byte-identical
      to today's; the effective per-job token scopes equal Poodl's (`authorize` without
      `packages`, `chromatic` and `build` with it, `deploy` with the two publishing
      scopes).
- [ ] Every job runs the same `just` recipes in the same order as `P/ci.yml`,
      `P/chromatic.yml` and the template's `pages.yml`.
- [ ] In the template repository `just check` is green, actionlint passes over
      `template/.github/workflows/*.yml` at source, and `test_pins_agree` holds the
      reduced comparison.
- [ ] The throwaway game's `ci / frontend`, `ci / documents` and `ci / stories` are
      green and are the branch's required contexts; the `/chromatic` path ran once and
      replied; Pages deployed and serves the site.
- [ ] C03's script, the template's `quality-gates.md` and its `CHANGELOG.md` name the
      new contexts; the release is marked MAJOR.
- [ ] Poodl's pull request is opened (not merged without approval) with the same
      callers and its protection updated in the same change.

## Verification

Tooling repository, from its root:

```sh
just check
uv run --frozen prek run --all-files actionlint check-yaml
```

Expected: exit 0; actionlint reports nothing on the four workflow files.

Template repository, from the repository root:

```sh
just check
uv run --frozen prek run --all-files actionlint
grep -n 'biscuit_games_tooling/.github/workflows/' template/.github/workflows/*.yml
```

Expected: `just check` green; actionlint clean; three matching lines, one per file,
each ending in a forty-character SHA and a `# v0.1.0` comment.

Throwaway game, from the throwaway clone, after step 2 under "A throwaway game, then
Poodl" (`R` is `steven-cutting/c01-throwaway`):

```sh
gh api "repos/$R/commits/$(git rev-parse main)/check-runs" --jq '.check_runs[] | "\(.name): \(.conclusion)"'
gh api "repos/$R/branches/main/protection" --jq '.required_status_checks.contexts'
gh run list --repo "$R" --workflow Chromatic --limit 1
gh run list --repo "$R" --workflow 'Deploy to GitHub Pages' --limit 1
curl -sI https://steven-cutting.github.io/c01-throwaway/ | head -n 1
gh api repos/steven-cutting/biscuit_games_tooling --jq .visibility
```

Expected, in order: `ci / frontend: success`, `ci / documents: success`,
`ci / stories: success`, plus `pages / build` and `pages / deploy` as `success`;
`["ci / frontend","ci / documents","ci / stories"]`; one completed Chromatic run with
`success` and a reply comment on the pull request; one completed Pages run with
`success`; `HTTP/2 200`; `public`.

## Hand-back notes

Filled in by the agent that executes this ticket.

- What was verified and how: quote the output of every command above, the exact
  check-run names GitHub reported, and the `BASE_PATH` the Pages build logged.
- What deviated from the ticket and why, with the file and the reason.
- What was handed back to another ticket: C02 and C04 (the host is now decided),
  C07 (whether Poodl keeps `stage`/`artifact_path` or its own `pages.yml`), and any
  handbook page beyond `quality-gates.md` whose prose no longer holds
  (`docs/how-to/deploy-to-github-pages.md` describes what `pages.yml` does).
- Which open points were settled, and how each check came out.

## Open points

No CONVENTIONS.md §12 claim is assigned to this ticket. These were reasoned from
GitHub's documentation and not executed; each names its check.

- A relative `uses: ./actions/...` inside a called workflow resolves against the
  caller's checkout, which is why the three workflows use the full
  `owner/repo/path@sha` form. Check: the throwaway game's first run; if a relative
  path also works there, say so and keep the SHA form anyway for C04.
- A called workflow's job cannot hold a scope the caller's job lacks, and the run
  fails naming the scope. Check: on the throwaway repository, drop `packages: read`
  from the `pages` caller job once and read the failure text, then restore it.
- Check-run names are `<caller job> / <called job>`, so the contexts are exactly
  `ci / frontend`, `ci / documents`, `ci / stories`. Check: the `check-runs` command
  above; if the strings differ, the bootstrap script, `quality-gates.md` and Poodl's
  pull request take the strings GitHub reports.
- A public repository's reusable workflows are callable from any repository without an
  access setting. Check:
  `gh api repos/steven-cutting/biscuit_games_tooling/actions/permissions/access`
  answers that the endpoint applies to private repositories only, and the throwaway
  run starts.
- `github.event.repository.name` is populated inside `with:` on `push` and
  `workflow_dispatch`, and `inputs` reaches a called workflow's workflow-level `env`.
  Check: the Pages build log shows `BASE_PATH=/c01-throwaway` on both triggers
  (CONVENTIONS.md §12 carries the `env:` form of this claim for T03 and T11).
- `setup-node` accepts an empty `cache:` from the `npm-cache` expression and skips
  caching. Check: the tooling repository's own `check` job on its first run.
- The template release level is MAJOR by CONVENTIONS.md §10. Check: confirm with the
  maintainer when the tag is authorised.
