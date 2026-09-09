---
id: T04
title: "Agent contract: AGENTS.md, CLAUDE.md, eight skills and sixteen bridges"
status: open
depends_on: [T00]
parallel_with: [T01, T02, T03, T05, T06, T07, T08, T09]
branch: ticket/t04-agent-contract
estimated_size: M
---

# T04: Agent contract: AGENTS.md, CLAUDE.md, eight skills and sixteen bridges

## Context

Every rendered game carries the agent contract Poodl carries: `AGENTS.md` as the single
source of truth, `CLAUDE.md` as a one-line adapter, eight canonical skills under
`.agents/skills/<name>/SKILL.md`, and a fixed-body bridge for each skill under
`.claude/skills/` and `.codex/skills/`. The hub's `scripts/validate_agents.py` (shipped
into the render by T02) gates the whole surface on every `just check` in a game, and the
template's own `tests/test_validators.py` runs it against a render on every `just test`.

Order: T00 merged first and placed a stub at all 26 paths this ticket owns, so the fast
suite is green today. This ticket replaces those stubs with the final content. It runs in
parallel with T01 to T03 and T05 to T09 and touches none of their files; T10 waits for it.

Sources, at the commits `CONVENTIONS.md §0` pins (P = `/Users/scutting/projects/poodl`
at `0a46a485`, H = `/Users/scutting/projects/biscuit_games` at `09b4894a`). Read first:

- `P/AGENTS.md`, all 189 lines. Lines 10-12 describe Poodl, 36-41 are invariant 3, 50-52
  invariant 6, 68-71 the platform-package bullet, 145-189 the Provenance section.
- `P/.agents/skills/<name>/SKILL.md` for the eight names in the table below, and the
  sixteen bridges at `P/.claude/skills/<name>/SKILL.md` and
  `P/.codex/skills/<name>/SKILL.md`. P also ships a ninth skill, `word-list-change`,
  which is not carried: the word lists it governs are not part of the template.
- `P/CLAUDE.md`: `@AGENTS.md` and a newline, 11 bytes in all.
- `H/scripts/validate_agents.py`, all 252 lines: the rules the result must satisfy. It is
  byte-identical at H's `v1.0.0` tag and at `09b4894a`.
- `P/scripts/run_project_check.py` lines 18-30: the `RECIPES` tuple. `project-check`
  step 2 says gates 2, 10 and 11 need the Allium binary; those are `lint`, `check-specs`
  and `analyse-specs` in that tuple, which T02 ships unchanged, so the skill is verbatim.

Why the edits: a managed file says "this game", never the name (`CONVENTIONS.md §4`,
last paragraph), and `tests/test_render.py::test_no_poodl_outside_provenance` allows the
word "poodl" only on a short allowlist that, among this ticket's files, holds
`AGENTS.md` alone. Poodl's `AGENTS.md` and four of its skills name
Poodl's modules, word lists, clipboard and timer; `CONVENTIONS.md §7` under "Managed
adaptations against Poodl files" gives the replacement text, and this ticket embeds it.

## Goal

- `template/AGENTS.md.jinja` is Poodl's `AGENTS.md` with the five edits of
  `CONVENTIONS.md §7` applied, renders with no Jinja delimiter left, carries the six
  phrases the validator requires and 300 or more words (about 1350 with the default
  answers), and names the template commit from `_copier_answers._commit`.
- `template/CLAUDE.md` is byte-identical to `P/CLAUDE.md`.
- The eight canonical skills exist under `template/.agents/skills/`: four byte-identical
  to P, four carrying the step edits of `CONVENTIONS.md §7`, all with P's frontmatter.
- The sixteen bridges are byte-identical to P's, and no `word-list-change` directory
  exists under any of the three skill roots.
- `just check` is green in the template repository, and `validate_agents.py` exits 0 in
  a render that has been `git init`ed.

## Non-goals

- `template/.claude/settings.json` and `template/scripts/validate_agents.py`: T02.
- `template/.github/copilot-instructions.md` (the second byte-pinned adapter): T03.
- The handbook page that documents this contract, `docs/reference/agent-contract.md`:
  T08. A hand-back about its bridge rule is in Open points.
