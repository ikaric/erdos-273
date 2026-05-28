# Critic review — polished manuscript (Erdős #273)

Date: 2026-05-29
Reviewer: critic (adversarial)
Scope: `manuscript/proof.tex` prose, cross-checked against
`formal/Erdos273/*.lean`. READ-ONLY review; no `lake build` was run
(per task constraint), so build-status concerns below are flagged for
the formalist/build to confirm, not independently compiled here.

---

## Verdict: REVISION REQUIRED

Two concrete fixes are required (R1, R2). One (R1) is a factual
mathematical misstatement in a proof; the other (R2) is a suspected
compile-breaker in a file the manuscript footnotes as `[verified]`,
which — if confirmed — downgrades three headline theorems. Everything
else (arithmetic, citations, abstract/body consistency, scaffolding,
overclaim discipline, appendix verbatim quotes) checks out. The
manuscript correctly presents #273 as OPEN and itself as proving only
partial results; no overclaim against the conjecture.

---

## Required fixes

### R1 (mathematical, prose). "Multiples of 108" mischaracterises the eleven new moduli at L = 83160.

- Location: §3, proof of Theorem 3.4 (numerical-83160), line ~363:
  "the eleven new moduli being precisely the admissible multiples of
  108 = 109 − 1 made available by the third factor of 3." Same wrong
  description echoed in the docstring of
  `formal/Erdos273/NumericalBound83160.lean` (lines ~8, ~58–60: "all
  multiples of 108 = 109 − 1").
- Claim: the 11 moduli in `M_{83160} \ M_{27720}` are *precisely the
  admissible multiples of 108*.
- Status: **wrong.** The set is
  `{108, 270, 378, 540, 756, 2376, 2970, 4158, 7560, 8316, 16632}`,
  and 4 of these — 270, 378, 2970, 4158 — are NOT multiples of 108
  (270/108 = 2.5, 378/108 = 3.5, 2970/108 = 27.5, 4158/108 = 38.5).
- Correct characterisation: these are exactly the admissible divisors
  of 83160 that are divisible by 3³ = 27 (equivalently, that do not
  divide 27720 because they need the third factor of 3). Verified: all
  11 are divisible by 27; none divides 27720.
- Impact: the *theorem itself is fine* — `M_{83160}` is the correct
  45-element set and D(83160) = 27241/27720 < 1 is correct. Only the
  parenthetical description of the new moduli is false. Fix the prose
  (and the Lean docstring) to "the admissible divisors of 83160
  requiring the full 3³, i.e. those divisible by 27" or similar.
- Falsification test (already run):
  `[m for m in {108,...,16632} if m % 108]` is non-empty
  (`{270,378,2970,4158}`); `all(m % 27 == 0)` is True.

### R2 (formal / build). Suspected invalid tactic `push Not` in IntegerForm.lean.

- Location: `formal/Erdos273/IntegerForm.lean` line 133:
  `push Not at hAll` inside `erdos273_modulus_not_dividing_27720`.
- Concern: the standard Mathlib tactic is `push_neg`. `push Not` is
  not a Lean/Mathlib tactic and is not defined as a macro anywhere in
  `formal/` (grepped). If this is a typo that does not elaborate, then
  `IntegerForm.lean` does not compile.
- Load-bearing consequences if it does not build:
  - `erdos273_modulus_not_dividing_27720` — quoted *verbatim* in
    Appendix A (lines 651–654) and footnoted `[verified]` on
    Corollary 3.3 — is not verified.
  - `no_strict_admissible_covering_Z_27720` (Thm 3.2 footnote) lives
    in the same file → not verified.
  - `NumericalBound83160.lean` and `NumericalBound180180.lean` both
    `import «Erdos273».IntegerForm`, so Theorems 3.4 and 3.5
    (`no_strict_admissible_covering_Z_83160`,
    `...Z_180180`) would fail to build transitively.
  - The Appendix A "Axiom witness" table (lines 672–691) lists all of
    these as "clean" — that table would be asserting an axiom report
    that was never produced.
- This is the single most load-bearing item: it gates four of the six
  headline `[verified]` claims and the entire axiom-witness table.
- Action: formalist must (a) replace `push Not` with `push_neg` (or
  confirm a local macro provides it), and (b) re-run `lake build` +
  `#print axioms` on `erdos273_modulus_not_dividing_27720`,
  `no_strict_admissible_covering_Z_27720`,
  `no_strict_admissible_covering_Z_83160`,
  `no_strict_admissible_covering_Z_180180` to confirm the axiom set is
  `{propext, Classical.choice, Quot.sound}` before the `[verified]`
  tags and the Appendix A table stand. Until confirmed, treat these
  four as `[sketch]`.
- Falsification test: `(cd formal && lake build «Erdos273».IntegerForm)`
  — expected to error on line 133 if `push Not` is a typo.

---

## What checks out (no action)

All independently recomputed in exact `fractions.Fraction` arithmetic.

1. **Core arithmetic — all correct.**
   - 27720 = 2³·3²·5·7·11 has 96 divisors; 34 admissible; D = 953/990
     ≈ 0.9626 < 1. Lemma 2.5's explicit 34-element list matches the
     computed set exactly. Range "4 (p=5) … 9240 (p=9241)" correct
     (9241 is prime).
   - 83160 = 2³·3³·5·7·11 has 128 divisors; 45 admissible; D =
     27241/27720 ≈ 0.9827 < 1. |M_{83160} \ M_{27720}| = 11 (abstract's
     "eleven further admissible moduli" — correct count).
   - 180180 = 2²·3²·5·7·11·13 has 144 divisors; 47 admissible; D =
     173003/180180 ≈ 0.9602 < 1. The 21 new-vs-M_{27720} moduli listed
     in the Lean docstring match exactly. 27720 ∤ 180180 (2³→2²), so
     the independence claim ("different family of covers") is correct;
     52 = 53−1 enters via the new prime 13 (53 prime — correct).
   - Concluding remarks: smallest L with D(L) ≥ 1 is 55440 = 27720·2,
     D = 6429/6160 ≈ 1.0437 — confirmed as the GLOBAL minimum by
     brute scan of all L ≤ 60000. Next chain period 360360 has D ≈
     1.0237 — correct. The 2-adic chain exits at k=1, 3-adic stays
     below 1 through k=3 — consistent.
   - Selfridge lcm(2,3,4,5,6,8,9,10,12) = 360 — correct. (Minor
     expository looseness: "all of which are of the form p−1 for
     p ∈ {3,5,7}" reads as applying to the lcm-arguments listed, of
     which 8,9,10,12 are not of that form; this is an attribution
     sentence, not load-bearing. Optional tightening only.)

2. **Prose ↔ Lean theorem statements — faithful, no silent
   strengthening.**
   - Thm 2.4 (density bound) ↔ `strict_covering_density_bound`:
     prose ∑1/m ≥ 1 ⇔ Lean `L ≤ ∑ L/m`; the rational form is the
     separate `strict_covering_reciprocal_bound`. Match.
   - Cor 2.6 ↔ `no_strict_cover_of_low_density`. Match.
   - Thms 3.2/3.4/3.5 say "moduli all lie in 𝓜 AND all divide L";
     Lean uses `AdmissibleModulus c.modulus ∧ c.modulus ∣ L`. Match.
   - The three Appendix-A "verbatim" quotes
     (`strict_covering_density_bound`,
     `erdos273_modulus_not_dividing_27720`,
     `admissible_reciprocal_not_summable`) are byte-faithful to the
     `.lean` sources.
   - Prop 4.2 (divergence): prose claims ∑_{m∈𝓜} 1/m = ∞; Lean proves
     `¬ Summable (fun p : Nat.Primes ↦ 1/((p:ℝ)−1))` over ALL primes.
     This indexes p ≥ 2 rather than p ≥ 5, but the prose proof
     explicitly notes "restoring or omitting the finitely many terms
     with p < 5 changes the sum by a finite amount," so divergence is
     equivalent. Honest, not an overclaim.

3. **No resolution overclaim.** Conjecture 1.1 is stated as a question
   and the intro (lines 142–145, 160–162) states it "appears to be open
   as of 2026" and that the L=27720 result "does not refute" it. The
   main-result paragraph frames everything as a lower bound on
   structural complexity. Abstract matches: "We prove a density
   obstruction… ruling out any strict admissible covering whose moduli
   all divide L." No claim to settle #273.

4. **Distortion-method paragraph (§4, lines 494–532) — honest, not
   overclaimed.** The argument is presented as a reasoned obstruction
   backed by "a numerical reconstruction of that optimisation," and the
   conclusion is hedged correctly: "A genuinely sharper non-existence
   result, *if one exists*, must come from a mechanism that sees more
   than the prime-support patterns." It does NOT assert a theorem of
   impossibility. (Note: STATUS.md uses the stronger word "the analyst
   *proved* the distortion method cannot be sharpened" — that wording
   is fine for an internal status file but should not migrate into the
   manuscript; it has not.) No fix required in the manuscript.

5. **Citations.** All six `\cite{}` keys (ErdosGraham1980, Hough2015,
   BBMS2022, CummingsFilasetaTrifonov2022, FormalConjectures,
   Biere2024CaDiCaL) resolve to `\bibitem` entries with venues / arXiv
   IDs (1307.0874, 1811.03547, 2211.08548) / URLs. No dangling or
   invented citations; no "folklore" presented as cited.

6. **No banned scaffolding.** No "Step 1/2/3", "Critic review PASS",
   "Initial attack vectors", "Revision history", "Top-3", "Current
   focus". The only `[verified:`-string hits are the `%`-comment form
   above theorem environments (the prescribed pattern), never inline
   in theorem headers.

7. **SAT appendix (§B) honest.** Explicitly states SAT outputs are
   "not, on their own, machine-checked" and that the verified Thm 3.1
   "does not depend on the SAT solver." `[numerical: …]` tag on
   Remark 3.6 is appropriate.

---

## Summary for /solve

- **R1**: fix the false "multiples of 108" description in the Thm 3.4
  proof (line ~363) and in the `NumericalBound83160.lean` docstring →
  "admissible divisors of 83160 divisible by 3³ = 27." Prose-only;
  theorem unaffected.
- **R2**: `push Not` (IntegerForm.lean:133) is a suspected typo for
  `push_neg`; dispatch formalist to fix and re-run `lake build` +
  `#print axioms` on the four affected `Z_` theorems. Until the build
  + clean-axiom report is confirmed, the `[verified]` tags on
  Corollary 3.3 / Theorems 3.2, 3.4, 3.5 and the Appendix-A axiom table
  are not substantiated.

Upgrade to PASS once R1 is corrected and R2's build + axiom report are
confirmed clean.

---

## Orchestrator resolution (2026-05-29)

Both findings addressed; verdict upgraded to **PASS**.

**R1 — corrected.** The "precisely the admissible multiples of 108" claim
was indeed false (270, 378, 2970, 4158 are not multiples of 108; all 11
new moduli are, however, divisible by 3³ = 27). Fixed in:
- `manuscript/proof.tex` §3 proof of Thm~\ref{thm:numerical-83160}: now
  "the admissible divisors of 83160 divisible by 3³ = 27 … which 27720
  lacks (the smallest is 108 = 109−1)."
- `formal/Erdos273/NumericalBound83160.lean` docstrings (three comment
  occurrences) — comment-only edits; the theorem, the 45-element set, and
  D(83160) were always correct (critic confirmed "the theorem itself is
  unaffected"). Re-built: all six theorems remain axiom-clean.

**R2 — false alarm (confirmed by build).** `push Not at hAll`
(`IntegerForm.lean` line 133) is valid: `push` is a current Mathlib tactic
and `push Not` pushes negations (the generalisation of `push_neg`). The
critic flagged it only because the review was read-only and could not
build. Targeted rebuild confirms:
`Erdos273.erdos273_modulus_not_dividing_27720 depends on axioms:
[propext, Classical.choice, Quot.sound]`, and the full `lake build`
completes (8478–8483 jobs) with every IntegerForm / NumericalBound83160 /
NumericalBound180180 theorem axiom-clean. All four headline `[verified]`
tags and the Appendix-A "clean" rows are substantiated.

Everything else in the review checked out (divisor counts, D(L) values,
55440/360360 numerics, faithful prose↔Lean correspondence, honest
open-conjecture framing, hedged distortion paragraph, resolved citations,
no scaffolding). **PASS.**
