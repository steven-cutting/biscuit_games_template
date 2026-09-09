---
id: C06
title: A template-impact skill and check for template-to-game updates
status: open
depends_on: [T10]
parallel_with: []
branch: ticket/c06-template-impact
estimated_size: M
---

# C06: A template-impact skill and check for template-to-game updates

## Context

A change under `template/` reaches games in one of three ways, and nothing in the
template repository tells the agent making the change which one applies
(CONVENTIONS.md §5): a **managed** file arrives by 3-way merge on `copier update` and
may conflict where the game edited the same hunk; a **managed file the game is expected
to edit** (`M†`, the `GAME_EDITED` set) conflicts often enough that the bottom-append
convention exists for it; a **seed** file never arrives at all, so a fix to a seed
reaches no existing game. A fourth kind of change, to the questionnaire in `copier.yml`,
makes `copier update` re-ask or fail for every game. And after `v0.1.0` a seed page or a
numbered decision may never be added, renamed or retitled, because `docs/manifest.yml`
and `docs/README.md` re-render while seeds do not (CONVENTIONS.md §5, "Frozen seed
inventory"; §13).

The hub has the analogous problem and answers it with a skill: the hub's
`.agents/skills/consumer-impact/SKILL.md` (`/Users/scutting/projects/biscuit_games`)
sorts a change into "travels as a package" and "travels by citation", names the version
level from a table, and records findings in a ledger. Its eight numbered steps (lines
8-15) are the shape to copy.

After T10, `tests/inventory.py` is the single source of the classification
(`MANAGED`, `SEED`, `GAME_EDITED`; CONVENTIONS.md §9), and the template `CHANGELOG.md`
uses four headings per release: Managed, Seed, Questionnaire, Update notes
(CONVENTIONS.md §9, §10). This ticket connects the two: a check that classifies a
change and a skill that writes the entry and picks the tag level.

Read first: CONVENTIONS.md §3 (the questions and computed values), §5, §9, §10, §13;
`tests/inventory.py` and `tests/helpers.py` as merged; the hub skill above; the template
repository's `AGENTS.md` and `Justfile`.

## Goal

- `scripts/template_impact.py` and a `just impact <old-ref> [<new-ref>]` recipe that
  render both refs with default answers, diff the two renders, print every changed
  rendered path with its class from `tests/inventory.py`, and report questionnaire
  changes by comparing `copier.yml` at both refs. A seed change is flagged "reaches no
  existing game"; a `GAME_EDITED` change is flagged "conflict-likely"; a path in the
  new render that is a seed and absent from the old render, or a new numbered decision,
  is refused with a non-zero exit, because the inventory is frozen.
- `.agents/skills/template-impact/SKILL.md` in the template repository: run the check,
  write the `CHANGELOG.md` entry under the four headings, decide the tag level by
  CONVENTIONS.md §10 (MAJOR: a managed file removed, a question renamed or added
  without a default, a validator contract change; MINOR: a managed file, page or recipe
  added or changed, a pin bump, a `_min_copier_version` change; PATCH: prose), and add
  a "Steps by version" line to `template/docs/how-to/update-from-template.md.jinja`
  when a game must act after updating.
- `tests/test_changelog.py`: the Unreleased section exists and uses only the four
  headings.

## Non-goals

- Running the check in a game (a game runs `copier update`; this is for template
  authors).
- Automating the release itself: tagging and pushing stay separately authorised
  (CONVENTIONS.md §11).
- Changing the classification: `tests/inventory.py` is T10's and is read, not edited.
- Shrinking the managed list (C02).

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `scripts/template_impact.py` | repo | new | The check, per Steps 2 |
| `Justfile` | repo | T00's file | Add the `impact` recipe |
| `.agents/skills/template-impact/SKILL.md` | repo | new | The skill, per Steps 4 |
| `tests/test_changelog.py` | repo | new | The four-headings test |
| `AGENTS.md` | repo | T12's file | One sentence pointing at the skill |
| `pyproject.toml` | repo | T00's file | Only if `[tool.ruff] src` or mypy `files` need `scripts/` added |

## Steps

1. Read `tests/inventory.py`, `tests/helpers.py` (`render_template`, `Render.files()`)
   and `tests/test_update.py`'s `template_clone` fixture (how a ref is rendered from a
   clone; CONVENTIONS.md §9). The check reuses those helpers rather than re-implementing
   a render.
