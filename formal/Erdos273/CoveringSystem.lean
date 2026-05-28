/-
Erdős Problem #273 — basic API.

We define the combinatorial objects that the rest of the project will
reason about:

* a single residue class `a (mod m)`,
* a covering system (a finite collection of residue classes whose union
  is `ℤ`),
* the *admissible modulus* predicate "`m = p - 1` for some prime
  `p ≥ 5`",
* the strict-covering convention (distinct moduli, Erdős–Graham),
* the conjecture itself, as a `Prop`,
* a density union bound and the resulting strict-covering lower bound,
  which is the verified bridge to the SAT/density numerical evidence
  in `findings/heur-sat-2026-05-28.md`.

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

/-- Positivity of the modulus. -/
lemma modulus_pos (c : ResidueClass) : 0 < c.modulus := by
  have := c.hmod; omega

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

/-- A covering system is *strict* if its moduli are all distinct
(Erdős–Graham convention). We follow the same convention used in the
DeepMind `formal-conjectures` `StrictCoveringSystem` type. -/
def IsStrict (C : CoveringSystem) : Prop :=
  (C.classes.image ResidueClass.modulus).card = C.classes.card

/-- Equivalent formulation of strictness in terms of an injectivity
condition on the modulus function. -/
def IsStrict' (C : CoveringSystem) : Prop :=
  ∀ c₁ ∈ C.classes, ∀ c₂ ∈ C.classes,
    c₁.modulus = c₂.modulus → c₁ = c₂

/-- The two formulations of strictness agree. -/
lemma isStrict_iff (C : CoveringSystem) : C.IsStrict ↔ C.IsStrict' := by
  unfold IsStrict IsStrict'
  rw [Finset.card_image_iff]
  refine ⟨fun h c₁ hc₁ c₂ hc₂ hmod => h hc₁ hc₂ hmod,
          fun h c₁ hc₁ c₂ hc₂ hmod => h c₁ hc₁ c₂ hc₂ hmod⟩

end CoveringSystem

/-- A natural number is *admissible for Erdős #273* if it is of the form
`p - 1` for some prime `p ≥ 5`. -/
def AdmissibleModulus (m : ℕ) : Prop :=
  ∃ p : ℕ, p.Prime ∧ 5 ≤ p ∧ m = p - 1

/-- **Erdős Problem #273** (strict version per the Erdős–Graham 1980
convention): does there exist a *strict* covering system of `ℤ` (one with
distinct moduli) all of whose moduli are of the form `p - 1` for some
prime `p ≥ 5`?

Stated as a `Prop`; the conjecture is to decide whether this proposition
holds. The strictness requirement is essential: without it the
non-strict version is trivially `True` (witness: `{0, 1, 2, 3} mod 4`,
since `4 = 5 - 1 ∈ ℳ`); see `non_strict_erdos273_trivially_solvable`
below. -/
def Erdos273Conjecture : Prop :=
  ∃ C : CoveringSystem, C.IsStrict ∧ C.SolvesErdos273

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

/-! ## Non-strict version is trivial: the sanity-check for Part A.

Without the distinctness constraint, the conjecture is settled by the
trivial cover `{0, 1, 2, 3} mod 4` (modulus 4 is admissible because
`5` is prime). This is precisely why the literature convention adds
the strictness requirement. -/

/-- The four residue classes `0, 1, 2, 3 (mod 4)`. -/
private def trivialFourClasses : Finset ResidueClass :=
  { ⟨4, by norm_num, (0 : ZMod 4)⟩
  , ⟨4, by norm_num, (1 : ZMod 4)⟩
  , ⟨4, by norm_num, (2 : ZMod 4)⟩
  , ⟨4, by norm_num, (3 : ZMod 4)⟩ }

