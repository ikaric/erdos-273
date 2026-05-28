"""
sat_covering.py — SAT encoding for the bounded-period instance of
Erdős Problem #273.

Question (Erdős #273). Does there exist a covering system
{a_i (mod m_i)} of Z such that every modulus m_i is of the form
p_i - 1 for some prime p_i >= 5? Equivalently, every m_i lies in

    M = {p - 1 : p prime, p >= 5}
      = {4, 6, 10, 12, 16, 18, 22, 28, 30, 36, 40, 42, 46, 52, 58, 60, ...}.

Covering-system convention. We use the canonical Erdős–Graham 1980
convention [ErGr80], which is also the convention adopted by
erdosproblems.com #273 and by DeepMind's formal-conjectures
formalization (FormalConjectures/ErdosProblems/273.lean,
December 2025): a covering system is a finite family
{ (a_i, m_i) }_{i=1..k} of congruence classes with EACH m_i > 1 and
with the moduli DISTINCT (the "strict" or "incongruent" notion).
This is what the formalization's `StrictCoveringSystem` type
captures, via an `injective_moduli` hypothesis.

Without the distinctness requirement the problem is trivial: 4 in M
(since 5 is prime), so { 0, 1, 2, 3 } (mod 4) is a strict covering by
mod-4 progressions if we are allowed to use the same modulus four
times. The "strict" convention is what makes #273 open and serious.

The bounded-L SAT instance. Fix a period L. Covering Z by
progressions whose moduli all divide L is equivalent to covering
Z/LZ by those progressions: if every residue mod L is covered, then
since each progression is L-periodic (when m | L), every integer is
covered. So:

    Choose a subset S of pairs (a, m) with m in M, m | L, 0 <= a < m,
    subject to:
        (Cover)    for every i in [0, L) some (a, m) in S has
                    i ≡ a (mod m);
        (Strict)   for every m in M with m | L, at most one a
                    appears as (a, m) in S.

CNF encoding.

    Variables. x_{(a, m)} for each pair (a, m) with m | L, m in M,
        0 <= a < m. The number of variables is sum_{m | L, m in M} m.

    Cover clauses. For each residue i in [0, L), the at-least-one
        clause OR_{(a, m) : i ≡ a (mod m)} x_{(a, m)}. (L clauses.)

    Strict (at-most-one) clauses. For each m in M with m | L, an AMO
        constraint on { x_{(a, m)} : 0 <= a < m }. Pairwise encoding
        for small m (m <= 64); sequential-counter encoding for larger
        m (so the formula stays O((sum m) + L) in size).

Density lower bound (counting argument). If S is any strict covering
modulo L using moduli in M ∩ div(L), the union of the chosen
progressions covers density at most sum_{(a, m) in S} 1/m. Since the
moduli are distinct,
    density(union) <= sum_{m in M, m | L} 1/m =: D(L).
If D(L) < 1, the bounded-L problem has NO solution — independent of
the SAT search. This gives a one-line constant-time proof of UNSAT
that holds wherever the SAT solver would also (eventually) prove
UNSAT. For all canonical L's <= 27720, D(L) < 1, so the SAT solver's
job at these sizes is purely confirmatory.

Implication of verdicts.

    SAT at L. There exists a strict covering of Z by progressions
        whose moduli lie in M and all divide L. The extracted set
        settles Erdős #273 AFFIRMATIVELY, with an explicit
        construction.

    UNSAT at L (either by density or by SAT search). No strict
        covering of Z by progressions in M with all moduli distinct
        AND all moduli dividing L exists. Hence any hypothetical
        Erdős #273 covering must use a modulus m in M with m not
        dividing L; equivalently, the LCM of the (distinct) moduli of
        any such covering does not divide L. This strengthens the
        numerical lower bound on the LCM of any Erdős #273 covering.

Usage.

    python sat_covering.py L [--solver cadical] [--no-min]
                              [--timeout SECONDS] [--no-sat]
    python sat_covering.py --batch                 # canonical L's

The solver is invoked as a subprocess (DIMACS-on-disk, output to stdout),
with a hard wall-clock timeout enforced via subprocess.timeout. Default
is `cadical`; `kissat` is also supported and typically stronger on hard
UNSAT instances. Both are available on macOS via Homebrew.

Indexing convention. Residues use 0-based indexing throughout
(0 <= a < m, 0 <= i < L).
"""

