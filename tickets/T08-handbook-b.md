---
id: T08
title: Handbook B: explanation, reference and operations pages
status: open
depends_on: [T00]
parallel_with: [T01, T02, T03, T04, T05, T06, T07, T09]
branch: ticket/t08-handbook-b
estimated_size: L
---

# T08: Handbook B: explanation, reference and operations pages

## Context

The rendered game ships a 38-file handbook (CONVENTIONS.md §8). T00 has merged and left
a stub for every page: frontmatter equal to `template/docs/manifest.yml`, a matching H1
and forty or more words, so the fast suite is green before any lane starts. This ticket
replaces the fourteen stubs under `template/docs/explanation/`,
`template/docs/reference/` and `template/docs/operations/` (CONVENTIONS.md §8 rows 14
to 27) with the real pages. T07 rewrites the project, tutorial and how-to pages and T09
the decisions in parallel; T10 waits for all three. Links from this lane into those
lanes' pages resolve today because T00's stubs exist at every path.

Every page here is **managed** (class M): re-rendered and 3-way merged by
`copier update` (CONVENTIONS.md §5). None is `.jinja`, so none may reference an answer:
the pages say "this game" or "the game" and never a name, a slug or an address
(CONVENTIONS.md §4, the rule after the tree). Thirteen are Poodl's page of the same
path made generic; `accessibility.md` is derived from the hub's page instead.

Read first, at the pinned commits (CONVENTIONS.md §0):

- CONVENTIONS.md §4, §5, §7 (what the seed source, ports, tests and story contain,
  which these pages describe), §8 (the page table and the link rule), §9 (the harness
  tests that judge the render), §11.
- P `docs/explanation/*.md`, `docs/reference/*.md`, `docs/operations/*.md` (the
  thirteen sources) and H `docs/explanation/accessibility.md` (344 lines, row 17).
- H `scripts/validate_docs.py` lines 32 to 43 (`MINIMUM_WORDS`, `BAD_CONTENT`) and 191
  to 219 (what a page must satisfy). The template ships this validator.
- P `docs/manifest.yml` lines 22 to 27, 29 to 34 and 36 to 37: the fourteen entries T00
  copied into the template manifest, the frontmatter authority.
