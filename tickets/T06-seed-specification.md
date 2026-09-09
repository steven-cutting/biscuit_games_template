---
id: T06
title: "Seed specification: the root Allium module and the platform-figures test"
status: open
depends_on: [T00]
parallel_with: [T01, T02, T03, T04, T05, T07, T08, T09]
branch: ticket/t06-seed-specification
estimated_size: S
---

# T06: Seed specification: the root Allium module and the platform-figures test

## Context

A rendered game passes `just check` on its first run, and two of that gate's recipes
read `docs/specs/`: `just check-specs` and `just analyse-specs`, both through
`scripts/run_allium.py`, which refuses an empty directory (`NO_INPUTS = 2`,
`P/scripts/run_allium.py` line 42) and passes only when every module reports an empty
`diagnostics` array and an empty `findings` array (lines 15-18). So every game ships
one module from the start: the seed `docs/specs/<slug>.allium`, rendered from
`template/docs/specs/{{ game_slug }}.allium.jinja`. It restates the six platform figures
under the names the platform uses, and `tests/platformSpecs.test.ts` holds those figures
equal to `src/lib/config.ts` and to the three modules `@steven-cutting/biscuit-games`
ships. The module is seed (CONVENTIONS.md §5: an update never merges, recreates or
deletes it); the test is managed.

T00 merged before this ticket and already shipped both files in the final form
CONVENTIONS.md §7 gives (CONVENTIONS.md §11, "T00 renders a shape-complete skeleton").
What remains, and what this lane is for, is proof: the module's parsing is the first
unverified claim in CONVENTIONS.md §12, assigned to T06, because it was written from the
platform's grammar without being run through the checker. The three doubts named there
are (a) bare `Play` as a surface identifier where the platform writes `PlaySurface`,
(b) a surface with no `contracts:` block, and (c) five figures referenced only inside
`--` comment bodies not tripping `allium.field.unused`.

The pinned binary, allium 3.6.1 (`H/scripts/install_allium.py` line 36, checksums at
53-58), accepts the module exactly as §7 embeds it: `allium check` and `allium analyse`
both return `"diagnostics": []` and `"findings": []`. The same holds with the surface
renamed `PlaySurface`, with `let` lines citing every figure, and with a same-module
`contracts:` block; a config figure nothing mentions at all raises no diagnostic
either. What this ticket adds is the proof in a render, through the scripts the
template ships, with the output quoted in the hand-back notes, and the corrective edits
below if that run disagrees. T10 (harness completion, `just test-full`) and T11 (the
first consumer render) wait for it.

Read first, in this order:

1. CONVENTIONS.md §4 (file classes), §5 (seed), §6 rules 5 and 6 (Allium file names
   and delimiters), §7 (both files), §9 (`just render`, `tests/test_specs.py`), §11,
   §12 (the claim) and §13.
2. `H/docs/specs/operation.allium` lines 68-85 (`given`), 91-108 (`config`, with
   `minimum_touch_target` at 96 and `narrowest_supported_width` at 101) and 211-252
   (`surface Operation`: a `let`, `exposes:`, `contracts:` and five guarantees). The
   seed module is modelled on these three blocks.
3. `H/docs/specs/appearance.allium` lines 97-98 (the two contrast figures) and 162-166
   (a guarantee body that cites both figures only in `--` comment lines; the hub's gate
   passes on it). `H/docs/specs/play-surfaces.allium` lines 126 and 141 (the two
   separation figures) and 198-207 (`surface PlaySurface` with `contracts:` naming the
   contract defined at line 150).
4. `P/tests/platformSpecs.test.ts`: lines 37-100 (`flatten`, `clauses`, `figures`,
   carried verbatim), 102-179 (what is adapted) and 181-194 (the version case with its
   comment, carried verbatim). `P/tests/platform.ts` for `platformPath` and
   `platformFile`.
