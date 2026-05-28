# Critic review — ℤ-form of L=27720 obstruction

**Author:** critic
**Date:** 2026-05-28 (session 2)
**Scope:** `formal/Erdos273/IntegerForm.lean` (post-`1af6b18` commit)

## Verdict
**PASS**

All three new theorems (`covers_int_iff_covers_range_L`,
`no_strict_admissible_covering_Z_27720`,
`erdos273_modulus_not_dividing_27720`) are correctly stated, correctly
proved, build cleanly, and depend only on the three Lean foundational
axioms. The IntegerForm.lean file is ready for promotion in the
manuscript.

There is one **manuscript-side** drift item (a footnote that should
be updated to cite the new ℤ-form theorem), which is out of scope for
this review per the orchestrator's read-only mandate. Flagged in
"Recommendations" below.

## Items reviewed

### Build and axiom audit (item 6)

Ran `lake build` from `formal/`. Exit 0. The only diagnostic
emissions are the `#print axioms` informational messages, all clean:

```
'Erdos273.covers_int_iff_covers_range_L' depends on axioms:
    [propext, Classical.choice, Quot.sound]
'Erdos273.no_strict_admissible_covering_Z_27720' depends on axioms:
    [propext, Classical.choice, Quot.sound]
'Erdos273.erdos273_modulus_not_dividing_27720' depends on axioms:
    [propext, Classical.choice, Quot.sound]
```

No `sorryAx`, no `Lean.ofReduceBool`, no project-local axioms.

### The equivalence lemma `covers_int_iff_covers_range_L` (item 1)

The lemma states: for any finite `S : Finset ResidueClass` and
`L ≥ 1` with every `c.modulus ∣ L`,

`(∀ n : ℤ, ∃ c ∈ S, n ∈ c.toSet) ↔ (∀ i : ℕ, i < L → ∃ c ∈ S, (i : ℤ) ∈ c.toSet)`.

**Forward direction.** Just specialization: `n := (i : ℤ)`. Trivial.
The proof reads `intro h i _; exact h (i : ℤ)`. Correct.

**Backward direction.** The proof picks `r := (n % L).toNat`, with
the chain:

| step | lemma | verified |
|---|---|---|
| `0 ≤ n % L` (when L > 0) | `Int.emod_nonneg n (L ≠ 0)` | OK |
| `n % L < L` (when L > 0) | `Int.emod_lt_of_pos n hLposℤ` | OK |
| `(r : ℤ) = n % L` | `Int.toNat_of_nonneg hmod_nonneg` | OK |
| `r < L` (as Nat) | cast of the above | OK |
| `n % L ≡ n [ZMOD L]` | `Int.mod_modEq n L` | OK |
| `n % L ≡ n [ZMOD c.modulus]` from `c.modulus ∣ L` | `Int.ModEq.of_dvd hcdvdℤ` | OK |
| congruence → `ZMod` equality | `ZMod.intCast_eq_intCast_iff` | OK |

I independently looked up each lemma's signature:
- `Int.ModEq.of_dvd : ∀ {m n a b : ℤ}, m ∣ n → a ≡ b [ZMOD n] → a ≡ b [ZMOD m]` — the direction is correct: from `a ≡ b mod L` and `m ∣ L`, we get `a ≡ b mod m`, which is precisely the direction the proof needs ("weaker" congruence from "stronger" one).
- `Int.emod_nonneg : ∀ (a : ℤ) {b : ℤ}, b ≠ 0 → 0 ≤ a % b` — used with `b = L`. Correct.
- `Int.emod_lt_of_pos : ∀ (a : ℤ) {b : ℤ}, 0 < b → a % b < b` — used with `b = L > 0`. Correct.
- `Int.mod_modEq : ∀ (a n : ℤ), a % n ≡ a [ZMOD n]` — direct. Correct.
- `ZMod.intCast_eq_intCast_iff : ∀ (a b : ℤ) (c : ℕ), ↑a = ↑b ↔ a ≡ b [ZMOD ↑c]` — used `.mpr` direction. Correct.
- `Int.toNat_of_nonneg : ∀ {a : ℤ}, 0 ≤ a → ↑a.toNat = a` — used `n % L`'s non-negativity. Correct.

I also stress-tested the lemma at `L = 1` (smallest legal value, with `S` forced empty by `ResidueClass.hmod : 2 ≤ modulus` and `c.modulus ∣ 1`) and `L = 27720` (the value actually used). Both compile.

### The ℤ-form theorem `no_strict_admissible_covering_Z_27720` (item 2)

Statement (verbatim Lean):
```
¬ ∃ (C : CoveringSystem), C.IsStrict ∧
    ∀ c ∈ C.classes, AdmissibleModulus c.modulus ∧ c.modulus ∣ 27720
```

Proof sketch:
1. `rintro ⟨C, hStrict, hSmod⟩` — assume the witness.
2. Extract `hdvd : ∀ c ∈ C.classes, c.modulus ∣ 27720` from the right
   side of the AdmissibleModulus ∧ divides conjunction.
3. `C.covers : ∀ n : ℤ, ∃ c ∈ classes, n ∈ c.toSet` is the global cover hypothesis built into `CoveringSystem`.
4. Apply `covers_int_iff_covers_range_L (.mp)` with `L = 27720` and `hdvd` to get the range form `hcovL : ∀ i < 27720, ∃ c ∈ C.classes, (i : ℤ) ∈ c.toSet`.
5. Feed `⟨C.classes, hSmod, hStrict, hcovL⟩` into `no_strict_admissible_cover_27720` to derive `False`.

Each step is mechanically correct. The strictness and admissibility
hypotheses chain through unchanged. The closing argument is a direct
application of the verified range-form theorem.