/-- The trivial covering system using only the modulus `4`. -/
private def trivialFourCovering : CoveringSystem where
  classes := trivialFourClasses
  covers := by
    intro n
    -- `(n : ZMod 4)` ranges over the four elements `0, 1, 2, 3`.
    have hr : ∀ r : ZMod 4, r = 0 ∨ r = 1 ∨ r = 2 ∨ r = 3 := by decide
    rcases hr ((n : ZMod 4)) with h | h | h | h
    · refine ⟨⟨4, by norm_num, 0⟩, ?_, ?_⟩
      · simp [trivialFourClasses]
      · simpa [ResidueClass.mem_toSet] using h
    · refine ⟨⟨4, by norm_num, 1⟩, ?_, ?_⟩
      · simp [trivialFourClasses]
      · simpa [ResidueClass.mem_toSet] using h
    · refine ⟨⟨4, by norm_num, 2⟩, ?_, ?_⟩
      · simp [trivialFourClasses]
      · simpa [ResidueClass.mem_toSet] using h
    · refine ⟨⟨4, by norm_num, 3⟩, ?_, ?_⟩
      · simp [trivialFourClasses]
      · simpa [ResidueClass.mem_toSet] using h

/-- Without the strictness constraint, the conjecture is trivially true:
the cover `{0, 1, 2, 3} mod 4` settles it because `4 = 5 - 1` is
admissible (`5` is prime, `5 ≥ 5`). This is why we adopt the strict
convention. -/
theorem non_strict_erdos273_trivially_solvable :
    ∃ C : CoveringSystem, C.SolvesErdos273 := by
  refine ⟨trivialFourCovering, ?_⟩
  intro c hc
  refine ⟨5, ?_, le_refl 5, ?_⟩
  · decide
  · simp only [trivialFourCovering, trivialFourClasses, Finset.mem_insert,
      Finset.mem_singleton] at hc
    rcases hc with h | h | h | h <;> · rw [h]

/-! ## Part B — Density union bound.

We now prove the density bound that the V1 SAT computations rely on.
The argument is purely combinatorial: each residue class with modulus
`m` dividing `L` covers exactly `L / m` of the residues in
`[0, L)`. By the union bound on `Finset.card_biUnion_le`, the total
number of covered residues is at most `∑ c, L / c.modulus`.

The strictness hypothesis is **not** needed for the basic density bound
(the sum is already over the elements of `S`); it becomes relevant when
one wants to rewrite the sum as `∑_{m ∈ S.image modulus} L/m`, which is
then identified with `D(L) · L` for the moduli set `M_L`.

We use a local `open Classical` so that the `Finset.filter` predicates
involving `∈ c.toSet` (a `Set ℤ` membership) and `∃ c ∈ S, …` (a
non-decidable existential) get their decidability from `propDecidable`.
This is a meta-level convenience and adds only the foundational
`Classical.choice` axiom to the dependency chain.
-/

open Classical

/-- For a residue class `c` with `c.modulus ∣ L`, the set of `i ∈ [0, L)`
that lie in `c.toSet` has cardinality exactly `L / c.modulus`. The proof
reduces to `Nat.count_modEq_card` after translating the predicate
`(i : ℤ) ∈ c.toSet` to a `MOD` congruence. -/
lemma card_covered_eq (c : ResidueClass) (L : ℕ)
    (hdvd : c.modulus ∣ L) :
    ((Finset.range L).filter
        (fun i : ℕ => (i : ℤ) ∈ c.toSet)).card = L / c.modulus := by
  classical
  have hpos : 0 < c.modulus := c.modulus_pos
  haveI : NeZero c.modulus := ⟨hpos.ne'⟩
  -- Translate `(i : ℤ) ∈ c.toSet` to a `Nat.ModEq` statement.
  have hpred : ∀ i : ℕ,
      ((i : ℤ) ∈ c.toSet) ↔ (i ≡ c.residue.val [MOD c.modulus]) := by
    intro i
    rw [ResidueClass.mem_toSet]
    -- `((i : ℤ) : ZMod m) = (i : ZMod m)` by `push_cast`.
    have h1 : ((i : ℤ) : ZMod c.modulus) = ((i : ℕ) : ZMod c.modulus) := by push_cast; rfl
    rw [h1]
    -- `(c.residue.val : ZMod m) = c.residue` by `ZMod.natCast_zmod_val`.
    have h2 : ((c.residue.val : ℕ) : ZMod c.modulus) = c.residue := ZMod.natCast_zmod_val _
    constructor
    · intro heq
      have : ((i : ℕ) : ZMod c.modulus) = ((c.residue.val : ℕ) : ZMod c.modulus) := by
        rw [h2]; exact heq
      exact (ZMod.natCast_eq_natCast_iff _ _ _).mp this
    · intro hcong
      have : ((i : ℕ) : ZMod c.modulus) = ((c.residue.val : ℕ) : ZMod c.modulus) :=
        (ZMod.natCast_eq_natCast_iff _ _ _).mpr hcong
      rw [this, h2]
  -- Replace the filter predicate.
  have hcong :
      (Finset.range L).filter (fun i : ℕ => (i : ℤ) ∈ c.toSet)
        = (Finset.range L).filter
            (fun i : ℕ => i ≡ c.residue.val [MOD c.modulus]) := by
    apply Finset.filter_congr
    intros i _
    exact hpred i
  rw [hcong]
  -- Apply `Nat.count_modEq_card`, then use `L % m = 0` to drop the if-branch.
  rw [← Nat.count_eq_card_filter_range, Nat.count_modEq_card L hpos]
  have hLmod : L % c.modulus = 0 := Nat.mod_eq_zero_of_dvd hdvd
  simp [hLmod]