2. Write `scripts/template_impact.py`:
   - Arguments: `old_ref`, optional `new_ref` (default `HEAD`), `--json`.
   - Clone the repository into a temporary directory (`git clone --no-checkout`, as
     the fixture does), render each ref with `copier.run_copy(..., vcs_ref=ref,
     defaults=True, data=DEFAULT_ANSWERS, unsafe=False, quiet=True)`.
   - Walk both renders; for each path present in either, compute added / removed /
     changed by content digest, ignoring `.copier-answers.yml`.
   - Classify each path with `pathspec` against `SEED` (the same patterns as
     `copier.yml`'s `_skip_if_exists`), then `GAME_EDITED`, then `MANAGED`; a path in
     none is reported as "unclassified" and fails the run (the inventory test would
     fail too).
   - Print one line per path: `<status> <class> <path>` plus the flag text; then a
     questionnaire section: questions added, removed, renamed, or whose `default`
     changed, by parsing `copier.yml` at both refs with `yaml.safe_load` and comparing
     the keys that do not start with `_`.
   - Exit 2 on a refused change (a seed path added, a `docs/decisions/00NN-*` added or
     renamed, a seed retitled: compare the `title:` line of seed pages), 1 on an
     unclassified path, 0 otherwise. `--json` prints the same as one object.
   - `mypy --strict` and ruff clean under the template repository's configuration.
3. Add to `Justfile`:

   ```just
   # What a template change does to every rendered game: each changed rendered path
   # with its class (managed, game-edited, seed) and the questionnaire diff. Refuses a
   # seed addition: the inventory is frozen after v0.1.0.
   impact old new="HEAD":
       uv run --frozen python scripts/template_impact.py "$1" "$2"
   ```

4. Write `.agents/skills/template-impact/SKILL.md` with frontmatter `name:
   template-impact` and a `description` that states the trigger ("Use before tagging a
   template release or when a change under template/ is finished"), and numbered steps
   in the hub skill's register: (1) read `AGENTS.md` and `tickets/CONVENTIONS.md` §5 and
   §10; (2) run `just impact <last tag>`; (3) sort the output into the four CHANGELOG
   headings; (4) for each managed removal, write the Update note a game will read; (5)
   for each questionnaire change, write what `copier update` will ask; (6) name the tag
   level from the rules above, the table deciding rather than the feeling of size; (7)
   add the "Steps by version" line to `update-from-template.md.jinja` when a game must
   act; (8) run `just check`. Say that the skill records; tagging and pushing are
   separately authorised.
5. Write `tests/test_changelog.py`: parse `CHANGELOG.md`, find `## [Unreleased]`,
   assert its `###` headings are a subset of `Managed`, `Seed`, `Questionnaire`,
   `Update notes` in that order, and that every release section carries at least one of
   them. Add one sentence to `AGENTS.md` pointing at the skill.
6. Prove the check on synthetic history in a clone (never on `main`): three commits on
   a scratch branch, one editing a seed (`template/README.md.jinja`), one editing a
   managed file (`template/Justfile`), one renaming a question in `copier.yml`; run
   `just impact` between each pair and assert the three flags; then one commit adding
   `template/docs/decisions/0011-x.md` and assert exit 2.

## Acceptance criteria

- [ ] `just impact v0.1.0` on the repository prints a classified list and exits 0 when
      nothing is refused.
- [ ] A seed-only change prints "reaches no existing game"; a `GAME_EDITED` change
      prints "conflict-likely"; a question rename is reported under the questionnaire
      section; a seed addition exits 2 with the frozen-inventory message.
- [ ] `tests/test_changelog.py` is green and fails on a fifth heading.
- [ ] The skill exists, the template repository's `AGENTS.md` names it, and
      `just check` (lint, typecheck, test) is green.

## Verification

From the template repository root:

```sh
just check
just impact v0.1.0
```

Expected: green; a list whose every line starts with `added`, `removed` or `changed`
followed by `managed`, `game-edited` or `seed`, then the questionnaire section, exit 0.

Synthetic check (step 6), from a clone in `ai_tmp/`:

```sh
git clone -q --no-checkout . ai_tmp/impact && cd ai_tmp/impact && git checkout -q -b scratch main
# make the four commits described in step 6, then:
just impact HEAD~4 HEAD~3; echo "exit $?"   # seed edit: 'reaches no existing game', exit 0
just impact HEAD~3 HEAD~2; echo "exit $?"   # managed edit: 'conflict-likely' for Justfile, exit 0
just impact HEAD~2 HEAD~1; echo "exit $?"   # question rename reported, exit 0
just impact HEAD~1 HEAD; echo "exit $?"     # seed addition refused, exit 2
```

## Hand-back notes

Filled in by the agent that executes this ticket.

- The exact flags and exit codes observed in the synthetic check.
- Whether `render_template` could be reused as-is or needed a parameter for the clone
  path.
- What was handed back to T10 (an inventory gap) or T12 (README wording).
- Which open points were settled.

## Open points

- Whether rendering two refs from a clone of a dirty worktree needs the same throwaway
  commit `test_update.py` makes; check by running `just impact HEAD~1` with an
  uncommitted change present.
- Whether `pathspec`'s gitwildmatch handles the `_skip_if_exists` directory patterns
  identically to copier's own matcher for the classification (CONVENTIONS.md §12, the
  pathspec item, is checked by T00's inventory test; this check reuses the same
  patterns).
- Whether a seed *retitle* can be detected reliably from the `title:` line alone when a
  page is `.jinja` (the title may contain an answer); render before comparing.
- How `just impact` behaves before any tag exists (`v0.1.0` absent): document that it
  takes any ref, and that `HEAD~1` is the fallback.
