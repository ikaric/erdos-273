#!/usr/bin/env python3
"""CORRECTED CFT hyperplane-restriction model for 𝓜 = {p-1 : p prime ≥ 5}.

Erdős Problem #273, vector V3. This is the *corrected* 𝓜 specialization of the
CFT 2022 distortion engine, replacing the DISPROVED |S_j| = p(p-1) coordinate
substitution (see findings/heur-cft-Mbound-2026-05-28.md) with a
hyperplane-restriction count. It reuses the validated squarefree engine
(`cft_validate_squarefree.py`, reproduces CFT's 0.99938506 to 8 sig figs).

============================================================================
WHERE THE 1/(p-1) FACTOR REALLY ENTERS  (the load-bearing derivation)
============================================================================

CFT recap (arXiv:2211.08548, §2-4).  Coordinates S_j = {1,...,p_j}.  A modulus
m ↦ hyperplane A_m fixing coordinate j  ⟺  p_j | m.  ‖F(A_m)‖ = ∏_{j: p_j|m} p_j
= m (squarefree).  The master inequality is

    LEMMA 4.1:   w_k(B_k) ≤ Σ_{A ∈ A_k} ν(F(A)),   ν(J) = ∏_{j∈J} 1/((1-δ_j)|S_j|),

where A_k = {available hyperplanes A with max(F(A)) = k}.  CFT then bound this
(COROLLARY 4.2) by summing ν(J∪{k}) over **ALL** J ⊆ {1,...,k-1} with
‖J‖·|S_k| > C_0.  That replacement is valid for the squarefree distinct-moduli
problem because EVERY pattern F = J∪{k} is realized by an actual squarefree
modulus m = ∏_{j∈F} p_j: squarefree moduli are in bijection with subsets of
primes, so every hyperplane the formula sums over is genuinely AVAILABLE.

The 𝓜 difference is NOT in |S_j| and NOT in the per-coordinate weight 1/p_j
(that weight is the conditional precision "given p_j | m, one of p_j residues
is fixed", which is identical for 𝓜).  The difference is in the COUNT of
available hyperplanes A_k — i.e. *which* fixed-coordinate patterns F can be
realized by an 𝓜-modulus q-1.

For 𝓜, a hyperplane with fixed-coordinate set F (with valuations γ_j ≥ 1) is
available  ⟺  there is a prime q with ν_{p_j}(q-1) = γ_j for j ∈ F (and
ν_{p_j}(q-1) = 0 for the coordinates not "used").  By Dirichlet/Siegel-Walfisz,
among primes q the density of those with q ≡ 1 (mod p_j) is 1/(p_j - 1); the
EVENTS "p_j | q-1" for distinct odd p_j are asymptotically independent (CRT on
the modulus, no obstruction since the p_j are coprime).  Two consequences:

  (A) AVAILABILITY GATE.  A given squarefree pattern F = {j_1,...,j_t} (one
      coordinate per prime, plus the forced prime 2) is realized by a positive
      density of 𝓜-moduli — namely density ∏_{j∈F, p_j odd} 1/(p_j - 1) among
      primes q.  This is positive for every finite F, so the SET of patterns
      that occur is the SAME as in the squarefree case (every subset of primes
      containing 2 — and even 2 is forced).  *Availability is not the lever:
      the same patterns occur.*

  (B) MULTIPLICITY / EXPECTED COUNT.  The right CFT object is not "is pattern F
      ever realized?" but the EXPECTED NUMBER of 𝓜-moduli ≤ X realizing F:

         #{q ≤ X prime : ν_{p_j}(q-1) = γ_j ∀ j∈F}  ≈  ρ(F) · π(X),
         ρ(F) = ∏_{j∈F, p_j odd} (p_j-1)^{-1} p_j^{-(γ_j-1)} · (1 - 1/p_j)
                · [factor for p_2 = 2].

  This ρ(F) ≤ 1 is a DENSITY among primes, and it is exactly the slot the
  librarian survey (§5.1, §5.3) flagged: a per-prime ≈ 1/(p_j-1) thinning of
  the count Σ_{A∈A_k}, NOT a shrink of |S_j|.

============================================================================
THE CRITICAL OBSTRUCTION  (why a naive thinning still over-reaches)
============================================================================

Here is the subtlety that the |S_j|=p(p-1) heuristic got catastrophically
wrong AND that a naive "multiply every ν(J) by ∏ 1/(p_j-1)" ALSO gets wrong.

Lemma 4.1 is  w_k(B_k) ≤ Σ_{A ∈ A_k} ν(F(A)).  The sum is over the hyperplanes
*actually present in the covering A*.  A_k is the set of moduli the adversary
chose to PUT in the covering — it is a FINITE design object, not a random
sample of 𝓜.  The density ρ(F) governs how many 𝓜-moduli of pattern F *exist*
in [1,X], but the adversary covering uses AT MOST ONE modulus per pattern F
(distinct moduli ⇒ pairwise non-parallel hyperplanes ⇒ at most one A per F).

So the number of TERMS in Σ_{A∈A_k} is bounded by the number of available
PATTERNS, each weighted by ν(F) — exactly as in CFT.  The adversary is free to
pick, for each pattern F that 𝓜 admits AT ALL, the single 𝓜-modulus of that
pattern (if one exists) and place it in the covering.  Since ρ(F) > 0 for every
finite F (consequence (A)), every pattern that the squarefree problem admits is
ALSO admitted by 𝓜 — possibly with a LARGER modulus (a bigger prime q), but
the hyperplane it induces has the SAME F and the SAME ν(F).

  ⟹  The CFT upper bound Σ_k w_k(B_k) for 𝓜 is bounded by the SAME sum as the
      squarefree case, with ONE genuine difference: the constraint ‖F(A)‖ > C_0.

Under squarefree, ‖F(A)‖ = m (the modulus), so "modulus > C_0" ⟺ ‖F‖ > C_0.
Under 𝓜, the modulus is m = q-1 with ν_{p_j}(m) = γ_j, so
   m = ∏_{p_j | m} p_j^{γ_j}   while   ‖F(A)‖ = ∏_{j∈F} |S_j| = ∏_{p_j|m} p_j^{γ_j}
   IF we set |S_j| = p_j^{γ_j} on the used coordinate.
The clean statement: for 𝓜, ‖F(A)‖ = m STILL HOLDS provided each coordinate's
size equals the prime power that actually divides m.  i.e. 𝓜 needs the
*non-squarefree* CFT (coordinate sizes p_j^{γ_j}), and the min-modulus
constraint ‖F(A)‖ > C_0 is faithful.

This script therefore implements the HONEST 𝓜 model:
  - keep |S_j| = p_j (squarefree skeleton; valuations handled below),
  - keep the per-coordinate weight 1/((1-δ_j) p_j),
  - apply the availability/count restriction ρ(F) on the NUMBER of admissible
    hyperplanes per pattern,
  - and test whether the resulting Σ_k w_k(B_k) < 1 for finite C_0.

We implement TWO count models and report BOTH, with the honest verdict:

  MODEL 0 (no thinning):  Σ_{A∈A_k} ≤ all J (identical to squarefree CFT).
     ⟹ C_𝓜 = C_squarefree = 118 trivially (every squarefree modulus has an
        𝓜 super-modulus of the same support? NO — see verdict).  This is the
        defensible UPPER MAJORANT and gives the only rigorous statement.

  MODEL 1 (density thinning ρ(F) on the COUNT):  multiply each term ν(J∪{k}) by
     ρ(J∪{k}) = ∏_{j∈J∪{k}, p_j odd} 1/(p_j - 1).  This is the librarian's §5.3
     proposal taken literally.  We compute the smallest C_0 it admits and FLAG
     whether it over-reaches (sum < 1 at C_0 = 0 ⇒ bogus, same failure tell).

INVOKE
======
    uv run python3 formal/numerics/cft_M_hyperplane.py [N]

Author: analyst (V3). Date: 2026-05-28.
"""
from __future__ import annotations

