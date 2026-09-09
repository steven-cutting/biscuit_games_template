---
id: C05
title: Should the hub's handbook pages ship in the package? A decision for the hub
status: open
depends_on: []
parallel_with: []
branch: ticket/c05-handbook-in-the-package
estimated_size: M
---

# C05: Should the hub's handbook pages ship in the package? A decision for the hub

## Context

The template solves "edit once" for toolchain prose: managed pages are template-owned
and arrive in every game by `copier update` (CONVENTIONS.md §1, decision 5; §5). What it
does not solve is the hub's own handbook. Every game's `docs/project/platform.md` cites
the hub's pages by `https://` link (Poodl's page, `/Users/scutting/projects/poodl`
`docs/project/platform.md`: the table of outbound links under "Where to read it" at line
59, and the section "What nothing here checks" at line 89), and nothing resolves those
links on any gate.

The hub (`/Users/scutting/projects/biscuit_games`) has already decided the current
state and recorded what is unsettled:

- `docs/decisions/0013-shared-material-travels-as-a-package.md` line 49: the package
  "carries no handbook page"; pages stay where they are and are cited.
- `docs/project/what-the-hub-owns.md` lines 125-129, "What is not settled": whether the
  handbook ever travels with the package; "shipping Markdown into `node_modules` would
  trade a rotting link for a stale copy".