/-- **Density union bound.** The number of residues in `[0, L)` covered
by a finite collection of residue classes whose moduli all divide `L` is
at most the sum of `L / modulus` over the collection. (No strictness
assumption.) -/
theorem density_union_bound
    (S : Finset ResidueClass) (L : ℕ)
    (hdvd : ∀ c ∈ S, c.modulus ∣ L) :
    ((Finset.range L).filter
        (fun i : ℕ => ∃ c ∈ S, (i : ℤ) ∈ c.toSet)).card
      ≤ ∑ c ∈ S, L / c.modulus := by
  classical
  -- The "covered" set rewrites as a biUnion of per-class filters.
  let covered : ResidueClass → Finset ℕ :=
    fun c => (Finset.range L).filter (fun i : ℕ => (i : ℤ) ∈ c.toSet)
  have hbiUnion :
      (Finset.range L).filter (fun i : ℕ => ∃ c ∈ S, (i : ℤ) ∈ c.toSet)
        = S.biUnion covered := by
    ext i
    simp only [Finset.mem_filter, Finset.mem_range, Finset.mem_biUnion, covered]
    constructor
    · rintro ⟨hi, c, hc, hmem⟩
      exact ⟨c, hc, hi, hmem⟩
    · rintro ⟨c, hc, hi, hmem⟩
      exact ⟨hi, c, hc, hmem⟩
  rw [hbiUnion]
  calc (S.biUnion covered).card
      ≤ ∑ c ∈ S, (covered c).card := Finset.card_biUnion_le
    _ = ∑ c ∈ S, L / c.modulus := by
        apply Finset.sum_congr rfl
        intros c hc
        exact card_covered_eq c L (hdvd c hc)

/-- **Strict-covering density lower bound.** If a (possibly strict)
covering of `ℤ/Lℤ` is given by a finite collection `S` of residue
classes whose moduli all divide `L`, then `L ≤ ∑ c ∈ S, L / c.modulus`.

This is the direct consequence of `density_union_bound` plus the fact
that the cover covers all of `[0, L)`. (Strictness is **not** needed
for this conclusion; it is included as a hypothesis for downstream
users who want to feed the result into a "sum over distinct moduli"
re-expression.) -/
theorem strict_covering_density_bound
    (S : Finset ResidueClass) (L : ℕ)
    (_hStrict : (S.image ResidueClass.modulus).card = S.card)
    (hdvd : ∀ c ∈ S, c.modulus ∣ L)
    (hcov : ∀ i : ℕ, i < L → ∃ c ∈ S, (i : ℤ) ∈ c.toSet) :
    L ≤ ∑ c ∈ S, L / c.modulus := by
  -- The covered subset of `[0, L)` equals all of `[0, L)`.
  have hall :
      (Finset.range L).filter
          (fun i : ℕ => ∃ c ∈ S, (i : ℤ) ∈ c.toSet)
        = Finset.range L := by
    apply Finset.filter_eq_self.mpr
    intros i hi
    exact hcov i (Finset.mem_range.mp hi)
  have hcount : (Finset.range L).card
      ≤ ∑ c ∈ S, L / c.modulus := by
    calc (Finset.range L).card
        = ((Finset.range L).filter
            (fun i : ℕ => ∃ c ∈ S, (i : ℤ) ∈ c.toSet)).card := by rw [hall]
      _ ≤ ∑ c ∈ S, L / c.modulus := density_union_bound S L hdvd
  simpa using hcount

