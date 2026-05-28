# Status

Current focus: HALTED — seeded attack complete (ROADMAP 6/6). The
conjecture is OPEN; 6/6 means all five seeded vectors are explored,
not that #273 is solved. This session closed V2 (#4) and V3 (#5) as
documented dead ends: the analyst proved the distortion method
(Hough/BBMST/CFT) cannot be sharpened for 𝓜 — the 1/(p-1) sparsity is
invisible to the distortion pattern-count (every prime-support pattern
is 𝓜-realizable by Dirichlet). Combined with the verified density
cap (∑1/m=∞), both known non-existence levers are exhausted.

Deliverables: 33 axiom-clean Lean theorems (density bound + 3 period
obstructions L=27720/83160/180180 + divergence); manuscript with the
proven distortion obstruction recorded.

Next (USER): run `/vector add` to seed a new direction — construction
search at D(L)≥1 periods, or the all-moduli-even structural lever
(𝓜⊂2ℤ≥4) — or `/polish` to finalize on the current verified state.
See findings/decision-halt-2026-05-29.md.

Last commit: session 6 end — V2+V3 closed as dead ends, halt to /vector.

Blocker: seeded non-existence vectors exhausted; new strategic posture
is a /vector (user) decision, not autonomous /solve scope.

Problem: Covering systems with moduli of the form $p-1$, $p \geq 5$ prime (Erdős Problem #273).
