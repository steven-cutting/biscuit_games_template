---
id: C03
title: "Repository bootstrap: the settings a rendered game and this repository need"
status: done
depends_on: []
parallel_with: []
branch: ticket/c03-repository-bootstrap
estimated_size: M
---

# C03: Repository bootstrap: the settings a rendered game and this repository need

## Context

A rendered game passes `just check` on its first run, but its GitHub repository still
needs settings that no file can carry, and Poodl records each of them:

- **The Pages source must be GitHub Actions.** Until it is, the build job succeeds and
  uploads its artefact but the deploy job fails with
  `Failed to create deployment (status: 404)`; the workflow cannot set it for itself
  (`/Users/scutting/projects/poodl/docs/how-to/deploy-to-github-pages.md` lines 17-31,
  "One-time setup"; the same symptom at
  `/Users/scutting/projects/poodl/docs/operations/troubleshooting.md` lines 124-128).
  The `github-pages` environment the deploy job names
  (`/Users/scutting/projects/poodl/.github/workflows/pages.yml` lines 78-80) is created by
  the first run, so no step makes it.
- **`main` is protected behind the three CI jobs** `frontend`, `documents` and
  `stories` (the job ids at `/Users/scutting/projects/poodl/.github/workflows/ci.yml`
  lines 23, 66 and 119; no job carries a `name:`, so the id is the check's name), not
  required to be up to date, no review, force pushes and deletion refused,
  administrators not bound
  (`/Users/scutting/projects/poodl/docs/reference/quality-gates.md` lines 139-151,
  "On `main`"). The Chromatic job is deliberately not required
  (`/Users/scutting/projects/poodl/.github/workflows/chromatic.yml` lines 163-164).
- **`CHROMATIC_PROJECT_TOKEN` is the one stored secret**
  (`/Users/scutting/projects/poodl/docs/operations/maintenance.md` lines 62-72,
  "Secrets"), and it is optional for a rendered game: the template's `chromatic.yml`
  carries the hub's guard, which notes the absent token and skips the publish
  (`/Users/scutting/projects/biscuit_games/.github/workflows/chromatic.yml` lines
  207-217 and 251-261; CONVENTIONS.md §7).
- **Private vulnerability reporting is promised** by the seed `SECURITY.md`, which is
  Poodl's minus three bullets (`/Users/scutting/projects/poodl/SECURITY.md` lines 3-7;
  CONVENTIONS.md §4). The promise is conditional and the file says so: GitHub offers the
  form on public repositories, and the paragraph T07 adds after Poodl's line 7 sends a
  reporter to the repository's owner directly while it is private. So this step turns the
  feature on where it exists, and where it does not the policy still names a route.
  `SECURITY.md` is a seed, excluded from `copier update`, so a game rendered before that
  paragraph existed keeps the older wording.
- **The platform package must grant the repository read access** so CI can install
  `@steven-cutting/biscuit-games` with the run's own token. It is "a setting on the
  package, not on either repository" (troubleshooting.md lines 69-70; maintenance.md
  lines 68-72;
  `/Users/scutting/projects/biscuit_games/docs/how-to/consume-the-hub.md` lines 48-50).
  A missing grant fails every installing job with `404 Not Found` for the package
  (troubleshooting.md lines 67-70).

The live state, read on 2026-09-09 with read-only `gh api` calls:

- `steven-cutting/poodl` is the reference. Its protection returns
  `required_status_checks.strict: false`, `contexts: ["frontend","documents","stories"]`
  (each with `app_id: 15368`, GitHub Actions), `enforce_admins.enabled: false`,
  `allow_force_pushes.enabled: false`, `allow_deletions.enabled: false`, and no
  `required_pull_request_reviews` or `restrictions` key. Its Pages record says
  `build_type: "workflow"`. It has no rulesets. Its private vulnerability reporting is
  `enabled: false`, so the promise in its own `SECURITY.md` is unkept today.
- `steven-cutting/biscuit_games_template` (public, `main` exists): `main` not
  protected, Pages not enabled, vulnerability reporting off, `delete_branch_on_merge`
  false, wiki and projects on.
- `steven-cutting/tic_tac_toe_beans` (**private**, `main` exists with one commit):
  `main` not protected, Pages not enabled; the vulnerability-reporting endpoint answers
  `404 Not Found`, and GitHub's documentation offers the feature to public repositories.
  Whether a private repository can publish a Pages site at all depends on the
  account's tier; step 10 checks before anything is applied there.

Where this ticket sits: it is not in the build order (T00 to T12), but its settings
are applied to this repository **right after T00 merges**, before the lanes fan out,
and to `tic_tac_toe_beans` **before T11's first push**. This repository's CI has two
jobs, `fast` and `full`, both meant to be required (CONVENTIONS.md §9), but `full`
cannot go green until the package grant exists, and a required check that cannot pass
blocks every merge (CONVENTIONS.md §11 and §13). So the check names differ from a
game's and are applied in two rounds, which is why the script takes options the
one-line summary in `tickets/README.md` does not show. C01, if adopted, changes the
check names to `<caller> / <callee>` and reruns this script.

