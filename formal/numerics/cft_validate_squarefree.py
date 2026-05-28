#!/usr/bin/env python3
"""Validation harness for the CFT 2022 squarefree minimum-modulus bound.

PURPOSE
=======
The acid test for Erdős Problem #273, vector V3 (CFT/Hough distortion).
Before trusting any 𝓜 = {p-1 : p prime ≥ 5} number produced by
`cft_delta_optimization.py`, we must reproduce CFT 2022's published
squarefree result:

    Theorem 1.1 (CFT 2022, arXiv:2211.08548): every covering system with
    distinct squarefree moduli has minimum modulus ≤ 118.

CFT prove this by exhibiting δ_j (their explicit table) such that, with
C_0 = 118 and the cut N = 10^6,

    Σ_{k=1}^{7}        w_k(B_k) ≤ 194/1365      = 0.142124542...   (eq. 9)
    Σ_{k=8}^{10^6}     w_k(B_k) ≤ 0.856857558639...                (eq. 10)
    Σ_{k>10^6}         w_k(B_k) ≤ 0.000402960685...                (eq. 11)
    -----------------------------------------------------------------------
    TOTAL              Σ_k       ≤ 0.999385061449... < 1           (eq. 12)

This script recomputes those three sums from the formulas (Cor. 4.2,
Cor. 4.6, Lemma 4.7) for a RANGE of cut values N, with C_0 = 118 fixed,
to confirm the implementation converges to ~0.9994 as N → 10^6.

If it does, the implementation is validated and the 𝓜 numbers can be
trusted. If it does NOT, the discrepancy localizes the bug/limitation.

INDEXING CONVENTION
===================
1-indexed primes: p_1 = 2, p_2 = 3, ...  |S_j| = p_j (squarefree).
δ_j table is 1-indexed exactly as printed in CFT §4.1.

PERFORMANCE
===========
- Prime sieve: O(p_N log log p_N) via a segmented/standard sieve.
- Small-k sum: K_small = 7 fixed → 2^6 subset enumerations, O(1).
- Mid-k sum (k = 8..N): O(1) per step using prefix products + a
  BINARY SEARCH for r (the original script used a linear scan → O(N^2)).
  The per-k subset enumeration (U, V) has n_small = (# primes with
  |S_j| ≤ C_0/|S_k|); since |S_k| grows, n_small ≤ 4 at C_0 = 118 for
  all k ≥ 8, so the inner 2^{2 n_small} work is bounded by a constant.
- Tail: closed form, O(1).

So total cost is O(p_N) for the sieve + O(N) for the mid-loop.
N = 10^6 needs primes up to p_{10^6} = 15485863 → ~1e7 sieve, a few
seconds, and 10^6 mid-steps, ~tens of seconds in mpmath.

INVOKE
======
    uv run python3 formal/numerics/cft_validate_squarefree.py [Nmax]

Default Nmax sweeps {200, 1000, 5000, 20000, 100000, 1000000}.

Author: computationalist (V3). Date: 2026-05-28.
"""
from __future__ import annotations

import sys
import time

from mpmath import mp, mpf, log, exp

mp.dps = 30

C0_DEFAULT = 118
K_SMALL = 7


# ----------------------------------------------------------------------
# Prime sieve (fast, integer).
# ----------------------------------------------------------------------
def primes_up_to(limit: int) -> list[int]:
    """All primes ≤ limit via a simple bytearray sieve."""
    if limit < 2:
        return []
    sieve = bytearray(b"\x01") * (limit + 1)
    sieve[0] = sieve[1] = 0
    i = 2
    while i * i <= limit:
        if sieve[i]:
            sieve[i * i :: i] = b"\x00" * len(sieve[i * i :: i])
        i += 1
    return [i for i in range(2, limit + 1) if sieve[i]]


def first_n_primes(n: int) -> list[int]:
    """Return [p_1, ..., p_n]. Uses a prime-count upper bound for the sieve."""
    if n < 6:
        return [2, 3, 5, 7, 11, 13][:n]
    import math

    # Upper bound for the n-th prime (Rosser): p_n < n(ln n + ln ln n) for n ≥ 6.
    ln = math.log(n)
    upper = int(n * (ln + math.log(ln))) + 10
    ps = primes_up_to(upper)
    while len(ps) < n:
        upper = int(upper * 1.2)
        ps = primes_up_to(upper)
    return ps[:n]


