# Instructions for agents working in this repository

This repository is a Copier template, not a game. `template/` is what `copier copy`
renders into a new Biscuit Games game; `tests/` renders it and inspects the result;
`tickets/` is the work breakdown, and `tickets/CONVENTIONS.md` is the design every change
obeys.

Three classes of file live under `template/`, and `tests/inventory.py` records which is
which: managed files are re-rendered into every game on `copier update` and merged with
the game's edits, seed files are rendered once and never touched again, and
`.copier-answers.yml` belongs to Copier. A change to a seed file reaches no existing
game; say so in `CHANGELOG.md` when you make one.

Never edit `template/` without running `just test`, and run `just check` before handing
back. Scratch work goes in `ai_tmp/`, which is gitignored and is where `just render`
writes by default. Pushing, tagging, opening pull requests, filing issues and touching any
other repository are separately authorised actions: stop and ask before each one.