5. `P/scripts/run_allium.py` (what clean means), `H/scripts/install_allium.py`,
   `P/Justfile` lines 43-44 and 148-156 (the three recipes, all `uv run --frozen`), and
   `P/.gitignore` lines 28-31 (`.tools/`, where the binary lands, is ignored).

## Goal

Both files in `template/` equal the texts embedded under Steps, and a render proves the
module clean: in `ai_tmp/render`, `just install-allium`, `just check-specs` and
`just analyse-specs` each exit 0, the two reports carry empty `diagnostics` and
`findings` arrays, and the six figures the module states (4.5, 3.0, 44, 320, 3.0, 2.0)
are the ones `src/lib/config.ts` exports and the shipped modules state. The outcome of
the CONVENTIONS.md §12 claim is recorded in the hand-back notes, and if the module had
to change, the exact diagnostic and the edit are recorded with it.

## Non-goals

- `tests/test_specs.py`, `template/scripts/install_allium.py` and
  `template/scripts/run_allium.py`: T02 writes them. This ticket runs them if T02 has
  merged and otherwise runs copies inside the scratch render, never edits them.
- `tests/platform.ts` (the `Restatement` interface): T00's, final.
- `tests/restated.ts` and `src/lib/config.ts`: T05's. If the six constants or the
  empty `RESTATED` table are not as CONVENTIONS.md §7 gives them, hand it back.
- `docs/how-to/work-with-the-specs.md` and `docs/explanation/specifications.md`: T07
  and T08 describe the module; nothing here edits a handbook page.
- The four files no lane touches (CONVENTIONS.md §11), and T00's `tests/inventory.py`.
- A second module, game rules, entities or outcomes: the module deliberately names
  none (its Excludes says so), and a game adds its own modules after rendering.
- Moving `VERSION` in `install_allium.py`, adding a waiver, or editing P or H.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `template/docs/specs/{{ game_slug }}.allium.jinja` | S | CONVENTIONS.md §7, modelled on `H/docs/specs/operation.allium` lines 68-85, 91-108, 211-252 | Hold equal to the text embedded in step 2; proven with the pinned binary in a render; changed only as step 5 directs, on a quoted diagnostic |
| `template/tests/platformSpecs.test.ts` | M | `P/tests/platformSpecs.test.ts` (lines 37-100 and 181-194 verbatim) adapted as CONVENTIONS.md §7 says | Hold equal to the text embedded in step 3 |

## Steps

1. Create the worktree as [README.md](README.md) says, then `just sync` at the
   repository root. Read the sources listed under Context.

