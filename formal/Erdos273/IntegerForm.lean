/-
ℤ-form of the L = 27720 obstruction for Erdős Problem #273.

The companion file `Erdos273/NumericalBound27720.lean` proves
`no_strict_admissible_cover_27720`: no strict covering of the
*finite range* `[0, 27720)` by residue classes with admissible
moduli dividing 27720 exists.

In the manuscript, however, we phrase the obstruction in terms of
covering all of `ℤ`. The bridge is a standard lift: if all moduli
divide `L`, then a finite family of residue classes covers `ℤ`
iff it covers `[0, L)`. The lemma `covers_int_iff_covers_range_L`
below makes this precise; the resulting integer-form theorem
`no_strict_admissible_covering_Z_27720` follows immediately.

Both new theorems are fully `[verified]`: their dependency chains
contain only the three Lean foundational axioms (`propext`,
`Classical.choice`, `Quot.sound`).
-/
import «Erdos273».CoveringSystem
import «Erdos273».NumericalBound27720
import Mathlib

namespace «Erdos273»

open Classical

/-- **Equivalence: covering `ℤ` ↔ covering `[0, L)`.**

For any finite family `S` of residue classes whose moduli all divide
`L ≥ 1`, the family covers all of `ℤ` if and only if it covers every
integer in `[0, L)`.

