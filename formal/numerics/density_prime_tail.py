"""
density_prime_tail.py — How does the "global" density
    Σ_{p prime, 5 <= p <= P} 1/(p-1)
behave as P -> ∞? This is the natural upper bound on D(L) when L is
"divisible by everything" up to P (i.e., L = lcm{1,..,P}).

By Mertens, Σ_{p <= P} 1/p ~ log log P. So Σ_{p <= P} 1/(p-1) =
Σ_{p <= P} (1/p)(1 + 1/p + O(1/p^2)) is also log log P. Therefore
D(L) -> ∞ as L -> ∞ along the "saturated" sequence L = lcm{1..P}.

This script computes the partial sums and confirms the empirical
growth rate.
"""

from __future__ import annotations

from fractions import Fraction
from math import log
from sympy import primerange


def main() -> None:
    import sys
    sys.set_int_max_str_digits(0)
    print(f"{'P':>10}  {'#primes':>8}  {'float Σ 1/(p-1)':>16}  {'log log P':>12}  {'ratio':>8}")
    print(f"{'-'*10}  {'-'*8}  {'-'*16}  {'-'*12}  {'-'*8}")
    for P in [100, 1000, 10_000, 100_000, 1_000_000]:
        primes = list(primerange(5, P + 1))
        s = sum(1.0 / (p - 1) for p in primes)
        llp = log(log(P))
        print(f"{P:>10}  {len(primes):>8}  {s:>16.6f}  {llp:>12.6f}  {s/llp:>8.4f}")


if __name__ == "__main__":
    main()
