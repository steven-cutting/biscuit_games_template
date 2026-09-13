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
# `game_name` and `description` have no default, so they are passed as
# tests/conftest.py's DEFAULT_ANSWERS spells them; the other answers derive.
render dest="ai_tmp/render":
    test ! -e "$1" || { printf '%s\n' "$1 exists; remove it first" >&2; exit 2; }
    uv run --frozen copier copy --defaults --vcs-ref=HEAD --quiet \
        --data game_name="Tic Tac Toe Beans" \
        --data description="A three-in-a-row game played with beans." \
        . "$1"
    printf '%s\n' "Rendered into $1"

# Interactive: asks the questionnaire and renders a new game into dest from the
# latest tag. Never initialises, commits or pushes; it prints what to do next.
new-game dest:
    test ! -e "$1" || { printf '%s\n' "$1 exists" >&2; exit 2; }
    uv run --frozen copier copy . "$1"
    printf '\n%s\n' "Next: cd $1 && git init -b main && just initialize && just check"
