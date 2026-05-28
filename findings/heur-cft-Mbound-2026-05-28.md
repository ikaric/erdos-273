# Heuristic / numerical — CFT δ_j optimization for 𝓜, validation status

**Author:** computationalist
**Session:** 2026-05-28 (session 3, V3 distortion track)
**Vector:** V3 (issue #5) — Hough/BBMST/CFT distortion specialized to 𝓜 = {p−1 : p prime ≥ 5}
**Scripts:**
- `formal/numerics/cft_validate_squarefree.py` (+ `.log`) — squarefree acid test
- `formal/numerics/cft_M_heuristic.py` (+ `.log`) — 𝓜 density-corrected heuristic
- `formal/numerics/cft_delta_optimization.py` — original combined script (c1 bug fixed)
- CFT 2022 paper text cached at `/tmp/cft.txt` (arXiv:2211.08548, full body)

## TL;DR

1. **The squarefree baseline VALIDATES — exactly.** Pushed N from 200 → 10⁶
   at C₀ = 118. TOTAL converges to **0.99938506**, matching CFT 2022's
   published 0.999385061449 (eq. 12) **to 8 significant digits**, with the
   small/mid/tail split each matching CFT eqs. (9)/(10)/(11) independently.
   The earlier TOTAL = 1.263 at N = 200 was entirely the loose tail at small
   N, exactly as suspected. **The CFT machinery is correctly implemented.**

2. **The 𝓜-mode does NOT validate — it is a mislocated-density heuristic
   that over-reaches.** With the substitution |S_j|^𝓜 = p_j(p_j−1), the
   density-corrected sum drops below 1 *even at C₀ = 0* (TOTAL ≈ 0.918).
   That would "prove" 𝓜 cannot cover ℤ **at all, with no minimum-modulus
   restriction** — far stronger than the open target, and the classic tell
   of an over-counting/over-discounting error. The reported "C_𝓜 = 1" is an
   artifact, not a bound. **It must not go in the manuscript as a result.**

So: squarefree acid test PASSED; 𝓜 distortion lever, as currently encoded,
is NOT validated. The honest status of V3 is below.

## 1. Squarefree validation (the acid test)

Fixed C₀ = 118, K_small = 7, CFT's exact δ_j table, mp.dps = 30. Swept the
cut N. Mid-loop made genuinely O(N) (binary-search for `r` instead of the
original O(N²) linear scan; at C₀ = 118 the per-k subset enumeration has
n_small = 0 for all k ≥ 18, so it is O(1) per step). Full N = 10⁶ run: sieve
+ prefix-product build 7.6 s, mid-loop 11.6 s.

| N        | p_N        | small      | mid          | tail        | TOTAL        | <1? |
|----------|-----------:|-----------:|-------------:|------------:|-------------:|-----|
| 200      | 1223       | 0.142125   | 0.73649426   | 4.080e-01   | 1.28658667   | no  |
| 1000     | 7919       | 0.142125   | 0.81989613   | 1.062e-01   | 1.06827010   | no  |
| 5000     | 48611      | 0.142125   | 0.84583008   | 2.921e-02   | 1.01716016   | no  |
| 20000    | 224737     | 0.142125   | 0.85314525   | 9.668e-03   | 1.00493807   | no  |
| 100000   | 1299709    | 0.142125   | 0.85591816   | 2.669e-03   | 1.00071213   | no  |
| **10⁶**  | **15485863** | **0.142125** | **0.85685756** | **4.030e-04** | **0.99938506** | **YES** |

CFT published (N = 10⁶):  small 0.142124542 (= 194/1365), mid 0.856857559,
tail 0.000402961, TOTAL **0.999385061** < 1.

Every column matches:
- small = 0.142125 at all N (only k = 1..7; matches 194/1365 exactly).
- mid → 0.85685756 vs CFT 0.856857558639 (8 digits).
- tail → 4.02961e-04 vs CFT 0.000402960685 (6 digits).
- p_N = 15485863 = the true 10⁶-th prime.

Crossover (at N = 10⁵, slightly looser tail): C₀ = 118 → 1.00071 (just over),
C₀ = 119 → 0.99231. At the full N = 10⁶, C₀ = 118 itself gives 0.99939 < 1,
i.e. **CFT's 118 is reproduced essentially on the nose.**

### Bug found & fixed
CFT Lemma 4.7 has c₁ = −log log p_N + **1/log² p_N**. The original
`cft_delta_optimization.py` had **1/(2·log² p_N)** — a tightening (wrong-
direction) error, harmless for the conclusion but not faithful. Fixed in
both scripts; the validation reproduces CFT after the fix.

## 2. Why the 𝓜-mode does NOT validate

The 𝓜 substitution comes from the librarian survey's "ρ_p density factor":
1/|S_j| → ρ_{p_j}/|S_j| with ρ_p = 1/(p−1), i.e. |S_j|^𝓜 = p_j(p_j−1).

Comparison sweep at N = 20000 (both settings, same δ_j table):

| setting        | C₀=0    | C₀=2    | C₀=118  |
|----------------|--------:|--------:|--------:|
| squarefree     | 3.5038  | 3.0038  | 1.0049  |
| 𝓜 = p(p−1)     | 0.9177  | 0.4177  | 0.0479  |

The squarefree column behaves correctly: at C₀ = 0 (no modulus restriction)
the sum is 3.5 ≫ 1, because squarefree coverings with small moduli genuinely
exist (Selfridge's example has minimum modulus 2). The sum only drops below
1 once C₀ rises to ~118. **The 𝓜 column at C₀ = 0 is already 0.918 < 1.**

By CFT Lemma 3.1, Σ_k w_k(B_k) < 1 with the C₀ = 0 constraint (i.e. NO
constraint ‖F(A)‖ > C₀) implies the hyperplane collection does **not** cover
Q. So the 𝓜-mode would assert: *no collection of 𝓜-hyperplanes covers ℤ,
period* — 𝓜 cannot cover ℤ even with arbitrarily small moduli. That is a
much stronger claim than Erdős #273 (which asks whether a *finite* 𝓜-cover
exists / what its min modulus can be), and exactly the "argument that
secretly proves something stronger than the target" pattern CLAUDE.md flags.

### Where the substitution is wrong
In CFT, for **squarefree** moduli ‖F(A)‖ = ∏_{j∈F} |S_j| = ∏ p_j = m **is the
modulus**; the weight per coordinate is 1/((1−δ_j)·p_j) because, given that a
modulus is divisible by p_j, it fixes exactly one of p_j residues at
coordinate j. The factor 1/p_j is the conditional "given p_j | m" precision.

The density factor 1/(p_j−1) is a **different** quantity: it is how *often*
the prime p_j divides an 𝓜-element q−1 (Dirichlet: q ≡ 1 mod p_j has density
1/(p_j−1) among primes). Folding it into |S_j| as p_j(p_j−1):

- **mis-locates it** — it belongs on the *number of available hyperplanes*
  (the size of the index set A_k in the sum Σ_{A∈A_k} ν(F(A))), NOT on the
  per-coordinate weight ν, and
- **double-counts the sparsity** — it shrinks every term by (p_j−1), so even
  the small-k terms (k ≤ 7, primes 2,3,5,7,11,13,17 — note 2,4,6,10,12,16 are
  all in 𝓜!) collapse from 2.41 to 0.918, killing the sum before C₀ matters.

The correct CFT-style 𝓜 instantiation (librarian §5.2–5.3) keeps
|S_j| = p_j (or p_j^{γ_j} for the valuations that actually occur in 𝓜) and
instead **restricts the hyperplane set** A to those A with ‖F(A)‖ = q−1 for
some prime q. That restriction removes terms from Σ_{A∈A_k}, lowering the
sum, but each surviving term keeps weight 1/((1−δ_j)p_j). Implementing it
requires the 𝓜-density count of admissible (F-pattern → is q−1 prime?)
hyperplanes per stage — genuine new analytic input (Siegel–Walfisz-type),
not a one-line |S_j| swap.

## 3. Honest status of the V3 distortion lever for 𝓜

- **Squarefree CFT pipeline: fully reproduced and trustworthy** (8-digit
  match to the published 118-bound computation). This is a reusable,
  validated numerical engine — `cft_validate_squarefree.py`.
- **𝓜 specialization via the |S_j| = p(p−1) substitution: a dead heuristic.**
  It over-discounts and would prove 𝓜 non-covering unconditionally, so it is
  unusable as stated. No defensible C_𝓜 comes out of it; the "1" it reports
  is an artifact.
- **What V3 actually needs next:** the *hyperplane-restriction* formulation,
  not a coordinate-size swap. Concretely (issue for next session):
  1. Per stage k, count admissible 𝓜-hyperplanes: among F ⊆ {1..k−1}∪{k}
     with kept weights 1/((1−δ_j)p_j), include only those whose product of
     primes-with-multiplicity equals q−1 for a prime q. This needs the
     density of primes q with prescribed ν_{p_j}(q−1) (librarian §5.1:
     1/((p_j−1)p_j^{γ−1}) by Siegel–Walfisz).
  2. Re-run the CFT sum over this restricted index set with the validated
     small/mid/tail engine. The savings is a per-prime ~1/log factor (the
     "is q−1 prime" gate), NOT a per-coordinate 1/(p−1) shrink.
  This is analyst-flavoured work (the moment bound §5.3), not a notebook
  tweak. The validated engine is ready to receive it once the admissibility
  count is specified.

**Bottom line:** the distortion method's *engine* is validated; the *𝓜 input
to it has not been correctly built yet*. The current 𝓜 number is not a
bound and must stay out of the manuscript. The next concrete V3 step is the
hyperplane-restriction count, which is a real (1–3 session) analyst task, not
a parameter change.

## Reproduce

```sh
# squarefree acid test (≈ 20 s for the full N=10^6 line):
uv run python3 formal/numerics/cft_validate_squarefree.py 1000000
# 𝓜 heuristic (≈ 4 s; shows the C0=0 over-reach):
cd formal/numerics && uv run python3 cft_M_heuristic.py 100000
```

## Manuscript suggestion

- `[numerical: N ≤ 10^6]` The CFT 2022 squarefree minimum-modulus computation
  (Σ_k w_k(B_k) ≤ 0.999385 at C₀ = 118) is independently reproduced to 8
  significant digits by `formal/numerics/cft_validate_squarefree.py`.
- **Do NOT** add any 𝓜 distortion bound; the |S_j| = p(p−1) heuristic is
  invalid (proves too much). V3's 𝓜 lever is open pending the
  hyperplane-restriction count.
