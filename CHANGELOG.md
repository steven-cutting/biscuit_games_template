# Changelog

All notable changes to this template are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Versions
are tags on `main`, and what each level means for a rendered game is stated in
`tickets/CONVENTIONS.md` §10.

## [Unreleased]

### Managed

- The complete template tree, as a shape: every managed file is rendered from Poodl's
  copy or a stub, and the lane tickets under `tickets/` replace each one.
- `.prettierignore` lists `.copier-answers.yml`, which Copier rewrites on every update,
  and neither it, `.gitattributes` nor either prek config names Poodl's `src/lib/data/`.
- `tests/ports.test.ts` covers the three ports the template ships, storage, randomness
  and the clock, so a render's `npm test` no longer imports a clipboard or timer adapter
  that does not exist.
- The handbook's project, tutorial and how-to pages in final form: the repository map,
  the platform page, the first-change tutorial, six how-to pages carried from Poodl, and
  a new `docs/how-to/update-from-template.md` stating the seed list, the append
  convention and the update procedure.

### Seed

- Every seed file, in the form CONVENTIONS §7 gives it or as a stub.
- `docs/decisions/` in final form: the index and ten records, eight carried from Poodl
  and two new, on being rendered from the template and on the project Pages site. A seed
  change reaches no game that already exists; none does yet.
- `README.md`, `CHANGELOG.md` and the two seed project pages, purpose and scope and
  terminology, in final form. A seed change reaches no game that already exists; none
  does yet.

### Questionnaire

- Four questions: `game_name`, `game_slug`, `description`, `repository`.
- `game_name` and `description` refuse what the render's Markdown would read as
  syntax: surrounding whitespace, a leading `#`, `>`, `-`, `+`, `*`, `_`, `~` or
  backtick, a numbered-list start, `<`, square brackets, and a web or email address.
  `game_name`, the README heading, also refuses a trailing `#`, `.`, `,`, `;`, `:` or
  `!`.

### Update notes

- Nothing yet; no game has been rendered from this template.

[Unreleased]: https://github.com/steven-cutting/biscuit_games_template/commits/main/