2. Hold the module to this text. Write it to `ai_tmp/t06/module.allium.jinja` and diff
   it against `template/docs/specs/{{ game_slug }}.allium.jinja`; replace the file only
   if they differ. Four-space indentation (the repository's `.editorconfig` sets it for
   `*.allium.jinja`), LF, one final newline, no trailing whitespace, no tab. The only
   Jinja in it is `{{ game_name }}` on the third line, inside a comment; after rendering
   the file must contain none of `{{`, `{%`, `{#` (CONVENTIONS.md §6 rule 1) and never
   the word "Poodl". Every `name: Type = value` line must keep the exact shape
   `figures()` reads in step 3.

   ```text
   -- allium: 3
   --
   -- {{ game_name }} — the game
   --
   -- Scope
   --   The root module of this game's specification. It states the figures the
   --   platform also states, so the gate can hold the two equal, and one surface
   --   with one guarantee, so the specification is checked rather than merely
   --   present. What the game is, how it starts and how it ends is still to be
   --   specified — here, or in modules that import this one.
   --
   -- Includes
   --   - The six figures @steven-cutting/biscuit-games states in
   --     appearance.allium, operation.allium and play-surfaces.allium, restated
   --     under the same names so tests/platformSpecs.test.ts can hold each equal
   --     to the shipped text and to src/lib/config.ts.
   --   - The Play surface: the one surface the game has before it has a game,
   --     and the width it has to lay out in.
   --
   -- Excludes
   --   - Play. Rules, entities, outcomes and what any mark means belong to the
   --     modules the game adds; this one names none of them.
   --   - Colour values, markup and mechanics. The figures below are thresholds a
   --     rendering either meets or does not, and they name no colour.
   --
   -- Dependencies
   --   None. This is the root module. Allium has no cross-repository import, so
   --   the platform's three modules are held equal by test rather than imported.

   ------------------------------------------------------------
   -- Given
   ------------------------------------------------------------

   given {
       -- How wide the surface has to lay out in, in CSS pixels. The device
       -- decides it and the game only ever lays out to it.
       viewport_width: Integer
   }

   ------------------------------------------------------------
   -- Config
   ------------------------------------------------------------

   config {
       -- Contrast ratios, as WCAG 2.2 computes them: the AA bar for text and
       -- the AA bar for anything that is not text. Stated by the platform in
       -- appearance.allium, which @steven-cutting/biscuit-games ships, and held
       -- equal to it by tests/platformSpecs.test.ts.
       minimum_text_contrast: Decimal = 4.5
       minimum_boundary_contrast: Decimal = 3.0

       -- CSS pixels across a control, in both directions, and the narrowest
       -- viewport every figure has to survive. Stated by the platform in
       -- operation.allium and held equal by tests/platformSpecs.test.ts.
       minimum_touch_target: Integer = 44
       narrowest_supported_width: Integer = 320

       -- How far an unmarked cell sits from a marked one, and absent from exact.
       -- Stated by the platform in play-surfaces.allium and held equal by
       -- tests/platformSpecs.test.ts.
       minimum_state_separation: Decimal = 3.0
       minimum_mark_separation: Decimal = 2.0
   }

   ------------------------------------------------------------
   -- Surfaces
   ------------------------------------------------------------

   -- Where the game is played. Today it carries nothing but the platform's
   -- chrome and the room the game will take; every surface the game adds is
   -- reached from here.
   surface Play {
       let within_supported_width = viewport_width >= config.narrowest_supported_width

       exposes:
           within_supported_width

       @guarantee EveryFigureHoldsAtTheNarrowestWidth
           -- Every control on this surface is at least config.minimum_touch_target
           -- across in both directions; its text reaches
           -- config.minimum_text_contrast against what is behind it and its
           -- boundary config.minimum_boundary_contrast against the page; a marked
           -- cell stands off an unmarked one by config.minimum_state_separation
           -- and absent stands off exact by config.minimum_mark_separation. All
           -- of it holds down to config.narrowest_supported_width, at which
           -- nothing scrolls sideways.
   }
   ```

   Read as the test reads it, `figures()` returns the six names with 4.5, 3, 44, 320,
   3, 2, and `clauses()` returns one entry keyed
   `Play.EveryFigureHoldsAtTheNarrowestWidth`.

