---
title: "Layering and dependency direction"
kind: "explanation"
audience: [contributor, maintainer, agent]
canonical_for: [dependency_boundaries]
requires: []
---

# Layering and dependency direction

Which module may import which, and why the direction matters. The page draws the layers
from routes and components down to the ports, places the platform package beneath all of
them, and states the rule that nothing lower reaches up. It counts five ports, three
defined here and two taken from the platform, and explains how a test replaces each one
with its fake.