- `docs/operations/poodl-handover.md` lines 695-705, "What a cross-repository link
  costs": `validate_docs.py` skips any target beginning `http://`, `https://` or
  `mailto:` (the hub's `scripts/validate_docs.py` line 229), lychee runs `--offline` in
  the hook and in `just check-docs` (the hub's `Justfile` line 127), and only
  `just check-links-online` (`Justfile` lines 153-154) resolves them, by hand.
- The package already ships non-code files: `package.json` lines 27-33 list `docs/specs`
  and `CHANGELOG.md` under `files`.

The hub's `.agents/skills/consumer-impact/SKILL.md` step 5 states the consequence: a
renamed page or a moved anchor "is still a link that rots silently". With the template,
the number of repositories carrying those links grows with every game, so the cost of
the status quo grows too.

This ticket is a recommendation (CONVENTIONS.md §1, decision 3). It produces a decision
record in the hub, which is another repository: opening that pull request is separately
authorised (CONVENTIONS.md §11). Read first: CONVENTIONS.md §0, §8 (row 4, the
`platform.md` rewrite), §11; the four hub files above; the hub's
`docs/reference/published-artefacts.md` (what a version number promises).

## Goal

A decision record in the hub, numbered `0018` (the hub's highest is
`0017-the-rest-of-the-design-system-is-ported.md`; verify nothing has landed since),
choosing one of:

- **A. Status quo.** Pages are cited by URL; `just check-links-online` stays the only
  check; the template's `platform.md` keeps its "What nothing here checks" section.
- **B. The package ships its handbook.** `package.json` `files` gains `docs` (or
  `docs/**/*.md` minus `docs/operations/` and `docs/decisions/`, which are the hub's
  own), and a game links relatively into
  `node_modules/@steven-cutting/biscuit-games/docs/...`. `validate_docs.py` then checks
  those links for existence and exact case on every gate (`node_modules` sits inside the
  repository root, so the escape check passes; `just lint` already needs the package
  installed). A rotting link becomes the same versioned staleness the specifications
  already have: a bump is when the game reads the new text.
- **C. A hub CI job resolves a citations list.** The hub keeps `citations.txt` naming
  the pages it promises to keep, a workflow fails when one moves, and the
  `consumer-impact` skill's step 5 becomes automatic for the listed pages.

The recommendation is B, with the trade stated: it removes the monthly manual recipe
from the critical path and makes a page rename a package MAJOR (so renames become rare
and announced); its costs are tarball size (measure it: the hub's `docs/` is a few
hundred kilobytes) and that `just check-docs` in a game can no longer run before
`just sync` and `npm ci`.

## Non-goals

- Changing the template's managed `platform.md` beyond what the chosen option needs
  (that is a template MINOR release, listed in `CHANGELOG.md`, after the hub decides).
- Moving toolchain pages (they are the template's, CONVENTIONS.md §5).
- Cross-repository Allium imports; Allium has none, and `tests/platformSpecs.test.ts`
  already holds restated clauses to the shipped modules (CONVENTIONS.md §7).

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `biscuit_games: docs/decisions/0018-<slug>.md` | other repo | new | The decision record, in the hub's decision shape |
| `biscuit_games: docs/decisions/README.md` | other repo | hub file | One index row |
| `biscuit_games: docs/manifest.yml` | other repo | hub file | One entry for the new record |
| `biscuit_games: docs/project/what-the-hub-owns.md` | other repo | hub file | Lines 125-129: the item moves from "not settled" to settled |
| `biscuit_games: package.json` | other repo | hub file | Only if B: `files` gains the pages; version bumped MINOR |
| `biscuit_games: docs/reference/published-artefacts.md` | other repo | hub file | Only if B: the pages listed as an interface with their version rules |
| `biscuit_games: .github/workflows/ci.yml` and `citations.txt` | other repo | hub files | Only if C: the citations job |
| `template/docs/project/platform.md` | M | T07's page | If B: outbound links become relative links into `node_modules`; if A or C: unchanged |

## Steps

1. Read the five hub files named in Context and CONVENTIONS.md §8 row 4. Measure what B
   would ship: `du -sh docs` in the hub, and `npm pack --dry-run` after a trial edit of
   `files` (not committed), reading the reported tarball size.
2. Prototype B in a render, without committing anything: `just render ai_tmp/render`,
   `git init -q -b main`, `just initialize`; then in `node_modules/@steven-cutting/biscuit-games/`
   create `docs/design/direction.md` by hand (a stand-in for a shipped page), change one
   outbound link in `docs/project/platform.md` to
   `../../node_modules/@steven-cutting/biscuit-games/docs/design/direction.md`, run
   `just check-docs`, and record whether `validate_docs.py` accepts the path (existence,
   exact case, inside the root) and whether lychee offline resolves it. Then rename the
   stand-in and confirm the gate fails. This is the evidence for B's central claim.
3. Prototype C's cost: list every hub page a game's `platform.md` cites (the table at
   Poodl's line 59 onward) and count them; that list is `citations.txt`.
4. Write the decision record in the hub's shape (read `0013` for the shape: context,
   decision, consequences, and the frontmatter and manifest entry the hub's
   `validate_docs.py` requires), choosing A, B or C with the step 2 and 3 evidence, and
   with the "not settled" paragraph in `what-the-hub-owns.md` updated to point at it.
5. If B: edit `package.json` `files`, bump the version MINOR, list the pages in
   `published-artefacts.md` as an interface whose rename is MAJOR, and add a
   `CHANGELOG.md` entry. If C: add the workflow job and `citations.txt`. Run the hub's
   `just check`.
6. **Authorisation required:** open the hub pull request; nothing in the hub is pushed
   without it.
7. After the hub merges and (if B) publishes: open a template ticket or follow-up on
   `main` that rewrites `template/docs/project/platform.md`'s outbound table to relative
   links, listed in the template `CHANGELOG.md` under Managed (MINOR). That follow-up is
   outside this ticket's files and is handed back.

## Acceptance criteria

- [ ] The hub carries decision `0018` choosing A, B or C, with the step 2 and 3
      evidence in its text, indexed in `docs/decisions/README.md` and `docs/manifest.yml`,
      and `what-the-hub-owns.md` no longer lists the question as unsettled.
- [ ] If B: `npm pack --dry-run` lists the pages; `published-artefacts.md` states the
      version rule for a page rename; in a render with the new package installed,
      `just check-docs` fails when a cited page is renamed in a locally packed tarball.
- [ ] If C: the hub job fails on a renamed cited page.
- [ ] If A: `platform.md`'s "What nothing here checks" section stays, and the record
      says why the cost is accepted.
- [ ] The hub's `just check` is green on the pull request.

## Verification

In the hub, on the branch:

```sh
just check
npm pack --dry-run 2>&1 | grep -c 'docs/'
```

Expected: green; a count of shipped pages (B) or zero (A, C).

In a render, for B:

```sh
just render ai_tmp/render && cd ai_tmp/render && git init -q -b main && just initialize
npm pack ../../../biscuit_games && npm install ./steven-cutting-biscuit-games-*.tgz --no-save
just check-docs
```

Expected: green with relative links into `node_modules`; red after renaming one shipped
page inside the tarball's extracted tree.

## Hand-back notes

Filled in by the agent that executes this ticket.

- The option chosen and the measured evidence (tarball size, the prototype's gate
  results, the citation count).
- The hub pull request and its check outcome.
- What was handed back to the template: the `platform.md` rewrite (B) or nothing.
- Which open points were settled.

## Open points

- Whether the hub's `validate_docs.py` accepts a relative link whose target sits under
  `node_modules` (the escape check compares resolved paths with the repository root;
  `node_modules` is inside it, but a symlinked package would resolve outside). Check in
  step 2.
- Whether lychee offline follows a relative link into `node_modules` or whether the
  render's `lychee.toml` `exclude_path` hides it. Check in step 2.
- Whether the hub wants `docs/decisions/` and `docs/operations/` excluded from the
  shipped set (they are the hub's own record, not an interface). Decide in step 4.
- The hub's next free decision number: `0018` on 2026-09-09; re-check before writing.
