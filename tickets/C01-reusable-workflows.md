---
id: C01
title: Reusable workflows and a composite toolchain action for every game
status: done
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
gh api "repos/$R/branches/main/protection" --jq '[.required_status_checks.checks[].context]'
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

### Outcome

- `steven-cutting/biscuit_games_tooling` exists, is public, and is tagged `v0.1.0` at
  `be41556ff01d00aba77cfac4c34f9727b8580bd6`. It holds the three `workflow_call`
  workflows, `actions/setup-toolchain/action.yml` and its own gate. Its `main` requires
  `check`.
- In this repository, the three managed workflows are callers pinned to that commit.
  Also changed: `test_pins_agree`, `quality-gates.md`, `update-from-template.md` and
  `CHANGELOG.md` (Unreleased, MAJOR). All of it is committed on the ticket branch and not
  yet pushed.
- The throwaway game `steven-cutting/c01-throwaway` proved every path with the new
  callers: CI, Pages on push and on dispatch, and `/chromatic` without a token.
- Still to come, each separately authorised: the pull request on `main` and the `v1.0.0`
  tag; the maintainer deleting the throwaway in the web UI; Poodl's adoption, handed to
  the maintainer as a Claude Code prompt to run in Poodl.

### What was verified, and how

Output is quoted. Elisions are in square brackets, and so is the `=` padding of pytest's
summary lines.

The tooling repository. Commit `73df4e2` is the action alone, and `be41556` is everything
else:

```text
$ just check
uv lock --check
Resolved 2 packages in 3ms
uv run --frozen prek run --all-files
[check for added large files, case conflicts, merge conflicts, shebang scripts, toml,
yaml, private key: Passed; shebangs and json: no files to check]
markdownlint.............................................................Passed
typos....................................................................Passed
Lint GitHub Actions workflow files.......................................Passed
ripsecrets...............................................................Passed
$ uv run --frozen prek run --all-files actionlint check-yaml
check yaml...............................................................Passed
Lint GitHub Actions workflow files.......................................Passed
$ gh run view 34945297742 -R steven-cutting/biscuit_games_tooling --json conclusion,jobs [...]
"conclusion":"success", job "check": "Run ./actions/setup-toolchain: success",
"Run just sync: success", "Run just check: success"
$ git ls-remote --tags origin 'v0.1.0*'
64256881a196ba046822c9d6e66a941b456a1eaf  refs/tags/v0.1.0
be41556ff01d00aba77cfac4c34f9727b8580bd6  refs/tags/v0.1.0^{}
$ gh api repos/steven-cutting/biscuit_games_tooling/branches/main/protection --jq [C03's read]
false check false false false false false
```

actionlint hands no `run:` block to shellcheck under prek (`quality-gates.md`). So the
three multi-line blocks of `game-chromatic.yml` were extracted and checked with
shellcheck 0.11.0 by hand: the `authorize` gate (85 lines), the token check (6) and the
reply (26). Exit 0. A control file carrying `echo $undefined_var` exited 1 with SC2154 and
SC2086, so the tool was reading.

This repository, with the callers pinned (commit `577f706`):

```text
$ just check
[every hook line Passed, Lint GitHub Actions workflow files among them]
Success: no issues found in 10 source files
[...] 45 passed, 3 skipped, 31 warnings in 60.76s (0:01:00) [...]
$ uv run --frozen prek run --all-files actionlint
Lint GitHub Actions workflow files.......................................Passed
$ grep -n 'biscuit_games_tooling/.github/workflows/' template/.github/workflows/*.yml
template/.github/workflows/ci.yml:28:    uses: steven-cutting/biscuit_games_tooling/.github/workflows/game-ci.yml@be41556ff01d00aba77cfac4c34f9727b8580bd6 # v0.1.0
template/.github/workflows/chromatic.yml:46:    uses: steven-cutting/biscuit_games_tooling/.github/workflows/game-chromatic.yml@be41556ff01d00aba77cfac4c34f9727b8580bd6 # v0.1.0
template/.github/workflows/pages.yml:31:    uses: steven-cutting/biscuit_games_tooling/.github/workflows/game-pages.yml@be41556ff01d00aba77cfac4c34f9727b8580bd6 # v0.1.0
```

The three skips are `test_full` and the two `test_specs` cases, which need
`BISCUIT_TEMPLATE_FULL` and `BISCUIT_TEMPLATE_NETWORK`. The 31 warnings are copier's
`DirtyLocalWarning`.

