---
id: T09
title: Decision records: the ten seed decisions and their index
status: done
depends_on: [T00]
parallel_with: [T01, T02, T03, T04, T05, T06, T07, T08]
branch: ticket/t09-decisions
estimated_size: M
---

# T09: Decision records: the ten seed decisions and their index

## Context

Every rendered game ships ten numbered decision records and their index under
`docs/decisions/`. The whole directory is seed (CONVENTIONS.md §4 and §5): `copier copy`
renders it once, and no `copier update` ever merges, recreates or deletes anything in it.
Eight records are carried from Poodl, the first Biscuit Games game, renumbered to close the
gaps left by the six that are Poodl's alone (its 0005, 0007, 0009, 0010, 0012 and 0013);
two are new, one on being rendered from the template and one on the Pages address. The
carried records keep Poodl's `canonical_for` slugs, following the hub's precedent: the hub
restarted its series at 0001, and "Ported entries say so and keep the topic slug they had,
because the slug is what a cross-repository reference names"
(`/Users/scutting/projects/biscuit_games/AGENTS.md` lines 242-243).

T00 has merged: `template/docs/manifest.yml` carries the eleven entries, `template/docs/README.md.jinja`
links to the index, and every file this ticket owns exists as a stub with valid frontmatter.
This lane replaces the stubs. T01 to T08 run beside it and touch none of these files; T10
waits for all nine lanes. Read `tickets/CONVENTIONS.md` §0, §4, §5, §6, §8 (rows 28 to 38 and
the paragraph after the table), §10, §11 and §13 first, then the sources below.

Source repositories, at the commits CONVENTIONS.md §0 pins:

- P = `/Users/scutting/projects/poodl` (`0a46a485`): `docs/decisions/README.md` and the
  records `0001`, `0002`, `0003`, `0004`, `0006`, `0008`, `0011`, `0013`; `docs/manifest.yml`
  lines 39-52 (the decision entries: titles, audiences, slugs); `docs/README.md` lines 67-69
  (how the map reaches the index); `.github/workflows/chromatic.yml` lines 19-29 and 174-178
  (permissions); `scripts/run_project_check.py` lines 18-30 (`RECIPES`: `check-specs` is
  gate 10, `analyse-specs` gate 11); `Justfile` lines 43, 148 and 155 (`install-allium`,
  `check-specs`, `analyse-specs`); `svelte.config.js` line 22 (`paths.base`).