- The template repository's own `AGENTS.md` and `CLAUDE.md` at the root: T12.
- No new skill, no renamed skill, and no change to any skill's frontmatter: a bridge
  must repeat its skill's frontmatter exactly, so a frontmatter edit is a change to
  three files and to the handbook page, and none is wanted.
- `docs/manifest.yml`, `docs/README.md.jinja`, `copier.yml`, `tests/inventory.py`: no
  lane touches them (`CONVENTIONS.md §11`).

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `template/AGENTS.md.jinja` | M† | P, same path without the suffix | Five edits, embedded below |
| `template/CLAUDE.md` | M | P, same path | Verbatim |
| `template/.agents/skills/accessibility-review/SKILL.md` | M | P, same path | Steps 2, 4, 5 |
| `template/.agents/skills/code-review/SKILL.md` | M | P, same path | Verbatim |
| `template/.agents/skills/fix-quality/SKILL.md` | M | P, same path | Verbatim |
| `template/.agents/skills/plan-change/SKILL.md` | M | P, same path | Verbatim |
| `template/.agents/skills/project-check/SKILL.md` | M | P, same path | Verbatim |
| `template/.agents/skills/review-docs/SKILL.md` | M | P, same path | New step 3 |
| `template/.agents/skills/spec-change/SKILL.md` | M | P, same path | Steps 1, 4 |
| `template/.agents/skills/svelte-change/SKILL.md` | M | P, same path | Steps 2, 4 |
| `template/.claude/skills/accessibility-review/SKILL.md` | M | P, same path | Verbatim |
| `template/.claude/skills/code-review/SKILL.md` | M | P, same path | Verbatim |
| `template/.claude/skills/fix-quality/SKILL.md` | M | P, same path | Verbatim |
| `template/.claude/skills/plan-change/SKILL.md` | M | P, same path | Verbatim |
| `template/.claude/skills/project-check/SKILL.md` | M | P, same path | Verbatim |
| `template/.claude/skills/review-docs/SKILL.md` | M | P, same path | Verbatim |
| `template/.claude/skills/spec-change/SKILL.md` | M | P, same path | Verbatim |
| `template/.claude/skills/svelte-change/SKILL.md` | M | P, same path | Verbatim |
| `template/.codex/skills/accessibility-review/SKILL.md` | M | P, same path | Verbatim |
| `template/.codex/skills/code-review/SKILL.md` | M | P, same path | Verbatim |
| `template/.codex/skills/fix-quality/SKILL.md` | M | P, same path | Verbatim |
| `template/.codex/skills/plan-change/SKILL.md` | M | P, same path | Verbatim |
| `template/.codex/skills/project-check/SKILL.md` | M | P, same path | Verbatim |
| `template/.codex/skills/review-docs/SKILL.md` | M | P, same path | Verbatim |
| `template/.codex/skills/spec-change/SKILL.md` | M | P, same path | Verbatim |
| `template/.codex/skills/svelte-change/SKILL.md` | M | P, same path | Verbatim |

Every path already exists as a T00 stub. Nothing else is edited except the `status:`
line of this ticket.

## Steps

Fenced blocks under a numbered step are indented by the list; the file content they
show starts at column 0. Run everything from the template repository root.

### Prepare

1. Create the worktree on `ticket/t04-agent-contract` from `main` (see `README.md`),
   run `just sync`, and confirm `just test` is green before changing anything.
2. Read `CONVENTIONS.md §4` (the tree and the "this game" rule), `§5` (`AGENTS.md` is
   `M†`: a game appends deviations at the end of Provenance, so keep that list last),
   `§6` (Jinja rules) and `§7` "Managed adaptations against Poodl files"; then the P
   and H files named in Context.