/-- **Strict-covering density bound, expressed as `∑ 1/m ≥ 1`.**
If `L ≥ 1` and the assumptions of `strict_covering_density_bound`
hold, the sum of reciprocal moduli is at least `1` (in `ℚ`). This is
the form used directly by the SAT-density numerical evidence:
`D(L) = ∑_{m ∈ M_L} 1/m`, and `D(L) < 1` rules out a strict cover. -/
theorem strict_covering_reciprocal_bound
    (S : Finset ResidueClass) (L : ℕ) (hL : 1 ≤ L)
    (hStrict : (S.image ResidueClass.modulus).card = S.card)
    (hdvd : ∀ c ∈ S, c.modulus ∣ L)
    (hcov : ∀ i : ℕ, i < L → ∃ c ∈ S, (i : ℤ) ∈ c.toSet) :
    (1 : ℚ) ≤ ∑ c ∈ S, (1 : ℚ) / c.modulus := by
  have hbase := strict_covering_density_bound S L hStrict hdvd hcov
  have hLQ : (0 : ℚ) < L := by exact_mod_cast hL
  have hLne : (L : ℚ) ≠ 0 := hLQ.ne'
  -- Cast the Nat-inequality to ℚ.
  have hcast : (L : ℚ) ≤ ((∑ c ∈ S, L / c.modulus : ℕ) : ℚ) := by exact_mod_cast hbase
  -- The sum coerced to ℚ becomes `∑ (L/c.modulus : ℚ)`, using `c.modulus ∣ L`.
  have hrewrite :
      ((∑ c ∈ S, L / c.modulus : ℕ) : ℚ) = ∑ c ∈ S, (L : ℚ) / c.modulus := by
    rw [Nat.cast_sum]
    apply Finset.sum_congr rfl
    intros c hc
    have hpos : (0 : ℕ) < c.modulus := c.modulus_pos
    have hmne : (c.modulus : ℚ) ≠ 0 := by exact_mod_cast hpos.ne'
    rw [Nat.cast_div (hdvd c hc) hmne]
  rw [hrewrite] at hcast
  -- Factor `L` out of the sum.
  have hsum_eq : ∑ c ∈ S, (L : ℚ) / c.modulus = L * ∑ c ∈ S, (1 : ℚ) / c.modulus := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intros c _
    ring
  rw [hsum_eq] at hcast
  -- Conclude by dividing by L: `L ≤ L * X` and `L > 0` gives `1 ≤ X`.
  have : (L : ℚ) * 1 ≤ L * ∑ c ∈ S, (1 : ℚ) / c.modulus := by linarith
  exact le_of_mul_le_mul_left this hLQ

/-! ## Part C — Abstract obstruction from `D_L < 1`.

The strict-covering reciprocal bound `1 ≤ ∑ 1/c.modulus` combined with
strictness gives the obstruction: if the set of *possible* moduli
`M_L := {m : admissible, m ∣ L, 2 ≤ m}` satisfies `D(L) = ∑_{m ∈ M_L} 1/m
< 1`, then no strict admissible cover of `ℤ/Lℤ` with moduli in `M_L`
can exist.

