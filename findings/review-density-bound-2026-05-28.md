# Critic review — strict-covering density bound for Erdős #273

**Author:** critic
**Date:** 2026-05-28
**Scope:** `formal/Erdos273/CoveringSystem.lean` (post-`eaf38bf` commit)

## Verdict

**PASS with caveats.**

The Part B chain (`card_covered_eq` → `density_union_bound` →
`strict_covering_density_bound` → `strict_covering_reciprocal_bound` →
`no_strict_cover_of_low_density`) is mathematically correct,
axiom-clean, and ready for `[verified]` promotion in the manuscript.
The Part C "headline" corollary `no_strict_admissible_cover_27720` is
honestly tagged `[sketch]` (the file leaves the rational-arithmetic
`D(27720) < 1` step as `sorry`); it should be kept at `[sketch]`
status, exactly as the file already marks it.

Two manuscript-alignment caveats are worth fixing before promotion;
neither is a math issue.

## Items reviewed

1. **`IsStrict` and the `isStrict_iff` equivalence** — PASS. The
   cardinality-based formulation
   `(C.classes.image ResidueClass.modulus).card = C.classes.card` is
   equivalent to the `Set.InjOn` formulation via
   `Finset.card_image_iff`, exactly as proved. Axioms: `{propext,
   Classical.choice, Quot.sound}`.

2. **Strictness convention vs. literature.** PASS — `IsStrict =
   distinct moduli` is the standard Erdős–Graham convention. Bloom's
   `erdosproblems.com/273`, Wikipedia's covering-systems article, the
   BBMST density papers, Klein–Koukoulopoulos–Lemieux 2024, and the
   DeepMind `formal-conjectures` repo's `StrictCoveringSystem` all
   use distinct-moduli. The "non-strict" reading (the trivial
   `{0,1,2,3} mod 4` witness) is not the intended question. The
   project's decision to adopt strictness is right, and the
   `non_strict_erdos273_trivially_solvable` Lean witness is a
   well-placed reductio against the alternative reading.

3. **The strictness sanity check (`non_strict_erdos273_trivially_solvable`)**
   — PASS. The four residue classes `0, 1, 2, 3 (mod 4)` cover ℤ
   because the residue of `n` mod 4 hits exactly one of `0, 1, 2, 3`;
   `4 = 5 - 1` and `5` is prime, so the cover is `SolvesErdos273`-valid.
   The proof is straightforward and axiom-clean. **Useful clarifying
   role:** it concretely shows why strictness is required for the
   question to be non-trivial. (Note: this Lean theorem does *not*
   refute the strict conjecture — it satisfies `SolvesErdos273` but
   not `IsStrict`, so it is not a witness for `Erdos273Conjecture`
   as defined.)

4. **`card_covered_eq`** — PASS. Mathematical content: for `c.modulus
   ∣ L`, the set `{i ∈ [0,L) : i ≡ c.residue (mod c.modulus)}` has
   cardinality exactly `L / c.modulus`. The Lean proof reduces to
   `Nat.count_modEq_card` after translating `(i : ℤ) ∈ c.toSet` to
   `i ≡ c.residue.val [MOD c.modulus]`. The boundary case `L %
   c.modulus = 0` is correctly used to simplify the conditional
   branch. Axioms clean.

5. **`density_union_bound`** — PASS. The proof writes the covered set
   as a `S.biUnion`, applies `Finset.card_biUnion_le`, and uses
   `card_covered_eq` per class. **Strictness is not used here**, in
   accordance with the file's docstring. Axioms clean.

   Honest accounting: this lemma is genuinely strictness-free. Even
   if S has repeated moduli, the union-bound still holds (it just
   becomes weaker than the version one would write summing over the
   distinct-modulus image). The docstring is accurate.

6. **`strict_covering_density_bound`** — PASS. Just packages
   `density_union_bound` plus "the cover covers all of `[0,L)`" to
   conclude `L ≤ ∑ c, L / c.modulus`. **Strictness is taken as a
   hypothesis but is not used in the proof body** — the docstring
   correctly notes this and explains the hypothesis is for
   downstream consumers. (A purist cleanup would remove the
   `_hStrict` argument from this lemma; it is stylistically
   defensible to leave it for API uniformity, and harmless either
   way.) Axioms clean.

7. **`strict_covering_reciprocal_bound`** — PASS. Casts the previous
   bound to ℚ, factors out `L`, divides by `L > 0`. Mathematically a
   one-line algebraic rearrangement; the Lean proof is the expected
   few lines of `linarith` / `le_of_mul_le_mul_left`. Same comment
   on the unused `hStrict` hypothesis. Axioms clean.

