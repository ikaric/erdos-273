/-
Numerical bound `D(83160) < 1` and the resulting verified corollary
`no_strict_admissible_cover_83160`.

Sibling to `formal/Erdos273/NumericalBound27720.lean`. The period
`83160 = 2³ · 3³ · 5 · 7 · 11` strengthens the `L = 27720` result
by introducing the modulus `108 = 109 - 1` (and its multiples in
`M83160`) coming from the extra factor of `3`. Since
`27720 ∣ 83160`, the new content over the existing 27720 bound is
exactly the family of admissible moduli that are multiples of `108`
but still divide `83160`.

The set
  `M₈₃₁₆₀ = { m ∈ ℕ : m ∣ 83160, m + 1 prime, m + 1 ≥ 5 }`
has exactly `45` elements (computed from the divisor lattice of
`83160`; the parent has `(3+1)(3+1)(1+1)(1+1)(1+1) = 128` divisors)
and
  `∑_{m ∈ M₈₃₁₆₀} 1/m = 27241 / 27720 < 1`,
with slack `479 / 27720 ≈ 0.0173`.

Compared to `M27720`, the new elements are
`{108, 270, 378, 540, 756, 2376, 2970, 4158, 7560, 8316, 16632}` —
all of the form `m = 3^a · …` exploiting the additional factor of
`3` in `83160 / 27720 = 3`.

The whole file is `decide`-based: the kernel evaluates both
`Nat.divisors 83160` (128 divisors) and primality of each `m + 1`
for `m ∣ 83160`. We crank `maxRecDepth` and `maxHeartbeats` because
the reductions are deep but finite. The largest primality check is
on `83161` (trial divisions up to `√83161 ≈ 288`), which is roughly
`1.3×` the cost of the 27720 case and well within the kernel-decide
envelope. No `native_decide` is used — the proofs therefore depend
only on the three Lean foundational axioms.
-/
import «Erdos273».CoveringSystem
import «Erdos273».IntegerForm
import Mathlib

namespace «Erdos273»

open Classical

/-- Explicit enumeration of the 45 admissible divisors of `83160`.

The list is the set of `m` such that `m ∣ 83160`, `m + 1` is prime,
and `m + 1 ≥ 5`, computed from the divisor lattice of
`83160 = 2³ · 3³ · 5 · 7 · 11`. The list is sorted ascending.

Compared to `M27720`, the 11 new elements are
`{108, 270, 378, 540, 756, 2376, 2970, 4158, 7560, 8316, 16632}` —
all multiples of `108 = 109 − 1`, which becomes admissible because
`83160` carries `3³` (and `27720` only `3²`). -/
def M83160 : Finset ℕ :=
  ({4, 6, 10, 12, 18, 22, 28, 30, 36, 40, 42, 60, 66, 70, 72, 88, 108,
    126, 180, 198, 210, 270, 280, 330, 378, 396, 420, 462, 540, 616,
    630, 660, 756, 990, 1320, 2310, 2376, 2520, 2970, 4158, 4620, 7560,
    8316, 9240, 16632} : Finset ℕ)

/-- Every element of `M83160` divides `83160`. -/
theorem M83160_dvd : ∀ m ∈ M83160, m ∣ 83160 := by decide

/-- Every element of `M83160` is at least `2` (in fact, at least `4`). -/
theorem M83160_ge_two : ∀ m ∈ M83160, 2 ≤ m := by decide

/-- The cardinality of `M83160` is `45`. -/
theorem M83160_card : M83160.card = 45 := by decide

set_option maxHeartbeats 20000000 in
set_option maxRecDepth 100000 in
/-- `M83160` is exactly the set of admissible divisors of `83160`, computed
via `Nat.divisors`. We use a higher `maxRecDepth` and `maxHeartbeats`
because the kernel must evaluate `Nat.divisors 83160` (a 128-element
Finset) and the primality of `m + 1` for each candidate `m`. -/
theorem M83160_eq_filter_divisors :
    M83160 = (Nat.divisors 83160).filter (fun m => (m + 1).Prime ∧ 4 ≤ m) := by
  decide

set_option maxHeartbeats 20000000 in
set_option maxRecDepth 100000 in
/-- Every element of `M83160` is an admissible modulus. Membership in
the explicit Finset is decidable; `Nat.Prime (m+1)` is verified for each
of the 45 cases by kernel reduction. -/
theorem M83160_admissible : ∀ m ∈ M83160, AdmissibleModulus m := by
  intro m hm
  rw [admissibleModulus_iff]
  -- The implication `m ∈ M83160 → 5 ≤ m + 1 ∧ (m + 1).Prime` is a
  -- decidable proposition over a finite set.
  revert hm
  revert m
  decide

/-- The key numerical inequality: `D(83160) = ∑_{m ∈ M83160} 1/m =
27241/27720 < 1`. The proof unfolds `M83160` to a concrete sequence of
`Finset.insert`s, then evaluates the rational sum by `norm_num`. -/
theorem D83160_lt_one : ∑ m ∈ M83160, (1 : ℚ) / m < 1 := by
  unfold M83160
  norm_num [Finset.sum_insert, Finset.mem_insert, Finset.sum_singleton]

