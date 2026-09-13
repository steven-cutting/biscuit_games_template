---
id: T07
title: "Handbook A: project, tutorial and how-to pages, and the three seed root files"
status: done
depends_on: [T00]
parallel_with: [T01, T02, T03, T04, T05, T06, T08, T09]
branch: ticket/t07-handbook-a
estimated_size: L
---

# T07: Handbook A: project, tutorial and how-to pages, and the three seed root files

## Context

T00 has merged to `main`. It shipped every path of the template tree, and for the
handbook that means a stub for each page: valid frontmatter equal to its
`template/docs/manifest.yml` entry, an H1 equal to the title, forty or more words of
prose, and no links. This ticket replaces the stubs for rows 2 to 13 of the handbook
table in CONVENTIONS.md §8 (the project pages, the tutorial and the how-to pages) and
writes the three seed root files (`README.md`, `CHANGELOG.md`, `SECURITY.md`) in final
form. T08 does the same for rows 14 to 27 and T09 for the decisions; all three run in
parallel with the other lanes and wait for nothing but T00. T10 waits for all of them.

The rendered pages are read by the game's maintainers and agents, offline, in every game
the template renders. Managed pages therefore say "this game" and never a name; the seed
pages and the two URL-bearing pages are the only ones that substitute an answer
(CONVENTIONS.md §4, the rule after the tree). Read, in this order:

1. CONVENTIONS.md §0 (the sources and their commits), §3 (the answer names a `.jinja`
   file may use), §4 and §5 (managed versus seed), §6 (Jinja rules), §8 (the handbook
   table and the two layouts T00 followed), §10 (what the update page must say), §11 and
   §13.
2. `template/docs/manifest.yml` and `template/docs/README.md.jinja` as T00 wrote them: the
   manifest is the authority for every page's frontmatter and title, and the map is where
   every page must be reachable from.
3. `tests/test_render.py` as T00 wrote it: `test_managed_pages_link_only_to_stable_pages`
   (the exact set of paths a managed page may link to), `test_no_poodl_outside_provenance`
   (the forbidden tokens and the allowlist) and
   `test_rendered_jinja_files_carry_no_delimiter`.
4. `/Users/scutting/projects/biscuit_games/scripts/validate_docs.py` (the hub's, which the
   render ships): `BAD_CONTENT` at lines 36-43, `MINIMUM_WORDS = 40` at line 32,
   `_check_page` at lines 191-220 and `_check_links` at lines 222-246.
5. The Poodl source of each page, named in its subsection below, under
   `/Users/scutting/projects/poodl` at commit `0a46a485`. Every line number below was
   verified against that commit; re-check any line you edit with `sed -n 'A,Bp'`.

## Goal

Fifteen files under `template/`, each in final form, such that a render with the default
answers passes `validate_docs.py`, markdownlint, typos and lychee offline, links from
managed pages resolve only to managed pages and carried decisions, no rendered text
carries a forbidden token, and every page reads as the rendered game's rather than
Poodl's. `docs/how-to/update-from-template.md` is new and states everything
CONVENTIONS.md §10 lists. `just test` is green in the template repository.

## Non-goals

- `template/docs/manifest.yml` and `template/docs/README.md.jinja` (T00). A page rename,
  a retitle, a new page or a missing map link is handed back as a T00 follow-up on `main`;
  this ticket never edits them.
- Rows 14 to 27 (T08) and rows 28 to 38 (T09), including the decision records this
  ticket links to. Link to the rendered decision names T00's manifest declares; do not
  touch the files.
- `template/AGENTS.md.jinja` and the skills (T04), `template/pyproject.toml.jinja` and
  the other configs (T01), `tests/inventory.py` and `copier.yml` (never a lane's).
- Changing what the validators accept (T02 ships them; a rule change goes back through
  CONVENTIONS.md).

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `template/README.md.jinja` | S | `P README.md` | Rewritten to the shape below; `game_name`, `description`, `pages_url`, `base_path` |
| `template/CHANGELOG.md.jinja` | S | `P CHANGELOG.md` lines 1-8 and 400 | Keep a Changelog skeleton; `repository_url` |
| `template/SECURITY.md` | S | `P SECURITY.md` | P minus lines 28-32, plus the private-reporting fallback paragraph |
| `template/docs/project/purpose-and-scope.md.jinja` | S | `P docs/project/purpose-and-scope.md` (shape) | Rewritten from `game_name` and `description` |
| `template/docs/project/terminology.md.jinja` | S | `P docs/project/terminology.md` | Repository table kept and edited; game table two rows (tier B) |
| `template/docs/project/repository-map.md` | M | `P docs/project/repository-map.md` | Tree and table trimmed to what ships |
| `template/docs/project/platform.md` | M | `P docs/project/platform.md` | Generic; no literal version; sixteen-row table kept |
| `template/docs/tutorials/first-change.md` | M | `P docs/tutorials/first-change.md` | Steps 2 to 5 around the seed files |
| `template/docs/how-to/develop-locally.md` | M | `P docs/how-to/develop-locally.md` | Base path generic; staging dropped |
| `template/docs/how-to/test-and-debug.md` | M | `P docs/how-to/test-and-debug.md` | Four lines made generic (tier B) |
| `template/docs/how-to/work-in-the-component-workshop.md` | M | `P docs/how-to/work-in-the-component-workshop.md` | Seed story example; renumbered decision links |
| `template/docs/how-to/work-with-the-specs.md` | M | `P docs/how-to/work-with-the-specs.md` | One-row module table; waiver history condensed |
| `template/docs/how-to/maintain-dependencies.md` | M | `P docs/how-to/maintain-dependencies.md` | Template-update section added; no version on the platform page |
| `template/docs/how-to/deploy-to-github-pages.md.jinja` | M | `P docs/how-to/deploy-to-github-pages.md` (steps 1-2, rolling back) | Project site; `pages_url`, `base_path`, `repository` |
| `template/docs/how-to/update-from-template.md.jinja` | M | `foo/www template/docs/how-to/update-from-template.md.jinja` (shape only) | New; exact content below; `_copier_answers._commit`, `template_url` |

## Steps

### 1. Rules every file below satisfies

1. **Frontmatter** is the six-line block P's pages carry (`title` and `kind` quoted, the
   three lists unquoted), and each of the five values equals the page's entry in
   `template/docs/manifest.yml`. Copy the block from the T00 stub, which already agrees,
   and never change it. The H1 equals `title` exactly.
