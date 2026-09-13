---
id: T05
title: "Source skeleton: src/, the managed and seed tests, the story and the workshop"
status: done
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

### What was verified, and how

Both clones were at their pinned commits (`0a46a48` and `09b4894`). Output is quoted, and
each elision is marked with square brackets.

Step 2: the seven CONVENTIONS.md §7 files, compared by `diff` with §7's fences extracted
by a script, are identical to them (the `// tests/lockup.test.ts` and
`// tests/route.test.ts` first lines are inside §7's fences). Step 8: step 8's `sed`
pipeline plus the inserted case, rebuilt in the scratchpad, is identical to T00's
`tests/ports.test.ts`. Step 4: `diff` against Poodl shows exactly the two lines the step
names. Steps 5, 6, 9, 10 and 11 were applied to Poodl's files by a script that takes every
replacement from this ticket's fences and asserts Poodl's text at each line number the
steps name before replacing it.

The template repository, on the edited tree:

```text
$ just test
[...]
================= 27 passed, 2 skipped, 16 warnings in 11.35s ==================
$ just check; echo "just check exit $?"
uv lock --check
Resolved 33 packages in 4ms
uv run --frozen prek run --all-files
[18 hook lines, every one ending Passed]
uv run --frozen mypy
Success: no issues found in 7 source files
uv run --frozen pytest "$@"
[...]
================= 27 passed, 2 skipped, 16 warnings in 11.40s ==================
just check exit 0
```

The two skips are `tests/test_specs.py` (`set BISCUIT_TEMPLATE_NETWORK=1`); the sixteen
warnings are copier's `DirtyLocalWarning`.

```text
$ for f in src/app.d.ts src/lib/ports/storage.ts tests/setup.ts static/.nojekyll; do [...]
src/app.d.ts ok
src/lib/ports/storage.ts ok
tests/setup.ts ok
static/.nojekyll ok
$ grep -r -i -n poodl template/src template/stories template/.storybook [...]
template/tests/restated.ts:10: * Poodl's table is the worked example: its `game.allium` restates
$ grep -rn 'statistics.allium\|settings.allium\|word' template/src/lib/ports/ template/src/app.html template/.storybook/
[nothing; exit 1]
```

`wc -c template/static/.nojekyll` prints `0`. In `tests/ports.test.ts`, `grep -c
'^describe('` prints `3` (`storage port` :67, `random port` :141, `clock port` :184),
`grep -c '^  it('` prints `16`, and `grep -n 'poodl:\|clipboard\|timer\|biscuit-games'`
prints nothing. `stories/Lockup.stories.svelte` has three `<Story`, imports `GAME_NAME`
(:6), declares `FRAME_WIDTH` (:13), `LOCKUP` (:14) and `ACTIONS` (:39) with the one
`settings` entry; its only template-literal interpolation other than through `String()`
is `LOCKUP`'s `GAME_NAME`, a string.

The render, with a `read:packages` token in `~/.npmrc`, taken from the working tree
before the content commit (copier's `DirtyLocalWarning`), whose T05 files are the ones
committed:

```text
$ rm -rf ai_tmp/render && just render
[...]
Rendered into ai_tmp/render
$ cd ai_tmp/render
$ git init -q -b main && git add -A
$ git -c user.name=t05 -c user.email=t05@example.invalid commit -q --no-verify -m render
$ just initialize
sh scripts/initialize.sh
[uv sync, npm install: added 377 packages, playwright install chromium]
installed allium 3.6.1 at [ai_tmp/render]/.tools/bin/allium
74 files left unchanged

> tic_tac_toe_beans@0.1.0 lint:fix
> svelte-kit sync && eslint . --fix && prettier --write .

[every file "(unchanged)" except:]
tests/platformSpecs.test.ts 7ms
[...]
prek installed at `.git/hooks/pre-commit`
Ready. Next: just check.
Nothing has been staged, committed, tagged, or pushed.
$ git status --porcelain
 M tests/platformSpecs.test.ts
?? package-lock.json
?? uv.lock
$ grep -c allowNumber eslint.config.js || true
0
```

ESLint reported nothing and Prettier rewrote no T05 file, so nothing was carried back into
`template/`. The modified file is T06's (Handed back). With `0` above, step 14's copy was
skipped: the render's `eslint.config.js` is already the hub's, from T01.

The gates, against the published `@steven-cutting/biscuit-games@1.0.0`:

```text
$ just frontend-static
npm run lint
[...]
All matched files use Prettier code style!
npm run check
[...]
ERROR "src/lib/components/Lockup.svelte" 20:11 "Type 'string' is not assignable to type 'never'."
COMPLETED 806 FILES 1 ERRORS 0 WARNINGS 1 FILES_WITH_PROBLEMS
error: recipe `frontend-static` failed on line 93 with exit code 1
$ just frontend-unit
[...]
 ❯ |unit| tests/lockup.test.ts (1 test | 1 failed) 15ms
     × names this game after the platform, with the mark silent 14ms
 ❯ |unit| tests/route.test.ts (3 tests | 1 failed) 51ms
     × carries the heading the platform header draws for this game 47ms
[lockup.test.ts:16] Expected: "biscuit games / tic tac toe beans"  Received: "biscuit games"
[route.test.ts:12] Expected element to have text content: biscuit games / tic tac toe beans
                   Received: b biscuit games
 Test Files  2 failed | 2 passed (4)
      Tests  2 failed | 28 passed (30)
error: recipe `frontend-unit` failed on line 96 with exit code 1
$ just frontend-coverage
[the same two failures, and no coverage table: Vitest reports none when a test fails]
error: recipe `frontend-coverage` failed on line 99 with exit code 1
$ npx vitest run --config vite.config.ts --coverage --coverage.reportOnFailure=true
[the same two failures]
File            | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s
All files       |   98.14 |      100 |     100 |     100 |
 lib/components |      50 |      100 |     100 |     100 |
  Lockup.svelte |      50 |      100 |     100 |     100 |
Statements   : 98.14% ( 53/54 )
Branches     : 100% ( 15/15 )
Functions    : 100% ( 23/23 )
Lines        : 100% ( 52/52 )
$ just frontend-build && grep -c 'biscuit games / tic tac toe beans' build/index.html
[...]
  Wrote site to "build"
  ✔ done
0
$ just storybook-test
[...]
   × Lockup 16ms
   × InTheHeaderAtTheNarrowestSupportedWidth 11ms
 FAIL  |storybook (chromium)| stories/Lockup.stories.svelte > Lockup
AssertionError: Expected: "biscuit games / tic tac toe beans"  Received: "biscuit games"
 FAIL  |storybook (chromium)| stories/Lockup.stories.svelte > InTheHeaderAtTheNarrowestSupportedWidth
TestingLibraryElementError: Unable to find an accessible element with the role "heading" and name "biscuit games / tic tac toe beans"
 Test Files  1 failed (1)
      Tests  2 failed | 1 passed (3)
error: recipe `storybook-test` failed on line 114 with exit code 1
```

The built page's `h1` text is `b biscuit games`. The text reporter omits files at 100 on
every metric; `coverage/coverage-summary.json` lists exactly the six files:

```text
src/lib/brand.ts                 stmts 100 (3/3)    branch 100 (0/0)  funcs 100  lines 100 (3/3)
src/lib/config.ts                stmts 100 (6/6)    branch 100 (0/0)  funcs 100  lines 100 (6/6)
src/lib/components/Lockup.svelte stmts 50 (1/2)     branch 100 (0/0)  funcs 100  lines 100 (1/1)
src/lib/ports/clock.ts           stmts 100 (7/7)    branch 100 (2/2)  funcs 100  lines 100 (6/6)
src/lib/ports/random.ts          stmts 100 (19/19)  branch 100 (6/6)  funcs 100  lines 100 (19/19)
src/lib/ports/storage.ts         stmts 100 (17/17)  branch 100 (7/7)  funcs 100  lines 100 (17/17)
```

`tests/ports.test.ts` and `tests/platformSpecs.test.ts` are the two files that passed: 30
tests are 16 ports, 1 lockup, 3 route and 10 platform cases.

Whether the seven files pass once the package carries `product`, measured without
touching either repository: `git archive HEAD` of the hub into the scratchpad, `npm ci`
and `npm pack` there (`prepack` runs `svelte-package`), a copy of the render at
`ai_tmp/render-hubhead`, and `npm install --no-save` of the tarball in it (`grep -c
product` on the installed `dist/components/Wordmark.svelte` prints `3`). No T05 file
differs from the render above:

```text
frontend-static exit 0     [All matched files use Prettier code style!]
                           [COMPLETED 816 FILES 0 ERRORS 0 WARNINGS 0 FILES_WITH_PROBLEMS]
frontend-unit exit 0       [Test Files  4 passed (4); Tests  30 passed (30)]
frontend-coverage exit 0   [Statements 100% (54/54), Branches 100% (15/15),
                            Functions 100% (23/23), Lines 100% (52/52)]
frontend-build exit 0      [grep -c 'biscuit games / tic tac toe beans' build/index.html: 1]
storybook-test exit 0      [Test Files  1 passed (1); Tests  3 passed (3)]
```

### Which CONVENTIONS.md §7 files changed

None. The render's gates reject `Lockup.svelte` (`svelte-check`: `Lockup.svelte` 20:11
`Type 'string' is not assignable to type 'never'.`) and the test and story assertions
that read its words, for a reason outside this lane: the published package's `Wordmark`
"takes no props". `npm view @steven-cutting/biscuit-games versions` against GitHub
Packages prints `["1.0.0"]`, and `product` arrived in hub commit `41c430b`, after the
tag. §7, the Non-goals (no `<style>` and no `{#if}` in `Lockup.svelte`) and every
assertion were left as written; the hub-HEAD run shows the seven files pass unchanged
against a package that carries `product`.

### Deviations, and why

- **Branch.** The work is on `T05-source-skeleton`, the Supacode worktree's branch, as
  T00's to T02's were, not on `ticket/t05-source-skeleton`.
- **What T00 had left.** `app.html` and `clock.ts` were still Poodl's verbatim;
  `random.ts` had lines 4-8 rewrapped into four lines where step 6 gives five, which is
  what keeps its branch sites at :27, :40, :60 and :61; `main.ts` read "no longer keeps"
  and "this game's own sidebar" and still cited decision 0013 and `fixtures.ts`;
  `preview.ts` had only line 46; the story was Poodl's with its words scrubbed, four
  actions and the chip. All six were rebuilt from Poodl's files, the story included, not
  from T00's copies. `clock.ts`'s branch sites moved up one line, to :13 and :23.
- **"No `chip`" in the story.** Step 9's own comment reads "no chip, because this game
  has no state yet", and it is kept as written. There is no chip constant and no `chip`
  prop.
- **The five-run `document.title` loop.** Its `|| break` stopped at run 1 on the heading
  case, which fails for the `Wordmark` reason, so it could not settle the title claim.
  `npx vitest run --config vite.config.ts tests/route.test.ts -t 'titles the document'`
  was run five times instead.
- **Coverage figures.** `just frontend-coverage` prints no table when a test fails, so
  the published-package figures come from `--coverage.reportOnFailure=true`, and the six
  files from `coverage/coverage-summary.json`. V8 counts fifteen branch sites (clock 2,
  random 6, storage 7) where step 6 counts fourteen by hand. Step 14's second coverage
  run, excluding `platformSpecs.test.ts`, was not needed: that file passes.
- **The hub-HEAD run** is outside the steps. It changed nothing in either repository;
  `ai_tmp/render-hubhead` and the tarball in the scratchpad are throwaway.
- **`CHANGELOG.md` untouched.** AGENTS.md asks for a seed change to be noted there, but
  the tickets README and this ticket confine the edit to the table. T00's "Every seed
  file, in the form CONVENTIONS §7 gives it or as a stub" under Seed covers the rewritten
  story, and no game has been rendered yet.

### Handed back

- **CONVENTIONS.md §0 and the hub (maintainer).** The third report, after T00's and
  T01's. The remedy is a hub release whose `Wordmark` carries `product`, with
  `hub_package_version` in `copier.yml` and the pin in `package.json.jinja` moved to it,
  or a different `Lockup.svelte`; either is a CONVENTIONS change on `main`, and the
  hub-HEAD run shows the first needs no T05 change. Until then, in every render,
  `frontend-static`, `frontend-unit`, `frontend-coverage` and `storybook-test` exit 1 and
  the built `h1` reads `b biscuit games`. `just initialize` is unaffected.
- **T06.** `tests/platformSpecs.test.ts` is still not Prettier-formatted: `initialize`'s
  `prettier --write .` rewrites it, which is the modified file in the status above. Its
  ten cases pass.
- **T00 follow-up.** None: `tests/inventory.py:158` lists `tests/ports.test.ts` in
  `GAME_EDITED`, and `tests/platform.ts` needed nothing.
- **T01, T02.** None: the render's ESLint config is the hub's, and `initialize.sh` ran
  through to `Ready. Next: just check.`

### Open points settled

- **`document.title`: kept.** Five runs of the title case alone each printed
  `Tests  1 passed | 2 skipped (3)`; it also passes in both 30-test runs above.
- **The 44px action.** Against the published package the narrow story fails at its
  heading query, which the play reaches only after the frame-overflow check and the
  `getAllByRole('button')` loop have passed; in the hub-HEAD run the whole play passes,
  axe included. So the one `settings` action measures at least `MINIMUM_TOUCH_TARGET` in
  both directions at 320px under either package. The loop asserts rather than prints, so
  no box figure was recorded (`H/src/lib/components/IconButton.svelte:57` sets
  `inline-size: 44px`). Not a platform defect.
- **The coverage denominator.** Exactly six files in both runs; `All files` at or above
  90 on every metric in both; `config.ts` at 100 on lines, loaded by
  `platformSpecs.test.ts`.
- **T00's `eslint.config.js`.** Gone: `grep -c allowNumber` printed `0`.
- **`tests/ports.test.ts` as M†.** Listed in `GAME_EDITED`.

### The render's `just check`

Not run. It reaches `frontend-static` third and would stop there, on `Lockup.svelte`,
under the published package. `ai_tmp/render` and `ai_tmp/render-hubhead` are left in
place; `ai_tmp/` is gitignored.

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