- H = `/Users/scutting/projects/biscuit_games` (`09b4894`): `docs/decisions/0003-static-site-no-backend.md`
  line 11 (the shape of a ported record's opening line); `docs/decisions/README.md` lines
  45-51 (a "The numbering" section); `scripts/validate_docs.py` (the validator the render
  ships: `BAD_CONTENT` at 36-43, `MINIMUM_WORDS` at 32, frontmatter at 54-86, links at
  222-249, reachability at 252-262); `.github/workflows/chromatic.yml` lines 201-217, 224
  and 230-265 (the no-token guard); `src/lib/index.ts` lines 26-65 (what the package
  exports); `package.json` lines 44-46 (the three specification modules it exports);
  `src/app.css` lines 322-387 (`data-theme` and `data-high-contrast` selectors).

## Goal

The eleven files under `template/docs/decisions/` in final form: eight carried records
restated for a game that starts from the template, two new records, and an index of ten
rows, each passing the hub's `validate_docs.py` in a render, `markdownlint-cli2`, and the
template's own `just test`. Nothing in the directory names a Poodl-only path, and the
index says, in the words of CONVENTIONS.md §5 and §13, that the template never adds,
renames or retitles a numbered decision after its first release.

## Non-goals

- `docs/manifest.yml` and `docs/README.md.jinja`: T00 wrote them and no lane edits them
  (CONVENTIONS.md §11). A title, audience or slug that has to change is handed back in the
  hand-back notes as a T00 follow-up on `main`, and this ticket's file keeps the manifest's
  value meanwhile.
- The pages the records link to: `project/`, `how-to/` and `tutorials/` are T07;
  `explanation/`, `reference/` and `operations/` are T08. A link target that a stub already
  provides is enough; do not wait for the lane.
- An eleventh decision, or a different number or file name for any of the ten. The
  inventory is frozen at `v0.1.0` (CONVENTIONS.md §5 "Frozen seed inventory"); a template
  decision goes in the template's `CHANGELOG.md` (T12).
- Poodl's and the hub's own records: never modified.
- `tests/test_render.py` and its allowlists (T00, then T10).

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `template/docs/decisions/README.md.jinja` | S | P's index | Ten rows, `game_name` once, a "The numbering" section, "Writing a new one" verbatim |
| `template/docs/decisions/0001-static-site-no-backend.md` | S | P decision 0001 | Carried; generic context, supersession notes dropped, base-path clause points at 0010 |
| `template/docs/decisions/0002-ports-and-fakes.md` | S | P decision 0002 | Carried; boundaries are storage, clock, randomness plus the platform's two ports |
| `template/docs/decisions/0003-specs-are-the-source-of-truth.md` | S | P decision 0003 | Carried; generic examples, the "not installed" cost replaced |
| `template/docs/decisions/0004-python-toolchain.md` | S | P decision 0004 | Carried; name only |
| `template/docs/decisions/0005-component-workshop.md` | S | P decision 0006 | Carried and renumbered; palette narratives dropped, notes folded in |
| `template/docs/decisions/0006-visual-review-in-chromatic.md` | S | P decision 0008 | Carried and renumbered; dated notes dropped, the no-token skip added |
| `template/docs/decisions/0007-project-managed-allium-cli.md` | S | P decision 0011 | Carried and renumbered; final form only |
| `template/docs/decisions/0008-design-system-as-a-package.md` | S | P decision 0013 | Rewritten for a game that starts with the package |
| `template/docs/decisions/0009-rendered-from-the-template.md` | S | new | Why Copier, managed versus seed, the frozen inventory, what `copier update` does |
| `template/docs/decisions/0010-a-project-pages-site.md.jinja` | S | new | The project Pages site at `pages_url`; replaces Poodl's 0009 |

## Steps

1. Read CONVENTIONS.md §4, §5, §8 rows 28 to 38 and §13, then every source file named
   in Context, then `template/docs/manifest.yml` in your worktree. The manifest is the
   authority for each file's frontmatter. Expected values, from P's `docs/manifest.yml`
   lines 39-52 for the carried records (the two new ones are whatever T00 wrote):

   | File | `title` | `audience` | `canonical_for` |
   | --- | --- | --- | --- |
   | `README.md` | Architecture decisions | `[contributor, maintainer, agent]` | `decision_index` |
   | `0001` | Decision 0001: A static site with no backend | `[maintainer, agent]` | `decision_no_backend` |
   | `0002` | Decision 0002: Side effects behind ports | `[contributor, maintainer, agent]` | `decision_ports_and_fakes` |
   | `0003` | Decision 0003: Specifications decide behaviour | `[contributor, maintainer, agent]` | `decision_spec_first` |
   | `0004` | Decision 0004: A Python toolchain in a frontend repository | `[maintainer, agent]` | `decision_python_toolchain` |
   | `0005` | Decision 0005: A component workshop | `[contributor, maintainer, agent]` | `decision_component_workshop` |
   | `0006` | Decision 0006: Visual review in Chromatic | `[contributor, maintainer, agent]` | `decision_visual_review` |
   | `0007` | Decision 0007: A project-managed Allium binary | `[maintainer, agent]` | `decision_allium_cli` |
   | `0008` | Decision 0008: The design system arrives as a package | `[contributor, maintainer, agent]` | `decision_design_system_as_a_package` |
   | `0009` | Decision 0009: Rendered from the template | as the manifest says | `decision_rendered_from_template` |
   | `0010` | Decision 0010: A project Pages site | as the manifest says | `decision_project_pages_site` |

   If the manifest disagrees with a carried record's P values, the manifest wins in your
   file and the disagreement is handed back. `kind` is `decision` and `requires` is `[]`
   throughout; key order is `title`, `kind`, `audience`, `canonical_for`, `requires`, as
   P's records carry it.

2. Rules every result obeys (the hub's `validate_docs.py` and T00's `tests/test_render.py`
   enforce them; run the Verification commands, step 15, rather than trusting a reading):

   - Frontmatter equal to the manifest entry, five keys, `title` double-quoted, lists
     inline; H1 exactly equal to `title`; 40 or more words in the body.
   - After rendering, none of `{{`, `{%`, `{#` anywhere. Only the two `.jinja` files
     substitute an answer: `game_name` once in the index, `pages_url` once in 0010
     (CONVENTIONS.md §6 rule 3). Every other file is byte-copied and must be Jinja-free.
   - No unfinished marker and no placeholder prose: the `BAD_CONTENT` patterns of H's
     `validate_docs.py` lines 36-43 (three annotation words, "lorem ipsum", "insert ...
     here").
   - Every relative link resolves, exact-case, to a page the render ships: only the
     paths in CONVENTIONS.md §8 rows 1 to 38. Never link to a Poodl-only record (its 0005,
     0007, 0009, 0010, 0012, 0013) or page (`how-to/replace-the-word-lists.md`).
   - The word "Poodl" is allowed in `docs/decisions/*.md` (the allowlist of
     `test_no_poodl_outside_provenance`). These tokens are forbidden everywhere, and P's
     records carry several: `pnut` (P 0009, P 0013 line 102), `site-root` and
     `stage_site` (P 0009), `stage-preview`, `word list` and `word-list` (P 0002 line 16,
     P 0003 line 14), `words.allium`, `daily.allium`, `sharing.allium` (P 0006 line 54),
     `statistics.allium` (P 0002 line 18), `foo/www`, `/Users/`.
   - Managed pages say "this game"; a carried record says "this game" too, and "Poodl"
     only where it reports what Poodl did.

3. The opening line. Each carried record, on line 11 (directly under the H1 and a blank
   line), carries exactly this sentence with its own number, modelled on H's
   `0003-static-site-no-backend.md` line 11:

   ```markdown
   *Carried from Poodl's decision 0001 at `0a46a485`, and restated for a game rendered from the Biscuit Games template. Poodl's own record stands where it is.*
   ```

4. `0001-static-site-no-backend.md`: P's `0001` verbatim except the following.
   - Lines 13-15 (Context) become: "This game is a single-player game with no accounts, no
     leaderboard and no shared state. The conventions it inherits arrive by way of Poodl,
     and Poodl's came from a full-stack template with a Python backend, a PostgreSQL
     database and a generated API client."
   - Lines 29-30 become: "Whatever the game keeps in the browser — settings, statistics, a
     game in progress — belongs to one browser on one device. Clearing browser data
     destroys it and nothing can restore it. That is a real cost borne by the player."
   - Lines 32-33 (the custom-game link to Poodl's 0005): drop.
   - Lines 39-41 become:

     ```markdown
     The base path becomes configuration. A project site is served from a subdirectory,
     so `BASE_PATH` is read at build time into `paths.base`. Where the value comes from,
     and why no domain sits in front of it, is [Decision 0010](0010-a-project-pages-site.md).
     ```

   - Lines 43-46 (the note pointing at Poodl's 0009) and lines 55-58 (the note pointing at
     Poodl's 0012): drop both. CONVENTIONS.md §8 row 29 cites them as 43-44 and 55-56;
     each note is a four-line paragraph and the whole paragraph goes.
   - Line 50: "a synchronised daily word" becomes "a synchronised daily puzzle". The
     purpose-and-scope link at line 53 stays (a seed page; row 2).
   - Related pages (62-63) unchanged: both targets are shipped (rows 14 and 12).

5. `0002-ports-and-fakes.md`: P's `0002` verbatim except:
   - Lines 13-16 become: "The template this game's conventions descend from isolates its
     one side effect — the HTTP API — behind a port with an in-memory fake, so components
     can be tested without a running backend. This game has no API, but it has boundaries
     of its own. Three are here: device storage, randomness and the clock. Two more — the
     device's preferences and its keyboard — arrive as ports the platform package exports,
     each with the fake it ships." (H `src/lib/index.ts` lines 56-65 export both.)
   - Lines 18-21 become: "Two of those are awkward to test directly. A specification that
     draws with `uniform_choice` calls it the one deliberately non-deterministic step. A
     specification that arms a countdown asks a test to wait real seconds, and a test that
     waits is not a test worth having."
   - Lines 43-44 become: "There is a cost: three small indirections here and two in the
     package, for boundaries some projects would touch directly, and a rule that has to be
     enforced by review because no tool checks it."
   - Lines 37-41 (Node 26 and jsdom) stay verbatim; they are generic and still true.
     Related pages (53-54): layering and testing, rows 15 and 22.

6. `0003-specs-are-the-source-of-truth.md`: P's `0003` verbatim except:
   - Lines 13-16 become: "This game's behaviour is written in Allium before the code that
     implements it: a root module under `docs/specs/`, and beside it the modules the game
     adds. The question is whether they remain authoritative once implementation starts,
     or become a design document that quietly falls behind."
   - Lines 18-20 become: "A game is a good argument for the former. The rule that decides a
     round has a well-known trap somewhere in it, and the difference between a correct
     implementation and a plausible one is a few lines. Left in prose, that detail is lost
     in the first refactor."
   - Lines 35-37 become: "Contracts become testable obligations rather than intentions. A
     surface's `@guarantee` clauses name what it owes, and a test asserts each one
     directly, including the edge cases a plausible implementation gets wrong."
   - Lines 39-42 become: "Unresolved product decisions stay visible. They are recorded as
     `open question` blocks and answered by someone entitled to answer them rather than by
     whoever writes the code first."
   - Lines 44-46 (CONVENTIONS.md §8 row 31 cites line 45; the sentence runs 44-46) become:

     ```markdown
     The costs are real. Every behaviour change is two edits, not one. The project-managed
     `allium` binary — [Decision 0007](0007-project-managed-allium-cli.md) — holds every
     module to parsing and analysing cleanly, but nothing mechanical holds the code to a
     clause, so drift between a clause and its implementation is still caught by review.
     ```

   - Related pages (57-58): specifications and work-with-the-specs, rows 16 and 10.

7. `0004-python-toolchain.md`: P's `0004` verbatim except line 13, "Poodl ships no Python.
   The hook gate it inherits from the template runs" becomes "This game ships no Python.
   The hook gate it inherits runs", and line 24, "on top of the template's gate list"
   becomes "on top of the inherited gate list". Related pages (50-51): rows 23 and 11.

8. `0005-component-workshop.md`: P's `0006` renumbered (frontmatter, H1 and opening line
   say 0005 and "Poodl's decision 0006") and:
   - Lines 13-22 (Context) become two paragraphs: "The specifications name surfaces, and
     every component that renders one is an accessibility contract as much as a rendering
     job: a shape for every mark, a name for every control, a keyboard path to every
     operation, and two palettes to satisfy." then "Nothing in the repository renders a
     component on its own. A component is reachable only through a route, and the states
     that matter are reached by playing the game until it produces them. The component
     tests assert accessible names in jsdom, which is exactly the right evidence and is
     not something anybody looks at."
   - Line 33: "which is what `src/app.css` already keys on" becomes "which is what the
     platform's stylesheet keys on" (a game has no `src/app.css`; H `src/app.css` lines
     322-387 select on both attributes).
   - Lines 36-42 (the "nothing publishes it" paragraph and the blockquote superseding it)
     become one paragraph:

     ```markdown
     The workshop is local: a recipe serves it, two recipes gate it, and the Pages
     workflow is untouched. What publishes it is `just chromatic` and a workflow of its
     own, for visual review — [Decision 0006](0006-visual-review-in-chromatic.md).
     ```

   - Lines 49-92 (the three palette-defect narratives and the two lessons drawn from
     them, Poodl's history): drop. In their place, one paragraph: "One lesson from Poodl's
     workshop is worth carrying without its history. A gate's silence is not a pass: axe's
     contrast rule downgrades any element whose visible text is a single character to
     *incomplete* and reports incomplete without failing, so a board of one-letter cells
     is never in scope for it; and a figure recorded in prose beside a colour drifts from
     the colour, so a colour this game adds needs a measurement of its own rather than a
     number in a comment."
   - Lines 108-113 (the dated blockquote) become a plain paragraph:

     ```markdown
     It is not the only request. The workshop composes the platform's published one
     through a Storybook `refs` entry, so `just storybook-build` makes a request of its
     own every time the gate runs. The difference from the download above is that this
     one cannot fail: an unreachable address degrades to a sidebar entry that does not
     open. [Quality gates](../reference/quality-gates.md) states the exception.
     ```

   - Line 133: "Or the ten surfaces getting built" becomes "Or the game's surfaces getting
     built". Lines 46-47, 94-106, 115-127, 131-135 and the related pages (139-141: rows 9,
     22, 17) stay.

9. `0006-visual-review-in-chromatic.md`: P's `0008` renumbered (0006, "Poodl's decision
   0008") and:
   - Lines 13-24 (Context) become:

     ```markdown
     [Decision 0005](0005-component-workshop.md) built the workshop and gates it. What the
     gate answers is a question about rules: axe says whether a rule is met. A rendered
     pixel answers a different question, whether the thing looks right, and that question
     has no local answer that survives being forgotten. Headless Chromium reports a light
     preference, so a dark-theme defect can stay green in the gate and be caught only by
     a person flipping a toolbar control, which is how Poodl found one. A workshop of many
     stories is also more than anyone re-opens by hand after a change to a stylesheet.
     ```

   - Line 30: "`chromatic@18.2.0` is a pinned devDependency" becomes "`chromatic` is a
     pinned devDependency" (a literal version drifts the moment a game bumps it; the same
     reasoning as CONVENTIONS.md §13 gives for the hub version).
   - Lines 38-48 (the gate paragraph and its dated blockquote) become:

     ```markdown
     The recipe sits outside `just check`, beside `check-links-online`, because it needs a
     token. Gate 6 composes the platform's published workshop through a `refs` entry and
     fetches its address while it builds, so `just check` does reach the network — but it
     needs no token and cannot fail on the request. [Quality gates](../reference/quality-gates.md)
     owns the list of gates.
     ```

   - Line 58: "a hundred and five snapshots is a real cost" becomes "every snapshot is a
     real cost". After line 62 ("Chromatic is not a required check.") add: "A missing
     token is not a failure either. When `CHROMATIC_PROJECT_TOKEN` is not set on the
     repository, a step notes its absence, the publish step is skipped, and the reply on a
     pull request says that no build was published; the run passes. A rendered game
     therefore does not fail its first push for a secret it has not created, and creating
     one is the whole of switching visual review on." (H `chromatic.yml` 207-217, 224 and
     251-257; T03 ships that guard.)
   - Line 69: "Poodl collects nothing" becomes "This game collects nothing".
   - Lines 104-119 (the untested permission query and the first refusal, Poodl's history)
     become one paragraph: "The workflow holds `pull-requests: write` as well as
     `issues: write`, because a comment on a pull request sits on `issues/*` endpoints but
     is weighed against the pull request. The acknowledging reaction and the closing reply
     are best-effort: neither is the build, and a note about a published build must not
     colour it red." (P `chromatic.yml` 19-29 and 174-178.)
   - Line 148: "reopen 0006" becomes "reopen 0005". Related pages: the first row becomes
     the link to `0005-component-workshop.md` titled "Decision 0005: A component
     workshop"; rows 9, 23 and 18 stay.

10. `0007-project-managed-allium-cli.md`: P's `0011` renumbered (0007, "Poodl's decision
    0011"), final form only:
    - Lines 13-15 become: "The specifications under `docs/specs/` decide every behaviour
      in this project, so something has to confirm mechanically that they parse and
      analyse cleanly, rather than leaving modules that outrank the code to be read by
      eye. `allium` is the tool that checks them."
    - Lines 30-31: the sentence "`just check-specs` runs the result." becomes
      "`just check-specs` and `just analyse-specs` run the result."
    - Lines 59-62 and 64-100 (the outside-the-gate paragraph and the four dated
      supersession notes) become three paragraphs:

      ```markdown
      Both recipes are gates: hooks in `.pre-commit-config.yaml` triggered by `docs/specs/`
      and by the pin itself, steps in the `documents` CI job, and gates 10 and 11 of
      `just check`.

      Gating took more than a line in the `Justfile`, because no exit code here carries
      the verdict. `allium check` exits non-zero on warnings as well as errors but 0 on an
      `info` diagnostic, and `allium analyse` keys its status on findings alone and ignores
      diagnostics entirely, so a module that fails to parse passes it with the `error` in
      the JSON it has just printed. Neither status means clean, so `scripts/run_allium.py`
      runs the subcommand, prints its output whole, and asserts what the contract says: an
      empty `diagnostics` array and an empty `findings` array in every module. A diagnostic
      can be waived with a whole-line `-- allium-ignore <code>` comment — the waiver terms
      are in [Work with the specifications](../how-to/work-with-the-specs.md) — and a
      finding cannot.

      The binary is a per-worktree install in a gitignored directory, so a worktree that
      has not run `just initialize` fails `just lint` and `just check` until
      `just install-allium` puts one there. That is accepted rather than softened: a gate
      that skips itself when its tool is missing asserts nothing.
      ```

    - Lines 111-113 (the two met conditions): drop. Keep line 115 (the `[upstream]`
      reference definition), lines 17-24, 28-31 with that edit, 33-40, 44-57, 102-103,
      107-109 and the related pages (119-121: rows 10, 11, 23).

11. `0008-design-system-as-a-package.md`: rewritten from P's `0013` (0008, "Poodl's
    decision 0013") for a game that never held a copy. Keep P's section shape and tone;
    reuse P's sentences where a bullet names them. Never state a literal package version:
    write "the version `package.json` pins" (CONVENTIONS.md §13).
    - Context: the hub, `steven-cutting/biscuit_games`, decides how Biscuit Games looks and
      publishes it as `@steven-cutting/biscuit-games`: the stylesheet and typefaces, the
      chrome (`HeaderBar`, `Wordmark`, `Monogram`, `Announcer`, `Modal`, `Notice`,
      `Button`, `IconButton`, `Tile`, `Key`, `Keyboard`, `PhysicalKeyboard` and the rest
      of H `src/lib/index.ts` 26-48), the preferences and keys ports with their fakes, and
      the three specification modules `appearance.allium`, `operation.allium` and
      `play-surfaces.allium`. Poodl ported a copy in first and replaced it with the package
      once the hub existed; its record explains the copies that drifted (P 0013 21-26).
      This game starts with the package and has nothing to delete.
    - Decision: installed at an exact version (invariant 4); `.npmrc` names the registry
      for the scope and holds no token; the token is a contributor's own in `~/.npmrc` and
      CI's `github.token` with `packages: read` (P 0013 32-35). The game restates only
      what it has a surface for: the six platform figures live in `src/lib/config.ts`,
      the root module states them by name, and `tests/platformSpecs.test.ts` holds both
      equal to the shipped text; a clause the game restates word for word is listed in
      `tests/restated.ts` and held to the platform's words. The workshop composes the
      platform's, which costs gate 6 a network request. `docs/project/platform.md` is the
      one page that points outward.
    - Consequences (P 0013 60-68 and 83-89, "Poodl" made "this game"): a first run needs a
      credential and the registry answers an anonymous read with a 404 naming the package;
      a build here can fail because of a release there, which is the point; the platform's
      clauses are not this game's to word, so amending one is a change upstream and a
      version bump here; the cross-repository links rot silently and
      `just check-links-online` is monthly and manual. Drop 70-81 (what changed when Poodl
      switched).
    - What would reopen this (P 93-96 minus the second-game clause). Related pages: rows 4,
      11, 23, 22 only; no link to Poodl's 0009 or 0010.

12. `0009-rendered-from-the-template.md`, new, in P's shape (Context, Decision,
    Consequences, What would reopen this, Related pages). No opening line: nothing is
    carried. Its facts are CONVENTIONS.md §1 (decision 1 and fact 3), §5, §10 and §13;
    write them as prose, not as a restatement of the tables:
    - Context: several games share a toolchain, a handbook, an agent contract and a gate,
      and a change to any of them should reach every game once. A GitHub repository
      template gives no substitution and no update path, and must itself be a valid
      project.
    - Decision: this game was rendered by Copier from `biscuit_games_template`; the
      answers and the template commit are recorded in `.copier-answers.yml`, which is
      committed and never hand-edited except for `_src_path`. Every rendered file is one of
      two kinds. A managed file is re-rendered on `copier update` and merged three ways
      with the game's edits: template-changed and game-untouched takes the new render;
      game-changed and template-untouched keeps the game's; both changed in different
      hunks merge cleanly; the same hunk leaves inline `<<<<<<< before updating` and
      `>>>>>>> after updating` markers, where the template's side is a suggestion. A seed
      file is rendered once and is the game's: an update never merges, recreates or
      deletes one, and one the game deletes stays deleted. The seeds are exactly these
      fourteen patterns, listed in the record verbatim:

      ```text
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
      ```

      Managed files the game is expected to edit (`docs/manifest.yml`, `docs/README.md`,
      `AGENTS.md`, `Justfile`, `package.json`, `eslint.config.js`, `.gitignore`,
      `src/lib/config.ts` and the others CONVENTIONS.md §5 lists) follow one convention:
      the template inserts in the upper blocks and the game appends at the end, so the
      two sides land in different hunks. The frozen inventory: `docs/manifest.yml` and
      `docs/README.md` re-render on every update while seeds never do, so after its first
      release the template never adds, renames or retitles a seed page or a numbered
      decision; anything it later hands to games is a managed page, and a template
      decision is recorded in the template's own changelog. This game's own decisions
      start at 0011 and can never collide with one the template ships.
    - Consequences: managed pages say "this game" and never the name, which reaches the
      tree through `src/lib/brand.ts` and a few rendered pages; taking an update is
      commit everything, `uvx copier update --skip-answered`, resolve every marker,
      `just lock && just fix && just check`, commit with the answers file; a managed file
      the template stops rendering is removed from the game even where edited, announced
      in the template changelog under "Update notes" as a MAJOR release; same-hunk appends
      still conflict and an agent that tidies ordering recreates them; a departure that
      would suit every game belongs in the template, and one that is this game's alone is
      recorded in `AGENTS.md` under "Deliberate deviations" and in a decision here.
    - What would reopen this: the template stopping being maintained (the game keeps what
      it has and updates stop); Copier changing what `_exclude` sees during an update
      (`_min_copier_version` refuses an older copier, not a newer one); a game needing to
      rewrite a managed file wholesale, which the frozen inventory cannot turn into a seed.
    - Related pages: `../how-to/update-from-template.md` (row 13),
      `../reference/documentation-contract.md` (row 24), and 0010.