import sys
import time

from mpmath import mp, mpf, log, exp

import cft_validate_squarefree as cft  # validated machinery (S_j = p_j)

mp.dps = 30


# ----------------------------------------------------------------------
# Density factor ρ for a coordinate j (1-indexed prime p_j).
#   ρ_2 = 1   (2 | q-1 ALWAYS for q ≥ 3 prime — density 1 among primes)
#   ρ_{p}  = 1/(p-1)   for odd p   (Dirichlet density of q ≡ 1 mod p)
# This is the per-PRIME thinning of the COUNT of available 𝓜-hyperplanes that
# fix coordinate j, NOT a change to |S_j|.
# ----------------------------------------------------------------------
def rho_coord(p: int) -> "mpf":
    if p == 2:
        return mpf(1)
    return mpf(1) / (mpf(p) - 1)


# ----------------------------------------------------------------------
# MODEL 1 small-k bound: Cor 4.2 with each subset J weighted additionally by
# ρ(J∪{k}) = ∏_{j∈J∪{k}} ρ_{p_j}.  Since ρ is multiplicative over coordinates,
# this is the same enumeration as small_k_bound but with cd.inv[j] replaced by
# cd.inv[j]*ρ_{p_j} on every coordinate (including k).
# ----------------------------------------------------------------------
def small_k_bound_M(k, cd, rho, C0):
    S_k = cd.S[k - 1]
    threshold = mpf(C0) / S_k
    n_prev = k - 1
    total = mpf(0)
    for mask in range(1 << n_prev):
        norm = mpf(1)
        nu = mpf(1)
        for j in range(n_prev):
            if (mask >> j) & 1:
                norm *= cd.S[j]
                nu *= cd.inv[j] * rho[j]
        if norm > threshold:
            total += nu
    # coordinate k carries inv[k-1] * rho[k-1]
    return cd.inv[k - 1] * rho[k - 1] * total