from __future__ import annotations

import argparse
import itertools
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Iterable

from sympy import divisors, isprime

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool


# ---------------------------------------------------------------------------
# Modulus set M = {p - 1 : p prime, p >= 5}.
# ---------------------------------------------------------------------------

def is_in_M(m: int) -> bool:
    """Return True iff m = p - 1 for some prime p >= 5, i.e. m >= 4 and
    m + 1 is prime."""
    return m >= 4 and isprime(m + 1)


def allowed_moduli(L: int) -> list[int]:
    """Return the sorted list of divisors of L that lie in M."""
    return sorted(d for d in divisors(L) if is_in_M(d))


def density_sum(mods: Iterable[int]) -> float:
    """Return sum_{m in mods} 1/m. Upper bound on the fraction of Z/LZ
    coverable by a STRICT covering using these moduli (each used at most
    once), since each progression with modulus m covers exactly density
    1/m."""
    return sum(1.0 / m for m in mods)


# ---------------------------------------------------------------------------
# CNF construction.
# ---------------------------------------------------------------------------

_PAIRWISE_AMO_THRESHOLD = 64
"""Use pairwise AMO encoding (C(m, 2) binary clauses) up to this group
size; switch to pysat's `ladder` atmost-1 encoding above (O(m) clauses
+ O(m) aux variables instead of O(m^2), and ~300x faster to construct
than the `seqcounter` encoder at m ~ 10^5). Keeps the formula
construction tractable at L = 360360 and L = 720720."""


def build_cnf(L: int, mods: list[int]) -> tuple[CNF, IDPool, list[tuple[int, int]]]:
    """Build the strict-covering CNF instance for the bounded-L question.

    Returns (cnf, pool, pairs) where:
      cnf:   pysat CNF object (cover clauses then at-most-one clauses);
      pool:  IDPool with the (a, m) -> variable-id map, plus any
             auxiliary vars introduced by the AMO encoding;
      pairs: the canonical list of (a, m) pairs, in iteration order.
    """
    pool = IDPool()
    pairs: list[tuple[int, int]] = []
    by_modulus: dict[int, list[int]] = {m: [] for m in mods}
    cover_clauses: list[list[int]] = [[] for _ in range(L)]

    for m in mods:
        for a in range(m):
            vid = pool.id(("x", a, m))
            pairs.append((a, m))
            by_modulus[m].append(vid)
            # Progression a (mod m) restricted to [0, L) hits residues
            # i with i ≡ a (mod m). When m | L, these are exactly the
            # arithmetic-progression points a, a+m, a+2m, ..., a+(L/m-1)m.
            for i in range(a, L, m):
                cover_clauses[i].append(vid)

    cnf = CNF()
    # Cover (at-least-one per residue). An empty clause => UNSAT.
    for clause in cover_clauses:
        cnf.append(clause)
    # At-most-one per modulus (strictness).
    for m in mods:
        vids = by_modulus[m]
        if len(vids) <= _PAIRWISE_AMO_THRESHOLD:
            for v1, v2 in itertools.combinations(vids, 2):
                cnf.append([-v1, -v2])
        else:
            amo = CardEnc.atmost(
                lits=vids, bound=1, vpool=pool, encoding=EncType.ladder
            )
            cnf.extend(amo.clauses)

    return cnf, pool, pairs