3. Hold the test to this text, the same way (`ai_tmp/t06/platformSpecs.test.ts`, diff,
   replace only if different). Lines 37-100 and 181-194 of
   `P/tests/platformSpecs.test.ts` are carried byte for byte; everything else is the
   adaptation CONVENTIONS.md §7 specifies. It is already formatted to the render's
   Prettier settings (`printWidth` 100, single quotes, no trailing commas), and it
   contains no "Poodl": `test_no_poodl_outside_provenance` allows the word in
   `tests/platform.ts` and `tests/restated.ts` but not here.

   ```ts
   import { readdirSync, readFileSync } from 'node:fs';
   import { resolve } from 'node:path';
   import { describe, expect, it } from 'vitest';

   import { platformFile, platformPath } from './platform';
   import { RESTATED } from './restated';
   import {
     MINIMUM_BOUNDARY_CONTRAST,
     MINIMUM_MARK_SEPARATION,
     MINIMUM_STATE_SEPARATION,
     MINIMUM_TEXT_CONTRAST,
     MINIMUM_TOUCH_TARGET,
     NARROWEST_SUPPORTED_WIDTH
   } from '../src/lib/config';

   /*
    * The clauses this game restates from the platform's specifications, held
    * equal to the text the platform ships, and the figures the platform states,
    * held equal to `src/lib/config.ts` and to every module under `docs/specs/`
    * that states one.
    *
    * Nothing else anywhere compares the two. Allium has no cross-repository
    * import, and putting a module inside `node_modules` does not give it one:
    * `just check-specs` reads this game's modules alone and the hub's gate reads
    * its three, and both stay green while the clauses drift apart. Only a person
    * diffing the texts side by side would notice, which is to say nobody would.
    *
    * It is meant to be over-sensitive. A reworded comma fails it, and that failure
    * is the one moment somebody is required to say whether the platform's meaning
    * moved. When it did, the clause is amended in the hub and taken here as a
    * version — never reworded here, which is what the failure is for.
    *
    * It compares clauses by the surface or contract that states them, not by name.
    * `FullyKeyboardOperable` is stated once by the platform, for its own
    * `Operation` surface, and a game may state it under several surfaces of its
    * own, each with the wording that surface needs. A register keyed by bare name
    * would compare one of those to the platform's and demand the rest be reworded.
    *
    * Which clauses are restated is the game's to say, in `tests/restated.ts`. A
    * fresh game restates none, and this file still holds the figures.
    */

   /** How a clause body reads once the shape of the comment is taken off it. */
   function flatten(body: readonly string[]): string {
     return body
       .map((line) => line.trim().replace(/^--[ ]?/u, ''))
       .join(' ')
       .replace(/\s+/gu, ' ')
       .trim();
   }

   /**
    * Every clause in a module, by the surface or contract stating it and its name.
    *
    * A body runs to the first line that is not a comment. The platform separates
    * the paragraphs of its longer clauses with lines that are exactly `--`, which
    * are part of the body and not the end of it.
    */
   function clauses(text: string): Map<string, string> {
     const found = new Map<string, string>();
     const lines = text.split('\n');
     let scope = '';

     for (const [index, line] of lines.entries()) {
       const opens = /^[ \t]*(?:surface|contract)[ \t]+(?<name>\w+)[ \t]*\{/u.exec(line);

       if (opens?.groups?.['name'] !== undefined) {
         scope = opens.groups['name'];
         continue;
       }

       const clause = /^[ \t]*@(?:guarantee|invariant)[ \t]+(?<name>\w+)[ \t]*$/u.exec(line);

       if (clause?.groups?.['name'] === undefined) {
         continue;
       }

       const body: string[] = [];

       for (const following of lines.slice(index + 1)) {
         if (!following.trim().startsWith('--')) {
           break;
         }
         body.push(following);
       }

       found.set(`${scope}.${clause.groups['name']}`, flatten(body));
     }

     return found;
   }

   /** Every figure a `config` block states as a number. `Duration` is not one. */
   function figures(text: string): Map<string, number> {
     const found = new Map<string, number>();
     const pattern =
       /^[ \t]*(?<name>\w+)[ \t]*:[ \t]*(?:Integer|Decimal)[ \t]*=[ \t]*(?<value>[0-9.]+)/gmu;

     for (const match of text.matchAll(pattern)) {
       if (match.groups?.['name'] !== undefined && match.groups['value'] !== undefined) {
         found.set(match.groups['name'], Number(match.groups['value']));
       }
     }

     return found;
   }

   const SPECS = resolve(process.cwd(), 'docs', 'specs');

   /** Every module this game keeps, which is what `just check-specs` reads. */
   function gameModules(): string[] {
     return readdirSync(SPECS)
       .filter((name) => name.endsWith('.allium'))
       .sort();
   }

   function gameModule(name: string): string {
     return readFileSync(resolve(SPECS, name), 'utf8');
   }

   /** Which platform module states each figure, and what `config.ts` mirrors it as. */
   const FIGURES = [
     { figure: 'minimum_text_contrast', module: 'appearance.allium', mirrored: MINIMUM_TEXT_CONTRAST },
     {
       figure: 'minimum_boundary_contrast',
       module: 'appearance.allium',
       mirrored: MINIMUM_BOUNDARY_CONTRAST
     },
     { figure: 'minimum_touch_target', module: 'operation.allium', mirrored: MINIMUM_TOUCH_TARGET },
     {
       figure: 'narrowest_supported_width',
       module: 'operation.allium',
       mirrored: NARROWEST_SUPPORTED_WIDTH
     },
     {
       figure: 'minimum_state_separation',
       module: 'play-surfaces.allium',
       mirrored: MINIMUM_STATE_SEPARATION
     },
     {
       figure: 'minimum_mark_separation',
       module: 'play-surfaces.allium',
       mirrored: MINIMUM_MARK_SEPARATION
     }
   ] as const;

   const MODULES = ['appearance.allium', 'operation.allium', 'play-surfaces.allium'] as const;

   describe('the platform specifications this game restates', () => {
     it.each(MODULES)('reads %s from the installed package', (module) => {
       expect(platformPath(`specs/${module}`)).toContain('node_modules');
     });

     it.each(RESTATED.flatMap((entry) => entry.clauses.map((name) => ({ ...entry, name }))))(
       '$file states $name exactly as $module does',
       ({ module, theirs, file, ours, alias, name }) => {
         const platform = clauses(platformFile(`specs/${module}`)).get(`${theirs}.${name}`);
         const restated = clauses(gameModule(file)).get(`${ours}.${name}`);

         expect(platform, `${module} no longer states ${theirs}.${name}`).toBeDefined();
         expect(restated, `${file} no longer states ${ours}.${name}`).toBeDefined();
         expect(
           alias === null ? restated : (restated ?? '').replaceAll(`${alias}/config.`, 'config.')
         ).toBe(platform);
       }
     );

     it.each(FIGURES)('agrees with $module on config.$figure', ({ figure, module, mirrored }) => {
       const platform = figures(platformFile(`specs/${module}`)).get(figure);

       expect(platform, `${module} no longer states ${figure}`).toBeDefined();
       expect(mirrored, `src/lib/config.ts disagrees with ${module} on ${figure}`).toBe(platform);
       // A game module states a platform figure only where it has a surface for
       // it; where it does, it states the same value.
       for (const name of gameModules()) {
         const stated = figures(gameModule(name)).get(figure);
         if (stated !== undefined) {
           expect(stated, `${name} disagrees with ${module} on ${figure}`).toBe(platform);
         }
       }
     });

     /*
      * The version is what makes drift visible, and a lockfile alone would not
      * say it: this asserts the tree these comparisons just read is the one
      * `package.json` pins, so a stale `node_modules` reports itself rather than
      * quietly proving the wrong thing.
      */
     it('reads the version package.json pins', () => {
       const installed = JSON.parse(platformFile('package.json')) as { version: string };
       const pinned = JSON.parse(readFileSync(resolve(process.cwd(), 'package.json'), 'utf8')) as {
         dependencies: Record<string, string>;
       };

       expect(pinned.dependencies['@steven-cutting/biscuit-games']).toBe(installed.version);
     });
   });
   ```

   `RESTATED` is typed `readonly Restatement[]` in `tests/restated.ts`, so `flatMap`
   over the empty table registers no case and throws nothing; `it.each([])` is a no-op
   (CONVENTIONS.md §7). `alias` replaces P's `prefixed` flag: `null` means no
   normalisation, a string is the `use` alias to strip from `<alias>/config.`.

