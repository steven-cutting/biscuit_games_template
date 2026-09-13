---
id: T03
title: "Workflows: ci.yml, chromatic.yml, pages.yml and the Copilot adapter"
status: done
depends_on: [T00]
parallel_with: [T01, T02, T04, T05, T06, T07, T08, T09]
branch: ticket/t03-workflows
estimated_size: S
---

# T03: Workflows: ci.yml, chromatic.yml, pages.yml and the Copilot adapter

## Context

Every rendered game carries three GitHub Actions workflows and one byte-pinned provider
adapter, and none of the four is rendered by Jinja. `${{ }}` is an undefined variable
under `StrictUndefined` and `{#` opens a Jinja comment, so a workflow never carries the
`.jinja` suffix (CONVENTIONS.md §1, fact 1, and §6, rule 2); `pages.yml` reads the
repository name from the workflow event instead of from an answer. The four files are
byte-copied into every game, and `tests/test_render.py`
`test_verbatim_files_are_byte_identical` (CONVENTIONS.md §9) holds each rendered file
equal to its template source, so what this ticket writes under `template/` is exactly
what a game gets.

T00 merged before this ticket and shipped a placeholder at each of the four paths so the
inventory test could pass from the first commit. For `.github/copilot-instructions.md`
that placeholder has to be the exact adapter already, because T00's
`tests/test_validators.py` runs the hub's `validate_agents.py` against a render and that
script compares the adapter whole; expect step 5 to change nothing. T10, the harness
completion, waits for this lane and the eight beside it; T11 renders `tic_tac_toe_beans`
from the tagged template and is where `pages.yml` runs for the first time.

Sources, at the commits CONVENTIONS.md §0 pins; every line number in this ticket was
read at those commits:

- P = `/Users/scutting/projects/poodl` at `0a46a485`: `P/.github/workflows/ci.yml`
  (167 lines), `P/.github/workflows/chromatic.yml` (249 lines),
  `P/.github/workflows/pages.yml` (83 lines), `P/.github/copilot-instructions.md`
  (235 bytes), and `P/Justfile` lines 30-32, the `lock-check` recipe the new `ci.yml`
  step calls (`uv lock --check`, then `npm ci --ignore-scripts --dry-run --no-audit`).
- H = `/Users/scutting/projects/biscuit_games` at `09b4894a`:
  `H/.github/workflows/chromatic.yml` (265 lines: the token guard is lines 201-217, the
  guarded publish step 223-228, the three-way report step 230-265) and
  `H/scripts/validate_agents.py` lines 33-40 (the `ADAPTERS` constant) and 169-176
  (`_check_adapters`, which compares the whole file, final newline included).
- CONVENTIONS.md: §4 (the four rows), §7 "Managed adaptations against Poodl files" (the
  three workflow entries, `pages.yml` in full), §9 (the template repository's gate runs
  actionlint over `template/.github/workflows/*.yml` at source, and the three tests this
  ticket keeps green), §11 (rules for lanes), §12 (the open point below).

One correction to CONVENTIONS.md §7: P's `chromatic.yml` has 249 lines, so its report
step is lines 232-249, not "232-250". Every other line number cited there for these
files was checked and is right.

## Goal

The three workflows under `template/.github/workflows/` in their final form: verbatim
`.yml`, every `${{ }}` intact, no game name anywhere, P's pins and action SHAs
unchanged. `template/.github/copilot-instructions.md` byte-identical to P's, to H's and
to the `ADAPTERS` string. `just check` green in the template repository, with actionlint
clean over the three shipped workflows at source and
`test_verbatim_files_are_byte_identical`, `test_pins_agree` and
`test_no_poodl_outside_provenance` passing.

## Non-goals

- The template repository's own `.github/workflows/ci.yml`: its `fast` job is T00's and
  its `full` job is T10's. This ticket touches only the shipped copies under
  `template/.github/`.
- The `lock-check` recipe the new `ci.yml` step calls: `template/Justfile` is T01's,
  which keeps P's lines 30-32 unchanged.
- `template/CLAUDE.md`, the other byte-pinned adapter, and every skill and bridge: T04.
- `template/chromatic.config.json` and `template/svelte.config.js`, which reads
  `BASE_PATH`: T01. `template/static/.nojekyll`, which rides along inside `build/`: T05.
- The handbook pages that describe these workflows: `deploy-to-github-pages` (T07),
  `quality-gates` and `maintenance` (T08), decisions 0006 and 0010 (T09).
- Repository settings. The Pages source, the `CHROMATIC_PROJECT_TOKEN` secret, branch
  protection and the package read grant are C03's, applied by the maintainer. Pushing a
  render and watching `pages.yml` run is T11's.
