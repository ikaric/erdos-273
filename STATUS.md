# Status

Current focus: V3 advanced + density divergence verified. This
session: (1) verified `admissible_reciprocal_not_summable`
(∑_{m∈𝓜}1/m=∞, DensityDivergence.lean) — formalizes why density is
capped; (2) V3 CFT engine VALIDATED (squarefree reproduces CFT's
0.99938506 to 8 sig figs), but the naive 𝓜-specialization disproved
(per-coordinate-weight substitution over-reaches). Next V3 step
(analyst): the hyperplane-restriction count — put 1/(p-1) on the
count of admissible hyperplanes (Siegel–Walfisz), feed the validated
engine. V2 (#4) recommended for retirement (both BBMST levers dead
for 𝓜).

Last commit: density-divergence promotion + V3 CFT findings + PDF.

Blocker: V3 hyperplane count is a multi-session analyst task; density
method is provably capped (verified), so V3 is the only forward lever.

Problem: Covering systems with moduli of the form $p-1$, $p \geq 5$ prime (Erdős Problem #273).