13. `0010-a-project-pages-site.md.jinja`, new, replacing Poodl's 0009 in the shape of P's
    records. `pages_url` is the only answer it substitutes, once, as the address; write
    the base path as `BASE_PATH=/<repository name>` in a code span, never as an answer.
    - Context: GitHub Pages serves a project site at `<owner>.github.io/<repository>/`
      (both in one code span; the account is lowercased in the host), and only a user
      site or a custom domain serves from a domain root. Poodl's record on its address
      chose a domain of its own, with a landing page in front of the game and a step that
      assembled the domain around the build; its own reopening clause was a second Biscuit
      Games game, because that shape put an address larger than the repository inside it.
      A rendered game has to publish on its first push with no domain, no DNS and nothing
      to stage.
    - Decision: this game is a project Pages site at the substituted `pages_url`.
      `.github/workflows/pages.yml` builds with `BASE_PATH=/<repository name>` read from
      the workflow event (`github.event.repository.name`) and uploads `build/`, so the
      file is identical in every game and never carries a name. `svelte.config.js` reads
      `BASE_PATH` into `paths.base` and it is empty locally (P line 22). `static/.nojekyll`
      rides along so Pages serves `_app/`. No custom domain: adding one later is a
      per-game change to the repository settings and to `BASE_PATH` in the workflow, an
      edit the game keeps through updates because it is game-changed and
      template-untouched.
    - Consequences: before the first push the Pages source is set to GitHub Actions (until
      then the deploy job fails with `Failed to create deployment (status: 404)`; P
      `docs/how-to/deploy-to-github-pages.md` 22-31) and the hub package grants the
      repository read access so the build job's token can install it; the address in the
      handbook is prose, decided by the `repository` answer, so a mismatch with the real
      repository is invisible to any gate while `pages.yml` stays correct, and
      `uvx copier update` re-asks the answer (CONVENTIONS.md §10 and §13); every path the
      app builds goes through `paths.base`; nothing outside `build/` is published, so
      there is no landing page, no second copy of a stylesheet and no staging script to
      keep true.
    - What would reopen this: a custom domain for this game; the platform serving games
      beneath a domain of its own.
    - Related pages: `../how-to/deploy-to-github-pages.md` (row 12),
      `../reference/configuration.md` (row 21), 0001, 0009.

