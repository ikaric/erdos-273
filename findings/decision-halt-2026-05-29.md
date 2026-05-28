# Decision: close V2 + V3 as documented dead-ends; halt `/loop /solve` to `/vector`

**Author:** orchestrator (/solve), session 6, 2026-05-29
**Context:** no user input available (autonomous mode); decision recorded per CLAUDE.md.

## What happened

The seeded ROADMAP for Erdős #273 had five attack vectors (V1–V5) plus a
literature-survey sub-lemma. After six sessions:

| Vector | Issue | Outcome |
|---|---|---|
| V1 SAT search | #3 | **Closed.** Script delivered; density theorem supersedes for $L\le27720$. |
| V4 Mathlib formalization | #6 | **Closed.** `CoveringSystem` + density bound + ℤ-form API verified. |
| V5 range extension | #7 | **Closed.** Verified obstructions at $L=27720,83160,180180$. |
| V2 distortion non-existence | #4 | **Dead end** (this decision). |
| V3 min-modulus argument | #5 | **Dead end** (this decision). |

The two remaining vectors, V2 and V3, are both flavors of the
**distortion method** (Hough 2015 / BBMST 2022 / CFT 2022) — the only
known non-existence technique beyond the elementary density bound. This
session rigorously established that the distortion method **cannot be
sharpened for 𝓜**:

- **Density lever (V2's BBMST density theorem):** the signed/unsigned
  reciprocal sums over 𝓜 diverge (Mertens). `DensityDivergence.lean`
  *verifies* $\sum_{m\in\mathcal{M}}1/m=\infty$. So the density theorem
  is inapplicable.
- **Divisibility-pair lever (V2, Schinzel/BBMST Thm 1.2):** trivially
  satisfied by 𝓜 and strictly subsumed by the verified density bound
  (`lit-V2-divisibility-2026-05-28.md`).
- **Distortion sharpening (V3):** `heur-cft-hyperplane-2026-05-28.md`
  proves (25-digit numerical verification of an algebraic identity) that
  the $1/(p-1)$ density is *invisible* to the CFT hyperplane count —
  every finite prime-support pattern is 𝓜-realizable by Dirichlet, so the
  method counts the same patterns and yields only the inherited
  CFT/BBMST bound, nothing 𝓜-sharpened. The validated squarefree engine
  (`cft_validate_squarefree.py`, matching CFT to 8 sig figs) confirms the
  engine is correct; the obstruction is intrinsic, not a bug.

## Decision

Close #4 and #5 with the `deadend` label (concrete, proven obstructions —
not defeatism). This ticks the ROADMAP to 6/6, which triggers the
`/loop /solve` target-reached **halt**.

**The conjecture itself remains OPEN.** The 6/6 meter means *all seeded
attack vectors are explored*, not that Erdős #273 is solved. The
manuscript correctly tags it as `Conjecture` with verified *partial*
results. Per the anti-overreach contract, /solve does not invent a
bigger contract; the strategic pivot to new directions is the user's
call via `/vector`.

## Recommended `/vector` directions (for the user)

The seeded attack was entirely **non-existence** flavored, and both
non-existence levers are now exhausted. Genuinely unexplored directions:

1. **Construction / existence search.** No vector targeted *building* an
   explicit 𝓜-covering at periods $L$ with $D(L)\ge 1$ (the smallest is
   $L=55440$). The BBMST bound says any distinct-moduli covering has a
   modulus $\le 616000$; 𝓜's minimum modulus is 4, so an 𝓜-covering is
   not excluded a priori. A focused ILP/SAT construction search at
   $L\in\{55440, 110880, \dots\}$ with 𝓜-restricted moduli could find an
   explicit covering (resolving the conjecture **affirmatively**) or
   give structured evidence. V1's SAT work timed out for large $L$ but
   did not specifically target the $D(L)\ge1$ regime with optimized
   encodings.

2. **The "all moduli even" structural lever.** Every $m=p-1$ with
   $p\ge5$ prime is **even** and $\ge4$, so $\mathcal{M}\subset
   2\mathbb{Z}_{\ge4}$. Whether covering $\mathbb{Z}$ with *distinct even
   moduli $\ge4$ drawn from the sparse set $\{p-1\}$* carries a parity /
   2-adic obstruction is unexplored and is not a distortion argument.

3. **Effective bounds / accept current state.** Alternatively, accept
   the verified partial results (density obstruction + three explicit
   period bounds + the divergence cap) as the deliverable and run
   `/polish` for the final manuscript pass.

## Why not auto-open one of these now

Anti-overreach: these are **new strategic postures** (existence vs
non-existence; structural vs analytic), not "filling toward" the seeded
contract. Construction search also risks spinning (covering-system SAT is
exponential; V1 already timed out). The deliberate choice among them
belongs to `/vector`, not to an autonomous /solve iteration.
