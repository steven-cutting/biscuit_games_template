---
title: "Decision 0007: A project-managed Allium binary"
kind: "decision"
audience: [maintainer, agent]
canonical_for: [decision_allium_cli]
requires: []
---

# Decision 0007: A project-managed Allium binary

Carried from Poodl's decision 0011. The Allium checker is a binary this project manages
itself, pinned by version and checksum in `scripts/install_allium.py` and installed into
a gitignored directory by `just install-allium`. The record will explain why the gate
reads the reported diagnostics rather than trusting an exit code, and what a new pin
requires.
