# Erdős Problem #273 — covering systems with moduli $p - 1$, $p \geq 5$ prime

> Is there a covering system of the integers all of whose moduli are of the form $p - 1$ for some prime $p \geq 5$?

Autonomous Lean 4 proof attempt against
[Mathlib](https://github.com/leanprover-community/mathlib4),
driven by the [formalia](https://github.com/ikaric/formalia)
harness. The Lean kernel is the trust root: every claim tagged
`[verified]` compiles under `lake build` with `#print axioms`
reporting only the three foundational axioms.

## Problem

A *covering system* of the integers is a finite collection of
arithmetic progressions
$\{ a_i \pmod{m_i} \}_{i=1}^{k}$ with moduli $m_i \geq 2$
whose union is $\mathbb{Z}$, i.e. every integer lies in at least one
progression. Erdős (1950), in Problem #273 of the Erdős–Graham
survey *Old and new problems and results in combinatorial number
theory* (L'Enseignement Mathématique 28, 1980, p.24), asks:

> Does there exist a covering system $\{ a_i \pmod{m_i} \}$ such
> that each modulus $m_i$ has the form $m_i = p_i - 1$ for some
> prime $p_i \geq 5$?

Selfridge observed that allowing $p = 3$ admits a covering system
using divisors of $360 = \operatorname{lcm}(2,3,4,5,6,8,9,10,12)$
(all of which are of the form $p - 1$ for $p \in \{3, 5, 7\}$), but
the 360-construction crucially uses the modulus $2 = 3 - 1$.
Forbidding $p = 3$ eliminates the modulus 2 and changes the problem.
The allowed moduli are therefore
$\mathcal{M} = \{ p - 1 : p \text{ prime}, p \geq 5 \} = \{4, 6, 10, 12, 16, 18, 22, 28, 30, 36, 40, 42, 46, 52, 58, 60, \ldots\}$.
The question is whether $\mathbb{Z}$ admits a finite covering using
only progressions with moduli drawn from $\mathcal{M}$. The problem
is open as of 2026; no partial result on the smallest required
modulus, on the number of progressions, or on the least common
multiple of any putative covering appears in the published
literature.

## Status

<!-- BEGIN STATUS -->
- **Last session**: `2026-05-28`
- **Roadmap**: [#1](../../issues/1) — sub-lemma checklist with progress meter (3 / 6 closed)
- **Verified results**: 2 headline theorems (density bound + numerical $L = 27720$), 17 `#print axioms`-clean Lean theorems total
- **Current focus**: V5 range extension; librarian sweep of Hough/BBMST auxiliary results applicable to $\mathcal{M}$
- **Manuscript**: [`proof.pdf`](manuscript/proof.pdf) — rebuilt every session
<!-- END STATUS -->

## What's verified

<!-- BEGIN VERIFIED -->
| Theorem | Lean file | Axiom check |
|---|---|---|
| Strict-covering density bound (Theorem 4) | [`formal/Erdos273/CoveringSystem.lean`](formal/Erdos273/CoveringSystem.lean) | clean |
| Abstract density obstruction (Corollary 5) | [`formal/Erdos273/CoveringSystem.lean`](formal/Erdos273/CoveringSystem.lean) | clean |
| $D(27720) = 953/990 < 1$ (Lemma 7) | [`formal/Erdos273/NumericalBound27720.lean`](formal/Erdos273/NumericalBound27720.lean) | clean |
| No strict admissible cover with moduli dividing 27720 (Theorem 8) | [`formal/Erdos273/NumericalBound27720.lean`](formal/Erdos273/NumericalBound27720.lean) | clean |

See [`proof.pdf`](manuscript/proof.pdf) and [Appendix A: Formal verification](manuscript/proof.pdf) for the full list (17 axiom-clean theorems).
<!-- END VERIFIED -->

## What's open

<!-- BEGIN OPEN -->
| Obligation | Status | Issue |
|---|---|---|
| V2: Distortion-method non-existence (BBMS 2022, $p-1$ specialization) | open | [#4](../../issues/4) |
| V3: Hough-style minimum-modulus argument adapted to $p-1$ | open | [#5](../../issues/5) |
| V5: Computational range extension — minimal coverings via $\mathcal{M} \cap [4, L]$ | open | [#7](../../issues/7) |

See the [ROADMAP issue](../../issues/1) for the live sub-lemma
checklist with progress meter.
<!-- END OPEN -->

## Repository tour

- [`manuscript/proof.tex`](manuscript/proof.tex) /
  [`proof.pdf`](manuscript/proof.pdf) — the canonical evolving paper
- [`formal/Erdos273/`](formal/Erdos273/) — Lean 4
  theorems (`#print axioms` checked, no `sorry` outside
  `[sketch]`-tagged files)
- [`findings/`](findings/) — inter-agent notes, literature
  surveys, reviewer reports, dead ends, strategic pivots
- [`STATUS.md`](STATUS.md) — brief pointer to the last session
  and current focus
- [ROADMAP](../../issues/1) — live work-queue dashboard with
  checkbox progress meter

## Harness

This clone runs the
[formalia](https://github.com/ikaric/formalia)
autonomous-proof harness: twelve specialist subagents under
`.claude/agents/`, three slash-commands (`/target`, `/solve`,
`/vector`) under `.claude/skills/`, a mandatory novelty gate
against Mathlib, and honest tagging
(`[verified]` / `[sketch]` / `[conditional on H]` /
`[numerical: range]` / `[heuristic]`).

The Status / Verified / Open blocks above are bounded by HTML
comment sentinels and are refreshed automatically at the end of
every `/solve` session — do not hand-edit between the markers.

## Setup requirements (beyond the harness defaults)

In addition to the harness's defaults (Lean via `elan`, Mathlib via
`lake exe cache get`, Python via `uv sync`, `tectonic`, `gh`), this
clone uses:

- **`cadical`** — DIMACS SAT solver used by `formal/numerics/sat_covering.py`
  for the bounded-period strict-covering search of Erdős #273.
  Install via `brew install cadical` (verified at 3.0.0).
- **`kissat`** — alternative DIMACS SAT solver, typically stronger
  than CaDiCaL on hard UNSAT instances. Used optionally with
  `--solver kissat` flag. Install via `brew install kissat`
  (verified at 4.0.4).

Both are invoked as subprocesses via `subprocess.run(..., timeout=…)`,
so wall-clock timeouts are deterministic. The Python `python-sat`
package (in `pyproject.toml`) handles CNF construction and AMO/
cardinality encodings; we shell out to the standalone binaries for
the SAT call itself.