`gh` 2.100.0 is authenticated as `steven-cutting` with scopes `repo`, `workflow`,
`read:org`, `gist` and `admin:public_key`; it lacks `read:packages`, so
`gh api users/steven-cutting/packages/npm/biscuit-games` answers `403` (CONVENTIONS.md
§0). The `repo` scope is what Pages, protection, secrets and vulnerability reporting
need. Every `--apply` run, every visibility change and the package grant are separately
authorised actions (CONVENTIONS.md §11; Poodl's own rule at
`/Users/scutting/projects/poodl/AGENTS.md` lines 110-113 names "enabling GitHub
Pages"). Read-only `gh api` GETs and the script's dry run are not.

Read first: the Poodl pages and workflows named above at the lines given, the hub's
`chromatic.yml` guard, `/Users/scutting/projects/biscuit_games/scripts/initialize.sh`
lines 1-5 for the shell shape this repository's scripts take, and CONVENTIONS.md §9,
§11, §12 and §13.

## Goal

- `scripts/bootstrap_repo.sh` exists in this repository (not under `template/`), is
  committed `100755`, passes the hook gate, prints what it would change without
  `--apply`, changes only what differs with `--apply`, and changes nothing on a second
  `--apply`.
- This repository's `main` requires `fast`; once the package grant is in place and
  `full` has gone green on a pull request, it requires `fast` and `full`.
- `tic_tac_toe_beans` is bootstrapped before its first push: its first CI run is green
  on `frontend`, `documents` and `stories`, and `pages.yml` deploys to
  `https://steven-cutting.github.io/tic_tac_toe_beans/`.
- The template `README.md` carries a "Bootstrap" section and the managed page
  `docs/how-to/deploy-to-github-pages.md` cites the script, each added here only if
  the ticket that owns the file has merged, and handed to that ticket otherwise.

## Non-goals

- Changing any workflow or check name: T03 writes the rendered workflows, T00 and T10
  write this repository's; C01 renames the contexts if adopted.
- Editing `README.md` beyond the one section (T12) or the Pages page beyond one
  sentence (T07); no other handbook page changes.
- Rendering, initialising, committing or pushing `tic_tac_toe_beans`: T11.
- Poodl's own settings. Its vulnerability reporting is off despite its `SECURITY.md`;
  that is reported in the hand-back notes for the maintainer, and C07 is where Poodl's
  repository is next touched.
- A `just` recipe wrapping the script, a custom domain, rulesets migration, or
  dependency automation (C04).
- Storing any token in any file. The Chromatic token, when supplied, arrives on stdin
  and is never echoed, never an argument.

## Files touched

| Path | Class | Source | Change |
| --- | --- | --- | --- |
| `scripts/bootstrap_repo.sh` | repo | new; shell shape from `/Users/scutting/projects/biscuit_games/scripts/initialize.sh` lines 1-5 | create, mode `100755` |
| `README.md` | repo | T12's file | add the `## Bootstrap` section in step 8, only if T12 has merged; otherwise hand the text to T12 |
| `template/docs/how-to/deploy-to-github-pages.md.jinja` | M | T07's page, from `/Users/scutting/projects/poodl/docs/how-to/deploy-to-github-pages.md` | one sentence after "One-time setup" step 2, only if T07 has merged; otherwise hand it to T07 |
| `steven-cutting/biscuit_games_template` (repository settings, no file) | repo | GitHub | protection on `main` (`fast`, later `fast` and `full`), vulnerability reporting on, optional hygiene; Pages stays off |
| `steven-cutting/tic_tac_toe_beans` (repository settings, no file) | repo | GitHub | visibility decision, Pages source, protection on `main`, vulnerability reporting, optional secret and hygiene |
| `@steven-cutting/biscuit-games` (package settings, no file) | repo | GitHub | read grant for both repositories, made by hand |

## Steps

1. **Confirm the endpoints before writing a line of shell.** Every `gh api` call below
   was checked against the REST documentation and against Poodl's live record on
   2026-09-09, and CONVENTIONS.md §12 still lists them as claims for this ticket to
   settle. Read, in this order, and note anything that has moved:
   - <https://docs.github.com/en/rest/pages/pages> (`POST` and `PUT /repos/{owner}/{repo}/pages`,
     the `build_type` field with values `legacy` and `workflow`; `POST` answers `409`
     when a site exists, `GET` answers `404` when none does).
   - <https://docs.github.com/en/rest/branches/branch-protection> (`PUT
     /repos/{owner}/{repo}/branches/{branch}/protection`; `required_status_checks`,
     `enforce_admins`, `required_pull_request_reviews` and `restrictions` are required
     and take `null` to disable; `contexts` is marked deprecated in favour of `checks`;
     `GET` answers `404` "Branch not protected").
   - <https://docs.github.com/en/rest/repos/repos> (`GET`, `PUT` and `DELETE
     /repos/{owner}/{repo}/private-vulnerability-reporting`; `GET` returns
     `{"enabled": bool}`, `PUT` returns `204`).
   - <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets>.
     Rulesets and branch protection "work alongside each other". Recommendation:
     classic branch protection, because Poodl uses it, the four settings map one to one
     onto its fields, and nothing here needs more than one rule on one branch. Take a
     ruleset instead only if the documentation now deprecates branch protection; a
     ruleset's bypass list is where "administrators not bound" goes.
   - <https://docs.github.com/en/packages/learn-github-packages/configuring-a-packages-access-control-and-visibility>,
     "Ensuring workflow access to your package": on the package's landing page click
     **Package settings**, under **Manage Actions access** click **Add repository**,
     search for the repository, and set its **Role** to **Read**. No REST endpoint for
     this is documented; if one now is, use it and say so.

   Live reference, read-only: `gh api repos/steven-cutting/poodl/branches/main/protection`,
   `gh api repos/steven-cutting/poodl/pages` and
   `gh api repos/steven-cutting/poodl/private-vulnerability-reporting`. Record the
   outcome of each check in the hand-back notes.

2. **Write `scripts/bootstrap_repo.sh`.** `#!/bin/sh`, `set -eu`, POSIX shell that
   shellcheck accepts, no `jq` dependency (every read goes through `gh api --jq`), the
   shape of `initialize.sh` lines 1-5. Interface:

   ```text
   scripts/bootstrap_repo.sh <owner>/<repo> [--apply] [--checks a,b,c] [--no-pages]
                             [--chromatic-token-stdin] [--hygiene]
   ```

   - `<owner>/<repo>` is required; a missing or malformed first argument, or an
     unknown option, exits 2 with a usage line on stderr.
   - `--checks` defaults to `frontend,documents,stories`. This repository passes
     `fast`, later `fast,full`.
   - `--no-pages` skips step 1 for a repository that deploys nothing, like this one.
   - `--chromatic-token-stdin` reads one line from stdin and stores it as the secret;
     without it the secret step is a skip with a notice.
   - `--hygiene` opts into step 6.
   - Without `--apply` the script runs every read, prints each step's current state
     and the exact command it would run, and exits 0 having changed nothing. With
     `--apply` it prints `+ <command>` before each mutating call and runs it, prints
     `already` where the state matches, and ends with `changed: N`. A second `--apply`
     prints `changed: 0` and issues no mutating call: that is the idempotency check.
   - A failed `gh` call aborts with exit 1, except the three `404`s the table below reads
     as a state. Read `404` from `gh`'s stderr (`HTTP 404`), not from a bare non-zero
     exit, so an expired login is not mistaken for "not enabled".
   - The token is never echoed, never placed in `argv`, never written to a file.

   The six steps, each a read, a comparison and a mutation, with `R` standing for
   `<owner>/<repo>`:

   | # | Step | Read | Already when | Mutation |
   | --- | --- | --- | --- | --- |
   | 1 | Pages source | `gh api repos/R/pages --jq .build_type` | prints `workflow` | `404`: `gh api -X POST repos/R/pages -f build_type=workflow`; `legacy`: `gh api -X PUT repos/R/pages -f build_type=workflow`; a `409` on the `POST` falls back to the `PUT` |
   | 2 | Protection on `main` | the `--jq` below | prints `false <checks sorted, comma-joined> false false false false false` | `gh api -X PUT repos/R/branches/main/protection --input -` with the body below (`404` "Branch not protected" means "not yet") |
   | 3 | `CHROMATIC_PROJECT_TOKEN` | `gh secret list -R R`, first column | present, unless `--chromatic-token-stdin` was given (then it is rotated) | `gh secret set CHROMATIC_PROJECT_TOKEN -R R` reading stdin; without a token: `skipped: no token supplied; chromatic.yml notes the absence and skips the publish` |
   | 4 | Private vulnerability reporting | `gh api repos/R/private-vulnerability-reporting --jq .enabled` | prints `true` | `gh api -X PUT repos/R/private-vulnerability-reporting`; a `404` prints `not available: the repository is private; SECURITY.md's fallback is the route` and continues |
   | 5 | Package read grant | none (no endpoint) | never; always printed | the five UI steps from step 1, and the check: the first CI run's install succeeds with `github.token`; a `404 Not Found` for the package is the missing grant |
   | 6 | Hygiene (`--hygiene` only) | `gh api repos/R --jq '[.delete_branch_on_merge, .has_wiki, .has_projects] \| map(tostring) \| join(" ")'` | prints `true false false` | `gh repo edit R --delete-branch-on-merge --enable-wiki=false --enable-projects=false` |

   The protection read:

   ```sh
   gh api "repos/$repo/branches/main/protection" --jq '[
     .required_status_checks.strict,
     ([.required_status_checks.checks[]?.context] | sort | join(",")),
     .enforce_admins.enabled,
     .allow_force_pushes.enabled,
     .allow_deletions.enabled,
     (.required_pull_request_reviews != null),
     (.restrictions != null)
   ] | map(tostring) | join(" ")'
   ```

   Expected for a game: `false documents,frontend,stories false false false false false`.
   The read takes the names from `checks`, the field the body below writes, rather than
   from the deprecated `contexts`, which GitHub mirrors today (Poodl's protection returns
   both) but which the idempotency check should not lean on. `[...checks[]?.context]`
   also reads a protection without required checks (`required_status_checks: null`) as
   an empty list, where `.contexts | sort` stops jq with "null cannot be sorted".

   The protection body, with one `checks` entry per name in `--checks`:

   ```json
   {
     "required_status_checks": {
       "strict": false,
       "checks": [
         { "context": "frontend" },
         { "context": "documents" },
         { "context": "stories" }
       ]
     },
     "enforce_admins": false,
     "required_pull_request_reviews": null,
     "restrictions": null,
     "allow_force_pushes": false,
     "allow_deletions": false
   }
   ```

   `checks` without `app_id` lets GitHub bind each context to the app that reports
   it; Poodl's record shows `15368`, GitHub Actions. If the `POST` or `PUT /pages` answers
   `422` asking for a source, send `--input -` with
   `{"build_type": "workflow", "source": {"branch": "main", "path": "/"}}` instead and
   record it. The branch must exist before protection can be set; both `main`
   branches do.