# ----------------------------------------------------------------------
# CFT δ_j table (verbatim, 1-indexed).
# ----------------------------------------------------------------------
_DELTA_TABLE = {
    8: 0.171, 9: 0.190, 10: 0.199, 11: 0.210, 12: 0.210,
    13: 0.224, 14: 0.233, 15: 0.237, 16: 0.237, 17: 0.237,
    18: 0.252, 19: 0.252, 20: 0.255, 21: 0.260, 22: 0.261,
    23: 0.263, 24: 0.264, 25: 0.262, 26: 0.265, 27: 0.269,
}


def cft_delta(j: int) -> float:
    if j <= 7:
        return 0.0
    if j in _DELTA_TABLE:
        return _DELTA_TABLE[j]
    if 28 <= j <= 35: return 0.279
    if 36 <= j <= 45: return 0.289
    if 46 <= j <= 60: return 0.297
    if 61 <= j <= 99: return 0.307
    if 100 <= j <= 1000: return 0.331
    if 1001 <= j <= 10000: return 0.372
    if 10001 <= j <= 1000000: return 0.418
    return 0.5


# ----------------------------------------------------------------------
# Precomputed coordinate data.
# ----------------------------------------------------------------------
class CoordData:
    """1-indexed access via [j]; arrays stored 0-indexed internally."""

    def __init__(self, primes, S, deltas):
        self.primes = primes
        self.S = S            # |S_j|, 0-indexed list, length n
        self.deltas = deltas  # δ_j, 0-indexed
        self.n = len(primes)
        # inv_1mdS[j] = 1/((1-δ_j)|S_j|)
        self.inv = [1 / ((1 - d) * s) for d, s in zip(deltas, S)]
        # prefix products (1-indexed: prefix[k] = prod_{j=1..k}).
        self.pref3 = [mpf(1)]
        self.pref1 = [mpf(1)]
        for j in range(self.n):
            self.pref3.append(self.pref3[-1] * (1 + 3 * self.inv[j]))
            self.pref1.append(self.pref1[-1] * (1 + self.inv[j]))

    def prod3(self, a, b):
        """prod_{j=a..b} (1+3 inv_j), 1-indexed inclusive."""
        if a > b:
            return mpf(1)
        return self.pref3[b] / self.pref3[a - 1]

    def prod1(self, a, b):
        if a > b:
            return mpf(1)
        return self.pref1[b] / self.pref1[a - 1]


def build_coord(primes, delta_fn, Sfn):
    S = [Sfn(p) for p in primes]
    deltas = [mpf(delta_fn(j)) for j in range(1, len(primes) + 1)]
    return CoordData(primes, S, deltas)


def S_squarefree(p):
    return mpf(p)


def S_M(p):
    """𝓜 = {p-1} effective coordinate size (HEURISTIC, see findings note).

    The librarian survey's "ρ_p density factor" reads:
        1/|S_j| (prob. of hitting residue 0 mod p_j via a squarefree modulus)
          ->  ρ_{p_j}/|S_j|  (prob. via an 𝓜-modulus)
    with ρ_2 = 1, ρ_{p} = 1/(p-1) for p ≥ 3 (Dirichlet). Equivalently
        |S_2|^M = 2,   |S_j|^M = p_j (p_j - 1) for p_j ≥ 3.

    CAVEAT (load-bearing): in CFT, ‖F(A)‖ = ∏_{j∈F} |S_j| = m IS the modulus,
    so the constraint ‖F(A)‖ > C_0 literally says "modulus > C_0". Under the
    S_M substitution, ‖F(A)‖^M = ∏ p_j(p_j-1) is NOT the modulus m = q-1, so
    the threshold C_0/|S_k| no longer corresponds to "modulus > C_0". This
    mode therefore produces a HEURISTIC density-corrected sum, not a validated
    CFT specialization. See findings/heur-cft-Mbound-2026-05-28.md.
    """
    if p == 2:
        return mpf(2)
    return mpf(p) * (mpf(p) - 1)


# ----------------------------------------------------------------------
# Small-k bound (Corollary 4.2).
#   w_k(B_k) ≤ (1/((1-δ_k)|S_k|)) Σ_{J⊆{1..k-1}, ||J||>C_0/|S_k|} ν(J)
# ----------------------------------------------------------------------
def small_k_bound(k, cd: CoordData, C0):
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
                nu *= cd.inv[j]
        if norm > threshold:
            total += nu
    return cd.inv[k - 1] * total


