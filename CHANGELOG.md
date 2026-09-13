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

### Seed

- Every seed file, in the form CONVENTIONS §7 gives it or as a stub.

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