- P `Justfile` (the template's is P minus lines 68 to 79), P `vite.config.ts` lines 18
  to 29 (`include`, coverage), P `tests/platform.ts` lines 25 to 34 (`platformPath`
  refuses a path outside `node_modules`), H `eslint.config.js` (the template's; no rule
  overrides, unlike P lines 42 to 57).

## Goal

Fourteen rendered pages that read as this game's handbook and pass every gate: the
render's `validate_docs.py` exits 0, `just check-docs` is green in a render, and in the
template repository `just test` passes with `test_validators.py`,
`test_managed_pages_link_only_to_stable_pages` and `test_no_poodl_outside_provenance`
green. `quality-gates.md` keeps Poodl's gate table and "On `main`" section verbatim;
`documentation-contract.md` gains one section on managed versus seed pages;
`agent-contract.md` states the bridge rule the shipped validator enforces;
`accessibility.md` is a trimmed derivation of the hub's page stating what a game owes.

## Non-goals

- `template/docs/manifest.yml` and `template/docs/README.md.jinja` (T00). A page whose
  title, audience or topic slug has to change is handed back, not renamed here.
- Project, tutorial and how-to pages, `README.md.jinja`, `CHANGELOG.md.jinja`,
  `SECURITY.md` (T07); decision records (T09).
- `scripts/validate_docs.py` (T02) and the harness tests in `tests/` (T00, T10).
- Turning any page here into `.jinja`, or substituting an answer anywhere in this lane.
- Pushing, opening a pull request, tagging (CONVENTIONS.md §11).

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `template/docs/explanation/architecture.md` | M | `P docs/explanation/architecture.md` | Generic; no reducer layer; two-row state table; five ports, three here; no seed link |
| `template/docs/explanation/layering.md` | M | `P docs/explanation/layering.md` | Tier B. Three layers; five ports, three here; no reducer |
| `template/docs/explanation/specifications.md` | M | `P docs/explanation/specifications.md` | One root module; generic "stated once" example; no seed link |
| `template/docs/explanation/accessibility.md` | M | `H docs/explanation/accessibility.md` | Tier B. Trimmed to what a game owes; content embedded below |
| `template/docs/explanation/security-model.md` | M | `P docs/explanation/security-model.md` | Drop custom-link paragraph and decision 0005; no seed link |
| `template/docs/explanation/quality-philosophy.md` | M | `P docs/explanation/quality-philosophy.md` | ESLint and coverage prose made true for the hub config; `localStorage` only |
| `template/docs/reference/commands.md` | M | `P docs/reference/commands.md` | Drop `stage` and `stage-preview` rows |
| `template/docs/reference/configuration.md` | M | `P docs/reference/configuration.md` | Project-site base path; six platform figures; no staging |
| `template/docs/reference/testing.md` | M | `P docs/reference/testing.md` | Suite table = managed tests plus the seed suite; lockup worked example |
| `template/docs/reference/quality-gates.md` | M | `P docs/reference/quality-gates.md` | Gate table and "On `main`" verbatim; decision links renumbered; five prose edits |
| `template/docs/reference/documentation-contract.md` | M | `P docs/reference/documentation-contract.md` | Verbatim plus one section on managed and seed pages |
| `template/docs/reference/agent-contract.md` | M | `P docs/reference/agent-contract.md` with H's skill and bridge sections | P 37-58 replaced by H 42-84; two edits inside |
| `template/docs/operations/maintenance.md` | M | `P docs/operations/maintenance.md` | Tier B. Word-list paragraph replaced by a template-update one; generic base path |
| `template/docs/operations/troubleshooting.md` | M | `P docs/operations/troubleshooting.md` | Drop staging and domain lines; generic base path; 401 section kept |

## Steps

1. Create the worktree on `ticket/t08-handbook-b` from `main` (README.md in `tickets/`
   gives the command). Run `just test` once before editing and keep the output: the
   suite is green with T00's stubs, and every failure after this point is yours.
2. Read the frontmatter authority. Every page's frontmatter must equal its manifest
   entry key for key, list order included, and the H1 must equal `title` byte for byte
   (H `validate_docs.py` lines 201 to 215). The fourteen entries are Poodl's, unchanged:

   | Page | `title` | `audience` | `canonical_for` |
   | --- | --- | --- | --- |
   | `explanation/architecture.md` | Architecture | contributor, maintainer, operator, agent | system_architecture |
   | `explanation/layering.md` | Layering and dependency direction | contributor, maintainer, agent | dependency_boundaries |
   | `explanation/specifications.md` | Specifications | contributor, maintainer, agent | specification_model |
   | `explanation/accessibility.md` | Accessibility | user, contributor, maintainer, agent | accessibility_model |
   | `explanation/security-model.md` | Security model | user, contributor, maintainer, operator, agent | security_model |
   | `explanation/quality-philosophy.md` | Quality philosophy | contributor, maintainer, agent | quality_philosophy |
   | `reference/commands.md` | Commands | contributor, maintainer, operator, agent | command_reference |
   | `reference/configuration.md` | Configuration | contributor, maintainer, operator, agent | configuration_reference |
   | `reference/testing.md` | Testing | contributor, maintainer, agent | testing_reference |
   | `reference/quality-gates.md` | Quality gates | contributor, maintainer, agent | quality_gate_reference |
   | `reference/documentation-contract.md` | Documentation contract | contributor, maintainer, agent | documentation_contract |
   | `reference/agent-contract.md` | Agent contract | contributor, maintainer, agent | agent_contract |
   | `operations/maintenance.md` | Maintenance | maintainer, operator, agent | maintenance_routine |
   | `operations/troubleshooting.md` | Troubleshooting | contributor, maintainer, operator, agent | troubleshooting |

   `kind` is the directory name; `requires` is `[]` everywhere. Confirm each row with
   `grep -n '<path>' template/docs/manifest.yml` before writing, and hand back any
   difference rather than editing the manifest.
3. Apply these rules to every page; the render's validator and the fast suite enforce
   each one:
   - Frontmatter as in step 2: five keys, inline lists, no duplicate key. Body of forty
     or more words, first heading level one and equal to the title.
   - None of `{{`, `{%` or `{#`; no unfinished marker and no placeholder prose
     (`BAD_CONTENT`, H `validate_docs.py` lines 36 to 43).
   - Relative links only to files that exist in the render, with exact case. A managed
     page links only to managed pages and to the carried decisions `0001` to `0008`
     (CONVENTIONS.md §8, `test_managed_pages_link_only_to_stable_pages`): no link to
     `project/purpose-and-scope.md`, `project/terminology.md`, anything under
     `docs/specs/`, decisions `0009` and `0010`, or a Poodl decision that does not exist
     here (`0005-obfuscation-not-security.md`, `0007-rules-as-a-reducer.md`, and Poodl's
     `0009` to `0013`). Surviving decision links are renumbered: Poodl 0011 is
     `0007-project-managed-allium-cli.md`, Poodl 0013 is
     `0008-design-system-as-a-package.md`, Poodl 0008 is
     `0006-visual-review-in-chromatic.md`; 0001, 0002 and 0003 keep their numbers.
   - No name: "this game" or "the game" in place of Poodl, no slug, no address. The
     harness refuses, case-insensitively, `poodl` outside its allowlist (none of these
     pages is on it) and `pnut`, `site-root`, `stage_site`, `stage-preview`,
     `word list`, `word-list`, `words.allium`, `daily.allium`, `sharing.allium`,
     `statistics.allium`, `foo/www` and `/Users/` anywhere. Treat `game.allium` and
     `settings.allium` the same way: they are Poodl's modules and do not exist here.
   - Every page keeps a `## Related pages` list, pruned to targets the rule above
     allows.
   - A placeholder for the repository name goes inside a fenced `console` block
     (`BASE_PATH=/<repository name>`) or is written in words; the render's markdownlint
     allows no inline HTML but `br`.
4. Rewrite each page as its subsection below specifies. "Verbatim" means byte for byte
   from P at commit `0a46a485`; "P a-b" names line numbers there, each verified against
   that commit. Overwrite the whole stub each time.
5. Tier B (`layering.md`, `accessibility.md`, `maintenance.md`) is the first to cut if
   the ticket runs long. "Cut" means: leave T00's stub untouched (it already passes every
   gate), list the page under hand-back notes as carried forward with the reason, and
   leave its row in the table above as the follow-up's scope. Never partially rewrite a
   tier B page.
