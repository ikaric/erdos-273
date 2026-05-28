# V2 analysis — the divisibility-pair theorem (Schinzel's conjecture) and what it forces for 𝓜-coverings

**Author:** combinatorialist
**Session:** 2026-05-28
**Vector:** V2
**Subject:** Pin the exact "every covering contains a divisibility pair" theorem, specialize the divisibility poset of 𝓜 = {p−1 : p prime, p ≥ 5}, and assess whether it gives any leverage beyond the verified reciprocal-sum density bound (L = 27720, in-progress L = 83160).

**Bottom line (read this first).** The theorem is real, sharp, and correctly attributed: it is **Schinzel's 1967 conjecture**, proved as **Theorem 1.2 of Balister–Bollobás–Morris–Sahasrabudhe–Tiba, *On the Erdős covering problem: the density of the uncovered set*, Inventiones math. 228 (2022), 377–414, arXiv:1811.03547**. It says: *any finite covering system of ℤ has two moduli, one dividing the other*. **But for 𝓜 it gives essentially no new leverage.** On every divisor lattice the project actually attacks (L | 27720, L | 83160, …) the antichain-exclusion content of Theorem 1.2 is **strictly subsumed by the elementary reciprocal bound Σ 1/mᵢ ≥ 1 that the project already verifies**: the maximum reciprocal sum of *any* divisibility-antichain inside M_27720 is 371/660 ≈ 0.562 < 1, so antichain coverings are killed by density alone, long before Theorem 1.2 is needed. Theorem 1.2 is a deep theorem about *general* moduli sets; on 𝓜 it is not the binding constraint. **Recommended posture: cite it as context, do not build a vector on it.** There is one small, honest, formalizable structural sub-lemma (below), but its value is modest.

---

## 1. The exact theorem and citation