2. **Forty or more words** after the frontmatter, counted after stripping Markdown
   punctuation (`_check_page`). No page below is near the floor; the stubs are.
3. **No delimiter after rendering.** `BAD_CONTENT["unresolved template syntax"]` refuses
   the three two-character Jinja openers anywhere in a rendered page, so a `.jinja` page
   uses them only where an answer is substituted, and `update-from-template.md.jinja`
   describes Jinja and the answers file in words. A page without the `.jinja` suffix
   contains none at all.
4. **None of the three unfinished-marker words** `BAD_CONTENT` names at line 41, and no
   placeholder prose (line 42). A page that has nothing to say yet says so in real
   sentences, as the seed pages below do.
5. **Answers.** Only `.jinja` files substitute, and only the names CONVENTIONS.md §3
   defines, with `_copier_answers._commit` guarded by `default` in the one managed page
   that renders it. **A seed `.jinja` file never renders `_copier_answers._commit`**: an
   update never touches a seed, and T10's `test_pristine_update_equals_fresh_render`
   compares an updated tree with a fresh render, which a seed carrying the old version
   would fail.
6. **Links.** Relative, exact-case, to a page that exists in the render, never to a
   `.jinja` name. A managed page links only to managed pages and to decisions (the set
   `tests/test_render.py` permits; read it first), so no managed page links to
   `project/purpose-and-scope.md`, `project/terminology.md`, `README.md`, a spec module or
   a seed source file: write those as code spans. No page links to a Poodl-only path
   (`how-to/replace-the-word-lists.md`, a decision by its Poodl number, `site-root/`).
   Decision links use the template's numbers: P `0006` is `0005-component-workshop.md`,
   P `0008` is `0006-visual-review-in-chromatic.md`, P `0011` is
   `0007-project-managed-allium-cli.md`, P `0013` is `0008-design-system-as-a-package.md`,
   and the two new ones are `0009-rendered-from-the-template.md` and
   `0010-a-project-pages-site.md`. Link text is the manifest title.
7. **Forbidden tokens** (`test_no_poodl_outside_provenance`): case-insensitive `poodl`
   only in `docs/project/platform.md` (its two hub URLs), and nowhere `pnut`,
   `site-root`, `stage_site`, `stage-preview`, `word list`, `word-list`, `words.allium`,
   `daily.allium`, `sharing.allium`, `statistics.allium`, `foo/www`, `/Users/`. The lines
   in each P source that carry one are listed in its subsection; every one goes.
8. **Files that do not ship** are never named as if they existed: `tests/contrast.test.ts`,
   `tests/scoring.test.ts`, `tests/components.test.ts`, `src/lib/domain/`, `src/lib/app/`,
   `src/lib/data/`, `Countdown.svelte`, `Board.svelte`, `docs/specs/game.allium`. What
   ships is CONVENTIONS.md §4; the seed files a tutorial can point at are
   `src/lib/brand.ts`, `src/lib/components/Lockup.svelte`, `src/routes/+page.svelte`,
   `stories/Lockup.stories.svelte`, `tests/lockup.test.ts`, `tests/route.test.ts`,
   `tests/restated.ts` and the one module under `docs/specs/`.
9. **Wrapping and style** as P's pages: prose wrapped by hand near 90 columns, `console`
   fences for commands, `text` for file content, one `## Related pages` list at the end.
   The embedded pages below use `~~~` fences only so that this ticket can enclose them;
   write every one of them as a triple-backtick fence in the page.

### 2. The three seed root files

**`template/README.md.jinja`.** Poodl's shape (`P README.md`, 74 lines) minus the modes
and status paragraph (lines 11-15), the address (line 6) and the `domain/` line (45).
Exact content:

````markdown
# {{ game_name }}

{{ description | trim }}

**Play it at <{{ pages_url }}>.**

{{ game_name }} is a Biscuit Games game: a single-page static site with no backend, no
accounts and no telemetry. It runs entirely in the browser and is published to GitHub
Pages as a project site beneath `{{ base_path }}/`. Every rule comes from the
specifications in `docs/specs/`.

## Quick start

~~~console
just initialize
just dev
~~~

`just initialize` creates both lockfiles, installs both toolchains, downloads the browser
the story gate needs, normalises formatting and installs the pre-commit hook. It never
stages, commits, tags or pushes.

It also installs the design system from GitHub Packages, which needs a token carrying
`read:packages` in `~/.npmrc` first — [Develop locally](docs/how-to/develop-locally.md) has
the line.

## Check your work

~~~console
just fix      # the only command that modifies files
just check    # every gate, read-only, proving the worktree is unchanged
~~~

`just --list` prints every recipe. Each one is described in
[Commands](docs/reference/commands.md).

## Layout

~~~text
src/lib/brand.ts     The one place this game's name is written
src/lib/ports/       Every side effect, each with an in-memory fake
src/lib/components/  Svelte 5 components, runes only
src/routes/          Prerendered routes
tests/               Vitest suites, never colocated
stories/             Svelte CSF stories, one per component
docs/                The handbook
docs/specs/          Allium specifications — the source of truth for behaviour
~~~

## Documentation

Start at [the documentation map](docs/README.md).

- [Purpose and scope](docs/project/purpose-and-scope.md) — what {{ game_name }} is, and is not
- [Make your first change](docs/tutorials/first-change.md) — clone to green gate
- [Architecture](docs/explanation/architecture.md) — how a site with no server fits together
- [Specifications](docs/explanation/specifications.md) — why behaviour is written down first

Engineering conventions and the agent working agreement are in [AGENTS.md](AGENTS.md).

## Boundaries

Behaviour is decided in `docs/specs/`, not in code. When the two disagree, the
specification is right and the code is a defect. Changing what the game does means
changing a specification first.

Whatever this game remembers lives in one browser on one device and is never uploaded.
Clearing browser data destroys it. See
[Security model](docs/explanation/security-model.md).

This repository was rendered from the Biscuit Games template. The toolchain, the
handbook's managed pages and the agent contract arrive from it by `copier update`, and
[Update from the template](docs/how-to/update-from-template.md) says which files are this
game's alone.
````

