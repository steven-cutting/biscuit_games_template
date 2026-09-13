---
id: T05
title: "Source skeleton: src/, the managed and seed tests, the story and the workshop"
status: open
depends_on: [T00]
parallel_with: [T01, T02, T03, T04, T06, T07, T08, T09]
branch: ticket/t05-source-skeleton
estimated_size: L
---

# T05: Source skeleton: src/, the managed and seed tests, the story and the workshop

## Context

The render is a static SvelteKit site that consumes the platform package
`@steven-cutting/biscuit-games`. This ticket owns everything under `template/src/`,
`template/stories/`, `template/.storybook/`, `template/static/` and the tests under
`template/tests/` other than the two T06 owns and the one T00 wrote final. The design is
CONVENTIONS.md §4 (the tree rows for these paths), §5 (managed versus seed), §6 (Jinja
rules: no `.svelte`, `.test.ts` or `.stories.svelte` file is ever `.jinja`; the name reaches
Svelte only through `src/lib/brand.ts`), §7 (exact content and "Managed adaptations
against Poodl files"), §12 (the two claims this ticket checks) and §13 (the coverage
denominator, `initialize.sh` aborting on an unfixable ESLint error).

Position: T00 has merged to `main`. T00 wrote seven of this ticket's files in final form
from CONVENTIONS.md §7 (`brand.ts.jinja`, `config.ts`, `Lockup.svelte`, `+page.svelte`,
`restated.ts`, `lockup.test.ts`, `route.test.ts`) and left every other file in this lane as
a copy of Poodl's with forbidden tokens scrubbed by the smallest edit. This ticket verifies
the seven under the real toolchain in a render and replaces the copies with the designed
files. T10 waits for it. The other lanes run alongside; the render this ticket checks
carries their stubs, which is why the steps say what to do when a stub, not a T05 file,
is what fails.

The fourteen seed patterns (CONVENTIONS.md §3, identical in `_exclude` and
`_skip_if_exists`): `/README.md`, `/CHANGELOG.md`, `/SECURITY.md`,
`/docs/project/purpose-and-scope.md`, `/docs/project/terminology.md`, `/docs/decisions/`,
`/docs/specs/`, `/src/lib/brand.ts`, `/src/lib/components/`, `/src/routes/+page.svelte`,
`/stories/`, `/tests/restated.ts`, `/tests/lockup.test.ts`, `/tests/route.test.ts`. Seven
of this ticket's files are seeds; the rest are managed and say "this game", never a name.

Gates the render applies to these files (CONVENTIONS.md §13): ESLint `strictTypeChecked`
with the hub's config, which has no `allowNumber`, so a number inside a template literal
is an error (`H/eslint.config.js`; Poodl's `eslint.config.js:42-57` adds the two rules
the template drops); `svelte-check --fail-on-warnings`, so an unused selector fails;
Prettier with `P/.prettierrc.json` (`printWidth` 100, single quotes, no trailing commas);
coverage at 90 on branches, functions, lines and statements over `src/lib/**/*.{ts,svelte}`
(`P/vite.config.ts:19-29`), where every file matching the glob is reported whether or not
a test loads it; and `scripts/initialize.sh` running `npm run lint:fix` under `set -eu`
before `install-hooks` (`H/scripts/initialize.sh:2,42,52-57`), so an unfixable ESLint
error in a seed file leaves a half-initialised tree.

Read first, at the commits CONVENTIONS.md §0 pins: `P/tests/ports.test.ts`,
`P/src/lib/ports/storage.ts`, `P/src/lib/ports/clock.ts`, `P/src/lib/ports/random.ts`,
`P/stories/Lockup.stories.svelte`, `P/.storybook/main.ts`, `P/.storybook/preview.ts`,
`P/src/app.html`, `P/src/routes/+layout.svelte`, `P/src/routes/+layout.ts`;
`H/src/lib/components/Wordmark.svelte:23,31,36` (`product` prop, `class="words"`),
`H/src/lib/components/Monogram.svelte:50-58` (the mark's text is `b`, `aria-hidden` when
unlabelled), `H/src/lib/components/HeaderBar.svelte:45-51,171` (the `h1` renders the
`brand` snippet; `.brand :global(.words)` is the collapse), `H/stories/HeaderBar.stories.svelte:11,136-141`
(`FRAME_WIDTH` through `String()`; the narrow story measures every button),
`H/tests/brand.test.ts:76-77` (the "b" query).

