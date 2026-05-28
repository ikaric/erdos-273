# Status

Current focus: V5 closed — two verified density strengthenings landed
this session. L=83160 (strictly strengthens 27720) and L=180180
(independent, introduces prime 13) are both axiom-clean and promoted.
Key fix: replaced the pathological kernel `decide` (range scan +
O(p) primality) with `Nat.divisors_mul` + `norm_num` — now the
standard recipe (builds ~2–4 min, not >20 min/OOM). Next: V3 (#5)
CFT/distortion δ_j optimization for 𝓜 — the only lever toward the
full problem (density alone is Mertens-capped); first debug the
squarefree sanity check (loose tail at N=200). V2 (#4) recommended
for retirement (BBMST levers dead for 𝓜).

Last commit: 6c21aa9 pdf: rebuild after L=180180 promotion.

Blocker: none.

Problem: Covering systems with moduli of the form $p-1$, $p \geq 5$ prime (Erdős Problem #273).
