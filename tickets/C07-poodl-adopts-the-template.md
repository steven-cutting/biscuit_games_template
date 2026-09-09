---
id: C07
title: Poodl adopts the template, or stays the reference implementation
status: open
depends_on: [T11]
parallel_with: []
branch: ticket/c07-poodl-adopts-the-template
estimated_size: XL
---

# C07: Poodl adopts the template, or stays the reference implementation

## Context

Poodl (`/Users/scutting/projects/poodl`, commit `0a46a485`) is the game the template was
distilled from, and it is not on the template: it has no `.copier-answers.yml` (checked
2026-09-09), so `copier update` cannot run there. Everything the template later fixes in
a managed file reaches every rendered game and never reaches Poodl.

`copier update` has preconditions, all in copier 9.18.2's `_main.py` `run_update`
(lines 1337-1367): the destination must be a git repository (1344), must be clean (1348-
1350), must carry the old template references in its answers file (1355), and both the
recorded and the current template versions must be detectable (1358-1367), which is
why the template tags releases (CONVENTIONS.md §10) and why T11 tags `v0.1.0` before
the first consumer render.

What diverges between Poodl and a render, and which side is Poodl's design rather than
drift (CONVENTIONS.md §1 and §4):

- `Justfile` lines 68-80: `stage` and `stage-preview`, Poodl's domain-root staging.
  Design.
- `.github/workflows/pages.yml`: `BASE_PATH: /poodl` at line 22 and `npm run stage` at
  line 67, with `site-root/` and `scripts/stage_site.sh`. Design (Poodl lives at a domain
  root; the hub's `docs/decisions/0012-the-domain-root-stays-with-poodl.md` records it).
- `eslint.config.js` lines 44-45 onward: the two word-vocabulary rules. Design.
- `.github/workflows/chromatic.yml`: assumes the token; the render takes the hub's
  guarded version. Drift.
- `scripts/validate_docs.py` and `scripts/validate_agents.py`: Poodl's are the older,
  looser copies; the render ships the hub's, which Poodl's files already satisfy
  (CONVENTIONS.md §1). Drift.
- `src/lib/data/`, `src/lib/app/`, `src/lib/domain/`, the word-list port, the extra
  ports, the extra decisions and `how-to/replace-the-word-lists.md`: Poodl's game.
  Game-added files, which `copier update` never touches (CONVENTIONS.md §5).
- Every handbook page: same structure, Poodl's prose. Managed in the template; on the
  first update each differs from the old render's side, so each conflicts once.

This ticket is a recommendation (CONVENTIONS.md §1, decision 3) with a real fallback
that must be decided before it is picked up: Poodl stays off the template as the
reference implementation, generic fixes flow from Poodl to the template by hand, and
Poodl's `AGENTS.md` provenance (line 145, `## Provenance`; "Deliberate deviations" at
line 149) says so. Every change to Poodl is a pull request there, separately authorised
(CONVENTIONS.md §11).

Read first: CONVENTIONS.md §1, §3 (the answers Poodl would give), §4, §5, §10, §11,
§13 ("C07 pays a per-page reconciliation"); Poodl's `AGENTS.md`, `Justfile`,
`.github/workflows/pages.yml`, `eslint.config.js`; the template `CHANGELOG.md`.

## Goal

Either Poodl runs `copier update` and takes future template releases with its
divergences kept in game-owned places, or the fallback is recorded and the template
stays the derived artefact. If adoption: `.copier-answers.yml` committed in Poodl with
`_src_path: gh:steven-cutting/biscuit_games_template` and `_commit: v0.1.0`, Poodl's
`just check` green after converging drift, and a dry update from `v0.1.0` to a test tag
producing hunks only in managed files and conflicts only in the named handbook pages.

## Non-goals

- Rewriting Poodl's handbook prose to the template's (the pages stay Poodl's; the cost
  is one reconciliation per page on the first update).