- Reusable `workflow_call` versions of these workflows: C01.
- Any test. If `tests/test_render.py` would need a change to pass over these files, the
  change is handed back as a T00 follow-up on `main` in the hand-back notes, not made.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `template/.github/workflows/ci.yml` | M | `P/.github/workflows/ci.yml` | P verbatim except lines 58-61, where the bare npm dry run becomes `just lock-check` (step 2) |
| `template/.github/workflows/chromatic.yml` | M | `P/.github/workflows/chromatic.yml` plus `H/.github/workflows/chromatic.yml` lines 201-217, 224 and 230-265 | P with the hub's token guard grafted in (step 3) |
| `template/.github/workflows/pages.yml` | M | `P/.github/workflows/pages.yml`, rewritten as CONVENTIONS.md §7 gives it | The exact content in step 4: P lines 16-20 and 22 rewritten, 66-67 removed, 70-72 rewritten |
| `template/.github/copilot-instructions.md` | M | `P/.github/copilot-instructions.md`, identical to H's and to `ADAPTERS` | Byte for byte; unchanged if T00's placeholder already matches (step 5) |

## Steps

1. Create the worktree from `main` on `ticket/t03-workflows` (README.md, "How to pick
   up a ticket"). Confirm the sources are at the pinned commits, then read the files
   Context names:

   ```sh
   git -C /Users/scutting/projects/poodl rev-parse --short=8 HEAD          # 0a46a485
   git -C /Users/scutting/projects/biscuit_games rev-parse --short=8 HEAD  # 09b4894a
   ```

   Every later command runs from the repository root with these set:

   ```sh
   P=/Users/scutting/projects/poodl/.github/workflows
   H=/Users/scutting/projects/biscuit_games/.github/workflows
   W=template/.github/workflows
   ```

2. `template/.github/workflows/ci.yml`: P's file verbatim except lines 58-61, which
   CONVENTIONS.md §7 replaces so:

   ```diff
   -      # No token: a dry run against a complete lockfile reads the registry
   -      # for nothing, which was checked by running it with no credential in
   -      # npm's configuration at all.
   -      - run: npm ci --ignore-scripts --dry-run --no-audit
   +      # No token: the dry run against a complete lockfile reads the registry
   +      # for nothing, which was checked by running it with no credential in
   +      # npm's configuration at all, and `uv lock --check` reads no registry.
   +      - run: just lock-check
   ```

   Three `sed` substitutions on those lines produce it and nothing else in the file
   moves:

   ```sh
   sed -e '58s/a dry run/the dry run/' \
       -e "60s/at all\\./at all, and \`uv lock --check\` reads no registry./" \
       -e '61s/npm ci --ignore-scripts --dry-run --no-audit/just lock-check/' \
       "$P/ci.yml" > "$W/ci.yml"
   diff "$P/ci.yml" "$W/ci.yml" | grep -E '^[0-9]'   # exactly: 58c58 and 60,61c60,61
   ```

   The job names `frontend`, `documents` and `stories` (the required checks C03 sets),
   every action SHA and every version pin stay P's: `test_pins_agree` reads them.

3. `template/.github/workflows/chromatic.yml`: P's file plus the hub's token guard. From
   P everything is kept, in particular the header comment at lines 3-5 (a game does
   deploy Pages, so P's wording is the right one), the `chromatic` job's `permissions`
   block with `packages: read` at 174-178, `registry-url` and `scope` at 202-203 and
   `NODE_AUTH_TOKEN` at 216-220, because a game installs the platform package. From H:
   lines 201-217 (the guard's comment and its `token` step) inserted after P line 220,
   line 224 (`if: steps.token.outputs.present == 'true'`) inserted after P line 226, and
   lines 230-265 (the report step with `PUBLISHED` and the three-way `case`) in place of
   P's report step at 232-249. Compose it from the two sources:

   ```sh
   {
     sed -n '1,220p' "$P/chromatic.yml"    # through NODE_AUTH_TOKEN on `just sync`
     printf '\n'
     sed -n '201,217p' "$H/chromatic.yml"  # the guard: its comment and the `token` step
     sed -n '221,226p' "$P/chromatic.yml"  # blank, branch-name comment, the publish step's name
     sed -n '224p' "$H/chromatic.yml"      # if: steps.token.outputs.present == 'true'
     sed -n '227,231p' "$P/chromatic.yml"  # run, env with BRANCH and the token, blank
     sed -n '230,265p' "$H/chromatic.yml"  # the report step with PUBLISHED and the case
   } > "$W/chromatic.yml"
   wc -l "$W/chromatic.yml"   # 286
   ```

   The result is H's file with exactly the four Poodl-specific blocks kept. This is the
   whole expected output of `diff "$H/chromatic.yml" "$W/chromatic.yml"`:

   ```text
   3,7c3,5
   < # Visual review of the component workshop. It lives apart from `ci.yml` because it
   < # holds a secret — the only one this repository has — and answers to triggers the
   < # gate has no use for. It is not a required check. Nothing else here is separated
   < # for that reason, because nothing else here deploys: there is no Pages workflow,
   < # and decision 0012 says why.
   ---
   > # Visual review of the component workshop. It lives apart from `ci.yml` for the
   > # same reason the Pages deploy does: it holds a secret nothing else holds, and it
   > # answers to triggers the gate has no use for. It is not a required check.
   171a170,178
   >     # A job block replaces the workflow's, so the two write scopes the reply
   >     # below needs are restated here beside the read `just sync` needs for the
   >     # design system package. `authorize` keeps the workflow's block and gains
   >     # no package scope: it installs nothing.
   >     permissions:
   >       contents: read
   >       issues: write
   >       pull-requests: write
   >       packages: read
   187a195,203
   >           # @steven-cutting/biscuit-games comes from GitHub Packages, which
   >           # authenticates every request including a read of a public package.
   >           # This writes a user-level .npmrc under RUNNER_TEMP naming the
   >           # registry for the scope and reading the token from the environment
   >           # of each step that installs; the committed .npmrc names the registry
   >           # and holds nothing, and the checkout the gates prove clean stays that
   >           # way.
   >           registry-url: 'https://npm.pkg.github.com'
   >           scope: '@steven-cutting'
   199a216,220
   >         env:
   >           # On the step that installs, never on the job: a step with no use for
   >           # the credential should not carry one. It is the run's own token,
   >           # minted and discarded with the run, so nothing is stored here.
   >           NODE_AUTH_TOKEN: ${{ github.token }}
   ```

   Against P the diff is additions plus the report step:
   `diff "$P/chromatic.yml" "$W/chromatic.yml" | grep -E '^[0-9]'` prints exactly
   `221a222,239`, `226a245`, `238a258`, `244,245c264,282` and `247c284`; the first
   of those proves P's lines 1-221 are untouched.

4. `template/.github/workflows/pages.yml`: the exact content CONVENTIONS.md §7 gives,
   which is P's file with lines 16-20 (the comment above `env:`) and 22 (`BASE_PATH`)
   rewritten for a project site named by the event, lines 66-67 (the staging step)
   removed, and lines 70-72 (the artifact comment and `path: site`) rewritten to upload
   `build/`. Write this at column 1 (drop this list's indentation; the first line of the
   file is `name: Deploy to GitHub Pages`):

   ```yaml
   name: Deploy to GitHub Pages

   # Publishing needs write scopes that no other workflow here has, so the deploy
   # lives in its own file rather than as a job on the end of CI.

   on:
     push:
       branches: ['main']
     workflow_dispatch:

   permissions:
     contents: read
     pages: write
     id-token: write

   # A project site: Pages serves the build at <owner>.github.io/<repository>/,
   # so the app is built to live under that path. The name is read from the event
   # rather than written here, which is what keeps this file the same in every
   # game and keeps `paths.base` in svelte.config.js from drifting away from the
   # address Pages actually serves.
   env:
     BASE_PATH: /${{ github.event.repository.name }}

   # One deployment at a time, and never cancel one that is already running: a
   # half-published site is worse than a slightly stale one.
   concurrency:
     group: pages
     cancel-in-progress: false

   jobs:
     build:
       runs-on: ubuntu-latest
       timeout-minutes: 15
       # A job block replaces the workflow's rather than adding to it, which is
       # what keeps the two publishing scopes on `deploy` and off the job that
       # installs. This one reads the design system package and needs neither.
       permissions:
         contents: read
         packages: read
       steps:
         - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
           with:
             persist-credentials: false
         - uses: actions/setup-node@820762786026740c76f36085b0efc47a31fe5020 # v7.0.0
           with:
             node-version: '26'
             cache: npm
             cache-dependency-path: package-lock.json
             # @steven-cutting/biscuit-games comes from GitHub Packages, which
             # authenticates every request including a read of a public package.
             # This writes a user-level .npmrc under RUNNER_TEMP naming the
             # registry for the scope and reading the token from the environment
             # of each step that installs; the committed .npmrc names the registry
             # and holds nothing, and the checkout the gates prove clean stays that
             # way.
             registry-url: 'https://npm.pkg.github.com'
             scope: '@steven-cutting'
         - run: npm ci --no-audit
           env:
             # On the step that installs, never on the job: a step with no use for
             # the credential should not carry one. It is the run's own token,
             # minted and discarded with the run, so nothing is stored here.
             NODE_AUTH_TOKEN: ${{ github.token }}
         - name: Build the static site
           run: npm run build
         - uses: actions/upload-pages-artifact@fc324d3547104276b827a68afc52ff2a11cc49c9 # v5.0.0
           with:
             # The build alone. A project site has no domain root to stage around
             # it, and static/.nojekyll rides along so Pages serves _app/.
             path: build

     deploy:
       needs: build
       runs-on: ubuntu-latest
       timeout-minutes: 10
       environment:
         name: github-pages
         url: ${{ steps.deployment.outputs.page_url }}
       steps:
         - id: deployment
           uses: actions/deploy-pages@cd2ce8fcbc39b97be8ca5fce6e763baed58fa128 # v5.0.0
   ```

   The same block sits at the top level of CONVENTIONS.md §7 and can be extracted
   instead of retyped; the two are identical, and CONVENTIONS.md wins if they ever
   differ:

   ```sh
   C=tickets/CONVENTIONS.md
   start=$(grep -n '^\*\*`\.github/workflows/pages\.yml`\*\*' "$C" | cut -d: -f1)
   awk -v s="$start" 'NR>s && /^[`][`][`]yaml$/ && !f {f=1; next} f && /^[`][`][`]$/ {exit} f' "$C" > "$W/pages.yml"
   wc -l "$W/pages.yml"   # 81
   diff "$P/pages.yml" "$W/pages.yml" | grep -E '^[0-9]'   # exactly: 16,20c16,20  22c22  66,67d65  70,72c68,70
   ```

5. `template/.github/copilot-instructions.md`: byte for byte P's, which is byte for
   byte H's and the string at `H/scripts/validate_agents.py` lines 35-40;
   `_check_adapters` (lines 169-176) compares the whole file, so the single final
   newline counts and a trailing blank line fails the gate. Compare first and copy only
   if the placeholder differs:

   ```sh
   cmp /Users/scutting/projects/poodl/.github/copilot-instructions.md template/.github/copilot-instructions.md && echo identical
   # only if cmp reported a difference:
   cp /Users/scutting/projects/poodl/.github/copilot-instructions.md template/.github/copilot-instructions.md
   shasum -a 256 template/.github/copilot-instructions.md
   # 0081da3f90697864970810296453a7e41f5a3ea1067844d96b593131a95973b1
   python3 -c "
   import pathlib, runpy
   m = runpy.run_path('/Users/scutting/projects/biscuit_games/scripts/validate_agents.py')
   print(pathlib.Path('template/.github/copilot-instructions.md').read_text(encoding='utf-8') == m['ADAPTERS']['.github/copilot-instructions.md'])
   "   # True
   ```

   `runpy.run_path` without a `run_name` defines the module and runs nothing: the
   script guards `main()` behind `__name__` and imports only the standard library.

6. Stage and run the gate. prek's `--all-files` reads `git ls-files`, so a new path is
   invisible to it until staged:

   ```sh
   git add template/.github
   just lint
   just test
   just test tests/test_render.py -k "verbatim or pins or poodl" -v
   ```

   The hook's actionlint lints every `run:` script with shellcheck only when a
   `shellcheck` binary is on `PATH`, and prints nothing when there is none. Run
   actionlint once more with shellcheck beside it (the network is needed the first
   time; nothing is installed outside uv's cache):

   ```sh
   uvx --from actionlint-py --with shellcheck-py actionlint -verbose "$W"/*.yml
   ```

   Expected: `Found 0 errors in 3 files` and no line saying `Rule "shellcheck" was
   disabled`. A `Rule "pyflakes" was disabled` line is irrelevant: no step runs Python.

7. `just check` green, then `git status --short` lists only the four files. Set
   `status: done` in `tickets/T03-workflows.md`, fill in the hand-back notes and commit
   on the ticket branch. **Authorisation required:** pushing the branch and opening the
   pull request are separately authorised actions (CONVENTIONS.md §11); stop and ask the
   maintainer.

## Acceptance criteria

- [ ] `template/.github/workflows/ci.yml`, `template/.github/workflows/chromatic.yml`
  and `template/.github/workflows/pages.yml` exist with no `.jinja` suffix; no file
  under `template/.github/` contains `{%` or `{#`, and each workflow still contains
  `${{`.
- [ ] `ci.yml`: `diff` against P reports only `58c58` and `60,61c60,61`, and line 61,
  at the step indentation, reads `- run: just lock-check`.
- [ ] `chromatic.yml`: 286 lines; `diff` against H is exactly the block in step 3;
  `diff` against P reports only `221a222,239`, `226a245`, `238a258`,
  `244,245c264,282` and `247c284`; the publish step carries
  `if: steps.token.outputs.present == 'true'` and the report step's `env` carries
  `PUBLISHED: ${{ steps.token.outputs.present }}`.
- [ ] `pages.yml`: 81 lines; `diff` against P reports only `16,20c16,20`, `22c22`,
  `66,67d65` and `70,72c68,70`; line 22 reads
  `BASE_PATH: /${{ github.event.repository.name }}` under `env:`; no step runs
  `npm run stage`; the artifact `path` is `build`.
- [ ] `copilot-instructions.md`: sha256
  `0081da3f90697864970810296453a7e41f5a3ea1067844d96b593131a95973b1`, and equal to
  the `ADAPTERS` string.
- [ ] A case-insensitive grep for `poodl`, `pnut`, `site-root`, `stage_site` and
  `stage-preview` over `template/.github/` prints nothing.
- [ ] Pins as P's: `node-version: '26'` five times across the three files,
  `version: 0.11.18`, `rust-just==1.51.0`, `npm@11.17.0` and `uv python install 3.14`
  four times each; the six action SHAs are P's (listed under Verification).
- [ ] `just check` green; the `just lint` output shows the `actionlint` hook passing;
  `test_verbatim_files_are_byte_identical`, `test_pins_agree` and
  `test_no_poodl_outside_provenance` pass.
- [ ] Standalone actionlint with shellcheck enabled reports 0 errors over the three
  files.
- [ ] `git diff --name-only main...HEAD` lists exactly the four files in Files touched
  and `tickets/T03-workflows.md`.
- [ ] Hand-back notes filled in, `status: done`, verification output quoted.

## Verification

Run from the repository root. The diff signatures, byte checks and pins:

```sh
P=/Users/scutting/projects/poodl/.github/workflows
H=/Users/scutting/projects/biscuit_games/.github/workflows
W=template/.github/workflows
diff "$P/ci.yml" "$W/ci.yml" | grep -E '^[0-9]'
diff "$P/chromatic.yml" "$W/chromatic.yml" | grep -E '^[0-9]'
diff "$H/chromatic.yml" "$W/chromatic.yml" | grep -E '^[0-9]'
diff "$P/pages.yml" "$W/pages.yml" | grep -E '^[0-9]'
wc -l "$W"/*.yml
```

Expected, in order: `58c58`, `60,61c60,61`; `221a222,239`, `226a245`, `238a258`,
`244,245c264,282`, `247c284`; `3,7c3,5`, `171a170,178`, `187a195,203`, `199a216,220`;
`16,20c16,20`, `22c22`, `66,67d65`, `70,72c68,70`; line counts 286, 167, 81.

```sh
W=template/.github/workflows
cmp /Users/scutting/projects/poodl/.github/copilot-instructions.md template/.github/copilot-instructions.md && echo identical
shasum -a 256 template/.github/copilot-instructions.md
grep -r -n -i -E 'poodl|pnut|site-root|stage_site|stage-preview|\{%|\{#' template/.github; echo "exit $?"
grep -c -E "node-version: '26'|version: 0\.11\.18|rust-just==1\.51\.0|npm@11\.17\.0|uv python install 3\.14" "$W"/*.yml
grep -h -o -E 'uses: [^ ]+' "$W"/*.yml | sort | uniq -c
```

Expected: `identical`; the hash `0081da3f90697864970810296453a7e41f5a3ea1067844d96b593131a95973b1`;
the grep prints nothing and `exit 1`; counts `chromatic.yml:5`, `ci.yml:15`,
`pages.yml:1`; and this SHA list:

```text
   1 uses: actions/cache@0057852bfaa89a56745cba8c7296529d2fc39830
   5 uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
   1 uses: actions/deploy-pages@cd2ce8fcbc39b97be8ca5fce6e763baed58fa128
   5 uses: actions/setup-node@820762786026740c76f36085b0efc47a31fe5020
   1 uses: actions/upload-pages-artifact@fc324d3547104276b827a68afc52ff2a11cc49c9
   4 uses: astral-sh/setup-uv@c771a70e6277c0a99b617c7a806ffedaca235ff9
```

The gate and the tests:

```sh
W=template/.github/workflows
git add template/.github
just lint
just test tests/test_render.py -k "verbatim or pins or poodl" -v
uvx --from actionlint-py --with shellcheck-py actionlint -verbose "$W"/*.yml
just check
git status --short
```

Expected: every hook `Passed`, `actionlint` among them; the three tests `PASSED` (the
`-k` expression selects them by name; `network` and `full` tests are skipped unless
their environment variables are set, which is expected); `Found 0 errors in 3 files`
with no `Rule "shellcheck" was disabled` line; `just check` exits 0; `git status`
shows only `template/.github/workflows/ci.yml`, `template/.github/workflows/chromatic.yml`,
`template/.github/workflows/pages.yml`, and `template/.github/copilot-instructions.md`
only if step 5 copied it.

## Hand-back notes

### What was verified, and how

Both clones were at their pinned commits (`git rev-parse --short=8 HEAD` printed
`0a46a485` and `09b4894a`). Before any edit, `just sync && just test` printed `27 passed`,
and T00's placeholders stood so: `ci.yml` and `chromatic.yml` equal to P's (`diff`
printed nothing), `pages.yml` equal to the block step 4's `awk` extracts from
CONVENTIONS.md §7 (`cmp` printed nothing, and that block is `cmp`-equal to step 4's), and
`copilot-instructions.md` equal to P's. Steps 2 and 3 then wrote `ci.yml` and
`chromatic.yml` with this ticket's commands. Every command below ran on the edited tree;
output is quoted, and each elision is marked with square brackets.

The diff signatures, with `P`, `H` and `W` set as in step 1:

```text
$ diff "$P/ci.yml" "$W/ci.yml"
58c58
<       # No token: a dry run against a complete lockfile reads the registry
---
>       # No token: the dry run against a complete lockfile reads the registry
60,61c60,61
<       # npm's configuration at all.
<       - run: npm ci --ignore-scripts --dry-run --no-audit
---
>       # npm's configuration at all, and `uv lock --check` reads no registry.
>       - run: just lock-check
$ diff "$P/chromatic.yml" "$W/chromatic.yml" | grep -E '^[0-9]'
221a222,239
226a245
238a258
244,245c264,282
247c284
$ diff "$H/chromatic.yml" "$W/chromatic.yml" | grep -E '^[0-9]'
3,7c3,5
171a170,178
187a195,203
199a216,220
$ diff "$P/pages.yml" "$W/pages.yml" | grep -E '^[0-9]'
16,20c16,20
22c22
66,67d65
70,72c68,70
$ wc -l "$W"/*.yml
     286 template/.github/workflows/chromatic.yml
     167 template/.github/workflows/ci.yml
      81 template/.github/workflows/pages.yml
     534 total
```

The whole of `diff "$H/chromatic.yml" "$W/chromatic.yml"` is `cmp`-equal to the block in
step 3 (this file's lines 167-202 with the list indentation dropped). `chromatic.yml`
line 245 is `if: steps.token.outputs.present == 'true'` on the publish step, and line
258 is `PUBLISHED: ${{ steps.token.outputs.present }}` in the report step's `env`.
`pages.yml` lines 21-22 are `env:` and `BASE_PATH: /${{ github.event.repository.name }}`,
line 70 is `path: build`, and no line runs `npm run stage`.

The byte checks, the residue grep and the pins:

```text
$ cmp /Users/scutting/projects/poodl/.github/copilot-instructions.md template/.github/copilot-instructions.md && echo identical
identical
$ shasum -a 256 template/.github/copilot-instructions.md
0081da3f90697864970810296453a7e41f5a3ea1067844d96b593131a95973b1  template/.github/copilot-instructions.md
$ python3 -c "[step 5's runpy comparison against ADAPTERS]"
True
$ grep -r -n -i -E 'poodl|pnut|site-root|stage_site|stage-preview|\{%|\{#' template/.github; echo "exit $?"
exit 1
$ grep -c -E "node-version: '26'|version: 0\.11\.18|rust-just==1\.51\.0|npm@11\.17\.0|uv python install 3\.14" "$W"/*.yml
template/.github/workflows/ci.yml:15
template/.github/workflows/pages.yml:1
template/.github/workflows/chromatic.yml:5
$ grep -h -o -E 'uses: [^ ]+' "$W"/*.yml | sort | uniq -c
   1 uses: actions/cache@0057852bfaa89a56745cba8c7296529d2fc39830
   5 uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1
   1 uses: actions/deploy-pages@cd2ce8fcbc39b97be8ca5fce6e763baed58fa128
   5 uses: actions/setup-node@820762786026740c76f36085b0efc47a31fe5020
   1 uses: actions/upload-pages-artifact@fc324d3547104276b827a68afc52ff2a11cc49c9
   4 uses: astral-sh/setup-uv@c771a70e6277c0a99b617c7a806ffedaca235ff9
```

The adapter is also `cmp`-equal to H's. Counted one pin at a time over the three files,
`node-version: '26'` appears 5 times and `version: 0.11.18`, `rust-just==1.51.0`,
`npm@11.17.0` and `uv python install 3.14` 4 times each. The `uses:` list over P's three
workflows is the same six lines with the same counts. `grep -c -F '${{'` gives
`chromatic.yml` 26, `ci.yml` 6 and `pages.yml` 3, and `find template/.github -name
'*.jinja'` prints nothing.

The gate, after `git add template/.github`:

```text
$ just lint
uv run --frozen prek run --all-files
Ruff lint................................................................Passed
Ruff format check........................................................Passed
check for added large files..............................................Passed
check for case conflicts.................................................Passed
check that executables have shebangs.....................................Passed
check json...............................................................Passed
check for merge conflicts................................................Passed
check that scripts with shebangs are executable..........................Passed
check toml...............................................................Passed
check yaml...............................................................Passed
detect private key.......................................................Passed
EditorConfig.............................................................Passed
markdownlint.............................................................Passed
typos....................................................................Passed
lychee...................................................................Passed
shellcheck...............................................................Passed
Lint GitHub Actions workflow files.......................................Passed
ripsecrets...............................................................Passed
$ just test tests/test_render.py -k "verbatim or pins or poodl" -v
[session header]
collecting ... collected 23 items / 20 deselected / 3 selected

tests/test_render.py::test_verbatim_files_are_byte_identical PASSED      [ 33%]
tests/test_render.py::test_no_poodl_outside_provenance PASSED            [ 66%]
tests/test_render.py::test_pins_agree PASSED                             [100%]
[one DirtyLocalWarning]
================= 3 passed, 20 deselected, 1 warning in 2.27s ==================
$ uvx --from actionlint-py --with shellcheck-py actionlint -verbose "$W"/*.yml
[Linting lines, and "Found 0 parse errors" for each file]
verbose: Rule "pyflakes" was disabled: exec: "pyflakes": executable file not found in $PATH
verbose: Rule "pyflakes" was disabled: exec: "pyflakes": executable file not found in $PATH
verbose: Rule "pyflakes" was disabled: exec: "pyflakes": executable file not found in $PATH
[a "Found total 0 errors" line for each file]
verbose: Found 0 errors in 3 files
$ just check
uv lock --check
Resolved 33 packages in 3ms
uv run --frozen prek run --all-files
[the 18 hook lines above, every one ending Passed]
uv run --frozen mypy
Success: no issues found in 6 source files
uv run --frozen pytest "$@"
[session header]
collected 27 items

tests/test_render.py .......................                             [ 85%]
tests/test_validators.py ....                                            [100%]

[16 DirtyLocalWarning lines]
======================= 27 passed, 16 warnings in 11.41s =======================
$ git status --short
M  template/.github/workflows/chromatic.yml
M  template/.github/workflows/ci.yml
```

`just lint`, the standalone actionlint run and `just check` each exited 0. Filtering
the standalone run's output for `disabled` printed only the three pyflakes lines, so the
shellcheck rule ran. The warnings are copier's `DirtyLocalWarning: Dirty template
changes included automatically.`, raised because the edits were not yet committed.
`git status` was taken before this file was edited.

### Step 5

Step 5 changed nothing. T00's placeholder at `template/.github/copilot-instructions.md`
was already P's file byte for byte, which is H's and the `ADAPTERS` string.

### Deviations, and why

- **Branch.** The work is on `T03-workflows`, the Supacode worktree's branch, as T01's
  was `T01-toolchain-configs`, not on `ticket/t03-workflows`.
- **Two files touched, not four.** T00's `pages.yml` was already the exact §7 content,
  and its `copilot-instructions.md` was already the adapter, so neither was rewritten.
  The criterion that `git diff --name-only main...HEAD` lists the four files in Files
  touched and this ticket cannot hold as written: `git diff --name-only
  origin/main...HEAD` lists `ci.yml`, `chromatic.yml` and this file. Every content
  criterion for the other two holds, as quoted above. Against this worktree's local
  `main`, still at `3db0adb` (T00's merge), the same command also lists T01's seven
  files, because that ref predates `190057d`, the T01 merge this branch starts from.
- **Steps 2 and 3 under zsh with `noclobber`.** Both redirections first refused to
  overwrite their placeholders (`file exists: template/.github/workflows/ci.yml`), so
  nothing was written. They were rerun with `>|` and produced the output above.

### Handed back

- **T00, `.pre-commit-config.yaml`.** On this machine the gate's actionlint hook lints
  without shellcheck, as the probe under Open points settled shows. A `run:` script
  error that standalone actionlint with shellcheck reports passes `just lint`. One fix
  is to give the actionlint hook a `shellcheck` it can find, for example a local hook
  running `uvx --from actionlint-py --with shellcheck-py actionlint`. Whether the
  template repository's CI runner has `shellcheck` on `PATH`, which decides the same
  question for the `fast` job, was not checked.
- **T00, `tests/test_render.py`.** No follow-up: the three tests pass over the final
  files unchanged.
- **T01.** No follow-up: `template/Justfile` lines 30-32 are P's `lock-check` recipe,
  `uv lock --check` then `npm ci --ignore-scripts --dry-run --no-audit`, which is what
  the new `ci.yml` step calls.

### Open points settled

- **Whether the gate's actionlint runs with shellcheck: settled, it does not here.**
  `command -v shellcheck` prints nothing on this machine. prek built the hook's
  actionlint into its own environment (`~/.cache/prek/hooks/golang-*/bin`, which holds
  no `shellcheck`), and shellcheck-py lives in a separate one. In a scratch repository
  holding only the actionlint hook at this repository's `rev`, and one workflow whose
  step is `run: echo $UNQUOTED`:

  ```text
  $ [this repository's .venv/bin/prek] run --all-files
  Lint GitHub Actions workflow files.......................................Passed
  $ actionlint -verbose .github/workflows/probe.yml   # the hook's binary
  [Using project line]
  verbose: Rule "shellcheck" was disabled: exec: "shellcheck": executable file not found in $PATH
  $ uvx --from actionlint-py --with shellcheck-py actionlint .github/workflows/probe.yml
  .github/workflows/probe.yml:7:9: shellcheck reported issue in this script: SC2086:info:1:6: Double quote to prevent globbing and word splitting [shellcheck]
    |
  7 |       - run: echo $UNQUOTED
    |         ^~~~
  ```

  The last command exited 1. Over the three shipped workflows the standalone run, with
  the rule on, reports 0 errors, so nothing is hidden in them today.

- **The correction to CONVENTIONS.md §7.** `wc -l` gives P's `chromatic.yml` 249
  lines, so its report step is lines 232-249, as Context says.
- **CONVENTIONS.md §12, `github.event.repository.name` in a workflow-level `env`: still
  open, for T11.** The only evidence at source is that actionlint accepts the `github`
  context in a workflow-level `env` and reports no error. That shows the expression is
  allowed there, not that the name is populated on `push` and `workflow_dispatch`. T11
  takes the reading this ticket's Open points describe: a green `build` job on the first
  push run and on a manual run, with both run URLs in its hand-back notes.

## Open points

- **CONVENTIONS.md §12: `github.event.repository.name` is populated in a workflow-level
  `env` on both `push` and `workflow_dispatch`.** Known at source: GitHub's
  [webhook payload reference](https://docs.github.com/en/webhooks/webhook-events-and-payloads)
  lists `repository` as a required common payload property "when the event occurs from
  activity in a repository", for `push` and `workflow_dispatch` alike, but it does not
  enumerate the object's fields, so the claim stays open until a run. This ticket
  cannot settle it: nothing is pushed from a lane. T11 settles it on the first push of
  `tic_tac_toe_beans` to `main`, and the reading is unambiguous. SvelteKit refuses a
  `paths.base` that ends with `/` (`@sveltejs/kit` 2.70.2,
  `src/core/config/options.js` lines 176-182 as installed in P's `node_modules`, and
  [the configuration reference](https://svelte.dev/docs/kit/configuration#paths)):
  an unpopulated name makes `BASE_PATH` the single character `/`, and `npm run build`
  then fails in the `build` job with "option must either be the empty string or a
  root-relative path that starts but doesn't end with '/'". Check, for T11: a green
  `build` job on the push run, then a green `build` job on a manual run (Actions, "Deploy
  to GitHub Pages", "Run workflow" on `main`); record both run URLs in T11's hand-back
  notes. The served page at `https://steven-cutting.github.io/tic_tac_toe_beans/` is
  not the reading, because `paths.relative` defaults to `true` and the prerendered HTML
  carries relative asset paths whatever `BASE_PATH` was. If either run fails on that
  message, the fix is a design change through CONVENTIONS.md, not a local edit.
- **Whether the gate's actionlint runs with shellcheck.** The hook installs actionlint
  alone; shellcheck is a separate hook in its own environment, so actionlint's
  shellcheck rule is silently off unless a `shellcheck` binary is on the runner's or the
  developer's `PATH`. Check: the standalone command in step 6 (which guarantees the rule
  runs) against the hook's output. If the hook lints without shellcheck, say so in the
  hand-back notes as a T00 follow-up on `.pre-commit-config.yaml` rather than editing
  that file here.