3. Read the rules `H/scripts/validate_agents.py` enforces, so every file below is
   written against them:
   - Inventory (lines 57-107, 136-150): the managed set is exactly `AGENTS.md`,
     `scripts/validate_agents.py`, the two adapters, and `SKILL.md` under each of the
     three roots for every directory found under `.agents/skills/`; a file missing from
     that set or present beyond it fails, with `.claude/settings.json` tolerated. The
     set is listed with `git ls-files --cached --others --exclude-from=.gitignore`, so
     the render must be a Git worktree and carry a `.gitignore`.
   - No delimiter (line 54, `UNRESOLVED`): no managed file may contain any of `{{`,
     `{%` or `{#` after rendering.
   - `AGENTS.md` (lines 46-53, 152-166): contains, case-insensitively, `untrusted`,
     `just check`, `explicit authorization`, `ai_tmp/`, `docs/specs/` and `runes`;
     splits into 300 or more words; no `CODEX.md` beside it.
   - `CLAUDE.md` (lines 33-34, 169-176): the exact text `@AGENTS.md` and one newline,
     compared unstripped.
   - Canonical skill (lines 179-205): frontmatter keys exactly `name` and `description`,
     no repeat; `name` equals the directory; `description` splits into 8 or more words;
     the body contains `just` followed by a space, and `AGENTS.md`.
   - Bridge (lines 19-25, 207-223): frontmatter equal to the canonical skill's, and the
     body, stripped, exactly the sentence ``Follow `../../../.agents/skills/<name>/SKILL.md`.
     That file is canonical and this bridge adds nothing to it.``

### `template/CLAUDE.md`

1. Copy `P/CLAUDE.md` over the stub and check the bytes:

   ```sh
   cp /Users/scutting/projects/poodl/CLAUDE.md template/CLAUDE.md
   cmp /Users/scutting/projects/poodl/CLAUDE.md template/CLAUDE.md
   wc -c template/CLAUDE.md
   ```

   `cmp` prints nothing; the count is 11.

### `template/AGENTS.md.jinja`

1. Copy `P/AGENTS.md` to `template/AGENTS.md.jinja` (the `.jinja` suffix is dropped on
   render, `CONVENTIONS.md §3`), then apply the five edits below and nothing else. Line
   numbers are P's; every other line stays as it is. The file uses only the answer names
   `game_name`, `description`, `hub_package`, `pages_url`, `template_url`, `base_path`
   and `_copier_answers._commit` guarded with `default`, all permitted by
   `CONVENTIONS.md §6` rule 3.
2. Lines 10-12, the paragraph that begins `Poodl is an unlimited-play`, become:

   ```text
   {{ game_name }} is a Biscuit Games game: {{ description | trim | trim('.') }}.
   It is a single-page static web app with no backend, no accounts and no server,
   built on the platform package `{{ hub_package }}` and deployed to GitHub Pages
   at <{{ pages_url }}>.
   ```

