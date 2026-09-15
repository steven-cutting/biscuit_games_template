# biscuit_games_template

A [Copier](https://copier.readthedocs.io/en/stable/) template that renders a Biscuit Games
game: a static SvelteKit site consuming `@steven-cutting/biscuit-games` from GitHub
Packages, carrying Poodl's toolchain, handbook, agent contract and quality gate in generic
form. A render passes its own `just check` on the first run.

There is one shape and no toggles. The questionnaire asks `game_name`, `game_slug`,
`description` and `repository` and nothing else, and no game rule is rendered: what a game
plays is written in the game.

The template is taskless: it declares no `_tasks`, no `_migrations` and no Jinja
extensions, so `copier` never needs `--trust`. `copier update` is how a toolchain change
made here reaches every rendered game.

## Use it

Prerequisites: git, uv 0.11.18, just 1.51.0, Node 26.5.1 with npm 11.17.0 (Volta-pinned in
the render), copier 9.18.2 or newer (`_min_copier_version` refuses an older one; the
template is tested against the version `pyproject.toml` pins), and a GitHub token carrying
`read:packages` in `~/.npmrc`, because GitHub Packages refuses an anonymous read of the
platform package. The line in `~/.npmrc`:

```text
//npm.pkg.github.com/:_authToken=<your token>
```

Replace the placeholder, angle brackets and all. It stays bracketed here because
`ripsecrets` reads this repository and takes a bare word after `_authToken=` for a token.

```sh
uvx copier copy gh:steven-cutting/biscuit_games_template <directory>
cd <directory>
git init -b main
just initialize
just check
```

- `copier copy` renders from the latest tag; `--vcs-ref vX.Y.Z` picks another. Never pass
  `--trust`.
- `git init -b main` is skipped inside an existing clone. There, delete an existing
  `README.md` first: `_skip_if_exists` keeps a file that is already present.
- `just initialize` creates both lockfiles, installs both toolchains, downloads Chromium,
  installs the Allium binary and the pre-commit hook, and never stages, commits, tags or
  pushes.
- `just check` runs the twelve gates. Its first run needs the network, to clone the hook
  repositories, and on Linux a prior `just storybook-browsers-deps`, which asks for sudo.

Then commit everything, `.copier-answers.yml` and both lockfiles included, because
`copier update` reads the answers file. Before the first push, grant the repository read
access on the package and set its Pages source to GitHub Actions; both are steps in
"Bootstrap a repository" below.

From a clone of this repository, `just new-game <directory>` asks the questionnaire,
renders from the latest tag and prints the next steps.

## What every rendered game gets

- The quality gate: `just check` runs twelve gates in order, `lock-check`, `lint`,
  `frontend-static`, `frontend-coverage`, `frontend-build`, `storybook-build`,
  `storybook-test`, `check-docs`, `check-agents`, `check-specs`, `analyse-specs` and
  `check-clean`, the last proving the run changed nothing.
- A handbook of 38 files, 28 pages and 10 decision records, held to `docs/manifest.yml` by
  `scripts/validate_docs.py`.
- The agent contract: `AGENTS.md`, `CLAUDE.md`, eight skills under `.agents/skills/` with
  sixteen bridges under `.claude/skills/` and `.codex/skills/`, and the Copilot adapter
  `.github/copilot-instructions.md`, held by `scripts/validate_agents.py`.
- Three workflows: `ci.yml`; `chromatic.yml`, which skips the publish cleanly without a
  `CHROMATIC_PROJECT_TOKEN`; and `pages.yml`, which publishes a project site with
  `BASE_PATH` read from the workflow event.
- The platform package pinned exactly, at the version `copier.yml`'s `hub_package_version`
  names.
- A root Allium module, `docs/specs/<slug>.allium`, stating the six platform figures;
  `src/lib/config.ts` mirroring them; and `tests/platformSpecs.test.ts` holding the three
  equal.
- Three ports under `src/lib/ports/`, storage, clock and randomness, each with an in-memory
  fake.
- A lockup component, a page, a story and their tests, all reading the game's name from
  `src/lib/brand.ts`.

## Managed and seed

Every file the template renders, except `.copier-answers.yml`, is one of two classes, and
`tests/inventory.py` records which. A managed file is re-rendered on every `copier update`
and 3-way merged with the game's edits: a change on one side arrives cleanly, changes to
different hunks merge, and the same hunk changed on both sides leaves inline
`<<<<<<< before updating` markers. A seed file is rendered once, by `copier copy`, and an
update never merges, recreates or deletes it. `.copier-answers.yml` is Copier's, rewritten
by every update.

The seed paths, as `copier.yml` lists them in `_skip_if_exists` and in the update block of
`_exclude`:

- `/README.md`
- `/CHANGELOG.md`
- `/SECURITY.md`
- `/docs/project/purpose-and-scope.md`
- `/docs/project/terminology.md`
- `/docs/decisions/`
- `/docs/specs/`
- `/src/lib/brand.ts`
- `/src/lib/components/`
- `/src/routes/+page.svelte`
- `/stories/`
- `/tests/restated.ts`
- `/tests/lockup.test.ts`
- `/tests/route.test.ts`

Fourteen managed files are ones a game is expected to edit (`GAME_EDITED` in
`tests/inventory.py`): `docs/manifest.yml`, `docs/README.md`, `AGENTS.md`, `Justfile`,
`package.json`, `eslint.config.js`, `.gitignore`, `.prettierignore`, `lychee.toml`,
`.pre-commit-config.yaml`, `.pre-commit-fix.yaml`, `pyproject.toml`, `src/lib/config.ts`
and `tests/ports.test.ts`. One convention keeps the template's edits and the game's in
different hunks: the template inserts in the upper blocks, and the game appends at the
end. When a departure would suit every game, change the template instead.

The seed inventory is frozen. `docs/manifest.yml` and `docs/README.md` re-render on every
update while seeds never do, so since `v0.1.0` the template never adds, renames or
retitles a seed page or a numbered decision: a game would keep its old seed while the
re-rendered manifest declared the new one, and its `check-docs` would fail. Anything the
template later hands to games is a managed page.

A managed file the template stops rendering is deleted from every game on its next update,
edited or not. Every removal is therefore a MAJOR release, announced under "Update notes"
in [`CHANGELOG.md`](CHANGELOG.md).

## Bootstrap a repository

A rendered game's repository needs five things no file can carry:

1. The Pages source set to GitHub Actions. Until it is, `pages.yml` builds its artefact
   and the deploy job fails with `Failed to create deployment (status: 404)`.
2. Protection on `main` requiring the checks `ci / frontend`, `ci / documents` and
   `ci / stories`: not required to be up to date, no review required, force pushes and
   deletion refused.
3. `CHROMATIC_PROJECT_TOKEN` as a repository secret. It is optional: without it
   `chromatic.yml` reports and skips the publish.
4. Private vulnerability reporting switched on where GitHub offers it, which is on public
   repositories. On a private one the endpoint answers `404`, and the fallback paragraph
   in the game's `SECURITY.md` is the route instead.
5. The package's grant of read access to the repository. It is a setting on
   `@steven-cutting/biscuit-games`, its "Manage Actions access" setting, and not on either
   repository; no REST endpoint for it is known. Without it every workflow that installs
   the package fails.

This repository needs three of the five: step 2, with `fast` and `full` as the checks, in
the order "Bootstrap of this repository" below gives; step 4; and step 5, because its
`full` job installs the package. It publishes no Pages site and has no Chromatic workflow,
so steps 1 and 3 do not apply.

These steps are done by hand until
[`tickets/C03-repository-bootstrap.md`](tickets/C03-repository-bootstrap.md) lands and its
script replaces this list.

## Maintain the template

| Recipe | Does | Needs |
| --- | --- | --- |
| `just sync` | Installs the Python toolchain from `uv.lock`. | uv |
| `just check` | `lock-check`, `lint`, `typecheck`, `test`: the gate CI's `fast` job runs. | Seconds; the network once, for the hook repositories |
| `just test` | Renders the template into temporary directories and inspects the trees. `BISCUIT_TEMPLATE_NETWORK=1` adds the Allium gate. | Seconds; offline |
| `just test-full` | Additionally runs `just initialize` and `just check` inside a render: what CI's `full` job runs. | The network, a `read:packages` token in `~/.npmrc`, Chromium, 10 to 20 minutes |
| `just render [dest]` | A render with default answers from the working tree, into `ai_tmp/render` by default. | Seconds |
| `just new-game <dest>` | The questionnaire, then a render from the latest tag. | Seconds |
| `just fix` | Runs the fixers over the tree, then `just lint`. | Seconds |

What `just test` proves, module by module:

- `tests/test_render.py`: the render holds exactly the paths `tests/inventory.py` lists,
  and the two seed lists in `copier.yml` are identical; every source without `.jinja`
  renders byte-identical, and every `.jinja` source renders with no `{{`, `{%` or `{#`; no
  Poodl residue outside the provenance files; the tool pins agree; managed pages link only
  to pages every game keeps; and an answer Markdown would read as syntax is refused.
- `tests/test_validators.py`: both shipped validators, `scripts/validate_docs.py` and
  `scripts/validate_agents.py`, pass on a render and fail on a planted defect.
- `tests/test_questionnaire.py`: the questionnaire refuses what the validators in
  `copier.yml` refuse, and computes the slug and the repository from the other answers.
- `tests/test_update.py`: the `copier update` round trip from `HEAD~2` and from the latest
  tag; a pristine game equals a fresh render, and a game's own work survives.
- `tests/test_specs.py`, with `BISCUIT_TEMPLATE_NETWORK=1`: the seed Allium module passes
  `check` and `analyse` inside a render.
- `tests/test_full.py`, under `just test-full`: a render passes `just initialize` and
  `just check` and leaves only its two lockfiles behind.

To add a managed file:

1. Create it under `template/`, with the `.jinja` suffix only if it substitutes an answer
   or a `_copier_*` value, and never for a `.svelte`, `.test.ts`, `.stories.svelte`,
   workflow `.yml` or `.py` file (`tickets/CONVENTIONS.md` §6).
2. Add its rendered path to `MANAGED` in `tests/inventory.py`, and to `GAME_EDITED` if a
   game is expected to edit it.
3. A handbook page also gets an entry in `template/docs/manifest.yml`, inside the upper
   blocks, and a link in `template/docs/README.md.jinja`.
4. Run `just test`.
5. Record it in `CHANGELOG.md` under Unreleased, Managed. It is a MINOR release.

Never add a seed.

The build is recorded in `tickets/`: [`tickets/README.md`](tickets/README.md) is the index
and [`tickets/CONVENTIONS.md`](tickets/CONVENTIONS.md) the design every ticket obeys. The
tickets stay in the repository as the record of how the template was built, and
`docs/reports/` holds the comparison behind choosing Copier.

## Release

Releases are annotated tags `vMAJOR.MINOR.PATCH` on `main`. A prerelease is spelt
`v0.2.0rc1`, with no hyphen, and `copier update` skips it unless asked with
`--prereleases`.

- MAJOR when a game must do work beyond resolving markers: a validator contract change, a
  removed managed file, a new question without a default.
- MINOR for a new managed file, page or recipe, a pin bump, or a change to
  `_min_copier_version`.
- PATCH for prose.

To release, move the Unreleased entries under `## [X.Y.Z] - YYYY-MM-DD`, keeping the four
headings (Managed, Seed, Questionnaire, Update notes) and leaving them empty under
Unreleased; add the `[X.Y.Z]` link reference and point `[Unreleased]` at the new tag; merge
to `main` through a pull request. Then, on the merged `main`:

```sh
git tag -a vX.Y.Z -m "biscuit_games_template vX.Y.Z"
git push origin vX.Y.Z
```

Both commands are separately authorised; see [`AGENTS.md`](AGENTS.md). Tag before any game
renders from the release: an untagged render records a bare SHA as `_commit`.
`pyproject.toml` pins `copier==9.18.2`; `_min_copier_version` moves only when the template
needs something newer.

## Bootstrap of this repository

CI (`.github/workflows/ci.yml`) runs two jobs on every pull request, on push to `main`,
weekly and on dispatch. `fast` runs the steps of `just check`, with the one download the
fast suite makes, the pinned Allium binary. `full` runs `just test-full`, which installs
the platform package inside a render with the run's own token under `packages: read`.

Neither job is a required check yet: `main` is not protected. Applying the bootstrap steps
to this repository is C03's first job, and it makes `fast` required. `full` becomes
required only once the package grants `steven-cutting/biscuit_games_template` read access
(step 5 of "Bootstrap a repository") and `full` has gone green, because a required check
that cannot pass would block every merge. `full` has passed since pull request 12, so the
run's own token already reads the package; C03 confirms whether a grant is in place or
none is needed, then requires both jobs.