4. Render and prove the module through the shipped scripts. `just render` renders the
   working tree, uncommitted edits included, with the default answers, so the module
   lands as `docs/specs/tic_tac_toe_beans.allium`. The render has no lockfile and every
   recipe runs `uv run --frozen`, so `uv lock` comes first. This step needs the network:
   `uv lock` reads PyPI and `install-allium` downloads the 3.6.1 release into
   `.tools/bin/`, which the render's `.gitignore` ignores. Nothing here needs the
   GitHub Packages token.

   ```sh
   rm -rf ai_tmp/render
   just render
   cd ai_tmp/render
   git init -q -b main
   uv lock
   just install-allium
   just check-specs
   just analyse-specs
   git status --porcelain
   ```

   The last command lists every rendered file as untracked and nothing under
   `.tools/`. Both `check-specs` and `analyse-specs` print one JSON block with
   `"diagnostics": []` and `"findings": []` and then, from `run_allium.py`,
   `allium check: 1 specifications, no diagnostics and no findings.` (or `analyse`;
   the script does not singularise). Quote all of it in the hand-back notes.

   If T01 or T02 has not merged yet, the render's `Justfile`, `pyproject.toml` or
   `scripts/` may still be T00's stubs and the recipes may not run. Then run the real
   scripts as copies inside the scratch render only, never inside `template/`: copy
   `H/scripts/install_allium.py` and `P/scripts/run_allium.py` into
   `ai_tmp/render/scripts/` and, from `ai_tmp/render`, run
   `python3 scripts/install_allium.py`, `python3 scripts/run_allium.py check` and
   `python3 scripts/run_allium.py analyse` (both scripts are standard library only).
   The expected output is the same. Say in the hand-back notes which path was taken.

