# biscuit_games_template

A [Copier](https://copier.readthedocs.io/en/stable/) template that renders a new Biscuit
Games game: a static SvelteKit site consuming `@steven-cutting/biscuit-games`, carrying
Poodl's toolchain, handbook, agent contract and quality gate in generic form.

The template is under `template/`; `tests/` renders it and inspects the render. The design
is `tickets/CONVENTIONS.md`, and the work breakdown is `tickets/README.md`.

## Maintaining

```sh
just sync          # the pinned toolchain
just check         # lock-check, lint, typecheck, test
just render        # a render with default answers, in ai_tmp/render
just new-game DIR  # ask the questionnaire and render a game into DIR
```

A render has nothing run in it: `git init -b main`, `just initialize` and `just check`
inside it come next, as the message after copy says.