**`template/CHANGELOG.md.jinja`.** `P CHANGELOG.md` lines 1-8 verbatim, one `### Added`
bullet, and line 400 with the answer:

````markdown
# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- The repository, rendered from the Biscuit Games template: the toolchain, the hook gate,
  the handbook, the agent contract, the three workflows, and a page that carries the
  platform's header with this game's lockup and nothing to play yet. `AGENTS.md` records
  the template version under Provenance.

[Unreleased]: {{ repository_url }}/commits/main/
````

**`template/SECURITY.md`.** `P SECURITY.md` verbatim minus lines 28-32, which hold the
two game-specific out-of-scope bullets (reading the answer; decoding a custom-game link,
whose third line is the decision link). Lines 33-34 stay. Lines 44-46 remain true of the
rendered workflows (`packages: read` on the install job, write scopes only in
`pages.yml`); leave them. Not a `.jinja` file: it says "this repository".

One paragraph is added, the file's only addition to P. P's reporting section names
GitHub's private vulnerability reporting and nothing else, and GitHub offers that form on
public repositories: the endpoint answers `404 Not Found` on a private one
(`tickets/C03-repository-bootstrap.md` lines 64-66). A game may be rendered into a
private repository, and `SECURITY.md` is a seed, so a later template fix would never
reach it. Insert this after P line 7 (the "do not open a public issue" sentence) and
before the "Include what you did" paragraph, wrapped as P wraps:

````markdown
GitHub offers that form on public repositories. While this repository is private, only
people its owner has added can see it at all, so report to the owner directly instead —
the account named in this repository's address. Do not open an issue.
````

### 3. The two seed handbook pages

**`template/docs/project/purpose-and-scope.md.jinja`.** Shape of `P` lines 1-9, 21, 40,
53, 59-63; everything between is new. Exact content after the frontmatter block (copy the
block from the stub):

````markdown
# Purpose and scope

{{ game_name }} is a Biscuit Games game: {{ description | trim | trim('.') }}. It runs
entirely in the browser as a static site: there is no server, no account and no database,
and the platform package `@steven-cutting/biscuit-games` supplies the look, the shared
components and the cell and key a play surface is built from, so what this repository
decides is the game.

## What it does

Today, nothing yet: the page carries the platform's header with this game's lockup and an
empty main landmark. What the game will do is stated first in `docs/specs/`, one rule at a
time, and built second; see [Specifications](../explanation/specifications.md). Rewrite
this section as the rules arrive, and keep it to what a player would notice.

## What it deliberately does not do

- **No accounts, no sync.** Whatever the game remembers belongs to one browser on one
  device. Clearing browser data clears it, and nothing can restore it.
- **No server.** Nothing is uploaded, and nothing is recorded anywhere but the device.
- **No analytics or telemetry.** See [Security model](../explanation/security-model.md).

## Who it is for

A single player, on their own device. Everything else follows from that, and this section
is the game's to rewrite when it knows more.

## Related pages

- [Repository map](repository-map.md)
- [Terminology](terminology.md)
- [Architecture](../explanation/architecture.md)
````

**`template/docs/project/terminology.md.jinja`** (tier B). `P docs/project/terminology.md`
lines 1-13 verbatim; replace lines 14-41 (the game and mode tables) with one `## The game`
section holding the sentence "Two rows to start with; the game adds a row for every term
its specification names." and a two-row table:

```markdown
| Term | Meaning |
| --- | --- |
| Player | Whoever is at the device. One at a time, and nothing here knows of a second. |
| Play surface | Where {{ game_name }} is played: the platform's cells and keys in an arrangement this game decides. `Play` is its name in the root module. |
```

Keep lines 43-56 (`## The repository`) with three rows edited: line 50 `Six are in` →
`Three are in`; line 51 `everything Poodl would share with a second game` →
`everything {{ game_name }} would share with another game`; line 52 → `The platform's
name for a mark that is wholly right, after the token that paints it. A game whose rules
use another word translates it where a mark reaches something rendered.` Keep lines 57-60.

### 4. The managed project pages

**`template/docs/project/repository-map.md`** (`P docs/project/repository-map.md`, 65
lines). Tree at lines 14-39: delete lines 24 (`app/`), 27 (`data/`, a forbidden token), 28
(`domain/`, not shipped) and 34 (`site-root/`); after line 20 add
`├── .copier-answers.yml  What the template was told; read by copier update`; after line
23 add `│   │   ├── brand.ts     The one place this game's name is written`; line 32 →
`Svelte CSF stories, one per component`; line 35 → `The repository checkers, the
installers and the preflight`. Table at lines 43-56: delete rows 45, 46, 50 and 53; row
54 lists exactly the eight shipped scripts (`validate_docs.py`, `validate_agents.py`,
`run_project_check.py`, `run_ripsecrets_redacted.py`, `install_allium.py`,
`run_allium.py`, `check_playwright_browsers.js`, `initialize.sh`); add after row 47 a row
`` `src/lib/brand.ts` `` ("The one place this game's name is written; every component,
story and test reads it from here.") and a row `` `src/lib/` (the rest) `` ("Pure behaviour
this game adds, in directories of its own beside these. Given the same input it returns
the same output, always."). Keep lines 58-59. Related pages: delete line 63 (a seed page);
keep 64-65.

**`template/docs/project/platform.md`** (`P docs/project/platform.md`, 106 lines). Lines
carrying `poodl` or `word list`: 11, 17, 24, 26, 30, 48, 70, 76, 78, 86. Edits:

- 11: `Poodl is one game` → `This game is one game`. 17: `what is Poodl's` → `what is
  this game's`.
- 24-27 → `This game decides its own rules and the specifications that state them; how its
  play surface is arranged; what a mark means and the words it says about one; its data;
  and its address. A component that encodes a rule or draws this game's own data stays
  here for that reason.` 30: `six rows of five is Poodl` → `how many of them, and in what
  arrangement, is this game's`.
- 34: `at **1.0.0**, pinned exactly` → ``at the version `package.json` pins, exactly``
  (CONVENTIONS.md §13: no literal version on this page). 41-43: end the sentence at
  ``under `node_modules/@steven-cutting/biscuit-games/`, which is where the
  specifications `tests/platformSpecs.test.ts` reads actually live.``
- 48-51 → ``So a game restates the clauses it needs and a test holds the restatements to
  the platform's text. This game starts by restating none: `tests/restated.ts` is the
  table a restated clause is entered in, and the six figures both sides declare — two
  contrast ratios, the touch target, the narrowest width and the two separations — are
  held equal across the shipped modules, `src/lib/config.ts` and the root module under
  `docs/specs/` by `tests/platformSpecs.test.ts`. It is deliberately
  over-sensitive`` and continue with line 52 from `— a reworded comma`.
- Table 67-82: all sixteen rows and their URLs stay (two URLs carry `poodl`, which is
  what the allowlist is for). 70: `the stylesheet Poodl wears` → `this game wears`. 74 →
  `The procedure a game follows to install the package; this one was rendered with it
  done.` 76 → `The ledger the first game worked through when it took the package, and
  what it still records.` 77: `the four below` → `the five below`.
- 84-87 → ``The platform's and this game's records are numbered independently, so a bare
  number means nothing without the repository. The ones above are all the platform's;
  this game's are indexed in `docs/decisions/README.md`.`` (a code span, not a link:
  the index is a seed).