The structural lemma `no_strict_cover_of_low_density` is verified; the
numerical fact `D(27720) < 1` (which would close the corollary
`no_strict_admissible_cover_27720`) is a finite rational computation but
is left as `sorry` here because a clean `decide`-based discharge needs
careful encoding (and `native_decide` would inject the
`Lean.ofReduceBool` axiom, which is disqualifying per project policy).

A separate session can either (a) compute `D(27720)` with explicit
rational arithmetic in `formal/numerics/` and emit a self-contained
inequality lemma, or (b) discharge a smaller `L` first where `decide` is
cheap.
-/

/-- **Abstract density obstruction.** If `L ≥ 1` and `M ⊆ ℕ` is a finite
set of admissible candidate moduli (each `≥ 2`, each dividing `L`) with
`∑_{m ∈ M} 1/m < 1`, then no strict cover of `ℤ/Lℤ` exists whose
moduli all lie in `M`. (This is the contrapositive of
`strict_covering_reciprocal_bound` plus the fact that strictness lets
us bound `∑_{c ∈ S} 1/c.modulus ≤ ∑_{m ∈ M} 1/m`.) -/
theorem no_strict_cover_of_low_density
    (L : ℕ) (hL : 1 ≤ L) (M : Finset ℕ)
    (_hM2 : ∀ m ∈ M, 2 ≤ m)
    (hMdvd : ∀ m ∈ M, m ∣ L)
    (hD : ∑ m ∈ M, (1 : ℚ) / m < 1) :
    ¬ ∃ (S : Finset ResidueClass),
        (∀ c ∈ S, c.modulus ∈ M) ∧
        (S.image ResidueClass.modulus).card = S.card ∧
        (∀ i : ℕ, i < L → ∃ c ∈ S, (i : ℤ) ∈ c.toSet) := by
  rintro ⟨S, hSmod, hStrict, hcov⟩
  have hdvd : ∀ c ∈ S, c.modulus ∣ L := fun c hc => hMdvd _ (hSmod c hc)
  -- Apply the reciprocal bound to get `1 ≤ ∑_{c ∈ S} 1/c.modulus`.
  have hone := strict_covering_reciprocal_bound S L hL hStrict hdvd hcov
  -- Strictness: the modulus map `c ↦ c.modulus` is injective on `S`, so
  -- `∑_{c ∈ S} 1/c.modulus = ∑_{m ∈ S.image modulus} 1/m`.
  have hInj : Set.InjOn (ResidueClass.modulus) (S : Set ResidueClass) :=
    Finset.card_image_iff.mp hStrict
  have hsum_eq :
      ∑ c ∈ S, (1 : ℚ) / c.modulus
        = ∑ m ∈ S.image ResidueClass.modulus, (1 : ℚ) / m := by
    rw [Finset.sum_image]
    intros c₁ hc₁ c₂ hc₂ h
    exact hInj hc₁ hc₂ h
  rw [hsum_eq] at hone
  -- `S.image modulus ⊆ M`, and reciprocals are non-negative, so
  -- `∑_{m ∈ S.image modulus} 1/m ≤ ∑_{m ∈ M} 1/m`.
  have hsub : S.image ResidueClass.modulus ⊆ M := by
    intros m hm
    simp only [Finset.mem_image] at hm
    obtain ⟨c, hcS, hcm⟩ := hm
    rw [← hcm]
    exact hSmod c hcS
  have hnonneg : ∀ m ∈ M, (0 : ℚ) ≤ 1 / m := by
    intros m hm
    have : 0 ≤ (m : ℚ) := by exact_mod_cast Nat.zero_le _
    positivity
  have hle : ∑ m ∈ S.image ResidueClass.modulus, (1 : ℚ) / m
              ≤ ∑ m ∈ M, (1 : ℚ) / m := by
    apply Finset.sum_le_sum_of_subset_of_nonneg hsub
    intros m hmM _
    exact hnonneg m hmM
  -- Combine: `1 ≤ ∑_{m ∈ S.image} 1/m ≤ ∑_{m ∈ M} 1/m < 1`, contradiction.
  linarith

/-- **Numerical corollary for `L = 27720` (sketch).** No strict
admissible cover of `ℤ/27720ℤ` exists.

