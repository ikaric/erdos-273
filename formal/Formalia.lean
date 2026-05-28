import Mathlib

/-!
# Formalia — formal proofs

Root module for the Formalia clone's formal-proof library. Per-concept files
live under `Formalia/` and are imported here as a convenience for tooling
(`exact?`, `apply?`, `loogle`) that benefits from the umbrella import.

`/target` rewrites this file's namespace and the parallel directory at
bootstrap to match the clone's `<DisplayName>`. In the template state,
this file imports Mathlib only and exposes no Formalia-specific content.
-/