- Related pages: line 102 → the link to `../decisions/0008-design-system-as-a-package.md`
  with the manifest title as text; delete line 103; keep 104-106.

### 5. The tutorial

**`template/docs/tutorials/first-change.md`** (`P docs/tutorials/first-change.md`, 89
lines; the only `poodl` is line 60; there is no base-path line to drop). Edits:

- 35-36 → ``Open the address it prints. You will see the platform's header carrying this
  game's lockup, and a main landmark with one sentence in it. The lockup's words come from
  `src/lib/brand.ts`, the one place the game's name is written.``
- 40-43 (step 3) → ``Open the one module under `docs/specs/`, named after this game's
  slug, and find the `Play` surface and its guarantee. The `config` block above it
  restates six figures the platform states, and `src/lib/config.ts` mirrors them;
  `tests/platformSpecs.test.ts` holds the three equal, so a figure changed in one
  place and not the others fails the gate rather than drifting.``
- 47-48 (step 4) → ``Decide what the main landmark should say instead of its placeholder
  sentence. Add a case to `tests/route.test.ts` that queries the `main` landmark
  by role and asserts the new words, then run the suite and watch it fail — which is the
  point.`` Keep the `console` block at 50-52. 54-55 → `A test that is green before you
  have changed anything is either already covered or vacuous.`
- 59-64 (step 5) → ``Change the sentence in `src/routes/+page.svelte`, run the suite
  again, and land the component change and the assertion in the same commit. Pick
  something this game owns: the cells, the keys and the primitives are the platform's,
  and their wording is amended upstream rather than here. The rule holds for every later
  change: a component change and its Testing Library assertion land together, and the
  assertion queries by accessible role and name.``
- 82-83 → `A specification you read, a test, a component, and the gate. That is the whole
  loop; every change after this one is the same shape, and the first real one starts by
  adding a rule to the module rather than reading it.`

### 6. The how-to pages

**`template/docs/how-to/develop-locally.md`** (`P docs/how-to/develop-locally.md`, 119
lines; `poodl` at 26, 79, 84, 85, 92; staging at 92-93). Keep lines 32-40 as they are: the
`<your token>` placeholder is deliberate, and line 36-40 says why. 26: `Poodl takes` →
`This game takes`. 79-86 → ``To reproduce the published site exactly, set the base path the
project site is served under — the repository's name, which `pages.yml` reads from the
event — on both commands, for the reason [Configuration](../reference/configuration.md)
gives:`` followed by a `console` block of `BASE_PATH=/<repository name> just frontend-build`
and `BASE_PATH=/<repository name> just preview`. Delete lines 88-94. Keep 96-119.

**`template/docs/how-to/test-and-debug.md`** (tier B; `P docs/how-to/test-and-debug.md`,
75 lines). Four edits: 23-24 → `npx vitest tests/lockup.test.ts` and
`npx vitest --watch tests/ports.test.ts`; 37-38 → ``If the expectation is about a rule,
work it through by hand against the module under `docs/specs/` that states it. The
specification is the arbiter, not the current code.``; 59-60 → the two
`BASE_PATH=/<repository name>` commands as above. Everything else verbatim.

**`template/docs/how-to/work-in-the-component-workshop.md`**
(`P docs/how-to/work-in-the-component-workshop.md`, 201 lines; `poodl` at 56, 57, 72, 74,
129). Edits:

- 14: link to `../decisions/0005-component-workshop.md`, text `Decision 0005`.
- 56-57 → `components — and the token sheet the platform keeps — appear under **Biscuit
  Games** in the sidebar, collapsed, below this game's own.` (keep `They are served ...`).
- 72-76 → `Every file here covers one component this game owns. The design tokens have a
  specimen sheet of their own, and it is the platform's rather than this repository's —
  the tokens are consumed by every component and owned by none of them. What each pair of
  them measures is held by the platform's own test, not by one here.`
- 84-98: the story example becomes the seed lockup, which takes no props (P's seed story
  title is `Brand/Lockup`, `P stories/Lockup.stories.svelte:30`):

  ```svelte
  <script module lang="ts">
    import { defineMeta } from '@storybook/addon-svelte-csf';

    import Lockup from '../src/lib/components/Lockup.svelte';

    const { Story } = defineMeta({ title: 'Brand/Lockup', component: Lockup, tags: ['autodocs'] });
  </script>

  <!-- The comment above a story becomes its description on the docs page. -->
  <Story name="Beside the platform's words" />
  ```

- 129: `and Poodl has no animation yet` → `and a fresh game has none`.
- 151: `a tile's marker bar is not checked by the contrast rule at all` → `the monogram
  beside the lockup's words is not checked by the contrast rule at all`.
- 162: link to `../decisions/0006-visual-review-in-chromatic.md`, text `Decision 0006`.
- 200-201: the same two decision links with their manifest titles as text.

**`template/docs/how-to/work-with-the-specs.md`** (`P docs/how-to/work-with-the-specs.md`,
150 lines; forbidden tokens at 18, 21, 22, 23, 46, 110). Edits:

- 11-12 → ``The Allium modules under `docs/specs/` decide what the game does; a fresh
  game has one, the root module named after its slug. This page is the procedure;
  [Specifications](../explanation/specifications.md) is the reasoning.``
