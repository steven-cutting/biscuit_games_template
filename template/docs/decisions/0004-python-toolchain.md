---
title: "Decision 0004: A Python toolchain in a frontend repository"
kind: "decision"
audience: [maintainer, agent]
canonical_for: [decision_python_toolchain]
requires: []
---

# Decision 0004: A Python toolchain in a frontend repository

Carried from Poodl's decision 0004. A small Python toolchain of `uv`, `prek` and `ruff`
runs the hook gate and the two validators in a repository whose application is
TypeScript. The record will weigh the cost of a second language runtime against the
value of the gate it provides, and say what would justify replacing it.