5. Act on a diagnostic only if one appears. `run_allium.py` prints each as
   `docs/specs/tic_tac_toe_beans.allium:<line>:<col>: <severity>: <code>: <message>`.

   - `code` printed as `parse error` (the JSON carries `"code": null`,
     `"severity": "error"`, a message such as `expected '}', found end of file`): the
     text was not copied exactly. Diff against step 2 again; compare the block shapes
     with `H/docs/specs/operation.allium` lines 68-85, 91-108 and 211-252.
   - A named code on the `surface Play {` line (doubt a): rename the identifier to
     `PlaySurface` on that line and in the Includes bullet ("The PlaySurface surface");
     the `clauses()` key becomes `PlaySurface.EveryFigureHoldsAtTheNarrowestWidth` and
     nothing else reads the name.
   - A named code asking for `contracts:` (doubt b): add, above the `-- Where the game
     is played.` comment, the contract below, and insert `contracts:` with
     `fulfils LaidOut` after the `exposes:` block, blank line before and after, at the
     same indentation as `exposes:`.

     ```text
     -- What every surface of this game owes to being laid out.
     contract LaidOut {
         @invariant FitsTheNarrowestWidth
             -- Nothing scrolls sideways at config.narrowest_supported_width.
     }
     ```

   - `allium.field.unused` on a figure (doubt c), which `allium check` reports as an
     `info` and `run_allium.py` refuses all the same: add, after the existing `let` and
     before `exposes:`, one `let` per unreferenced figure in this shape, then rerun.

     ```text
         let text_bar = config.minimum_text_contrast
         let boundary_bar = config.minimum_boundary_contrast
         let target = config.minimum_touch_target
         let state_gap = config.minimum_state_separation
         let mark_gap = config.minimum_mark_separation
     ```

   Any edit here changes the text CONVENTIONS.md §7 carries. This ticket edits the
   template file; the correction to CONVENTIONS.md is handed back (a pull request on
   `main`, CONVENTIONS.md preamble), with the quoted diagnostic. Never add a waiver: a
   finding cannot be waived, and a diagnostic only where the checker itself is wrong.