**Verbatim statement (from arXiv:1811.03547, just before §1's Theorem 1.2, read directly from the PDF):**

> "Schinzel [10] showed that if no such [Erdős–Selfridge odd] covering system exists, then for every polynomial f(x) ∈ ℤ[X] with f ≢ 1, f(0) ≠ 0 and f(1) ≠ −1, there exists an (infinite) arithmetic progression of values of n ∈ ℤ such that xⁿ + f(x) is irreducible over the rationals. He also showed that this would imply the following statement: in any covering system, one of the moduli divides another. In Section 9 we will prove this latter statement, known as Schinzel's conjecture.
>
> **Theorem 1.2.** If 𝒜 is a finite collection of arithmetic progressions that covers the integers, then at least one of the moduli divides another."

**Attribution.**
- **Conjectured:** Andrzej **Schinzel, 1967** ([10] in BBMST = Schinzel, *Reducibility of polynomials and covering systems of congruences*, Acta Arith. 13 (1967), 91–101). Schinzel's motivation was the **reducibility of polynomials xⁿ + f(x)**; the covering-divisibility statement is the combinatorial residue of that program, and is tied to the Erdős–Selfridge odd-covering question.
- **Proved:** **Balister, Bollobás, Morris, Sahasrabudhe, Tiba (2022)**, Theorem 1.2, arXiv:1811.03547, Inventiones 228 (2022) 377–414, §9. The proof reuses the distortion-method density machinery developed for their main density theorem (Theorem 1.1).

**Equivalent Erdős-problem framing.** The contrapositive is **Erdős Problem #586**: *"Is there a covering system such that no two of the moduli divide each other?"* — status **DISPROVED** by BBMST22 (erdosproblems.com/586, verified this session). #586 was "asked by Schinzel, motivated by a question of Erdős and Selfridge." So "covering ⇒ divisibility pair" = "no antichain-covering exists" = #586-negative = BBMST Thm 1.2. All three are the same statement.

**Precise hypotheses — important, and cleaner than one might guess:**
- **Finite collection of arithmetic progressions covering ℤ.** That is the *only* hypothesis.
- **No distinctness assumption.** The theorem does **not** require distinct moduli. (Trivially: if two moduli are equal, one divides the other, so the interesting content is exactly the distinct-moduli case, but the theorem as stated is unconditional on distinctness.) The phrase "no two of the moduli divide each other" in #586 carries the distinctness implicitly, since equal moduli divide.
- **No minimum-modulus hypothesis**, **no "all moduli > M"**, **no bound on the number of progressions** beyond finiteness. This is a genuinely clean, hypothesis-light theorem — unlike Theorem 1.1 (the density theorem), which needs minimum modulus ≥ M(ε).

**Status of the surrounding folklore, to be honest about what is theorem vs conjecture:**
- "Every covering has a divisibility pair" — **THEOREM** (BBMST22). Not folklore, not conjecture (as of 2022).
- Schinzel's *polynomial-irreducibility* statement (the xⁿ+f(x) consequence) is conditional on the **Erdős–Selfridge odd-covering** question, which **remains OPEN** (Erdős Problem #7, $25/$2000 prizes). So Schinzel's *original application* to polynomial reducibility is still conditional; only the combinatorial covering-divisibility statement was unconditionally settled.

---

## 2. The divisibility poset (𝓜, |)

𝓜 = {4, 6, 10, 12, 16, 18, 22, 28, 30, 36, 40, 42, 46, 52, 58, 60, 66, 70, 72, 78, 82, …} = {p−1 : p ≥ 5 prime}.

### 2.1 The divisibility relation, combinatorially

For m = p−1 and m' = p'−1 in 𝓜, "m | m'" is just integer divisibility of the shifted primes; there is **no multiplicative structure linking p−1 and p'−1** (the map p ↦ p−1 destroys the prime structure). So (𝓜, |) is best described as: 𝓜 is an explicit, density-≈ N/(2 log N) subset of the even integers ≥ 4, inheriting the divisibility order from (ℤ₊, |). Concretely (computed this session, sympy):

- **4 | {12, 16, 28, 36, 40, 52, 60, 72, 88, 96, 100, 108, 112, 136, 148, 156, 172, 180, …}** (𝓜-multiples of 4 = the m ∈ 𝓜 with 4 | m, i.e. p ≡ 1 mod 4).
- **6 | {12, 18, 30, 36, 42, 60, 66, 72, 78, 96, 102, 108, 126, …}** (p ≡ 1 mod 6, i.e. p ≡ 1 mod 3 since p odd).
- **10 | {30, 40, 60, 70, 100, 130, 150, 180, 190, …}** (p ≡ 1 mod 5).
- **12 | {36, 60, 72, 96, 108, 156, 180, 192, …}**, **18 | {36, 72, 108, 126, 162, 180, 198}**, **16 | {96, 112, 192}**, **22 | {66, 88, 198}**, etc.

A pair (m, m') with m | m' in 𝓜 ⟺ primes p, p' ≥ 5 with (p−1) | (p'−1). E.g. 4|12 ↔ (5−1)|(13−1); 6|18 ↔ (7−1)|(19−1); 10|30 ↔ (11−1)|(31−1).

### 2.2 Minimal elements (an explicit infinite antichain)

The **minimal elements** of (𝓜, |) — those m ∈ 𝓜 divisible by no smaller element of 𝓜 — are pairwise incomparable, hence form an antichain. First ones:

> 4, 6, 10, 22, 46, 58, 82, 106, 166, 178, 226, 238, 262, 346, 358, 382, 442, 466, 478, 502, 562, 586, 646, 658, 718, …

Density of minimal elements among 𝓜: ≈ **12%** up to 5·10⁴ (621 of 5131). Structurally, after the three "small" exceptions 4, 6, 10, almost every minimal element has the shape **2q with q an odd prime** (22 = 2·11, 46 = 2·23, 58 = 2·29, 82 = 2·41, 106 = 2·53, …): if q is prime then 2q's only divisors are 1, 2, q, 2q, and none of 2, q lies in 𝓜 generically, so 2q is minimal whenever 2q ∈ 𝓜 (i.e. 2q+1 prime). This is the cleanest infinite antichain.

### 2.3 Are there infinite antichains in (𝓜, |)? YES — provably.

**Provable infinite antichain (no conjecture needed).** The set of **minimal elements** of (𝓜, |) is infinite: 𝓜 is infinite (Dirichlet — infinitely many primes), and an infinite subset of ℤ₊ cannot be covered by finitely many principal divisibility up-sets unless it has infinitely many minimal elements (if there were finitely many minimal elements m₁,…,m_r, every element of 𝓜 would be a multiple of some mᵢ, but the multiples of a fixed mᵢ inside 𝓜 have density ≤ 1/mᵢ of 𝓜's counting function, and a finite union of these cannot exhaust the full PNT-density of 𝓜 — contradiction). Hence **(𝓜, |) has an infinite antichain, unconditionally.** This matters: it means one *cannot* dismiss 𝓜-coverings by "𝓜 is a chain-like / well-ordered set."

**Conjecturally infinite, cleaner antichain.** {2q : q prime, 2q+1 prime} (so 2q ∈ 𝓜): 6, 10, 22, 46, 58, 82, 106, 166, 178, 226, 262, 346, …. Here 2q | 2q' ⟺ q | q' ⟺ q = q' (primes), so this is an antichain by inspection. Infinite **iff** there are infinitely many primes q with 2q+1 prime (a Sophie-Germain-type / Dickson-conjecture statement — believed, not proved). The minimal-elements antichain in the previous paragraph is the unconditional substitute.

### 2.4 Chains

Chains exist and are long. The longest divisibility chain inside 𝓜 ∩ [1, 5·10⁴] has **length 9**:

> 4 | 12 | 36 | 108 | 540 | 1620 | 4860 | 9720 | 19440

(each step a genuine 𝓜-element: 5−1, 13−1, 37−1, 109−1, 541−1, 1621−1, 4861−1, 9721−1, 19441−1 are all prime). So (𝓜, |) has both unboundedly long chains and infinite antichains — it is a "generic" infinite poset, neither a chain nor an antichain.

---

## 3. The actual leverage of Theorem 1.2 on 𝓜 — honest negative assessment

**Claim: Theorem 1.2 gives no new obstruction beyond what the project already has.** Three independent reasons.

### 3.1 𝓜 is full of divisibility pairs, so the conclusion is trivially compatible with an 𝓜-covering

Theorem 1.2 only says a covering *must contain* a pair m | m'. Since 𝓜 contains a huge supply of such pairs (4|12, 6|12, 6|18, 10|30, 4|16, 12|36, …), the conclusion places **no restriction whatsoever** on the existence of an 𝓜-covering: any putative 𝓜-covering can trivially include a divisibility pair. Theorem 1.2 would only be an *obstruction* if 𝓜 were an antichain (then no covering could live in 𝓜). 𝓜 is not an antichain. **So as a non-existence tool, Theorem 1.2 is vacuous for 𝓜.** (This is already noted, correctly, in the prior survey lit-covering §2.3 and lit-V3 §2.5 — V2 confirms it concretely.)

### 3.2 The only "structural" use — forbidding antichain-coverings — is strictly weaker than the verified density bound on the relevant lattices

The one way Theorem 1.2 could bite is the contrapositive lever: *"an 𝓜-covering cannot use a set of moduli that forms a divisibility antichain."* This would matter only if someone tried to construct an 𝓜-covering from a minimal-elements / Sophie-Germain antichain. But this is already excluded — more cheaply — by the elementary necessary condition **Σ 1/mᵢ ≥ 1** that the project's verified results rest on. Computation this session:

- Max reciprocal sum over **any divisibility-antichain inside M_27720** (= 𝓜 ∩ div(27720), 34 elements): the optimum is the antichain **{4, 6, 10, 22}** with Σ 1/m = **371/660 ≈ 0.562 < 1**.
- The all-minimal antichain {4, 6, 10, 22} already maxes this out; adding any further 𝓜-element to keep an antichain only lowers (or barely changes) the sum since the next candidates (28, 46, 58, …) are large.
- Even the unconstrained best small antichain {4, 6, 10} gives 31/60 ≈ 0.517 < 1.

So on the divisor lattice L = 27720 (and a fortiori on every sublattice the SAT search and the L = 83160 extension cover), **any antichain of 𝓜-moduli has Σ 1/m < 1 and therefore cannot cover ℤ for the elementary reason — no appeal to Theorem 1.2 needed.** The project's verified `D(27720) = 953/990 < 1` bound is over the *entire* admissible set, which dominates any antichain subset; Theorem 1.2's antichain-exclusion is a strictly weaker consequence. **Net: Theorem 1.2 is subsumed by the density bound the project already verifies.**

### 3.3 Combining Theorem 1.2 with the density bound yields nothing new

The density obstruction (Σ 1/m < 1 over moduli dividing L) already excludes *all* L-coverings, antichain or not, for L ∈ {12, 60, 120, 360, 840, 2520, 27720} (verified) and the in-progress 83160. Theorem 1.2 restricts only to the antichain case, a sub-case already inside the density net. There is no "if smallest modulus is 4 and there is a divisibility pair then …" refinement that escapes the density bound: the density bound is insensitive to the poset structure and already handles every case. **The conjunction (density) ∧ (Theorem 1.2) = (density).** No finite-case analysis built on Theorem 1.2 improves on the existing approach.

**Where Theorem 1.2 *does* matter (for orientation, not for us):** it is the binding constraint for the *general* (unrestricted-moduli) Erdős–Selfridge program and for #586, where moduli can be enormous and Σ 1/m can sit at exactly the covering threshold — there, ruling out antichains is genuine content the density bound alone cannot supply. 𝓜 is simply not in that regime on any lattice we attack.

---

## 4. Formalizable sub-lemma (modest, optional)

There is one small, honest, Lean-formalizable structural fact. State it precisely:

**Lemma (𝓜 antichains undershoot the covering threshold on bounded lattices).** Let L be one of the project's lattice bounds (e.g. 27720) and let M_L = 𝓜 ∩ div(L). For every subset S ⊆ M_L that is an antichain under divisibility (no two distinct elements with one dividing the other), Σ_{m∈S} 1/m < 1. Concretely for L = 27720 the maximum is attained at S = {4, 6, 10, 22} with value 371/660.

- **Formalization handle.** This is a *finite check*: enumerate the 34 elements of M_27720, enumerate antichains (or just bound by the trivial observation that {4,6,10,22} is the reciprocal-maximal antichain and all other antichains are dominated), and verify 371/660 < 1 by `decide`/`norm_num` on rationals. Lives naturally as a companion to the existing `NumericalBound27720.lean` (`Mathlib.Data.Rat`, `Finset`-based). ~30–50 lines. **But:** it is *implied by* the already-verified `D(27720) = 953/990 < 1` (any antichain reciprocal sum ≤ full-set reciprocal sum < 1), so it adds no logical content to the manuscript — it would only be a presentational footnote. **Recommendation: skip unless the manuscript wants an explicit "even antichain-coverings fail" remark; the existing density lemma already covers it.**

**A structural fact worth recording (not for Lean, for the manuscript discussion section):** (𝓜, |) has both unboundedly long chains (length-9 example: 4|12|36|108|540|1620|4860|9720|19440) and a provably infinite antichain (its minimal elements, ≈12% of 𝓜). This rules out any "𝓜 is poset-trivial" shortcut and explains *why* Schinzel/Theorem 1.2 cannot decide #273 either way: 𝓜 is rich enough to host divisibility pairs (so Theorem 1.2 is satisfiable) yet the binding constraint is metric (reciprocal density), not order-theoretic.

---

## 5. Verdict and recommendation for the orchestrator

- **Theorem 1.2 = Schinzel's conjecture, proved BBMST22 (arXiv:1811.03547, Thm 1.2), hypothesis-light** (finite covering of ℤ, no distinctness/min-modulus needed). Cite it in the manuscript's SOTA/discussion as the resolution of #586 and as context for why an "antichain-covering" attack is impossible in general.
- **It does not advance #273 negatively or positively for 𝓜.** Its non-existence content (no antichain-covering) is, on every divisor lattice the project attacks, strictly weaker than the verified Σ 1/m < 1 density bound. There is no productive V2 vector here built on Theorem 1.2; **recommend not opening a sketch issue around it** (anti-overreach: it would not advance the seeded target).
- **One optional cosmetic Lean lemma** (§4) exists but is logically redundant given `D(27720) < 1`. Skip unless wanted for exposition.
- The genuinely productive levers remain the ones already identified: the **density/reciprocal-sum bound pushed to larger L** (the L = 83160 work in progress) and the **𝓜-specialized distortion bound** (V3). Theorem 1.2 is a footnote, not a tool, for this problem.

---

### Audit trail

- arXiv:1811.03547 (BBMST, Inventiones 228 (2022) 377–414): abstract + body read directly (PDF downloaded via WebFetch, parsed with `pypdf`). **Theorem 1.2 quoted verbatim from the PDF body**; confirmed hypothesis is "finite collection of arithmetic progressions that covers the integers" with no distinctness/min-modulus condition; confirmed attribution to Schinzel [10] = Schinzel 1967, Acta Arith. 13.
- erdosproblems.com/586 (fetched via curl + UA): "DISPROVED … Asked by Schinzel, motivated by a question of Erdős and Selfridge … The answer is no, as proved by Balister, Bollobás, Morris, Sahasrabudhe, and Tiba [BBMST22]."
- Schinzel 1967 reference confirmed via WebSearch: *Reducibility of polynomials and covering systems of congruences*, Acta Arith. 13 (1967) 91–101 — the polynomial-irreducibility origin of the conjecture; its xⁿ+f(x) consequence is conditional on the still-open Erdős–Selfridge odd-covering question (#7).
- Poset computations (sympy, this session): divisibility relations on 𝓜 up to 2·10⁵; minimal elements (infinite antichain, ≈12% density); longest chain length 9 (4|12|36|108|540|1620|4860|9720|19440); antichain reciprocal-sum optimum within M_27720 = 371/660 (at {4,6,10,22}) < 1.
- Cross-checked against prior surveys: findings/lit-covering-2026-05-28.md §2.3, findings/lit-V3-hough-2026-05-28.md §2.5 (both correctly flag Theorem 1.2 as vacuous-for-𝓜; V2 makes the subsumption quantitative).