14. `README.md.jinja`: P's `docs/decisions/README.md` with line 16, "These are decisions
    about *how* Poodl is built.", written with `{{ game_name }}` in place of "Poodl"; the
    table replaced by ten rows in the template's numbering, each linking its file and
    carrying the short title (the `title` after "Decision NNNN: "); a new section between
    "The record" and "Writing a new one", modelled on H's `docs/decisions/README.md` 45-51:

    ```markdown
    ## The numbering

    The ten entries above came with the template this game was rendered from, and eight
    of them were carried from Poodl, the first Biscuit Games game. Each of those says so
    under its heading and keeps the topic slug it had, because the slug is what a
    cross-repository reference names. The template never adds, renames or retitles a
    numbered decision after its first release, because this directory is the game's from
    the first commit and a template update never touches it;
    [Decision 0009](0009-rendered-from-the-template.md) says why. A decision this game
    takes is numbered 0011 onward and never collides with one the template ships.
    ```

    "Writing a new one" (P 38-42) and "Related pages" (P 44-47) stay verbatim.

15. Run every command under Verification and fix until each gives its expected outcome.
    Commit on the ticket branch, set `status: done` in this file in the same commit. **Authorisation required:** pushing
    the branch and opening the pull request are separately authorised actions
    (CONVENTIONS.md §11); stop and ask.

