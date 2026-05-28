"""
density_scan.py — Scan periods L > 27720 for which the density bound
D(L) < 1 still holds, giving additional verified non-existence claims
for free.

Context (Erdős Problem #273, V5). Let
    M = {p - 1 : p prime, p >= 5}       (admissible moduli)
For each period L, define
    M_L = M ∩ divisors(L),
    D(L) = sum_{m in M_L} 1/m         (computed as an exact rational).

If D(L) < 1, then by `no_strict_cover_of_low_density`
(`formal/Erdos273/CoveringSystem.lean`), there is no strict covering of
Z/LZ by progressions with moduli in M, all dividing L. Equivalently:
any hypothetical Erdős #273 covering must use a modulus that does not
divide L.

The existing verified result `no_strict_admissible_cover_27720` covers
L = 27720, where D(27720) = 953/990 ≈ 0.9626. Question: are there
L > 27720 where D(L) < 1 ALSO holds, and the corresponding M_L is
NOT a subset of M_27720 (so the bound is non-redundant)?

This script:
  1. Computes M_L and D(L) (exact Fraction) for a list of candidate L's.
  2. Reports (L, |M_L|, D(L) as Fraction, D(L) as float, D(L) < 1?).
  3. Flags which L's are "relevant" — i.e., D(L) < 1 holds AND there
     exists m in M_L with m ∤ 27720.

Conventions.
  - Divisor enumeration via sympy.divisors.
  - Primality via sympy.isprime (deterministic on this range).
  - Rational arithmetic via fractions.Fraction (kept exact).
  - 0-indexed list iteration internally; L itself is 1-indexed (positive).

Usage:
    .venv/bin/python formal/numerics/density_scan.py                # default canonical list
    .venv/bin/python formal/numerics/density_scan.py 55440 83160    # specific L's
    .venv/bin/python formal/numerics/density_scan.py --extra        # extended list
"""

from __future__ import annotations

import argparse
import sys
from fractions import Fraction
from typing import Iterable

from sympy import divisors, isprime, factorint


# ---------------------------------------------------------------------------
# Admissible set M = {p - 1 : p prime, p >= 5}.
# ---------------------------------------------------------------------------

def is_in_M(m: int) -> bool:
    """Return True iff m = p - 1 for some prime p >= 5, i.e. m >= 4 and
    m + 1 is prime."""
    return m >= 4 and isprime(m + 1)


def admissible_divisors(L: int) -> list[int]:
    """Sorted list of divisors d of L with d in M (d >= 4, d+1 prime)."""
    return sorted(d for d in divisors(L) if is_in_M(d))


def density_fraction(mods: Iterable[int]) -> Fraction:
    """Return sum_{m in mods} 1/m as an exact rational."""
    total = Fraction(0)
    for m in mods:
        total += Fraction(1, m)
    return total


# ---------------------------------------------------------------------------
# Relevance check.
# ---------------------------------------------------------------------------

# The "subsumed by 27720" check. If every m in M_L also divides 27720,
# then M_L ⊆ M_27720, and the non-existence claim at L follows trivially
# from the existing 27720 result. We want L's that introduce a *new*
# admissible modulus.
BASE_L = 27720  # 2^3 · 3^2 · 5 · 7 · 11


def new_moduli_vs_base(mods: list[int], base: int = BASE_L) -> list[int]:
    """Return the admissible moduli in `mods` that do NOT divide `base`.
    These are the moduli that make the claim "no strict cover at L"
    genuinely stronger than the corresponding claim at `base`."""
    return [m for m in mods if base % m != 0]


# ---------------------------------------------------------------------------
# Pretty factorization for the log.
# ---------------------------------------------------------------------------

def pretty_factorization(n: int) -> str:
    """Render the prime factorization of n as 2^a · 3^b · ... ."""
    f = factorint(n)
    if not f:
        return "1"
    parts = []
    for p, e in sorted(f.items()):
        parts.append(f"{p}^{e}" if e > 1 else f"{p}")
    return " · ".join(parts)


# ---------------------------------------------------------------------------
# Main scan driver.
# ---------------------------------------------------------------------------

