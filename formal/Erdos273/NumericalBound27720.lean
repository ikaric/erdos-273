/-
Numerical bound `D(27720) < 1` and the resulting verified corollary
`no_strict_admissible_cover_27720`.

Companion to `formal/Erdos273/CoveringSystem.lean`, which states the
abstract obstruction `no_strict_cover_of_low_density` and the
*sketch* corollary `no_strict_admissible_cover_27720` (one isolated
`sorry` on this very inequality).

The set
  `M₂₇₇₂₀ = { m ∈ ℕ : m ∣ 27720, m + 1 prime, m + 1 ≥ 5 }`
has exactly `34` elements (computed from the divisor lattice of
`27720 = 2³ · 3² · 5 · 7 · 11`) and
  `∑_{m ∈ M₂₇₇₂₀} 1/m = 953 / 990 < 1.`

The whole file is `decide`-based: the kernel evaluates both
`Nat.divisors 27720` (a `Nat.Prime`-aware filter giving the 96 divisors)
and primality of each `m + 1` for `m ∣ 27720`. We crank `maxRecDepth`
and `maxHeartbeats` because the reductions are deep but finite. No
`native_decide` is used — the proofs therefore depend only on the three
Lean foundational axioms.
-/
import «Erdos273».CoveringSystem
import Mathlib

namespace «Erdos273»

open Classical

/-- Explicit enumeration of the 34 admissible divisors of `27720`.

The list is the set of `m` such that `m ∣ 27720`, `m + 1` is prime,
and `m + 1 ≥ 5`, computed from the divisor lattice of
`27720 = 2³ · 3² · 5 · 7 · 11`. The list is sorted ascending. -/
def M27720 : Finset ℕ :=
  ({4, 6, 10, 12, 18, 22, 28, 30, 36, 40, 42, 60, 66, 70, 72, 88, 126,
    180, 198, 210, 280, 330, 396, 420, 462, 616, 630, 660, 990, 1320,
    2310, 2520, 4620, 9240} : Finset ℕ)

/-- Every element of `M27720` divides `27720`. -/
theorem M27720_dvd : ∀ m ∈ M27720, m ∣ 27720 := by decide

/-- Every element of `M27720` is at least `2` (in fact, at least `4`). -/
theorem M27720_ge_two : ∀ m ∈ M27720, 2 ≤ m := by decide

/-- The cardinality of `M27720` is `34`. -/
theorem M27720_card : M27720.card = 34 := by decide

set_option maxHeartbeats 10000000 in
set_option maxRecDepth 100000 in
/-- `M27720` is exactly the set of admissible divisors of `27720`, computed
via `Nat.divisors`. We use a higher `maxRecDepth` and `maxHeartbeats`
because the kernel must evaluate `Nat.divisors 27720` (a 96-element
Finset) and the primality of `m + 1` for each candidate `m`. -/
theorem M27720_eq_filter_divisors :
    M27720 = (Nat.divisors 27720).filter (fun m => (m + 1).Prime ∧ 4 ≤ m) := by
  decide

set_option maxHeartbeats 10000000 in
set_option maxRecDepth 100000 in
/-- Every element of `M27720` is an admissible modulus. Membership in
the explicit Finset is decidable; `Nat.Prime (m+1)` is verified for each
of the 34 cases by kernel reduction. -/
theorem M27720_admissible : ∀ m ∈ M27720, AdmissibleModulus m := by
  intro m hm
  rw [admissibleModulus_iff]
  -- The implication `m ∈ M27720 → 5 ≤ m + 1 ∧ (m + 1).Prime` is a
  -- decidable proposition over a finite set.
  revert hm
  revert m
  decide

/-- The key numerical inequality: `D(27720) = ∑_{m ∈ M27720} 1/m =
953/990 < 1`. The proof unfolds `M27720` to a concrete sequence of
`Finset.insert`s, then evaluates the rational sum by `norm_num`. -/
theorem D27720_lt_one : ∑ m ∈ M27720, (1 : ℚ) / m < 1 := by
  unfold M27720
  norm_num [Finset.sum_insert, Finset.mem_insert, Finset.sum_singleton]

/-- The reverse-direction bridge: any admissible divisor of `27720` is
in `M27720`. This is the contrapositive of the filter equality
`M27720_eq_filter_divisors`. -/
theorem mem_M27720_of_admissible_dvd
    (m : ℕ) (hadm : AdmissibleModulus m) (hdvd : m ∣ 27720) : m ∈ M27720 := by
  rw [admissibleModulus_iff] at hadm
  obtain ⟨h5, hp⟩ := hadm
  have hm_in : m ∈ Nat.divisors 27720 := by
    rw [Nat.mem_divisors]
    exact ⟨hdvd, by norm_num⟩
  rw [M27720_eq_filter_divisors, Finset.mem_filter]
  exact ⟨hm_in, hp, by omega⟩

/-- **Verified numerical corollary.** No strict covering of
`ℤ/27720ℤ` by progressions with admissible moduli dividing `27720`
exists.

This is the headline numerical claim from the V1 SAT/density run.
Compared to `no_strict_admissible_cover_27720` (which is `[sketch]`
because of the trailing arithmetic `sorry`), the present theorem is
fully verified: its dependency chain contains only the three Lean
foundational axioms.

The argument is: take `M := M27720`; every `c.modulus` lies in `M`
by hypothesis; `D(27720) = 953/990 < 1` discharges the density
inequality; conclude via `no_strict_cover_of_low_density`. -/
theorem no_strict_admissible_cover_27720 :
    ¬ ∃ (S : Finset ResidueClass),
        (∀ c ∈ S, AdmissibleModulus c.modulus ∧ c.modulus ∣ 27720) ∧
        (S.image ResidueClass.modulus).card = S.card ∧
        (∀ i : ℕ, i < 27720 → ∃ c ∈ S, (i : ℤ) ∈ c.toSet) := by
  rintro ⟨S, hSmod, hStrict, hcov⟩
  -- Each `c.modulus` lies in `M27720` because it's admissible and
  -- divides `27720`.
  have hSmem : ∀ c ∈ S, c.modulus ∈ M27720 := by
    intros c hc
    have hadm := hSmod c hc
    exact mem_M27720_of_admissible_dvd c.modulus hadm.1 hadm.2
  exact no_strict_cover_of_low_density 27720 (by norm_num) M27720
    M27720_ge_two M27720_dvd D27720_lt_one
    ⟨S, hSmem, hStrict, hcov⟩

end «Erdos273»

-- Acceptance checks. Per project policy, the verified theorems must
-- depend only on `propext`, `Classical.choice`, `Quot.sound`. No
-- `sorryAx`, no `Lean.ofReduceBool` (no `native_decide`), no
-- project-local `axiom` declarations.
#print axioms «Erdos273».D27720_lt_one
#print axioms «Erdos273».M27720_eq_filter_divisors
#print axioms «Erdos273».M27720_admissible
#print axioms «Erdos273».mem_M27720_of_admissible_dvd
#print axioms «Erdos273».no_strict_admissible_cover_27720