/-- The reverse-direction bridge: any admissible divisor of `83160` is
in `M83160`. This is the contrapositive of the filter equality
`M83160_eq_filter_divisors`. -/
theorem mem_M83160_of_admissible_dvd
    (m : ℕ) (hadm : AdmissibleModulus m) (hdvd : m ∣ 83160) : m ∈ M83160 := by
  rw [admissibleModulus_iff] at hadm
  obtain ⟨h5, hp⟩ := hadm
  have hm_in : m ∈ Nat.divisors 83160 := by
    rw [Nat.mem_divisors]
    exact ⟨hdvd, by norm_num⟩
  rw [M83160_eq_filter_divisors, Finset.mem_filter]
  exact ⟨hm_in, hp, by omega⟩

/-- **Verified numerical corollary.** No strict covering of
`ℤ/83160ℤ` by progressions with admissible moduli dividing `83160`
exists.

Strengthens `no_strict_admissible_cover_27720` by introducing the
admissible modulus `108 = 109 - 1` (and its multiples in `M83160`)
that become available once the period carries `3³` instead of just
`3²`. Since `27720 ∣ 83160`, this strictly contains the previous
obstruction: any strict admissible cover with all moduli dividing
`27720` also has all moduli dividing `83160` (and is thus excluded
by the present theorem), and additionally we now rule out covers
that use moduli like `108, 270, 378, 540, 756, 2376, 2970, 4158,
7560, 8316, 16632` that divide `83160` but not `27720`.

The argument is: take `M := M83160`; every `c.modulus` lies in `M`
by hypothesis; `D(83160) = 27241/27720 < 1` discharges the density
inequality; conclude via `no_strict_cover_of_low_density`. -/
theorem no_strict_admissible_cover_83160 :
    ¬ ∃ (S : Finset ResidueClass),
        (∀ c ∈ S, AdmissibleModulus c.modulus ∧ c.modulus ∣ 83160) ∧
        (S.image ResidueClass.modulus).card = S.card ∧
        (∀ i : ℕ, i < 83160 → ∃ c ∈ S, (i : ℤ) ∈ c.toSet) := by
  rintro ⟨S, hSmod, hStrict, hcov⟩
  -- Each `c.modulus` lies in `M83160` because it's admissible and
  -- divides `83160`.
  have hSmem : ∀ c ∈ S, c.modulus ∈ M83160 := by
    intros c hc
    have hadm := hSmod c hc
    exact mem_M83160_of_admissible_dvd c.modulus hadm.1 hadm.2
  exact no_strict_cover_of_low_density 83160 (by norm_num) M83160
    M83160_ge_two M83160_dvd D83160_lt_one
    ⟨S, hSmem, hStrict, hcov⟩

/-! ## ℤ-form of the obstruction (mirrors `IntegerForm.lean` for 27720). -/

/-- **ℤ-form of the L = 83160 obstruction.**

No strict covering of `ℤ` by residue classes with admissible moduli
all dividing `83160` exists. This is the integer-form restatement
of `no_strict_admissible_cover_83160`, phrased over all of `ℤ`
instead of the finite range `[0, 83160)`. The bridge is
`covers_int_iff_covers_range_L` (already in `IntegerForm.lean`).

The statement is the precise analogue of
`no_strict_admissible_covering_Z_27720`, and the proof is the same
template with `27720` replaced by `83160`. -/
theorem no_strict_admissible_covering_Z_83160 :
    ¬ ∃ (C : CoveringSystem),
        C.IsStrict ∧
        ∀ c ∈ C.classes, AdmissibleModulus c.modulus ∧ c.modulus ∣ 83160 := by
  rintro ⟨C, hStrict, hSmod⟩
  -- Extract the divisibility hypothesis as a standalone statement.
  have hdvd : ∀ c ∈ C.classes, c.modulus ∣ 83160 := fun c hc => (hSmod c hc).2
  -- The global `C.covers` hypothesis says every `n : ℤ` is covered.
  have hcovZ : ∀ n : ℤ, ∃ c ∈ C.classes, n ∈ c.toSet := C.covers
  -- Apply the equivalence (forward direction) to get the range form.
  have hcovL : ∀ i : ℕ, i < 83160 → ∃ c ∈ C.classes, (i : ℤ) ∈ c.toSet :=
    (covers_int_iff_covers_range_L C.classes 83160 (by norm_num) hdvd).mp hcovZ
  -- Now `no_strict_admissible_cover_83160` closes the loop.
  exact no_strict_admissible_cover_83160
    ⟨C.classes, hSmod, hStrict, hcovL⟩

end «Erdos273»

-- Acceptance checks. Per project policy, the verified theorems must
-- depend only on `propext`, `Classical.choice`, `Quot.sound`. No
-- `sorryAx`, no `Lean.ofReduceBool` (no `native_decide`), no
-- project-local `axiom` declarations.
#print axioms «Erdos273».D83160_lt_one
#print axioms «Erdos273».M83160_eq_filter_divisors
#print axioms «Erdos273».M83160_admissible
#print axioms «Erdos273».mem_M83160_of_admissible_dvd
#print axioms «Erdos273».no_strict_admissible_cover_83160
#print axioms «Erdos273».no_strict_admissible_covering_Z_83160