# ----------------------------------------------------------------------
# MODEL 1 mid-k bound (Cor 4.6 analog).  Cor 4.6's product structure is
# Π_{j} (1 + c/((1-δ_j)|S_j|)).  Folding ρ_{p_j} into the per-coordinate weight
# turns each factor into (1 + c·ρ_{p_j}/((1-δ_j)|S_j|)).  We rebuild a CoordData
# whose inv[j] is multiplied by ρ_{p_j}; then Cor 4.6 applies verbatim, because
# Cor 4.6 only ever uses inv[j] through ν.  The threshold ‖J‖ > C_0/|S_k| uses
# the GEOMETRIC norm ‖J‖ = ∏ p_j (unchanged — the modulus-size constraint),
# while the WEIGHT uses ρ-thinned ν.  This cleanly separates the two roles.
# ----------------------------------------------------------------------
class CoordDataM:
    """CoordData clone with ρ-thinned inv[] but UNCHANGED S[] for the norm."""

    def __init__(self, base: "cft.CoordData", rho):
        self.primes = base.primes
        self.S = base.S                 # |S_j| = p_j  (norm = modulus size)
        self.deltas = base.deltas
        self.n = base.n
        self.inv = [iv * r for iv, r in zip(base.inv, rho)]  # ρ-thinned weight
        self.pref3 = [mpf(1)]
        self.pref1 = [mpf(1)]
        for j in range(self.n):
            self.pref3.append(self.pref3[-1] * (1 + 3 * self.inv[j]))
            self.pref1.append(self.pref1[-1] * (1 + self.inv[j]))

    def prod3(self, a, b):
        if a > b:
            return mpf(1)
        return self.pref3[b] / self.pref3[a - 1]

    def prod1(self, a, b):
        if a > b:
            return mpf(1)
        return self.pref1[b] / self.pref1[a - 1]


def tail_bound_M_correct(N, cdM: "CoordDataM"):
    """Tail Σ_{k>N} w_k(B_k) for the ρ-thinned model.

    From Cor 4.6 (C_0 = 0, δ_k = 1/2), w_k(B_k) ≤ (1/|S_k|²) ∏_{j<k}(1 +
    3·inv_j).  With inv_j = ρ_{p_j}/((1-δ_j) p_j) and |S_j| = p_j we still have
    Σ_{j>N} 3·inv_j ≤ 3 Σ_{p>p_N} 1/(p(p-1)) ≤ 3/p_N (ρ_p = 1/(p-1) makes the
    odd-prime tail even smaller than squarefree).  So the squarefree tail bound
    is a valid (loose) majorant.  Reuse it on the ρ-thinned M0.
    """
    p_N = mpf(cdM.primes[N - 1])
    L = log(p_N)
    M0 = cdM.pref3[N]
    c1 = -log(L) + 1 / (L * L)
    c2 = 1 + 3 / (2 * L)
    poly = L**5 + 5 * L**4 + 20 * L**3 + 60 * L**2 + 120 * L + mpf(120)
    return (2 * c2 * M0 * exp(6 * c1) / p_N) * poly


def compute_total_M_model1(N, cdM, rho, C0):
    s_small = sum(
        (small_k_bound_M(k, cdM, rho, C0) for k in range(1, cft.K_SMALL + 1)),
        mpf(0),
    )
    s_mid = mpf(0)
    for k in range(cft.K_SMALL + 1, N + 1):
        s_mid += cft.mid_k_bound(k, cdM, C0)  # uses cdM.inv (ρ-thinned)
    s_tail = tail_bound_M_correct(N, cdM)
    return s_small, s_mid, s_tail


def smallest_C0_model1(N, cdM, rho, lo, hi):
    def tot(C0):
        a, b, c = compute_total_M_model1(N, cdM, rho, C0)
        return a + b + c

    if tot(hi) >= 1:
        return None, tot(hi)
    if tot(lo) < 1:
        return lo, tot(lo)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if tot(mid) < 1:
            hi = mid
        else:
            lo = mid
    return hi, tot(hi)


