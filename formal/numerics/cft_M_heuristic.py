#!/usr/bin/env python3
"""Heuristic 𝓜-density-corrected CFT sum for Erdős Problem #273.

⚠️  HEURISTIC — NOT a validated CFT specialization. ⚠️

This reuses the CFT 2022 squarefree machinery (validated to 8 digits in
`cft_validate_squarefree.py`: TOTAL = 0.99938506 at C_0=118, N=10^6,
matching CFT's published 0.999385061449) but with the coordinate sizes
replaced by the librarian survey's 𝓜 "density-factor" heuristic:

    |S_2|^M = 2,    |S_j|^M = p_j (p_j - 1)  for p_j ≥ 3.

WHY THIS IS A HEURISTIC, NOT A THEOREM
======================================
In the genuine CFT framework, for squarefree distinct moduli the
hyperplane fixed-coordinate norm equals the modulus:
        ‖F(A)‖ = ∏_{j∈F(A)} |S_j| = ∏_{j∈F(A)} p_j = m,
so the running constraint ‖F(A)‖ > C_0 says exactly "modulus > C_0", and
the bound C_0 = 118 IS a min-modulus bound. Under the S_M substitution,
        ‖F(A)‖^M = ∏ p_j(p_j-1)  ≠  m = q-1,
so the threshold C_0/|S_k| and the constraint no longer track the modulus.
The number this script reports is therefore the smallest C_0 making a
DENSITY-CORRECTED majorant sum drop below 1 — evidence about the relative
"hardness" of 𝓜-covering under the distortion heuristic, NOT a proven
min-modulus bound for 𝓜. See findings/heur-cft-Mbound-2026-05-28.md.

INVOKE
======
    uv run python3 formal/numerics/cft_M_heuristic.py [N]

Author: computationalist (V3). Date: 2026-05-28.
"""
from __future__ import annotations

import sys
import time

from mpmath import mp, mpf

import cft_validate_squarefree as cft  # validated machinery

mp.dps = 30


def compute_total_M(N, cd, C0):
    """small + mid + tail using S_M coordinate sizes."""
    s_small = sum(
        (cft.small_k_bound(k, cd, C0) for k in range(1, cft.K_SMALL + 1)), mpf(0)
    )
    s_mid = mpf(0)
    for k in range(cft.K_SMALL + 1, N + 1):
        s_mid += cft.mid_k_bound(k, cd, C0)
    s_tail = cft.tail_bound_M(N, cd)
    return s_small, s_mid, s_tail


def smallest_C0(N, cd, lo, hi):
    """Smallest integer C_0 in [lo, hi] with TOTAL < 1 (monotone decreasing)."""
    def tot(C0):
        a, b, c = compute_total_M(N, cd, C0)
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
    print("HEURISTIC 𝓜-density-corrected CFT sum (Erdős #273, V3).")
    print("=" * 78)
    print("⚠️  Heuristic only — see module docstring + findings note.")
    print(f"mp.dps = {mp.dps}, N = {N}, K_small = {cft.K_SMALL}")
    print(f"|S_j|^M = p_j(p_j-1) for p_j>=3,  |S_2|^M = 2.")
    print()

    t = time.time()
    primes = cft.first_n_primes(N + 5)
    cd = cft.build_coord(primes, cft.cft_delta, cft.S_M)
    print(f"[sieve+build: {time.time()-t:.1f}s, p_N = {primes[N-1]}]")
    print(f"|S_j|^M[0..9] = {[float(x) for x in cd.S[:10]]}")
    print()

    # Show the split at the squarefree baseline C_0 = 118.
    print("-" * 78)
    print("Split at C_0 = 118 (same C_0 as the squarefree baseline):")
    a, b, c = compute_total_M(N, cd, 118)
    print(f"  small = {float(a):.6f}  mid = {float(b):.6f}  tail = {float(c):.3e}")
    print(f"  TOTAL = {float(a+b+c):.6f}   (<1? {a+b+c < 1})")
    print()

    # Bisect for the smallest C_0 with TOTAL < 1.
    print("-" * 78)
    print("Smallest C_0 with heuristic TOTAL < 1:")
    t = time.time()
    C0, total = smallest_C0(N, cd, lo=1, hi=200000)
    print(f"  [bisection: {time.time()-t:.1f}s]")
    if C0 is None:
        print(f"  No C_0 ≤ 200000 gives TOTAL < 1 (TOTAL at 200000 = {float(total):.6f}).")
    else:
        a, b, c = compute_total_M(N, cd, C0)
        print(f"  ==> C_𝓜(heuristic) = {C0}")
        print(f"      split: small={float(a):.6f} mid={float(b):.6f} tail={float(c):.3e}")
        print(f"      TOTAL = {float(a+b+c):.8f} < 1")
        # also show C0-1 is >= 1
        a2, b2, c2 = compute_total_M(N, cd, C0 - 1)
        print(f"      check C_0={C0-1}: TOTAL = {float(a2+b2+c2):.8f}"
              f" ({'<1' if a2+b2+c2 < 1 else '>=1'})")
    print()
    print("COMPARISON:")
    print("  squarefree (validated CFT)    : C_0 = 118")
    print("  BBMST universal (published)   : 615,999")
    print(f"  𝓜 heuristic (this script, N={N}): "
          f"{'>200000' if C0 is None else C0}")
    print()
    print("⚠️  The 𝓜 number is HEURISTIC: ‖F(A)‖^M ≠ modulus, so it is NOT a")
    print("    proven min-modulus bound. It indicates relative hardness only.")


if __name__ == "__main__":
    main()