This is the headline numerical claim from the V1 SAT/density run.
The proof relies on the abstract obstruction `no_strict_cover_of_low_density`
applied to `M := admissibleDivisors 27720`. The remaining gap is the
arithmetic fact `D(27720) = ∑_{m ∈ M_{27720}} 1/m < 1` (numerically
`0.9626 < 1`); a clean `decide` discharge of this rational inequality
over 34 terms is left for a dedicated numerical-Lean session. -/
theorem no_strict_admissible_cover_27720 :
    ¬ ∃ (S : Finset ResidueClass),
        (∀ c ∈ S, AdmissibleModulus c.modulus ∧ c.modulus ∣ 27720) ∧
        (S.image ResidueClass.modulus).card = S.card ∧
        (∀ i : ℕ, i < 27720 → ∃ c ∈ S, (i : ℤ) ∈ c.toSet) := by
  -- Set `M := admissible divisors of 27720` (these are exactly the
  -- moduli appearing in the SAT-bounded problem at `L = 27720`).
  classical
  set M : Finset ℕ :=
    (Finset.range 27721).filter (fun m => AdmissibleModulus m ∧ m ∣ 27720) with hMdef
  rintro ⟨S, hSmod, hStrict, hcov⟩
  -- Each `c.modulus` lies in `M`.
  have hSmem : ∀ c ∈ S, c.modulus ∈ M := by
    intros c hc
    have hadm : AdmissibleModulus c.modulus ∧ c.modulus ∣ 27720 := hSmod c hc
    have h4 : 4 ≤ c.modulus := four_le_of_admissible hadm.1
    have hle : c.modulus ≤ 27720 := Nat.le_of_dvd (by norm_num) hadm.2
    rw [hMdef]
    simp [Finset.mem_filter, Finset.mem_range]
    exact ⟨by omega, hadm⟩
  have hM2 : ∀ m ∈ M, 2 ≤ m := by
    intros m hm
    rw [hMdef] at hm
    simp [Finset.mem_filter] at hm
    have h4 : 4 ≤ m := four_le_of_admissible hm.2.1
    omega
  have hMdvd : ∀ m ∈ M, m ∣ 27720 := by
    intros m hm
    rw [hMdef] at hm
    simp [Finset.mem_filter] at hm
    exact hm.2.2
  -- Numerical: D(27720) < 1. This is the gap.
  -- TODO: discharge by exact rational computation; native_decide is
  -- forbidden, so this needs a careful `decide` invocation or a
  -- manually-summed witness.
  have hD : ∑ m ∈ M, (1 : ℚ) / m < 1 := by
    sorry -- TODO: D(27720) = 0.9626... < 1, computable but heavy
  exact no_strict_cover_of_low_density 27720 (by norm_num) M hM2 hMdvd hD
    ⟨S, hSmem, hStrict, hcov⟩

end «Erdos273»

-- Verification: axiom check on the auxiliary lemmas. The output must
-- list only `propext`, `Classical.choice`, `Quot.sound` for these to
-- qualify as `[verified]` per the project's promotion policy.
#print axioms «Erdos273».admissibleModulus_iff
#print axioms «Erdos273».admissibleModulus_four
#print axioms «Erdos273».four_le_of_admissible
#print axioms «Erdos273».smallest_admissible_modulus_is_four
#print axioms «Erdos273».admissibleModulus_below_60
#print axioms «Erdos273».CoveringSystem.isStrict_iff
#print axioms «Erdos273».non_strict_erdos273_trivially_solvable
#print axioms «Erdos273».card_covered_eq
#print axioms «Erdos273».density_union_bound
#print axioms «Erdos273».strict_covering_density_bound
#print axioms «Erdos273».strict_covering_reciprocal_bound
#print axioms «Erdos273».no_strict_cover_of_low_density
-- `no_strict_admissible_cover_27720` depends on a numerical `sorry`
-- (the `D(27720) < 1` rational arithmetic fact); it is therefore
-- `[sketch]` and is not promoted to `[verified]`.
#print axioms «Erdos273».no_strict_admissible_cover_27720