- 16-23: a one-row table, no link (the module is a seed): `` `<slug>.allium`, the root
  module `` in the first column and ``The six figures the platform also states, and the
  `Play` surface with its one guarantee. Every module the game adds imports this one.``
  in the second. Keep 25-26.
- 32 → ``Check the modules that depend on it. A module others import is depended on by
  each of them, so a change to a trigger or an entity ripples, and a restated platform
  clause is held to the platform's text by `tests/platformSpecs.test.ts`.``
- 44-47 → ``An `open question` block records a product decision nobody has made yet, so
  the gap is visible rather than silently filled in. A fresh game has none; treat a low
  count as the settled state, not as a reason to stop adding them.``
- 60 and 77: link to `../decisions/0007-project-managed-allium-cli.md`, text
  `decision 0007`.
- 54-104 otherwise verbatim (the tooling section, the waiver terms, and the sentence
  ending `No waiver is currently in the modules.` at 104; drop the rest of 105-107).
- 105-144 are Poodl's history and name a forbidden module; replace them with three short
  paragraphs that keep the transferable lessons: (a) where prose can carry what the
  checker cannot resolve — a `related:` clause naming a surface through a module alias —
  the honest form is prose, and a waiver that would assert the checker is wrong is not
  written; (b) `allium.field.unused` counts uses within one module only, so a definition
  whose readers sit in another module is reported; read it twice before waiving, because
  the diagnostic can be wrong about the language and still right that the declaring
  module has something true to say about the field; (c) a `.created(...)` call is seen
  only when it stands alone as an ensures statement, so create unbound and let a
  `.created` rule pick the entity up; and 3.6.1 resolves `alias/config.field` without
  checking the name behind the dot, so a cross-module config reference is read by eye,
  while a local one is reported from a derived value, a rule or a module-level invariant
  but not from inside an entity-level `invariant` block. Keep the sentence that every
  waiver was verified against 3.6.1 and is re-verified when the pin moves.
- Related pages: keep 148 and 150; delete 149 (a seed page).

**`template/docs/how-to/maintain-dependencies.md`**
(`P docs/how-to/maintain-dependencies.md`, 149 lines; `poodl` at 60, 84). Line 26 stays
true: the shipped `Justfile` keeps P's `lock-check` recipe (`P Justfile:30-32`). Edits:

- 60: `the stylesheet Poodl wears` → `the stylesheet this game wears`.
- 76-80 → ``Run `just frontend-coverage` before anything else. One gate fails by design
  here: `tests/platformSpecs.test.ts`, on a figure whose value moved or a restated
  clause whose wording did. Each failure is the moment somebody decides whether the
  platform's meaning moved — a reworded clause is amended upstream and taken, never
  reworded here.``
- 81-82 → ``Add a `CHANGELOG.md` entry naming what a reader would see; `package.json`
  is the one place the installed version is stated.``
- 84: `Poodl's own stories` → `this game's own stories`. 86-87 stay until C04.
- 94: link to `../decisions/0007-project-managed-allium-cli.md`, text `decision 0007`.
- Insert before line 134 a section `## Take a template update`: ``The pins above move
  through the template too. `copier update` carries a changed pin into
  `package.json` or `pyproject.toml` as an ordinary hunk, which is why the game
  commits its lockfiles and relocks after an update;
  [Update from the template](update-from-template.md) is the procedure.``

**`template/docs/how-to/deploy-to-github-pages.md.jinja`**
(`P docs/how-to/deploy-to-github-pages.md`, 150 lines). Kept verbatim: one-time setup
steps 1-2 (22-25) and the paragraph at 29-31, the concurrency sentence (82-83), the
rolling-back paragraph (138-140). Dropped: DNS (26-27, 45-66), the domain (33-43), staging
(73-77, 85-110), the old address (112-134), 142-143, and every decision 0009 link. Exact
content after the frontmatter block:

````markdown
# Deploy to GitHub Pages

This game publishes to GitHub Pages from `.github/workflows/pages.yml` on every push to
`main`. The workflow builds the static site and hands `build/` to the Pages deployment
action; nothing is committed to a branch.

The site is a project site, served at <{{ pages_url }}>: the repository
`{{ repository }}`, beneath `{{ base_path }}/` on its owner's Pages host.

## One-time setup

A rendered repository starts from nothing, so both steps are done once, before the first
push that should deploy.

1. In the repository settings, under Pages, set the source to **GitHub Actions**. The
   workflow cannot do this for itself.
2. Confirm the `github-pages` environment exists. The deploy job references it, and GitHub
   creates it on the first run.

Until step 1 is done, the build job succeeds and uploads its artefact but the deploy job
fails with `Failed to create deployment (status: 404)`, even though the workflow itself is
correct.

## Where the site is served from

A project site lives beneath the repository's name on the owner's Pages host, so the app is
built to live under `{{ base_path }}`. The workflow reads that name from the event that
triggered it rather than carrying it in the file, which keeps `pages.yml` the same in every
game and keeps `paths.base` in `svelte.config.js` from drifting away from the address Pages
serves. A custom domain is a later change to the repository settings and to nothing here;
[decision 0010](../decisions/0010-a-project-pages-site.md) records why the project site is
the starting point.

## What the workflow does

- Sets `BASE_PATH` from the repository name in the event, in the workflow's own `env`
  block, so the build cannot drift from where Pages serves it.
- Builds with `npm run build`, which is `just frontend-build`.
- Uploads `build/` as the Pages artefact. `static/.nojekyll` rides along so Pages serves
  the underscore-prefixed `_app/` directory rather than treating it as a Jekyll internal.
- Deploys it in a second job that holds the `pages: write` and `id-token: write` scopes.
  The job that builds holds `contents: read` and `packages: read` and neither publishing
  scope, so the credential that installs and the credential that deploys never meet.

Deployments are serialised by a concurrency group and are never cancelled mid-flight: a
half-published site is worse than a slightly stale one.

## Reproduce a deployment locally

~~~console
BASE_PATH={{ base_path }} just frontend-build
BASE_PATH={{ base_path }} just preview
~~~

The base path goes on both commands, so the preview sits where Pages serves. See
[Configuration](../reference/configuration.md).

## Rolling back

Re-run the last good deployment from the Actions tab, or revert the commit and let the push
trigger a fresh build. There is no state to migrate and no cache to clear beyond the
browser's.

## Related pages