## Acceptance criteria

- [ ] Eleven files under `template/docs/decisions/`, no other file changed except this
  ticket's `status:` line.
- [ ] Each carried record's line 11 is the exact opening sentence of step 3 with the
  right Poodl number (0001 to 0004 same numbers; 0005 from 0006; 0006 from 0008; 0007 from
  0011; 0008 from 0013), and every carried record keeps its P `canonical_for` slug.
- [ ] Frontmatter of all eleven files equals the manifest entry; H1 equals `title`;
  each body has 40 or more words.
- [ ] Only `README.md.jinja` (`game_name`) and `0010-a-project-pages-site.md.jinja`
  (`pages_url`) contain Jinja; the render carries no `{{`, `{%` or `{#` under
  `docs/decisions/`.
- [ ] No forbidden token from step 2 anywhere under `template/docs/decisions/`; no link
  to a Poodl-only record or page; every relative link resolves in a render.
- [ ] The index has ten rows, "The numbering" states the frozen-inventory rule and the
  0011 start, and "Writing a new one" is P's verbatim.
- [ ] 0009 lists the fourteen seed patterns exactly as CONVENTIONS.md §3 spells them;
  0010 names the address once through `pages_url` and no literal domain.
- [ ] `just check` green in the template repository; `validate_docs.py` exits 0 in a
  render; `markdownlint-cli2` clean over the rendered `docs/decisions/`.

