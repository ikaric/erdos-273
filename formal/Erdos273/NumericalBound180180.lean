/-
Numerical bound `D(180180) < 1` and the resulting verified corollary
`no_strict_admissible_cover_180180`.

Sibling to `formal/Erdos273/NumericalBound27720.lean`. The period
`180180 = 2² · 3² · 5 · 7 · 11 · 13` strengthens the `L = 27720`
result by introducing the prime `13` (and hence the admissible
modulus `52 = 53 - 1` and its multiples). Since `27720 ∤ 180180`,
the two obstructions constrain *different* families of admissible
strict covers — this is not subsumed by the `L = 83160` bound either.

The set
  `M₁₈₀₁₈₀ = { m ∈ ℕ : m ∣ 180180, m + 1 prime, m + 1 ≥ 5 }`
has exactly `47` elements (computed from the divisor lattice of
`180180`; the parent has `(2+1)(2+1)(1+1)(1+1)(1+1)(1+1) = 144`
divisors) and
  `∑_{m ∈ M₁₈₀₁₈₀} 1/m = 173003 / 180180 < 1`,
with slack `7177 / 180180 ≈ 0.0398`.

**Performance note.** As with `NumericalBound83160.lean`, the naive
`by decide` route (a `[1, 180181)` range scan to build
`Nat.divisors 180180`, then kernel `decide` of `Nat.Prime (m+1)` via
the `O(p)` instance on all `144` divisors) does not finish within a
sane budget. We instead compute the divisor lattice as the pointwise
product of the six small prime-power divisor sets via
`Nat.divisors_mul` applied to `180180 = 4 · 9 · 5 · 7 · 11 · 13`,
and discharge every primality obligation with `norm_num`. No
`native_decide` is used — the proofs depend only on the three Lean
foundational axioms.
-/
import «Erdos273».CoveringSystem
import «Erdos273».IntegerForm
import Mathlib

namespace «Erdos273»

open Classical
open scoped Pointwise

/-- Explicit enumeration of the 47 admissible divisors of `180180`.

The list is the set of `m` such that `m ∣ 180180`, `m + 1` is prime,
and `m + 1 ≥ 5`, computed from the divisor lattice of
`180180 = 2² · 3² · 5 · 7 · 11 · 13`. The list is sorted ascending.

Compared to `M27720`, the new elements are
`{52, 78, 130, 156, 546, 858, 910, 1092, 1170, 2002, 2340, 2730,
2860, 6006, 8190, 8580, 16380, 20020, 25740, 36036, 180180}` —
all multiples of the new prime contribution `13` or of `52 = 53 - 1`. -/
def M180180 : Finset ℕ :=
  ({4, 6, 10, 12, 18, 22, 28, 30, 36, 42, 52, 60, 66, 70, 78, 126, 130,
    156, 180, 198, 210, 330, 396, 420, 462, 546, 630, 660, 858, 910,
    990, 1092, 1170, 2002, 2310, 2340, 2730, 2860, 4620, 6006, 8190,
    8580, 16380, 20020, 25740, 36036, 180180} : Finset ℕ)

/-- Every element of `M180180` divides `180180`. -/
theorem M180180_dvd : ∀ m ∈ M180180, m ∣ 180180 := by decide

/-- Every element of `M180180` is at least `2` (in fact, at least `4`). -/
theorem M180180_ge_two : ∀ m ∈ M180180, 2 ≤ m := by decide

/-- The cardinality of `M180180` is `47`. -/
theorem M180180_card : M180180.card = 47 := by decide

/-- The 144 explicit divisors of `180180 = 2² · 3² · 5 · 7 · 11 · 13`,
sorted ascending. -/
def D180180 : Finset ℕ :=
  ({1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 18, 20, 21, 22, 26,
    28, 30, 33, 35, 36, 39, 42, 44, 45, 52, 55, 60, 63, 65, 66, 70, 77,
    78, 84, 90, 91, 99, 105, 110, 117, 126, 130, 132, 140, 143, 154,
    156, 165, 180, 182, 195, 198, 210, 220, 231, 234, 252, 260, 273,
    286, 308, 315, 330, 364, 385, 390, 396, 420, 429, 455, 462, 468,
    495, 546, 572, 585, 630, 660, 693, 715, 770, 780, 819, 858, 910,
    924, 990, 1001, 1092, 1155, 1170, 1260, 1287, 1365, 1386, 1430,
    1540, 1638, 1716, 1820, 1980, 2002, 2145, 2310, 2340, 2574, 2730,
    2772, 2860, 3003, 3276, 3465, 4004, 4095, 4290, 4620, 5005, 5148,
    5460, 6006, 6435, 6930, 8190, 8580, 9009, 10010, 12012, 12870,
    13860, 15015, 16380, 18018, 20020, 25740, 30030, 36036, 45045,
    60060, 90090, 180180} : Finset ℕ)

set_option maxHeartbeats 4000000 in
set_option maxRecDepth 100000 in
/-- The divisor set of `180180` equals the explicit list `D180180`,
computed as the pointwise product of the six prime-power divisor sets
via `Nat.divisors_mul` on `180180 = 4 · 9 · 5 · 7 · 11 · 13`. No
`[1, 180181)` range scan, no primality checks. -/
theorem divisors_180180_eq : Nat.divisors 180180 = D180180 := by
  rw [show (180180 : ℕ) = 4 * 9 * 5 * 7 * 11 * 13 from by norm_num,
      Nat.divisors_mul, Nat.divisors_mul, Nat.divisors_mul,
      Nat.divisors_mul, Nat.divisors_mul]
  decide