## Goal

Every path in the table below carries its designed content: the seven CONVENTIONS.md §7
files unchanged unless the toolchain rejects one, the four verbatim Poodl files byte
for byte, the six prose-edited managed files with no Poodl-specific sentence left,
`tests/ports.test.ts` derived from Poodl's with the one added case, and
`stories/Lockup.stories.svelte` rewritten around the platform's `Wordmark`. The fast
suite is green, and in a render `just frontend-static`, `just frontend-coverage` (at or
above 90 on every metric), `just frontend-build` and `just storybook-test` pass. The two
CONVENTIONS.md §12 claims assigned here are answered in the hand-back notes.

## Non-goals

- `template/tests/platform.ts`: T00 wrote it final; not touched. A change it needs is
  handed back as a T00 follow-up.
- `tests/platformSpecs.test.ts` and the seed Allium module: T06. If they fail in the
  render, the failure is recorded and handed to T06, not fixed here.
- Root configs (`eslint.config.js`, `vite.config.ts`, `package.json.jinja`,
  `.prettierignore`, `Justfile` and the rest): T01. Scripts including `initialize.sh`:
  T02. Workflows: T03. Agent contract: T04. Handbook and decisions: T07 to T09.
  `tests/test_full.py` and the `full` CI job: T10. `docs/manifest.yml`,
  `docs/README.md.jinja`, `copier.yml`, `tests/inventory.py`: a T00 follow-up on `main`.
- No new component, story, test or constants file beyond the table: every file under
  `src/lib/**` counts against the coverage floor. No `<style>` in `Lockup.svelte`, no
  `{#if}` in it. No change to the coverage thresholds.
- Nothing is pushed, published or deployed.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `template/src/app.html` | M | `P/src/app.html` | Comment lines 2-7 replaced (step 5). |
| `template/src/app.d.ts` | M | `P/src/app.d.ts` | Verbatim; confirm with `cmp`. |
| `template/src/routes/+layout.svelte` | M | `P/src/routes/+layout.svelte` | Line 7: "Poodl's own styles" becomes "the game's own styles". |
| `template/src/routes/+layout.ts` | M | `P/src/routes/+layout.ts` | Line 1: "Poodl is served" becomes "The game is served". |
| `template/src/routes/+page.svelte` | S | CONVENTIONS.md §7 | T00 wrote it; verify in the render, fix only what the gate rejects. |
| `template/src/lib/brand.ts.jinja` | S | CONVENTIONS.md §7 | As above. |
| `template/src/lib/config.ts` | M† | CONVENTIONS.md §7 | As above. |
| `template/src/lib/ports/storage.ts` | M | `P/src/lib/ports/storage.ts` | Verbatim; confirm with `cmp`. |
| `template/src/lib/ports/clock.ts` | M | `P/src/lib/ports/clock.ts` | Comment lines 4-7 replaced (step 6). |
| `template/src/lib/ports/random.ts` | M | `P/src/lib/ports/random.ts` | Comment line 2 and lines 4-8 replaced (step 6). |
| `template/src/lib/components/Lockup.svelte` | S | CONVENTIONS.md §7 | T00 wrote it; verify, fix only what the gate rejects. |
| `template/stories/Lockup.stories.svelte` | S | `P/stories/Lockup.stories.svelte` | Rewritten around `Wordmark` (step 9). |
| `template/tests/setup.ts` | M | `P/tests/setup.ts` | Verbatim, one line; confirm with `cmp`. |
| `template/tests/ports.test.ts` | M† | `P/tests/ports.test.ts:1-204` | Three ports only, keys renamed, one case added (step 8). |
| `template/tests/restated.ts` | S | CONVENTIONS.md §7 | T00 wrote it; verify, fix only what the gate rejects. |
| `template/tests/lockup.test.ts` | S | CONVENTIONS.md §7 | As above. |
| `template/tests/route.test.ts` | S | CONVENTIONS.md §7 | As above; the `document.title` case is an open point. |
| `template/.storybook/main.ts` | M | `P/.storybook/main.ts` | Prose only (step 10); `refs` block kept. |
| `template/.storybook/preview.ts` | M | `P/.storybook/preview.ts` | Prose and one identifier (step 11). |
| `template/static/.nojekyll` | M | `P/static/.nojekyll` | Empty, 0 bytes. |