## Verification

From the template repository root.

```sh
just check
```

Expected: `lock-check`, `lint`, `typecheck` and `test` all green; in `test`,
`tests/test_validators.py` and `tests/test_render.py::test_no_poodl_outside_provenance`
pass.

```sh
rm -rf ai_tmp/render && just render
python3 ai_tmp/render/scripts/validate_docs.py
```

Expected: exit 0; the hub's version of the script (T02) prints
`Validated 38 pages and <n> canonical topics.`, and until T02 merges the stub copy T00
shipped may word it differently. The validator derives its root from its own path, so no
`just initialize` is needed for this check.

```sh
cd ai_tmp/render && npx --yes markdownlint-cli2@0.23.2 "docs/decisions/*.md"
```

Expected: no findings, exit 0 (the render's own `.markdownlint-cli2.jsonc` applies).

```sh
grep -rniE 'pnut|site-root|stage_site|stage-preview|word[ -]list|words\.allium|daily\.allium|sharing\.allium|statistics\.allium|foo/www|/Users/' template/docs/decisions/ || echo clean
grep -lE '\{\{|\{%|\{#' ai_tmp/render/docs/decisions/*.md || echo clean
for f in template/docs/decisions/000[1-8]-*.md; do sed -n '11p' "$f"; done
```

Expected: `clean` twice, then eight lines each beginning `*Carried from Poodl's decision`.

```sh
cd ai_tmp/render && git init -q -b main && just initialize && just check-docs
```

Expected: exit 0. This needs the network and a `read:packages` token in `~/.npmrc`
(CONVENTIONS.md §11 "Credentials"); it is not a separately authorised action, but if it
cannot run, say so in the hand-back notes and rely on the two offline checks above.

## Hand-back notes

**What was verified and how.**

- `just check`, exit 0. `uv lock --check` resolved 33 packages; every prek hook reported
  Passed (Ruff lint and format, the builtin checks including merge conflicts,
  EditorConfig, markdownlint, typos, lychee, shellcheck, actionlint, ripsecrets); mypy
  printed `Success: no issues found in 6 source files`; pytest printed
  `27 passed, 16 warnings in 11.44s`, 23 in `tests/test_render.py` (among them
  `test_no_poodl_outside_provenance` and `test_managed_pages_link_only_to_stable_pages`)
  and 4 in `tests/test_validators.py`. The warnings are Copier's `DirtyLocalWarning`.
- `rm -rf ai_tmp/render && just render`, then `python3 ai_tmp/render/scripts/validate_docs.py`:
  `Validated 38 pages and 39 canonical topics.`, exit 0.
- `npx --yes markdownlint-cli2@0.23.2 "docs/decisions/*.md"` in the render:
  `Linting: 68 files` and `Summary: 0 issues in 0 files`, exit 0. The render's config adds
  its own `**/*.md` glob, so the run covers every page.
- The forbidden-token grep printed `clean`, and so did the rendered-delimiter grep. The
  line-11 loop printed eight lines, each the step 3 sentence, naming Poodl's 0001, 0002,
  0003, 0004, 0006, 0008, 0011 and 0013 in that order.
- `game_name` occurs once in `README.md.jinja` and renders once; `pages_url` occurs once
  in 0010 and renders as `https://steven-cutting.github.io/tic_tac_toe_beans/` inside a
  code span. The only other `github.io` in the directory is the
  `<owner>.github.io/<repository>/` pattern.
- The network run happened. `git init -q -b main && just initialize` exited 1 at
  `npm run lint:fix`, after `npm ci`, Chromium and allium 3.6.1 had installed and before
  `install-hooks`: ESLint `@typescript-eslint/restrict-template-expressions` at
  `stories/Lockup.stories.svelte:83:31`. `just check-docs` then exited 0, but prek skipped
  markdownlint, typos and lychee with `(no files to check)`, because the fresh repository
  tracked nothing. After `git add -A` in the render, `just check-docs` reported
  markdownlint, typos and lychee Passed and `Validated 38 pages and 39 canonical topics.`,
  exit 0. `npx prettier --check docs/decisions/` printed
  `All matched files use Prettier code style!`; `*.md` is in the render's `.prettierignore`.
- A word-level `git diff --no-index` of each carried record against P's at `0a46a485`
  shows only the edits steps 3 to 10 name.

**What deviated from the ticket and why.**

- Every P line range in steps 4 to 11 matched the paragraph the step describes; no number
  or content differed.
- Step 9: the no-token sentences extend the paragraph ending "Chromatic is not a required
  check." rather than starting a new one, because "either" reads back to that sentence.
- Step 11 gives bullets rather than text, so 0008's prose is new. P's "written down in
  three places, including the troubleshooting page" became "written down where a first
  run meets it, including the troubleshooting page", because the count across T07's and
  T08's pages cannot be checked from this lane. P 0013 lines 21-26 are summarised without
  naming Poodl's modules, and the Decision's lead sentence ends "and restate only what this
  game has a surface for" in place of P's "and delete every copy it makes redundant".
- Step 12: 0009 writes out every managed file a game is expected to edit, because a game
  has no CONVENTIONS.md to point at. It names both conflict markers without saying which
  side each bounds, and keeps them mid-line in code spans so no line starts with one (the
  template's `check-merge-conflict` hook). "An update refuses a dirty worktree" comes from
  CONVENTIONS.md §10. The link to the update procedure sits in Related pages, not the body.
- Step 13: 0010 writes `github.event.repository.name` bare in a code span, since the
  workflow expression syntax would be read as Jinja in a `.jinja` file. One sentence is
  added to the `paths.base` consequence: a root-relative path works locally and breaks
  once published beneath the repository's name. The re-asked answer comes from §10.
- Kept verbatim as steps 5 and 8 direct, though they read slightly past a template game:
  0002 still says "no `navigator.clipboard` at all" and "both real code paths" while the
  template ships no clipboard port (CONVENTIONS.md §4 "Not shipped"); 0002 and 0005 still
  say "the domain" with no `src/lib/domain/` shipped; 0005 keeps the TypeScript 5.x and
  6.x detail. A game that finds one untrue edits its own seed copy.
- No `CHANGELOG.md` entry for the seed change: no game has been rendered before `v0.1.0`,
  this ticket touches no other file, and the changelog is T12's.
- The ticket's `branch:` is `ticket/t09-decisions`; the worktree was created on
  `T09-decisions`, and the commit is there.

**What was handed back to another ticket.**

- Nothing. The manifest's eleven entries already equal the frontmatter, every link target
  is a shipped page (the validator's link check passed in the render), and no allowlist
  in `tests/test_render.py` needs to change.
- The `just initialize` abort is `stories/Lockup.stories.svelte` line 83, T05's file
  (step 9 and its `FRAME_WIDTH`). T00's hand-back notes already record the same ESLint
  error, so no new hand-back is raised; the networked documentation check was completed by
  running `just check-docs` directly on the staged render.

**Which open points were settled, and how.**

- CONVENTIONS.md §12 assigns nothing here, and nothing was checked under it.
- `test_managed_pages_link_only_to_stable_pages` admits targets matching
  `fnmatchcase(resolved, "docs/decisions/*.md")` (`tests/test_render.py` line 275), which
  includes `decisions/README.md`, 0009 and 0010 as well as the carried records. No T00
  follow-up.
- The manifest names 0009 "Decision 0009: Rendered from the template" and 0010
  "Decision 0010: A project Pages site", both with audience
  `[contributor, maintainer, agent]`; the files carry those values unchanged.
- typos flags nothing: the template's `just lint` ran it over all eleven sources and the
  render's `check-docs` ran it over the rendered pages. No `extend-words` entry is needed,
  so nothing goes to T01.

## Open points

- CONVENTIONS.md §12 assigns no unverified claim to this ticket.
- `test_managed_pages_link_only_to_stable_pages` (T00, `tests/test_render.py`) is stated
  for "managed pages and carried decisions". Whether its stable set includes
  `decisions/README.md`, 0009 and 0010 decides if `AGENTS.md` may link to the index and
  if T07's `how-to/update-from-template.md` may link to 0009. Check: read the test's
  allowlist in your worktree; if the three are excluded, hand back a T00 follow-up asking
  for all ten records and the index, since a game never deletes them either.
- The titles and audiences of 0009 and 0010 are whatever T00 wrote into the manifest.
  Check: `grep -n 'decisions/00\(09\|10\)' template/docs/manifest.yml`; if T00 chose
  words other than "Rendered from the template" and "A project Pages site", use the
  manifest's and note it.
- Whether the render's `typos` hook flags a word in a record (CONVENTIONS.md §12 names
  this for T11 on the slug; a decision record is another place it could bite). Check: the
  `just check-docs` run above; the remedy is an `extend-words` entry in the game's
  `pyproject.toml`, which is T01's file, so hand it back.
