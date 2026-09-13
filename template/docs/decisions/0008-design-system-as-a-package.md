---
title: "Decision 0008: The design system arrives as a package"
kind: "decision"
audience: [contributor, maintainer, agent]
canonical_for: [decision_design_system_as_a_package]
requires: []
---

# Decision 0008: The design system arrives as a package

Carried from Poodl's decision 0013. The design system, with its components, tokens and
three specification modules, arrives as the pinned package
`@steven-cutting/biscuit-games` from GitHub Packages rather than being copied in. The
record will explain why a game starts with the package, how restated clauses are held
equal to it by test, and what an upgrade involves.