3. **Lint.** `just lint` runs shellcheck, `check-executables-have-shebangs` and
   `check-shebang-scripts-are-executable` over the script (CONVENTIONS.md §9). Commit
   the file with `git add --chmod=+x` or `chmod 755` first; `git ls-files -s` must show
   `100755`.

4. **Dry run.** `scripts/bootstrap_repo.sh steven-cutting/tic_tac_toe_beans` and
   `scripts/bootstrap_repo.sh steven-cutting/biscuit_games_template --no-pages --checks fast`.
   Read-only; no authorisation needed. Every step prints; nothing changes.

5. **Apply to this repository, round one, right after T00 has merged.**
   **Authorisation required:** changing this repository's settings. Stop and ask, then:

   ```sh
   scripts/bootstrap_repo.sh steven-cutting/biscuit_games_template --no-pages --checks fast --apply
   ```

   Add `--hygiene` if the maintainer wants it. `fast` is required from this point on,
   so this ticket's own pull request must pass `fast` to merge.

6. **The package grant for this repository.** **Authorisation required:** a setting on
   the hub's package. Stop and ask, then the maintainer (or the agent, if told to)
   follows the five UI steps for `steven-cutting/biscuit_games_template` with role
   Read. Proof: the next pull request's `full` job installs and goes green.

