# Copier or a GitHub template repository: the comparison behind decision 1

This report records why `biscuit_games_template` is a [Copier](https://copier.readthedocs.io)
template rather than a GitHub template repository, with the evidence each claim rests on,
so that a future maintainer or agent can re-open the question with the facts in hand.
It expands decision 1 in [`tickets/CONVENTIONS.md`](../../tickets/CONVENTIONS.md) §1 and is
the basis for the rendered handbook's decision 0009 ("rendered from the template",
written by ticket T09). Written 2026-09-09 against Copier 9.18.2 and the GitHub
documentation current on that date.

## Context

One Biscuit Games game exists, Poodl. A second, `tic_tac_toe_beans`, is starting, and
more are expected. The hub package `@steven-cutting/biscuit-games` carries the shared
code (design system, ports, specifications), but not the toolchain, the handbook or the
agent contract: those live as files in each game's repository. The render the template
produces holds 126 files, of which 101 are template-owned ("managed") and 24 are the
game's own from the first commit ("seed"), and 14 of the managed files are ones every game
is expected to edit (`tickets/T00-foundation.md`, the inventory; `CONVENTIONS.md` §5).

The problem is not the first day. Either mechanism produces a working repository on day
one. The problem is every later day: a validator gets stricter, a workflow pin moves, a
handbook page is corrected, a recipe is added to the `Justfile`, and every game should
take that change without a maintainer hand-carrying it. With N games, "hand-carry" is N
pull requests per change, each a manual diff between two repositories that share no
history.

## How each mechanism works

### A GitHub template repository

- "Use this template" or `gh repo create --template <owner>/<repo>` copies the tree into
  a new repository that "starts with a single commit". The default branch only is
  copied unless "Include all branches" (`--include-all-branches`) is chosen, and
  "branches created from a template have unrelated histories, so you cannot create pull
  requests or merge between the branches". Source: GitHub's pages on
  [creating a repository from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)
  and [creating a template repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-template-repository),
  and `gh repo create --help` (gh 2.100.0).
- There is no substitution. The new repository is byte for byte the template's tree, so
  a project name, slug, description or repository path can only be a placeholder the
  new owner finds and replaces.
- There is no update path. Nothing on GitHub records which template a repository came
  from in a form a tool can act on, and the unrelated histories rule out `git merge`.
- The template must itself be a valid repository: its own CI runs on its own tree, so
  the tree cannot contain unrendered placeholders in files the tooling parses
  (`package.json`, `pyproject.toml`, workflow files, the Allium module).
- Anyone with read access to the template can use it; a private template is usable by
  the owner and collaborators, which fits this account.
- Git LFS files are not allowed in a template repository. No Biscuit Games repository
  uses LFS.

### Copier

- `copier copy` asks the questions in `copier.yml` (four here: `game_name`, `game_slug`,
  `description`, `repository`), renders every `.jinja` file with those answers, copies
  everything else byte for byte, and writes `.copier-answers.yml` recording the answers
  and the template commit (`CONVENTIONS.md` §3).
- `copier update` renders the template at the recorded commit and at the new one,
  diffs the old render against the game, applies the template's change with
  `git apply --reject`, and 3-way merges whatever does not apply cleanly, leaving
  `<<<<<<< before updating` / `>>>>>>> after updating` markers in the file. A managed
  file the game edited keeps its edits unless the same hunk moved. Verified in Copier
  9.18.2's `_main.py`; `CONVENTIONS.md` §1 fact 3 and §2 give the line references.
- The seed and managed split is two lists in `copier.yml`: `_skip_if_exists` (never
  overwrite an existing file) and a Jinja-conditional `_exclude` that hides the same
  paths from every update. A seed is the game's from the first commit; a managed file is
  the template's, merged on every update (`CONVENTIONS.md` §5).
- The template is taskless: no `_tasks`, no `_migrations`, no Jinja extensions, so
  `copier` never needs `--trust` and runs nothing from the template on the user's
  machine.
- Versions are git tags in PEP 440 form; `copier update` picks the latest tag by default
  and refuses a dirty worktree or a downgrade (`CONVENTIONS.md` §10).