def scan_one(L: int, base: int = BASE_L, verbose: bool = True) -> dict:
    """Compute the density data for one period L."""
    mods = admissible_divisors(L)
    n = len(mods)
    D = density_fraction(mods)
    D_float = float(D)
    below_one = D < 1
    new_mods = new_moduli_vs_base(mods, base) if L != base else []
    nonredundant = (L > base) and below_one and (len(new_mods) > 0)
    subsumed = (L > base) and (len(new_mods) == 0)

    if verbose:
        print(f"L = {L} = {pretty_factorization(L)}")
        print(f"  |M_L| = {n}")
        print(f"  D(L)  = {D}  (= {D_float:.6f})")
        print(f"  D(L) < 1 ? {below_one}")
        if L != base:
            print(f"  M_L \\ div({base}) = {new_mods}")
            print(f"  subsumed by L={base}? {subsumed}")
            print(f"  NONREDUNDANT (D<1 and new mods)? {nonredundant}")
        print(f"  M_L = {mods}")
        print()

    return {
        "L": L,
        "factorization": pretty_factorization(L),
        "moduli": mods,
        "n_moduli": n,
        "density": D,
        "density_float": D_float,
        "below_one": below_one,
        "new_moduli_vs_base": new_mods,
        "subsumed_by_base": subsumed,
        "nonredundant": nonredundant,
    }


# ---------------------------------------------------------------------------
# Candidate lists.
# ---------------------------------------------------------------------------

