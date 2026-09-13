# Tickets for building `biscuit_games_template`

This directory is the work breakdown for building the Copier template that renders new
Biscuit Games games. Each ticket is written for an AI agent with no other context,
working in its own git worktree. `CONVENTIONS.md` is the shared design every ticket
obeys and cites by section; read it first, then the ticket.

Filing these as GitHub issues, tagging, pushing and opening pull requests are separately
authorised actions. Nothing here has been filed.

## Index

Build tickets, in dependency order. The `status:` field in each ticket's frontmatter is
authoritative; this table is a snapshot.

| Id | Title | File | Depends on | Parallel with | Status |
| --- | --- | --- | --- | --- | --- |
| T00 | Foundation: `copier.yml`, tooling, harness core, manifest, stubs for every path | `T00-foundation.md` | none | none | open |
| T01 | Toolchain configs | `T01-toolchain-configs.md` | T00 | T02 to T09 | open |
| T02 | Scripts | `T02-scripts.md` | T00 | T01, T03 to T09 | open |
| T03 | Workflows | `T03-workflows.md` | T00 | T01, T02, T04 to T09 | open |
| T04 | Agent contract | `T04-agent-contract.md` | T00 | T01 to T03, T05 to T09 | open |
| T05 | Source skeleton | `T05-source-skeleton.md` | T00 | T01 to T04, T06 to T09 | open |
| T06 | Seed specification | `T06-seed-specification.md` | T00 | T01 to T05, T07 to T09 | open |
| T07 | Handbook A: project, tutorial and how-to pages | `T07-handbook-a.md` | T00 | T01 to T06, T08, T09 | open |
| T08 | Handbook B: explanation, reference and operations pages | `T08-handbook-b.md` | T00 | T01 to T07, T09 | open |
| T09 | Decision records | `T09-decisions.md` | T00 | T01 to T08 | open |
| T10 | Harness completion and the `full` CI job | `T10-harness-completion.md` | T01 to T09 | none | open |
| T11 | Integration: first green render, tag `v0.1.0`, render `tic_tac_toe_beans` | `T11-integration.md` | T10 | none | open |
| T12 | Maintainer docs: README, CHANGELOG, AGENTS.md | `T12-maintainer-docs.md` | T11 | none | open |

Centralisation tickets. Each is a recommendation written to be picked up on its own;
none blocks the build, and C03 is the one to apply first.

| Id | Title | File | Depends on | Status |
| --- | --- | --- | --- | --- |
| C01 | Reusable workflows and a composite toolchain action | `C01-reusable-workflows.md` | C03 for the check names | open |
| C02 | Validators and installers as an installable dev dependency | `C02-tooling-package.md` | C01 host decision | open |
| C03 | Repository bootstrap script | `C03-repository-bootstrap.md` | none; apply to this repository after T00 | open |
| C04 | Central dependency-update preset | `C04-dependency-updates.md` | C01 host decision if colocated | open |
| C05 | Toolchain handbook pages in the hub package | `C05-handbook-in-the-package.md` | none | open |
| C06 | Template-impact skill and check | `C06-template-impact.md` | T10 (`tests/inventory.py`) | open |
| C07 | Poodl adopts the template | `C07-poodl-adopts-the-template.md` | T11 (`v0.1.0`) | open |

## Dependency graph

```text
T00 ──┬── T01 ──┐
      ├── T02 ──┤
      ├── T03 ──┤
      ├── T04 ──┤
      ├── T05 ──┼── T10 ── T11 ── T12
      ├── T06 ──┤          │
      ├── T07 ──┤          └── C07
      ├── T08 ──┤
      └── T09 ──┘
C03 (apply to this repository right after T00) ── C01 ── C02, C04
C05, C06 stand alone (C06 reads tests/inventory.py from T10)
```

The graph is acyclic: T00, then nine parallel lanes, then T10, T11, T12 in sequence.

## How to pick up a ticket

1. Create a worktree on the branch the ticket's `branch:` field names, from `main`,
   after every ticket it depends on has merged. Below, `<branch>` is that field, which
   is lowercase (`ticket/t03-workflows`), and `<id>` is the ticket id (`T03`):

   ```sh
   supacode repo worktree-new --branch <branch> --base main --name <id>
   ```

   Outside a Supacode terminal:

   ```sh
   git worktree add ../<id> -b <branch> main
   ```

2. Read `CONVENTIONS.md`, then the ticket. Read the source files the ticket names in
   the Poodl and hub clones at the commits `CONVENTIONS.md` §0 pins.
3. Edit only the files the ticket lists, plus the `status:` line of the ticket itself.
   A change needed elsewhere is handed back in the ticket's hand-back notes, not made.
4. Run the ticket's verification commands and quote their output in the hand-back notes.
5. Commit on the ticket branch. Pushing and opening the pull request are separately
   authorised: stop and ask.

## Definition of done

For a build ticket: `just check` is green in the template repository, the ticket's
acceptance criteria are met, its verification commands ran with the output quoted in
the hand-back notes, every open point is answered or explicitly carried forward, and
the ticket's `status:` is `done` in the same pull request.

For a centralisation ticket: the recommendation is implemented where the ticket says,
its acceptance criteria are met, and every action that touches another repository or a
repository setting was authorised before it was taken.

## Ticket format

Every ticket carries frontmatter (`id`, `title`, `status`, `depends_on`,
`parallel_with`, `branch`, `estimated_size`) and these sections in this order: Context,
Goal, Non-goals, Files touched, Steps, Acceptance criteria, Verification, Hand-back
notes, Open points. Rendered template paths are written as code spans, never as links,
because the hook gate T00 installs runs lychee offline over this directory.