set_option maxHeartbeats 4000000 in
/-- Every element of `M180180` is an admissible modulus. `fin_cases`
splits into the 47 concrete moduli; `norm_num` discharges each
primality obligation. -/
theorem M180180_admissible : ∀ m ∈ M180180, AdmissibleModulus m := by
  intro m hm
  rw [admissibleModulus_iff]
  fin_cases hm <;> norm_num

/-- The key numerical inequality: `D(180180) = ∑_{m ∈ M180180} 1/m =
173003/180180 < 1`. -/
theorem D180180_lt_one : ∑ m ∈ M180180, (1 : ℚ) / m < 1 := by
  unfold M180180
  norm_num [Finset.sum_insert, Finset.mem_insert, Finset.sum_singleton]

set_option maxHeartbeats 4000000 in
set_option maxRecDepth 100000 in
/-- The reverse-direction bridge: any admissible divisor of `180180`
is in `M180180`. Routes through the explicit divisor list `D180180`;
`fin_cases` splits into the 144 divisors, each closed by membership
(`decide`), the `4 ≤ m` hypothesis (`omega`), or composite `m + 1`
contradicting the primality hypothesis (`norm_num`). -/
theorem mem_M180180_of_admissible_dvd
    (m : ℕ) (hadm : AdmissibleModulus m) (hdvd : m ∣ 180180) : m ∈ M180180 := by
  rw [admissibleModulus_iff] at hadm
  obtain ⟨h5, hp⟩ := hadm
  have h4 : 4 ≤ m := by omega
  have hmem : m ∈ Nat.divisors 180180 :=
    Nat.mem_divisors.mpr ⟨hdvd, by norm_num⟩
  rw [divisors_180180_eq] at hmem
  fin_cases hmem <;>
    first
      | (exact by decide)
      | omega
      | (exact absurd hp (by norm_num))

/-- **Verified numerical corollary.** No strict covering of
`ℤ/180180ℤ` by progressions with admissible moduli dividing `180180`
exists.

Strengthens `no_strict_admissible_cover_27720` by introducing the
prime `13` (and the admissible modulus `52 = 53 - 1` together with
its multiples in `M180180`). Since `27720 ∤ 180180`, this is not
subsumed by the previous bounds — the two obstructions constrain
different families of strict admissible covers.

The argument is: take `M := M180180`; every `c.modulus` lies in `M`
by hypothesis; `D(180180) = 173003/180180 < 1` discharges the
density inequality; conclude via `no_strict_cover_of_low_density`. -/
theorem no_strict_admissible_cover_180180 :
    ¬ ∃ (S : Finset ResidueClass),
        (∀ c ∈ S, AdmissibleModulus c.modulus ∧ c.modulus ∣ 180180) ∧
        (S.image ResidueClass.modulus).card = S.card ∧
        (∀ i : ℕ, i < 180180 → ∃ c ∈ S, (i : ℤ) ∈ c.toSet) := by
  rintro ⟨S, hSmod, hStrict, hcov⟩
  have hSmem : ∀ c ∈ S, c.modulus ∈ M180180 := by
    intros c hc
    have hadm := hSmod c hc
    exact mem_M180180_of_admissible_dvd c.modulus hadm.1 hadm.2
  exact no_strict_cover_of_low_density 180180 (by norm_num) M180180
    M180180_ge_two M180180_dvd D180180_lt_one
    ⟨S, hSmem, hStrict, hcov⟩

/-! ## ℤ-form of the obstruction (mirrors `IntegerForm.lean` for 27720). -/

/-- **ℤ-form of the L = 180180 obstruction.**

No strict covering of `ℤ` by residue classes with admissible moduli
all dividing `180180` exists. The integer-form restatement of
`no_strict_admissible_cover_180180`, via the bridge
`covers_int_iff_covers_range_L` (in `IntegerForm.lean`). -/
theorem no_strict_admissible_covering_Z_180180 :
    ¬ ∃ (C : CoveringSystem),
        C.IsStrict ∧
        ∀ c ∈ C.classes, AdmissibleModulus c.modulus ∧ c.modulus ∣ 180180 := by
  rintro ⟨C, hStrict, hSmod⟩
  have hdvd : ∀ c ∈ C.classes, c.modulus ∣ 180180 := fun c hc => (hSmod c hc).2
  have hcovZ : ∀ n : ℤ, ∃ c ∈ C.classes, n ∈ c.toSet := C.covers
  have hcovL : ∀ i : ℕ, i < 180180 → ∃ c ∈ C.classes, (i : ℤ) ∈ c.toSet :=
    (covers_int_iff_covers_range_L C.classes 180180 (by norm_num) hdvd).mp hcovZ
  exact no_strict_admissible_cover_180180
    ⟨C.classes, hSmod, hStrict, hcovL⟩

end «Erdos273»

-- Acceptance checks. Per project policy, the verified theorems must
-- depend only on `propext`, `Classical.choice`, `Quot.sound`. No
-- `sorryAx`, no `Lean.ofReduceBool` (no `native_decide`), no
-- project-local `axiom` declarations.
#print axioms «Erdos273».divisors_180180_eq
#print axioms «Erdos273».D180180_lt_one
#print axioms «Erdos273».M180180_admissible
#print axioms «Erdos273».mem_M180180_of_admissible_dvd
#print axioms «Erdos273».no_strict_admissible_cover_180180
#print axioms «Erdos273».no_strict_admissible_covering_Z_180180