- Making `pages.yml` or the handbook seed for every game to spare Poodl (a class change
  is a template MAJOR, CONVENTIONS.md §10, and would take the deploy workflow away from
  every future game's update path; the extension points below are the alternative).
- Bumping Poodl's dependencies or its hub package version.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `poodl: .copier-answers.yml` | other repo | new | Hand-written, per Steps 5 |
| `poodl: scripts/validate_docs.py`, `poodl: scripts/validate_agents.py` | other repo | hub files | Take the hub's (drift) |
| `poodl: .github/workflows/chromatic.yml` | other repo | render's file | Take the guarded version (drift) |
| `poodl: Justfile`, `poodl: Justfile.local` | other repo | Poodl's | `stage` and `stage-preview` move to `Justfile.local`; the `Justfile` gains the import line |
| `poodl: eslint.config.js`, `poodl: eslint.local.js` | other repo | Poodl's | The vocabulary rules move to the local file |
| `poodl: AGENTS.md` | other repo | Poodl's | Provenance names the template and `v0.1.0`, or the fallback |
| `template/Justfile` | M† | T01's file | Gains `import? 'Justfile.local'` as its last line |
| `template/eslint.config.js` | M† | T01's file | Gains an optional import of `eslint.local.js` |
| `template/.gitignore` | M† | T01's file | Nothing: the two local files are committed, not ignored |
| `CHANGELOG.md` | repo | T12's file | Unreleased, Managed: the two extension points (MINOR) |

## Steps

1. **Decide the fallback question first.** With the maintainer, before any file
   changes: is one reconciliation per handbook page (about 28 pages) worth Poodl taking
   template updates? If not, execute only step 8 (the fallback) and close the ticket.
2. **Add the extension points to the template** (a template pull request of its own,
   merged and tagged before Poodl is touched): append `import? 'Justfile.local'` as
   the last line of `template/Justfile` (the syntax works on just 1.51.0: a two-line
   Justfile with that import and a `default` recipe prints `ok` when the local file is
   absent; checked 2026-09-09), and make `template/eslint.config.js` end by spreading
   an optional local configuration:

   ```js
   import { existsSync } from 'node:fs';

   const local = existsSync(new URL('./eslint.local.js', import.meta.url))
     ? (await import('./eslint.local.js')).default
     : [];

   export default [/* the shared configuration */, ...local];
   ```

   Keep the shared configuration as it is; only the tail changes. Run `just test` (the
   verbatim test for `eslint.config.js` now compares against the edited source), list
   both under Managed in the template `CHANGELOG.md`, and **Authorisation required:**
   open the template pull request and tag the MINOR release after it merges.
3. **Render with Poodl's answers** on a Poodl branch (**Authorisation required:** a
   branch in Poodl): `uvx copier copy --vcs-ref <the new tag> --data game_name=Poodl
   --data game_slug=poodl --data 'description=<Poodl's README sentence>' --data
   repository=steven-cutting/poodl gh:steven-cutting/biscuit_games_template ai_tmp/render`
   and diff the render against Poodl's tree: `diff -r --brief ai_tmp/render .` filtered
   to the paths the render ships.
