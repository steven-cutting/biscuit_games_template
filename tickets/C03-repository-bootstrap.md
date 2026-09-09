---
id: C03
title: "Repository bootstrap: the settings a rendered game and this repository need"
status: open
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
     (.required_status_checks.contexts | sort | join(",")),
     .enforce_admins.enabled,
     .allow_force_pushes.enabled,
     .allow_deletions.enabled,
     (.required_pull_request_reviews != null),
     (.restrictions != null)
   ] | map(tostring) | join(" ")'
   ```

   Expected for a game: `false documents,frontend,stories false false false false false`.

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
gh api repos/steven-cutting/tic_tac_toe_beans/branches/main/protection --jq '[.required_status_checks.strict, .required_status_checks.contexts, .enforce_admins.enabled, .allow_force_pushes.enabled, .allow_deletions.enabled]'
gh api repos/steven-cutting/tic_tac_toe_beans/private-vulnerability-reporting --jq .enabled
gh secret list -R steven-cutting/tic_tac_toe_beans
gh api repos/steven-cutting/biscuit_games_template/branches/main/protection --jq .required_status_checks.contexts
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

Filled in by the agent that executes this ticket.

- What was verified and how: quote the dry-run output, the two `--apply` outputs with
  their `changed:` lines, the five read-backs, and `just lint`.
- Each endpoint check from step 1: confirmed as written, or what moved and what the
  script does instead; branch protection or ruleset, and why.
- What deviated from the ticket and why (a `422` on `PUT /pages`, a `checks` entry
  that needed `app_id`, a `404` that meant something other than "not enabled").
- What was handed to another ticket: the README section to T12 or the Pages
  paragraph to T07 if either had not merged; anything C01 must redo.
- For the maintainer: Poodl's private vulnerability reporting is off while its
  `SECURITY.md` promises it; the same script fixes it with
  `scripts/bootstrap_repo.sh steven-cutting/poodl --apply`, which this ticket does not
  run.
- Which authorisations were asked for and given, with the date of each `--apply`, the
  visibility decision for `tic_tac_toe_beans`, and the two package grants.
- Which open points were settled, and which are carried forward.

## Open points

- Every `gh api` endpoint named here (Pages with `build_type=workflow`, branch
  protection, private vulnerability reporting) and whether rulesets are now preferred
  (CONVENTIONS.md §12). Check: step 1, the four documentation pages and the three
  read-only calls against Poodl, before writing the script.
- The hub package grants a repository read access through the package's "Manage
  Actions access" setting and no REST endpoint exists for it (CONVENTIONS.md §12).
  Check: the package settings page, and the packages documentation page in step 1.
  The token's missing `read:packages` scope means `gh` cannot read the package at all.
- Whether `POST /repos/{owner}/{repo}/pages` accepts `build_type=workflow` with no
  `source`, and whether the `PUT` demands one. Check: the first `--apply` on
  `tic_tac_toe_beans`; the fallback body is in step 2.
- Whether a `checks` entry without `app_id` is accepted on a repository no workflow
  has run in yet. Check: the read-back after the first `--apply` shows the three
  contexts.
- Whether `tic_tac_toe_beans` goes public, or stays private on a tier that allows
  Pages. Check: `gh api repos/steven-cutting/tic_tac_toe_beans --jq .visibility` and
  the maintainer's answer; vulnerability reporting stays `not available` while it is
  private.
- Whether a Chromatic project is wanted for `tic_tac_toe_beans`. Check: the
  maintainer's answer; without one, `/chromatic` on a pull request replies with the
  no-token notice and the run stays green.
- Whether the `github-pages` environment is created by the first deploy run with no
  step here (`deploy-to-github-pages.md` lines 24-25 and GitHub's documentation both
  say so).
  Check: the environments list after T11's first push.
- Whether T07 and T12 have merged when this ticket is picked up. Check:
  `status:` in `tickets/T07-handbook-a.md` and `tickets/T12-maintainer-docs.md`.
- Whether `gh secret set` reads stdin when `--body` is absent, as its help text on
  2.100.0 states. Check: the one `--apply` that supplies a token, then
  `gh secret list`.