This is the lift used everywhere in the covering-systems literature
to pass between the "global" formulation (cover `ℤ`) and the "local"
formulation (cover the finite quotient `ℤ/Lℤ`, represented as
`[0, L) ⊆ ℕ`). The proof is elementary: forward is specialization;
backward replaces an integer `n` by its reduced representative
`r = (n % L).toNat ∈ [0, L)` and uses `c.modulus ∣ L` to transport
the mod-L congruence to a mod-`c.modulus` congruence. -/
theorem covers_int_iff_covers_range_L
    (S : Finset ResidueClass) (L : ℕ) (hL : 1 ≤ L)
    (hdvd : ∀ c ∈ S, c.modulus ∣ L) :
    (∀ n : ℤ, ∃ c ∈ S, n ∈ c.toSet) ↔
    (∀ i : ℕ, i < L → ∃ c ∈ S, (i : ℤ) ∈ c.toSet) := by
  refine ⟨?_, ?_⟩
  · -- Forward: specialize `n` to `(i : ℤ)` for `i ∈ [0, L)`.
    intro h i _
    exact h (i : ℤ)
  · -- Backward: pick the reduced representative `r := (n % L).toNat`.
    intro h n
    -- `L > 0` as an integer.
    have hLposℤ : (0 : ℤ) < L := by exact_mod_cast hL
    -- `0 ≤ n % L` and `n % L < L`.
    have hmod_nonneg : 0 ≤ n % (L : ℤ) := Int.emod_nonneg n (by exact_mod_cast hLposℤ.ne')
    have hmod_lt : n % (L : ℤ) < (L : ℤ) := Int.emod_lt_of_pos n hLposℤ
    -- The natural-number representative `r := (n % L).toNat`.
    set r : ℕ := (n % (L : ℤ)).toNat with hr_def
    -- `(r : ℤ) = n % L` because `0 ≤ n % L`.
    have hr_cast : (r : ℤ) = n % (L : ℤ) := by
      rw [hr_def]; exact Int.toNat_of_nonneg hmod_nonneg
    -- `r < L` as a natural number.
    have hrL : r < L := by
      have : (r : ℤ) < (L : ℤ) := by rw [hr_cast]; exact hmod_lt
      exact_mod_cast this
    -- Apply the range hypothesis at `r`.
    obtain ⟨c, hcS, hcmem⟩ := h r hrL
    refine ⟨c, hcS, ?_⟩
    -- Now translate the membership `(r : ℤ) ∈ c.toSet` to `n ∈ c.toSet`.
    -- Strategy: show `n ≡ r [ZMOD c.modulus]` and combine with
    -- `(r : ZMod c.modulus) = c.residue` (which is `hcmem`).
    have hcdvdℤ : (c.modulus : ℤ) ∣ (L : ℤ) := by exact_mod_cast hdvd c hcS
    -- `n % L ≡ n [ZMOD L]` always; from that, `n % L ≡ n [ZMOD c.modulus]`
    -- because `c.modulus ∣ L`.
    have hcongL : n % (L : ℤ) ≡ n [ZMOD (L : ℤ)] := Int.mod_modEq n (L : ℤ)
    have hcong_m : n % (L : ℤ) ≡ n [ZMOD (c.modulus : ℤ)] :=
      hcongL.of_dvd hcdvdℤ
    -- Rewrite `n % L` as `(r : ℤ)`.
    have hcong_rn : (r : ℤ) ≡ n [ZMOD (c.modulus : ℤ)] := by
      rw [hr_cast]; exact hcong_m
    -- Convert the congruence to a ZMod equality.
    have hZMod : ((r : ℤ) : ZMod c.modulus) = (n : ZMod c.modulus) :=
      (ZMod.intCast_eq_intCast_iff _ _ _).mpr hcong_rn
    -- The membership `(r : ℤ) ∈ c.toSet` unfolds to `((r : ℤ) : ZMod m) = c.residue`.
    rw [ResidueClass.mem_toSet] at hcmem ⊢
    -- Conclude `(n : ZMod m) = c.residue` by transitivity.
    rw [← hZMod]; exact hcmem

/-- **ℤ-form of the L = 27720 obstruction.**

No strict covering of `ℤ` by residue classes with admissible moduli
all dividing 27720 exists. This is the integer-form restatement of
`no_strict_admissible_cover_27720`, which is phrased over the finite
range `[0, 27720)`. The bridge is `covers_int_iff_covers_range_L`.

This is the precise statement used in the manuscript: it captures
the "global" obstruction that the SAT/density argument really
proves, namely that any *strict admissible* covering of `ℤ` must
use at least one modulus that does not divide 27720. -/
theorem no_strict_admissible_covering_Z_27720 :
    ¬ ∃ (C : CoveringSystem),
        C.IsStrict ∧
        ∀ c ∈ C.classes, AdmissibleModulus c.modulus ∧ c.modulus ∣ 27720 := by
  rintro ⟨C, hStrict, hSmod⟩
  -- Extract the divisibility hypothesis as a standalone statement.
  have hdvd : ∀ c ∈ C.classes, c.modulus ∣ 27720 := fun c hc => (hSmod c hc).2
  -- The global `C.covers` hypothesis says every `n : ℤ` is covered.
  have hcovZ : ∀ n : ℤ, ∃ c ∈ C.classes, n ∈ c.toSet := C.covers
  -- Apply the equivalence (forward direction) to get the range form.
  have hcovL : ∀ i : ℕ, i < 27720 → ∃ c ∈ C.classes, (i : ℤ) ∈ c.toSet :=
    (covers_int_iff_covers_range_L C.classes 27720 (by norm_num) hdvd).mp hcovZ
  -- Now `no_strict_admissible_cover_27720` closes the loop.
  exact no_strict_admissible_cover_27720
    ⟨C.classes, hSmod, hStrict, hcovL⟩

/-- **Corollary (modulus must escape 27720).**

If Erdős Problem #273 *can* be settled affirmatively — i.e., a
strict covering of `ℤ` by residue classes with all moduli of the
form `p − 1` for primes `p ≥ 5` exists — then any such covering
must use at least one modulus that does not divide 27720.

This is the contrapositive packaging of
`no_strict_admissible_covering_Z_27720` against
`Erdos273Conjecture`. -/
theorem erdos273_modulus_not_dividing_27720 :
    Erdos273Conjecture → ∃ C : CoveringSystem, C.IsStrict ∧
        C.SolvesErdos273 ∧ ∃ c ∈ C.classes, ¬ c.modulus ∣ 27720 := by
  rintro ⟨C, hStrict, hSolves⟩
  refine ⟨C, hStrict, hSolves, ?_⟩
  -- Suppose, for contradiction, that *every* modulus in `C` divides 27720.
  by_contra hAll
  push Not at hAll
  -- Combine `hSolves` (admissibility) with `hAll` (divisibility).
  have hPair : ∀ c ∈ C.classes, AdmissibleModulus c.modulus ∧ c.modulus ∣ 27720 := by
    intros c hc
    refine ⟨?_, hAll c hc⟩
    -- Admissibility comes from `hSolves`.
    obtain ⟨p, hp, hp5, hpm⟩ := hSolves c hc
    exact ⟨p, hp, hp5, hpm⟩
  -- This contradicts `no_strict_admissible_covering_Z_27720`.
  exact no_strict_admissible_covering_Z_27720 ⟨C, hStrict, hPair⟩

end «Erdos273»

-- Acceptance checks. Both headline theorems must depend only on the
-- three Lean foundational axioms (`propext`, `Classical.choice`,
-- `Quot.sound`) — no `sorryAx`, no `Lean.ofReduceBool`, no project-
-- local axioms. The corollary inherits the same dependency chain.
#print axioms «Erdos273».covers_int_iff_covers_range_L
#print axioms «Erdos273».no_strict_admissible_covering_Z_27720
#print axioms «Erdos273».erdos273_modulus_not_dividing_27720
