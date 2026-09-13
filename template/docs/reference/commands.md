---
title: "Commands"
kind: "reference"
audience: [contributor, maintainer, operator, agent]
canonical_for: [command_reference]
requires: []
---

# Commands

Every recipe the `Justfile` offers, what it runs and what it must not change. The
`Justfile` is the only supported interface to the checks, so this page is the
reference for the whole gate: the setup recipes, the formatting recipes, each check
`just check` runs in order, and the recipes that serve the site or the workshop. It
is a managed page: the template rewrites it, and a game appends its own recipes below.
