---
title: "Security model"
kind: "explanation"
audience: [user, contributor, maintainer, operator, agent]
canonical_for: [security_model]
requires: []
---

# Security model

What a site with no backend defends, and what it does not. The page sets out the threat
model for a static game served from GitHub Pages: no accounts, no server and no data
leaving the browser, dependencies pinned and locked, actions pinned by commit, workflow
permissions kept narrow, and secrets scanned in the gate. It is explicit about the risks
that remain inside the visitor's own browser.