# Canonical list: the focused multiplier sweep over 27720.
CANONICAL_LS: list[int] = [
    # Self-check: should reproduce D(27720) = 953/990 ≈ 0.9626.
    27720,
    # Multipliers k of 27720: L = 27720 * k.
    27720 * 2,    # 55440  = 2^4 · 3^2 · 5 · 7 · 11
    27720 * 3,    # 83160  = 2^3 · 3^3 · 5 · 7 · 11
    27720 * 4,    # 110880 = 2^5 · 3^2 · 5 · 7 · 11
    27720 * 5,    # 138600 = 2^3 · 3^2 · 5^2 · 7 · 11
    27720 * 6,    # 166320 = 2^4 · 3^3 · 5 · 7 · 11
    27720 * 7,    # 194040 = 2^3 · 3^2 · 5 · 7^2 · 11
    27720 * 8,    # 221760 = 2^6 · 3^2 · 5 · 7 · 11
    27720 * 9,    # 249480 = 2^3 · 3^4 · 5 · 7 · 11
    27720 * 11,   # 304920 = 2^3 · 3^2 · 5 · 7 · 11^2
    27720 * 13,   # 360360 = 2^3 · 3^2 · 5 · 7 · 11 · 13   (known D>1)
    # New small primes p (gives modulus p-1 ∈ M if p prime).
    27720 * 17,   # 471240  — adds 16 ∈ M (17 prime)
    27720 * 19,   # 526680  — adds 18 ∈ M (19 prime, but 18 | 27720 already? 27720/18 = 1540 yes; 18 divides 27720! → check)
    27720 * 23,   # 637560  — adds 22 ∈ M? wait, 22 = 2·11 divides 27720; need new mods from 23
    27720 * 29,   # 803880  — 29 prime; 28 = 4·7 already divides 27720
    27720 * 31,   # 859320  — 31 prime; 30 = 2·3·5 already divides 27720
    27720 * 37,   # 1025640 — 37 prime; 36 = 4·9 already divides 27720
    27720 * 41,   # 1136520 — 41 prime; 40 = 8·5 already divides 27720
    27720 * 43,   # 1192560 — 43 prime; 42 = 2·3·7 already divides 27720
    # Some other interesting variants.
    27720 * 16,   # 443520 = 2^7 · 3^2 · 5 · 7 · 11
    27720 * 25,   # 693000 = 2^3 · 3^2 · 5^3 · 7 · 11
    27720 * 27,   # 748440 = 2^3 · 3^5 · 5 · 7 · 11
    27720 * 49,   # 1358280 = 2^3 · 3^2 · 5 · 7^3 · 11
    27720 * 121,  # 3354120 = 2^3 · 3^2 · 5 · 7 · 11^3
    # Compound multipliers.
    27720 * 2 * 3,    # = 27720 * 6, already above
    27720 * 4 * 9,    # = 27720 * 36 = 997920
    27720 * 8 * 27,   # = 27720 * 216 = 5987520
    # Variants NOT divisible by 27720: drop 2-adic, add new prime.
    13860 * 13,       # = 180180 = 2^2 · 3^2 · 5 · 7 · 11 · 13
    13860 * 17,       # = 235620 = 2^2 · 3^2 · 5 · 7 · 11 · 17
    13860 * 19,       # = 263340 = 2^2 · 3^2 · 5 · 7 · 11 · 19
    13860 * 23,       # = 318780
    13860 * 29,       # = 401940
    13860 * 31,       # = 429660
    13860 * 37,       # = 512820
    13860 * 41,       # = 568260
    13860 * 43,       # = 595980
    13860 * 47,       # = 651420
    13860 * 53,       # = 734580
    # Multipliers that combine 13 with the 27720-divisors-style multiplier.
    13860 * 13 * 3,   # = 540540 = 2^2 · 3^3 · 5 · 7 · 11 · 13
    13860 * 13 * 5,   # = 900900 = 2^2 · 3^2 · 5^2 · 7 · 11 · 13
    13860 * 13 * 7,   # = 1261260
    13860 * 13 * 11,  # = 1981980
]


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("Ls", nargs="*", type=int,
                    help="period(s) L to scan (omit for canonical list)")
    ap.add_argument("--base", type=int, default=BASE_L,
                    help=f"base L for the redundancy check (default {BASE_L})")
    args = ap.parse_args()

    if args.Ls:
        Ls = sorted(set(args.Ls))
    else:
        Ls = sorted(set(CANONICAL_LS))

    results = []
    print("=" * 78)
    print(f"density_scan.py: D(L) = sum_{{m | L, m+1 prime, m >= 4}} 1/m")
    print(f"Base for redundancy: L = {args.base} = {pretty_factorization(args.base)}")
    print("=" * 78)
    print()
    for L in Ls:
        r = scan_one(L, base=args.base, verbose=True)
        results.append(r)

    # ---- Summary table -------------------------------------------------------
    print("=" * 78)
    print("SUMMARY TABLE")
    print("=" * 78)
    header = (
        f"{'L':>10}  {'|M_L|':>5}  {'D(L) (Fraction)':>22}  "
        f"{'D(L)':>9}  {'<1?':>4}  {'new mods?':>9}  {'NONREDUND.':>10}"
    )
    print(header)
    print("-" * len(header))
    for r in results:
        n_new = len(r["new_moduli_vs_base"])
        nr = "YES" if r["nonredundant"] else ("base" if r["L"] == args.base else "no")
        print(
            f"{r['L']:>10}  {r['n_moduli']:>5}  "
            f"{str(r['density']):>22}  "
            f"{r['density_float']:>9.6f}  "
            f"{('YES' if r['below_one'] else 'no'):>4}  "
            f"{n_new:>9}  "
            f"{nr:>10}"
        )

    # ---- Winners (nonredundant): L's that genuinely strengthen 27720. --------
    winners = [r for r in results if r["nonredundant"]]
    print()
    print("=" * 78)
    print(f"WINNERS: L > {args.base} with D(L) < 1 AND M_L \\not\\subseteq M_{args.base}")
    print("=" * 78)
    if not winners:
        print(f"(none of the scanned L's are nonredundant winners)")
    else:
        for r in winners:
            print(
                f"  L = {r['L']:>8} = {r['factorization']}"
                f" :  D = {r['density']} ≈ {r['density_float']:.6f},"
                f" new moduli = {r['new_moduli_vs_base']}"
            )

    # ---- Subsumed: L > base with D(L) < 1 but every m | base. ----------------
    subsumed = [r for r in results if r["L"] > args.base and r["below_one"]
                and not r["nonredundant"]]
    if subsumed:
        print()
        print("=" * 78)
        print(f"SUBSUMED: L > {args.base} with D(L) < 1 but every m in M_L divides {args.base}")
        print("=" * 78)
        for r in subsumed:
            print(f"  L = {r['L']} : every admissible divisor already divides {args.base}")

    # ---- Failed: L's with D(L) >= 1. -----------------------------------------
    failed = [r for r in results if not r["below_one"]]
    if failed:
        print()
        print("=" * 78)
        print("FAILED density (D(L) >= 1) — these L's give NO direct conclusion")
        print("=" * 78)
        for r in failed:
            print(f"  L = {r['L']:>8}: D(L) = {r['density']} ≈ {r['density_float']:.6f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