def decode_model(model: Iterable[int], pool: IDPool, pairs: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """Extract the chosen (a, m) pairs from a SAT model."""
    true_vars = {abs(v) for v in model if v > 0}
    return [(a, m) for (a, m) in pairs if pool.id(("x", a, m)) in true_vars]


def verify_strict_covering(L: int, chosen: list[tuple[int, int]]) -> tuple[bool, str]:
    """Verify that (1) the moduli in `chosen` are pairwise distinct, and
    (2) every residue in [0, L) is covered by at least one (a, m) in
    chosen. Returns (ok, reason)."""
    moduli = [m for (_, m) in chosen]
    if len(moduli) != len(set(moduli)):
        seen: dict[int, int] = {}
        for m in moduli:
            seen[m] = seen.get(m, 0) + 1
        dups = sorted(m for m, c in seen.items() if c > 1)
        return False, f"non-distinct moduli: {dups}"

    covered = [False] * L
    for (a, m) in chosen:
        for i in range(a % m, L, m):
            covered[i] = True
    if not all(covered):
        uncovered = [i for i in range(L) if not covered[i]]
        return False, f"uncovered residues: {uncovered[:10]}..."
    return True, "ok"


# ---------------------------------------------------------------------------
# Solver wrapper with wall-clock timeout via subprocess.
# ---------------------------------------------------------------------------
# We shell out to the standalone `cadical` binary (or another DIMACS-
# compatible solver) via subprocess so that wall-clock timeouts can be
# enforced reliably via subprocess.timeout — pysat's in-process
# interrupt API is not reliable on hard UNSAT instances since the
# interrupt is only polled at solver decision points.

def write_dimacs(cnf_clauses: list[list[int]], n_vars: int, path: Path) -> None:
    """Write a CNF to DIMACS format at `path`.

    Optimized for large instances: we batch-join clause strings into a
    big chunk and `write()` once per chunk, since per-line `f.write`
    has high Python overhead at 10^6+ clauses.
    """
    with open(path, "w") as f:
        f.write(f"p cnf {n_vars} {len(cnf_clauses)}\n")
        # Batch up to ~50k clauses per write call.
        BATCH = 50_000
        parts: list[str] = []
        for i, clause in enumerate(cnf_clauses):
            parts.append(" ".join(map(str, clause)))
            parts.append(" 0\n")
            if (i + 1) % BATCH == 0:
                f.write("".join(parts))
                parts.clear()
        if parts:
            f.write("".join(parts))


def parse_dimacs_solution(stdout: str) -> tuple[str, list[int] | None]:
    """Parse a DIMACS-style solver output.

    Returns (verdict, model). Verdict is "SAT", "UNSAT", or "TIMEOUT".
    """
    lines = stdout.splitlines()
    verdict = "TIMEOUT"
    model: list[int] = []
    for line in lines:
        if line.startswith("s "):
            tag = line[2:].strip()
            if tag == "SATISFIABLE":
                verdict = "SAT"
            elif tag == "UNSATISFIABLE":
                verdict = "UNSAT"
            elif tag == "UNKNOWN":
                verdict = "TIMEOUT"
        elif line.startswith("v "):
            model.extend(int(t) for t in line[2:].split() if t)
    if verdict == "SAT":
        # Drop the trailing 0 sentinel.
        model = [v for v in model if v != 0]
        return verdict, model
    return verdict, None


def solve_with_timeout(
    n_vars: int,
    clauses: list[list[int]],
    timeout_s: float,
    solver_bin: str = "cadical",
    extra_args: list[str] | None = None,
) -> tuple[str, list[int] | None, float]:
    """Run the SAT solver in a subprocess with a hard wall-clock timeout.

    The CNF is written to a temporary DIMACS file; `solver_bin` is
    invoked with that file as its argument. The subprocess is killed
    after `timeout_s` seconds.

    Returns (verdict, model_or_None, runtime). Verdict is "SAT",
    "UNSAT", or "TIMEOUT".
    """
    if extra_args is None:
        # Defaults per solver. -q for cadical suppresses the noisy
        # progress comments (we only need the "s ..." and "v ..." lines).
        if "cadical" in solver_bin:
            extra_args = ["-q"]
        else:
            extra_args = []
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".cnf", delete=False
    ) as tf:
        cnf_path = Path(tf.name)
    try:
        write_dimacs(clauses, n_vars, cnf_path)
        cmd = [solver_bin, *extra_args, str(cnf_path)]
        t0 = time.perf_counter()
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_s,
                check=False,
            )
            runtime = time.perf_counter() - t0
            # cadical's exit code: 10 = SAT, 20 = UNSAT, 0 / other = unknown.
            verdict, model = parse_dimacs_solution(proc.stdout)
            return verdict, model, runtime
        except subprocess.TimeoutExpired:
            runtime = time.perf_counter() - t0
            return "TIMEOUT", None, runtime
    finally:
        try:
            cnf_path.unlink()
        except FileNotFoundError:
            pass


