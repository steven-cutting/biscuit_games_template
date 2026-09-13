"""The specification gate the render ships, run inside a render.

`scripts/run_allium.py` refuses an empty `docs/specs/` (its `NO_INPUTS`), so a
green `check` and `analyse` is also the proof that the seed module exists and
parses. Subprocess rather than `runpy`, because `run_allium.py` imports
`install_allium` as a sibling and needs an interpreter started in the render.

Network: `install_allium.py` downloads the pinned binary, about 1.6 MB and
checksummed, into `<render>/.tools/bin`, once per render. The `network` marker
is enabled by `BISCUIT_TEMPLATE_NETWORK=1`; without it every test here is
skipped.
"""

from __future__ import annotations

import pytest

from tests.helpers import Render, run_script


def _install(render: Render) -> None:
    install = run_script(render, "install_allium.py")
    assert install.returncode == 0, install.stdout + install.stderr


@pytest.mark.network
def test_seed_module_is_clean(git_render: Render) -> None:
    _install(git_render)
    for command in ("check", "analyse"):
        result = run_script(git_render, "run_allium.py", command)
        assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.network
def test_gate_refuses_an_empty_specs_directory(git_render: Render) -> None:
    # The negative control: a gate that read nothing must not pass, or a
    # render whose seed module went missing would still be green above.
    _install(git_render)
    for module in (git_render.path / "docs" / "specs").glob("*.allium"):
        module.unlink()
    result = run_script(git_render, "run_allium.py", "check")
    assert result.returncode == 1, result.stdout + result.stderr
    assert "resolved no specification under docs/specs/" in result.stderr