7. **Apply to this repository, round two, once `full` has gone green on a pull
   request.** **Authorisation required.** Stop and ask, then:

   ```sh
   scripts/bootstrap_repo.sh steven-cutting/biscuit_games_template --no-pages --checks fast,full --apply
   ```

   Both `fast` and `full` are the contexts from then on. Neither job may carry a
   `paths` filter, since a skipped required check blocks the merge (CONVENTIONS.md
   §9); confirm that, and that neither job carries a `name:` that would change its
   context.

8. **The template `README.md`.** If `tickets/T12-maintainer-docs.md` is `done` and
   `README.md` carries T12's sections, add this section after "Maintaining" (or where
   T12 left a pointer to this ticket); otherwise put the text in the hand-back notes
   for T12 and touch nothing.

   ```markdown
   ## Bootstrap

   A rendered game passes `just check` on its first run, but four settings no file can
   carry stand between it and a green first push: the Pages source set to GitHub
   Actions, `main` protected behind the three CI jobs, private vulnerability reporting
   switched on where GitHub offers it (public repositories; on a private one
   `SECURITY.md` names the fallback), and the platform package granting the repository
   read access. `scripts/bootstrap_repo.sh` applies the first three with `gh` and
   prints the fourth, which has no API. Run
   `scripts/bootstrap_repo.sh steven-cutting/<game>` to see what
   it would change and add `--apply` to change it; every `--apply` is an authorised
   action, and a second one changes nothing. This repository was bootstrapped the same
   way with `--no-pages --checks fast,full`, `full` joining only once the package
   grant let it go green.
   ```

9. **The managed Pages page.** If `tickets/T07-handbook-a.md` is `done`, add this
   paragraph to `template/docs/how-to/deploy-to-github-pages.md.jinja` between the
   numbered "One-time setup" list and the paragraph beginning "Until step 1 is done";
   otherwise hand it to T07. It contains no Jinja delimiter and no game name, and it
   links nothing, so `validate_docs.py` and lychee are unaffected:

   ```markdown
   The template repository's `scripts/bootstrap_repo.sh` applies step 1 with `gh`,
   together with the branch protection and the vulnerability-reporting setting the
   rest of this handbook assumes. Run it from a checkout of the template before the
   first push; it also prints the one setting it cannot make, the package's read
   grant.
   ```

10. **Apply to `tic_tac_toe_beans` before T11's first push.** Two decisions first,
    each **Authorisation required:** (a) the repository is private today, vulnerability
    reporting is offered to public repositories, and whether a private repository can
    publish a Pages site depends on the account's tier (read GitHub's Pages
    documentation for the current statement), so ask whether it goes public
    (`gh repo edit steven-cutting/tic_tac_toe_beans --visibility public --accept-visibility-change-consequences`)
    or stays private on a tier that allows Pages; (b) whether a Chromatic project
    exists for it, and if so pipe its token in. Then, with authorisation:

    ```sh
    scripts/bootstrap_repo.sh steven-cutting/tic_tac_toe_beans --apply
    ```

    with `--chromatic-token-stdin`, piping the token in from wherever the maintainer
    keeps it, only when (b) says yes, and `--hygiene` if wanted. Then the package grant
    for `steven-cutting/tic_tac_toe_beans`
    (**Authorisation required**, the same five UI steps). The protection goes on before
    the first push on purpose: the owner's direct push is not bound (administrators
    not bound), so T11's push to `main` proceeds, and every later change arrives
    through a pull request behind the three checks.

11. Commit on the ticket branch, fill in the hand-back notes, set `status: done` on
    this file. Pushing and opening the pull request are separately authorised.