# ---------------------------------------------------------------------------
# Min-covering search (only when SAT and requested).
# ---------------------------------------------------------------------------

def find_min_covering(
    L: int,
    mods: list[int],
    solver_bin: str,
    upper_bound: int,
    timeout_s: float,
) -> tuple[int, list[tuple[int, int]]] | None:
    """Top-down linear search for the minimum strict-covering size at L.

    Each iteration adds a cardinality bound sum_{(a, m)} x_{(a, m)} <= k
    to the base CNF and asks the SAT solver for any solution. If SAT,
    k_curr := |solution| < k (the solver may return a strictly smaller
    covering than the bound permits); recurse with k = k_curr - 1. If
    UNSAT, the previous k_curr is the minimum. TIMEOUT returns the
    best-so-far without a min certificate.

    Returns (k_min, covering). k_min is the verified minimum if the
    final call returned UNSAT, else the smallest SAT solution found
    within the timeout.
    """
    best_k: int | None = None
    best_chosen: list[tuple[int, int]] = []

    k = upper_bound
    while k >= 1:
        cnf, pool, pairs = build_cnf(L, mods)
        all_vars = [pool.id(("x", a, m)) for (a, m) in pairs]
        card = CardEnc.atmost(
            lits=all_vars, bound=k, vpool=pool, encoding=EncType.seqcounter
        )
        cnf.extend(card.clauses)
        verdict, model, _ = solve_with_timeout(
            pool.top, cnf.clauses, timeout_s, solver_bin=solver_bin
        )
        if verdict == "SAT":
            chosen = decode_model(model or [], pool, pairs)
            best_k = len(chosen)
            best_chosen = chosen
            k = best_k - 1
        else:
            # UNSAT confirms best_k as the minimum; TIMEOUT means best-so-far.
            break

    return (best_k, best_chosen) if best_k is not None else None


# ---------------------------------------------------------------------------
# Driver.
# ---------------------------------------------------------------------------

