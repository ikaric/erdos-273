# Polish audit — manuscript/proof.tex (2026-05-29)

**Mode:** full polish (ROADMAP 6/6; 11 `[verified]` tags, 1 `[numerical]`, 0 `[sketch]`).

The manuscript is already largely publication-style — the `/solve` sessions
kept it clean. No placeholder abstract, no banned sections/phrases, no
unresolved citations, all five headline statements carry the
formal-verification footnote, all proofs are real `\begin{proof}` blocks.
The audit findings are therefore narrow, concentrated on the
formal-verification appendix.

## Findings

- [x] [abstract] Real abstract present, summarises density obstruction +
      27720/83160/180180 bounds + Lean verification. OK.
- [x] [intro] States problem, history (Selfridge, Hough, BBMST), main
      result, proof strategy, open-status. OK.
- [x] [footnotes] All 5 headline statements (thm:density,
      thm:numerical-27720, thm:numerical-83160, thm:numerical-180180,
      prop:density-diverges) carry the "Formally verified in Lean 4 +
      Mathlib" footnote. Aux lemmas correctly catalogued in the appendix,
      not footnoted individually. OK.
- [x] [proofs] Every theorem/lemma/prop/cor has a real proof block; no
      `\begin{sketch}`, no "Step 1/2" labels. OK.
- [x] [banned] grep for banned sections/phrases: none. OK.
- [ ] [appendix-snippet] **The Formal verification appendix catalogues the
      Lean theorems by name/file but does NOT quote any statement
      verbatim.** Modern formalisation-paper standard (Mathlib/PFR/LTE
      papers) is to quote the headline Lean statements so the reader sees
      the exact correspondence. Add verbatim snippets for the headline
      trio: `strict_covering_density_bound`,
      `erdos273_modulus_not_dividing_27720`, `admissible_reciprocal_not_summable`.
- [ ] [appendix-table] No explicit axiom-witness table. Add a compact
      table: headline theorem → Lean file → axioms (all clean).
- [ ] [appendix-reproduce] No "reproducing the verification" steps. Add the
      standard 3-step block (clone → `lake exe cache get && lake build` →
      `#print axioms`).
- [ ] [preamble] No `listings`/verbatim package. Add `\usepackage{listings}`
      with a `literate` block mapping the Lean Unicode (ℕ ℤ ℝ ∈ ∀ ∃ ∣ ≤ ∑
      → ∧ ¬ ↦) to LaTeX math, so snippets render font-independently under
      tectonic/XeLaTeX.
- [ ] [minor xref] Intro line ("see Section~\ref{sec:numerics}" for SAT
      confirmation) could also point to Appendix~\ref{sec:sat} where the
      SAT encoding is detailed. Minor.

## Out of scope (flag, do not act)

The conjecture itself is open; both non-existence levers are exhausted
(density Mertens-capped, distortion un-sharpenable for 𝓜). `/polish` does
not open vectors. The verified partial results are the deliverable.