6. Run the checks in Verification, at source and in a render, and fix until clean.
   `just check` must be green in the template repository.
7. Commit on the ticket branch with the ticket's `status:` set to `done` and the
   hand-back notes filled in. **Authorisation required:** pushing the branch and opening
   the pull request. Stop and ask.

### `explanation/architecture.md`

P `docs/explanation/architecture.md`, 106 lines. Edits:

- P 11 "Poodl is a static site." becomes "This game is a static site."
- P 26-27 "drawing an answer, reading stored statistics, looking at the clock" becomes
  "drawing a random value, reading device storage, looking at the clock".
- P 30-32 become: "The build is portable across base paths. SvelteKit emits relative
  asset URLs, and `paths.base` is read from `BASE_PATH` at build time, which `pages.yml`
  sets from the repository name, so a local build and the deployed build differ in that
  value alone."
- P 36-42, the tree, becomes three levels: `routes/` "assembles the page, and is the
  only place a port is built", `components/` "renders and handles interaction",
  `ports/` "every side effect, behind an interface". Follow it with: "`src/lib/config.ts`
  and `src/lib/brand.ts` sit beneath all three and import nothing."
- P 47-53 (the `app/` paragraph and the decision 0007 link) become: "There is no rules
  layer yet: the seed tree is a route, a lockup component and three ports. When this
  game has rules, they belong in pure modules under `src/lib/` between the components
  and the ports, fed their clock and randomness as arguments rather than imports, so
  that the whole of the behaviour is testable without a browser."
- P 59 "an older Poodl" becomes "an older release of this game".
- P 62-69, the state table, becomes two rows: "Whatever this game keeps between visits,
  such as a game in progress or its settings" living in "Device storage, through the
  storage port, under one key with a schema version inside it", lost when "Browser data
  is cleared"; and "Whatever the game is saying at the moment" living "Nowhere at all",
  lost when "The page is reloaded". Drop P 71-78.
- P 82-92 become:

  ```markdown
  Five things reach outside the pure core: storage, randomness, the clock, the device's
  colour-scheme and reduced-motion preferences, and the device's keyboard. Each sits
  behind a port with a real adapter and an in-memory fake, so the entire application
  above them is testable without a browser. The first three are in `src/lib/ports/`; the
  last two are the platform's and arrive from `@steven-cutting/biscuit-games`. A side
  effect this game adds gets a port there in the same shape. The reasoning is in
  [Decision 0002](../decisions/0002-ports-and-fakes.md).
  ```

- P 96-98: replace the link with the words "as this game's purpose-and-scope page
  records" (a seed page; no link).
- Related pages: drop P 103 (decision 0007). Keep the other four.

### `explanation/layering.md`

P `docs/explanation/layering.md`, 94 lines. Tier B. Edits:

- P 11 becomes "Three layers, and imports only ever run downwards."
- P 13-20, the table, becomes four rows: `src/routes/` may import "components, ports,
  brand, config" and must not "be imported by anything below it";
  `src/lib/components/` may import "components, brand, config, platform types" and must
  not "import a port adapter or reach for a browser global"; `src/lib/ports/` may import
  "config" and must not "import a component or a route";
  `@steven-cutting/biscuit-games` may import "nothing here" and must not "be copied back
  into `src/`".
- P 22-25 become: "`src/lib/config.ts` and `src/lib/brand.ts` sit below everything and
  import nothing. The package is below every layer: it is a dependency, so anything may
  name it and it names nothing here."
- P 27-37 become: "There is no rules layer yet. When this game has rules, they go in
  pure modules under `src/lib/` between the components and the ports, and the
  components row already says what a component may do with them: name a type, render a
  value, and call the callback it was handed. A component may not construct a port,
  reach for a browser global, or keep a fact the rules own as view state of its own."
- P 41-42: "the two claims below" becomes "the claims below". Drop P 44-51; keep P
  53-57.
- P 69-72 become: "There are five, and three of them are here: storage, randomness and
  the clock. The device's preferences and the device's keyboard are the platform's,
  taken from `@steven-cutting/biscuit-games` with the fakes it ships, because what a
  surface reads from a device is not one game's question." P 76 "all eight" becomes
  "all five".
- P 84-87 become: "There is no import-boundary checker here: a three-directory frontend
  does not earn the machinery. The direction is enforced by review, by the
  `svelte-change` and `code-review` skills, and by the shape of the tests: code in the
  wrong layer is usually code that is hard to test."