8. **`no_strict_cover_of_low_density`** — PASS. This is where
   strictness genuinely enters. The proof:

   a. Applies `strict_covering_reciprocal_bound` to get
      `1 ≤ ∑_{c ∈ S} 1/c.modulus`.
   b. Uses strictness via `Finset.card_image_iff` + `Finset.sum_image`
      to rewrite `∑_{c ∈ S} 1/c.modulus = ∑_{m ∈ S.image modulus} 1/m`.
   c. Uses `S.image modulus ⊆ M` + `1/m ≥ 0` +
      `Finset.sum_le_sum_of_subset_of_nonneg` to bound the LHS by
      `∑_{m ∈ M} 1/m`.
   d. Combines `1 ≤ ∑_{m ∈ M} 1/m` with the hypothesis `∑_{m ∈ M}
      1/m < 1` via `linarith`.

   All four steps are correct. The strictness is used essentially
   at step (b); without it, step (b) over-counts repeated moduli
   and the chain breaks. Axioms clean.

9. **`no_strict_admissible_cover_27720`** — PASS-with-disclosed-`sorry`.
   The structural wiring from `no_strict_cover_of_low_density` to
   the 27720-specific statement is correct. The only gap is the
   rational-arithmetic fact `∑_{m ∈ admissibleDivisors(27720)} 1/m
   < 1`, which is correctly left as `sorry` (with a `TODO` comment
   explaining the deferred discharge). This file's `#print axioms
   no_strict_admissible_cover_27720` correctly lists `sorryAx`, so
   the build artifact transparently advertises its conditional
   status. **This theorem must NOT be promoted to `[verified]`;
   keep it `[sketch]`.**

10. **Independent numerical check of D(27720) < 1.** PASS.
    Reproduced in Python (sympy `Rational` arithmetic):
    - Admissible divisors of 27720 are 34 in number; explicit list:
      `{4, 6, 10, 12, 18, 22, 28, 30, 36, 40, 42, 60, 66, 70, 72, 88,
      126, 180, 198, 210, 280, 330, 396, 420, 462, 616, 630, 660,
      990, 1320, 2310, 2520, 4620, 9240}`.
    - `D(27720) = 953/990 ≈ 0.96263 < 1`.
    - 27720 factorization: `2^3 · 3^2 · 5 · 7 · 11` ✓.
    - The claim's wording "the 34 moduli `m` with `m ∣ 27720`, `m ≥ 4`,
      and `m + 1` prime" agrees with `AdmissibleModulus m ↔ (m + 1)
      prime ∧ m + 1 ≥ 5` (equivalently `(m + 1) prime ∧ m ≥ 4`),
      matching the Lean definition `AdmissibleModulus`.

    The numerical claim is correct; the `sorry` is purely about
    formalizing the rational-arithmetic computation in Lean
    (which is hard with `decide` over 34 large denominators and is
    `Lean.ofReduceBool`-forbidden under project policy).

11. **`#print axioms` audit on the build artifact.** PASS for
    everything except `no_strict_admissible_cover_27720`, which is
    explicitly `[sketch]`:

    | Theorem | Axioms |
    |---|---|
    | `admissibleModulus_iff` | `[propext, Quot.sound]` ✓ |
    | `admissibleModulus_four` | `[propext, Classical.choice, Quot.sound]` ✓ |
    | `four_le_of_admissible` | `[propext, Quot.sound]` ✓ |
    | `smallest_admissible_modulus_is_four` | `[propext, Classical.choice, Quot.sound]` ✓ |
    | `admissibleModulus_below_60` | `[propext, Classical.choice, Quot.sound]` ✓ |
    | `CoveringSystem.isStrict_iff` | `[propext, Classical.choice, Quot.sound]` ✓ |
    | `non_strict_erdos273_trivially_solvable` | `[propext, Classical.choice, Quot.sound]` ✓ |
    | `card_covered_eq` | `[propext, Classical.choice, Quot.sound]` ✓ |
    | `density_union_bound` | `[propext, Classical.choice, Quot.sound]` ✓ |
    | `strict_covering_density_bound` | `[propext, Classical.choice, Quot.sound]` ✓ |
    | `strict_covering_reciprocal_bound` | `[propext, Classical.choice, Quot.sound]` ✓ |
    | `no_strict_cover_of_low_density` | `[propext, Classical.choice, Quot.sound]` ✓ |
    | `no_strict_admissible_cover_27720` | `[propext, sorryAx, Classical.choice, Quot.sound]` (sketch — `sorryAx` is the disclosed rational-arithmetic step) |

    No `Lean.ofReduceBool`. No project-local `axiom`. No `native_decide`.
    All clean for the Part B chain (the proposed promotion).