### The contrapositive corollary `erdos273_modulus_not_dividing_27720` (item 3)

Statement:
```
Erdos273Conjecture → ∃ C : CoveringSystem, C.IsStrict ∧
    C.SolvesErdos273 ∧ ∃ c ∈ C.classes, ¬ c.modulus ∣ 27720
```

In words: if Erdős #273 has an affirmative answer, then any witness
covering uses at least one modulus that does **not** divide 27720.

Proof:
1. `rintro ⟨C, hStrict, hSolves⟩` from `Erdos273Conjecture`.
2. `refine ⟨C, hStrict, hSolves, ?_⟩` — leave the new ∃-goal.
3. `by_contra hAll` — assume every modulus divides 27720.
4. `push Not at hAll` — converts `¬ ∃ c ∈ C.classes, ¬ c.modulus ∣ 27720`
   into `∀ c ∈ C.classes, c.modulus ∣ 27720`.
5. Pair the divisibility with admissibility from `hSolves` to obtain
   `hPair : ∀ c ∈ C.classes, AdmissibleModulus c.modulus ∧ c.modulus ∣ 27720`.
6. Apply `no_strict_admissible_covering_Z_27720 ⟨C, hStrict, hPair⟩`
   for the contradiction.

**Subtle item I stress-tested:** the tactic `push Not at hAll` is
**not** a typo — it is the current Mathlib syntax that has replaced
the deprecated `push_neg`. Lean 4.30.0 + recent Mathlib emit a
deprecation warning if `push_neg` is used:

> `push_neg` has been deprecated. Prefer using `push Not` instead.

I verified by running a minimal test that `push Not at hAll` correctly
transforms `¬ ∃ c ∈ s, ¬ P c` into `∀ c ∈ s, P c` — exactly the
expected `push_neg` semantics.

The orchestrator's English description of the corollary in the brief
was slightly imprecise (it referred to the conclusion as the "negation
of 'every modulus divides 27720'", whereas it is technically the
contrapositive packaging) — but the Lean theorem says the correct
thing, which is what matters.

### Manuscript-Lean correspondence (item 4)

The manuscript's Theorem 8 (`thm:numerical-27720`, lines 286–294 of
`manuscript/proof.tex`) states:

> "There is no strict covering of ℤ by residue classes whose moduli
> all lie in 𝓜 and all divide 27720 = 2³·3²·5·7·11."

The Lean theorem `no_strict_admissible_covering_Z_27720` states:

> ¬ ∃ C : CoveringSystem, C.IsStrict ∧ ∀ c ∈ C.classes,
>   AdmissibleModulus c.modulus ∧ c.modulus ∣ 27720

Unpacking: `CoveringSystem` carries `covers : ∀ n : ℤ, ∃ c ∈ classes,
n ∈ c.toSet` by construction (i.e., the cover is over ℤ).
`AdmissibleModulus m` unfolds to `∃ p prime, p ≥ 5 ∧ m = p − 1`
(i.e., `m ∈ 𝓜`). Strictness corresponds to "distinct moduli". So
the Lean statement is **verbatim** the manuscript Theorem 8 modulo
notation.

### Import structure (item 5)

```
Erdos273/CoveringSystem.lean       → import Mathlib
Erdos273/NumericalBound27720.lean  → import Erdos273.CoveringSystem, Mathlib
Erdos273/IntegerForm.lean          → import Erdos273.CoveringSystem,
                                       Erdos273.NumericalBound27720, Mathlib
```

No circular imports, no anomalies. `lake build` runs to completion
with only `#print axioms` info messages (no warnings, no errors).

## Concerns

### Minor — manuscript footnote drift (out of scope)

The footnote on the manuscript's Theorem 8 (line 293) currently
cites the *range-form* theorem:

```
\texttt{formal/Erdos273/NumericalBound27720.lean}, theorem
\texttt{no\_strict\_admissible\_cover\_27720}.
```

But Theorem 8 makes a **ℤ-form** claim, and the gap between "no
cover of ℤ" and "no cover of [0, 27720)" was previously bridged in
the manuscript by a one-paragraph informal lift inside the proof of
Theorem 8. That informal lift is now formalized as
`covers_int_iff_covers_range_L`, and the ℤ-form claim itself is
formalized as `no_strict_admissible_covering_Z_27720`. The footnote
should be updated to cite the latter (or both, with the
ℤ-form as the primary citation).

This is a **manuscript** change, not a Lean change, and is outside
this review's read-only mandate. The `/solve` orchestrator can pick
it up in the next session.

### Untracked file note (informational, not a defect)

`formal/Erdos273/NumericalBound180180.lean` is present in the working
tree as an untracked file, and `formal/Erdos273.lean` has an
unstaged modification adding it to the imports. Neither is part of
the commit under review (`1af6b18`). Mentioning it here so the next
session is aware; it does not affect this review.

## Recommendations

1. **Promote the three IntegerForm theorems to `[verified]` in the
   manuscript.** The Lean is correct; the axiom audit is clean; the
   build is clean. No reservations.

2. **Update the footnote on manuscript Theorem 8** to cite
   `no_strict_admissible_covering_Z_27720` in `IntegerForm.lean`
   (instead of, or alongside, the range-form theorem). Optionally,
   replace the informal "lift" paragraph inside the proof of
   Theorem 8 with a single sentence citing
   `covers_int_iff_covers_range_L`.

3. **Optional improvement (not blocking):** in
   `no_strict_admissible_covering_Z_27720`, the variable `hSmod`
   bundles `AdmissibleModulus c.modulus ∧ c.modulus ∣ 27720`
   together. This is fine, but a future refactor could split it into
   two separate `∀ c ∈ classes, ...` hypotheses to match the
   manuscript phrasing more cleanly. Cosmetic only.
