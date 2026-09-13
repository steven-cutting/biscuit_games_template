"""The classification of every rendered path, and the single source of it.

`MANAGED` is re-rendered into a game on `copier update` and merged with the game's edits.
`SEED` is rendered once and never touched again. `GAME_EDITED` is the managed subset a game
is expected to edit (CONVENTIONS §5). `.copier-answers.yml` is Copier's and in none of them.
`tests/test_render.py`, `tests/test_update.py` and C06's impact check read all three.
"""

from __future__ import annotations

from tests.conftest import DEFAULT_ANSWERS

SLUG = DEFAULT_ANSWERS["game_slug"]

SKILLS = (
    "accessibility-review",
    "code-review",
    "fix-quality",
    "plan-change",
    "project-check",
    "review-docs",
    "spec-change",
    "svelte-change",
)
DECISIONS = (
    "0001-static-site-no-backend",
    "0002-ports-and-fakes",
    "0003-specs-are-the-source-of-truth",
    "0004-python-toolchain",
    "0005-component-workshop",
    "0006-visual-review-in-chromatic",
    "0007-project-managed-allium-cli",
    "0008-design-system-as-a-package",
    "0009-rendered-from-the-template",
    "0010-a-project-pages-site",
)
MANAGED_PAGES = (
    "project/repository-map",
    "project/platform",
    "tutorials/first-change",
    "how-to/develop-locally",
    "how-to/test-and-debug",
    "how-to/work-in-the-component-workshop",
    "how-to/work-with-the-specs",
    "how-to/maintain-dependencies",
    "how-to/deploy-to-github-pages",
    "how-to/update-from-template",
    "explanation/architecture",
    "explanation/layering",
    "explanation/specifications",
    "explanation/accessibility",
    "explanation/security-model",
    "explanation/quality-philosophy",
    "reference/commands",
    "reference/configuration",
    "reference/testing",
    "reference/quality-gates",
    "reference/documentation-contract",
    "reference/agent-contract",
    "operations/maintenance",
    "operations/troubleshooting",
)

MANAGED: frozenset[str] = frozenset(
    {
        ".editorconfig",
        ".gitattributes",
        ".gitignore",
        ".markdownlint-cli2.jsonc",
        ".npmrc",
        ".pre-commit-config.yaml",
        ".pre-commit-fix.yaml",
        ".prettierignore",
        ".prettierrc.json",
        ".python-version",
        "AGENTS.md",
        "CLAUDE.md",
        "chromatic.config.json",
        "eslint.config.js",
        "lychee.toml",
        "package.json",
        "pyproject.toml",
        "svelte.config.js",
        "tsconfig.json",
        "vite.config.ts",
        "vitest.config.ts",
        "vitest.storybook.config.ts",
        "Justfile",
        ".claude/settings.json",
        ".github/copilot-instructions.md",
        ".github/workflows/ci.yml",
        ".github/workflows/chromatic.yml",
        ".github/workflows/pages.yml",
        ".storybook/main.ts",
        ".storybook/preview.ts",
        "scripts/check_playwright_browsers.js",
        "scripts/initialize.sh",
        "scripts/install_allium.py",
        "scripts/run_allium.py",
        "scripts/run_project_check.py",
        "scripts/run_ripsecrets_redacted.py",
        "scripts/validate_docs.py",
        "scripts/validate_agents.py",
        "static/.nojekyll",
        "src/app.html",
        "src/app.d.ts",
        "src/routes/+layout.svelte",
        "src/routes/+layout.ts",
        "src/lib/config.ts",
        "src/lib/ports/storage.ts",
        "src/lib/ports/clock.ts",
        "src/lib/ports/random.ts",
        "tests/setup.ts",
        "tests/platform.ts",
        "tests/platformSpecs.test.ts",
        "tests/ports.test.ts",
        "docs/manifest.yml",
        "docs/README.md",
        *(
            f".{provider}/skills/{name}/SKILL.md"
            for provider in ("agents", "claude", "codex")
            for name in SKILLS
        ),
        *(f"docs/{page}.md" for page in MANAGED_PAGES),
    }
)

SEED: frozenset[str] = frozenset(
    {
        "README.md",
        "CHANGELOG.md",
        "SECURITY.md",
        "docs/project/purpose-and-scope.md",
        "docs/project/terminology.md",
        "docs/decisions/README.md",
        *(f"docs/decisions/{name}.md" for name in DECISIONS),
        f"docs/specs/{SLUG}.allium",
        "src/lib/brand.ts",
        "src/lib/components/Lockup.svelte",
        "src/routes/+page.svelte",
        "stories/Lockup.stories.svelte",
        "tests/restated.ts",
        "tests/lockup.test.ts",
        "tests/route.test.ts",
    }
)

# Managed, and expected to be edited by the game (CONVENTIONS §5).
GAME_EDITED: frozenset[str] = frozenset(
    {
        "docs/manifest.yml",
        "docs/README.md",
        "AGENTS.md",
        "Justfile",
        "package.json",
        "eslint.config.js",
        ".gitignore",
        ".prettierignore",
        "lychee.toml",
        ".pre-commit-config.yaml",
        ".pre-commit-fix.yaml",
        "pyproject.toml",
        "src/lib/config.ts",
        "tests/ports.test.ts",
    }
)