12. **No "secretly proves Erdős #273"  red flag.** PASS. The verified
    theorem `no_strict_cover_of_low_density` is an *abstract*
    obstruction: "IF you produce a finite candidate-modulus set M
    with ∑ 1/m < 1, THEN no strict M-cover of [0,L) exists." The
    27720 instantiation does NOT settle Erdős #273; it only shows
    that any covering with moduli in M must have LCM of moduli not
    dividing 27720. This is a partial obstruction, a `[numerical: L
    ≤ 27720]`-style claim, not a resolution of the conjecture.

13. **No hidden uses of famous open hypotheses.** PASS. The argument
    is purely elementary combinatorics: residue counting + the
    Pigeonhole inequality `card_biUnion_le`. No GRH, no
    Elliott–Halberstam, no Hardy–Littlewood, no Bombieri–Vinogradov,
    no density hypotheses on Dirichlet L-functions. No parity
    barrier shenanigans (this isn't a sieve argument over primes).

## Concerns

In severity order:

### C1. Manuscript-Lean alignment: conjecture statement in `proof.tex` does not mention "distinct moduli."

**Status:** Manuscript polish issue, NOT a math issue.

**What:** `manuscript/proof.tex` Conjecture 1 (line 70–75) currently
reads:
> Does there exist a covering system $\{ a_i \pmod{m_i} \}_{i=1}^{k}$
> of $\mathbb{Z}$ such that each modulus $m_i$ has the form
> $m_i = p_i - 1$ for some prime $p_i \geq 5$?

The Lean `Erdos273Conjecture` requires `C.IsStrict` (distinct moduli).
The manuscript wording is faithful to Erdős–Graham 1980 (which uses
"covering system" with implicit distinct moduli per its earlier
definition in the same paper), but a reader who doesn't know the
literature convention might miss the strictness requirement.

**Falsification test:** point the reader at Section "Covering system"
(line 57) — does it explicitly require distinct moduli? Reading
lines 56–66: "A *covering system* of the integers is a finite
collection of arithmetic progressions $\{ a_i \pmod{m_i} \}_{i=1}^{k}$,
$m_i \geq 2$, whose union is $\mathbb{Z}$." This does *not* require
distinct moduli. Without strictness, the conjecture is trivially
provable (witness `{0, 1, 2, 3} mod 4`), and the entire density
argument loses its bite.

**Resolution:** Before promoting Part B's theorems to `[verified]`,
the manuscript should:
- Either add "with distinct moduli $m_1 < m_2 < \cdots < m_k$" to
  the covering-system definition or to Conjecture 1.
- Or add a remark immediately after Conjecture 1 explaining that
  the standard literature convention (Erdős–Graham 1980;
  DeepMind formal-conjectures `StrictCoveringSystem`) requires
  distinct moduli, and that this is the convention used throughout.

This is the kind of tightening `/solve` would normally do as part
of the promotion edit. **Important for the promotion to be honest;
not blocking if the promotion edit fixes it inline.**

### C2. Two unused hypotheses (`_hStrict`) signal an opportunity for cleaner statements.

**Status:** Cosmetic. Not blocking.

**What:** `strict_covering_density_bound` and
`strict_covering_reciprocal_bound` take an `hStrict` /
`_hStrict` argument that is not used in their proof bodies. The
docstrings disclose this honestly ("strictness is included as a
hypothesis for downstream users").

**Why it matters:** the *name* `strict_covering_*` suggests the
bound depends on strictness, when in fact it does not. The actual
strictness-dependent bound is `no_strict_cover_of_low_density`. A
future reader (or a /solve session trying to apply these lemmas)
might assume strictness is required when it is not.

**Suggested cleanup (optional, post-promotion):**
- Rename `strict_covering_density_bound` → `covering_density_bound`,
  drop the `_hStrict` argument.
- Rename `strict_covering_reciprocal_bound` →
  `covering_reciprocal_bound`, drop the `hStrict` argument.
- `no_strict_cover_of_low_density` stays as-is since it genuinely
  uses strictness.

This is a refactor for a follow-up session, not a blocker for
promotion. The current names are honest given the disclosed
docstrings.

### C3. The 27720 corollary's `sorry` is acknowledged correctly but the manuscript should clearly tag the corollary as `[sketch]`.

**Status:** Already handled in the Lean file's comments
("`[sketch]` and is not promoted to `[verified]`"). Just confirming
this convention propagates to the manuscript.

**What:** When `/solve` writes the manuscript entry for
`no_strict_admissible_cover_27720`, it must use a `% [sketch]`
comment (NOT `% [verified: …]`), and the theorem footnote should
mention the deferred `D(27720) < 1` rational-arithmetic step. If
the manuscript inadvertently promotes the 27720 corollary to
`[verified]`, that would be a fabrication.

The Part B chain (the abstract obstruction + per-class count + union
bound + reciprocal bound) IS ready for `[verified]` promotion. The
27720 corollary is NOT.

### C4. Strictness-as-stored-hypothesis style — minor naming nitpick (already covered by C2).

See C2. No additional concern.

## Stronger-than-target test

The verified Part B lemmas, combined with the (numerical-only)
`D(27720) < 1` fact, would imply: any strict cover of ℤ by
M-moduli must use a modulus whose LCM doesn't divide 27720 (i.e.,
LCM must be divisible by some prime power not in
`{2^3, 3^2, 5, 7, 11}`). This is a partial *non-existence* result,
which is honest progress on the open problem — but it does NOT
settle the conjecture (positive or negative).

If the lemmas accidentally implied a *full* resolution of Erdős
#273, that would be a red flag. They do not: the abstract
obstruction `no_strict_cover_of_low_density` only rules out covers
whose moduli are a subset of some FINITE M with D(M) < 1. The
literature (BBMST 2022 §2.1 of the librarian survey) explicitly
notes that for the infinite set $\mathcal{M} = \{p-1 : p \geq 5
\text{ prime}\}$, $\sum_{m \in \mathcal{M}} 1/m$ diverges (Mertens-style).
So the density argument cannot be lifted to the full conjecture
without additional structural input. **The Lean lemmas correctly
stop short of overreach.**

## Recommendations to the orchestrator

Before promoting the Part B chain to `[verified]` in
`manuscript/proof.tex`:

1. **Promote the Part B chain to `[verified]`.** Specifically
   eligible:
   - `card_covered_eq`
   - `density_union_bound`
   - `strict_covering_density_bound`
   - `strict_covering_reciprocal_bound`
   - `no_strict_cover_of_low_density`
   - `non_strict_erdos273_trivially_solvable` (the sanity-check
     witness — verified and useful for the manuscript's discussion
     of why strictness is required)
   - `isStrict_iff` (the IsStrict ↔ IsStrict' equivalence)
   - `admissibleModulus_iff`, `four_le_of_admissible`,
     `admissibleModulus_below_60` (utility lemmas, all axiom-clean)

2. **Tag `no_strict_admissible_cover_27720` as `[sketch]`** in the
   manuscript entry, with a footnote noting the deferred
   `D(27720) < 1` step.

3. **(C1 fix) Add strictness to the manuscript's conjecture
   statement.** Edit `Section: Introduction`, either:
   - Add to the covering-system definition (line 57–66) the phrase
     "with distinct moduli $m_1 < m_2 < \cdots < m_k$" so that
     Conjecture 1 inherits strictness implicitly; or
   - Add a remark after Conjecture 1: "We follow the standard
     literature convention requiring distinct moduli; see
     Erdős–Graham 1980 §… and DeepMind `formal-conjectures`
     `StrictCoveringSystem`."

4. **(Optional, C2) Plan a future session for the rename refactor.**
   Drop the unused `hStrict` argument from
   `strict_covering_density_bound` and
   `strict_covering_reciprocal_bound`. This is post-promotion
   cleanup, not a blocker.

5. **Do NOT promote `no_strict_admissible_cover_27720`.** Keep it
   `[sketch]`. The orchestrator may also choose to open a new
   sub-goal "discharge `D(27720) < 1` by exact ℚ computation in
   Lean" for a future session.

## Bottom line

The Part B chain is mathematically correct, axiom-clean (all 12
non-sketch theorems list only `{propext, Classical.choice,
Quot.sound}`), and ready for `[verified]` promotion. The 27720
corollary's `sorry` is correctly disclosed and should stay
`[sketch]` until the rational-arithmetic step is discharged.

The manuscript needs a one-sentence edit to make the strictness
convention explicit (caveat C1) — this should happen at the same
time as the promotion edit, not later.

Verdict: **PASS with caveats.** The math is sound; the caveats
are about manuscript hygiene at promotion time, not about the
Lean artifacts.