## Acceptance criteria

- [ ] `scripts/bootstrap_repo.sh` is committed `100755`, `#!/bin/sh`, and `just lint`
      is clean over it.
- [ ] Without `--apply`, the script prints every step (six, or five under
      `--no-pages`) with its current state and the command it would run, makes only
      `GET` calls, and exits 0.
- [ ] `--apply` twice against the same repository: the second run prints `already` or
      `skipped` for every step and `changed: 0`, with no line beginning `+`.
- [ ] After the first `--apply`, the four reads show: `build_type` `workflow` (games),
      the protection line `false <checks> false false false false false`, vulnerability
      reporting `true` (public repositories), and the secret listed when supplied.
- [ ] On a private repository, step 4 prints
      `not available: the repository is private; SECURITY.md's fallback is the route`
      and the run continues. The rendered file is not this ticket's to check — rendering
      is a non-goal above and T11's work — but the message must name the fallback so the
      maintainer is not left with a policy pointing nowhere.
- [ ] `steven-cutting/biscuit_games_template` requires `fast` right after T00 merges,
      and `fast` plus `full` only after the package grant and one green `full`.
- [ ] `tic_tac_toe_beans`' first push runs `frontend`, `documents` and `stories`
      green, and `pages.yml` deploys to
      `https://steven-cutting.github.io/tic_tac_toe_beans/`.
- [ ] `README.md` carries the "Bootstrap" section or T12 was handed the text; the
      Pages page carries the paragraph or T07 was handed it. No other file changed.
- [ ] Every `--apply`, visibility change and package grant was authorised before it
      happened, and each is recorded in the hand-back notes.
- [ ] Each open point below is answered in the hand-back notes.

## Verification

Dry run, read-only, from the repository root:

```sh
scripts/bootstrap_repo.sh steven-cutting/tic_tac_toe_beans
scripts/bootstrap_repo.sh steven-cutting/biscuit_games_template --no-pages --checks fast
```

Expected: six numbered steps (five for the second command), each with a state and a
command, no line beginning `+`, exit 0.

The gate:

```sh
git ls-files -s scripts/bootstrap_repo.sh
just lint
```

Expected: `100755` in the first column; `just lint` exits 0.

Apply and idempotency (**Authorisation required** for each `--apply`; ask first):

```sh
scripts/bootstrap_repo.sh steven-cutting/tic_tac_toe_beans --apply
scripts/bootstrap_repo.sh steven-cutting/tic_tac_toe_beans --apply
```

Expected: the first run ends `changed: N` with `N` at least 3 on a fresh public
repository; the second ends `changed: 0`.

The settings, read back:

```sh
gh api repos/steven-cutting/tic_tac_toe_beans/pages --jq .build_type
gh api repos/steven-cutting/tic_tac_toe_beans/branches/main/protection --jq '[.required_status_checks.strict, [.required_status_checks.checks[].context], .enforce_admins.enabled, .allow_force_pushes.enabled, .allow_deletions.enabled]'
gh api repos/steven-cutting/tic_tac_toe_beans/private-vulnerability-reporting --jq .enabled
gh secret list -R steven-cutting/tic_tac_toe_beans
gh api repos/steven-cutting/biscuit_games_template/branches/main/protection --jq '[.required_status_checks.checks[].context]'
```

Expected: `workflow`; `[false,["frontend","documents","stories"],false,false,false]`
(contexts in the order sent);
`true` if step 10 (a) made the repository public, and `HTTP 404` while it is private,
which is the answer step 4 reports as `not available` and `SECURITY.md`'s fallback
covers; `CHROMATIC_PROJECT_TOKEN` listed or nothing; `["fast"]` after round one and
`["fast","full"]` after round two.

The end-to-end proof, after T11's first push:

```sh
gh run list -R steven-cutting/tic_tac_toe_beans --limit 5
gh api repos/steven-cutting/tic_tac_toe_beans/pages --jq .html_url
```

Expected: the `CI` run's three jobs and the `Deploy to GitHub Pages` run all
`success`; the URL is `https://steven-cutting.github.io/tic_tac_toe_beans/` and it
serves the game.

## Hand-back notes

### Outcome

- `scripts/bootstrap_repo.sh` exists, committed `100755`, `#!/bin/sh`, POSIX, no `jq`.
  Six steps, fixed numbers: `--no-pages` omits step 1 rather than renumbering the rest.
- `steven-cutting/biscuit_games_template` was bootstrapped in the two rounds the ticket
  gives: `--checks fast` first, then `--checks fast,full`. `main` requires `fast` and
  `full`; private vulnerability reporting is on; Pages stays off; `--hygiene` was not
  wanted here.
- `steven-cutting/tic_tac_toe_beans` was bootstrapped before its first push: Pages source
  `workflow`, `main` requiring `ci / frontend`, `ci / documents` and `ci / stories`,
  vulnerability reporting on, `--hygiene` applied. No Chromatic project exists, so no
  secret was stored.
- T11's render then reached `main` through pull request 1, which passed all three checks.
  The merge deployed the site, and it serves.
- `README.md` carries the rewritten "Bootstrap a repository" section, and the managed page
  `docs/how-to/deploy-to-github-pages.md` cites the script, with its `CHANGELOG.md` entry
  under Unreleased -> Managed. The next release is at least MINOR.