6. If `tests/test_specs.py` exists at the repository root (T02 merged), run it from the
   root with the network gate on; it renders, installs the binary and runs both
   commands, so it is the same proof under pytest.

   ```sh
   BISCUIT_TEMPLATE_NETWORK=1 just test tests/test_specs.py
   ```

   Expected: `1 passed`. If the file does not exist yet, step 4 is the check; say so in
   the hand-back notes and T02 runs it on merge.

7. Run the figure cases against the installed package, if a token is available. This is
   the subset of what T10's `just test-full` runs and needs a GitHub token carrying
   `read:packages` in `~/.npmrc` (`//npm.pkg.github.com/:_authToken=<your token>`),
   the network and a Chromium download of a few minutes. From `ai_tmp/render`:

   ```sh
   just initialize
   npx vitest run --config vite.config.ts tests/platformSpecs.test.ts
   ```

   Expected: `Tests  10 passed (10)`: three `reads ... from the installed package`, six
   `agrees with ... on config....` and `reads the version package.json pins`; no
   `states ... exactly as` case, because `RESTATED` is empty. Without a token,
   `scripts/initialize.sh` fails at `npm install` (line 12); record that and leave the
   run to T10.

8. `just check` at the repository root: the fast suite renders the working tree and
   the two files pass the inventory, residue and no-Poodl tests along with the hook
   gate (editorconfig-checker and typos read `template/` at source).

9. Fill in the hand-back notes, set `status: done`, commit on the ticket branch.
   **Authorisation required:** pushing the branch and opening the pull request are
   separately authorised (CONVENTIONS.md §11); stop and ask before either.

## Acceptance criteria

- [ ] `template/docs/specs/{{ game_slug }}.allium.jinja` is byte-equal to the step 2
  text, or differs only by an edit step 5 directs, with the diagnostic that forced it
  quoted in the hand-back notes.
- [ ] `template/tests/platformSpecs.test.ts` is byte-equal to the step 3 text; its
  lines 43-106 equal `P/tests/platformSpecs.test.ts` lines 37-100.
- [ ] In `ai_tmp/render`, `just check-specs` and `just analyse-specs` exit 0 and each
  prints one block with `"diagnostics": []` and `"findings": []` for
  `docs/specs/tic_tac_toe_beans.allium`; the output is quoted in the hand-back notes.
- [ ] `git status --porcelain` in the render lists nothing under `.tools/`.
- [ ] The module's six figures equal the exports in `src/lib/config.ts` (4.5, 3.0, 44,
  320, 3.0, 2.0) and the shipped text: `H/docs/specs/appearance.allium` lines 97-98,
  `H/docs/specs/operation.allium` lines 96 and 101,
  `H/docs/specs/play-surfaces.allium` lines 126 and 141.
- [ ] The rendered module contains `{{`, `{%` and `{#` nowhere; neither file contains
  "poodl" in any case; the module has no tab and no trailing whitespace.
- [ ] `BISCUIT_TEMPLATE_NETWORK=1 just test tests/test_specs.py` passes if the file
  exists; otherwise the hand-back notes say the manual run stood in.
- [ ] `just check` is green at the repository root.
- [ ] The CONVENTIONS.md §12 claim about this module is answered in the hand-back notes,
  doubt by doubt.
- [ ] No file outside the two listed changed, apart from this ticket's `status:` line;
  nothing under `template/scripts/`, P or H was edited.

## Verification

From the repository root, after `just sync`:

```sh
just check
```

Expected: `lock-check`, `lint`, `typecheck` and `test` all pass; no test under `tests/`
fails on either file.

```sh
rm -rf ai_tmp/render && just render && cd ai_tmp/render && git init -q -b main && uv lock
just install-allium
```

Expected: `Rendered into ai_tmp/render`; `uv lock` writes `uv.lock`; the install prints
`downloading https://github.com/juxt/allium-tools/releases/download/v3.6.1/allium-<target>.tar.gz`
and then `installed allium 3.6.1 at <render>/.tools/bin/allium`, exit 0.

