/-
Divergence of the reciprocal sum over the admissible moduli.

The density obstruction proved in `CoveringSystem.lean` shows that a
strict covering with all moduli dividing a common period `L` forces
`∑_{m} 1/m ≥ 1`. This gives an unconditional non-existence statement
whenever the admissible divisors of `L` have reciprocal sum below `1`
(the `L = 27720, 83160, 180180` bounds). It cannot, however, settle
the full problem: the reciprocal sum over *all* admissible moduli
diverges, so for every threshold there are admissible moduli whose
reciprocals already exceed it. This file records that divergence.

`𝓜 = { p - 1 : p prime, p ≥ 5 }`. Indexing the moduli by their
witnessing prime, the reciprocal sum is `∑_{p} 1/(p - 1)` over primes
`p` (the terms `p = 2, 3` are finite and do not affect divergence).
We show this is not summable by comparison with `∑_{p} 1/p`, which
Mathlib knows diverges (`Nat.Primes.not_summable_one_div`).

This is the precise sense in which the elementary density method is
"capped": it is why the project must turn to the distortion method
(Hough 2015 / BBMST 2022 / CFT 2022) for any argument reaching beyond
the finitely many periods `L` with `D(L) < 1`.
-/
import Mathlib

namespace «Erdos273»

open scoped BigOperators

/-- The reciprocal sum over the admissible moduli `𝓜 = {p - 1 : p ≥ 5}`,
indexed by the witnessing prime, diverges: `∑_{p prime} 1/(p - 1)` is
not summable.

Proof by comparison with `∑_{p prime} 1/p`, which is not summable
(`Nat.Primes.not_summable_one_div`): for every prime `p` one has
`1/p ≤ 1/(p - 1)`, so summability of the larger series would force
summability of the smaller. -/
theorem admissible_reciprocal_not_summable :
    ¬ Summable (fun p : Nat.Primes ↦ (1 : ℝ) / ((p : ℝ) - 1)) := by
  intro h
  refine Nat.Primes.not_summable_one_div ?_
  refine h.of_nonneg_of_le (fun p => by positivity) (fun p => ?_)
  have hp2 : (2 : ℝ) ≤ (p : ℝ) := by exact_mod_cast p.property.two_le
  exact one_div_le_one_div_of_le (by linarith) (by linarith)

end «Erdos273»

-- Acceptance check: only the three Lean foundational axioms.
#print axioms «Erdos273».admissible_reciprocal_not_summable