- **No package grant was asked for or made.** The package is public; see Deviations.

### What was verified, and how

Output is quoted. Elisions are in square brackets.

The gate:

```console
$ git ls-files -s scripts/bootstrap_repo.sh
100755 [sha] 0  scripts/bootstrap_repo.sh
$ just lint
[18 hooks] Passed
```

`just lint` was first run while the file was still untracked, and passed because prek
lists tracked files only. Staged, it failed twice and both were fixed: the usage
heredoc's continuation was indented 33 columns, which editorconfig-checker refuses
("Wrong amount of left-padding spaces(want multiple of 2)"), and shellcheck raised SC1003
on the `*'"'* | *'\'*` case pattern, which is now `*'"'* | *\\*`. A script this
repository does not track is a script the hook gate does not see.

The dry runs, read-only, nothing changed:

```console
$ scripts/bootstrap_repo.sh steven-cutting/tic_tac_toe_beans
repository: steven-cutting/tic_tac_toe_beans
mode: dry run (nothing is changed)

1. Pages source
   state: no Pages site (HTTP 404)
   would: gh api -X POST repos/steven-cutting/tic_tac_toe_beans/pages -f build_type=workflow

2. Protection on main requiring ci / frontend,ci / documents,ci / stories
   state: not protected (HTTP 404)
   wanted: false ci / documents,ci / frontend,ci / stories false false false false false
   would: gh api -X PUT repos/steven-cutting/tic_tac_toe_beans/branches/main/protection --input -
     [the body, one checks entry per name]

3. CHROMATIC_PROJECT_TOKEN
   state: not set
   skipped: no token supplied; chromatic.yml notes the absence and skips the publish

4. Private vulnerability reporting
   state: false
   would: gh api -X PUT repos/steven-cutting/tic_tac_toe_beans/private-vulnerability-reporting

5. Package read access for @steven-cutting/biscuit-games
   state: cannot be read: no REST endpoint, and the package needs a read:packages scope
   [the four notes]

6. Hygiene
   state: not read
   skipped: --hygiene not given

changed: 0 (dry run; 3 would change)
rc=0
$ scripts/bootstrap_repo.sh steven-cutting/biscuit_games_template --no-pages --checks fast
[five steps, numbered 2 to 6; step 2 wants `false fast false false false false false`]
changed: 0 (dry run; 2 would change)
rc=0
```

Both were re-read afterwards: protection still `404`, Pages still `404`, reporting still
`false` on each repository.

The applies, each run twice. This repository, round one, 2026-09-16:

```console
$ scripts/bootstrap_repo.sh steven-cutting/biscuit_games_template --no-pages --checks fast --apply
[step 2: + gh api -X PUT [...]/branches/main/protection --input -]
[step 4: + gh api -X PUT [...]/private-vulnerability-reporting]
changed: 2
$ scripts/bootstrap_repo.sh steven-cutting/biscuit_games_template --no-pages --checks fast --apply
2. Protection on main requiring fast
   state: false fast false false false false false
   already
4. Private vulnerability reporting
   state: true
   already
changed: 0
```

The game, the same day, with `--hygiene`:

```console
$ scripts/bootstrap_repo.sh steven-cutting/tic_tac_toe_beans --hygiene --apply
[step 1: + gh api -X POST [...]/pages -f build_type=workflow]
[step 2: + gh api -X PUT [...]/branches/main/protection --input -]
[step 4: + gh api -X PUT [...]/private-vulnerability-reporting]
[step 6: state false true true; + gh repo edit [...] --delete-branch-on-merge --enable-wiki=false --enable-projects=false]
changed: 4
$ scripts/bootstrap_repo.sh steven-cutting/tic_tac_toe_beans --hygiene --apply
[every step `already` or `skipped`]
changed: 0
```

This repository, round two, 2026-09-16:

```console
$ scripts/bootstrap_repo.sh steven-cutting/biscuit_games_template --no-pages --checks fast,full --apply
2. Protection on main requiring fast,full
   state: false fast false false false false false
   wanted: false fast,full false false false false false
   + gh api -X PUT [...]/branches/main/protection --input -
[changed: 1. The tail was elided when the run was captured; the one `+` line above
is the whole of what it did.]
$ [the same command again]
   state: false fast,full false false false false false
   already
changed: 0
```

No second run printed a line beginning `+`.

The read-backs:

```console
$ gh api repos/steven-cutting/tic_tac_toe_beans/pages --jq '[.build_type, .html_url] | join(" ")'
workflow http://stevencutting.com/tic_tac_toe_beans/
$ gh api repos/steven-cutting/tic_tac_toe_beans/branches/main/protection --jq '[.required_status_checks.checks[] | [.context, (.app_id|tostring)] | join("@")]'
["ci / frontend@null","ci / documents@null","ci / stories@null"]
$ gh api repos/steven-cutting/tic_tac_toe_beans/private-vulnerability-reporting --jq .enabled
true
$ gh secret list -R steven-cutting/tic_tac_toe_beans
[empty]
$ gh api repos/steven-cutting/tic_tac_toe_beans --jq '[.delete_branch_on_merge, .has_wiki, .has_projects] | map(tostring) | join(" ")'
true false false
$ gh api repos/steven-cutting/biscuit_games_template/branches/main/protection --jq '[.required_status_checks.checks[] | [.context, (.app_id|tostring)] | join("@")]'
["fast@15368","full@15368"]
```