- Related pages: drop P 94 (decision 0007).

### `explanation/specifications.md`

P `docs/explanation/specifications.md`, 84 lines. Edits:

- P 11-13 become: "This game's behaviour is written down, in a formal language, before
  it is built. The Allium modules under `docs/specs/`, rooted at the module named after
  this game, are the source of truth for what the game does. This handbook, the code and
  the tests all answer to them."
- P 18-31 (the scoring example) become a generic "stated once" example under the same
  heading: a figure such as the minimum touch target is stated once, in
  `operation.allium`'s `config` block as 44, restated by name in this game's root
  module, mirrored once in `src/lib/config.ts`, and held equal across the three by
  `tests/platformSpecs.test.ts`; a control drawn at 40 pixels fails on the number rather
  than on a reviewer's eye. Left to prose, a figure like that drifts; stated as a
  contract with a named guarantee, it is testable. Quote nothing from Poodl's modules.
- P 33-51 (the module graph) become, under the same heading:

  ```markdown
  One is the game's today: the root module under `docs/specs/`, named after this game,
  which [the documentation map](../README.md) names. It states the six figures the
  platform states, so `tests/platformSpecs.test.ts` can hold the two equal, and one
  surface with one guarantee, so the specification is checked rather than merely
  present. Modules this game adds import it. The platform's own three,
  `appearance.allium`, `operation.allium` and `play-surfaces.allium`, ship inside
  `@steven-cutting/biscuit-games` and are not imported: Allium has no cross-repository
  import, so a clause this game restates is held to the platform's text by test instead.
  ```