# ----------------------------------------------------------------------
# Find r (Corollary 4.6): minimal r s.t. |S_t| > C_0/|S_k| for ALL t ≥ r.
# Since |S_t| = p_t is strictly increasing, this is the first index where
# |S_t| > threshold; r-1 = (# indices with |S_t| ≤ threshold).
# Binary search → O(log k) per call instead of O(k).
# ----------------------------------------------------------------------
def find_r(threshold, cd: CoordData, k):
    """Return r in [1, k]. n_small = r-1 = count of t in 1..k-1 with |S_t|<=thr."""
    import bisect

    # cd.S is strictly increasing. Count how many of S[0..k-2] are <= threshold.
    # bisect on the prefix S[0:k-1].
    lo, hi = 0, k - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if cd.S[mid] <= threshold:
            lo = mid + 1
        else:
            hi = mid
    n_small = lo  # number of indices (0-based) with S <= threshold among 0..k-2
    return n_small + 1


def mid_k_bound(k, cd: CoordData, C0):
    """Corollary 4.6 bound (falls back to Cor 4.2 when δ_k = 0)."""
    S_k = cd.S[k - 1]
    d_k = cd.deltas[k - 1]
    if d_k == 0:
        return small_k_bound(k, cd, C0)

    threshold = mpf(C0) / S_k
    r = find_r(threshold, cd, k)
    n_small = r - 1

    Pi3 = cd.prod3(1, k - 1)
    Pi1_from_r = cd.prod1(r, k - 1)

    U = mpf(0)
    V = mpf(0)
    if n_small > 0:
        norms = []
        weights = []
        for mask in range(1 << n_small):
            norm = mpf(1)
            w = mpf(1)
            for j in range(n_small):
                if (mask >> j) & 1:
                    norm *= cd.S[j]
                    w *= cd.inv[j]
            norms.append(norm)
            weights.append(w)
        small_masks = [i for i, nm in enumerate(norms) if nm <= threshold]
        for m1 in small_masks:
            for m2 in range(1 << n_small):
                w_union = weights[m1 | m2]
                if norms[m2] <= threshold:
                    U += w_union
                else:
                    V += w_union
    else:
        if mpf(1) <= threshold:
            U = mpf(1)

    prefactor = 1 / (4 * d_k * (1 - d_k) * S_k * S_k)
    body = Pi3 - 2 * (U + V) * Pi1_from_r + U
    return prefactor * body


# ----------------------------------------------------------------------
# Tail bound (Lemma 4.7), squarefree, EXACT to the paper.
#   c1 = -log log p_N + 1/log^2 p_N     (paper line "c1 = -loglog pN + 1/log^2 pN")
#   c2 = 1 + 3/(2 log p_N)
#   M0 = prod_{j=1..N} (1 + 3/((1-δ_j)|S_j|))
#   Σ_{k>N} w_k ≤ (2 c2 M0 e^{6c1}/p_N)(log^5+5log^4+20log^3+60log^2+120log+120)
# ----------------------------------------------------------------------
def tail_bound_squarefree(N, cd: CoordData):
    p_N = mpf(cd.primes[N - 1])
    L = log(p_N)
    M0 = cd.pref3[N]
    c1 = -log(L) + 1 / (L * L)            # paper uses 1/log^2 p_N
    c2 = 1 + 3 / (2 * L)
    poly = L**5 + 5 * L**4 + 20 * L**3 + 60 * L**2 + 120 * L + mpf(120)
    return (2 * c2 * M0 * exp(6 * c1) / p_N) * poly


def tail_bound_M(N, cd: CoordData):
    """𝓜-version of Lemma 4.7's tail (HEURISTIC, mirrors S_M caveat).

    Re-derive the tail with |S_j|^M = p_j(p_j-1). The proof of Lemma 4.7
    starts from (δ_k = 1/2 for k > N):
        w_k(B_k) ≤ (1/|S_k|^2) prod_{j=1..k-1}(1 + 3/((1-δ_j)|S_j|))
                 = (1/|S_k|^2) M0 prod_{j=N+1..k-1}(1 + 6/|S_j|^M).
    Since |S_j|^M = p_j(p_j-1), we have
        sum_{j>N} 1/|S_j|^M = sum_{p>p_N} 1/(p(p-1)) ≤ 1/p_N  (telescoping on
        1/(p(p-1)) < 1/((p-1)) - 1/p is FALSE; the clean telescoping is
        1/(p(p-1)) = 1/(p-1) - 1/p, so sum over ALL integers > p_N telescopes
        to 1/p_N; restricting to primes only shrinks it, so ≤ 1/p_N holds).
    Hence prod(1+6/|S_j|^M) ≤ exp(6/p_N), and
        sum_{k>N} w_k ≤ M0 exp(6/p_N) sum_{p>p_N} 1/(p(p-1))^2
                     ≤ M0 exp(6/p_N) sum_{n>p_N} 1/(n^2(n-1))
                     ≤ M0 exp(6/p_N) / (p_N^2(p_N - 1)) * (small const).
    We use the simple bound sum_{n>p_N} 1/(n(n-1))^2 < 1/(p_N(p_N-1)) (since
    1/(n(n-1))^2 < 1/(n(n-1)) and that telescopes); so
        sum_{k>N} w_k ≤ M0 exp(6/p_N) / (p_N(p_N-1)).
    This is generous (loose) but the 𝓜 tail is tiny anyway.
    """
    p_N = mpf(cd.primes[N - 1])
    M0 = cd.pref3[N]
    return M0 * exp(6 / p_N) / (p_N * (p_N - 1))


