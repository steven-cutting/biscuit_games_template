# Conventions for building `biscuit_games_template`

This document is the design every ticket under `tickets/` obeys. A ticket cites it by
section (`CONVENTIONS.md §3`) instead of restating it, and embeds exact content only
where the agent executing the ticket would otherwise have to guess. Where a ticket and
this document disagree, this document wins and the ticket is corrected. Changes to
this document go through a pull request on `main`, never through a lane branch, because
every lane reads it.

## 0. What is being built, and where the sources are

`steven-cutting/biscuit_games_template` (this repository) is a [Copier](https://copier.readthedocs.io/en/stable/)
template. `copier copy` renders a new Biscuit Games game: a static SvelteKit site that
consumes the platform package `@steven-cutting/biscuit-games` from GitHub Packages,
carries Poodl's toolchain, handbook, agent contract and quality gate in generic form, and
passes its own `just check` on the first run. `copier update` later carries toolchain
changes into every rendered game. The template is tested by rendering it and inspecting
the render.

Three repositories are the sources, and this document cites them with a letter and line
numbers that refer to these exact commits:

| Letter | Repository | Local clone | Commit |
| --- | --- | --- | --- |
| **P** | `steven-cutting/poodl`, the first Biscuit Games game | `/Users/scutting/projects/poodl` | `0a46a485` (HEAD on 2026-09-09) |
| **H** | `steven-cutting/biscuit_games`, the hub that publishes the platform package | `/Users/scutting/projects/biscuit_games` | `09b4894a` (HEAD on 2026-09-09; the tag `v1.0.0` sits four commits earlier at `dfebaf4`, and every file this design takes from H is identical at both) |
| **foo/www** | the earlier copier template Poodl was distilled from | `/Users/scutting/projects/foo/www` | `42ed403` |

The first consumer is `steven-cutting/tic_tac_toe_beans`, cloned at
`/Users/scutting/projects/tic_tac_toe_beans`: one commit, a stub `README.md` and nothing
else. It is rendered from the tagged template in ticket T11 as the end-to-end check.

Tooling versions verified on 2026-09-09: uv 0.11.18, just 1.51.0 (`rust-just==1.51.0`),
node 26.5.1 with npm 11.17.0, Python 3.14, copier 9.18.2 (the latest, run through
`uvx`), prek 0.4.12, ruff 0.16.2, `gh` 2.100.0 authenticated as `steven-cutting` with a
token that lacks `read:packages`.

## 1. Decisions taken with the maintainer, and three facts everything rests on

Decisions, taken on 2026-09-08:

1. **Copier, not a GitHub template repository.** A repository template gives no
   substitution and no update path, and must itself be a valid project. `copier update`
   is what makes N games manageable; a rendered tree is what makes the template
   testable. `just new-game` is a two-line wrapper for one-click ergonomics.
2. **Deploy target: a project Pages site.** `pages.yml` builds with
   `BASE_PATH=/<repository name>` read from the workflow event and uploads `build/`. No
   `site-root/`, no staging script. A custom domain is a later per-game change.
3. **Centralisation is recommend-only.** What could be managed centrally is written up as
   the self-contained hand-off tickets C01 to C07, not built here.
4. **`tic_tac_toe_beans` is the first consumer** and the end-to-end verification (T11).
5. **The full handbook ships, centralised through the template.** Toolchain pages are
   managed (template-owned, merged on update); game pages are seed. Pages stay local so
   agents read them offline; edits happen once, in the template. Shipping the hub's own
   pages inside the package is ticket C05.
6. **The template is built by tickets**, executed by AI agents in separate git worktrees
   (§11).
7. **foo/www is the style reference** for `copier.yml`, the taskless copy, the template
   repository's own `Justfile` and `pyproject.toml`, and the harness shape. Its `tests/`
   holds only `__init__.py`, so the harness is written fresh.

Three facts, each verified in source, that shape the mechanism:

1. **Svelte block syntax is Jinja syntax.** `{#` is Jinja's comment opener. Rendered
   with jinja2 3.1.6 under `StrictUndefined` (the `_envops` this template uses):
   `{#snippet brand()}...` and `{#if a}b{/if}` raise `TemplateSyntaxError: Missing end
   of comment tag`; `parameters={{ docs: 1 }}` raises `TemplateSyntaxError`;
   `x=${{ github.token }}` raises `UndefinedError`; `{@render children?.()}` renders
   unchanged. Consequence: **no `.svelte`, `.test.ts`, `.stories.svelte`, workflow
   `.yml` or `.py` file ever carries the `.jinja` suffix.** Answers reach Svelte through
   one rendered TypeScript module, `src/lib/brand.ts.jinja`.
2. **The hub's validators are the stricter, newer ones**, not Poodl's. Against Poodl's,
   the hub's `scripts/validate_docs.py` adds duplicate-key rejection in frontmatter and
   `json.loads(..., object_pairs_hook=_reject_duplicates)`; the hub's
   `scripts/validate_agents.py` adds an exact `BRIDGE_BODY`, duplicate-key rejection and
   an unstripped adapter comparison. Poodl's bridges, `CLAUDE.md` and
   `.github/copilot-instructions.md` already satisfy the hub's constants byte for byte.
   The template ships the hub's validators.
3. **`copier update` merges; it never overwrites.** `_apply_update` (copier
   `_main.py` 1414-1700) renders the old and the new template, diffs the old render
   against the project, applies that diff with `git apply --reject`, and 3-way merges
   the rejects with inline `<<<<<<< before updating` / `>>>>>>> after updating`
   markers. A managed file the game edited keeps its edits unless the same hunk moved.

## 2. Copier facts the mechanism rests on (copier 9.18.2 source, as `uvx copier` caches it)

| Fact | Where |
| --- | --- |
| With `_subdirectory` set, no default exclusions apply; `DEFAULT_EXCLUDE` only when subdirectory is the root. | `_template.py` 47-56, 337-347 |
| `_exclude` patterns are Jinja-rendered with `_copier_operation` (`"copy"`/`"update"`) in scope and split on line breaks; matched on the rendered **destination** path with gitignore syntax. `_copier_operation` is not in the file render context. | `_main.py` 771-786, 447-483, 829, 1025 |
| `as_operation` sets the context only "if not defined already", so old_copy/new_copy/project renders inside `run_update` all run as `update`; `run_recopy` is `copy`. | `_main.py` 106-121, 1261, 1316, 1336 |
| `_skip_if_exists` is consulted before `overwrite` in `_solve_render_conflict`; update's `files_removed` excludes skip paths ("should even be recreated if deleted intentionally"); modified skip files are `--exclude`d from `git apply`. | `_main.py` 492-527, 1439-1454, 1544-1577 |
| `_remove_old_files` deletes paths in old_copy absent from new_copy. | `_main.py` 1693, 1941-1982 |
| Answers file = `_commit`, `_src_path`, then every asked, non-secret answer. `_commit` is `git describe --tags --always`. | `_main.py` 377-397; `_template.py` 649-676 |
| Default ref = latest PEP 440 tag, prereleases skipped; none → warning "No git tags found in template; using HEAD as ref". | `_vcs.py` 166-205 |
| `--trust` is a bare `cli.Flag` (alias `--UNSAFE`); foo/www's `--trust=false` is not valid. Taskless template → never pass it. | `_cli.py` 165-170 |

## 3. `copier.yml` (complete)

```yaml
_min_copier_version: "9.18.2"
_subdirectory: template
_templates_suffix: .jinja
_answers_file: .copier-answers.yml
_envops:
  keep_trailing_newline: true
  undefined: jinja2.StrictUndefined

# With `_subdirectory` set, Copier adds no default exclusions (copier/_template.py,
# `exclude`), so the housekeeping patterns are restated here.
_exclude:
  - .DS_Store
  - Thumbs.db
  - "*.py[co]"
  - __pycache__
  - .pytest_cache
  - .ruff_cache
  # Seed paths: rendered by `copier copy`, never by `copier update`. The current
  # operation reaches this list (copier/_main.py `match_exclude`) and nowhere
  # else, which is what makes a seed copy-only: an update neither merges,
  # recreates nor deletes one. One YAML entry, split on line breaks by Copier.
  # Leading slashes anchor the root files so that docs/README.md and
  # docs/decisions/README.md are matched only where intended.
  # This block and `_skip_if_exists` must stay identical; tests/test_render.py
  # asserts it.
  - |-
    {%- if _copier_operation == 'update' %}
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
    {%- endif %}

# The same list, for `copier recopy` (a copy operation that would otherwise
# overwrite the game's files). Matched before `--overwrite` is consulted. It also
# means a first `copier copy` into a directory already holding one of these files
# keeps that file: delete a stub README.md first.
_skip_if_exists:
  - /README.md
  - /CHANGELOG.md
  - /SECURITY.md
  - /docs/project/purpose-and-scope.md
  - /docs/project/terminology.md
  - /docs/decisions/
  - /docs/specs/
  - /src/lib/brand.ts
  - /src/lib/components/
  - /src/routes/+page.svelte
  - /stories/
  - /tests/restated.ts
  - /tests/lockup.test.ts
  - /tests/route.test.ts

_message_after_copy: |-
  {{ game_name }} is rendered. Nothing ran, no lockfile exists and Git is
  untouched. In order:

    1. Put a GitHub token carrying read:packages in ~/.npmrc as
         //npm.pkg.github.com/:_authToken=<your token>
       {{ hub_package }} is read from GitHub Packages, which refuses an
       anonymous read.
    2. git init -b main                   (skip inside an existing clone)
    3. just initialize                    (lockfiles, npm ci, Chromium, allium, hooks)
    4. just check
    5. Commit everything, .copier-answers.yml and both lockfiles included:
       copier update reads the answers file.

  Before the first push: grant {{ repository }} read access on the
  {{ hub_package }} package (a setting on the package, not on either
  repository) so CI's own token can install it, and set the Pages source to
  GitHub Actions so pages.yml can publish to {{ pages_url }}.

_message_after_update: |-
  Template {{ _copier_answers._commit | default('(untagged)') }} applied. Resolve
  every "<<<<<<< before updating" marker, then run
    just lock && just fix && just check
  and commit the result together with .copier-answers.yml. Seed files were not
  touched; docs/how-to/update-from-template.md lists them.

# ---------------------------------------------------------------- identity ---

# The free-text answers reach Markdown, TOML, JSON and a single-quoted
# TypeScript string, and from there Svelte markup. `{` and `}` cannot be escaped
# out of every one of those at once and are rejected; everything else is escaped
# at the point of use with the `*_escaped` (TOML/JSON) and `*_ts` (TypeScript)
# variants. No `.svelte` file is a Jinja template: the name and the description
# reach the page through `src/lib/brand.ts`.

game_name:
  type: str
  help: The game's display name, as the document title and the README heading spell it.
  placeholder: Tic Tac Toe Beans
  validator: |-
    {% set value = game_name | trim %}
    {% if value | length < 2 or value | length > 40 %}
    Enter between 2 and 40 non-whitespace characters.
    {% elif game_name | regex_search('[\\x00-\\x1f\\x7f]') %}
    Remove the control characters. This is a single-line value, and a raw control
    character is not legal inside the generated TOML and JSON strings.
    {% elif '{' in game_name or '}' in game_name %}
    Remove the braces. They open and close expressions in the generated Svelte
    markup, and no escaping turns them back into ordinary text.
    {% elif not (value | regex_search('[A-Za-z]')) %}
    Include at least one letter: the package name and the specification module
    are named after this value, and both must start with a letter.
    {% endif %}

game_slug:
  type: str
  help: Repository-style identifier; names the npm package, the tooling project and the root specification module.
  default: >-
    {{ game_name | trim | lower | regex_replace('[^a-z0-9]+', '_') | trim('_')
       | regex_replace('^[0-9_]+', '') }}
  validator: >-
    {% if not (game_slug | regex_search('^[a-z][a-z0-9]*(_[a-z0-9]+)*$')) %}
    Use lowercase letters and digits separated by single underscores, starting with a letter.
    {% endif %}

description:
  type: str
  help: One sentence saying what the game is; used in the README, the page metadata and AGENTS.md.
  placeholder: A tic-tac-toe game played with beans.
  validator: |-
    {% set value = description | trim %}
    {% if value | length < 10 or value | length > 200 %}
    Enter between 10 and 200 characters.
    {% elif description | regex_search('[\\x00-\\x1f\\x7f]') %}
    Remove the control characters. This is a single-line value, and a raw control
    character is not legal inside the generated TOML and JSON strings.
    {% elif '{' in description or '}' in description %}
    Remove the braces. They open and close expressions in the generated Svelte
    markup, and no escaping turns them back into ordinary text.
    {% endif %}

repository:
  type: str
  help: GitHub repository as owner/name. Decides the Pages address the handbook states.
  default: "steven-cutting/{{ game_slug }}"
  validator: |-
    {% set parts = repository.split('/') %}
    {% if parts | length != 2 or not (repository | regex_search('^[A-Za-z0-9-]{1,39}/[A-Za-z0-9._-]{1,100}$')) %}
    Enter owner/name: a GitHub account name, one slash, and a repository name of
    letters, digits, dots, hyphens and underscores.
    {% elif parts[0].startswith('-') or parts[0].endswith('-') or '--' in parts[0] %}
    A GitHub account name cannot start or end with a hyphen or contain two in a row.
    {% elif parts[1] in ['.', '..'] or parts[1].endswith('.git') %}
    That repository name is not one GitHub accepts.
    {% endif %}

# ---------------------------------------------------------------- computed ---

repository_owner:
  type: str
  default: "{{ repository.split('/')[0] }}"
  when: false

repository_name:
  type: str
  default: "{{ repository.split('/')[1] }}"
  when: false

# Decision 2 in §1: a project Pages site, built with BASE_PATH=/<repo> and
# served at <owner>.github.io/<repo>/. GitHub lowercases the account in the host.
base_path:
  type: str
  default: "/{{ repository_name }}"
  when: false

repository_url:
  type: str
  default: "https://github.com/{{ repository }}"
  when: false

pages_url:
  type: str
  default: "https://{{ repository_owner | lower }}.github.io{{ base_path }}/"
  when: false

# The words after "biscuit games / " in the lockup, lowercase as the platform's
# own words are. A game that wants otherwise edits src/lib/brand.ts, which is its.
game_lockup:
  type: str
  default: "{{ game_name | trim | lower }}"
  when: false

# For a TOML basic string and a JSON string alike: escape the backslash and the
# double quote. Validators already excluded control characters.
game_name_escaped:
  type: str
  default: >-
    {{ game_name | trim | replace('\\', '\\\\') | replace('"', '\\"') }}
  when: false

# For a single-quoted TypeScript string literal in src/lib/brand.ts, the only
# road an answer takes into Svelte markup.
game_title_ts:
  type: str
  default: >-
    {{ game_name | trim | replace('\\', '\\\\') | replace("'", "\\'") }}
  when: false

game_lockup_ts:
  type: str
  default: >-
    {{ game_lockup | replace('\\', '\\\\') | replace("'", "\\'") }}
  when: false

description_ts:
  type: str
  default: >-
    {{ description | trim | replace('\\', '\\\\') | replace("'", "\\'") }}
  when: false

# The platform. The scope is the hub's, fixed by the package name. The version is
# a template pin: the template is tested against exactly one hub release, and
# moving it is a template release. A game that bumps package.json locally keeps
# the bump through `copier update` (identical same-hunk changes merge silently).
hub_scope:
  type: str
  default: "@steven-cutting"
  when: false

hub_package:
  type: str
  default: "{{ hub_scope }}/biscuit-games"
  when: false

hub_package_version:
  type: str
  default: 1.0.0
  when: false

template_url:
  type: str
  default: https://github.com/steven-cutting/biscuit_games_template
  when: false
```

Decisions folded into this file (§1): four questions and nothing else (`default_branch`, `author_name`, `initial_version` and every tool-version answer dropped; `main`, `0.1.0`, `3.14`, `26`/`26.§2`, `11.17.0`, `0.11.18`, `1.51.0`, `90` stay literal in the files that carry them today, and `tests/test_render.py::test_pins_agree` holds the copies equal). `hub_package_version` is a constant, not a question. Test vocabulary: `DEFAULT_ANSWERS = {"game_name": "Tic Tac Toe Beans", "game_slug": "tic_tac_toe_beans", "description": "A three-in-a-row game played with beans.", "repository": "steven-cutting/tic_tac_toe_beans"}`.

## 4. Template tree (exact paths under `template/`)

Legend: **M** managed (re-rendered on update, game edits merged 3-way); **M†** managed and expected to be edited by the game (layout convention in §5); **S** seed (in both seed lists); `.jinja` only where an answer is substituted; everything else is byte-copied from the named source. "P" = `/Users/scutting/projects/poodl`, "H" = `/Users/scutting/projects/biscuit_games`.

```text
copier.yml                                        (template root, above template/)
template/
├── {{ _copier_conf.answers_file }}.jinja         copier-owned: "# Managed by Copier. Do not edit by hand; run `copier update` instead." + `{{ _copier_answers | to_nice_yaml -}}` (foo/www)
├── .editorconfig                                 M   P verbatim
├── .gitattributes                                M   P minus lines 5-6 (the src/lib/data line and the blank line before it, so the file does not end blank)
├── .gitignore                                    M†  P minus lines 24-27 (site/ and its blank line)
├── .markdownlint-cli2.jsonc                      M   P minus "site"
├── .npmrc                                        M   P verbatim (@steven-cutting:registry=https://npm.pkg.github.com)
├── .pre-commit-config.yaml                       M†  P minus line 10 `src/lib/data/|`
├── .pre-commit-fix.yaml                          M†  P minus line 12 `src/lib/data/|`
├── .prettierignore                               M†  P minus lines 6, 14-16 (the two entries and the blank line after them); PLUS `.copier-answers.yml` (Prettier rewrites YAML it does not own; Copier regenerates the file on every update)
├── .prettierrc.json                              M   P verbatim
├── .python-version                               M   P verbatim (3.14)
├── AGENTS.md.jinja                               M†  diff in §7
├── CLAUDE.md                                     M   P verbatim (`@AGENTS.md\n`, byte-pinned)
├── README.md.jinja                               S   game_name, description, pages_url, base_path; Poodl README shape minus modes/status
├── CHANGELOG.md.jinja                            S   Keep a Changelog skeleton; `[Unreleased]: {{ repository_url }}/commits/main/`
├── SECURITY.md                                   S   P minus the three game-specific out-of-scope bullets (lines 28-32) and the decision link, plus the private-reporting fallback paragraph (T07 §2)
├── chromatic.config.json                         M   P verbatim (autoAcceptChanges "main")
├── eslint.config.js                              M†  H's minus `'dist/'` in ignores (Poodl's two vocabulary rules dropped)
├── lychee.toml                                   M†  P minus "site"
├── package.json.jinja                            M†  `"name": "{{ game_slug }}"`; drop the `stage` script (P line 20); everything else P verbatim
├── pyproject.toml.jinja                          M†  name `{{ game_slug }}-tooling`, description with `{{ game_name_escaped }}`; drop `"src/lib/data/"` and its comment from typos extend-exclude; line 15 "Poodl ships no Python package." → "This game ships no Python package."; line 17 cites the template's `docs/decisions/0004-python-toolchain.md`
├── svelte.config.js                              M   comment lines 4-15 rewritten ("a project site under BASE_PATH, set by pages.yml from the repository name; empty locally"); code unchanged
├── tsconfig.json                                 M   P verbatim
├── vite.config.ts                                M   P verbatim (thresholds 90)
├── vitest.config.ts                              M   P verbatim
├── vitest.storybook.config.ts                    M   P verbatim (keep optimizeDeps.include)
├── Justfile                                      M†  P minus lines 68-80 (`stage`, `stage-preview`, their comments and the blank line after them)
├── .claude/settings.json                         M   P verbatim (tolerated by the validator)
├── .claude/skills/<8>/SKILL.md                   M   P verbatim (word-list-change dropped)
├── .codex/skills/<8>/SKILL.md                    M   P verbatim
├── .agents/skills/{code-review,fix-quality,plan-change,project-check}/SKILL.md      M   P verbatim
├── .agents/skills/{review-docs,spec-change,svelte-change,accessibility-review}/SKILL.md  M   edits in §7, no answers
├── .github/copilot-instructions.md               M   P verbatim (byte-pinned by the hub validator; verified equal)
├── .github/workflows/ci.yml                      M   P with lines 58-61 replaced by `- run: just lock-check` (§7)
├── .github/workflows/chromatic.yml               M   P + hub token guard (§7)
├── .github/workflows/pages.yml                   M   exact content in §7
├── .storybook/main.ts                            M   prose only: lines 38-40, 44-45 "Poodl" → "this game"; refs block kept
├── .storybook/preview.ts                         M   line 46 `'poodl-simulated-reduced-motion'` → `'game-simulated-reduced-motion'`; prose at 13-17, 73-76 generic
├── scripts/check_playwright_browsers.js          M   P verbatim
├── scripts/initialize.sh                         M   H's (Linux sudo notice, worktree-aware install-hooks); committed 100755
├── scripts/install_allium.py                     M   H's (adds only the comment at 29-35)
├── scripts/run_allium.py                         M   P verbatim (identical to H)
├── scripts/run_project_check.py                  M   P's (no package recipes)
├── scripts/run_ripsecrets_redacted.py            M   P verbatim (identical to H)
├── scripts/validate_docs.py                      M   H's; comment lines 26-29 → "This game is generated from the Biscuit Games template and has no feature toggles, ..."
├── scripts/validate_agents.py                    M   H's verbatim
├── static/.nojekyll                              M   empty (0 bytes)
├── src/app.html                                  M   P with comment lines 2-7 replaced (§7)
├── src/app.d.ts                                  M   P verbatim
├── src/routes/+layout.svelte                     M   line 7 "Poodl's own styles" → "the game's own styles"
├── src/routes/+layout.ts                         M   line 1 "Poodl is served" → "The game is served"
├── src/routes/+page.svelte                       S   exact in §7; never .jinja
├── src/lib/brand.ts.jinja                        S   exact in §7 (the one place the name is written)
├── src/lib/config.ts                             M†  six platform figures, exact in §7; a game appends its own figures below
├── src/lib/ports/storage.ts                      M   P verbatim
├── src/lib/ports/clock.ts                        M   P, comment lines 4-7 (§7)
├── src/lib/ports/random.ts                       M   P, comment lines 2-8 (§7)
├── src/lib/components/Lockup.svelte              S   exact in §7
├── stories/Lockup.stories.svelte                 S   exact in §7
├── tests/setup.ts                                M   P verbatim (one line)
├── tests/platform.ts                             M   P + `Restatement` interface, comment self-contained (§7)
├── tests/platformSpecs.test.ts                   M   adapted, exact in §7
├── tests/ports.test.ts                           M†  P lines 1-204 minus clipboard/preferences/timer (§7)
├── tests/restated.ts                             S   exact in §7
├── tests/lockup.test.ts                          S   exact in §7
├── tests/route.test.ts                           S   exact in §7
├── docs/manifest.yml                             M†  layout in §8
├── docs/README.md.jinja                          M†  layout in §8
├── docs/project/purpose-and-scope.md.jinja       S
├── docs/project/terminology.md.jinja             S
├── docs/project/{repository-map,platform}.md     M
├── docs/tutorials/first-change.md                M
├── docs/how-to/{develop-locally,test-and-debug,work-in-the-component-workshop,work-with-the-specs,maintain-dependencies}.md   M
├── docs/how-to/deploy-to-github-pages.md.jinja   M   pages_url, base_path, repository
├── docs/how-to/update-from-template.md.jinja     M   _copier_answers._commit, template_url
├── docs/explanation/{architecture,layering,specifications,accessibility,security-model,quality-philosophy}.md   M
├── docs/reference/{commands,configuration,testing,quality-gates,documentation-contract,agent-contract}.md       M
├── docs/operations/{maintenance,troubleshooting}.md   M
├── docs/decisions/README.md.jinja                S   game_name once
├── docs/decisions/0001..0009-*.md                S   verbatim after generic edits (§8)
├── docs/decisions/0010-a-project-pages-site.md.jinja   S   pages_url
└── docs/specs/{{ game_slug }}.allium.jinja       S   exact in §7; game_name once, inside a comment
```

Not shipped: `site-root/`, `scripts/stage_site.sh`, `src/lib/data/`, `src/lib/app/`, `src/lib/domain/`, `src/lib/ports/{clipboard,timer,words}.ts`, `static/word-lists-NOTICE.txt`, `stories/fixtures.ts`, `tests/engineHarness.ts`, every Poodl component/story/test not named above, decisions 0005/0007/0009/0010/0012/0013, `how-to/replace-the-word-lists.md`, skill `word-list-change`, lockfiles.

Rule for managed pages and files: say "this game"/"the game", not the name; only `AGENTS.md`, `docs/README.md`, the seeds and the two URL-bearing pages carry an answer. Fewer `.jinja` files, fewer merge points on a rename.

## 5. Managed versus seed

- **Seed** = the 14 patterns above. Excluded on `update` (never merged, recreated or deleted; a seed the game deleted stays deleted), skipped on `recopy` and on a `copy` into a directory that already holds it. Seeds are exactly the template-rendered files a game rewrites wholesale.
- **Managed** = everything else the template renders. On update: template-changed, game-untouched → new render; game-changed, template-untouched → game's version kept (the hunk re-applies); both changed, different hunks → clean 3-way; same hunk → inline markers; identical change on both sides → silent. A managed file the game deleted stays deleted. A managed file the template stops rendering is removed from the game even if edited: every such removal is announced in the template `CHANGELOG.md` under "Update notes".
- **Game-added files** (new components, tests, stories, pages, spec modules) are never in old_copy or new_copy and are untouched. Same path as a seed edit: the old→project diff is a creation patch that `git apply` refuses because the file exists. `tests/test_update.py` proves both.
- **Frozen seed inventory.** `docs/manifest.yml` and `docs/README.md` re-render on every update while seeds never do, so after `v0.1.0` the template may never add, rename or retitle a seed page or a numbered decision. Anything it later wants to hand to games is a managed page; template decisions are recorded in the template's own CHANGELOG. Stated in the template README, `docs/how-to/update-from-template.md` and `tickets/CONVENTIONS.md`.
- **Managed files the game is expected to edit** (`M†`) and the layout convention that keeps template and game edits in different hunks:
  - `docs/manifest.yml`: managed entries first, grouped by kind exactly as Poodl's; then a final block holding the seed entries (`project/purpose-and-scope.md`, `project/terminology.md`, `decisions/README.md`, `decisions/0001…0010`); game-added entries go **after the last decision**. The first entry a game appends also adds a comma to the previous last line; that line is a frozen seed entry, so the edit never conflicts. Do not reorder: page order is irrelevant to the validator and the position is the whole convention. The template inserts new managed entries inside the upper blocks only.
  - `docs/README.md`: Poodl's sections in Poodl's order, then `## Decisions`, then a final `## This game` section the game extends.
  - `AGENTS.md`: the game adds to the "Deliberate deviations" list at the end of Provenance and to the invariants only through the template.
  - `Justfile`, `package.json`, `eslint.config.js`, `.gitignore`, `.prettierignore`, `lychee.toml`, the two prek configs, `pyproject.toml`, `src/lib/config.ts`, `tests/ports.test.ts`: append at the end of the relevant block; the template inserts, the game appends.
- `.copier-answers.yml`: always rewritten by update, excluded from the diff, committed. The one sanctioned hand edit is `_src_path` when moving from a local render to the GitHub URL.

## 6. Jinja rules

1. `.jinja` only where an answer or `_copier_*` value is substituted; every other file is byte-copied. The residue test (§9) enforces both halves: a file whose source lacks `.jinja` must be byte-identical to its source; a file rendered from `.jinja` must contain none of `{{`, `{%`, `{#`.
2. No `.svelte`, `.test.ts`, `.stories.svelte`, `.yml` workflow or `.py` file is `.jinja`. Workflows keep their `${{ }}` because they are verbatim; `pages.yml` reads the repository name from the event.
3. Only `.jinja` files may reference answers, and only the names in §3 plus `_copier_answers._commit` (guarded with `default`) and `_copier_conf.answers_file`; `StrictUndefined` fails anything else.
4. Markdown pages, `AGENTS.md`, skills and adapters must contain no delimiter after rendering: `validate_docs.py` `BAD_CONTENT["unresolved template syntax"]` and `validate_agents.py` `UNRESOLVED` forbid them, so `docs/how-to/update-from-template.md.jinja` describes Jinja and `.copier-answers.yml` without writing a delimiter.
5. Path names: `docs/specs/{{ game_slug }}.allium.jinja`; `game_slug` is `[a-z0-9_]`, Allium modules use no `import` (grep of all nine modules), and the hub ships `play-surfaces.allium`, so any legal slug is a legal filename.
6. `.allium` files use `--` comments and `{ }` blocks with no `{{`/`{%`/`{#` (grep over Poodl's six and the hub's three).

## 7. Seed and managed source content (exact)

### `src/lib/brand.ts.jinja` (seed)

```ts
/**
 * What this game is called, wherever the platform asks for a name.
 *
 * `GAME_NAME` is the words the lockup shows after the platform's own:
 * `Wordmark`'s `product` prop renders "biscuit games / <GAME_NAME>", and the
 * page's only `h1` reads exactly that. `GAME_TITLE` is the document title and
 * `GAME_DESCRIPTION` its description.
 *
 * A file of its own rather than lines in `config.ts`, because `config.ts`
 * holds only figures a specification also states, and because this is the
 * one place the name is written: every component, story and test reads it
 * from here. This file is the game's; a template update never touches it.
 */
export const GAME_NAME = '{{ game_lockup_ts }}';
export const GAME_TITLE = '{{ game_title_ts }}';
export const GAME_DESCRIPTION = '{{ description_ts }}';
```

### `src/lib/config.ts` (managed, no Jinja)

Poodl's `src/lib/config.ts` lines 1-7 and 44-99 with lines 9-42 and 101-130 deleted and every `game.allium` reference rewritten to the game's root module:

```ts
/**
 * Values the specifications declare in their `config` blocks.
 *
 * These are the only numbers in the implementation that a specification also
 * states, so they live in one place and are named after the spec parameter
 * they mirror. Changing one here without changing it in `docs/specs/` is drift.
 *
 * All six are the platform's, stated in the modules
 * `@steven-cutting/biscuit-games` ships and restated by name in this game's
 * root module. `tests/platformSpecs.test.ts` holds this file, that module and
 * the shipped text equal. A figure this game alone states — an attempt count,
 * a board size — belongs below these, mirrored from the module that states it.
 */

/**
 * `appearance.allium` — `config.minimum_text_contrast` and
 * `config.minimum_boundary_contrast`, as WCAG 2.2 computes a ratio.
 *
 * The two AA bars: text against what is behind it, and anything that is not
 * text — a control's boundary, a state indicator — against what is adjacent
 * to it.
 */
export const MINIMUM_TEXT_CONTRAST = 4.5;
export const MINIMUM_BOUNDARY_CONTRAST = 3.0;

/**
 * `operation.allium` — `config.minimum_touch_target`, in CSS pixels.
 *
 * Across a control, in both directions, for
 * `DirectManipulation.EveryControlIsAComfortableTarget`. That invariant names
 * the two shapes it cannot be met in and says what each owes instead, rather
 * than stating a size alone.
 */
export const MINIMUM_TOUCH_TARGET = 44;

/**
 * `operation.allium` — `config.narrowest_supported_width`, in CSS pixels.
 *
 * The narrowest viewport the game is playable on without scrolling sideways,
 * which is the width every target and spacing figure has to survive.
 */
export const NARROWEST_SUPPORTED_WIDTH = 320;

/**
 * `play-surfaces.allium` — `config.minimum_state_separation`.
 *
 * How far a cell nothing is known about sits from one that has been marked.
 * No standard supplies this figure, because standards ask a colour to stand
 * off its background rather than off another state, and marks sit side by side.
 */
export const MINIMUM_STATE_SEPARATION = 3.0;

/**
 * `play-surfaces.allium` — `config.minimum_mark_separation`.
 *
 * How far absent sits from exact, and that pair only. Lower than the figure
 * above deliberately: four states 3 to one apart would need a range of 27 to
 * one, which no palette has. The specification's own reasoning for the gap is
 * worth reading before either number is touched.
 */
export const MINIMUM_MARK_SEPARATION = 2.0;
```

### `src/lib/components/Lockup.svelte` (seed)

```svelte
<script lang="ts">
  import { Wordmark } from '@steven-cutting/biscuit-games';

  import { GAME_NAME } from '$lib/brand';

  /**
   * This game's lockup: the platform's words, and then its own.
   *
   * The platform's `Wordmark` draws it, given a `product`, so the display face,
   * the weight, the tracking and the `words` class `HeaderBar` reaches into
   * to collapse the words below about 26rem are all the platform's. The route
   * hands this to `HeaderBar` as its `brand` snippet, and the page's only `h1`
   * reads "biscuit games / <GAME_NAME>".
   *
   * No markup of its own and no `{#if}`: a component with a branch nothing
   * renders is a branch the coverage floor counts against the whole tree.
   */
</script>

<Wordmark product={GAME_NAME} />
```

Grounding: `H/src/lib/components/Wordmark.svelte:23,31,36` (`product` prop, `class="words"`), `Monogram.svelte:50-58` (text "b", `aria-hidden` when unlabelled), `HeaderBar.svelte:45-47` (`<h1 class="brand">{@render brand()}`), `:171` (`.brand :global(.words)`). No `<style>`, so nothing for `svelte-check --fail-on-warnings`.

### `src/routes/+page.svelte` (seed)

```svelte
<script lang="ts">
  import { HeaderBar } from '@steven-cutting/biscuit-games';

  import { GAME_DESCRIPTION, GAME_TITLE } from '$lib/brand';
  import Lockup from '$lib/components/Lockup.svelte';

  /*
   * The whole application, assembled. Today that is the platform's chrome
   * carrying this game's lockup and a main landmark with nothing in it yet.
   *
   * Everything that differs per visitor — a stored game, the device
   * preferences, a token in the address bar — belongs after hydration, inside
   * `onMount`: `+layout.ts` prerenders every route, so module-scope work here
   * runs once in Node at build time. The three ports under `src/lib/ports/`
   * are built there when the game has a store to hand them to.
   *
   * Every selector below names an element or a class this markup carries,
   * because `svelte-check --fail-on-warnings` turns an unused selector into a
   * failed gate.
   */
</script>

<svelte:head>
  <title>{GAME_TITLE}</title>
  <meta name="description" content={GAME_DESCRIPTION} />
</svelte:head>

<div class="shell">
  <HeaderBar>
    {#snippet brand()}
      <Lockup />
    {/snippet}
  </HeaderBar>

  <main>
    <p>Nothing to play yet. The board goes here.</p>
  </main>
</div>

<style>
  .shell {
    max-inline-size: var(--shell-max);
    margin-inline: auto;
    padding: 0 var(--shell-pad) var(--s-11);
  }

  main {
    padding-block-start: var(--s-6);
  }

  p {
    margin-block: 2rem;
    color: var(--text-2);
    text-align: center;
  }
</style>
```

Tokens exist in `H/src/app.css` (`--shell-max` :276, `--shell-pad` :268, `--s-6` :257, `--s-11` :262, `--text-2` :169). Shape from `P/src/routes/+page.svelte:294-327,547-563`. `src/routes/` is outside the coverage glob.

### `tests/platform.ts` (managed)

Poodl's file with (a) the comment's reference to `directManipulation.test.ts` (lines 12-13) made self-contained: "under Vitest's SSR transform `import.meta.url` is a served path rooted at `/`", and "Poodl actually installs" → "this game actually installs"; (b) after `platformFile`, add:

```ts
/** The three modules the package ships under `specs/`. */
export type PlatformModule = 'appearance.allium' | 'operation.allium' | 'play-surfaces.allium';

/**
 * A run of clauses this game restates from one platform module, word for word.
 *
 * `alias` is the `use` alias `file` reaches its config through when it reaches
 * another module's rather than its own — Poodl's `settings.allium` wrote
 * `game/config.` where the platform wrote `config.` — or null when no
 * normalisation is needed. `tests/restated.ts` holds the game's table.
 */
export interface Restatement {
  module: PlatformModule;
  theirs: string;
  file: string;
  ours: string;
  alias: string | null;
  clauses: readonly string[];
}
```

### `tests/platformSpecs.test.ts` (managed)

Poodl's `flatten`, `clauses`, `figures` (lines 37-100) unchanged. Changes: the header comment says "this game" and ends "Which clauses are restated is the game's to say, in `tests/restated.ts`. A fresh game restates none, and this file still holds the figures."; `RESTATED` is imported from `./restated`; `poodlModule` becomes `gameModules()`/`gameModule(name)` over `docs/specs/*.allium`; the six constants are imported from `../src/lib/config` (which is what covers that file); `prefixed`/`replaceAll('game/config.', ...)` becomes `alias`:

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

// ... flatten, clauses, figures: Poodl lines 37-100 verbatim ...

const SPECS = resolve(process.cwd(), 'docs', 'specs');

/** Every module this game keeps, which is what `just check-specs` reads. */
function gameModules(): string[] {
  return readdirSync(SPECS).filter((name) => name.endsWith('.allium')).sort();
}

function gameModule(name: string): string {
  return readFileSync(resolve(SPECS, name), 'utf8');
}

/** Which platform module states each figure, and what `config.ts` mirrors it as. */
const FIGURES = [
  { figure: 'minimum_text_contrast', module: 'appearance.allium', mirrored: MINIMUM_TEXT_CONTRAST },
  { figure: 'minimum_boundary_contrast', module: 'appearance.allium', mirrored: MINIMUM_BOUNDARY_CONTRAST },
  { figure: 'minimum_touch_target', module: 'operation.allium', mirrored: MINIMUM_TOUCH_TARGET },
  { figure: 'narrowest_supported_width', module: 'operation.allium', mirrored: NARROWEST_SUPPORTED_WIDTH },
  { figure: 'minimum_state_separation', module: 'play-surfaces.allium', mirrored: MINIMUM_STATE_SEPARATION },
  { figure: 'minimum_mark_separation', module: 'play-surfaces.allium', mirrored: MINIMUM_MARK_SEPARATION }
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

  it('reads the version package.json pins', () => {
    // Poodl lines 187-194 verbatim
  });
});
```

`it.each([])` registers nothing and does not throw (`P/node_modules/@vitest/runner/dist/chunk-artifact.js:2018-2021`, `cases.every` then `cases.forEach`). `RESTATED` must be typed `readonly Restatement[]`, not `[] as const`, or `.flatMap` on `never` is a TypeScript error.

### `tests/restated.ts` (seed)

```ts
import type { Restatement } from './platform';

/*
 * What this game restates from the platform's specifications, and where.
 *
 * Empty until the game restates a clause. When a module under docs/specs/
 * copies a platform `@guarantee` or `@invariant` word for word — a contract it
 * fulfils, a surface it inherits — the copy is listed here, and
 * `tests/platformSpecs.test.ts` holds it equal to the text the package ships.
 * Poodl's table is the worked example: its `game.allium` restates
 * `operation.allium`'s `DirectManipulation` under the same name with no alias,
 * and its `settings.allium` restates `appearance.allium`'s `Appearance` through
 * the alias `game`.
 */
export const RESTATED: readonly Restatement[] = [];
```

### `tests/ports.test.ts` (managed)

`P/tests/ports.test.ts` lines 1-204 with imports at lines 4, 6, 7, 9 removed; every `'poodl:...'` key spelt `'game:...'`; lines 206-493 (clipboard, preferences, timer describes) removed; one case added inside `describe('storage port')` after line 136:

```ts
  it('starts empty when given nothing', () => {
    const storage = createFakeStorage();

    expect(storage.read('game:settings')).toBeNull();
  });
```

Needed for coverage: `createFakeStorage`'s default argument (`storage.ts:68`) is a branch Poodl covers from `engineHarness.ts`, which is not shipped. Branch sites in the three ports: storage 8 (:25, :41, :45×2, :52, :59, :68, :71), random 4 (:27, :40, :60, :61), clock 2 (:14, :24); every path is taken by Poodl's cases plus this one.

### `tests/lockup.test.ts` and `tests/route.test.ts` (seed)

```ts
// tests/lockup.test.ts
import { render, screen } from '@testing-library/svelte';
import { describe, expect, it } from 'vitest';

import { GAME_NAME } from '../src/lib/brand';
import Lockup from '../src/lib/components/Lockup.svelte';

describe('Lockup', () => {
  // Two assertions because neither holds the claim alone: a text query matches
  // an element's own text nodes, so the words are found whether or not the
  // mark beside them is hidden. The mark is held silent on its own.
  it('names this game after the platform, with the mark silent', () => {
    render(Lockup, {});

    expect(screen.getByText('b')).toHaveAttribute('aria-hidden', 'true');
    expect(screen.getByText(/biscuit/).textContent).toBe(`biscuit games / ${GAME_NAME}`);
  });
});
```

```ts
// tests/route.test.ts
import { render, screen } from '@testing-library/svelte';
import { describe, expect, it } from 'vitest';

import { GAME_NAME, GAME_TITLE } from '../src/lib/brand';
import Page from '../src/routes/+page.svelte';

describe('the page', () => {
  it('carries the heading the platform header draws for this game', () => {
    render(Page);

    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent(
      `biscuit games / ${GAME_NAME}`
    );
  });

  it('titles the document after the game', () => {
    render(Page);

    expect(document.title).toBe(GAME_TITLE);
  });

  it('has a main landmark to put the game in', () => {
    render(Page);

    expect(screen.getByRole('main')).toBeInTheDocument();
  });
});
```

The heading assertion is Poodl's `route.test.ts:62-66`; the "b" query is the hub's own `tests/brand.test.ts:76`. The `document.title` case is unverified (jsdom + Svelte 5 `<svelte:head>`); drop it rather than weaken the heading case if it proves flaky.

### `stories/Lockup.stories.svelte` (seed)

`P/stories/Lockup.stories.svelte` with: imports gain `GAME_NAME` from `../src/lib/brand`; `` FRAME_WIDTH = `${String(NARROWEST_SUPPORTED_WIDTH)}px` `` and `` LOCKUP = `biscuit games / ${GAME_NAME}` `` constants (numbers through `String()` because the hub's ESLint config has no `allowNumber`, cf. `H/stories/HeaderBar.stories.svelte:11`); the `chip` constant dropped and `actions` reduced to one `settings` entry (so `getAllByRole('button')` has something to measure); `OVERVIEW` rewritten to describe `Wordmark`'s `product` prop; the first play asserts `getByText('b')` is `aria-hidden` and `getByText(/biscuit/).textContent` equals `LOCKUP`; the narrow story's heading query uses `name: LOCKUP` and the template's `style` uses `{FRAME_WIDTH}`; `<HeaderBar actions={ACTIONS}>` (no chip); the dark-theme story unchanged. Stories are never measured for coverage (`P/vitest.storybook.config.ts`).

### `docs/specs/{{ game_slug }}.allium.jinja` (seed) — **parsing unverified**

Modelled on `H/docs/specs/operation.allium` (`given` :68-85, `config` :91-108, surface :211-252). The figure lines must match `figures()`'s regex (`name: Integer = 44` / `name: Decimal = 4.5`). Only `game_name` is substituted, inside a comment line.

```text
-- allium: 3
--
-- {{ game_name | trim }} — the game
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

Unproven until T06 runs `just install-allium && just check-specs && just analyse-specs` in a render: (a) bare `Play` as a surface identifier (the platform uses `PlaySurface`, `PlayCell`, `PlayMark`); (b) a surface with no `contracts:` block; (c) figures referenced only inside `--` bodies not tripping `allium.field.unused` (the hub's `appearance.allium:97-98,162-166` does exactly this and its gate passes, so (c) is the least doubtful). Neither tree has a runnable copy here that read-only mode allows exercising against a new module (`H/.tools/bin/allium` exists; `P/.tools/` does not).

### Managed adaptations against Poodl files

**`AGENTS.md.jinja`** (against `P/AGENTS.md`; the six required phrases and 300+ words survive):

- Lines 10-12: `Poodl is an unlimited-play, Wordle-style word guessing game: a single-page static web app with no backend, no accounts and no server, deployed to GitHub Pages.` → ``{{ game_name }} is a Biscuit Games game: {{ description | trim | trim('.') }}. It is a single-page static web app with no backend, no accounts and no server, built on the platform package `{{ hub_package }}` and deployed to GitHub Pages at <{{ pages_url }}>.``
- Invariant 3 (lines 36-41): `Storage, randomness, the clock, the clipboard, the word lists and the repeating timer are reached through` → ``Storage, randomness and the clock are reached through `src/lib/ports/`, each with an in-memory fake, and every side effect this game adds gets a port there in the same shape; the device's preferences and its keyboard are reached through the two ports `@steven-cutting/biscuit-games` exports, with the fakes it ships.``
- Invariant 6: `Every letter result and key state has a non-colour indication` → `Every state a surface shows has a non-colour indication`.
- Stack bullet (68-71): `the cells and keys of the play surface` → `the play-surface cells and keys`; `What a second game would render unchanged` → `What another game would render unchanged`.
- `## Provenance` (145-189) replaced whole:

```markdown
## Provenance

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

**Skills** (`.agents/skills/*/SKILL.md`; bridges unchanged because frontmatter is unchanged):

- `review-docs`: insert a new step 3, renumber 3-7 → 4-8: ``3. Say which side of the template the page is on. A managed page is changed in `biscuit_games_template` and arrives by `copier update`; editing it here is a stopgap the next update will merge. A seed page is this game's and no update touches it. `docs/how-to/update-from-template.md` lists both.``
- `spec-change` step 1: ``Identify which module owns the behaviour: `words`, `game`, `settings`, `statistics`, `sharing` or `daily`.`` → ``Identify which module under `docs/specs/` owns the behaviour; each module's header states its Scope, Includes and Excludes, and a clause the platform states is owned by `@steven-cutting/biscuit-games` and only restated here.`` Step 4: `` `game.allium` is depended on by the other four, so a change to a trigger or an entity ripples. `` → ``A module others import is depended on by each of them, so a change to a trigger or an entity ripples, and a restated platform clause is held to the platform's text by `tests/platformSpecs.test.ts`.``
- `svelte-change` step 2: ``Never reach for `localStorage`, `crypto`, `Date`, or `navigator.clipboard` outside a port adapter.`` → ``Never reach for `localStorage`, `crypto`, `Date` or any other browser global outside a port adapter.`` Step 4: `a non-colour indication for every letter result and key state.` → `a non-colour indication for every state a surface shows.`
- `accessibility-review` step 2 → ``Check the colour obligation. Every state the surface distinguishes by colour also carries a non-colour indication and an accessible description, in the words the surface's `@guarantee` clauses use, so it is readable without colour vision.``; step 4 → ``Check what is announced. Every outcome the surface's `@guarantee` clauses say is announced reaches assistive technology through the platform's `Announcer`, carrying the detail the clause names.``; step 5 → `Check what is not exposed. Whatever a surface's specification withholds from the player stays out of the DOM as well, attributes included.`
- `word-list-change` and its two bridges: dropped. `project-check`'s gate numbers 2/10/11 match the unchanged `RECIPES` tuple.

**`.github/workflows/ci.yml`**: `P` verbatim except lines 58-61:

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

**`.github/workflows/chromatic.yml`**: `P` (its `permissions` block with `packages: read` at 174-178, `registry-url`/`scope` at 202-203, `NODE_AUTH_TOKEN` at 216-220 all kept) plus the hub's guard: insert after line 220 the hub's "Note whether a Chromatic token is configured" step (`H:201-217` verbatim); add `if: steps.token.outputs.present == 'true'` to the publish step (P 226); replace the report step's env and script (P 232-249) with the hub's (`H:230-265`, i.e. add `PUBLISHED: ${{ steps.token.outputs.present }}` and the three-way `case`). Header comment lines 3-5 stay Poodl's (a game does deploy Pages). No game name anywhere.

**`.github/workflows/pages.yml`** (exact; from `P` with lines 16-22 rewritten, 66-67 removed, 68-72 → `build`):

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

**`Justfile`**: `P` minus lines 68-80. Every other recipe byte-identical (`initialize` through `chromatic`).

**`src/app.html`**: comment lines 2-7 → ``data-theme="dark" is `default AppearanceSettings appearance_settings` from the platform's appearance.allium, which @steven-cutting/biscuit-games ships, stated in the markup so the prerendered page paints the default before anything hydrates. A route that lets the player choose writes their choice over it: `light` replaces it, `system` removes it.``

**`src/lib/ports/clock.ts`** lines 4-7 → ``A specification reads `now` when something starts and when it ends. A test that has to wait real seconds to watch a countdown expire is not a test worth having, so time arrives through a port.`` **`random.ts`** line 2 `Drawing an answer.` → `Drawing one candidate from many.`; lines 4-8 → ``A specification that calls `uniform_choice` says the same thing about it every time: what matters is that every candidate is equally likely, not that the same input yields the same value. That makes it the one deliberately non-deterministic step, and therefore the one that has to sit behind a port.``

## 8. Handbook: every page the render ships (38)

Class **M** managed, **M†** managed and game-edited, **S** seed. Tier **A** ships in v0.1.0; **B** cheap to carry, first to cut if T07/T08 run long. Source is Poodl's page of the same path unless stated.

| # | Rendered path | Class | Tier | Rewrite |
| --- | --- | --- | --- | --- |
| 1 | `docs/README.md` (.jinja) | M† | A | Layout below; `{{ game_name }}` once, `{{ game_slug }}.allium` once. |
| 2 | `docs/project/purpose-and-scope.md` (.jinja) | S | A | From `description`: What it does / What it does not do / Who it is for; 40+ real words, no TODO/TBD/"insert here". |
| 3 | `docs/project/repository-map.md` | M | A | Drop `app/`, `data/`, `site-root/`, `stage_site.sh`, `pnut.fans`; scripts list = the eight shipped. |
| 4 | `docs/project/platform.md` | M | A | "Poodl" → "this game"; "What is Poodl's" generic; version stated as "the version `package.json` pins" (P line 34 states a literal 1.0.0, which would drift the moment a game bumps); restated-clauses paragraph names the six figures; 13-row outbound table kept (whole-page `https://` links; two carry "poodl" in the URL, hence the allowlist). |
| 5 | `docs/project/terminology.md` (.jinja) | S | B | Keep "The repository" section (P lines 43-56); game section a two-row table. |
| 6 | `docs/tutorials/first-change.md` | M | A | Steps 3-5 around the seed module, seed test and seed component; BASE_PATH line dropped. |
| 7 | `docs/how-to/develop-locally.md` | M | A | `<your token>` kept (ripsecrets, P 33-40); drop `stage` blocks; `BASE_PATH=/<repository name>`. |
| 8 | `docs/how-to/test-and-debug.md` | M | B | Only P 59-60 (`BASE_PATH=/poodl`) → generic. |
| 9 | `docs/how-to/work-in-the-component-workshop.md` | M | A | Story example (P 88-93) → the seed lockup; "token sheet Poodl no longer keeps" generic. |
| 10 | `docs/how-to/work-with-the-specs.md` | M | A | Module table (P 18-23) → one row "the root module"; tooling and waiver sections verbatim. |
| 11 | `docs/how-to/maintain-dependencies.md` | M | A | Add "Take a template update" cross-link; "no Dependabot" sentence kept until C04. |
| 12 | `docs/how-to/deploy-to-github-pages.md` (.jinja) | M | A | Project site at `{{ pages_url }}`, `BASE_PATH={{ base_path }}`, upload `build/`; keep One-time setup steps 1-2 (P 22-25, 29-31) and Rolling back; drop DNS, staging, "address Poodl used to have". |
| 13 | `docs/how-to/update-from-template.md` (.jinja) | M | A | New; from foo/www's page: `uvx copier update --skip-answered` (no `--trust`), seed list verbatim, merge points and the bottom-append convention, marker names, `just lock && just fix && just check`, answers-file rule, tag pinning, frozen-inventory rule; "Steps by version" section for future releases; renders `_copier_answers._commit`. `canonical_for: [template_update_procedure]`. |
| 14 | `docs/explanation/architecture.md` | M | A | Drop the `app/` reducer layer and decision 0007 links; ports: three here plus the platform's two. |
| 15 | `docs/explanation/layering.md` | M | B | Drop reducer references; "five ports, three here". |
| 16 | `docs/explanation/specifications.md` | M | A | Module graph (P 35-44) → one root module; scoring example → generic. |
| 17 | `docs/explanation/accessibility.md` | M | B | From the hub's page, trimmed to what a game owes (~300 words), not Poodl's 3573-word game page. |
| 18 | `docs/explanation/security-model.md` | M | A | Drop custom-link/obfuscation paragraphs (P 39-47) and decision 0005 link. |
| 19 | `docs/explanation/quality-philosophy.md` | M | A | Verbatim except `navigator.clipboard` example (P 59) → `localStorage`. |
| 20 | `docs/reference/commands.md` | M | A | Drop `stage`, `stage-preview` rows. |
| 21 | `docs/reference/configuration.md` | M | A | BASE_PATH row for a project site; figures table = the six platform figures; word/share/daily rows dropped. |
| 22 | `docs/reference/testing.md` | M | A | Suite table = managed tests plus the seed suite. |
| 23 | `docs/reference/quality-gates.md` | M | A | P line 62 "Poodl" → "this game"; gate table and "On `main`" verbatim (keeps the stated network exception for gate 6 so `.storybook/main.ts` refs stay verbatim). |
| 24 | `docs/reference/documentation-contract.md` | M | A | Verbatim plus one paragraph: managed vs seed pages and what `copier update` does to each. |
| 25 | `docs/reference/agent-contract.md` | M | A | P's page with its "What a skill must be" and "What a bridge must be" sections (P 37-58) replaced by H's (H 42-84): the shipped validator is H's, whose bridge rule is one exact sentence, not P's "at most forty words". |
| 26 | `docs/operations/maintenance.md` | M | B | Drop word-list paragraph (P 29-30); Secrets section verbatim. |
| 27 | `docs/operations/troubleshooting.md` | M | A | Drop `stage` lines; 401 section kept. |
| 28 | `docs/decisions/README.md` (.jinja) | S | A | Ten rows; "how {{ game_name }} is built"; Writing-a-new-one verbatim. |
| 29 | `decisions/0001-static-site-no-backend.md` | S | A | Poodl 0001; drop the two supersession notes (P 43-46, 55-58); slug `decision_no_backend`. |
| 30 | `decisions/0002-ports-and-fakes.md` | S | A | Poodl 0002; boundaries = storage, clock, randomness plus the platform's two; `decision_ports_and_fakes`. |
| 31 | `decisions/0003-specs-are-the-source-of-truth.md` | S | A | Poodl 0003; drop "not installed" cost (P 44-46); `decision_spec_first`. |
| 32 | `decisions/0004-python-toolchain.md` | S | A | Poodl 0004; name only; `decision_python_toolchain`. |
| 33 | `decisions/0005-component-workshop.md` | S | A | Poodl 0006 renumbered; drop the three palette-defect narratives; `decision_component_workshop`. |
| 34 | `decisions/0006-visual-review-in-chromatic.md` | S | A | Poodl 0008 renumbered; keep entry points, fork refusal, token, auto-accept, add the no-token skip; `decision_visual_review`. |
| 35 | `decisions/0007-project-managed-allium-cli.md` | S | A | Poodl 0011 renumbered; final form only; `decision_allium_cli`. |
| 36 | `decisions/0008-design-system-as-a-package.md` | S | A | Poodl 0013 rewritten for a game that starts with the package; `decision_design_system_as_a_package`. |
| 37 | `decisions/0009-rendered-from-the-template.md` | S | A | New: why Copier, managed vs seed, the frozen inventory, what `copier update` does; `decision_rendered_from_template`. |
| 38 | `decisions/0010-a-project-pages-site.md` (.jinja) | S | A | New, replaces Poodl 0009: `{{ pages_url }}`, `BASE_PATH` from the event, no domain; `decision_project_pages_site`. |

Each carried decision opens "Carried from Poodl's decision NNNN" and keeps Poodl's `canonical_for` slug (the hub's precedent: `H/AGENTS.md:242-243`). Managed pages link only to managed pages and to carried decisions (which a game never deletes: `decisions/README.md` "marked rather than deleted"); `test_managed_pages_link_only_to_stable_pages` enforces it. No page may link to Poodl-only paths.

**`docs/manifest.yml` layout** (strict JSON, `schema_version: 1`): Poodl's entries in Poodl's grouping minus `how-to/replace-the-word-lists.md` and decisions 0005/0007/0009/0010/0012/0013; `{"path": "how-to/update-from-template.md", "title": "Update from the template", "kind": "how-to", "audience": ["maintainer", "agent"], "canonical_for": ["template_update_procedure"], "requires": []}` after `deploy-to-github-pages.md`; then a blank line and the seed block in this order: `project/purpose-and-scope.md`, `project/terminology.md`, `decisions/README.md`, `decisions/0001…0010` (titles `Decision NNNN: <title from the table>`, audiences as Poodl's, the two new slugs `decision_rendered_from_template`, `decision_project_pages_site`). Game entries follow the last decision.

**`docs/README.md.jinja` layout**: Poodl's frontmatter and intro (line 15-16 → "rooted at `{{ game_slug }}.allium`", "Poodl's restatements" → "this game's restatements"); `## Start here` (Purpose and scope "what {{ game_name }} is for", Repository map, Terminology, first change); `## How to` (Poodl's seven minus word lists plus `- [Update from the template](how-to/update-from-template.md)`); `## Platform`; `## Understand`; `## Look up`; `## Run it`; `## Decisions`; then:

```markdown
## This game

Pages this game adds are listed here, after everything the template manages, so an
update from the template and an addition here land in different places.
```

## 9. Template repository: tooling, harness, CI

Root layout: `.github/workflows/ci.yml`, `.gitignore`, `.editorconfig` (Poodl's plus `[*.md.jinja]` unset/no-trim, `[*.allium.jinja]` 4), `.markdownlint-cli2.jsonc` (Poodl's, ignores add `template`?—no: lint shipped `.md` at source; ignores `.venv`, `ai_tmp`), `lychee.toml` (Poodl's with `exclude_path = [".git", ".venv", "ai_tmp", "template"]`: shipped pages link to `.jinja`-suffixed neighbours the offline checker cannot resolve; the render's own gate checks them), `.pre-commit-config.yaml`, `.pre-commit-fix.yaml`, `.python-version` (3.14), `AGENTS.md` (~150 words: three file classes, never edit `template/` without `just test`, a seed change reaches no existing game, tagging/pushing are separately authorised, scratch in `ai_tmp/`), `CLAUDE.md` (`@AGENTS.md`), `CHANGELOG.md` (Keep a Changelog; per release the headings Managed / Seed / Questionnaire / Update notes), `Justfile`, `README.md`, `copier.yml`, `pyproject.toml`, `uv.lock` (committed), `template/`, `tests/`, `tickets/`.

`pyproject.toml`: foo/www's shape switched to Poodl's `[tool.uv] package = false` idiom and Poodl's ruff `select`; `requires-python = ">=3.14"`; `dependencies = ["copier==9.18.2", "pathspec==<verify>", "PyYAML==6.0.3"]`; dev group `mypy`, `pytest`, `pytest-timeout`, `types-PyYAML` (foo/www's pins, verify), `prek==0.4.12`, `ruff==0.16.2`; pytest `addopts = ["-ra", "--strict-config", "--strict-markers", "--timeout=1800"]`, markers `network` and `full`; `[tool.ruff] src = ["tests", "template/scripts"]` with Poodl's `scripts/**` per-file ignores applied to `template/scripts/**` and `tests/**` = `["PLR2004", "S101", "S603", "S607"]`; `[tool.typos.files] extend-exclude = ["uv.lock"]`.

`Justfile` (foo/www shape + Poodl's `install-hooks`/`fix`/`lock-check`):

```just
set positional-arguments := true
set shell := ["sh", "-eu", "-c"]

default:
    @just --list

sync:
    uv sync --frozen

lock:
    uv lock

lock-check:
    uv lock --check

install-hooks:
    git rev-parse --is-inside-work-tree >/dev/null
    uv run --frozen prek install --overwrite --hook-type=pre-commit

format:
    uv run --frozen ruff check --fix-only .
    uv run --frozen ruff format .

fix:
    -uv run --frozen prek run --all-files --config .pre-commit-fix.yaml
    uv run --frozen prek run --all-files --config .pre-commit-fix.yaml
    just lint

lint:
    uv run --frozen prek run --all-files

typecheck:
    uv run --frozen mypy

# Renders the template into temporary directories and inspects the trees: no
# unrendered Jinja, no Poodl, the managed/seed inventory, the validators the
# render ships, the questionnaire's refusals, and a copier update round trip.
# Offline and seconds. BISCUIT_TEMPLATE_NETWORK=1 adds the allium gate.
test *args:
    uv run --frozen pytest "$@"

# Additionally runs `just initialize` and `just check` inside a render. Needs
# the network, a read:packages token npm can see, Chromium, and 10-20 minutes.
test-full *args:
    BISCUIT_TEMPLATE_NETWORK=1 BISCUIT_TEMPLATE_FULL=1 uv run --frozen pytest "$@"

check: lock-check lint typecheck test

# A render to look at, with default answers, from the working tree: dirty
# changes are included (copier stages them into a throwaway commit and says so).
render dest="ai_tmp/render":
    test ! -e "$1" || { printf '%s\n' "$1 exists; remove it first" >&2; exit 2; }
    uv run --frozen copier copy --defaults --vcs-ref=HEAD --quiet . "$1"
    printf '%s\n' "Rendered into $1"

# Interactive: asks the questionnaire and renders a new game into dest from the
# latest tag. Never initialises, commits or pushes; it prints what to do next.
new-game dest:
    test ! -e "$1" || { printf '%s\n' "$1 exists" >&2; exit 2; }
    uv run --frozen copier copy . "$1"
    printf '\n%s\n' "Next: cd $1 && git init -b main && just initialize && just check"
```

`.gitignore`: `.DS_Store`, `.venv/`, `__pycache__/`, `*.py[cod]`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `.cache/`, `.lycheecache`, `ai_tmp/`, `.claude/settings.local.json`, `.codex/settings.local.json`.

`.pre-commit-config.yaml`: Poodl's reduced: `exclude` = `.git/|.venv/|ai_tmp/|uv.lock$`; local ruff check/format (`types_or: [python, pyi]`); builtin (`check-added-large-files --maxkb=768`, `check-case-conflict`, `check-executables-have-shebangs`, `check-json`, `check-merge-conflict`, `check-shebang-scripts-are-executable`, `check-toml`, `check-yaml`, `detect-private-key`); editorconfig-checker, markdownlint-cli2, typos, lychee (offline, root + tickets), shellcheck, actionlint with `files: ^(\.github|template/\.github)/workflows/.*\.ya?ml$` (all three shipped workflows are verbatim `.yml`, so they are linted at source), ripsecrets — all at Poodl's `rev` SHAs. No ESLint, no validator/spec hooks (those run inside pytest against the render). `.pre-commit-fix.yaml` mirrors Poodl's.

**Harness API** (`tests/`):

- `conftest.py`: `TEMPLATE_ROOT`, `DEFAULT_ANSWERS` (§3), `NETWORK`/`FULL` env gates with `pytest_collection_modifyitems` skipping `network`/`full`, session fixture `default_render` (one render with default answers), function fixture `git_render` (private copy + `git init -q -b main`; `validate_agents.py` lists with `git ls-files --others`, so init is enough).
- `helpers.py`: `Render(path)` with `files()`, `text_files()`, `read()`, `answers()`, `copy_to()`; `render_template(template, dest, data, vcs_ref="HEAD")` → `copier.run_copy(str(template), dest, data=data, defaults=True, unsafe=False, vcs_ref=vcs_ref, quiet=True)` (validation of `data=` answers raises `ValueError("Validation error for question '<name>': ...")`); `run_script_in_process(render, script)` via `runpy.run_path(..., run_name="__main__")` capturing `SystemExit` (both validators derive `ROOT` from `__file__`); `run_script(render, script, *args)` subprocess with `sys.executable` (for `run_allium.py`, which imports `install_allium` as a sibling); `git()`, `commit_all()` with `--no-verify` and a fixed identity.
- `inventory.py`: `MANAGED`, `SEED` frozensets of rendered paths transcribed from §4 with `<slug>` from `DEFAULT_ANSWERS["game_slug"]`, plus `GAME_EDITED` (the `M†` subset). Single source for the classification; C06's impact script reads it too.

**Tests**:

- `test_render.py` (offline): `test_inventory_matches_classification` (`render.files() == MANAGED | SEED | {".copier-answers.yml"}`; every SEED path matches `pathspec.PathSpec.from_lines("gitwildmatch", _skip_if_exists)` and no MANAGED path does; the `_exclude` update block's lines equal `_skip_if_exists`); `test_verbatim_files_are_byte_identical` (for every template source without `.jinja`, rendered bytes == source bytes; this is the residue test's first half and is what lets `.svelte` files carry `{{`/`{#`); `test_rendered_jinja_files_carry_no_delimiter` (for every `.jinja` source, the render has none of `{{`, `{%`, `{#`); `test_no_poodl_outside_provenance` (case-insensitive "poodl" only in `AGENTS.md`, `docs/project/platform.md`, `docs/decisions/*.md`, `tests/restated.ts`, `tests/platform.ts`; tokens `pnut`, `site-root`, `stage_site`, `stage-preview`, `word list`, `word-list`, `words.allium`, `daily.allium`, `sharing.allium`, `statistics.allium`, `foo/www`, `/Users/` nowhere); `test_answers_file_and_provenance` (`{"_commit", "_src_path", *DEFAULT_ANSWERS} <= answers.keys()`; `_commit` appears in `AGENTS.md`); `test_no_lockfiles_shipped`; `test_pins_agree` (workflows' `node-version: '26'`, `version: 0.11.18`, `rust-just==1.51.0`, `npm@11.17.0`, `uv python install 3.14` agree with `package.json` volta/engines and `.python-version`; `package.json` pins `@steven-cutting/biscuit-games` at `copier.yml`'s `hub_package_version`); `test_managed_pages_link_only_to_stable_pages`.
- `test_validators.py` (offline): both validators exit 0 on `git_render`; negative controls: appending `\nTODO: prove the gate reads this\n` to `docs/reference/commands.md` makes `validate_docs.py` exit 1 with "an unfinished marker" on stderr; deleting `.claude/skills/fix-quality/SKILL.md` makes `validate_agents.py` exit 1.
- `test_questionnaire.py` (offline): `pytest.raises(ValueError, match="Validation error for question 'game_name'")` for `""`, `"x"`, `"Bad{Name}"`, `"a"*41`, `"tab\there"`, `"123"`; `game_slug` refused for `"Tic Tac"`, `"_leading"`, `"UPPER"`, `"a-b"`, `"a__b"`; `repository` refused for `"nogroup"`, `"-x/y"`, `"a/.git"`; `test_computed_defaults` (only `game_name` and `description` given → `game_slug == "tic_tac_toe_beans"`, `repository == "steven-cutting/tic_tac_toe_beans"`, `docs/specs/tic_tac_toe_beans.allium` exists, `brand.ts` reads `GAME_NAME = 'tic tac toe beans'` and `GAME_TITLE = 'Tic Tac Toe Beans'`).
- `test_specs.py` (`network`): `install_allium.py` then `run_allium.py check` and `analyse` exit 0 in `git_render` (this is the test that the seed module exists and parses; `NO_INPUTS = 2` on an empty `docs/specs/`).
- `test_update.py` (offline): module fixture `template_clone` (`git clone --no-checkout` of `TEMPLATE_ROOT` into tmp; if the worktree is dirty, `git --work-tree=TEMPLATE_ROOT add -A && commit` in the clone only; skip when fewer than two commits; then, in the clone only, one synthetic commit appending `TEMPLATE_CHANGE` to `template/docs/reference/testing.md` and inserting `MAP_CHANGE` after the H1 of `template/docs/README.md.jinja`, so every round trip carries a managed and a game-edited change); `old_refs()` = `HEAD~2` plus the latest `v*` tag if any; `test_pristine_update_equals_fresh_render[old_ref]` (render at old ref, both synthetic strings absent, `git init` + commit, `copier.run_update(path, defaults=True, overwrite=True, skip_answered=True, unsafe=False, vcs_ref="HEAD", conflict="inline", quiet=True)`, no markers and no `*.rej`, tree digest equals a fresh render at HEAD ignoring `.copier-answers.yml`, both synthetic strings present, both validators pass, `git status --porcelain` empty after commit); `test_update_keeps_game_work` (render at `HEAD~2`; add `docs/project/beans.md` with frontmatter + its manifest line after the last decision + a link under `## This game`; rewrite `README.md`; rewrite the spec module; add `src/lib/components/Board.svelte` and `tests/board.test.ts`; commit; update to HEAD; no markers, no `*.rej`; the page, its manifest line and link, the README, the module and the two added files are byte-unchanged; both synthetic strings present; every MANAGED path equals the fresh render; `validate_docs.py` passes).
- `test_full.py` (`full`): copy `default_render`, `git init -q -b main`, `just initialize` exit 0, on Linux CI `just storybook-browsers-deps`, `just check` exit 0, untracked set after initialize is exactly `{package-lock.json, uv.lock}` and `just check` adds nothing.

Timing: fast suites ~10 s (one shared render plus ~15 throwaway renders at ~1 s), update ~15 s, specs ~5 s, full 10-20 min.

**Template CI** (`.github/workflows/ci.yml`, SHAs as Poodl's): triggers `pull_request`, `push` to `main`, weekly `schedule` (`17 6 * * 1`), `workflow_dispatch`; `permissions: contents: read`; concurrency cancels PR runs only. Job `fast` (15 min): checkout `fetch-depth: 0` (the update test and copier's `git describe` need history), setup-uv 0.11.18 with cache, `uv python install 3.14`, `uv tool install rust-just==1.51.0`, `just sync`, `just lock-check`, `just lint`, `just typecheck`, `just test` with `BISCUIT_TEMPLATE_NETWORK: '1'`. Job `full` (60 min, `permissions: contents: read, packages: read`): checkout `fetch-depth: 0`; setup-node 26 with `registry-url`/`scope` and **no** `cache: npm` (the lockfile it would key on does not exist in the workspace); setup-uv; python; just; `npm install --global npm@11.17.0`; `actions/cache` on `~/.cache/ms-playwright` keyed `${{ runner.os }}-playwright-${{ hashFiles('template/package.json.jinja') }}`; `just sync`; `just test-full` with `NODE_AUTH_TOKEN: ${{ github.token }}` on that step. **Both `fast` and `full` are required checks**; no `paths` filter (a skipped required check blocks the merge). `full` cannot go green until the hub package grants `biscuit_games_template` read access (UI-only, per-package).

## 10. `copier update` for a game; tags and versions

Commands (taskless, never `--trust`): `uvx copier update --skip-answered` (add `--vcs-ref=vX.Y.Z` to pick a tag, `--vcs-ref=HEAD` for the tip, `--conflict rej` for `.rej` files, `--defaults` in CI); reset with `uvx copier recopy --skip-answered`; change an answer with `uvx copier update` (re-asks with the recorded answers as defaults). Refused on a dirty worktree, a downgrade, or an undetectable version.

What `docs/how-to/update-from-template.md` and the template README tell a maintainer, in order: (1) commit everything, then update; (2) the seed list, verbatim: "these are yours; an update never touches them, and one you delete stays deleted"; (3) the merge points that conflict when both sides append (`docs/manifest.yml`, `docs/README.md`, `AGENTS.md`, `Justfile`, `package.json`, `eslint.config.js`, `.gitignore`, `src/lib/config.ts`) and the bottom-append convention; (4) the marker names, and that the template side is a suggestion where a real disagreement exists; (5) `just lock && just fix && just check`, commit with the answers file; (6) never edit `.copier-answers.yml` except `_src_path`; (7) pin to a tag; `copier update` picks the latest PEP 440 tag, a prerelease needs `--prereleases`; (8) a release that deletes a managed file says so in the template CHANGELOG "Update notes"; (9) when a departure would suit every game, change the template.

Tags: annotated `vMAJOR.MINOR.PATCH` on `main`; prereleases as `v0.2.0rc1` (no hyphen). MAJOR: a game must do work beyond resolving markers (validator contract change, removed managed file, new question without a default). MINOR: new managed file/page/recipe, pin bump, `_min_copier_version` change. PATCH: prose. **Tag `v0.1.0` before the first consumer render**: an untagged render records a bare SHA as `_commit` and update leans on dunamai's `0.0.0.postN` fallback. `pyproject.toml` pins `copier==9.18.2`; `_min_copier_version` moves only when the template needs something newer.

## 11. Rules for tickets and lanes

- **Worktrees and branches.** Each ticket is executed on the branch its `branch:` field
  names (`<branch>`, lowercase: `ticket/t03-workflows`) in its own worktree, created from
  `main` after T00 has merged. From a Supacode terminal:
  `supacode repo worktree-new --branch <branch> --base main --name <id>`;
  otherwise `git worktree add ../<id> -b <branch> main`. A ticket touches only
  its listed files plus the `status:` line of its own `tickets/<id>-*.md`.
- **T00 renders a shape-complete skeleton.** The fast suite (inventory, residue, both
  validators) can only be green if every path in §4 exists from the first commit, so
  T00 ships a stub for every managed and seed file: each registered page with valid
  frontmatter, a matching H1 and 40 or more words of real prose summarising what the
  page will say; `AGENTS.md` carrying the six required phrases and 300 words; all eight
  skills with descriptions that state a trigger and bodies that cite `AGENTS.md` and a
  `just` recipe, plus the sixteen fixed-body bridges; the seed module, source and test
  files of §7 in final form. Lanes **replace** stubs.
- **Files no lane touches:** `docs/manifest.yml`, `docs/README.md.jinja`, `copier.yml`
  and `tests/inventory.py`. A lane that needs a change there (a page rename, a new
  path) stops and hands it back as a T00 follow-up on `main`, because every other lane
  reads those files and the manifest and map re-render into every game.
- **No rendered path appears in two lane tickets' Files-touched lists.** The tickets
  were checked against each other for this; an agent that finds a need to edit another
  lane's file hands it back instead.
- **Self-contained.** A ticket is written for an agent with no context: it embeds exact
  content or cites this document by section, and names the P, H and foo/www source
  paths to read. It never cites a chat transcript, a scratch directory or a tool
  result.
- **Paths as code spans.** Ticket text writes template paths as code spans, never as
  relative Markdown links: T00's hook gate runs lychee offline over `tickets/`, and a
  link to a `template/` file that does not exist yet fails it.
- **Definition of done**, for every build ticket: `just check` green in the template
  repository (the fast suite), the ticket's own acceptance criteria met, the
  verification commands run with their output quoted in the hand-back notes, and the
  ticket's `status:` set to `done` in the same pull request.
- **Separately authorised actions.** Commits on the ticket branch are the ticket's work.
  Pushing, opening a pull request, tagging, filing GitHub issues, deploying, editing
  another repository (P, H, `tic_tac_toe_beans`) and changing repository settings are
  each a separately authorised action: the ticket says where one occurs, and the agent
  stops and asks the maintainer rather than proceeding. Nothing under `tickets/` has
  been filed as a GitHub issue.
- **`full` is not a required check until the grant exists.** The template repository's
  `full` CI job cannot go green until the hub package grants
  `steven-cutting/biscuit_games_template` read access (a per-package setting in the
  GitHub UI; no REST endpoint was found). C03 sets branch protection and carries that
  order explicitly; no lane ticket touches repository settings.
- **Credentials.** The GitHub Packages token lives only in `~/.npmrc` on the developer's
  machine and in `github.token` in CI. No file in any repository carries a token, and
  documentation writes `<your token>` after `_authToken=` because ripsecrets flags a bare
  word there.

## 12. Unverified claims, and the ticket that checks each

Each claim below was reasoned from source but not executed. The named ticket runs the
check and records the outcome in its hand-back notes; a claim that fails is a design
change that goes back through this document.

- The seed Allium module (§7) parses and reports no diagnostics: bare `Play` as a
  surface identifier, a surface with no `contracts:` block, and figures referenced only
  in `--` comment bodies not tripping `allium.field.unused` (H's
  `docs/specs/appearance.allium` lines 97-98 and 162-166 do the last and its gate
  passes). Check: `just install-allium && just check-specs && just analyse-specs` in a
  render; the automated form of the same check is T02's `tests/test_specs.py`. **T06.**
- `github.event.repository.name` is populated in a workflow-level `env` on both `push`
  and `workflow_dispatch`. Check: the first dispatch run of a rendered `pages.yml`.
  **T03 at source, T11 on the first push.**
- jsdom reflects a Svelte 5 `<svelte:head><title>` into `document.title` under
  `@testing-library/svelte` (the `titles the document after the game` case in
  `tests/route.test.ts`). Check: run the seed suite in a render; drop the case rather
  than weaken the heading case if it proves flaky. **T05.**
- `git clone --no-checkout` of a linked worktree path (the `template_clone` fixture)
  yields a clone whose HEAD is the worktree's. Check: `tests/test_update.py` on its
  first run in a `.supacode` worktree. **T10.**
- Python pins for the template repository: mypy 2.3.0, pytest 9.1.1, pytest-timeout
  2.4.0, types-PyYAML 6.0.12.20250915 (foo/www's), and a pathspec version (a copier
  transitive dependency). Check against PyPI when writing `pyproject.toml`. **T00.**
- dunamai's `Pattern.DefaultUnprefixed` accepts both `v0.1.0` and `0.1.0` tags. Check:
  `uv run python -c 'import dunamai; print(dunamai.Pattern.DefaultUnprefixed.regex())'`
  in the template venv. **T10.**
- `copier.run_copy(..., data=...)` raises
  `ValueError("Validation error for question '<name>': ...")` when a validator fails.
  Check: `tests/test_questionnaire.py` on its first run. **T10.**
- A pathspec gitwildmatch pattern with a leading and a trailing slash (`/docs/decisions/`)
  matches every file beneath the directory when matched against rendered relative paths,
  and an empty rendered `_exclude` line is ignored. Check:
  `test_inventory_matches_classification` builds the same `PathSpec` and asserts on every
  seed path. **T00.**
- typos never flags the default slug words or a game name. Check: `just check-docs` in
  the first render; the remedy is an `extend-words` entry in the game's `pyproject.toml`.
  **T11.**
- Storybook's `getAllByRole('button')` in the narrow lockup story measures the one
  `settings` action at or above 44px inside a 320px frame with the hub's `HeaderBar`
  1.0.0 (Poodl's story measures four actions and passes). Check: `just storybook-test`
  in a render. **T05.**
- `just import? 'Justfile.local'` works on just 1.51.0. Check: `just --version` and a
  two-line Justfile in `ai_tmp/`. **C07.**
- Every `gh api` endpoint C03 names (Pages with `build_type=workflow`, branch
  protection, private vulnerability reporting), and whether rulesets are now preferred.
  Check: the `gh api` documentation before writing `scripts/bootstrap_repo.sh`. **C03.**
- Renovate and Dependabot capabilities C04 relies on (GitHub Packages host rules, uv
  lockfile updates, SHA-with-comment action pinning, pre-commit rev handling, the
  absence of shared Dependabot presets). Check before choosing. **C04.**
- The hub package grants a repository read access through the package's "Manage Actions
  access" setting, and no REST endpoint exists for it. Check: the package settings UI.
  **C03.**

## 13. Risks every ticket states where it applies

- **Frozen seed inventory.** `docs/manifest.yml` and `docs/README.md` re-render on every
  update while seeds never do, so after `v0.1.0` the template can never add, rename or
  retitle a seed page or a numbered decision without breaking `check-docs` in every
  game. Later hand-offs must be managed pages. Stated in the template README,
  `docs/how-to/update-from-template.md` and here; C06's impact check refuses a seed
  addition.
- **The two seed lists must stay identical.** The `_exclude` update block and
  `_skip_if_exists`; drift shows only on `copier recopy`.
  `test_inventory_matches_classification` asserts equality.
- **A managed file the template stops rendering is removed from every game**, even where
  edited (copier's `_remove_old_files`). Every removal is announced in the template
  `CHANGELOG.md` under "Update notes" and is a MAJOR release.
- **Tag before the first consumer render.** An untagged render records a bare SHA as
  `_commit` and update leans on dunamai's `0.0.0.postN` fallback. T11 tags `v0.1.0`
  first; `tests/test_update.py` depends on `HEAD~2` having a smaller distance than
  `HEAD`, which merge-commit histories can confuse until tags exist.
- **Delete the stub README before copying into `tic_tac_toe_beans`.** `_skip_if_exists`
  is checked before overwrite, so `copier copy` keeps an existing `README.md` and
  `_message_after_copy` prints too late to help.
- **`initialize.sh` aborts half-way on an unfixable ESLint error.** It runs
  `npm run lint:fix` under `set -eu` before `install-hooks`, so a seed file that
  strictTypeChecked rejects leaves a half-initialised tree. The template's `full` job
  and T05's lint-clean seeds are the guard.
- **Same-hunk appends conflict inline on update** in `docs/manifest.yml`,
  `docs/README.md`, `AGENTS.md`, `Justfile`, `package.json`, `eslint.config.js` and
  `src/lib/config.ts`. The bottom-append convention (§5) reduces but does not eliminate
  them; an agent that "tidies" ordering recreates them.
- **`full` is blocked until the package grant.** Until the hub package grants this
  repository read access, `full` as a required check would block every merge, so C03 is
  applied to this repository immediately after T00, or `full` is made required only once
  it is green.
- **Small coverage denominator.** Coverage over `src/lib/**` has about fourteen branch
  sites; dropping any of Poodl's storage "unusable store" cases, adding an untested
  constants file or putting a `{#if}` in `Lockup.svelte` breaches 90%.
- **The first `just check` in a render needs the network** (prek clones every hook
  repository on the first `lint`) and, on Linux, a manual `just storybook-browsers-deps`
  with sudo; an offline first run fails at `lint` or `storybook-test` for no template
  reason.
- **`.copier-answers.yml` must be in `.prettierignore`.** Prettier rewrites YAML it does
  not own; without the entry `prettier --check` and copier's regenerated answers file
  fight on every update (foo/www never ignored it).
- **`_copier_operation` inside `_exclude` was verified in copier 9.18.2 only.**
  `_min_copier_version` is pinned there so an older copier is refused rather than
  rendering wrongly; a newer major could change the semantics.
- **The 38-page handbook must clear `validate_docs` on T00's first commit as stubs** and
  again after every lane's rewrite; a lane that renames a page breaks the manifest it may
  not edit, so renames go through a T00 follow-up on `main`.
- **`docs/project/platform.md` must not state a literal hub version** (P's line 34 says
  `1.0.0`), or it drifts the moment a game bumps the package locally.
- **C07 pays a per-page reconciliation** on Poodl's first update for every handbook page
  whose old-render side differs from Poodl's prose; the fallback of leaving Poodl off the
  template is real and is decided before that ticket is picked up.
- **`tic_tac_toe_beans` is a private repository today** (`gh repo view --json isPrivate`
  on 2026-09-09). GitHub Pages from a private repository needs a paid plan, so its first
  `pages.yml` run may fail for that reason alone; whether it goes public is the
  maintainer's decision, taken in C03 before T11's first push.
- **`repository` defaulting to `steven-cutting/<slug>` is prose-only.** It reaches
  `pages_url` and `base_path` in the handbook and `AGENTS.md`; a mismatch with the real
  repository name is invisible to any gate, while `pages.yml` stays correct because it
  reads the event.