- [Decision 0010: A project Pages site](../decisions/0010-a-project-pages-site.md)
- [Architecture](../explanation/architecture.md)
- [Configuration](../reference/configuration.md)
- [Maintenance](../operations/maintenance.md)
````

Use the manifest's title for decision 0010 as the last link's text.

**`template/docs/how-to/update-from-template.md.jinja`.** New. Its manifest entry (T00
wrote it; verify) is title `Update from the template`, kind `how-to`, audience
`[maintainer, agent]`, `canonical_for: [template_update_procedure]`, `requires: []`; write
the frontmatter in P's six-line form. The seed list is `copier.yml`'s fourteen lines,
verbatim, leading slashes included. Exact content after the frontmatter block:

````markdown
# Update from the template

This game was rendered by Copier from the Biscuit Games template,
<{{ template_url }}>, at template version
`{{ _copier_answers._commit | default('an untagged commit') }}`. The answers the
questionnaire took are recorded in `.copier-answers.yml`, and that file is what makes a
later update possible: `copier update` reads it, renders the template again at a newer
version, and merges what changed between the two renders into this repository. In the
template's own tree a file carries a `.jinja` suffix where an answer is substituted into
it; the files rendered here carry no such syntax.

## What an update touches, and what it never does

Every file the template renders is one of two kinds.

**Seed files are this game's.** The template writes them once, on the first render, and an
update never merges, recreates or deletes one: rewrite them freely, and one you delete
stays deleted. `copier.yml` lists them, and the list is frozen — after the template's first
release it never adds, renames or retitles a seed page or a numbered decision, because
`docs/manifest.yml` and `docs/README.md` re-render on every update while seeds do not.

~~~text
/README.md
/CHANGELOG.md
/SECURITY.md
/docs/project/purpose-and-scope.md
/docs/project/terminology.md
/docs/decisions/
/docs/specs/
/src/lib/brand.ts
/src/lib/components/
/src/routes/+page.svelte
/stories/
/tests/restated.ts
/tests/lockup.test.ts
/tests/route.test.ts
~~~

**Managed files are the template's**, and an update is a three-way merge onto each: a
change the template made arrives as a hunk, an edit this game made is kept where the
template left that hunk alone, and where both sides changed the same lines Copier writes
markers. A managed file this game deleted stays deleted. A managed file the template stops
rendering is removed from this game even where it was edited; the template's changelog
announces every such removal under "Update notes".

Some managed files are expected to be edited here, and a convention keeps the two sides in
different hunks: the template inserts into the upper blocks, and this game appends at the
end. `docs/manifest.yml` takes game pages after the last decision entry; `docs/README.md`
takes them under "This game"; `AGENTS.md` takes deviations at the end of Provenance; the
`Justfile`, `package.json`, `eslint.config.js`, `.gitignore` and `src/lib/config.ts` take
additions at the end of the relevant block. Reordering any of these is what brings the
markers back.

## Take an update

1. Commit everything. Copier refuses a dirty worktree.
2. Run the update. The template declares no tasks, so no trust flag is passed:

   ~~~console
   uvx copier update --skip-answered
   ~~~

   That takes the template's latest release tag. Add `--vcs-ref=vX.Y.Z` to pick one, or
   `--vcs-ref=HEAD` for the tip; a prerelease tag is skipped unless `--prereleases` is
   given. Add `--conflict rej` to have conflicts written as `.rej` files beside the
   originals instead of inline markers.
3. Resolve every marker. They read `<<<<<<< before updating` and `>>>>>>> after
   updating`; the template's side is a suggestion, and this game's behaviour wins where
   the two genuinely disagree. The hook gate refuses a commit that still carries one.
4. Regenerate what is generated, repair formatting, and run the whole gate:

   ~~~console
   just lock
   just fix
   just check
   ~~~

   `just lock` relocks both lockfiles against the manifests the update may have moved;
   read the lockfile diff before accepting it.
5. Commit the result as one change, `.copier-answers.yml` included. Copier rewrites that
   file on every update, and the next update reads it.

Never edit `.copier-answers.yml` by hand, with one exception: `_src_path`, when a game
rendered from a local clone moves to the template's GitHub address.

## Change an answer

Run `uvx copier update` without `--skip-answered`. Copier asks the questionnaire again with
the recorded answers as defaults, and the change lands as an update. Only the four
questions are asked; everything else is computed from them.

## Reset a managed file

`uvx copier recopy --skip-answered` renders the template again over this repository with
no merge. Seed files are skipped; every other file is overwritten, so commit first and
read the diff.

## When this game and the template disagree

A departure that suits only this game is recorded under "Deliberate deviations" in
`AGENTS.md`, and the file that carries it is edited here. A departure that would suit
every game is made in the template instead, and arrives by the next update.

## Steps by version

A template release that asks something of a game beyond resolving markers records it
here, newest first. Nothing yet: the first release asks nothing.

## Related pages

- [Maintain dependencies](maintain-dependencies.md)
- [Documentation contract](../reference/documentation-contract.md)
- [Decision 0009: Rendered from the template](../decisions/0009-rendered-from-the-template.md)
````

Use the manifest's title for decision 0009 as the last link's text. The claim in step 3
that the hook gate refuses a marker rests on `check-merge-conflict` being in the shipped
`.pre-commit-config.yaml`; confirm with `grep -n merge-conflict template/.pre-commit-config.yaml`
and drop the sentence if it is absent.

### 7. If the ticket runs long

Tier B is `terminology.md.jinja` and `test-and-debug.md`, in that order of cutting. To
cut a page is to leave T00's stub in place — it already passes every gate — and to record
in the hand-back notes that the page is carried forward to a follow-up ticket. Nothing
else changes: the manifest entry, the map link and the frontmatter stay as they are.

### 8. Check, commit, hand over

Run the Verification commands below, then commit on the ticket branch, set this ticket's
`status:` to `done`, and fill in the hand-back notes.

**Authorisation required:** pushing the branch and opening the pull request
(CONVENTIONS.md §11). Stop and ask before either.

## Acceptance criteria

- [ ] Every path in Files touched is in final form; nothing outside it changed except this
      ticket's `status:` line.
- [ ] `just test` is green in the template repository, including `tests/test_validators.py`
      and `test_managed_pages_link_only_to_stable_pages`,
      `test_no_poodl_outside_provenance` and `test_rendered_jinja_files_carry_no_delimiter`
      in `tests/test_render.py`.
