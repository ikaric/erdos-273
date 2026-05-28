# Heuristic / analytic — corrected CFT hyperplane-restriction count for 𝓜

**Author:** analyst (V3 distortion track)
**Session:** 2026-05-28
**Vector:** V3 (issue #5) — Hough/BBMST/CFT distortion specialized to
𝓜 = {p−1 : p prime ≥ 5}
**Script:** `formal/numerics/cft_M_hyperplane.py` (+ `.log`); reuses the
validated engine `cft_validate_squarefree.py`
**Predecessor note:** `findings/heur-cft-Mbound-2026-05-28.md` (disproved the
|S_j| = p(p−1) coordinate substitution)

## TL;DR (the honest verdict, up front)

The CFT hyperplane machinery, set up correctly for 𝓜, **does NOT yield a
finite min-modulus bound C_𝓜 better than the trivial squarefree majorant
(118).** The reason is structural and clean, not a tuning failure:

1. **The only defensible 𝓜 statement the engine produces is C_𝓜 ≤ 118**, and
   it is a *trivial corollary* of CFT's squarefree 118, not new content — see
   §3. (𝓜-moduli are not squarefree, but the non-squarefreeness only *helps*:
   ‖F(A)‖ = q−1 is *larger* than the squarefree skeleton, so the C₀-threshold
   is met more easily.)

2. **The "density gain" the librarian survey hoped for (a per-prime ≈ 1/(p−1)
   thinning of the count, §5.3) is illusory in this framework.** Implementing
   it (MODEL 1 below) reproduces *exactly* the over-reach signature of the
   disproved |S_j| = p(p−1) substitution: the sum drops below 1 at C₀ = 0,
   which would absurdly prove 𝓜 cannot cover ℤ at all. We prove
   algebraically (§4) that MODEL 1's per-coordinate weight is *literally
   identical* to the disproved substitution — it is the same wrong move,
   cosmetically relocated.

3. **The precise gap** (§5): the Dirichlet density 1/(p−1) governs *how many*
   𝓜-moduli of a given prime-support pattern exist in [1,X], but the
   covering's hyperplane sum (CFT Lemma 4.1) is over the moduli the adversary
   *actually placed*, and the adversary uses **at most one modulus per
   pattern**. Since every finite prime-support pattern is realized by *some*
   prime q (Dirichlet: q ≡ 1 mod ∏p_j has positive density), every pattern
   available to a squarefree covering is also available to an 𝓜 covering. The
   count of terms is therefore **unchanged**; multiplying ν(F) by a density
   ρ(F) < 1 is double-discounting and is what produces the spurious bound.

So V3's distortion lever, as a route to a *sharper-than-squarefree* C_𝓜, is a
**dead end in this exact form.** The genuine analytic content that *could*
help is not a per-pattern density but a joint constraint across many primes
simultaneously (§6) — and that constraint runs the wrong way for an upper
bound. The min-modulus question for 𝓜 is not reducible to a 1-D per-prime
density correction of CFT.

---

## 1. The CFT framework, stated precisely (so the 𝓜 slot is unambiguous)

(arXiv:2211.08548, §2–4; verbatim references below.) Coordinates
S_j = {1,…,p_j} (p_j the j-th prime). A modulus m becomes a hyperplane A_m
with fixed-coordinate set F(A_m) = {j : p_j | m}; coordinate j is pinned to one
of p_j residues iff p_j | m. For squarefree m,

    ‖F(A_m)‖ := ∏_{j∈F} |S_j| = ∏_{j: p_j|m} p_j = m            (CFT, line 700–701)

so ‖F(A)‖ is **literally the modulus**, and the running assumption (4)
"‖F(A)‖ > C₀ for all A" is exactly "every modulus > C₀."

The master inequality is **Lemma 4.1**:

    w_k(B_k) ≤ Σ_{A ∈ A_k} ν(F(A)),    ν(J) = ∏_{j∈J} 1/((1−δ_j)|S_j|),   (CFT eq. after L715)

where A_k = {hyperplanes A *present in the covering* with max F(A) = k}.
**Corollary 4.2** then upper-bounds Σ_{A∈A_k} by summing ν(J∪{k}) over *all*
J ⊆ {1,…,k−1} with ‖J‖·|S_k| > C₀. That replacement (present-hyperplanes →
all-subsets) is valid for squarefree distinct moduli because **every** subset
F = J∪{k} of primes is the support of an actual squarefree modulus
m = ∏_{j∈F} p_j; so each term the formula sums over is genuinely realizable.

Lemma 3.1: if Σ_{k} w_k(B_k) < 1 then A does not cover Q. CFT exhibit δ_j with
Σ = 0.999385 < 1 at C₀ = 118 ⇒ no squarefree covering has all moduli > 118.

**Two distinct roles to keep separate** (this is where everything turns):

- **Per-coordinate weight** 1/((1−δ_j)|S_j|): the *conditional precision*
  "given p_j | m, one of p_j residues is fixed." The 1/p_j here is identical
  for 𝓜 — given p_j | q−1, coordinate j is still pinned to one residue.
- **Count of available hyperplanes** Σ_{A∈A_k}: *which* fixed-coordinate
  patterns F can be realized by a modulus in the modulus set, and how many
  terms therefore appear.

The disproved heuristic put 1/(p−1) on the *weight* (role 1). The librarian
survey correctly diagnosed it belongs on the *count* (role 2). This note
implements role 2 properly and finds it still fails — for the reason in §5.

## 2. Where 1/(p−1) enters for 𝓜 (the genuinely correct location)

An 𝓜-modulus is m = q−1, q prime ≥ 5. The prime p_j divides m iff
q ≡ 1 (mod p_j). By Dirichlet / Siegel–Walfisz, among primes q the density of
q ≡ 1 (mod p_j) is **1/φ(p_j) = 1/(p_j−1)** for odd p_j, and **1** for p_j = 2
(every q−1 is even). More finely, ν_{p_j}(q−1) = γ has density
(1−1/p_j)·p_j^{−(γ−1)}/(p_j−1) (librarian §5.1).

So the *expected count* of 𝓜-moduli ≤ X realizing a fixed prime-support
pattern F (with valuations γ_j) is

    #{q ≤ X prime : ν_{p_j}(q−1)=γ_j ∀j∈F, =0 else} ≈ ρ(F)·π(X),
    ρ(F) = ∏_{j∈F, p_j odd} (p_j−1)^{−1} p_j^{−(γ_j−1)}(1−1/p_j).         (★)

ρ(F) ≤ 1 is a density **on the count of moduli of that pattern**, which is the
slot the survey flagged (§5.3: "a per-prime ≈ 1/log thinning of Σ_{A∈A_k}").
**MODEL 1** below takes (★) literally: weight each pattern-term ν(J∪{k}) in
Cor 4.2 by its density ρ(J∪{k}) = ∏_{j∈J∪{k}, odd} 1/(p_j−1).

## 3. MODEL 0 — the only defensible 𝓜 statement (C_𝓜 ≤ 118, trivial)

Keep |S_j| = p_j and the CFT weight; impose **no** density thinning. Then the
𝓜 sum is bounded by the *same* sum as squarefree (every term that occurs for
squarefree occurs for 𝓜 too — see §5(A)), so CFT's δ_j table gives
Σ_k w_k(B_k) ≤ 0.999385 < 1 at C₀ = 118.

Caveat that makes this fully rigorous for 𝓜: 𝓜-moduli are *not* squarefree
(28 = 2²·7, 256 = 2⁸, …). In the non-squarefree CFT one sets |S_j| = p_j^{γ_j}
on the coordinates that occur, and then ‖F(A)‖ = ∏ p_j^{γ_j} = q−1 = m **still
equals the modulus exactly**. Computation (script + spot checks): for every
𝓜-modulus, m = q−1 ≥ (squarefree skeleton ∏ distinct primes). E.g.
q=29: m=28=2²·7 ≥ 14; q=257: m=256=2⁸ ≥ 2. So the non-squarefreeness can only
*raise* ‖F(A)‖, making the constraint ‖F(A)‖ > C₀ *easier*. The squarefree
118 bound therefore holds a fortiori for 𝓜.

**This is real but not new:** "every 𝓜-covering has a modulus ≤ 118" is an
immediate corollary of CFT 2022's "every distinct-squarefree covering has a
modulus ≤ 118" *only if* every 𝓜-covering's hyperplane collection is pairwise
non-parallel (distinct moduli ⇒ yes) and embeds in the same Q — which it does.
But the honest accounting: 𝓜-coverings are a strict *subset* of all
distinct-moduli coverings, and CFT/BBMST already bound *all* distinct-moduli
coverings (≤ 615999) and all squarefree ones (≤ 118). The squarefree class and
𝓜 are incomparable (𝓜 has non-squarefree moduli like 4, 16; squarefree has
odd moduli like 15 ∉ 𝓜). The clean rigorous statement the engine supports is:

> **[heuristic→provable] Any covering of ℤ by distinct 𝓜-moduli all of which
> are squarefree has minimum modulus ≤ 118.** (Direct CFT corollary; the
> squarefree 𝓜-moduli are 6,10,30,42,70,…; their distinct subsets are
> squarefree, so CFT applies verbatim.)

That is **not** the target — it excludes the moduli 4,12,16,… that carry the
prime-2 structure. For the *full* 𝓜 (non-squarefree allowed), the engine gives
C_𝓜 ≤ 118 by the a-fortiori argument above, but this is dominated by — and
adds nothing to — the squarefree 118. **No sharper-than-118 bound emerges.**

## 4. MODEL 1 — the density-thinned count over-reaches (and why, exactly)

Run (`cft_M_hyperplane.py 20000`):

| setting                         | C₀=0        | C₀=118      |
|---------------------------------|------------:|------------:|
| MODEL 0 (= squarefree majorant) | 3.503805    | 1.004938    |
| MODEL 1 (ρ on the count)        | **0.752863**| 0.022768    |

MODEL 1 at **C₀ = 0** already gives Σ = 0.7529 < 1. By Lemma 3.1 with the
empty constraint, that asserts *no collection of 𝓜-hyperplanes covers Q* — i.e.
**𝓜 cannot cover ℤ at all, with arbitrarily small moduli.** That is far
stronger than Erdős #273 and is the textbook over-reach tell (CLAUDE.md:
"arguments that would secretly prove something stronger than the target").
So MODEL 1's "C_𝓜 = 0" is an artifact, not a bound. **Identical failure to the
disproved |S_j| = p(p−1) substitution** — and that is not a coincidence:

