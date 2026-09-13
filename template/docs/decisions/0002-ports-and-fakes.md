---
title: "Decision 0002: Side effects behind ports"
kind: "decision"
audience: [contributor, maintainer, agent]
canonical_for: [decision_ports_and_fakes]
requires: []
---

# Decision 0002: Side effects behind ports

Carried from Poodl's decision 0002. Every side effect is reached through a port with an
in-memory fake, so tests inject fakes and never stub a global. The record will name the
boundaries a new game starts with, which are storage, the clock and randomness, plus the
device preferences and keyboard the platform exports, and what the indirection costs.
