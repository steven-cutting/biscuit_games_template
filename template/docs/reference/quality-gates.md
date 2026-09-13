---
title: "Quality gates"
kind: "reference"
audience: [contributor, maintainer, agent]
canonical_for: [quality_gate_reference]
requires: []
---

# Quality gates

Every check `just check` runs, in order, with what each one proves and what makes it
fail. The page tables the lockfile check, the hook gate, the documentation and agent
contracts, the specification gates, static analysis, unit tests with coverage, the build
and the story run, and states the one gate that reaches the network. It also records
what runs on `main` after a merge.
