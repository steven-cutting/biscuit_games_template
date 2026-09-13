---
title: "Architecture"
kind: "explanation"
audience: [contributor, maintainer, operator, agent]
canonical_for: [system_architecture]
requires: []
---

# Architecture

How a static site with no server is put together. The page follows a visit from the
prerendered HTML through hydration, shows where the platform package ends and this game
begins, and explains why every side effect sits behind a port: three here for storage,
the clock and randomness, and two the platform exports for device preferences and the
keyboard. It closes on what the build uploads.