The throwaway game was made with `just render ai_tmp/c01-game` from `577f706`, then
`git init -b main`, `just initialize` (exit 0), `just check` (exit 0, ending "All checks
passed and the worktree is unchanged.") and a commit, `3d02eb5`:

```text
$ gh api -X POST repos/steven-cutting/c01-throwaway/pages -f build_type=workflow   [before the first push]
{"build_type":"workflow","html_url":"http://stevencutting.com/c01-throwaway/"}
$ gh api repos/steven-cutting/c01-throwaway/branches/main/protection --jq '[.required_status_checks.checks[].context]'
["ci / frontend","ci / documents","ci / stories"]
$ gh run list --commit 3d02eb5 --event push [...]
Chromatic 34945783019: success
Deploy to GitHub Pages 34945782902: success
CI 34945783035: success
$ gh api repos/steven-cutting/c01-throwaway/commits/3d02eb5[...]/check-runs --jq [name: conclusion]
chromatic / chromatic: success
chromatic / authorize: success
pages / deploy: success
ci / documents: success
ci / frontend: success
ci / stories: success
pages / build: success
[chromatic / authorize and chromatic / chromatic once more: the /chromatic run below]
$ gh run view 34945782902 --log | grep BASE_PATH   [push]
pages / build | BASE_PATH: /c01-throwaway
pages / deploy | BASE_PATH: /c01-throwaway
$ gh run view 34946072661 --log | grep BASE_PATH   [workflow_dispatch, success]
pages / build | BASE_PATH: /c01-throwaway
pages / deploy | BASE_PATH: /c01-throwaway
```

Pull request #1 came from the branch `c01-chromatic-review`. Its CI, run 34945838871,
succeeded, and the head `605fc71` reports `ci / frontend`, `ci / documents` and
`ci / stories`, each `success`. The comment `/chromatic` got a `rocket` reaction, and run
34945840577 finished `success`:

```text
chromatic / authorize: Decide whether this comment may publish: success
chromatic / chromatic: Run steven-cutting/biscuit_games_tooling/actions/setup-toolchain@73df4e2[...]: success
  Run just sync: success
  Note whether a Chromatic token is configured: success
  ##[notice]CHROMATIC_PROJECT_TOKEN is not set; skipping the publish.
  Publish the workshop to Chromatic: skipped
  Report back on the pull request: success
github-actions[bot]: No Chromatic build was published: `CHROMATIC_PROJECT_TOKEN` is not set on this repository. The run finished `success` and is at https://github.com/steven-cutting/c01-throwaway/actions/runs/34945840577
```

The Codex app's review-summary comment on the same pull request started a second
`issue_comment` run, 34946057508. It finished `skipped`, because the job's prefilter
refused a comment that is not `/chromatic`.

The scope experiment ran on the throwaway's `main`. Commit `0d4ca05` dropped
`packages: read` from the `pages` calling job and was pushed, and commit `98b2940`
reverted it:

```text
$ gh run view 34946332089   [the Pages run on 0d4ca05]
X main Deploy to GitHub Pages · 34946332089
X This run likely failed because of a workflow file issue.
$ gh api repos/steven-cutting/c01-throwaway/actions/runs/34946332089 --jq '{conclusion, path}'
{"conclusion":"startup_failure","path":".github/workflows/pages.yml"}
[the run's page, at .github/workflows/pages.yml line 23, column 3:]
Error calling workflow 'steven-cutting/biscuit_games_tooling/.github/workflows/game-pages.yml@be41556ff01d00aba77cfac4c34f9727b8580bd6'. The nested job 'build' is requesting 'packages: read', but is only allowed 'packages: none'.
$ gh run list --commit 98b2940 --event push [...]
Deploy to GitHub Pages 34946370657: success
Chromatic 34946370778: success
CI 34946370763: success
$ git diff 3d02eb5 98b2940 --stat
[empty: the revert's tree is the first push's]
```

The failure text is only on the run's web page. `gh run view` does not print it, and the
GraphQL check suite reads `STARTUP_FAILURE` with no check runs. The experiment's CI run,
34946332106, was cancelled when the revert was pushed (`ci.yml`'s
`cancel-in-progress`). Its Chromatic run, 34946332147, succeeded.

The ticket's verification ran on the throwaway's final `main`, `98b2940`, with `R` set to
`steven-cutting/c01-throwaway`:

```text
$ gh api "repos/$R/commits/$(git rev-parse main)/check-runs" --jq '.check_runs[] | "\(.name): \(.conclusion)"'
pages / deploy: success
chromatic / chromatic: success
ci / stories: success
ci / frontend: success
ci / documents: success
chromatic / authorize: success
pages / build: success
$ gh api "repos/$R/branches/main/protection" --jq '[.required_status_checks.checks[].context]'
["ci / frontend","ci / documents","ci / stories"]
$ gh run list --repo "$R" --workflow Chromatic --limit 1
completed  success  Revert "Drop packages: read from the pages caller job, to read the fa…  Chromatic  main  push  34946370778  55s  2026-09-15T08:19:59Z
$ gh run list --repo "$R" --workflow Chromatic --event issue_comment --limit 2
completed  skipped  Test /chromatic through the shared workflow  Chromatic  main  issue_comment  34946057508  2s  2026-09-15T08:16:29Z
completed  success  Test /chromatic through the shared workflow  Chromatic  main  issue_comment  34945840577  37s  2026-09-15T08:14:07Z
$ gh run list --repo "$R" --workflow 'Deploy to GitHub Pages' --limit 1
completed  success  Revert "Drop packages: read from the pages caller job, to read the fa…  Deploy to GitHub Pages  main  push  34946370657  43s  2026-09-15T08:19:59Z
$ curl -sI https://steven-cutting.github.io/c01-throwaway/ | head -n 1
HTTP/2 301
$ curl -sIL https://steven-cutting.github.io/c01-throwaway/ | grep -iE '^(HTTP|location)'
HTTP/2 301
location: https://stevencutting.com/c01-throwaway/
HTTP/2 200
$ gh api repos/steven-cutting/biscuit_games_tooling --jq .visibility
public
```

`gh run list` separates its columns with tabs, shown here as two spaces. The latest
Chromatic run is the revert's push, which sets the baseline. The `/chromatic` run is the
`issue_comment` one, listed with the skipped run the Codex comment started.

### Deviations

- **C03 had not run.** `scripts/bootstrap_repo.sh` does not exist, so this ticket did not
  edit it. Both new repositories were protected with a direct `gh api -X PUT
  .../branches/main/protection` carrying C03 step 2's body. The maintainer chose this on
  2026-09-15 rather than doing C03 first.
- **Poodl got a prompt, not a pull request.** Cross-repository work goes to the maintainer
  as a Claude Code prompt to run in that repository, so nothing in Poodl was touched. The
  prompt carries the three callers (`pages.yml` with `base_path: /poodl`, `stage: true`,
  `artifact_path: site`), the `quality-gates.md` edits, the protection change before the
  merge, and a stop before every outward step.
- **`template/docs/how-to/update-from-template.md.jinja`, a file this ticket does not
  list,** gained a `### 1.0.0` entry under "Steps by version". The section said "Nothing
  yet: the first release asks nothing", which this release makes false, and it is where a
  game looks for what a release asks of it. The change is recorded under Managed in
  `CHANGELOG.md`.
- **`README.md` line 133, also unlisted,** now names `ci / frontend`, `ci / documents` and
  `ci / stories` in the by-hand bootstrap list, for the same reason: the old names became
  false with this change. A repository file reaches no game, so it has no changelog entry.
- **`quality-gates.md` changed beyond its two named paragraphs.** The actionlint-gap
  paragraph placed the multi-line shell in `chromatic.yml`, and the `packages: read`
  sentence placed the scope on "the one job in each that does". Both became false, and
  both were rewritten.
- **The tooling repository has 14 files, not 13.** `.markdownlint-cli2.jsonc` turns MD013
  off, as Poodl's and this repository's configs do, because the README's caller fences
  carry `uses:` lines wider than markdownlint's default of 80 columns.
- **Comments in the called workflows.** A script sliced the three workflows from this
  repository's copies and diffed them against the originals. The diff shows only these
  comment edits:
  - the note in `game-chromatic.yml` naming the required checks now names the `ci / …`
    contexts;
  - the two job-block comments that said a block "replaces the workflow's" now say what a
    called job's block does;
  - `authorize` and `deploy` each gained a comment over their new `permissions`;
  - the upload's comment covers `artifact_path`;
  - `game-ci.yml` and `game-chromatic.yml` open with a short header comment.
- **Comments in the callers.**
  - `ci.yml` names the three contexts over `ci:`.
  - `chromatic.yml` says the secret is optional.
  - `pages.yml` carries the substance of the old workflow-level `env` comment (lines
    16-20) on `with:`, instead of the one-line comment in step 1's fence, because
    `base_path` is the block that comment described.
- **`test_pins_agree` asserts two things more.** Each workflow calls its own counterpart
  (`ci.yml` calls `game-ci.yml`, and so on), and all three pin one SHA and one tag.
- **The throwaway's site is served from a custom domain.** The account's user Pages site
  has one, so `https://steven-cutting.github.io/c01-throwaway/` answers `HTTP/2 301` to
  `https://stevencutting.com/c01-throwaway/`, which answers `HTTP/2 200` with the title
  "Tic Tac Toe Beans". The ticket expected `HTTP/2 200` on the first address.
- **The throwaway is not deleted.** The `gh` token lacks `delete_repo`, and the maintainer
  chose to delete the repository in the web UI.
- **Branch name and release.** The branch is the Supacode worktree's
  `C01-reusable-workflows-2026-9-15`, as T10 to T12's were. The release is `v1.0.0`, the
  maintainer's choice.

### Handed back

- **To C03:**
  - `--checks` should default to `ci / frontend,ci / documents,ci / stories`. The names
    carry spaces, so the list is split on commas alone, with no trimming.
  - The expected protection line becomes
    `false ci / documents,ci / frontend,ci / stories false false false false false`.
  - Step 8's "Bootstrap" section replaces `README.md`'s by-hand list, which now names the
    new contexts; the section should keep them.
  - Two of C03's open points were settled here. `POST /repos/{owner}/{repo}/pages` accepted
    `build_type=workflow` with no `source` on a repository that had no commits yet. A
    `checks` list without `app_id` was accepted before any workflow had run, and it read
    back as sent.
- **To a pull request on `main` for `CONVENTIONS.md` (§11):** §7's exact `ci.yml`,
  `chromatic.yml` and `pages.yml`, §9's description of `test_pins_agree`, and §3's note
  that `test_pins_agree` holds the tool versions equal no longer describe this repository.
- **Managed pages whose prose no longer holds:**
  - In `template/docs/how-to/deploy-to-github-pages.md.jinja`, "What the workflow does"
    says `BASE_PATH` is set "in the workflow's own `env` block". It is now set in the
    shared workflow's, from `base_path`.
  - In `template/docs/how-to/maintain-dependencies.md`, "Actions in the workflows" tells a
    game to move action SHAs in its workflows. They now hold one pin each, the shared
    workflow's, and the toolchain pins move in the tooling repository.
- **To C03 or C07, or a T00 follow-up:** `copier.yml`'s `pages_url`
  (`https://<owner>.github.io/<repository>/`) is a redirect for this account, not the
  address Pages serves. The handbook, `AGENTS.md` and a game's README all state it.
- **To C02 and C04:** the host is `steven-cutting/biscuit_games_tooling`, public, released
  as annotated `vMAJOR.MINOR.PATCH` tags that callers pin by commit. `v0.1.0` is `be41556`.
  Under the two-commit rule, the tagged workflows pin the action at `73df4e2 # v0.1.0`,
  the commit before the tag's. Both commits hold the same `action.yml`, but an updater
  that moves a SHA to its comment's tag (C04) would rewrite that pin to `be41556`.
- **To C07:** whether Poodl keeps `stage` and `artifact_path`, which the prompt uses, or
  takes the template's project-site `pages.yml`. Poodl's `chromatic.yml` lacks the token
  guard the shared workflow carries, so adopting it changes what happens only while the
  secret is unset.
- **`tic_tac_toe_beans`** is unprotected today. When it takes this release, its protection
  uses the new names, as the `1.0.0` step says.
- **Seed decisions 0006 and 0007** name `documents` and `stories` as CI jobs, which stays
  true. They are untouched.

### Open points, settled

- **A relative `uses:` inside a called workflow:** not tried. The workflows use the
  `owner/repo/path@sha` form, and every job ran
  `steven-cutting/biscuit_games_tooling/actions/setup-toolchain@73df4e2[...]: success`.
- **A called job cannot hold a scope the calling job lacks:** see the scope experiment
  above.
- **Check-run names:** exactly `ci / frontend`, `ci / documents` and `ci / stories`, plus
  `pages / build`, `pages / deploy`, `chromatic / authorize` and `chromatic / chromatic`.
- **Public reusable workflows need no access setting:**
  `gh api repos/steven-cutting/biscuit_games_tooling/actions/permissions/access` answered
  `Access policy only applies to internal and private repositories. (HTTP 422)`, and the
  throwaway's runs started with nothing set.
- **`github.event.repository.name` in `with:`, and `inputs` in a called workflow's
  workflow-level `env`:** `BASE_PATH: /c01-throwaway` on the push run and on the dispatch
  run.
- **`setup-node` with an empty `cache:`:** accepted. The tooling repository's run
  34945297742 logged the action's inputs as `node-version: 26`,
  `cache-dependency-path: package-lock.json` and `package-manager-cache: true`, with no
  `cache`, and the job passed.
- **Release level:** MAJOR, confirmed with the maintainer, to be tagged `v1.0.0` once
  merged.
- **Not in the ticket, and settled by the same runs:**
  - A caller's workflow-level `permissions` reaches a calling job that has no block of its
    own: `ci / *` installed the package under `ci.yml`'s workflow-level `packages: read`.
  - `actions/deploy-pages` works inside a reusable workflow hosted in another repository.
  - No package grant was added for the throwaway, and every install with the run's token
    succeeded.

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