- [ ] In a render with the default answers, `scripts/validate_docs.py` exits 0 and
      markdownlint reports no error over `docs/`, `README.md`, `SECURITY.md` and
      `CHANGELOG.md`.
- [ ] `template/SECURITY.md` carries the private-reporting fallback paragraph, so the
      policy names a route that exists whether the repository is public or private.
- [ ] The only rendered lines carrying `poodl` (any case) among this ticket's files are the
      two hub URLs in `docs/project/platform.md`; no other forbidden token appears.
- [ ] `docs/project/platform.md` states no literal package version.
- [ ] `docs/how-to/update-from-template.md` carries the fourteen seed paths verbatim, the
      two marker names, `just lock && just fix && just check`, the frozen-inventory rule
      and a "Steps by version" section, and its rendered text has no Jinja delimiter.
- [ ] No managed page links to a seed page, a spec module or a Poodl-only path; every
      decision link uses the template's numbering.
- [ ] `README.md.jinja` and `CHANGELOG.md.jinja` substitute §3 names only, never
      `_copier_answers._commit`.
- [ ] Cut tier-B pages, if any, are named in the hand-back notes.

## Verification

From the repository root. The first block is the fast suite:

```sh
just test
```

Expected: every test passes; none of the four tests named above is skipped or fails.

A render to inspect (the destination is gitignored; the validator runs against the render
it sits in because `ROOT` derives from `__file__`):

```sh
rm -rf ai_tmp/render && just render
uv run --frozen python ai_tmp/render/scripts/validate_docs.py; echo "exit $?"
```

Expected: no output from the validator, then `exit 0`.

```sh
cd ai_tmp/render && npx --yes markdownlint-cli2@0.23.2 "docs/**/*.md" README.md SECURITY.md CHANGELOG.md
```

Expected: `Summary: 0 error(s)`.

```sh
grep -rniE 'poodl|pnut|site-root|stage_site|stage-preview|word[ -]list|(words|daily|sharing|statistics)\.allium|foo/www|/Users/' \
  ai_tmp/render/README.md ai_tmp/render/SECURITY.md ai_tmp/render/CHANGELOG.md \
  ai_tmp/render/docs/project ai_tmp/render/docs/tutorials ai_tmp/render/docs/how-to
grep -rnE '\{\{|\{%|\{#' ai_tmp/render/docs ai_tmp/render/README.md ai_tmp/render/CHANGELOG.md
```

Expected: the first prints exactly two lines, both in `docs/project/platform.md`, both
`https://` URLs; the second prints nothing.

The render's own documentation gate, which needs the network once (a lockfile, the Python
tooling and prek's hook clones) and is the acceptance check the brief names:

```sh
cd ai_tmp/render && git init -q -b main && uv lock && uv sync --frozen && just check-docs
```