- Local prerequisites: `uv` (already required by every game's toolchain) and
  `uvx copier`.

## Comparison

| Criterion | GitHub template repository | Copier |
| --- | --- | --- |
| Name, slug, description, repository in files | Placeholder text; the new owner finds and replaces every site by hand | Four answers, rendered into 15 files (`.jinja` suffix); everything else byte-copied |
| A later toolchain change reaching existing games | Manual: diff two unrelated repositories, open one PR per game | `copier update`: a 3-way merge with markers only where the game edited the same hunk |
| Knowing which template version a game is on | Nothing recorded | `.copier-answers.yml` holds `_commit` and `_src_path`, committed in the game |
| Game-owned files (README, decisions, components, specs) | Indistinguishable from template files; a later "sync" would overwrite them | The 14 seed patterns: never merged, recreated or deleted by an update |
| Testing the template itself | The template is a live project; its CI proves the placeholder game works, not that a real game will | The harness renders the template with test answers and runs the render's own gate; `test_update.py` proves updates apply and seeds survive |
| Day-one ergonomics | One click in the GitHub UI, no local tools | `uvx copier copy gh:steven-cutting/biscuit_games_template <dir>`, wrapped as `just new-game`; then `git init`, `just initialize`, `just check` |
| Local prerequisites | None | `uv`, which every game needs anyway |
| Private template | Works for the owner and collaborators | Works: `copier` clones over the same `gh:` credentials |
| Files that clash with the template syntax | None | Real cost: `{#` in Svelte and `${{ }}` in workflows are Jinja syntax. Mitigation: no `.svelte`, `.test.ts`, workflow or `.py` file is ever `.jinja`; answers reach Svelte through one module, `src/lib/brand.ts` (`CONVENTIONS.md` §6) |
| Drift across N games after a year | Unbounded; each game is a fork in all but name | Bounded to seeds and to game-added files; the managed set converges on every update |
| What an AI agent does to take a change | Reads two repositories, reasons about which differences are template and which are game, edits by hand | Runs `copier update`, resolves any markers, runs `just check`; the seed list tells it what not to touch |
| Cost carried by the template maintainer | Low: edit the live project | Higher: `.jinja` discipline, a tag before every consumer render, a frozen seed inventory after `v0.1.0`, a CHANGELOG that says what an update will do |
| Failure mode | Silent: a game quietly falls behind and nobody can list what it is missing | Loud: an update conflicts, or `test_update.py` fails in the template's CI before the tag exists |

## What each would look like for Biscuit Games

**A template repository** would be a working game named after a placeholder, say
`game_template`, with its own green CI. Starting a game means clicking the button and
then replacing the placeholder in the 14 files an answer touches (`package.json`,
`pyproject.toml`, `AGENTS.md`, `README.md`, `CHANGELOG.md`, `docs/README.md`, the two
project pages, two decision pages, two how-to pages, `src/lib/brand.ts` and the Allium
module; the 15th `.jinja` file is `.copier-answers.yml`, which has no counterpart),
plus the repository path in the Pages workflow. Nothing checks that the replacement was complete: `validate_docs.py`
forbids `{{`, not "game_template". Every later change to the 101 managed files is a
manual PR per game, or a bespoke sync script that would have to reinvent the seed and
managed split Copier already implements, without the version record to diff against.

**Copier** is what tickets T00 to T12 build: a `template/` tree with 15 `.jinja` files, a
`copier.yml` with four questions and the two seed lists, a harness that renders and
gates the result in CI, a `v0.1.0` tag before the first consumer render, and
`tic_tac_toe_beans` rendered from that tag as the end-to-end check
([`tickets/README.md`](../../tickets/README.md)).

## Decision

Copier. The deciding criterion is the second row of the table: N games have to keep
taking toolchain changes, and only Copier gives a mechanical, versioned path for that.
A rendered tree is also what makes the template testable before anyone consumes it.

## Consequences

Every consequence is already a rule in the tickets:

- The seed inventory is frozen after `v0.1.0`: `docs/manifest.yml` and `docs/README.md`
  re-render on every update while seeds never do, so a seed page or a numbered decision
  can never be added, renamed or retitled by the template (`CONVENTIONS.md` §5).
- A tag precedes every consumer render, so that `.copier-answers.yml` records a version
  an update can compare (`CONVENTIONS.md` §10; ticket T11).
- The 14 managed files a game edits follow a layout convention (the template inserts in
  upper blocks, the game appends at the end) so that both sides rarely touch the same
  hunk (`CONVENTIONS.md` §5).
- `.copier-answers.yml` is listed in `.prettierignore`, because the formatter would
  rewrite a file Copier owns (`CONVENTIONS.md` §13).
- `test_update.py` in the template's harness proves, on every change, that an update
  from the previous commit and from the latest tag applies without markers and leaves
  seeds and game-added files alone (`CONVENTIONS.md` §9; ticket T10).
- A managed file the template stops rendering is deleted from every game on update, so
  every such removal is a MAJOR release announced under "Update notes" in the
  template's CHANGELOG (`CONVENTIONS.md` §5, §10).

## When a template repository would be the right answer

- There will only ever be one or two games, so hand-carrying changes costs less than
  maintaining `.jinja` discipline and a harness.
- The shared material is small enough to live entirely in the hub package, leaving each
  game with nothing template-owned to keep in step.
- The people starting games do not have, and should not need, `uv` on their machine.
- The template is itself the product: a working demo that is meant to be browsed and
  forked, not a generator.

None of these holds today: a third game is expected, 101 files are template-owned, `uv`
is a prerequisite of every game's toolchain, and the template is not a game.

## Hybrids considered and rejected

- **A GitHub template repository whose content is the Copier template.** Marking
  `biscuit_games_template` as a template repository would make the "Use this template"
  button produce a copy of the generator (the `template/` tree, `copier.yml`, the
  harness), not a game. It adds nothing over `git clone` and invites the wrong click.
- **A pre-rendered example game as a template repository, with Copier for updates.**
  The example would be a render with fixed answers; a game created from it would need
  its `.copier-answers.yml` rewritten by hand before `copier update` could run, which is
  the same find-and-replace with a new failure mode. C07 in the tickets shows what
  hand-writing that file costs for Poodl.
- **Cookiecutter or cruft.** Cookiecutter has no update path; cruft adds one built on
  the same idea as Copier's, with a smaller set of controls over what an update may
  touch. Both carry the same Jinja hazard in Svelte files. Copier was
  already the tool Poodl's toolchain was distilled from (`foo/www`), so its conventions
  cost nothing new.

## Sources

- [`tickets/CONVENTIONS.md`](../../tickets/CONVENTIONS.md): §1 (decisions and the three
  facts), §2 (Copier 9.18.2 source references), §3 (`copier.yml`), §4 (the template
  tree and its 15 `.jinja` files), §5 (managed versus seed), §6 (Jinja rules), §9 (the
  harness), §10 (update, tags), §13 (risks).
- `tickets/T00-foundation.md`: the inventory counts (101 managed, 24 seed, 14
  game-edited, 126 files in a render).
- GitHub Docs, "Creating a repository from a template" and "Creating a template
  repository", read 2026-09-09 (links above); `gh repo create --help`, gh 2.100.0.
- Copier 9.18.2, as `uvx copier` installs it.