4. **Converge drift toward the render** where the difference is not Poodl's design: the
   two validators (take the hub's), `chromatic.yml` (take the guarded one),
   `.storybook/*` prose, the ports' comments. Keep Poodl's `.gitignore` and
   `.prettierignore` extras. Run Poodl's `just check`.
5. **Route Poodl's design through the extension points.** Move `stage` and
   `stage-preview` (Poodl's `Justfile` lines 68-80) into `Justfile.local`; move the
   vocabulary rules into `eslint.local.js` exporting an array; take the template's
   `Justfile` and `eslint.config.js` otherwise verbatim. `pages.yml` stays Poodl's own:
   record in the hand-back notes that its first update will conflict, and that the
   template side is a suggestion (CONVENTIONS.md §10, point 4). Run `just check`.
6. **Write `.copier-answers.yml` by hand:**

   ```yaml
   # Changes here will be overwritten by Copier; NEVER EDIT MANUALLY
   _commit: v0.1.0
   _src_path: gh:steven-cutting/biscuit_games_template
   description: <Poodl's sentence>
   game_name: Poodl
   game_slug: poodl
   repository: steven-cutting/poodl
   ```

   using the `_commit` of the tag that carries the extension points (not `v0.1.0` if
   step 2 tagged later), and the answer names exactly as CONVENTIONS.md §3 spells them.
   Add `.copier-answers.yml` to Poodl's `.prettierignore` (CONVENTIONS.md §13). Commit
   on the branch.
7. **Dry update.** Tag a throwaway prerelease on the template (`v0.2.0rc1`, on a scratch
   branch; **Authorisation required**) carrying one managed edit, then in Poodl run
   `uvx copier update --skip-answered --pretend --prereleases --vcs-ref v0.2.0rc1` and
   read the report: hunks only in managed files; conflicts only in the handbook pages
   and `pages.yml`. Record the list of conflicting pages. Delete the throwaway tag.
8. **Fallback, if step 1 said no** (or step 7 conflicts in files it should not): revert
   the Poodl branch, and instead add one paragraph to Poodl's `AGENTS.md` Provenance
   (after line 149) saying Poodl is the reference implementation the template was
   distilled from, that it does not take template updates, and that generic fixes are
   carried to `steven-cutting/biscuit_games_template` by hand. **Authorisation
   required:** the Poodl pull request either way.

## Acceptance criteria

- [ ] The decision from step 1 is recorded in the hand-back notes and in Poodl's
      `AGENTS.md` provenance.
- [ ] If adopting: `.copier-answers.yml` committed in Poodl with the tag's `_commit` and
      the GitHub `_src_path`; Poodl's `just check` green after step 5; the dry update
      shows hunks only in managed files and conflicts only in the named pages and
      `pages.yml`; Poodl's three required checks green on the pull request.
- [ ] The template's two extension points exist, are listed in `CHANGELOG.md` under
      Managed, and `just test` is green (a render's `Justfile` with no `Justfile.local`
      still runs every recipe; `eslint.config.js` with no `eslint.local.js` still lints).
- [ ] If the fallback: Poodl's provenance paragraph exists and no other Poodl file
      changed.

## Verification

Template repository, after step 2:

```sh
just test
just render ai_tmp/render && cd ai_tmp/render && just --list >/dev/null && echo "justfile ok"
```

Expected: green; `justfile ok` with no `Justfile.local` present.

Poodl branch, after step 6:

```sh
just check
uvx copier update --skip-answered --pretend --prereleases --vcs-ref v0.2.0rc1 2>&1 | tee ai_tmp/update-report.txt
grep -c '<<<<<<< before updating' -r docs AGENTS.md Justfile package.json || true
```

Expected: `just check` green; the report lists hunks under managed paths only; the
marker count is zero outside the handbook pages and `pages.yml` (a `--pretend` run
writes nothing; run without `--pretend` on a throwaway copy of the branch to count
markers).

## Hand-back notes

Filled in by the agent that executes this ticket.

- The step 1 decision and who took it.
- The diff summary from step 3: which paths were drift, which were design, which were
  game-added.
- The list of pages that conflict on the first update, and whether the maintainer
  accepted paying that once or chose the fallback.
- The pull requests opened (template, Poodl) and their outcomes.
- Which open points were settled.

## Open points

- `just import? 'Justfile.local'` on just 1.51.0: checked on 2026-09-09 (`ok` printed
  with the local file absent); re-check after any just bump in the template
  (CONVENTIONS.md §12).
- Whether ESLint's flat config accepts a top-level `await` in `eslint.config.js` under
  Poodl's Node 26 and `"type": "module"`; check with `npm run lint` in a render.
- Whether copier's `--pretend` reports conflicts or only hunks; if only hunks, the
  marker count on a throwaway copy is the check (Verification).
- Whether Poodl's `pages.yml` should instead become a caller of C01's reusable
  `game-pages.yml` with a staging input, which would remove its conflict; decide with
  C01.
- Whether the per-page reconciliation is accepted (CONVENTIONS.md §13): the step 1
  decision.