Expected: `markdownlint`, `typos` and `lychee` each report `Passed`, and the validator
prints nothing. A typos finding on a rewritten page is fixed in the page; one on the slug
or the name is handed back (its remedy is T01's `pyproject.toml.jinja`).

Finally, the definition of done:

```sh
just check
```

Expected: `lock-check`, `lint`, `typecheck` and `test` all pass.

## Hand-back notes

### Verified, and how

`just test` in the template repository, after the last edit:

```text
tests/test_render.py .......................                             [ 79%]
tests/test_specs.py ss                                                   [ 86%]
tests/test_validators.py ....                                            [100%]
SKIPPED [1] tests/test_specs.py:26: set BISCUIT_TEMPLATE_NETWORK=1
SKIPPED [1] tests/test_specs.py:34: set BISCUIT_TEMPLATE_NETWORK=1
================= 27 passed, 2 skipped, 16 warnings in 12.04s ==================
```

The sixteen warnings are copier's `DirtyLocalWarning` for the uncommitted tree. The four
named tests are among the passes; none is skipped.

The render and its validator:

```text
Rendered into ai_tmp/render
Validated 38 pages and 39 canonical topics.
exit 0
```

The hub's validator prints that one line on success, so the exit status is the check
rather than silence.

markdownlint over the render:

```text
markdownlint-cli2 v0.23.2 (markdownlint v0.41.1)
Linting: 68 files
Summary: 0 issues in 0 files
```

The render's `.markdownlint-cli2.jsonc` adds its own `**/*.md` glob, so every Markdown
file in the render was linted, not only the four named. This version says "0 issues"
where the ticket expected "0 error(s)".

The forbidden-token grep printed exactly two lines, both in `docs/project/platform.md`,
both `https://` URLs:

```text
ai_tmp/render/docs/project/platform.md:76:| [Poodl handover](https://github.com/steven-cutting/biscuit_games/blob/main/docs/operations/poodl-handover.md) | The ledger the first game worked through when it took the package, and what it still records. |
ai_tmp/render/docs/project/platform.md:78:| [Their decision 0012](https://github.com/steven-cutting/biscuit_games/blob/main/docs/decisions/0012-the-domain-root-stays-with-poodl.md) | Why the domain root is still Poodl's. |
```

The delimiter grep printed nothing.

The render's own documentation gate:

```text
markdownlint.............................................................Passed
typos....................................................................Passed
lychee...................................................................Passed
uv run --frozen python scripts/validate_docs.py
Validated 38 pages and 39 canonical topics.
```

The Verification block as written is one step short. prek's `--all-files` reads the files
Git tracks, a freshly initialised render tracks none, and all three hooks then print
"(no files to check) Skipped". Running `git add -A` inside the render after `git init` is
what makes them read anything; T11 runs the same gate.

`just check` in the template repository: `lock-check` passed, every `lint` hook passed,
`mypy` reported "Success: no issues found in 7 source files", and `test` gave the same 27
passed and 2 skipped.

### Deviations

- `template/SECURITY.md` is unchanged. T00 had already shipped it in final form: its diff
  against `P SECURITY.md` is exactly lines 28-32 removed and the fallback paragraph added
  after line 7.
- `docs/tutorials/first-change.md`: the seed `src/routes/+page.svelte` puts two sentences
  in the main landmark ("Nothing to play yet. The board goes here."), so step 2 says "a
  short placeholder" where the ticket said "one sentence", step 4 says "instead of its
  placeholder" and step 5 says "Change the placeholder".
- `docs/how-to/work-in-the-component-workshop.md`: P lines 62-65 name Quality gates twice
  in consecutive sentences ("What it costs is in [Quality gates]. [Quality gates] states
  the exception"), an editing slip; here they are one sentence.
- `docs/how-to/update-from-template.md`: step 3 keeps each marker name whole on one line
  (the ticket's wrap split `>>>>>>> after updating` over a line break), so a search finds
  either; no line starts with a marker, so `check-merge-conflict` does not read the page as
  a conflict. The regenerate step is the ticket's three-line `console` block, not the
  one-liner the acceptance criterion quotes, which `_message_after_update` carries.
- `docs/how-to/work-with-the-specs.md`: P 105-144 became three paragraphs, the third
  holding both the `.created(...)` lesson and the 3.6.1 alias lesson. The sentence that
  every waiver was verified against 3.6.1 and is re-verified when the pin moves is P
  102-104, kept.
- `docs/project/platform.md`: rows 76 and 78 keep "Poodl" beside their URLs, as the edit
  list leaves them. Row 76's link text is the hub page's own title and row 78's
  description is the hub decision's subject; the allowlist covers the page.
- The template root's `CHANGELOG.md`, outside Files touched, gains one Managed bullet (the
  ten managed pages) and one Seed bullet (the four seed files that changed), because
  `AGENTS.md` asks for a note on every seed change and T09 set the precedent.
- Prose an edit touched was rewrapped near 90 columns. Untouched P lines keep P's
  wrapping, including the workshop page's one long line under "Switch theme, contrast and
  motion".

### Handed back

- **T00 follow-up, a questionnaire change through CONVENTIONS.md §3.** `game_name` accepts
  `|`, and `docs/project/terminology.md` puts the name in two table rows. A render with
  `game_name=Tic | Beans` gives a terminology page markdownlint refuses:

  ```text
  docs/project/terminology.md:21:28 error MD056/table-column-count Table column count [Expected: 2; Actual: 3; Too many cells, extra data will be missing]
  docs/project/terminology.md:31:72 error MD056/table-column-count Table column count [Expected: 2; Actual: 3; Too many cells, extra data will be missing]
  ```

  The pages do not work around it, as the open point says. The remedy is a refusal in the
  `game_name` validator and a case in `MARKDOWN_ANSWERS`.
- No manifest or map change, no `extend-words` entry and no validator change. No tier-B
  page was cut: `terminology.md.jinja` and `test-and-debug.md` both shipped.
- For the next edit of CONVENTIONS.md §8: row 4 calls platform.md's outbound table
  thirteen rows, where P has sixteen and all sixteen shipped; row 6 drops a `BASE_PATH`
  line the tutorial never had.
- For T12 or C03: the deploy page's one-time setup, as the ticket's exact content, names
  the Pages source and the environment but not the package read grant that
  `_message_after_copy` asks for before the first push. By CONVENTIONS.md §11's reasoning
  the build job's install is refused without it. Adding that step is a managed-page
  change; unverified here.

### Open points settled

- **The links a managed page may use.** `test_managed_pages_link_only_to_stable_pages`
  accepts a target in `managed_pages`, every `docs/` Markdown path in `MANAGED`, which
  includes `docs/README.md`, or one matching `docs/decisions/*.md`, which includes
  `docs/decisions/README.md`. Both indexes are permitted, and the map is exempt only as a
  source. This ticket's pages link to neither; platform.md names the decision index as a
  code span, as the ticket asks.
- **Decision titles**, `template/docs/manifest.yml` lines 43-48, each after "Decision
  NNNN: ": 0005 "A component workshop", 0006 "Visual review in Chromatic", 0007 "A
  project-managed Allium binary", 0008 "The design system arrives as a package", 0009
  "Rendered from the template", 0010 "A project Pages site". They are the link text in
  platform.md, the workshop page, the deploy page and the update page.
- **Reachability.** `validate_docs.py` exits 0 on the render, so all twelve pages here,
  `how-to/update-from-template.md` included, are reachable from `docs/README.md`.
- **Markdown-active answers.** The ticket's command omits `game_name`, which has no
  default, so it cannot render as written. With `-d 'game_name=Tic Tac Toe Beans'` and
  `-d 'description=A *marked* game_with_under_scores.'`, markdownlint over the render's
  `README.md`, `purpose-and-scope.md` and `terminology.md` reports 0 issues. The `|` case
  above is the one failure found.
- **`check-merge-conflict`** is at `template/.pre-commit-config.yaml:78`, so the update
  page keeps the hook-gate sentence.
- **typos** passes over the rewritten pages and the default slug in the render's
  `just check-docs`.

## Open points

CONVENTIONS.md §12 assigns this ticket no claim. Settle these while executing:

- The exact set of link targets `test_managed_pages_link_only_to_stable_pages` permits,
  in particular whether `docs/README.md` and `docs/decisions/README.md` are in it. Check:
  read the test in `tests/test_render.py`. This ticket's pages link to neither, so the
  answer changes nothing here; record it for T08.
- The manifest titles of decisions 0005 to 0010, used as link text in four pages. Check:
  `grep -n '"decisions/' template/docs/manifest.yml`.
- Every page in this ticket is reachable from `docs/README.md` in a render, in particular
  `how-to/update-from-template.md`. Check: `validate_docs.py` reports an unreachable page
  by name; a missing link is a T00 follow-up, not an edit here.
- A `description` or `game_name` holding Markdown-active characters (`*`, `_`, `<`)
  reaches the seed pages unescaped: `copier.yml` refuses only braces and control
  characters. Check: `uv run --frozen copier copy --defaults --vcs-ref=HEAD -d 'description=A *marked* game.' . ai_tmp/marked`,
  then markdownlint over `ai_tmp/marked/README.md` and
  `ai_tmp/marked/docs/project/purpose-and-scope.md`. A failure is a questionnaire change
  and goes back through CONVENTIONS.md §3 as a T00 follow-up; do not work around it in
  the pages.
- Whether `check-merge-conflict` is in the shipped `.pre-commit-config.yaml`, which the
  update page's step 3 relies on. Check: the `grep` in step 6 above.
- Whether the typos hook accepts the rewritten pages and the default slug. Check: the
  `just check-docs` block above.
