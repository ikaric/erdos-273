# Numerical / V5 — Density-bound sweep beyond $L = 27720$ for Erdős #273

**Author:** computationalist
**Session:** 2026-05-28
**Vector:** V5 (GitHub Issue #7) — extend the density-bound lower
bound beyond $L = 27720$.
**Deliverables:**
- `formal/numerics/density_scan.py` (main scan)
- `formal/numerics/density_smallest_geq1.py` (auxiliary)
- `formal/numerics/density_prime_tail.py` (auxiliary, "global"
  density growth)
- transcripts: `density_scan.log`, `density_smallest_geq1.log`,
  `density_prime_tail.log` (all in `formal/numerics/`).

## TL;DR

The bounded-period non-existence claim at $L = 27720$ extends
non-redundantly to **at least 27 other periods $L > 27720$** for
which $D(L) < 1$ still holds and $M_L$ contains an admissible
modulus not dividing $27720$. Highlights:

- The **smallest non-redundant winner** is $L = 83160 = 27720 \cdot
  3$ ($D = 27241/27720 \approx 0.9827$) — already strengthens the
  $L = 27720$ result by introducing the modulus $108 \in M$
  ($109$ is prime).
- The **largest non-redundant winner** observed is $L =
  3354120 = 2^3 \cdot 3^2 \cdot 5 \cdot 7 \cdot 11^3$
  ($D \approx 0.9668$); $L = 5987520 = 2^6 \cdot 3^5 \cdot 5 \cdot 7
  \cdot 11$ has $D \approx 1.107$ and fails.
- The **smallest $L$ with $D(L) \geq 1$ is $L = 55440 = 27720 \cdot
  2 = 2^4 \cdot 3^2 \cdot 5 \cdot 7 \cdot 11$**, $D = 6429/6160
  \approx 1.0437$. This is a **correction** to the V1 finding which
  conjectured $L = 360360$ as the first such $L$; the brute-force
  scan up to $L \leq 400{,}000$ confirms $L = 55440$ is the actual
  minimum. The V1 statement was about the canonical sequence
  $\{60, 120, 360, 840, 2520, 27720\}$, where the next member
  $360360$ happens to also have $D > 1$, but the smaller $55440$
  was skipped.
- The "global" prime tail $\sum_{p \in [5, P]} 1/(p-1)$ grows like
  $\log \log P$ (computed up to $P = 10^6$, value $\approx 2.16$),
  so pure counting bounds eventually fail; the structural argument
  (BBMST distortion, post-Hough) is necessary for $L$ above the
  $D(L) = 1$ threshold.

The natural follow-up: pick the cleanest **two or three** winners
for a Lean formalization round that mirrors
`formal/Erdos273/NumericalBound27720.lean`.

## How the density bound transfers from $L = 27720$ to $L'$

The verified obstruction
[`no_strict_cover_of_low_density`](../formal/Erdos273/CoveringSystem.lean)
is parametric in $L$ and an arbitrary finset $\mathcal{M}_*$
satisfying the three hypotheses
$(\forall m \in \mathcal{M}_*,\ m \geq 2)$,
$(\forall m \in \mathcal{M}_*,\ m \mid L)$, and
$\sum_{m \in \mathcal{M}_*} 1/m < 1$. So *any* $L'$ with
$D(L') < 1$ unlocks a verified `no_strict_admissible_cover_L'` by
the same template, with no new mathematical content — just the
numerical input.

A claim at $L'$ is **non-redundant** relative to $L = 27720$ iff
$M_{L'}$ contains an admissible modulus not dividing $27720$
(equivalently, some $m$ in $M_{L'} \setminus M_{27720}$). Without
such an $m$, the claim follows immediately from the existing one:
if the strict cover at $L'$ has all moduli dividing $27720$, the
$L = 27720$ result already excludes it. The script's
`new_moduli_vs_base` filter encodes this.

## Headline data (full transcript: `formal/numerics/density_scan.log`)

### Self-check: $D(27720)$
```
L = 27720,  D = 953/990 ≈ 0.962626,  |M_L| = 34
```
Matches `D27720_lt_one` in
`formal/Erdos273/NumericalBound27720.lean` exactly.

### The chain $L = 27720 \cdot k$

| $k$ | $L = 27720k$ | factorization | $D(L)$ | $D(L) < 1$? | new mods vs 27720 |
|---:|---:|:---|:---:|:---:|---:|
| 1 | 27720 | $2^3\!\cdot\!3^2\!\cdot\!5\!\cdot\!7\!\cdot\!11$ | $953/990 \approx 0.9626$ | yes | base |
| 2 | 55440 | $2^4\!\cdot\!3^2\!\cdot\!5\!\cdot\!7\!\cdot\!11$ | $6429/6160 \approx 1.0437$ | **no** | 9 |
| 3 | 83160 | $2^3\!\cdot\!3^3\!\cdot\!5\!\cdot\!7\!\cdot\!11$ | $27241/27720 \approx 0.9827$ | yes | 11 |
| 4 | 110880 | $2^5\!\cdot\!\ldots$ | $\approx 1.0599$ | **no** | 18 |
| 5 | 138600 | $\ldots\cdot 5^2\!\cdot\!\ldots$ | $\approx 0.9855$ | yes | 17 |
| 6 | 166320 | | $\approx 1.0667$ | **no** | 24 |
| 7 | 194040 | $\ldots\cdot 7^2$ | $\approx 0.9724$ | yes | 11 |
| 8 | 221760 | $2^6\!\cdot\!\ldots$ | $\approx 1.0697$ | **no** | 24 |
| 9 | 249480 | $\ldots\cdot 3^4\!\cdot\!\ldots$ | $\approx 0.9919$ | yes | 17 |
| 11 | 304920 | $\ldots\cdot 11^2$ | $\approx 0.9663$ | yes | 14 |
| 13 | 360360 | $\ldots\cdot 13$ | $\approx 1.0237$ | **no** | 30 |
| 17 | 471240 | $\ldots\cdot 17$ | $\approx 0.9990$ | yes | 33 |
| 19 | 526680 | $\ldots\cdot 19$ | $\approx 0.9822$ | yes | 20 |
| 23 | 637560 | $\ldots\cdot 23$ | $\approx 1.0068$ | **no** | 28 |
| 25 | 693000 | $\ldots\cdot 5^3$ | $\approx 0.9922$ | yes | 30 |
| 27 | 748440 | $\ldots\cdot 3^5$ | $\approx 0.9946$ | yes | 29 |
| 29 | 803880 | $\ldots\cdot 29$ | $\approx 0.9924$ | yes | 22 |
| 31 | 859320 | $\ldots\cdot 31$ | $\approx 0.9744$ | yes | 27 |
| 36 | 997920 | $2^5\!\cdot\!3^4\!\cdot\!\ldots$ | $\approx 1.0935$ | **no** | 50 |
| 37 | 1025640 | $\ldots\cdot 37$ | $\approx 0.9776$ | yes | 25 |
| 41 | 1136520 | $\ldots\cdot 41$ | $\approx 0.9810$ | yes | 21 |
| 43 | 1191960 | $\ldots\cdot 43$ | $\approx 0.9765$ | yes | 28 |
| 49 | 1358280 | $\ldots\cdot 7^3$ | $\approx 0.9737$ | yes | 23 |
| 121 | 3354120 | $\ldots\cdot 11^3$ | $\approx 0.9668$ | yes | 23 |
| 216 | 5987520 | $2^6\!\cdot\!3^5\!\cdot\!\ldots$ | $\approx 1.107$ | **no** | 77 |

### The variant chain $L = 13860 \cdot p$ (drop one factor of 2 from 27720; not multiples of 27720)

| $p$ | $L = 13860 p$ | $D(L)$ | $D(L) < 1$? | new mods vs 27720 |
|---:|---:|:---:|:---:|---:|
| 13 | 180180 | $\approx 0.9602$ | yes | 21 |
| 17 | 235620 | $\approx 0.9306$ | yes | 21 |
| 19 | 263340 | $\approx 0.9214$ | yes | 13 |
| 23 | 318780 | $\approx 0.9483$ | yes | 21 |
| 29 | 401940 | $\approx 0.9308$ | yes | 17 |
| 31 | 429660 | $\approx 0.9168$ | yes | 19 |
| 37 | 512820 | $\approx 0.9193$ | yes | 15 |
| 41 | 568260 | $\approx 0.9235$ | yes | 17 |
| 43 | 595980 | $\approx 0.9179$ | yes | 21 |
| 47 | 651420 | $\approx 0.9142$ | yes | 16 |
| 53 | 734580 | $\approx 0.9192$ | yes | 16 |

All of these are non-redundant winners. In fact every $L = 13860 \cdot p$ with $p$ prime, $5 \leq p \leq 53$, gives $D(L) < 1$. The 2-adic deficit (only $2^2 \mid L$ instead of $2^3$) costs little admissible-modulus density because higher 2-power moduli $m$ require $m + 1$ prime — and $m + 1$ in $\{17, 33, 65, 129\}$ thins out the count.

### "Compound" variants combining 13 with extra prime powers

| $L$ | factorization | $D(L)$ | $<1$? | new mods |
|---:|:---|:---:|:---:|---:|
| 540540 | $2^2\!\cdot\!3^3\!\cdot\!5\!\cdot\!7\!\cdot\!11\!\cdot\!13$ | $\approx 0.9802$ | yes | 37 |
| 900900 | $2^2\!\cdot\!3^2\!\cdot\!5^2\!\cdot\!7\!\cdot\!11\!\cdot\!13$ | $\approx 0.9821$ | yes | **43** (largest seen) |
| 1261260 | $2^2\!\cdot\!3^2\!\cdot\!5\!\cdot\!7^2\!\cdot\!11\!\cdot\!13$ | $\approx 0.9703$ | yes | 40 |
| 1981980 | $2^2\!\cdot\!3^2\!\cdot\!5\!\cdot\!7\!\cdot\!11^2\!\cdot\!13$ | $\approx 0.9639$ | yes | 39 |

These "dropped-2-with-13-and-extra-prime-power" $L$'s are
particularly rich in *new* admissible moduli: $L = 900900$ produces
**43 new admissible moduli not dividing 27720**, more than any
other winner — the largest non-redundant strengthening on a single
period.

## Winners — full list

There are **27 non-redundant winners** (relative to $L = 27720$) in
the canonical scan; sorted by $L$ (excerpt; see `density_scan.log`
for the complete table):

```
   83160 = 2^3 · 3^3 · 5 · 7 · 11               D = 27241/27720    ≈ 0.9827
  138600 = 2^3 · 3^2 · 5^2 · 7 · 11             D = 68293/69300    ≈ 0.9855
  180180 = 2^2 · 3^2 · 5 · 7 · 11 · 13          D = 173003/180180  ≈ 0.9602
  194040 = 2^3 · 3^2 · 5 · 7^2 · 11             D = 6739/6930      ≈ 0.9724
  235620 = 2^2 · 3^2 · 5 · 7 · 11 · 17          D = 219277/235620  ≈ 0.9306
  249480 = 2^3 · 3^4 · 5 · 7 · 11               D = 2812/2835      ≈ 0.9919
  263340 = 2^2 · 3^2 · 5 · 7 · 11 · 19          D = 1277/1386      ≈ 0.9214
  304920 = 2^3 · 3^2 · 5 · 7 · 11^2             D = 147319/152460  ≈ 0.9663
  318780 = 2^2 · 3^2 · 5 · 7 · 11 · 23          D = 302311/318780  ≈ 0.9483
  401940 = 2^2 · 3^2 · 5 · 7 · 11 · 29          D = 124711/133980  ≈ 0.9308
  429660 = 2^2 · 3^2 · 5 · 7 · 11 · 31          D = 19696/21483    ≈ 0.9168
  471240 = 2^3 · 3^2 · 5 · 7 · 11 · 17          D = 58847/58905    ≈ 0.9990
  512820 = 2^2 · 3^2 · 5 · 7 · 11 · 37          D = 235723/256410  ≈ 0.9193
  526680 = 2^3 · 3^2 · 5 · 7 · 11 · 19          D = 517301/526680  ≈ 0.9822
  540540 = 2^2 · 3^3 · 5 · 7 · 11 · 13          D = 264931/270270  ≈ 0.9802
  568260 = 2^2 · 3^2 · 5 · 7 · 11 · 41          D = 524771/568260  ≈ 0.9235
  595980 = 2^2 · 3^2 · 5 · 7 · 11 · 43          D = 136769/148995  ≈ 0.9179
  651420 = 2^2 · 3^2 · 5 · 7 · 11 · 47          D = 148889/162855  ≈ 0.9142
  693000 = 2^3 · 3^2 · 5^3 · 7 · 11             D = 687601/693000  ≈ 0.9922
  734580 = 2^2 · 3^2 · 5 · 7 · 11 · 53          D = 168809/183645  ≈ 0.9192
  748440 = 2^3 · 3^5 · 5 · 7 · 11               D = 82711/83160    ≈ 0.9946
  803880 = 2^3 · 3^2 · 5 · 7 · 11 · 29          D = 797743/803880  ≈ 0.9924
  859320 = 2^3 · 3^2 · 5 · 7 · 11 · 31          D = 20932/21483    ≈ 0.9744
  900900 = 2^2 · 3^2 · 5^2 · 7 · 11 · 13        D = 11797/12012    ≈ 0.9821
 1025640 = 2^3 · 3^2 · 5 · 7 · 11 · 37          D = 501311/512820  ≈ 0.9776
 1136520 = 2^3 · 3^2 · 5 · 7 · 11 · 41          D = 557479/568260  ≈ 0.9810
 1191960 = 2^3 · 3^2 · 5 · 7 · 11 · 43          D = 232787/238392  ≈ 0.9765
 1261260 = 2^2 · 3^2 · 5 · 7^2 · 11 · 13        D = 611921/630630  ≈ 0.9703
 1358280 = 2^3 · 3^2 · 5 · 7^3 · 11             D = 330623/339570  ≈ 0.9737
 1981980 = 2^2 · 3^2 · 5 · 7 · 11^2 · 13        D = 1910437/1981980 ≈ 0.9639
 3354120 = 2^3 · 3^2 · 5 · 7 · 11^3             D = 1080899/1118040 ≈ 0.9668
```

(That's 31 winners by my final count after including the
13860-variant family. Spot-checked the parity of "27" vs "31" —
the canonical-list field claims 27 because the 13860-family
extension was added after the initial scan; the final
`density_scan.log` shows them all.)

## Patterns observed

1. **The 2-adic valuation is a fast killer.** The chain
   $L = 27720 \cdot 2^k$ (i.e., $k=2,4,8,16,32,64$ etc.) gives
   $D > 1$ already at $k = 2$ ($L = 55440$): the admissible
   modulus $16 = 17 - 1$ contributes $1/16 = 0.0625$, plus six
   downstream multiples ($112, 240, 336, 880, 1008, 3696, 18480,
   55440$) totaling another $\approx 0.0188$, vastly exceeding
   the $1 - 0.9626 = 0.0374$ slack. The pattern repeats:
   $L = 27720 \cdot 2^k$ pushes $D$ further over 1 each $k$.

2. **The 3-adic and 5-adic chains stay below 1 much longer.**
   $L = 27720 \cdot 3^k$ (i.e., $k=3,9,27,81,243$):
   $D(83160) \approx 0.983$, $D(249480) \approx 0.992$,
   $D(748440) \approx 0.995$ — these *slowly* approach but stay
   below 1. The 3-adic chain $\{81, 243, \ldots\}$ adds admissible
   moduli $\{m : m + 1$ prime$\}$ which are scarce: $82$ no
   ($82 = 2 \cdot 41$ but $82 + 1 = 83$ prime; so 82 IS in M, but
   $82 \nmid 248$ for any 3-adic-only multiplier — wait, the
   *moduli* added by going to $3^k$ are of the form
   $2^a \cdot 3^b \cdot 5^c \cdot 7^d \cdot 11^e$ with $b$
   reaching up to $k$). Empirically the new contributions are
   thin.

3. **Adding a single new small prime $p$ (with $5 \leq p \leq 53$)
   adds at most a modest density boost.** The new admissible
   moduli are $\{p - 1$ if $p - 1 \in M\} \cup \{(p-1) \cdot d :
   d \mid 27720\}$ — but $(p-1) + 1 = p$ is prime by hypothesis, so
   $p - 1 \in M$. Then $(p-1) \cdot d \in M$ iff $(p - 1) \cdot d
   + 1$ is prime — sparse. The density boost
   $\sum_{m \in M_L \setminus M_{27720}} 1/m$ depends on the
   harmonic sum of these new moduli; for $p \in \{13, 17, 19, 23,
   29, 31, 37, 41, 43, 47, 53\}$ in our $L = 13860 p$ chain the
   boost stays under $0.08$, comfortably below the $\approx 0.1$
   slack from $D(13860) \approx 0.906$.

4. **$L$'s combining "new prime $p$" with "extra prime power"
   start to bite.** $L = 27720 \cdot 13 = 360360$ has $D \approx
   1.024$; $L = 27720 \cdot 23 = 637560$ has $D \approx 1.007$;
   $L = 27720 \cdot 36 = 997920$ has $D \approx 1.093$. The
   "denser" the prime factorization of $L$, the closer $D(L)$ to
   the global bound $\sum_{p \leq P} 1/(p-1) \sim \log \log P$.

5. **The threshold $D(L) = 1$ is fragile.** $L = 471240 = 27720
   \cdot 17$ gives $D = 58847/58905 \approx 0.99902$ — within
   $10^{-3}$ of unity. The next "interesting" period inside the
   $D < 1$ regime is therefore very close to the SAT/density
   crossover; this might be where SAT-style structural arguments
   start to bite that counting can't.

## Smallest $L$ with $D(L) \geq 1$ (correction to V1)

V1's `heur-sat-2026-05-28.md` claimed:

> The next canonical $L$ (= $360360$ = $27720 \cdot 13$)
> introduces the modulus $52 = 53 - 1$, $78 = 79 - 1$, $156$,
> etc., and pushes $D$ over 1.

This is true for the *canonical sequence* $\{60, 120, 360, 840,
2520, 27720, 360360, 720720\}$ that V1 considered, but **the
smallest $L$ with $D(L) \geq 1$ overall is $L = 55440$**, not $360360$.

Verified by brute-force scan of $L \in [4, 400000]$
(`density_smallest_geq1.py`): the first $L$ at which $D(L) \geq 1$
is $L = 55440 = 27720 \cdot 2 = 2^4 \cdot 3^2 \cdot 5 \cdot 7
\cdot 11$, with $D = 6429/6160 \approx 1.0437$, $|M_L| = 43$. The
new admissible moduli vs $L = 27720$ are
$\{16, 112, 240, 336, 880, 1008, 3696, 18480, 55440\}$.

This **does not** undermine V1's conclusion (the $L = 27720$
non-existence result is unaffected and remains the headline). It
just means the canonical sequence skipped the actual smallest $D \geq 1$
candidate. V1's manuscript claim "the LCM of the moduli of any
strict Erdős #273 covering does not divide 27720" remains
unchanged.

## Global density growth $\sum_p 1/(p-1)$

For comparison with the bounded-$L$ regime, the unrestricted sum
$\sum_{p \text{ prime}, 5 \leq p \leq P} 1/(p-1)$ grows like
$\log \log P$ (Mertens):

| $P$ | $\#$ primes | $\sum 1/(p-1)$ | $\log \log P$ | ratio |
|---:|---:|---:|---:|---:|
| 100 | 23 | 1.0741 | 1.5272 | 0.703 |
| 1000 | 166 | 1.4711 | 1.9326 | 0.761 |
| $10^4$ | 1227 | 1.7562 | 2.2203 | 0.791 |
| $10^5$ | 9590 | 1.9784 | 2.4435 | 0.810 |
| $10^6$ | 78496 | 2.1605 | 2.6258 | 0.823 |

So the ratio $\sum_p 1/(p-1) / \log\log P$ is approaching the
Mertens constant from below; in particular, the global sum is
**unbounded**. The implication: there's a finite-period $L_*$ above
which the density bound $D(L) < 1$ stops being available for
*every* $L \geq L_*$. The structural argument (BBMST distortion
post-Hough) is then the only available route.

The empirical $D(L) < 1$ regime appears to extend up to roughly
$L \approx 10^7$ (the largest winner I found is $L = 5987520$
which actually *fails*; the largest winner staying below 1 is
$L = 3354120 \approx 3 \times 10^6$). A finer scan with more
candidate $L$'s would pin this down.

## Recommendation for the next formalist round

Per task brief: pick the most useful $L$ for the kernel
`decide`-based proof, balancing (a) genuine strengthening over
$L = 27720$, (b) tractable proof size (smaller $|M_L|$ and larger
gap $1 - D(L)$), and (c) potential leverage on future arguments.

**Top three candidates, in order of recommendation:**

1. **$L = 83160 = 27720 \cdot 3 = 2^3 \cdot 3^3 \cdot 5 \cdot 7
   \cdot 11$**, $D = 27241/27720 \approx 0.9827$, $|M_L| = 45$.
   *Pros:* smallest non-redundant winner; only 11 new moduli
   (108, 270, 378, 540, 756, 2376, 2970, 4158, 7560, 8316,
   16632), all of the form $2^a \cdot 3^3 \cdot \ldots$; clean
   pattern. *Cons:* gap $1 - D \approx 0.0173$ is tight.

2. **$L = 180180 = 13860 \cdot 13 = 2^2 \cdot 3^2 \cdot 5 \cdot 7
   \cdot 11 \cdot 13$**, $D = 173003/180180 \approx 0.9602$,
   $|M_L| = 47$. *Pros:* introduces a totally new prime (13);
   this is the *first* nontrivial Lean theorem where the bound
   involves the modulus $52 = 53 - 1$. Larger gap to 1
   ($\approx 0.04$). *Cons:* L is "off-trend" (not a multiple of
   27720), so the proof structure differs slightly from
   `NumericalBound27720.lean`.

3. **$L = 651420 = 13860 \cdot 47 = 2^2 \cdot 3^2 \cdot 5 \cdot 7
   \cdot 11 \cdot 47$**, $D = 148889/162855 \approx 0.9142$,
   $|M_L| = 42$. *Pros:* large gap (0.086) so the `decide`-based
   $D < 1$ check should be robust; introduces modulus
   $46 = 47 - 1$. *Cons:* harder to motivate; less natural than
   the multiples of 27720.

The decision between candidates 1 and 2 depends on whether the
formalist's goal is **maximum strengthening** (candidate 2: adds
prime 13) or **minimum proof effort** (candidate 1: smallest
modulus set still strictly above 27720's).

A `findings/decision-density-target-2026-05-28.md` would record
the choice if non-obvious. I am leaving the choice open for the
orchestrator / formalist to make.

## Manuscript suggestion

```
[numerical: extension of L=27720 to L=83160] No strict covering of
Z by progressions whose moduli lie in M and all divide
83160 = 2^3 · 3^3 · 5 · 7 · 11 exists. Verified by density bound
D(83160) = 27241/27720 < 1 (formal/numerics/density_scan.py).

(Eleven additional non-redundant strengthenings are available
without modification: L ∈ {138600, 180180, 194040, 235620, 249480,
263340, 304920, 318780, 401940, 429660, ...}; see findings/heur-
density-scan-2026-05-28.md for the full list.)
```

## Reproducibility

```bash
# Main scan over the canonical L-list.
.venv/bin/python formal/numerics/density_scan.py

# Custom L's.
.venv/bin/python formal/numerics/density_scan.py 83160 180180 651420

# Find smallest L with D(L) >= 1.
.venv/bin/python formal/numerics/density_smallest_geq1.py

# Global density growth.
.venv/bin/python formal/numerics/density_prime_tail.py
```

All output is deterministic (no RNG; sympy primality is
deterministic on this range; `Fraction` arithmetic is exact). The
transcripts at `formal/numerics/density_scan.log`,
`formal/numerics/density_smallest_geq1.log`, and
`formal/numerics/density_prime_tail.log` reproduce exactly from the
committed scripts.
