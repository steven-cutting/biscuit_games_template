# Changelog

All notable changes to this template are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and
releases follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html) as
[the README](README.md) defines MAJOR, MINOR and PATCH for a template. Every release
uses the same four headings: Managed (files an update merges into every game that keeps
them), Seed (files a game gets once, on copy), Questionnaire (questions and computed
values) and Update notes (what a game must do beyond resolving markers). Only changes to
`copier.yml` and `template/` are recorded: the rest of this repository, its README, tests,
CI and tickets, reaches no game.

## [Unreleased]

### Managed

- `.github/workflows/ci.yml`, `.github/workflows/chromatic.yml` and
  `.github/workflows/pages.yml` become callers of the shared workflows in
  `steven-cutting/biscuit_games_tooling`, pinned to its `v0.1.0` commit: `ci.yml` calls
  `game-ci.yml`, `chromatic.yml` calls `game-chromatic.yml` and passes
  `CHROMATIC_PROJECT_TOKEN`, and `pages.yml` calls `game-pages.yml` with `base_path` read
  from the event. Triggers, the workflow-level `permissions` and `concurrency` are
  unchanged, every job runs the same recipes in the same order, and the toolchain setup
  each job repeated is that repository's `setup-toolchain` action. The calling jobs in
  `chromatic.yml` and `pages.yml` hold `packages: read` beside the workflow's scopes, which
  the called jobs narrow as the jobs here did.
- `docs/reference/quality-gates.md` names the shared workflow and the renamed required
  checks, and `docs/how-to/update-from-template.md` records the protection change as the
  first of its steps by version.

### Seed

### Questionnaire

### Update notes

- A MAJOR release: the required checks are renamed. `frontend`, `documents` and `stories`
  now report as `ci / frontend`, `ci / documents` and `ci / stories`. After
  `copier update`, change the branch protection on `main` to the new names, in the
  repository settings or with `gh api`; until then the old names never report and every
  pull request waits on them.
- No file is removed. A game that edited one of the three workflows resolves the markers
  against the callers; a step it added to a job has no place in a caller and moves to a
  workflow file of the game's own.

## [0.1.0] - 2026-09-14

### Managed

- Configs and the `Justfile` (21): `.editorconfig`, `.gitattributes`, `.gitignore`,
  `.markdownlint-cli2.jsonc`, `.npmrc`, `.pre-commit-config.yaml`, `.pre-commit-fix.yaml`,
  `.prettierignore`, `.prettierrc.json`, `.python-version`, `chromatic.config.json`,
  `eslint.config.js`, `lychee.toml`, `package.json`, `pyproject.toml`, `svelte.config.js`,
  `tsconfig.json`, `vite.config.ts`, `vitest.config.ts`, `vitest.storybook.config.ts` and
  `Justfile`. `package.json` pins `@steven-cutting/biscuit-games` at exactly `1.1.0`, the
  version `hub_package_version` names and the first release whose `Wordmark` takes
  `product`. `.prettierignore` lists `.copier-answers.yml`, which Copier rewrites on every
  update.
- Scripts (8): `scripts/check_playwright_browsers.js`, `scripts/initialize.sh`,
  `scripts/install_allium.py`, `scripts/run_allium.py`, `scripts/run_project_check.py`,
  `scripts/run_ripsecrets_redacted.py`, and the two validators, `scripts/validate_docs.py`
  and `scripts/validate_agents.py`.
- Workflows and the Copilot adapter (4): `.github/workflows/ci.yml`,
  `.github/workflows/chromatic.yml`, which skips the publish without
  `CHROMATIC_PROJECT_TOKEN`, `.github/workflows/pages.yml`, which publishes a project
  Pages site with `BASE_PATH` read from the event, and `.github/copilot-instructions.md`.
- The agent contract (27): `AGENTS.md`, `CLAUDE.md`, `.claude/settings.json`, and eight
  skills, `accessibility-review`, `code-review`, `fix-quality`, `plan-change`,
  `project-check`, `review-docs`, `spec-change` and `svelte-change`, each a `SKILL.md`
  under `.agents/skills/` with its two bridges under `.claude/skills/` and
  `.codex/skills/`.
- The handbook with its manifest and map (26): `docs/manifest.yml`, `docs/README.md` and
  24 pages under `docs/project/`, `docs/tutorials/`, `docs/how-to/`, `docs/explanation/`,
  `docs/reference/` and `docs/operations/`, among them the new
  `docs/how-to/update-from-template.md`, which states the seed list, the append convention
  and the update procedure.
- Source and tests (12): `src/app.html`, `src/app.d.ts`, `src/routes/+layout.svelte`,
  `src/routes/+layout.ts`, `src/lib/config.ts` with the six platform figures, the three
  ports `src/lib/ports/storage.ts`, `src/lib/ports/clock.ts` and
  `src/lib/ports/random.ts`, and `tests/setup.ts`, `tests/platform.ts`,
  `tests/platformSpecs.test.ts` and `tests/ports.test.ts`.
- `.storybook/` (2): `.storybook/main.ts` and `.storybook/preview.ts`.
- `static/.nojekyll` (1), empty, so that Pages serves `_app/`.
- 101 managed paths in all, 14 of them expected to be edited by a game (`GAME_EDITED` in
  `tests/inventory.py`).
- `.copier-answers.yml` is Copier's and outside the 101: every update rewrites it, and the
  next update reads it.

### Seed

Rendered once by `copier copy` and never merged, recreated or deleted by an update; the
seed inventory is frozen with this release (`tickets/CONVENTIONS.md` §5), so no later
release adds, renames or retitles a seed page or a numbered decision. The 24 seed files
render under these 14 paths:

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

### Questionnaire

- `game_name`, with no default: 2 to 40 characters including a letter. Refuses control
  characters, braces, surrounding whitespace, a leading `#`, `>`, `-`, `+`, `*`, `_`, `~`,
  backtick or list number, `<`, square brackets, a web or email address, and a trailing
  `#`, `.`, `,`, `;`, `:`, `!`, `。`, `，`, `；`, `：` or `！`.
- `game_slug`, defaulting to `game_name` lowercased, each run of other characters made one
  underscore and leading digits dropped: lowercase letters and digits in words joined by
  single underscores, starting with a letter.
- `description`, with no default: 10 to 200 characters. Refuses control characters,
  braces, surrounding whitespace, a leading `#`, `>`, `-`, `+`, `*`, `_`, `~`, backtick or
  list number, `<`, square brackets, and a web or email address.
- `repository`, defaulting to `steven-cutting/<game_slug>`: `owner/name`, where the owner
  is a GitHub account name of letters, digits and hyphens with no leading, trailing or
  doubled hyphen, and the name is letters, digits, dots, hyphens and underscores, neither
  `.` nor `..` and not ending in `.git`.
- Computed and never asked, each `when: false`: `repository_owner`, `repository_name`,
  `base_path`, `repository_url`, `pages_url`, `game_lockup`, `game_name_escaped`,
  `game_title_ts`, `game_lockup_ts`, `description_ts`, `hub_scope`, `hub_package`,
  `hub_package_version` (`1.1.0`) and `template_url`.
- `_min_copier_version` is `9.18.2`: an older copier is refused.

### Update notes

- The first release, so there is nothing to update from. A game rendered from `v0.1.0`
  records `_commit: v0.1.0` in `.copier-answers.yml` and takes later releases with
  `uvx copier update --skip-answered`.

[Unreleased]: https://github.com/steven-cutting/biscuit_games_template/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/steven-cutting/biscuit_games_template/releases/tag/v0.1.0