- Keep P 55-58 and 68-70; drop P 60-66 (Poodl's twenty questions).
- P 74-77 become: "It is not a design document, and it does not choose a language, a
  framework, a storage mechanism or a layout. A module states what any implementation
  must satisfy and describes no scheme for satisfying it. How is this repository's
  business; `AGENTS.md` decides that."
- Related pages: drop P 83 (terminology, a seed page); keep 81, 82 and 84.

### `explanation/accessibility.md`

Derived from H `docs/explanation/accessibility.md` (344 lines), not from P's 299-line
game page. Tier B. Hub facts used: six `@guarantee` clauses on `Appearance` (H 11-15; H
`docs/specs/appearance.allium` lines 134 to 175), colour (H 71-75), the floor in four
combinations (H 88-95), the device winning on contrast and motion (H 107-108, 126-128),
keyboard (H 183-184), 44 and 320 (H 207-208; `operation.allium` lines 96 and 101),
`AMarkIsNeverOnlyAColour` (H 80; `play-surfaces.allium` line 151), role-and-name
queries (H 289-291), axe in error mode (H 299-301), what axe skips (H 312-319), what
needs a person (H 327-336).

- Write the page as follows, exactly:

  ```markdown
  ---
  title: "Accessibility"
  kind: "explanation"
  audience: [user, contributor, maintainer, agent]
  canonical_for: [accessibility_model]
  requires: []
  ---

  # Accessibility

  Accessibility is specified, not retrofitted. The platform package
  `@steven-cutting/biscuit-games` ships three Allium modules, and their clauses are
  acceptance criteria for any change that touches a surface here. `appearance.allium`
  carries six `@guarantee` clauses on its `Appearance` surface; `operation.allium` states
  keyboard operability, visible focus, announcement, and the figures every control has to
  meet; `play-surfaces.allium` states that a mark is never only a colour. None of the
  three imports anything, so this game inherits the obligations whole rather than
  restating them, and owes an account of whatever it adds on top.

  ## What the platform decides

  **Colour never carries meaning alone.** Every state a colour helps to show also carries
  a shape, a word, or both, and has an accessible name that says it in words. This holds
  in every theme and in both palettes.

  **The legibility floor holds in all four combinations of theme and high contrast.**
  Text reaches `config.minimum_text_contrast` (4.5) against what is behind it; a control's
  boundary reaches `config.minimum_boundary_contrast` (3.0) against the page. High
  contrast is a second palette that clears the same bar, not the place legibility is
  finally attended to.

  **Everything is keyboard operable, and every control is big enough to hit.** 44 CSS
  pixels in both directions, down to the 320-pixel viewport that is the narrowest
  supported width. `src/lib/config.ts` mirrors those figures from the module that states
  them, and `tests/platformSpecs.test.ts` holds the mirror to the shipped text.

  **The device wins.** More contrast asked of the operating system turns high contrast
  on, and a reduced-motion preference stops every animation whatever the setting says.

  ## What this game owes

  - A non-colour indication and an accessible name for every state it adds beyond the
    platform's marks, in the words its own specification uses.
  - A stated distance between two of its own states that sit side by side. No standard
    supplies one, so the game states the figure and measures it.
  - The sentence each mark is read out as, arriving at the call site rather than being
    inferred.
  - Proof of what only it renders. The platform measures its palette and its primitives
    in its own workshop; this game's stories measure its arrangements, framed at the
    narrowest width, with axe over every render.

  ## How this is checked

  By test, not by audit. Component tests query by accessible role and name, never by
  class or test id, with one bounded exception for an element that is `aria-hidden`
  because the words beside it already say the same thing. `.storybook/preview.ts` sets
  the accessibility addon's test mode to `error`, so a violation fails
  `just storybook-test` rather than being reported. A gate's silence is not a pass: axe
  never checks contrast behind `aria-hidden`, downgrades any single-character text to
  *incomplete*, and answers `target-size` at 24 pixels rather than 44. Focus order,
  announcement timing and a palette on a phone at minimum backlight still need a person.
  The `accessibility-review` skill in `.agents/skills/` is the procedure.

  ## Related pages

  - [Specifications](specifications.md)
  - [Testing](../reference/testing.md)
  - [Work in the component workshop](../how-to/work-in-the-component-workshop.md)
  - [Work with the specifications](../how-to/work-with-the-specs.md)
  - [Decision 0005](../decisions/0005-component-workshop.md)
  ```

### `explanation/security-model.md`

P `docs/explanation/security-model.md`, 95 lines. Edits:

- P 11 "Poodl has no server" becomes "This game has no server".
- P 21-22 "Statistics, settings and the current game live in device storage and are
  never uploaded." becomes "Whatever the game keeps, its settings and a game in
  progress, lives in device storage and is never uploaded."
- P 25 "not to Poodl" becomes "not to the game".
- P 33-35 become: "The practical consequence for a player is that clearing browser data
  destroys whatever this game kept for them, irrecoverably. That is a real cost of the
  design, and the game's own purpose-and-scope page is where it is stated." (no link).
- Keep the heading at P 37. Drop P 39-43 (the custom-link paragraph and its decision
  0005 link). P 45-47 become: "**Nothing prevents a player cheating themselves.**
  Whatever this game holds in memory or in device storage, a player with developer
  tools can read. There is no opponent and no leaderboard, so there is nobody to cheat
  but themselves."
- P 49-95 verbatim.

### `explanation/quality-philosophy.md`

P `docs/explanation/quality-philosophy.md`, 70 lines. The template's `eslint.config.js`
is the hub's, which carries none of P's two rule overrides, so P 33-36 would describe a
file that does not exist. Edits:

- P 32-36 become: "Where a rule is genuinely wrong for this project, the fix is to
  configure it once, in the config file, with a comment saying why. `eslint.config.js`
  carries no such override today: the seed passes `strictTypeChecked` as shipped, and a
  number reaching a template literal goes through `String()` rather than through an
  `allowNumber` exception. The first override this game adds is a project decision,
  recorded where the rule lives."
- P 40-48 become: "Coverage distinguishes two things that look alike. A branch no input
  can reach is not a gap in the tests; it is code that should not exist, whether a
  bounds check after a modulo, a null fallback after an exhaustive assignment, or a
  defensive default no caller can trigger. Delete it rather than cover it with a
  contrived test. The corollary: do not chase the last few percent. The floor is 90,
  and in a fresh render the denominator is small, three ports and about fourteen branch
  sites, so an untested constants file or a branch in a component nothing renders can
  breach the floor on its own."
- P 58-59 "no `localStorage` and no `navigator.clipboard` at all" becomes "no
  `localStorage` at all".
- Everything else verbatim.

### `reference/commands.md`

P `docs/reference/commands.md`, 95 lines. Drop P 40-41 (the `just stage` and
`just stage-preview` rows). Everything else verbatim: every remaining recipe exists in
the template `Justfile` (P minus lines 68 to 79), `check-links-online` and `check-clean`
included.

### `reference/configuration.md`

P `docs/reference/configuration.md`, 153 lines. Edits:

- P 18, the `BASE_PATH` row: the effect becomes "Where this game sits beneath its host,
  read into `paths.base`. The Pages workflow sets it to a slash followed by the
  repository name, from the workflow event, because a project site is served beneath
  that name; left empty for local builds."
- P 24-48 become: "`BASE_PATH` is read twice, not once. `svelte.config.js` reads it into
  `paths.base` for the build, and the preview server reads it to decide where it mounts
  the output. So it belongs on both commands that touch the deployment:", then a
  `console` block with `BASE_PATH=/<repository name> just frontend-build` and
  `BASE_PATH=/<repository name> just preview`, then "Build with it and preview without
  it and the site comes up at `/` rather than beneath the repository name, which is not
  the path Pages serves, so the preview is not the deployment.", then P 42-45 verbatim.
- P 72, the governs cell, becomes "Flat config on `strictTypeChecked`, the Svelte and
  Storybook presets, and no rule overrides yet."
- P 78 becomes "Notably excludes Markdown, which markdownlint owns, and
  `.copier-answers.yml`, which Copier rewrites on every update."
- P 95 "which swaps the correct and present colours" becomes "which swaps in the
  high-contrast palette".
- P 98-137 become, exactly:

  ```markdown
  ## Values the specifications decide

  `src/lib/config.ts` mirrors the `config` blocks in `docs/specs/`. These are not tunables:
  changing one here without changing it in the specification is drift. All six are the
  platform's, stated in the modules `@steven-cutting/biscuit-games` ships and restated by
  name in this game's root module; `tests/platformSpecs.test.ts` holds this file, that
  module and the shipped text equal. A figure this game alone states belongs below these,
  mirrored from the module that states it, and a constant that appears here without a
  `config` entry to name is drift in the other direction.

  | Constant | Value | Specification |
  | --- | --- | --- |
  | `MINIMUM_TEXT_CONTRAST` | 4.5 | `appearance.allium`, `config.minimum_text_contrast`, a contrast ratio |
  | `MINIMUM_BOUNDARY_CONTRAST` | 3.0 | `appearance.allium`, `config.minimum_boundary_contrast`, a contrast ratio |
  | `MINIMUM_TOUCH_TARGET` | 44 | `operation.allium`, `config.minimum_touch_target`, in CSS pixels |
  | `NARROWEST_SUPPORTED_WIDTH` | 320 | `operation.allium`, `config.narrowest_supported_width`, in CSS pixels |
  | `MINIMUM_STATE_SEPARATION` | 3.0 | `play-surfaces.allium`, `config.minimum_state_separation`, a contrast ratio |
  | `MINIMUM_MARK_SEPARATION` | 2.0 | `play-surfaces.allium`, `config.minimum_mark_separation`, a contrast ratio |

  `MINIMUM_TOUCH_TARGET` and `NARROWEST_SUPPORTED_WIDTH` are the two whose real consumer
  is a stylesheet, and CSS cannot import a TypeScript constant. Both figures are written
  out in the platform's stylesheet, so the story run is what holds this repository's
  constants to them: it frames the header at `NARROWEST_SUPPORTED_WIDTH` and measures
  every control there against `MINIMUM_TOUCH_TARGET`. The specification is held to the
  platform's separately, by `tests/platformSpecs.test.ts`, so a figure that moved upstream
  fails on the number rather than on the paint.
  ```

- Everything else verbatim, Related pages included.

### `reference/testing.md`

P `docs/reference/testing.md`, 168 lines. The render's tests are `ports.test.ts` and
`platformSpecs.test.ts` (managed), `lockup.test.ts` and `route.test.ts` (seed), with
`platform.ts` and `restated.ts` as helpers and one story (CONVENTIONS.md §7). Edits:

- P 26-29 become: "Tests live in `tests/`, never colocated with `src/`. Stories live in
  `stories/`, also at the repository root, one file per component."
- P 37-43 become: "Files are named for what they cover rather than mirroring a source
  path: `ports.test.ts`, `platformSpecs.test.ts`, `lockup.test.ts`, `route.test.ts`."
  then: "Two files in `tests/` are not tests. `platform.ts` resolves what the package
  ships through its own `exports` subpaths and refuses any path outside `node_modules`,
  because a resolve that fell back to a copy in this repository would stay green while
  proving nothing about the package this game actually installs. `restated.ts` is this
  game's table of the platform clauses its modules restate, empty until it restates
  one. The `include` glob is `tests/**/*.test.ts`, so both are imported and never
  collected."
- P 51-54, the example block, becomes two lines:
  `screen.getByRole('heading', { level: 1 });` and `screen.getByRole('main');`.
- P 80-90 become: "The lockup is the worked example of the split. The platform's
  `Wordmark` draws a mark beside the words and hides it with `aria-hidden`, so the
  role-and-name convention cannot reach it; `tests/lockup.test.ts` queries the mark by
  its text and asserts it is hidden, and queries the words to assert they read
  `biscuit games /` followed by this game's name. jsdom holds that the mark is there and
  silent; that the words collapse below about 26rem is the platform's, measured in the
  workshop upstream. What this repository holds is what it renders."
- P 109-132, the suite table, becomes five rows: `ports.test.ts` covers "The three ports
  here, storage, randomness and the clock: real adapter and fake, including the failure
  paths an unusable store produces. Managed by the template; a port this game adds gets
  its cases appended at the end."; `platformSpecs.test.ts` covers "The six figures
  `src/lib/config.ts` mirrors, held equal to the modules `@steven-cutting/biscuit-games`
  ships and to any module under `docs/specs/` that states them; and every clause
  `tests/restated.ts` lists, held to the platform's text word for word.";
  `lockup.test.ts` covers "That the lockup names this game after the platform, with the
  mark silent. This game's file."; `route.test.ts` covers "The page: the heading the
  platform header draws for this game, and a main landmark to put the game in. This
  game's file."; `stories/` covers "Each component in the states its surface names,
  rendered in Chromium with axe over every one, and the figures only a layout engine
  can produce: the seed story frames the header at the narrowest supported width and
  measures the control there."
- Drop P 134-162 (Poodl's stylesheet and contrast suites). Keep P 164-168.
- Everything else verbatim.

### `reference/quality-gates.md`

P `docs/reference/quality-gates.md`, 167 lines. P 14-27 (the gate table) and P 139-160
("On `main`") verbatim, which keeps the stated network exception for gate 6. Edits:

- P 29-35 become:

  ```markdown
  Gates 10 and 11 cost the gate something real: the pinned `allium` binary lives in the
  gitignored `.tools/bin/`, which is a per-worktree install, so a worktree that has never
  run `just initialize` fails `just lint` and `just check` until `just install-allium`
  puts one there. The alternative was a gate that skipped itself whenever its tool was
  absent, which asserts nothing.
  [Decision 0007](../decisions/0007-project-managed-allium-cli.md) is the record.
  ```

- P 62 "Poodl's sidebar" becomes "this game's sidebar" (the one replacement
  CONVENTIONS.md §8 row 23 names).
- P 68: link text `Decision 0008`, target `../decisions/0008-design-system-as-a-package.md`.
- P 88 "excluding the lockfiles and the word lists" becomes "excluding the lockfiles"
  (the template's `pyproject.toml` drops the data exclusion).
- P 115 "the lockfile dry run" becomes "`lock-check`" (the template's `ci.yml` runs
  `just lock-check` there, CONVENTIONS.md §7).
- P 131: link text `decision 0006`, target `../decisions/0006-visual-review-in-chromatic.md`.
- Everything else verbatim, P 97-104 included (the `authorize` job survives in the
  template's `chromatic.yml`).

### `reference/documentation-contract.md`

P `docs/reference/documentation-contract.md`, 93 lines, verbatim, plus one new section
inserted before "## Outside the contract" (P 82). The seed set it describes is
CONVENTIONS.md §3's `_skip_if_exists` list:

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

- Write the section exactly:

  ```markdown
  ## Managed and seed pages

  This game was rendered from the Biscuit Games template, and every page under `docs/`
  is on one side of that line. A managed page is the template's: `copier update`
  re-renders it and merges the template's changes into it three-way, so an edit made
  here survives until the template changes the same lines, and is best made in the
  template when it would suit every game. A seed page is this game's: the two project
  pages that say what it is, every decision record and every specification module are
  rendered once by `copier copy` and never merged, recreated or deleted by an update. The
  manifest and [the documentation map](../README.md) are managed but expected to be
  edited here, which is why a page this game adds is registered after the last decision
  and linked under the map's final section: the template inserts above, the game appends
  below, and the two never touch the same lines.
  [Update from the template](../how-to/update-from-template.md) lists both sets.
  ```

### `reference/agent-contract.md`

P `docs/reference/agent-contract.md`, 78 lines. It names no game. Its two sections
"What a skill must be" and "What a bridge must be" (P 37-58) describe Poodl's older
validator, whose bridge rule was a forty-word budget; the render ships H's
`scripts/validate_agents.py`, which compares a bridge's body to one exact sentence,
rejects a duplicated frontmatter key and refuses a blank line inside the frontmatter
(CONVENTIONS.md §1, fact 2). Edits:

- Replace P 37-58 with H `docs/reference/agent-contract.md` lines 42-84 (the same two
  sections in H's form), with two edits inside the copied text: H 44 "This repository
  carries ten canonical skills" becomes "This game carries eight canonical skills";
  H's example frontmatter at 48-52 names the hub's `component-change` skill, so replace
  that fenced block with P's example at 41-46 (`svelte-change`, whose description is
  unchanged in the template's skill: P `.agents/skills/svelte-change/SKILL.md` line 3;
  CONVENTIONS.md §7 edits the body only).
- Everything else verbatim: P 1-36 and P 59-78 ("The inventory" and "Related pages").

After the edit, `grep -n forty` over the page prints nothing.

### `operations/maintenance.md`

P `docs/operations/maintenance.md`, 79 lines. Tier B. Edits:

- P 29-32 (the word-list paragraph; CONVENTIONS.md §8 row 26 says 29-30, the paragraph
  runs to 32) become:

  ```markdown
  **Per template release.** Take the update on its own, never alongside a behaviour
  change: [Update from the template](../how-to/update-from-template.md) says what it
  touches and what it leaves alone.
  ```

- P 43-44 become `BASE_PATH=/<repository name> just frontend-build` and
  `BASE_PATH=/<repository name> just preview`.
- P 57-60 become:

  ```markdown
  One caveat with real consequences: whatever this game keeps for a player lives in
  their browser. A rollback cannot restore data a bad release destroyed, because the
  release never had it. Treat any change to how state is stored as one-way, and read
  [Architecture](../explanation/architecture.md) before making one.
  ```

- P 62-73 (Secrets) verbatim; everything else verbatim.

### `operations/troubleshooting.md`

P `docs/operations/troubleshooting.md`, 141 lines. Edits:

- P 82 heading becomes "## Tests fail on `localStorage`"; P 84-85 become "It is not
  available. Node ships its own experimental `localStorage` that shadows the one jsdom
  would provide and stays undefined."
- P 92-93 become: "The base path. This game is a project site, served beneath the
  repository name rather than at the root of its host, so serve it from there before
  concluding anything:"
- P 96-97 become `BASE_PATH=/<repository name> just frontend-build` and
  `BASE_PATH=/<repository name> just preview`.
- Drop P 105-107 (the landing page and `just stage`) and P 119-122 (the domain change).
- P 56-72 (the 401 section) and everything else verbatim.

## Acceptance criteria

- [ ] All fourteen paths in Files touched are rewritten, or a tier B page is left as
      T00's stub and listed under hand-back notes as carried forward; nothing outside
      the table changed except this ticket's `status:`.
- [ ] No page is `.jinja`; no page contains `{{`, `{%` or `{#`, a name, a slug, an
      address, or any token the harness refuses (step 3).
- [ ] Every page's frontmatter equals its manifest entry and its H1 equals the title;
      every body has forty or more words.
- [ ] Every relative link resolves in a render with exact case; managed pages link only
      to managed pages and decisions 0001 to 0008; no link targets a Poodl-only page.
- [ ] `reference/quality-gates.md` lines P 14-27 and P 139-160 are byte-identical to
      Poodl's; `reference/agent-contract.md` equals Poodl's outside P 37-58 and states
      the exact-sentence bridge rule (`grep -n forty` over it prints nothing).
- [ ] `reference/documentation-contract.md` carries the "Managed and seed pages"
      section as written; `reference/configuration.md` lists exactly the six platform
      figures; `reference/commands.md` has no `stage` row.
- [ ] `just test` is green, `test_validators.py`,
      `test_managed_pages_link_only_to_stable_pages` and
      `test_no_poodl_outside_provenance` included; `just check` is green.
- [ ] In a render, `python3 scripts/validate_docs.py` exits 0 and `just check-docs` is
      green.

## Verification

From the template repository root:

```sh
just test
```

Expected: every test passes; none of `test_validators.py`, `test_render.py` is skipped.

```sh
just lint
```

Expected: markdownlint, typos and lychee are clean over `template/docs/` at source.

```sh
rm -rf ai_tmp/render && just render ai_tmp/render
python3 ai_tmp/render/scripts/validate_docs.py
```

Expected: `Validated 38 pages and <N> canonical topics.` and exit 0. This needs no
network and no `uv`.

```sh
grep -rniE 'poodl|pnut|site-root|stage_site|stage-preview|word[ -]list|(words|daily|sharing|statistics|game|settings)\.allium|foo/www|/Users/' \
  ai_tmp/render/docs/explanation ai_tmp/render/docs/reference ai_tmp/render/docs/operations
```

Expected: no output, exit 1.

```sh
grep -rnE '\]\([^)]*(purpose-and-scope|terminology|/specs/|decisions/(0009|001[0-9]))' \
  ai_tmp/render/docs/explanation ai_tmp/render/docs/reference ai_tmp/render/docs/operations
```

Expected: no output, exit 1 (no link to a seed page, a spec module or a decision beyond
0008).

```sh
cd ai_tmp/render && git init -q -b main && git add -A && uv lock && just check-docs
```

Expected: markdownlint, typos and lychee clean, then
`Validated 38 pages and <N> canonical topics.` Needs the network the first time (prek
clones its hook repositories); see the open point on running it without
`just initialize`.

```sh
just check
```

Expected: green in the template repository.

## Hand-back notes

Filled in by the agent that executes this ticket.

- What was verified and how: quote the output of each Verification command.
- What deviated from the ticket and why (a P line that had moved, a replacement
  sentence that failed a gate, a link the harness refused).
- Tier B pages cut, if any, with the reason; each stays as T00's stub.
- What was handed back to another ticket: any manifest, map, decision or how-to change
  this lane needed (T00 follow-up, T07, T09), stated as the exact edit.
- Which open points were settled, and how.

## Open points

CONVENTIONS.md §12 assigns no claim to T08. Points raised while writing this ticket:

- Whether `test_managed_pages_link_only_to_stable_pages` (T00, `tests/test_render.py`)
  treats decisions `0009` and `0010` as stable. This ticket links to neither; if the
  test admits them, the "Managed and seed pages" section may also link to
  `../decisions/0009-rendered-from-the-template.md`. Check: read the test's allowlist
  in the worktree.
- Whether `just check-docs` runs in a render after `git init` and `uv lock` alone,
  without `just initialize` (the `markdownlint-cli2` hook has to install its own node
  through prek). Check: the Verification command. Fallback: `python3
  scripts/validate_docs.py` in the render plus
  `npx --yes markdownlint-cli2@0.23.2 --config ai_tmp/render/.markdownlint-cli2.jsonc "ai_tmp/render/docs/**/*.md"`
  from the template repository root.
- Whether `typos` accepts every word in the new prose. Check: `just lint` at source and
  `just check-docs` in the render; the remedy is rewording, never an `extend-words`
  entry in a managed page's name.
- Whether the claim in `accessibility.md` that no platform module uses `import` holds
  for the package version `package.json` pins. Check:
  `grep -l '^import' /Users/scutting/projects/biscuit_games/docs/specs/*.allium` at
  commit `09b4894a` (expected: no output), or the same over
  `node_modules/@steven-cutting/biscuit-games/specs/` in an initialised render.
