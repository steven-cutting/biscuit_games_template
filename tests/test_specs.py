"""The specification gate the render pins, run inside a render.

`bg-run-allium` refuses an empty `docs/specs/` (its `NO_INPUTS`), so a green
`check` and `analyse` is also the proof that the seed module exists and parses.
A subprocess rather than in-process, because both scripts read their arguments
from the command line; `python -m` from this repository's environment, which
installs the package at the render's pin.

Network: `install_allium` downloads the pinned binary, about 1.6 MB and
checksummed, into `<render>/.tools/bin`, once per render. The `network` marker
is enabled by `BISCUIT_TEMPLATE_NETWORK=1`; without it every test here is
skipped.
"""

from __future__ import annotations

import pytest

from tests.helpers import Render, run_tool


def _install(render: Render) -> None:
    install = run_tool(render, "install_allium")
    assert install.returncode == 0, install.stdout + install.stderr


@pytest.mark.network
def test_seed_module_is_clean(git_render: Render) -> None:
    _install(git_render)
    for command in ("check", "analyse"):
        result = run_tool(git_render, "run_allium", command)
        assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.network
def test_gate_refuses_an_empty_specs_directory(git_render: Render) -> None:
    # The negative control: a gate that read nothing must not pass, or a
    # render whose seed module went missing would still be green above.
    _install(git_render)
    # Recursive, as the gate's own `_modules()` and allium's walk are: a nested
    # module left behind would be checked, and the test would fail on exit 0.
    for module in (git_render.path / "docs" / "specs").rglob("*.allium"):
        module.unlink()
    result = run_tool(git_render, "run_allium", "check")
    assert result.returncode == 1, result.stdout + result.stderr
    assert "resolved no specification under docs/specs/" in result.stderr