def solve_one(
    L: int,
    solver_bin: str = "cadical",
    do_min: bool = True,
    timeout_s: float = 60.0,
    run_sat: bool = True,
    verbose: bool = True,
) -> dict:
    """Run the full pipeline at L. Returns a structured dict of results.

    Parameters
    ----------
    L : period to test.
    solver_bin : standalone SAT-solver binary on $PATH (default cadical).
    do_min : if SAT, search for the minimum-size strict covering.
    timeout_s : wall-clock timeout for each SAT-solver call (seconds).
    run_sat : if False, skip the SAT call and report only the density verdict.
    verbose : human-readable progress to stdout.
    """
    t0 = time.perf_counter()
    mods = allowed_moduli(L)
    dens = density_sum(mods)

    if verbose:
        print(f"L = {L}")
        print(f"  allowed moduli (m in M with m | L, where M = {{p-1 : p prime, p>=5}}):")
        print(f"    {mods}")
        print(f"    ({len(mods)} moduli)")
        print(f"  density-bound D(L) = sum_{{m | L, m in M}} 1/m = {dens:.6f}")
        if dens < 1:
            print(f"    --> D(L) < 1 ==> NO strict covering exists at this L.")
            print(f"        (Counting proof: each modulus contributes density 1/m,")
            print(f"         and the moduli are distinct, so total density <= D(L) < 1.)")
        else:
            print(f"    --> D(L) >= 1: counting bound does not rule out SAT.")

    cnf, pool, pairs = build_cnf(L, mods)
    n_vars_intern = len(pairs)  # only the x_{(a,m)} vars; AMO aux not counted here
    n_vars_total = pool.top
    n_clauses = len(cnf.clauses)
    n_cover_clauses = L
    n_amo_clauses = n_clauses - L
    if verbose:
        print(f"  variables: {n_vars_intern} (x_{{(a,m)}}) + {n_vars_total - n_vars_intern} (AMO aux) = {n_vars_total}")
        print(f"  clauses:   {n_clauses}")
        print(f"    cover:        {n_cover_clauses}")
        print(f"    at-most-one:  {n_amo_clauses}")

    # Detect empty cover clauses (residue with no candidate progression).
    # When mods is non-empty, this only happens if no m in mods divides
    # the residue + 0; but actually when m | L for all m in mods, every
    # residue i in [0, L) has i mod m well-defined, so there's at least
    # the (i mod m, m) candidate per modulus. So empty clauses only
    # appear when mods is empty.
    empty_cover_clauses = [i for i in range(L) if len(cnf.clauses[i]) == 0]
    if empty_cover_clauses and verbose:
        print(f"  NOTE: {len(empty_cover_clauses)} residues have no candidate progression")
        print(f"        (e.g., i = {empty_cover_clauses[:5]}); instance is trivially UNSAT.")

    # ----- SAT call -----------------------------------------------------------
    verdict_sat = "SKIPPED"
    runtime_sat = 0.0
    chosen: list[tuple[int, int]] = []
    if run_sat:
        if verbose:
            print(f"  calling {solver_bin} (wall-clock timeout: {timeout_s:.1f}s)...")
        verdict_sat, model, runtime_sat = solve_with_timeout(
            pool.top, cnf.clauses, timeout_s, solver_bin=solver_bin
        )
        if verdict_sat == "SAT":
            chosen = decode_model(model or [], pool, pairs)
            ok, reason = verify_strict_covering(L, chosen)
            assert ok, f"SAT solver returned an invalid covering: {reason}"
        if verbose:
            print(f"  SAT-solver runtime: {runtime_sat:.4f} s")
            print(f"  SAT-solver verdict: {verdict_sat}")

    # ----- Reconcile verdicts -------------------------------------------------
    # Final verdict logic:
    #   - If SAT returned SAT, it's a proof of existence (we verified above).
    #   - If SAT returned UNSAT, it's a proof of non-existence.
    #   - If density < 1, UNSAT by counting (independent of SAT result).
    #   - If SAT TIMEOUT and density >= 1, the answer is INDETERMINATE.
    if verdict_sat == "SAT":
        final_verdict = "SAT"
        proof_source = "SAT-solver"
    elif verdict_sat == "UNSAT":
        final_verdict = "UNSAT"
        proof_source = "SAT-solver"
    elif dens < 1:
        final_verdict = "UNSAT"
        proof_source = "density-bound"
    elif verdict_sat == "SKIPPED" and dens < 1:
        final_verdict = "UNSAT"
        proof_source = "density-bound"
    else:
        final_verdict = "INDETERMINATE"
        proof_source = "(none: SAT timed out and D(L) >= 1)"

    if verbose:
        print()
        print(f"  FINAL VERDICT: {final_verdict}  (proof source: {proof_source})")
        if final_verdict == "SAT":
            print()
            print(f"  Strict covering found, size = {len(chosen)}.")
            print(f"  Moduli used: {sorted(set(m for (_, m) in chosen))}")
            print(f"  IMPLICATION FOR ERDŐS #273:")
            print(f"    There exists a strict covering of Z by congruence classes")
            print(f"    whose moduli all lie in M and all divide L = {L}.")
            print(f"    This is an explicit construction that SETTLES Erdős #273")
            print(f"    AFFIRMATIVELY. The next session formalizes it in Lean as")
            print(f"    a StrictCoveringSystem.")
        elif final_verdict == "UNSAT":
            print()
            print(f"  IMPLICATION FOR ERDŐS #273:")
            print(f"    No strict covering of Z by progressions whose moduli lie")
            print(f"    in M and all divide L = {L} exists. Therefore any")
            print(f"    Erdős #273 covering must use a modulus m in M with")
            print(f"    m NOT dividing {L}; equivalently, the LCM of the moduli")
            print(f"    of any such covering does not divide {L}. This is a")
            print(f"    numerical lower bound on the LCM of any Erdős #273")
            print(f"    covering.")
        else:
            print()
            print(f"  IMPLICATION: at L = {L}, the SAT search did not finish within")
            print(f"    the {timeout_s:.0f}-second timeout and the counting bound is")
            print(f"    insufficient (D(L) = {dens:.4f} >= 1). Retry with --timeout")
            print(f"    larger or use a different solver to settle.")

    # ----- Minimum-size search (only if SAT) ---------------------------------
    min_size: int | None = None
    min_chosen: list[tuple[int, int]] = []
    runtime_min = 0.0
    if final_verdict == "SAT" and do_min:
        if verbose:
            print()
            print(f"  searching for the minimum strict-covering size...")
        t_min0 = time.perf_counter()
        result = find_min_covering(
            L, mods, solver_bin, upper_bound=len(chosen), timeout_s=timeout_s
        )
        runtime_min = time.perf_counter() - t_min0
        if result is not None:
            min_size, min_chosen = result
            ok, reason = verify_strict_covering(L, min_chosen)
            assert ok, f"min-search returned an invalid covering: {reason}"
            if verbose:
                print(f"  minimum strict-covering size: {min_size}")
                print(f"  min-search runtime (cumulative): {runtime_min:.4f} s")
                print(f"  minimum covering (a, m), sorted by modulus:")
                for (a, m) in sorted(min_chosen, key=lambda p: (p[1], p[0])):
                    print(f"    ({a}, {m})")

    total_runtime = time.perf_counter() - t0
    if verbose:
        print(f"  total wall-clock: {total_runtime:.4f} s")

    return {
        "L": L,
        "moduli": mods,
        "density_sum": dens,
        "n_vars": n_vars_intern,
        "n_vars_total": n_vars_total,
        "n_clauses": n_clauses,
        "n_cover_clauses": n_cover_clauses,
        "n_amo_clauses": n_amo_clauses,
        "verdict_sat": verdict_sat,
        "final_verdict": final_verdict,
        "proof_source": proof_source,
        "covering": min_chosen if (do_min and min_size is not None) else chosen,
        "covering_size": min_size if (do_min and min_size is not None) else len(chosen),
        "min_size": min_size if do_min else None,
        "runtime_sat": runtime_sat,
        "runtime_min": runtime_min,
        "runtime_total": total_runtime,
    }