# ----------------------------------------------------------------------
# Driver.
# ----------------------------------------------------------------------
def compute_split(N, cd: CoordData, C0):
    s_small = sum((small_k_bound(k, cd, C0) for k in range(1, K_SMALL + 1)), mpf(0))
    s_mid = mpf(0)
    for k in range(K_SMALL + 1, N + 1):
        s_mid += mid_k_bound(k, cd, C0)
    s_tail = tail_bound_squarefree(N, cd)
    return s_small, s_mid, s_tail


def main():
    out = sys.stdout
    out.reconfigure(line_buffering=True)

    Nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 1_000_000
    sweep = [n for n in (200, 1000, 5000, 20000, 100000, 1_000_000) if n <= Nmax]
    if Nmax not in sweep:
        sweep.append(Nmax)
    sweep = sorted(set(sweep))

    print("=" * 78)
    print("CFT 2022 SQUAREFREE VALIDATION — reproduce TOTAL ≈ 0.999385 at C_0=118.")
    print("=" * 78)
    print(f"mp.dps = {mp.dps}, C_0 = {C0_DEFAULT}, K_small = {K_SMALL}")
    print()
    print("CFT published split (N = 10^6):")
    print("  small (k=1..7)     = 0.142124542  (= 194/1365)")
    print("  mid   (k=8..10^6)  = 0.856857559")
    print("  tail  (k>10^6)     = 0.000402961")
    print("  TOTAL              = 0.999385061  < 1")
    print()

    # Build the largest CoordData once, reuse prefixes for all N.
    Nbig = max(sweep)
    t = time.time()
    primes = first_n_primes(Nbig + 5)
    print(f"[sieved {len(primes)} primes, p_max = {primes[-1]}, {time.time()-t:.1f}s]")
    t = time.time()
    cd = build_coord(primes, cft_delta, S_squarefree)
    print(f"[built CoordData + prefix products, {time.time()-t:.1f}s]")
    print()

    print(f"{'N':>9} | {'p_N':>10} | {'small':>10} | {'mid':>12} | "
          f"{'tail':>12} | {'TOTAL':>12} | <1?")
    print("-" * 90)

    # Incremental mid-sum: accumulate mid terms as N grows, so total mid work
    # is O(Nbig) not O(sum of N's).
    s_small = sum((small_k_bound(k, cd, C0_DEFAULT) for k in range(1, K_SMALL + 1)),
                  mpf(0))
    s_mid_running = mpf(0)
    next_k = K_SMALL + 1
    for N in sweep:
        t = time.time()
        for k in range(next_k, N + 1):
            s_mid_running += mid_k_bound(k, cd, C0_DEFAULT)
        next_k = N + 1
        s_tail = tail_bound_squarefree(N, cd)
        total = s_small + s_mid_running + s_tail
        dt = time.time() - t
        print(f"{N:>9} | {primes[N-1]:>10} | {float(s_small):>10.6f} | "
              f"{float(s_mid_running):>12.8f} | {float(s_tail):>12.5e} | "
              f"{float(total):>12.8f} | {'YES' if total < 1 else 'no '}"
              f"  [{dt:.1f}s]")

    print()
    print("INTERPRETATION:")
    print("  - small should be 0.142124542 at all N (k=1..7 only).")
    print("  - mid should rise toward 0.856857559 as N -> 10^6.")
    print("  - tail should fall toward 0.000402961 as N -> 10^6.")
    print("  - TOTAL crossing below 1 (and approaching 0.999385) validates")
    print("    the implementation against CFT 2022.")


if __name__ == "__main__":
    main()