CONVENTIONS.md §4 and §5 both mark the ports test M†: a game appends its own port cases
at the end of the file. The Class column is informational here; the classification lives
in the harness, which no lane edits.

## Steps

1. Create the worktree on `ticket/t05-source-skeleton` from `main` (README.md "How to
   pick up a ticket"), run `just sync`, then read CONVENTIONS.md §4 to §7, §12, §13 and
   the P and H files named in Context.

2. Confirm the seven CONVENTIONS.md §7 files T00 wrote are exactly §7's text:
   `template/src/lib/brand.ts.jinja`, `template/src/lib/config.ts`,
   `template/src/lib/components/Lockup.svelte`, `template/src/routes/+page.svelte`,
   `template/tests/restated.ts`, `template/tests/lockup.test.ts`,
   `template/tests/route.test.ts`. Where one differs, rewrite it from §7. They change
   again only in step 14, and only where the render's gate rejects them.

3. Confirm the verbatim files against Poodl and copy them if they differ:

   ```sh
   for f in src/app.d.ts src/lib/ports/storage.ts tests/setup.ts static/.nojekyll; do
     cmp "/Users/scutting/projects/poodl/$f" "template/$f" && printf '%s ok\n' "$f"
   done
   ```

   `static/.nojekyll` is 0 bytes (`wc -c` prints `0`); Git tracks an empty file.

4. `template/src/routes/+layout.svelte`: Poodl's file with line 7 changed from
   `the global element rules together — and Poodl's own styles name tokens from` to
   `the global element rules together — and the game's own styles name tokens from`.
   `template/src/routes/+layout.ts`: Poodl's file with line 1 changed to
   `// The game is served as static files, so every route is rendered at build time.`
   Nothing else in either file changes (the `{@render children?.()}` line is not Jinja
   and the file is not `.jinja`).

5. `template/src/app.html`: Poodl's file with lines 2-7 (the whole comment) replaced by

   ```html
   <!--
     data-theme="dark" is `default AppearanceSettings appearance_settings` from
     the platform's appearance.allium, which @steven-cutting/biscuit-games ships,
     stated in the markup so the prerendered page paints the default before
     anything hydrates. A route that lets the player choose writes their choice
     over it: `light` replaces it, `system` removes it.
   -->
   ```

   The markup from line 8 on is unchanged (`data-theme="dark"` only; the hub's extra
   `data-animations` attribute is not added). `default AppearanceSettings
   appearance_settings` is `H/docs/specs/appearance.allium:109`.

6. Ports: `storage.ts` is verbatim (its header names no Poodl module). In
   `template/src/lib/ports/clock.ts` replace lines 4-7 of Poodl's file with

   ```ts
    * A specification reads `now` when something starts and when it ends. A test
    * that has to wait real seconds to watch a countdown expire is not a test
    * worth having, so time arrives through a port.
   ```

   In `template/src/lib/ports/random.ts` replace line 2 with

   ```ts
    * Drawing one candidate from many.
   ```

   and lines 4-8 with

   ```ts
    * A specification that calls `uniform_choice` says the same thing about it
    * every time: what matters is that every candidate is equally likely, not
    * that the same input yields the same value. That makes it the one
    * deliberately non-deterministic step, and therefore the one that has to sit
    * behind a port.
   ```

   Code in both files is untouched; the branch sites the coverage floor counts are
   `storage.ts` :25, :41, :45 (two), :52, :59, :68, :71; `random.ts` :27, :40, :60, :61;
   `clock.ts` :14, :24 (line numbers verified in P; the edits above do not move them
   in `clock.ts` by more than one line and do not move them in `random.ts`).

7. Keep step 6's text exactly; this step is the reason for it. Every branch above is
   taken by Poodl's storage, random and clock cases plus one addition: `createWebStorage()`
   with no argument (P `ports.test.ts:86`) takes both defaults and every `?.`
   short-circuit; `deviceStore(() => { throw ... })` (:101-104) takes the catch;
   `unusableStorage()` (:114) takes the three method catches; `memoryStorage()` (:73)
   takes `??` both ways; `createFakeStorage({...})` (:126) takes one side of `:68` and
   the added case the other; `createCryptoRandom()` (:155) and with a source (:141,
   :149) take `:40` both ways and the rejection loop; `createFakeRandom()` (:175), `([])`
   (:171) and `([2, 0])` (:161) take `:60` and `:61` both ways; the empty-items throws
   (:175-176) take `:27`; the four clock cases (:184, :188, :192, :202) take `:14` and
   `:24` both ways. Dropping any of them breaches the floor (CONVENTIONS.md §13).

8. `template/tests/ports.test.ts`: Poodl's lines 1-204 with the imports at lines 4
   (clipboard), 6 and 7 (preferences and `MediaQueryListLike`) and 9 (timer) removed,
   every `'poodl:` key spelt `'game:`, and lines 205-493 (the clipboard, preferences and
   timer describes with their comments) dropped:

   ```sh
   sed -n '1,204p' /Users/scutting/projects/poodl/tests/ports.test.ts \
     | sed -e '4d;6d;7d;9d' -e "s/'poodl:/'game:/g" > template/tests/ports.test.ts
   ```

   Then insert, after the `});` that closes `offers the same contract in memory` (P line
   136, the last case in `describe('storage port')`) and before the describe's own
   `});`, a blank line and

   ```ts
     it('starts empty when given nothing', () => {
       const storage = createFakeStorage();

       expect(storage.read('game:settings')).toBeNull();
     });
   ```

   Nothing else is edited: no other case is renamed, reordered or removed.

9. `template/stories/Lockup.stories.svelte`: written from `P/stories/Lockup.stories.svelte`.
   Replace P lines 1-49 (the whole `<script module>`) with

   ```svelte
   <script module lang="ts">
     import { HeaderBar } from '@steven-cutting/biscuit-games';
     import { defineMeta } from '@storybook/addon-svelte-csf';
     import { expect, fn, within } from 'storybook/test';

     import { GAME_NAME } from '../src/lib/brand';
     import Lockup from '../src/lib/components/Lockup.svelte';
     import { MINIMUM_TOUCH_TARGET, NARROWEST_SUPPORTED_WIDTH } from '../src/lib/config';

     // The gutters `.shell` gives the page at every width, so a frame here leaves
     // the header exactly the room the route does.
     const SHELL_GUTTER = '1rem';
     const FRAME_WIDTH = `${String(NARROWEST_SUPPORTED_WIDTH)}px`;
     const LOCKUP = `biscuit games / ${GAME_NAME}`;

     const OVERVIEW = [
       'This game’s lockup: the platform’s words and then its own, drawn by the platform’s',
       '`Wordmark` through its `product` prop. The route hands it to `HeaderBar` as the `brand`',
       'snippet, so the page’s only `h1` names the page rather than the platform alone.',
       '',
       'No governing surface — this is brand, decided upstream. The mark is `aria-hidden`: the',
       'words are the whole accessible text, which the first play holds.',
       '',
       'The second story is the evidence that the lockup meets the platform’s collapse contract,',
       'which is a class name and nothing else: `Wordmark` puts the words in an element of class',
       '`words`, so below about 26rem the header hides them and keeps the mark rather than',
       'overflowing a phone.'
     ].join('\n');

     const { Story } = defineMeta({
       title: 'Brand/Lockup',
       component: Lockup,
       tags: ['autodocs'],
       parameters: { docs: { description: { component: OVERVIEW } } }
     });

     // One action, so the narrow story has a control to measure and
     // MINIMUM_TOUCH_TARGET has a use; no chip, because this game has no state yet.
     const ACTIONS = [
       { icon: 'settings', label: 'Settings', popup: 'dialog', onclick: fn() }
     ] as const;
   </script>
   ```

   Replace P lines 51-59 (the first story) with

   ```svelte
   <Story
     name="Lockup"
     play={async ({ canvasElement }) => {
       const canvas = within(canvasElement);

       // Two assertions because neither holds the claim alone: a text query matches
       // an element's own text nodes, so the words are found whether or not the
       // mark beside them is hidden. The mark is held silent on its own.
       await expect(canvas.getByText('b')).toHaveAttribute('aria-hidden', 'true');
       await expect(canvas.getByText(/biscuit/).textContent).toBe(LOCKUP);
     }}
   />
   ```

   In the narrow story (P lines 61-140) make exactly four edits: line 81
   `styles: { width: FRAME_WIDTH, height: '568px' }`; line 108 `name: LOCKUP` (keep the
   object's three-line shape, which Prettier preserves); lines 129-132 collapse to the
   one line `<div data-frame style="inline-size: {FRAME_WIDTH}; padding-inline: {SHELL_GUTTER}">`
   (indented as P's `<div` was; the hub's `HeaderBar.stories.svelte:167` is the model);
   line 133 `<HeaderBar actions={ACTIONS}>`. The comments at 61-66, 71-76, 88, 104-105
   and 111-120 and the dark-theme story (P lines 142-149) are byte-identical to Poodl's.
   Numbers go through `String()` because the hub's ESLint config has no `allowNumber`;
   `MINIMUM_TOUCH_TARGET`, `NARROWEST_SUPPORTED_WIDTH`, `HeaderBar`, `fn` and
   `GAME_NAME` are all used, so no import is unused. Stories are never measured for
   coverage (`P/vitest.storybook.config.ts:7-20`).

10. `template/.storybook/main.ts`: Poodl's file with these line edits and nothing else
    (the `refs` block at 60-66 stays, address included):

    - Line 39: `here: its components, and the token sheet Poodl no longer keeps. Its`
      becomes `here: its components, and the token sheet this game does not keep. Its`.
    - Lines 44-45: `` `expanded: false` because Poodl's own components belong at the top of``
      / `Poodl's own sidebar.` become
      `` `expanded: false` because this game's own components belong at the top of``
      / `its own sidebar.`
    - Line 57: `decision 0013` becomes `decision 0008` (the template renumbers Poodl's
      design-system decision; CONVENTIONS.md §8 row 36).
    - Line 91: `` which covers `fixtures.ts` as well as the `*.stories.svelte`. `` becomes
      `` which covers a helper module beside the `*.stories.svelte` as well. `` (the
      template ships no `stories/fixtures.ts`).

11. `template/.storybook/preview.ts`: Poodl's file with these edits and nothing else:

    - Lines 13-17 become

      ```ts
       * `appearance.allium`'s Appearance surface, which `@steven-cutting/biscuit-games`
       * ships, derives `dark_active` and `animations_active` from the stored settings
       * and from the device. The toolbar below makes those inputs adjustable so a
       * component can be built and inspected in every combination of theme and high
       * contrast before the route that sets them exists.
      ```

    - Lines 25-28 become

      ```ts
       * application expressing a preference, so it needs no port. The application
       * does need one, and the platform ships it: a route that lets the player choose
       * reads the device through the platform's preferences port and writes these
       * same three attributes from what it says — see `docs/explanation/layering.md`.
      ```

    - Line 46 becomes `const REDUCED_MOTION_STYLE_ID = 'game-simulated-reduced-motion';`
      (a DOM id inside the preview iframe; any unique string works).
    - Lines 73-76 become

      ```ts
       * freezes declarative motion so a reviewer sees the still frame. It stands in
       * for the device half of `Appearance.animations_active`, and because it is a
       * simulation it is not evidence that the real preference is honoured; the
       * platform's preferences port and the tests behind it are.
      ```

    - Lines 128-131 become

      ```ts
         * `Appearance.animations_active`, on the terms a route that lets the player
         * choose writes it: the setting and the device's reduced-motion preference
         * taken together, and the device wins. Without this the attribute is never
         * present in the workshop and every story renders the animation-off path,
         * whatever the toolbar says.
      ```

    - Lines 242-243 become the single line

      ```ts
            // own default is 'todo', which reports and passes. No rule is disabled.
      ```

      (Poodl's decision 0006 is the template's 0005, which drops the palette narratives;
      CONVENTIONS.md §8 row 33).

12. Fast suite in the template repository: `just test`, then `just check`. Both green
    before any render. `test_no_poodl_outside_provenance` is the test that catches a
    missed sentence in steps 4 to 11; `test_verbatim_files_are_byte_identical` proves the
    render carries these files byte for byte.

13. Render and initialise. **Authorisation required:** a GitHub token carrying
    `read:packages` must be in `~/.npmrc` as `//npm.pkg.github.com/:_authToken=<your token>`;
    the agent never creates or writes one. If none is present, stop and ask the
    maintainer; if none can be had, record it in the hand-back notes and rely on the
    `full` CI job T10 adds. Then run the render block in Verification (render, `git init`,
    commit, `just initialize`, `git status --porcelain`).

    The commit before `just initialize` is what makes formatter drift visible: after
    `initialize` the status must be exactly `?? package-lock.json` and `?? uv.lock`. A
    status line with `M` in its second column against a T05 file means the template
    source is not Prettier- or ESLint-clean; carry that reformatting back into
    `template/` and re-render. A modified `.copier-answers.yml` is T01's
    (`.prettierignore` gains that entry there), not a T05 defect. On Linux,
    **Authorisation required:** `just storybook-browsers-deps` runs `playwright
    install-deps`, which asks for sudo; stop and ask before running it (macOS needs
    nothing). `initialize.sh` aborting at `npm run lint:fix` is an ESLint error in a
    rendered file: read it, fix the T05 file in `template/`, hand any other back.

14. Make the ESLint check meaningful. Until T01 merges the render carries Poodl's
    `eslint.config.js`, whose `allowNumber` hides the error the template's config
    reports. In the render only (never in `template/`), run the `grep -c allowNumber`
    line in Verification. If it prints `1`:
    `cp /Users/scutting/projects/biscuit_games/eslint.config.js eslint.config.js` and
    delete `'dist/',` and the space after it from the `ignores` line (line 11), for
    example with `perl -pi -e "s/'dist\/', //" eslint.config.js`. Then, in the render,
    `just frontend-static`, `just frontend-unit`, `just frontend-coverage`,
    `just frontend-build`, `just storybook-test` (expected outcomes in Verification). A
    failure in a file from the table is fixed in `template/` and the render is redone
    from step 13; a failure in `tests/platformSpecs.test.ts` or the Allium module is T06's
    and in a config or script is T01's or T02's: record it and hand it back. If
    `platformSpecs.test.ts` fails for a T06 reason, measure coverage a second time with
    `npx vitest run --config vite.config.ts --coverage --exclude tests/platformSpecs.test.ts`
    and report both figures; `config.ts` is loaded only by that test, so it reports at
    zero in the second run.

15. Answer the two CONVENTIONS.md §12 claims. (a) `document.title`: if `just frontend-unit`
    fails or flakes on `titles the document after the game` (run
    `npx vitest run --config vite.config.ts tests/route.test.ts` five times), delete that
    one `it` block from `template/tests/route.test.ts`; never weaken the heading case.
    (b) The 44px action: `just storybook-test` runs the narrow story's loop over
    `getAllByRole('button')`. `H/src/lib/components/IconButton.svelte:57` sets
    `inline-size: 44px` and the hub's own narrow story measures two actions and a chip
    (`H/stories/HeaderBar.stories.svelte:136-141`) and passes, so it is expected to pass.
    If it does not, that is a platform defect: record the measured box, do not weaken
    the loop, and stop and ask the maintainer.

16. Optionally run `just check` in the render and quote the outcome. Its recipe order is
    `lock-check`, `lint`, `frontend-static`, `frontend-coverage`, `frontend-build`,
    `storybook-build`, `storybook-test`, `check-docs`, `check-agents`, `check-specs`,
    `analyse-specs` (`P/scripts/run_project_check.py:18-30`); the first `lint` needs the
    network for the hook repositories, and a stop at `lint`, `check-docs`, `check-agents`
    or `check-specs` is another lane's stub, not this ticket's. Delete `ai_tmp/render`
    afterwards or leave it; `ai_tmp/` is gitignored.

17. Commit on the ticket branch with the hand-back notes filled in and `status: done`.
    **Authorisation required:** pushing the branch and opening the pull request. Stop and
    ask.

## Acceptance criteria

- [ ] Every path in Files touched exists in `template/` with the content the steps
      specify; no other file changed except this ticket's `status:` line.
- [ ] `cmp` reports no difference for `src/app.d.ts`, `src/lib/ports/storage.ts`,
      `tests/setup.ts` and `static/.nojekyll` against Poodl.
- [ ] `grep -in poodl` over the twenty files finds nothing; `grep -n 'statistics.allium\|settings.allium\|word'`
      over `src/lib/ports/`, `src/app.html` and `.storybook/` finds nothing.
- [ ] `template/tests/ports.test.ts` has exactly three describes (`storage port`,
      `random port`, `clock port`), sixteen cases, no `poodl:` key and no import of
      `clipboard`, `timer` or the package's preferences port.
- [ ] `template/stories/Lockup.stories.svelte` has three stories, imports `GAME_NAME`,
      declares `FRAME_WIDTH`, `LOCKUP` and a one-entry `ACTIONS`, and contains no `chip`
      and no bare number inside a template literal.
- [ ] `just test` and `just check` green in the template repository.
- [ ] In a render after `just initialize`: `git status --porcelain` shows only the two
      lockfiles (and at most `.copier-answers.yml` until T01 merges).
- [ ] In the render, with the hub's ESLint config in place: `just frontend-static` exit 0
      with `svelte-check found 0 errors and 0 warnings`; `just frontend-unit` passes
      every test in `lockup.test.ts`, `ports.test.ts` and `route.test.ts`;
      `just frontend-coverage` reports `All files` at or above 90 on Stmts, Branch, Funcs
      and Lines with exactly `brand.ts`, `config.ts`, `Lockup.svelte`, `clock.ts`,
      `random.ts` and `storage.ts` listed; `just frontend-build` exit 0 and
      `build/index.html` contains `biscuit games / tic tac toe beans`; `just storybook-test`
      passes all three stories with no axe violation.
- [ ] Both CONVENTIONS.md §12 claims answered in the hand-back notes, with the
      `document.title` case either kept and green or deleted.
- [ ] Hand-back notes quote the verification output and name every failure handed to
      another lane.

## Verification

From the template repository root:

```sh
just test
just check
```

Expected: every test passes; `lock-check`, `lint`, `typecheck` and `test` all exit 0.

```sh
for f in src/app.d.ts src/lib/ports/storage.ts tests/setup.ts static/.nojekyll; do
  cmp "/Users/scutting/projects/poodl/$f" "template/$f" && printf '%s ok\n' "$f"
done
grep -r -i -n poodl template/src template/stories template/.storybook template/static \
  template/tests/setup.ts template/tests/ports.test.ts template/tests/restated.ts \
  template/tests/lockup.test.ts template/tests/route.test.ts
```

Expected: four `ok` lines; the grep prints only lines from `template/tests/restated.ts`
(its comment names Poodl as the worked example, which the residue test allows).

```sh
rm -rf ai_tmp/render && just render
cd ai_tmp/render
git init -q -b main && git add -A
git -c user.name=t05 -c user.email=t05@example.invalid commit -q --no-verify -m render
just initialize
git status --porcelain
```

Expected: `Rendered into ai_tmp/render`; `initialize` ends `Ready. Next: just check.`;
the status is exactly `?? package-lock.json` and `?? uv.lock` (plus a modified
`.copier-answers.yml` until T01 merges). Needs the network and the `~/.npmrc` token.

```sh
grep -c allowNumber eslint.config.js || true
```

Expected `0`. If `1`, copy `/Users/scutting/projects/biscuit_games/eslint.config.js`
over it and remove `'dist/',` and its trailing space from line 11 (step 14), then:

```sh
just frontend-static
just frontend-unit
just frontend-coverage
just frontend-build && grep -c 'biscuit games / tic tac toe beans' build/index.html
just storybook-test
```

Expected: `frontend-static` prints nothing from ESLint, `All matched files use Prettier
code style!` and `svelte-check found 0 errors and 0 warnings`; `frontend-unit` reports
four test files passed and 30 tests (16 ports, 1 lockup, 3 route, 10 platform figures)
when `platformSpecs.test.ts` is T00's final form; `frontend-coverage` passes the same
tests and prints a table whose `All files` row is at or above 90 in every column with no
`ERROR: Coverage for` line; the build exits 0 and the grep prints at least `1`;
`storybook-test` reports the three stories in `Lockup.stories.svelte` passed.

```sh
for i in 1 2 3 4 5; do npx vitest run --config vite.config.ts tests/route.test.ts || break; done
```

Expected: five green runs, which settles the `document.title` claim; a failure means the
case is deleted (step 15).

## Hand-back notes

Filled in by the agent that executes this ticket.

- What was verified and how: quote the output of every Verification block, including
  the coverage table and the `git status --porcelain` line after `just initialize`.
- Which of the seven CONVENTIONS.md §7 files changed and why (a gate's exact message),
  or that none did.
- What deviated from the ticket and why (a line number in P that had moved, a Prettier
  rewrite carried back, an edit the steps did not foresee).
- What was handed to another ticket: T01 (a config the render needed), T02
  (`initialize.sh`), T06 (`platformSpecs.test.ts` or the Allium module), a T00 follow-up
  (`tests/platform.ts`, `tests/inventory.py`, CONVENTIONS), the hub (a platform defect).
- Which open points were settled and how: the `document.title` case kept or deleted; the
  measured width and height of the `settings` action at 320px.
- Whether the render's `just check` was run and where it stopped.

## Open points

- CONVENTIONS.md §12: jsdom reflects a Svelte 5 `<svelte:head><title>` into
  `document.title` under `@testing-library/svelte`. Check: `just frontend-unit` in the
  render and the five-run loop in Verification; on a failure or a flake, delete the
  `titles the document after the game` case from `template/tests/route.test.ts` and keep
  the heading case unchanged.
- CONVENTIONS.md §12: Storybook's `getAllByRole('button')` in the narrow lockup story
  measures the one `settings` action at or above 44px inside a 320px frame with the hub's
  `HeaderBar` 1.0.0. Check: `just storybook-test` in the render. Grounding:
  `H/src/lib/components/IconButton.svelte:57`, `H/stories/HeaderBar.stories.svelte:136-141`.
  A failure is a platform defect: stop and ask.
- CONVENTIONS.md §13 risk: the coverage denominator is about fourteen branch sites, so a
  `{#if}` in `Lockup.svelte`, a constants file no test loads, or a dropped storage case
  breaches 90. Check: the `frontend-coverage` table lists exactly six files and every
  column of `All files` is at or above 90; `config.ts` shows 100 on lines, which proves
  `platformSpecs.test.ts` loaded it.
- Whether T00's Poodl copy of `eslint.config.js` is still in the render when this ticket
  runs (T01 merges in parallel). Check: `grep -c allowNumber eslint.config.js` in the
  render; step 14 says what to do when it prints `1`.
- `tests/ports.test.ts` is M† in CONVENTIONS.md §4 and §5. Check that `tests/inventory.py`
  lists it in `GAME_EDITED`; if it does not, hand back a T00 follow-up rather than editing
  the file.