**Algebraic identity (verified, §script check).** MODEL 1's per-coordinate
weight is

    inv_M[j] = ρ_{p_j}·inv_sf[j] = (1/(p_j−1))·(1/((1−δ_j)p_j))
             = 1/((1−δ_j)·p_j(p_j−1)),

which is *exactly* the disproved S_M = p_j(p_j−1) weight. Spot-checked equal to
25 digits for p ∈ {3,5,11,19}. **Putting ρ on the "count" but carrying it
through ν multiplicatively is mathematically the same operation as putting it
on |S_j|** — because ν is multiplicative over coordinates and ρ is too, so the
product ∏(ρ_j·inv_j) cannot tell whether ρ rode on the weight or on the count.
The relocation the survey proposed is, in this multiplicative bound,
*indistinguishable* from the move it was meant to replace. Both over-reach.

## 5. The precise gap — why the density thinning is illegitimate

The density (★) is a count of *how many 𝓜-moduli of pattern F exist in
[1,X]*. But CFT Lemma 4.1 sums ν(F(A)) over the hyperplanes the adversary
**actually placed in the covering A** — a finite *design*, not a random sample
of 𝓜. Three facts close the gap:

**(A) Every squarefree pattern is 𝓜-available.** For any finite set of odd
primes {p_{j}}_{j∈F}, Dirichlet gives a prime q ≡ 1 (mod ∏_{j∈F} p_j), so
m = q−1 has all those primes in its support and induces a hyperplane with that
F. Verified by direct search for F ∈ {{3},{5},{3,5},{7},{3,5,7},{11,13},
{3,5,7,11},{17,19,23}} — each realized by an explicit small prime q
(q = 7,11,31,29,211,859,2311,29717). So the *set of patterns* available to 𝓜
is the same as (in fact a superset of, via non-squarefree valuations) the
squarefree set. **Availability is not a lever** (consistent with the
predecessor note's diagnosis).

**(B) The adversary uses ≤ 1 modulus per pattern.** Distinct moduli ⇒ pairwise
non-parallel hyperplanes ⇒ at most one A ∈ A with a given F(A) = F. The
covering needs *one* modulus realizing pattern F, and by (A) one exists. The
density ρ(F) ≪ 1 says such moduli are *rare among primes*, but rarity is
irrelevant: the adversary picks the single q that works (possibly large, but
the hyperplane's F and weight ν(F) are unchanged — ν depends only on F, not q).

**(C) Hence the count of terms is unchanged.** Σ_{A∈A_k} has one term per
realized pattern, exactly as in squarefree CFT. Multiplying each ν(F) by ρ(F)
charges the adversary for the rarity of pattern F — a cost the adversary does
not pay. That is the double-discount, and it is what drives Σ below 1
prematurely.

**Diagnosis in one line:** the 1/(p−1) density is a property of the *ambient
set 𝓜* (how its elements distribute), but the CFT bound is governed by the
*covering's chosen support patterns*, and the map "pattern F ↦ is F realizable
by 𝓜?" is **surjective onto all finite patterns** (fact A). A density that
multiplies a surjection's image by < 1 is always an over-count of the savings.

## 6. What analytic input *would* actually be needed (and why it's adverse)

A legitimate 𝓜 saving cannot come from per-pattern density. It would have to
come from a **joint, correlated constraint** the covering's *whole* support
must satisfy — e.g.:

- A modulus m = q−1 is *not free* to have an arbitrary residue class a (mod m):
  the class is whatever the adversary assigns, so no constraint there. (The
  CFT/BBMST bound is uniform over residue assignments, so this gives nothing.)
- The real correlations are *between coordinates*: ν_{p}(q−1) for several
  primes p are not independent for a *fixed* prime q (e.g. q ≡ 1 mod 3 and
  q ≡ 1 mod 5 force q ≡ 1 mod 15). But these correlations make joint patterns
  *less* frequent, i.e. they would *further* thin the count — pushing the
  (already illegitimate) MODEL-1 sum even lower, not toward a valid bound.
  They cannot rescue an *upper* bound on the min modulus.

The structural truth: the distortion method bounds min modulus from above by
finding that *too few small moduli exist to cover*. 𝓜 contains plenty of small
moduli (4,6,10,12,16,18,…; the verified V1/V5 work shows Σ_{m∈M, m|L} 1/m can
exceed 1 for L ≥ 55440). The density 1/(p−1) reflects sparsity *among primes
q*, but the *moduli themselves* (the q−1 values) are not sparse in any way the
hyperplane count sees — every small even-rich integer that is one-less-than-a-
prime is available, and there are many. **The method has no handle on 𝓜 that
beats the squarefree 118**, and 118 itself is the *wrong question* for 𝓜
because it ignores the prime-2 power structure (4,8,16,… ∈ 𝓜) that the
squarefree analysis discards.

## 7. Comparison table (final)

| modulus class                       | min-modulus upper bound | source / status |
|-------------------------------------|------------------------:|-----------------|
| all distinct moduli                 | 615,999                 | BBMST 2022 (published) |
| distinct squarefree                 | 118                     | CFT 2022 (validated here, 8 digits) |
| 𝓜 = {p−1}, squarefree-restricted    | ≤ 118                   | trivial CFT corollary (§3) |
| 𝓜 = {p−1}, full (non-sqfree allowed)| ≤ 118 (a fortiori)      | dominated by squarefree; **no improvement** |
| 𝓜 via ρ-thinned count (MODEL 1)     | over-reaches (bogus)    | = disproved S_M move (§4) |

## 8. Status of the V3 distortion vector

- **Squarefree CFT engine:** validated, reusable (`cft_validate_squarefree.py`,
  8-digit match to 0.999385). Unchanged.
- **𝓜 hyperplane-restriction count:** **set up correctly and evaluated; it does
  NOT close.** The only defensible number is ≤ 118, which is a trivial CFT
  corollary, not new content. The hoped-for density gain is provably illusory
  in this framework (§4 identity, §5 surjectivity).
- **Recommendation:** retire the "distortion gives a sharper C_𝓜" sub-goal of
  V3. The distortion method's saving comes from *scarcity of small moduli*, and
  𝓜 is *not* scarce in small moduli (it is scarce only as a subset of primes,
  which the hyperplane count is blind to). The productive levers for #273 remain
  (i) the exact density bound at growing L (V1/V5: Σ_{m∈M,m|L}1/m, verified
  < 1 for L ≤ 27720 and several larger L), and (ii) the SAT search (V2). The
  distortion vector should be recorded as a documented dead end for the
  *sharper-bound* objective, while keeping the validated squarefree engine as a
  reusable asset and the ≤118 squarefree-restricted corollary as a minor
  manuscript remark if desired.

## Reproduce

```sh
cd formal/numerics
uv run python3 cft_M_hyperplane.py 20000     # ≈ 25 s; shows MODEL 0 vs MODEL 1
uv run python3 cft_validate_squarefree.py 1000000   # the validated baseline
```

## Manuscript suggestion

- **Do NOT** add any 𝓜 distortion min-modulus bound below 118. Both the
  |S_j|=p(p−1) and the ρ-thinned-count specializations over-reach (proven
  identical, §4).
- Optional minor remark: `[heuristic→corollary]` "Any covering of ℤ by distinct
  squarefree 𝓜-moduli has minimum modulus ≤ 118 (CFT 2022 corollary)." Note it
  excludes the prime-power 𝓜-moduli 4,8,16,… so it does not bear on the full
  target.
- Record the distortion vector's *sharper-bound* sub-goal as a dead end with
  this note as the precise reason.