The end-to-end proof. Pull request 1 in `tic_tac_toe_beans`, opened from `setup` and
squash-merged as `de27e13`:

```console
$ gh pr checks 1 --repo steven-cutting/tic_tac_toe_beans
ci / documents  pass  1m31s
ci / frontend  pass  35s
ci / stories  pass  1m7s
$ gh run list --repo steven-cutting/tic_tac_toe_beans --limit 3
completed  success  [...] (#1)  Chromatic  main  push  35067100845  36s
completed  success  [...] (#1)  Deploy to GitHub Pages  main  push  35067100832  42s
completed  success  [...] (#1)  CI  main  push  35067100749
$ gh run view 35067100832 --repo steven-cutting/tic_tac_toe_beans --log | grep -i BASE_PATH
pages / build  [...]   base_path: /tic_tac_toe_beans
pages / build  [...]   BASE_PATH: /tic_tac_toe_beans
$ gh api repos/steven-cutting/tic_tac_toe_beans/environments --jq '.environments[].name'
github-pages
$ curl -sIL https://steven-cutting.github.io/tic_tac_toe_beans/ | grep -iE '^(HTTP|location)'
HTTP/2 301
location: https://stevencutting.com/tic_tac_toe_beans/
HTTP/2 200
$ curl -sL https://stevencutting.com/tic_tac_toe_beans/ | grep -o '<title>[^<]*</title>'
<title>Tic Tac Toe Beans</title>
```

`gh run list`, `gh pr checks` and `git ls-files -s` separate their columns with
tabs, shown here as two spaces.

### Each endpoint check from step 1

- **Pages.** `POST /repos/{owner}/{repo}/pages` with `-f build_type=workflow` and no
  `source` was accepted on `tic_tac_toe_beans`, a repository with commits and no site, and
  `GET` then returned `workflow`. No `422` asked for a source, so the fallback body in the
  ticket's step 2 was never needed. The `409`-to-`PUT` fallback is in the script and was
  not exercised. C01 had already accepted the same `POST` on a repository with no commits.
- **Branch protection.** `PUT .../branches/main/protection` with the ticket's body was
  accepted as written; `required_status_checks`, `enforce_admins`,
  `required_pull_request_reviews` and `restrictions` are all required and the last two take
  `null`. `GET` answers `404` "Branch not protected", which the script reads from gh's
  stderr. The deprecated `contexts` is still mirrored back beside `checks`; the script
  reads `checks[].context`, so it does not lean on the mirror.
- **Private vulnerability reporting.** `GET` returns `{"enabled": bool}` and `PUT` with no
  body enables it. Both repositories answered `false` and then `true`.
- **Rulesets, not adopted.** Classic branch protection was kept. Both repositories answer
  `[]` on `/rulesets`, Poodl uses classic protection, the four settings map one to one onto
  its fields, and nothing here needs more than one rule on one branch. Nothing in GitHub's
  documentation deprecates branch protection.
- **The package grant.** No REST endpoint was found, and the token lacks `read:packages`,
  so `gh api users/steven-cutting/packages/npm/biscuit-games` answers `403`. See
  Deviations: the grant turned out not to be needed at all.

### Deviations

- **The package grant is not needed, and none was made or asked for.**
  `https://github.com/users/steven-cutting/packages/npm/package/biscuit-games` answers an
  unauthenticated request, redirecting to the hub's package page, which reads **Public**; a
  nonexistent-package control answers `404`. A public package is installable by any
  repository with the run's own token. That agrees with C01, whose throwaway installed with
  no grant, and with this repository's `full`, green since pull request 12. So the
  ticket's steps 6 and 10, and its "A missing grant fails every installing job", describe a
  setting that does not apply today. Step 5 still prints, because no endpoint reads it
  back, and it names the five UI steps for the day the package is made private.
- **Two `README.md` sections changed, not the one step 8 names.** "Bootstrap of this
  repository" said `main` was unprotected, that `fast` was not yet required and that C03
  would confirm whether a grant existed. All three became false as this ticket ran.
- **The step 8 section is not the ticket's text.** It keeps the `ci / ...` names and the
  two-round story, drops the claim that the grant stands between a game and a green push,
  and gains the option summary, because the script now has five options the ticket's
  paragraph does not mention.
- **The Pages paragraph sits after the numbered list**, not "between the numbered list and
  the paragraph beginning 'Until step 1 is done'". C01 rewrote that page: it now has two
  numbered items, then the `github-pages` paragraph, then a paragraph beginning "Until
  step 2 is done". The paragraph also says the script prints "step 2", which on that page
  is the grant, rather than naming the grant twice.
- **Step 10 (a) needed no decision.** `tic_tac_toe_beans` is public, not private as the
  ticket and T11 record, so there was no visibility change, and step 4 was a `PUT`.
- **`--checks` defaults to `ci / frontend,ci / documents,ci / stories`**, C01's names, not
  the ticket's `frontend,documents,stories`. The list is split on commas alone, with no
  trimming, because the names carry spaces.
- **`--no-pages` omits step 1 rather than renumbering**, so its output is five steps
  numbered 2 to 6. The numbers are the ticket's and the README's.