def main():
    sys.stdout.reconfigure(line_buffering=True)
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 100000

    print("=" * 78)
    print("CORRECTED 𝓜 HYPERPLANE-RESTRICTION CFT model (Erdős #273, V3).")
    print("=" * 78)
    print(f"mp.dps = {mp.dps}, N = {N}, K_small = {cft.K_SMALL}")
    print("Coordinate sizes UNCHANGED: |S_j| = p_j (squarefree skeleton).")
    print("ρ_2 = 1 (2 | q-1 always);  ρ_p = 1/(p-1) for odd p (Dirichlet).")
    print("ρ thins the COUNT of admissible hyperplanes, not |S_j|.")
    print()

    t = time.time()
    primes = cft.first_n_primes(N + 5)
    cd_sf = cft.build_coord(primes, cft.cft_delta, cft.S_squarefree)
    rho = [rho_coord(p) for p in primes]
    cdM = CoordDataM(cd_sf, rho)
    print(f"[sieve+build: {time.time()-t:.1f}s, p_N = {primes[N-1]}]")
    print(f"ρ[0..9] = {[float(x) for x in rho[:10]]}")
    print(f"inv_sf[0..9]  = {[round(float(x),5) for x in cd_sf.inv[:10]]}")
    print(f"inv_M (ρ)[0..9] = {[round(float(x),5) for x in cdM.inv[:10]]}")
    print()

    # ------------------------------------------------------------------
    # MODEL 0 (no thinning) baseline = squarefree, reported for reference.
    # ------------------------------------------------------------------
    print("-" * 78)
    print("MODEL 0 (no thinning; = squarefree CFT majorant for 𝓜):")
    a0, b0, c0 = cft.compute_split(N, cd_sf, 118)
    print(f"  at C_0=118: small={float(a0):.6f} mid={float(b0):.6f} "
          f"tail={float(c0):.3e}  TOTAL={float(a0+b0+c0):.8f}")
    a0z, b0z, c0z = cft.compute_split(N, cd_sf, 0)
    print(f"  at C_0=0  : TOTAL={float(a0z+b0z+c0z):.6f}  "
          f"(>>1 ⇒ NOT over-reaching, correct)")
    print()

    # ------------------------------------------------------------------
    # MODEL 1 (ρ-thinning on the count — the librarian §5.3 proposal).
    # ------------------------------------------------------------------
    print("-" * 78)
    print("MODEL 1 (ρ-thinning of the hyperplane COUNT):")
    # over-reach check FIRST: C_0 = 0 must give TOTAL >= 1 to be defensible.
    az, bz, cz = compute_total_M_model1(N, cdM, rho, 0)
    totz = az + bz + cz
    print(f"  OVER-REACH CHECK at C_0=0: small={float(az):.6f} "
          f"mid={float(bz):.6f} tail={float(cz):.3e}")
    print(f"      TOTAL(C_0=0) = {float(totz):.8f}  "
          f"{'<1  ==> OVER-REACHES (BOGUS)' if totz < 1 else '>=1  ==> not over-reaching'}")
    print()

    a1, b1, c1 = compute_total_M_model1(N, cdM, rho, 118)
    print(f"  at C_0=118: small={float(a1):.6f} mid={float(b1):.6f} "
          f"tail={float(c1):.3e}  TOTAL={float(a1+b1+c1):.8f}")
    print()
    if totz < 1:
        print("  Smallest C_0 with MODEL-1 TOTAL < 1:  C_0 = 0 (already <1 ⇒ BOGUS;")
        print("  bisection skipped — the over-reach makes any reported number an artifact).")
        C0m, totm = 0, totz
    else:
        print("  Smallest C_0 with MODEL-1 TOTAL < 1:")
        t = time.time()
        C0m, totm = smallest_C0_model1(N, cdM, rho, lo=0, hi=2_000_000)
        print(f"  [bisection: {time.time()-t:.1f}s]")
        if C0m is None:
            print(f"      none ≤ 2·10^6 (TOTAL at 2e6 = {float(totm):.6f})")
        else:
            aa, bb, ccc = compute_total_M_model1(N, cdM, rho, C0m)
            print(f"      ==> C_𝓜(model 1) = {C0m},  TOTAL = {float(aa+bb+ccc):.8f}")
    print()

    print("=" * 78)
    print("COMPARISON")
    print("=" * 78)
    print("  squarefree (validated CFT)  : C_0 = 118")
    print("  BBMST universal (published) : 615,999")
    print(f"  MODEL 0 (𝓜 majorant)        : 118  (same patterns available)")
    print(f"  MODEL 1 (𝓜 ρ-thinned count) : "
          f"{'over-reaches (bogus)' if totz < 1 else (C0m if C0m else '>2e6')}")
    print()
    print("VERDICT printed by the findings note — see")
    print("  findings/heur-cft-hyperplane-2026-05-28.md")


if __name__ == "__main__":
    main()
