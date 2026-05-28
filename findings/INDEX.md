# Findings index

Inter-agent notes drop here. Naming conventions:

- `lit-<topic>-<date>.md` — literature survey (librarian)
- `heur-<topic>-<date>.md` — heuristic / numerical (computationalist)
- `deadend-<topic>-<date>.md` — abandoned approach
- `openq-<topic>-<date>.md` — open question surfaced during work
- `review-<topic>-<date>.md` — critic adversarial review
- `decision-<topic>-<date>.md` — orchestrator decision recorded without user input
- `breakthrough-<topic>-<date>.md` — a genuine novel result
- `pivot-<date>.md` — strategic pivot ceremony (`/vector pivot`)

## Entries

- `lit-covering-2026-05-28.md` — librarian — foundational literature survey for Erdős #273 (covering systems with moduli $p-1$, $p\geq 5$). Maps the Hough/BBMST/CFT distortion-method literature, the 22 covering-system Erdős problems on Bloom's index, the Lean 4 `StrictCoveringSystem` type already in `google-deepmind/formal-conjectures` (a free upstream asset), the precise classical Selfridge construction context (6 of 14 moduli in the 120-divisor example already lie in $\mathcal{M}$; the gap is precisely the modulus 2), and a prioritized list of 5 next-step attack vectors plus 5 concrete sub-lemmas the formalist can attempt in one session.
- `heur-sat-2026-05-28.md` — computationalist — SAT encoding `formal/numerics/sat_covering.py` of the bounded-period strict-covering question for Erdős #273. Headline result: UNSAT confirmed for $L \in \{60, 120, 360, 840, 2520, 27720\}$ (by CaDiCaL for the first four, by density-bound counting for the latter two; CDCL times out where density succeeds). For $L \in \{360360, 720720\}$ the density bound no longer applies and both CaDiCaL and kissat fail to settle within reasonable timeouts. Manuscript claim: any Erdős #273 covering must use a modulus that does not divide $27720 = 2^3 \cdot 3^2 \cdot 5 \cdot 7 \cdot 11$. Includes the Lean pseudocode for `strict_covering_density_bound` — the single lemma needed to wire the SAT evidence into the manuscript.
