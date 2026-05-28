/-
Erdős Problem #273 — basic API.

We define the combinatorial objects that the rest of the project will
reason about:

* a single residue class `a (mod m)`,
* a covering system (a finite collection of residue classes whose union
  is `ℤ`),
* the *admissible modulus* predicate "`m = p - 1` for some prime
  `p ≥ 5`",
* the conjecture itself, as a `Prop`.

The Mathlib idiom for "the integer `n` lies in the class `a (mod m)`" is
`{n : ℤ | (n : ZMod m) = a}`, used for example in
`Mathlib.Analysis.SumOverResidueClass`. We follow the same convention.
-/
import Mathlib

namespace «Erdos273»

/-- A residue class `a (mod m)` with modulus at least `2`. The residue is
stored as an element of `ZMod m`, so it lives canonically in
`Fin m`. -/
structure ResidueClass where
  /-- The modulus of the residue class. -/
  modulus : ℕ
  /-- Moduli are at least `2`; the modulus `1` would collapse the class to
  all of `ℤ` and is pointless. -/
  hmod : 2 ≤ modulus
  /-- The residue, an element of `ZMod modulus`. -/
  residue : ZMod modulus

namespace ResidueClass

/-- Equality of residue classes is decidable.

Two residue classes are equal iff they have the same modulus and the
same residue (modulo that common modulus). -/
instance : DecidableEq ResidueClass
  | ⟨m₁, h₁, r₁⟩, ⟨m₂, h₂, r₂⟩ =>
    if hm : m₁ = m₂ then
      (by subst hm
          exact if hr : r₁ = r₂
            then isTrue (by subst hr; rfl)
            else isFalse (fun h => hr (by injection h)))
    else
      isFalse (fun h => hm (by injection h))

/-- The set of integers congruent to `c.residue` modulo `c.modulus`. -/
def toSet (c : ResidueClass) : Set ℤ :=
  { n : ℤ | (n : ZMod c.modulus) = c.residue }

@[simp] lemma mem_toSet (c : ResidueClass) (n : ℤ) :
    n ∈ c.toSet ↔ (n : ZMod c.modulus) = c.residue := Iff.rfl

end ResidueClass

/-- A *covering system* of `ℤ`: a finite collection of residue classes
whose union covers all integers. -/
structure CoveringSystem where
  /-- The (finite) collection of residue classes. -/
  classes : Finset ResidueClass
  /-- Every integer lies in at least one class. -/
  covers : ∀ n : ℤ, ∃ c ∈ classes, n ∈ c.toSet

namespace CoveringSystem

/-- A covering system *solves Erdős #273* if every modulus appearing in
it is of the form `p - 1` for some prime `p ≥ 5`. -/
def SolvesErdos273 (C : CoveringSystem) : Prop :=
  ∀ c ∈ C.classes, ∃ p : ℕ, p.Prime ∧ 5 ≤ p ∧ c.modulus = p - 1

end CoveringSystem

/-- A natural number is *admissible for Erdős #273* if it is of the form
`p - 1` for some prime `p ≥ 5`. -/
def AdmissibleModulus (m : ℕ) : Prop :=
  ∃ p : ℕ, p.Prime ∧ 5 ≤ p ∧ m = p - 1

/-- **Erdős Problem #273** (Erdős–Graham 1980): does there exist a
covering system of `ℤ` all of whose moduli are of the form `p - 1` for
some prime `p ≥ 5`? Stated as a `Prop`; the conjecture is to decide
whether this proposition holds. -/
def Erdos273Conjecture : Prop :=
  ∃ C : CoveringSystem, C.SolvesErdos273

/-! ## Auxiliary lemmas exercising the API. -/

/-- Membership in `AdmissibleModulus` is bounded above by `m + 1`: any
witness prime `p` satisfies `p = m + 1` and `p ≥ 5`. This lets us decide
`AdmissibleModulus m` by a bounded search. -/
lemma admissibleModulus_iff (m : ℕ) :
    AdmissibleModulus m ↔ 5 ≤ m + 1 ∧ (m + 1).Prime := by
  constructor
  · rintro ⟨p, hp, hp5, hpm⟩
    have hp1 : 1 ≤ p := hp.one_lt.le
    have hpeq : p = m + 1 := by omega
    refine ⟨?_, ?_⟩
    · omega
    · rw [← hpeq]; exact hp
  · rintro ⟨h5, hprime⟩
    exact ⟨m + 1, hprime, h5, by omega⟩

/-- `AdmissibleModulus` is a decidable predicate. -/
instance : DecidablePred AdmissibleModulus := fun m =>
  decidable_of_iff _ (admissibleModulus_iff m).symm

/-- The modulus `4` is admissible: take `p = 5`. -/
theorem admissibleModulus_four : AdmissibleModulus 4 := by
  refine ⟨5, ?_, le_refl 5, by norm_num⟩
  decide

/-- Any admissible modulus is at least `4` (because the smallest prime
`p ≥ 5` is `5`, giving `p - 1 = 4`). -/
theorem four_le_of_admissible {m : ℕ} (h : AdmissibleModulus m) : 4 ≤ m := by
  obtain ⟨p, _hp, hp5, hpm⟩ := h
  omega

/-- The smallest admissible modulus is `4`. -/
theorem smallest_admissible_modulus_is_four :
    AdmissibleModulus 4 ∧ ∀ m, AdmissibleModulus m → 4 ≤ m :=
  ⟨admissibleModulus_four, fun _ => four_le_of_admissible⟩

/-- The admissible moduli below `60` are exactly
`{4, 6, 10, 12, 16, 18, 22, 28, 30, 36, 40, 42, 46, 52, 58}`. This is a
purely decidable check; we use `decide` rather than `native_decide` so
the resulting proof depends only on the three foundational Lean axioms.
-/
theorem admissibleModulus_below_60 :
    (Finset.range 60).filter AdmissibleModulus =
      ({4, 6, 10, 12, 16, 18, 22, 28, 30, 36, 40, 42, 46, 52, 58} :
        Finset ℕ) := by
  decide

end «Erdos273»

-- Verification: axiom check on the auxiliary lemmas. The output must
-- list only `propext`, `Classical.choice`, `Quot.sound` for these to
-- qualify as `[verified]` per the project's promotion policy.
#print axioms «Erdos273».admissibleModulus_iff
#print axioms «Erdos273».admissibleModulus_four
#print axioms «Erdos273».four_le_of_admissible
#print axioms «Erdos273».smallest_admissible_modulus_is_four
#print axioms «Erdos273».admissibleModulus_below_60
