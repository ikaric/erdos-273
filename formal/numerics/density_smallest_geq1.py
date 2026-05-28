"""
density_smallest_geq1.py — Auxiliary scan to find the smallest L with
D(L) >= 1, where D(L) = sum_{m | L, m+1 prime, m >= 4} 1/m.

Strategy: D(L) only depends on the SQUAREFREE-like "richness" of L's
divisor lattice, not on L itself — adding extra prime factors monotone
increases D(L), but the same admissible divisors are inherited
whenever m | L_old ⊆ L_new.

We iterate L over multiples of 12 in increasing order (12 is the
smallest L containing two distinct primes p-1, but actually 4 already
has D(4) = 1/4). Brute-force scan is feasible up to a few hundred
thousand.

We also report the smallest L for which D(L) >= 1 in the family
L = 27720 * k, k = 1, 2, 3, ... (the "natural multiplicative
neighborhood" of 27720).
"""

from __future__ import annotations

from fractions import Fraction
from sympy import divisors, isprime


def is_in_M(m: int) -> bool:
    return m >= 4 and isprime(m + 1)


def D_of(L: int) -> Fraction:
    total = Fraction(0)
    for d in divisors(L):
        if is_in_M(d):
            total += Fraction(1, d)
    return total


def find_smallest_L_with_D_geq_one(L_max: int = 400_000) -> tuple[int | None, Fraction]:
    """Brute-force search for the smallest L with D(L) >= 1."""
    smallest = None
    smallest_D = Fraction(0)
    for L in range(4, L_max + 1):
        D = D_of(L)
        if D >= 1:
            smallest = L
            smallest_D = D
            break
    return smallest, smallest_D


def scan_multiples_of_27720(k_max: int = 50) -> list[tuple[int, int, Fraction, float]]:
    """For k = 1..k_max, compute D(27720 * k) and report whether < 1."""
    out = []
    for k in range(1, k_max + 1):
        L = 27720 * k
        D = D_of(L)
        out.append((k, L, D, float(D)))
    return out


if __name__ == "__main__":
    print("=" * 78)
    print("Smallest L with D(L) >= 1 (brute force, L up to 400_000)")
    print("=" * 78)
    L_star, D_star = find_smallest_L_with_D_geq_one(L_max=400_000)
    if L_star is None:
        print("No such L found within the search budget.")
    else:
        from sympy import factorint
        fac = " · ".join(
            f"{p}^{e}" if e > 1 else str(p)
            for p, e in sorted(factorint(L_star).items())
        )
        print(f"L* = {L_star} = {fac}")
        print(f"D(L*) = {D_star} ≈ {float(D_star):.6f}")
        # Show the moduli.
        mods = [d for d in divisors(L_star) if is_in_M(d)]
        print(f"|M_{{L*}}| = {len(mods)}")
        print(f"M_{{L*}} = {mods}")

    print()
    print("=" * 78)
    print("D(27720 * k) for k = 1..30")
    print("=" * 78)
    print(f"{'k':>4}  {'L':>10}  {'D(L)':>30}  {'D(L) float':>10}  {'<1?':>4}")
    for k, L, D, Df in scan_multiples_of_27720(k_max=30):
        flag = "YES" if D < 1 else "no"
        print(f"{k:>4}  {L:>10}  {str(D):>30}  {Df:>10.6f}  {flag:>4}")