3. Lines 36-41, invariant 3, become (the last sentence is P's, kept):

   ```text
   3. **Side effects sit behind a port.** Storage, randomness and the clock are
      reached through `src/lib/ports/`, each with an in-memory fake, and every
      side effect this game adds gets a port there in the same shape; the
      device's preferences and its keyboard are reached through the two ports
      `@steven-cutting/biscuit-games` exports, with the fakes it ships. Tests
      inject fakes; they never stub a global.
   ```

4. Lines 50-52, invariant 6, become:

   ```text
   6. **Colour never carries meaning alone.** Every state a surface shows has a
      non-colour indication and an accessible name, as the `@guarantee` clauses
      in `docs/specs/` require.
   ```

5. Lines 68-71, the bullet that begins `The platform's primitives`, become:

   ```text
   - The platform's primitives, the play-surface cells and keys and the token
     stylesheet are imported from `@steven-cutting/biscuit-games`, never copied.
     What another game would render unchanged belongs upstream — see
     [The platform upstream](docs/project/platform.md).
   ```

6. Keep line 145 (`## Provenance`) and the blank line 146. Replace lines 147-189, the
   rest of the file, with the block below, so that the file ends after
   `every game.` with a single newline:

   ```markdown
   Rendered by Copier from the `biscuit_games_template` template
   (<{{ template_url }}>) at `{{ _copier_answers._commit | default('an untagged commit') }}`.
   The answers are recorded in `.copier-answers.yml`; `copier update` is how the
   toolchain moves, and [Update from the template](docs/how-to/update-from-template.md)
   says which files it manages and which are this game's alone. The template's
   conventions were distilled from Poodl, the first Biscuit Games game, which took
   them from an earlier copier template. What the template decides is recorded in
   the decision records it ships under `docs/decisions/`:

   - A static site with no backend, prerendered by `adapter-static` and published
     as a project Pages site beneath `{{ base_path }}/`.
   - Side effects behind ports with in-memory fakes.
   - Specifications in Allium as the source of truth for behaviour, checked by a
     project-managed binary pinned in `scripts/install_allium.py`.
   - A small Python toolchain (`uv`, `prek`, `ruff`) for the hook gate and the
     two validators; Markdown formatted by `markdownlint-cli2` alone.
   - The design system taken as a package from the Biscuit Games hub, with a test
     holding every restated clause to the platform's text.
   - Storybook as a component workshop gated by `just check`, and Chromatic as
     its visual review.

   Deliberate deviations for this repository, each recorded in
   [the decision records](docs/decisions/README.md): none yet. Record one here
   when this game departs from the template, and change the template instead
   when the departure would suit every game.
   ```

7. The word "poodl" now occurs exactly once (in Provenance) and none of `pnut`,
   `site-root`, `stage_site`, `stage-preview`, `word list`, `foo/www` or `/Users/`
   remains; the render grep in Verification checks both.

### The four verbatim skills

1. Copy P's files over the stubs and confirm the bytes:

   ```sh
   P=/Users/scutting/projects/poodl
   for n in code-review fix-quality plan-change project-check; do
     cp "$P/.agents/skills/$n/SKILL.md" "template/.agents/skills/$n/SKILL.md"
     cmp "$P/.agents/skills/$n/SKILL.md" "template/.agents/skills/$n/SKILL.md"
   done
   ```

### The four edited skills

Start each from P's file (`cp` as above), then change only the lines named. Frontmatter
and every other line stay P's, including the single long line per step.

1. `review-docs`: insert a new step 3 and renumber P's steps 3-7 to 4-8. The body's list
   reads, in full:

   ```markdown
   1. Read `AGENTS.md` and `docs/reference/documentation-contract.md`. The contract is enforced by `scripts/validate_docs.py`, which reports every violation at once.
   2. Find the topic's owner first. Every topic in `docs/manifest.yml` has exactly one canonical page, so prefer editing the owning page over writing a new one.
   3. Say which side of the template the page is on. A managed page is changed in `biscuit_games_template` and arrives by `copier update`; editing it here is a stopgap the next update will merge. A seed page is this game's and no update touches it. `docs/how-to/update-from-template.md` lists both.
   4. A new page needs a `docs/manifest.yml` entry whose `title`, `kind`, `audience`, `canonical_for` and `requires` match the page frontmatter exactly, including list order — the comparison is order-sensitive.
   5. Give the page one level-one heading identical to its `title`, at least forty words of substance, and no unfinished markers or placeholder prose.
   6. Link the page in from `docs/README.md`, directly or transitively. An unreachable page fails the contract even when everything else about it is correct.
   7. Use relative links and check the case; the contract verifies link targets exist with exact case, and heading anchors within Markdown targets.
   8. Run `just check-docs`, then `just check` before handoff.
   ```

2. `spec-change`: step 1 (P line 10) and step 4 (P line 13) become:

   ```markdown
   1. Read `AGENTS.md` and `docs/explanation/specifications.md`. Identify which module under `docs/specs/` owns the behaviour; each module's header states its Scope, Includes and Excludes, and a clause the platform states is owned by `@steven-cutting/biscuit-games` and only restated here.
   4. Check that dependent modules still hold. A module others import is depended on by each of them, so a change to a trigger or an entity ripples, and a restated platform clause is held to the platform's text by `tests/platformSpecs.test.ts`.
   ```

3. `svelte-change`: step 2 (P line 9) and step 4 (P line 11) become:

   ```markdown
   2. Inspect the route, the component, the ports under `src/lib/ports/` and the two `@steven-cutting/biscuit-games` exports — the device's preferences and its keyboard — and the existing tests before editing. Never reach for `localStorage`, `crypto`, `Date` or any other browser global outside a port adapter.
   4. Preserve semantic HTML, labels bound to controls, keyboard operation, visible focus, and a non-colour indication for every state a surface shows.
   ```

4. `accessibility-review`: steps 2, 4 and 5 (P lines 11, 13, 14) become:

   ```markdown
   2. Check the colour obligation. Every state the surface distinguishes by colour also carries a non-colour indication and an accessible description, in the words the surface's `@guarantee` clauses use, so it is readable without colour vision.
   4. Check what is announced. Every outcome the surface's `@guarantee` clauses say is announced reaches assistive technology through the platform's `Announcer`, carrying the detail the clause names.
   5. Check what is not exposed. Whatever a surface's specification withholds from the player stays out of the DOM as well, attributes included.
   ```

5. The diff-count loop in Verification confirms each file differs from P's only at the
   lines above.

### The sixteen bridges

1. Copy P's bridges for the eight names over the stubs, under both providers, and
   confirm the bytes and the directory listings:

   ```sh
   for d in .claude .codex; do
     for n in accessibility-review code-review fix-quality plan-change project-check review-docs spec-change svelte-change; do
       cp "$P/$d/skills/$n/SKILL.md" "template/$d/skills/$n/SKILL.md"
       cmp "$P/$d/skills/$n/SKILL.md" "template/$d/skills/$n/SKILL.md"
     done
   done
   ls template/.agents/skills template/.claude/skills template/.codex/skills
   ```

   Each listing is exactly the eight names; no `word-list-change`, no other file.

### Check, commit, hand back

1. Run the Verification blocks below and quote their output in Hand-back notes.
2. Run `just check` (lock-check, lint, typecheck, test); every step green.
3. Commit on the ticket branch, then set this ticket's `status:` to `done` in the same
   commit or a following one.
4. **Authorisation required:** pushing the branch and opening the pull request are
   separately authorised actions (`CONVENTIONS.md §11`). Stop and ask before either.

## Acceptance criteria

- [ ] `template/CLAUDE.md` is 11 bytes and `cmp`-equal to `P/CLAUDE.md`.
- [ ] `template/AGENTS.md.jinja` differs from `P/AGENTS.md` only at the five edits in
      Steps; rendered with the default answers it has no `{{`, `{%` or `{#`, 300 or
      more words, the six required phrases, and the value of `_commit` from
      `.copier-answers.yml` in its Provenance paragraph.
- [ ] "poodl" occurs once in the rendered `AGENTS.md` and nowhere under the render's
      `.agents/`, `.claude/` or `.codex/`.
- [ ] `template/.agents/skills/` holds exactly `accessibility-review`, `code-review`,
      `fix-quality`, `plan-change`, `project-check`, `review-docs`, `spec-change` and
      `svelte-change`; four are `cmp`-equal to P's and four differ only at the lines
      the Steps name; every frontmatter is P's.
- [ ] All sixteen bridges are `cmp`-equal to P's; the three skill roots list the same
      eight names and nothing else.
- [ ] `scripts/validate_agents.py` exits 0 in a `git init`ed render, printing
      `Validated AGENTS.md, 2 adapters, and 8 skills.`
- [ ] `just check` is green in the template repository; `tests/test_validators.py`,
      `test_rendered_jinja_files_carry_no_delimiter`, `test_answers_file_and_provenance`
      and `test_no_poodl_outside_provenance` pass.
- [ ] No file outside the Files touched table changed, other than this ticket's
      `status:` line.

## Verification

From the template repository root, on the ticket branch.

```sh
just check
```

Expected: `lock-check`, `lint`, `typecheck` and `test` all pass; in `test`, every case in
`tests/test_render.py` and `tests/test_validators.py` passes and only `network` or `full`
cases are skipped.

```sh
rm -rf ai_tmp/t04-render
just render ai_tmp/t04-render
cmp ai_tmp/t04-render/scripts/validate_agents.py /Users/scutting/projects/biscuit_games/scripts/validate_agents.py
```

Expected: `Rendered into ai_tmp/t04-render`; `cmp` prints nothing. If `cmp` reports a
difference, T02 has not merged yet and the render carries T00's stub: copy H's script
into `ai_tmp/t04-render/scripts/` only (never into `template/`) before the next block,
and say so in Hand-back notes.

```sh
git -C ai_tmp/t04-render init -q -b main
uv run --frozen python ai_tmp/t04-render/scripts/validate_agents.py; echo "exit $?"
```

Expected: `Validated AGENTS.md, 2 adapters, and 8 skills.` then `exit 0`. The script is
standard library only and finds its root from its own path.

```sh
wc -w ai_tmp/t04-render/AGENTS.md
grep -ci poodl ai_tmp/t04-render/AGENTS.md
grep -n -i -E 'pnut|site-root|stage_site|stage-preview|word list|foo/www|/Users/' ai_tmp/t04-render/AGENTS.md
grep -rli poodl ai_tmp/t04-render/.agents ai_tmp/t04-render/.claude ai_tmp/t04-render/.codex; echo "exit $?"
grep -cE '\{\{|\{%|\{#' ai_tmp/t04-render/AGENTS.md
grep -o '_commit: .*' ai_tmp/t04-render/.copier-answers.yml
grep -n 'Rendered by Copier' -A1 ai_tmp/t04-render/AGENTS.md
```

Expected: a word count of 300 or more (about 1350); `1`; nothing; nothing printed and
`exit 1`; `0`; the `_commit` value, and the same value inside the backticks on the line
after `Rendered by Copier`.

```sh
P=/Users/scutting/projects/poodl
cmp "$P/CLAUDE.md" template/CLAUDE.md
for n in code-review fix-quality plan-change project-check; do
  cmp "$P/.agents/skills/$n/SKILL.md" "template/.agents/skills/$n/SKILL.md"
done
for d in .claude .codex; do
  for n in accessibility-review code-review fix-quality plan-change project-check review-docs spec-change svelte-change; do
    cmp "$P/$d/skills/$n/SKILL.md" "template/$d/skills/$n/SKILL.md"
  done
done
for n in accessibility-review review-docs spec-change svelte-change; do
  diff "$P/.agents/skills/$n/SKILL.md" "template/.agents/skills/$n/SKILL.md" | grep -c '^[<>]'
done
ls template/.agents/skills template/.claude/skills template/.codex/skills
```

Expected: every `cmp` silent; the four counts are `6` (accessibility-review: three lines
each side), `11` (review-docs: five lines removed, six added), `4` and `4`; each of the
three listings is exactly the eight names.

```sh
git status --porcelain
```

Expected: after the commit, empty; before it, only paths from the Files touched table and
`tickets/T04-agent-contract.md`.

## Hand-back notes

Filled in by the agent that executes this ticket.

- What was verified and how: paste the output of every Verification block, including
  the word count and the `_commit` value the render recorded.
- What deviated from the ticket and why (a line number in P that did not match, a
  validator rule that read differently, a wording changed to pass a gate).
- What was handed back to another ticket: anything found in `scripts/validate_agents.py`
  (T02), `docs/reference/agent-contract.md` (T08), the template repository's own
  `pyproject.toml` or `.markdownlint-cli2.jsonc` (T00 follow-up on `main`).
- Which open points below were settled, with the command run and what it printed.

## Open points

None of the `CONVENTIONS.md §12` claims is assigned to this ticket. Unsettled while
writing it:

- **The bridge rule the handbook states.** P's `docs/reference/agent-contract.md` lines
  55-58 say a bridge is "one sentence pointing at" the canonical skill with "at most
  forty words in total", which is P's older validator; the validator the template ships
  (H's) compares the bridge body to one exact sentence, and H's page, lines 70-83, says
  so. `CONVENTIONS.md §8` row 25 carries the page from P "Verbatim". Hand back to T08:
  take H's "What a bridge must be" section. Check, once T08 has merged:
  `grep -n forty ai_tmp/t04-render/docs/reference/agent-contract.md` prints nothing.
- **`_commit` before the first tag.** Copier records `git describe --tags --always`, so
  until T11 tags `v0.1.0` the Provenance line names a bare commit hash, and the
  `default('an untagged commit')` guard fires only when no `_commit` is recorded at all.
  Check: the `grep -o '_commit: .*'` line in Verification matches the Provenance line.
  Settled by T11.
- **A description that does not end in a full stop.** `trim('.')` strips full stops
  only, so `A game with beans!` renders `... game: A game with beans!.`. Check:
  `uv run --frozen copier copy --defaults --data 'description=A game with beans!' --vcs-ref=HEAD --quiet . ai_tmp/t04-punct`
  then `sed -n 10p ai_tmp/t04-punct/AGENTS.md`. Cosmetic; if it is to be fixed, the fix
  is a change to the `description` validator or the expression in `CONVENTIONS.md §7`,
  through `main`, not here.
- **The shipped skills are linted at source.** The template repository's own gate runs
  markdownlint and typos over `template/.agents/**/*.md`, `template/.claude/**/*.md` and
  `template/.codex/**/*.md`, under T00's configuration rather than Poodl's. Check:
  `just lint`. A typos finding on a skill's vocabulary is fixed by an `extend-words`
  entry in the template repository's `pyproject.toml`, which is T00's file: hand it
  back rather than rewording the skill.