```sh
just check-specs && just analyse-specs
```

Expected, for each of the two:

```text
{
  "command": "check",
  "diagnostics": [],
  "findings": [],
  "spec_file": "docs/specs/tic_tac_toe_beans.allium"
}
allium check: 1 specifications, no diagnostics and no findings.
```

with `analyse` in place of `check` on the second run; exit 0 both times.

```sh
git status --porcelain
```

Expected: no line naming `.tools/`.

```sh
cd ../.. && BISCUIT_TEMPLATE_NETWORK=1 just test tests/test_specs.py
```

Expected: `1 passed` (only once T02 has merged; otherwise `pytest` reports the file as
not found, and the three commands above are the check).

Optional, with a `read:packages` token in `~/.npmrc`, from `ai_tmp/render`:

```sh
just initialize && npx vitest run --config vite.config.ts tests/platformSpecs.test.ts
```

Expected: `Test Files  1 passed (1)` and `Tests  10 passed (10)`.

## Hand-back notes

Filled in by the agent that executes this ticket.

- What was verified and how: the exact `check-specs` and `analyse-specs` output from
  the render, which path step 4 took (recipes, or copied scripts), whether
  `tests/test_specs.py` existed and its result, whether step 7 ran and its result, and
  the `just check` outcome.
- The CONVENTIONS.md §12 claim, doubt by doubt: bare `Play` accepted or not, no
  `contracts:` accepted or not, comment-only figure references accepted or not, each
  with the diagnostic if there was one.
- What deviated from the ticket and why: any edit to the module, with the diagnostic
  that forced it and the CONVENTIONS.md §7 correction to be made on `main`.
- What was handed back to another ticket: anything found wrong in `src/lib/config.ts`
  or `tests/restated.ts` (T05), in the shipped scripts (T02), or in the render's
  `Justfile` and `pyproject.toml` (T01).
- Which open points were settled, with the command and its output.

## Open points

- CONVENTIONS.md §12, first claim: the seed module parses and reports no diagnostics
  under the pinned binary, with bare `Play`, no `contracts:` block and figures cited
  only in comment bodies. Check: step 4 (`just install-allium && just check-specs &&
  just analyse-specs` in the render). Expected to hold; step 5 says what to do if not.
- ESLint under the hub's `strictTypeChecked` configuration on the lines of the test
  that are not P's (`gameModules`, `gameModule`, `FIGURES` with `mirrored`, the
  `alias` branch, the `for` loop). P's own lines pass P's stricter superset of the same
  configuration; the new lines were written to it but not run through it. Check:
  `npm run lint` in the render after `just initialize` (needs the token), or T10's
  `just test-full`; `initialize.sh` runs `npm run lint:fix` and stops on anything it
  cannot fix.
- `uv lock` in a render before T01 has merged: the render's `pyproject.toml` may still
  be T00's stub. Check: `uv lock` in step 4; if it refuses, take the copied-scripts
  path and say so.
- A `game_name` answer with trailing whitespace renders it onto the module's third
  line, where the render's editorconfig hook (`trim_trailing_whitespace = true`)
  would flag it, because `{{ game_name }}` is not trimmed there while every other use
  in `copier.yml` is. Check, from the repository root:
  `uv run --frozen copier copy --defaults --vcs-ref=HEAD --quiet --data 'game_name=Tic Tac Toe Beans ' . ai_tmp/ws`
  then `grep -n ' $' ai_tmp/ws/docs/specs/tic_tac_toe_beans.allium`. If it prints a
  line, the remedy is `{{ game_name | trim }}` on that line and a CONVENTIONS.md §7
  correction, handed back rather than applied here.
- Step 7 depends on a `read:packages` token being present on the executing machine.
  If it is not, the figure cases run first under T10's `just test-full`; record which.
