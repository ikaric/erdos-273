# Decision — Erdős #273 strictness convention adopted

**Author:** formalist
**Date:** 2026-05-28
**Vector:** Part A of the formalist round 2 task
**Status:** Implemented in `formal/Erdos273/CoveringSystem.lean`.

## What changed

The Lean type `Erdos273.Erdos273Conjecture` was redefined from

```lean
def Erdos273Conjecture : Prop := ∃ C : CoveringSystem, C.SolvesErdos273
```

to require strictness:

```lean
def Erdos273Conjecture : Prop :=
  ∃ C : CoveringSystem, C.IsStrict ∧ C.SolvesErdos273
```

where `IsStrict` says the moduli of the covering system are all
distinct (`(C.classes.image ResidueClass.modulus).card = C.classes.card`).

## Why

The previous (non-strict) version was **trivially provable**: the four
residue classes `{0, 1, 2, 3} (mod 4)` cover `ℤ`, and `4 = 5 - 1` is
admissible because `5` is prime and `5 ≥ 5`. We promote this to a Lean
witness in the same file:

```lean
theorem non_strict_erdos273_trivially_solvable :
    ∃ C : CoveringSystem, C.SolvesErdos273
```

(verified, axiom-clean), demonstrating concretely why the strictness
constraint is essential.

## Literature alignment

- **Erdős–Graham 1980** ("Old and new problems in combinatorial
  number theory") introduce covering systems with **distinct moduli**
  as the canonical object; without strictness the question collapses.
- **DeepMind formal-conjectures repo**
  (`FormalConjecturesForMathlib/NumberTheory/CoveringSystem.lean`)
  uses the same convention with their `StrictCoveringSystem` type.
- **Klein–Koukoulopoulos–Lemieux (2024)** and the BBMST 2007 program
  both work with distinct moduli; the density obstruction
  `∑_d 1/d ≥ 1` only has bite under strictness.
- The V1 SAT computations
  (`findings/heur-sat-2026-05-28.md`) explicitly encode the
  distinct-moduli constraint as per-modulus at-most-one CNF clauses;
  the headline `D(L) < 1 ⇒ UNSAT` argument is contingent on
  strictness.

## Two equivalent formulations

We define both:

```lean
def IsStrict  (C : CoveringSystem) : Prop :=
  (C.classes.image ResidueClass.modulus).card = C.classes.card

def IsStrict' (C : CoveringSystem) : Prop :=
  ∀ c₁ ∈ C.classes, ∀ c₂ ∈ C.classes,
    c₁.modulus = c₂.modulus → c₁ = c₂
```

and prove `isStrict_iff : C.IsStrict ↔ C.IsStrict'` (axiom-clean).
The cardinality form (`IsStrict`) is more convenient for `Finset.sum_image`
manipulations downstream; the injectivity form (`IsStrict'`) is more
natural in some hypotheses.

## Downstream consequences

- The literature side: the manuscript and ROADMAP should refer to
  `Erdos273Conjecture` in its strict form throughout. The bare
  "solves Erdős #273" formulation is now exhibited as a counterexample,
  not the target.
- The V1 SAT lane: the SAT encoding already uses distinct moduli, so
  the strictness change is a no-op on that side. The bridge lemma
  `strict_covering_reciprocal_bound` (the verified Part B deliverable)
  is what closes the gap between SAT/density numerical evidence and
  the strict-Conjecture formulation.
- The Part C corollary `no_strict_admissible_cover_27720` is stated
  in terms of `Finset.image ResidueClass.modulus ... .card = S.card`
  (the same form as `IsStrict`), matching the V1 SAT encoding.

## Reviewer signal

This decision is fully internal to the project's Lean encoding —
no published mathematics is affected, only the Lean formalization
choice. The strict convention is the standard and unambiguous one;
the non-strict version is degenerate and not what the question is
intended to ask.