CANONICAL_LS = [60, 120, 360, 840, 2520, 27720, 360360, 720720]


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("L", nargs="?", type=int, help="period L (omit with --batch)")
    ap.add_argument("--solver", default="cadical",
                    help="standalone SAT-solver binary on $PATH (default: cadical)")
    ap.add_argument("--no-min", action="store_true",
                    help="skip the minimum-size search even on SAT")
    ap.add_argument("--no-sat", action="store_true",
                    help="skip the SAT-solver call; rely solely on the density bound")
    ap.add_argument("--timeout", type=float, default=60.0,
                    help="wall-clock SAT-solver timeout in seconds (default: 60.0)")
    ap.add_argument("--batch", action="store_true",
                    help="run the canonical L's")
    args = ap.parse_args()

    if args.batch:
        results = []
        for L in CANONICAL_LS:
            print("=" * 72)
            r = solve_one(
                L,
                solver_bin=args.solver,
                do_min=not args.no_min,
                timeout_s=args.timeout,
                run_sat=not args.no_sat,
            )
            results.append(r)
            print()
        # Summary table.
        print("=" * 72)
        print("SUMMARY TABLE")
        print("=" * 72)
        print(
            f"{'L':>10}  {'#mods':>6}  {'D(L)':>9}  {'#vars':>8}  {'#cls':>10}  "
            f"{'SAT':>9}  {'FINAL':>14}  {'min':>5}  {'t_sat':>10}  {'t_min':>10}"
        )
        for r in results:
            min_s = f"{r['min_size']}" if r['min_size'] is not None else "-"
            print(
                f"{r['L']:>10}  {len(r['moduli']):>6}  {r['density_sum']:>9.4f}  "
                f"{r['n_vars']:>8}  {r['n_clauses']:>10}  "
                f"{r['verdict_sat']:>9}  {r['final_verdict']:>14}  {min_s:>5}  "
                f"{r['runtime_sat']:>10.4f}  {r['runtime_min']:>10.4f}"
            )
        return 0

    if args.L is None:
        ap.print_help()
        return 1
    solve_one(
        args.L,
        solver_bin=args.solver,
        do_min=not args.no_min,
        timeout_s=args.timeout,
        run_sat=not args.no_sat,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