- **A `checks` entry without `app_id` is stored as `app_id: null`** on a repository no
  workflow has run in: the game read back `ci / frontend@null` and the two others, where
  this repository, whose `fast` had run, read back `fast@15368`. The ticket expected GitHub
  to bind each context to the reporting app at write time. It does not, and the checks
  matched their runs anyway. The script compares `.context` alone, so idempotency is
  unaffected either way.
- **`gh` prints a 404's JSON body on stdout even under `--jq`**, and its `HTTP 404`
  message on stderr. The script therefore discards captured stdout on a non-zero exit and
  reads the status from stderr, and `gh_read` sets globals rather than returning through a
  command substitution, whose subshell would have swallowed the status.
- **The branch is the Supacode worktree's** `C03-repository-bootstrap-2026-9-15`, not the
  `ticket/c03-repository-bootstrap` in this file's frontmatter, as T10 to T12 and C01 were.
- **`setup` reached `main` through a pull request**, the maintainer's choice, not the
  direct push the ticket's step 10 anticipated. It passed the three required checks, which
  is a stronger proof than a push by an unbound administrator would have been.

### Handed back

- **To the maintainer, for Poodl:** its private vulnerability reporting is `false` today
  while its `SECURITY.md` promises it. `scripts/bootstrap_repo.sh steven-cutting/poodl
  --apply` fixes it; this ticket did not run it. Poodl's protection already reads
  `false ci / documents,ci / frontend,ci / stories false false false false false`, so C01's
  prompt was applied there.
- **To T07, or a follow-up:** the seed `SECURITY.md` rendered into `tic_tac_toe_beans`
  still says "While this repository is private, only people its owner has added can see it
  at all". The repository is public and its reporting form is on. Seeds are frozen at
  `v0.1.0`, so this is not C03's to change, and the paragraph is conditional prose rather
  than a false claim, but it reads oddly on a public repository.
- **To a follow-up on the Pages page:** its step 2 and the paragraph beginning "Until step
  2 is done" tell a game the package grant is needed and that `npm ci` fails with
  `404 Not Found` without it. The package is public, so neither is true today. C03's scope
  on that page is one paragraph, so the prose was left as C01 wrote it.
- **To C04:** `--hygiene` sets `delete_branch_on_merge`, which deleted `setup` when pull
  request 1 merged. Any automation that expects a long-lived branch in a bootstrapped
  repository has to account for that.
- **Nothing to C01.** It had already renamed the contexts this script encodes.

### Which authorisations were asked for and given

| Date | Action | Given |
| --- | --- | --- |
| 2026-09-15 | Chromatic, `setup` route and `--hygiene`, asked together | no Chromatic project; a pull request from `setup`; `--hygiene` on the game only |
| 2026-09-16 | `--apply` on `biscuit_games_template`, round one | yes |
| 2026-09-16 | `--apply` on `tic_tac_toe_beans`, with `--hygiene` | yes |
| 2026-09-16 | Push `setup` and open its pull request | yes |
| 2026-09-16 | Merge pull request 1, squash | yes |
| 2026-09-16 | `--apply` on `biscuit_games_template`, round two | yes |

No package grant was asked for, because none is needed. No visibility change was asked
for, because `tic_tac_toe_beans` is already public. Pushing this branch and opening its
pull request are asked for separately, after this file is committed.

## Open points, settled

- **The `gh api` endpoints, and rulesets** (CONVENTIONS.md §12). All three endpoints
  behave as the ticket wrote them; classic branch protection was kept over rulesets. See
  "Each endpoint check from step 1".
- **The package grant.** No REST endpoint exists, and the token cannot read the package at
  all without `read:packages`. It does not matter: the package is public and no grant is
  needed. See Deviations.
- **`POST /pages` with no `source`.** Accepted, on a repository with commits and no site.
  No `422`, so the fallback body was never sent. C01 had accepted the same call on a
  repository with no commits.
- **A `checks` entry without `app_id`.** Accepted before any workflow had run, stored as
  `app_id: null`, read back as sent, and it matched the runs when they came. Compare
  `fast@15368` on this repository, where a run already existed.
- **`tic_tac_toe_beans`' visibility.** Already `public`, so no decision and no change.
  Vulnerability reporting is on, not `not available`.
- **A Chromatic project for `tic_tac_toe_beans`.** None wanted. Step 3 skips in every run,
  and the workflow's own guard keeps `/chromatic` green without a token.
- **The `github-pages` environment.** Created by the first deploy run with no step here:
  the environments list was empty before the merge and holds `github-pages` after it.
- **T07 and T12.** Both `done`, so steps 8 and 9 both applied and nothing was handed back
  to either.

## Open points, carried forward

- **`gh secret set` reading stdin when `--body` is absent.** Its help text on 2.100.0 says
  so ("reads from standard input if not specified") and the script is written to it, but no
  Chromatic project exists, so no `--apply` supplied a token and the path was never run.
  Stated rather than claimed as seen.
- **Step 4's `not available` message.** It exists in the script, exactly as the ticket
  words it, and no repository in reach exercises it: `tic_tac_toe_beans`,
  `biscuit_games_template` and Poodl are all public, and all three answer the endpoint. The
  first private repository bootstrapped will be its first run.
- **The `409`-to-`PUT` fallback on `POST /pages`.** In the script, not exercised: neither
  repository had a site.
