---
name: polish
description: Final-pass review of the per-clone manuscript once the target is reached. Audits the .tex against publication standards (abstract written, scaffolding removed, every theorem has a proof block plus a footnote linking to its Lean file, references complete), adds or refines the "Formal verification" appendix with verbatim Lean snippets for the headline theorems, runs critic adversarially over the polished draft, rebuilds the PDF with tectonic, and commits. Designed to run after the ROADMAP shows N/N closed and `/loop /solve` has halted; can also be invoked mid-project for a partial polish on what's verified so far. Mostly autonomous (no AskUserQuestion); produces one commit `polish: final manuscript pass for <DisplayName>` plus a refreshed `proof.pdf`.
---

You are the **polish** skill. The verify-cycle work is done (or
mostly done); your job is to turn the evolving working manuscript
into something a referee would read as a finished paper.

The harness's day-to-day work optimises for *machine-checkability*:
every claim has its tag, every verified theorem has its Lean file,
every sub-lemma has its issue. That discipline is what makes the
results trustworthy. It is also what makes the manuscript read like
a project log if you stop there. `polish` is the final pass that
removes the project-log smell and leaves a paper.

# Pre-flight

Run in parallel:

```sh
grep -L "FORMALIA_TEMPLATE" manuscript/proof.tex     # template marker should be ABSENT
gh auth status 2>&1 | head -3                        # active account sanity
git remote -v                                        # remote sanity
git pull --rebase origin main                        # up-to-date
(cd formal && lake build) 2>&1 | tail -5             # everything still compiles
```

Refuse to run if:

- The `FORMALIA_TEMPLATE` marker is present → tell the user to run
  `/target` first.
- `make init` placeholders (`<GH_USERNAME>`, `<GIT_USER_NAME>`,
  `<GIT_USER_EMAIL>`) still appear in CLAUDE.md or README.md →
  tell the user to run `make init` first.
- `lake build` exits non-zero → fix the build first by re-running
  `/solve` or by manual repair; `polish` will not paper over
  broken Lean.

# Scope check: is anything verified?

```sh
VERIFIED=$(grep -cE '^% \[verified: formal/' manuscript/proof.tex)
SKETCHES=$(grep -cE '^% \[sketch\]|^% \[heuristic\]|^% \[conditional' manuscript/proof.tex)
ROADMAP_NUM=$(gh issue list --label roadmap --json number --jq '.[0].number')
BODY=$(gh issue view "$ROADMAP_NUM" --json body --jq '.body')
TOTAL=$(printf '%s\n' "$BODY" | grep -cE '^- \[[ x]\] #' || true)
CLOSED=$(printf '%s\n' "$BODY" | grep -cE '^- \[x\] #' || true)
echo "verified=$VERIFIED sketches=$SKETCHES roadmap=$CLOSED/$TOTAL"
```

Modes:

- **Full polish** — `CLOSED == TOTAL` (target reached). The
  manuscript should end this session looking like the
  preprint-ready arXiv version. All sections in scope.
- **Partial polish** — `CLOSED < TOTAL` but `VERIFIED > 0`. The
  user has asked for a polish of what's been verified so far
  (perhaps mid-project for an intermediate write-up). Same passes
  as full polish, but: leave `[sketch]` / `[conditional]` blocks
  in place (with their tags), and add a clear "Status of the
  proof" remark at the start of any section that contains
  unverified material.
- **Refuse** — `VERIFIED == 0`. There's nothing to polish; the
  manuscript is still scaffolding. Emit a one-line message
  ("polish: nothing verified yet — re-run after at least one
  `[verified]` promotion lands") and exit.

# Audit pass (read-only, builds the to-do list)

Before editing anything, build a `findings/polish-audit-<date>.md`
note listing what's wrong with the current manuscript. Each finding
is an entry like:

```
- [ ] [abstract] still says "to be written once the first verified
      result has landed" — replace with a real abstract summarising
      <main theorem>.
- [ ] [intro] §Introduction does not state the main theorem; only
      gestures at the problem. Add a one-paragraph summary of the
      result and the proof strategy.
- [ ] [thm 2.1] no footnote linking to formal/Ramsey33/UpperBound.lean.
- [ ] [thm 2.2] proof block is a `[sketch]` placeholder. Promote
      using the polished-proof template in CLAUDE.md § Manuscript
      style.
- [ ] [appendix] no "Formal verification" appendix; the verified
      theorems aren't catalogued for the reader.
- [ ] [bibliography] §References section is empty / only has
      `\bibitem` stubs.
- [ ] [scaffolding] grep found "Step 1" / "Critic review PASS" /
      "Initial attack vectors" — remove.
```

Audit checks to run:

1. **Abstract**: is it placeholder text? (`grep -iE "to be (written|filled)" manuscript/proof.tex`)
2. **Introduction**: does it state the main theorem? Does it cite the historical literature? Does it close with a roadmap of the paper?
3. **Theorem footnotes**: every `\begin{theorem}` or `\begin{lemma}` for a `[verified: …]` claim should have a footnote of the form `\footnote{Formally verified in \texttt{formal/<DisplayName>/<File>.lean}; Mathlib commit \texttt{<short SHA>}; \texttt{\#print axioms} lists only \texttt{propext}, \texttt{Classical.choice}, \texttt{Quot.sound}.}` on the statement.
4. **Proof blocks**: every theorem must have a `\begin{proof} … \end{proof}` block. Sketches with `\begin{sketch}` are *not* publication-acceptable; they must be expanded to full proofs (or, in partial-polish mode, left in place but explicitly flagged).
5. **Banned phrases / sections**: grep for the manuscript-style ban list (CLAUDE.md § "Banned from the manuscript") — `\section{Initial attack vectors}`, `\section{Roadmap}`, `\section{Revision history}`, `\section{Status}`, `\section{Current focus}`, `\section{Verified results}`, `\section{Sketches}`, `% [verified: …]` text inside theorem headers, "Step 1 / Step 2" labels in proofs, "Critic review PASS" remarks. None of these belong in a paper.
6. **Formal verification appendix**: does it exist? If yes, is it complete (one entry per verified theorem, with the Lean file path, the theorem name, the axiom-check status, and the Mathlib commit SHA)?
7. **References**: are all citations resolved? Are arXiv IDs / DOIs included? Run a quick grep for `[??]` style unresolved citations.
8. **Lean snippets**: do the headline theorems appear quoted (verbatim) in the appendix? Standard practice in modern formalisation papers (Mathlib paper, LTE paper, PFR paper) is to quote the Lean statement of the main result so the reader can see exactly what was proved.

# Polish pass (write the audit to-do list down)

For each audit item, dispatch the appropriate subagent or edit the
manuscript directly:

## Abstract

Rewrite to a real abstract. Three-to-five sentences. Convention:

> *We prove ⟨main theorem⟩. ⟨One-sentence proof strategy: e.g.,
> "The upper bound follows from a pigeonhole argument on the
> degrees of an arbitrary vertex in $K_6$; the lower bound is
> witnessed by the standard $C_5$-edge-colouring of $K_5$.">⟩ The
> entire proof is mechanically verified in Lean 4 against Mathlib
> ⟨commit ⟨short SHA⟩⟩; `#print axioms` on the headline theorem
> reports only `propext`, `Classical.choice`, and `Quot.sound`.*

If the result is conditional on a named open hypothesis, the
abstract must say so plainly.

## Introduction

Audit the existing intro. If it's a placeholder or paragraph-stub,
expand to four standard sections:

1. **The problem and its history** (one paragraph). The problem
   statement, who first asked it, the key historical milestones.
   Cite Greenwood–Gleason 1955, Erdős–Szekeres 1935, etc. via
   `\cite{}` keys that resolve to a bibliography entry.
2. **The result** (one paragraph). The headline theorem stated
   informally, with a forward reference to the formal statement
   (`Theorem~\ref{thm:main}`).
3. **Proof strategy** (one paragraph). A reader-friendly tour: "the
   upper bound by pigeonhole; the lower bound by the explicit
   $C_5/\overline{C_5}$ construction; the two are wired in
   Section~\ref{sec:main}". No formal symbols.
4. **Formalisation** (one paragraph). One paragraph on the
   machine-checked status: "All claims in this paper carry a
   machine-checkable verification status — `[verified]` claims
   are accompanied by a Lean 4 file whose `#print axioms` reports
   only the three foundational axioms. The complete formal
   development is in Appendix~\ref{sec:formal}."

If a `librarian` survey exists in `findings/lit-*.md`, mine it for
references. Dispatch `librarian` again only if the existing survey
is materially stale.

## Theorems: footnotes, proofs, banned text

For each `\begin{theorem}` / `\begin{lemma}` block:

- Add the footnote on the statement line (not the `\section` head)
  per the form above. Do not put `[verified: file.lean]` text in
  the visible theorem header — the verification status is carried
  by the comment above plus the footnote.
- If the proof block is `\begin{sketch}` or empty: promote to a
  proper proof following the manuscript-style policy in CLAUDE.md
  § Manuscript style → "Promotion: rewriting sketch → publication-style
  proof". Pull out auxiliary sub-claims as `\begin{lemma}` blocks
  with their own proofs. Use mathematical exposition, not "Step 1 /
  Step 2" labels.
- Strip any project-log remnants: "Critic review PASS",
  `\texttt{[verified: …]}` in headers, "Revision history" mentions,
  "Initial attack vectors" prose.

## Formal verification appendix

Append (or refine) an appendix:

```latex
\appendix
\section{Formal verification}
\label{sec:formal}

All numbered theorems in this paper are formally verified in Lean
4 against Mathlib. The complete development is at \texttt{formal/}
in the project repository; the Mathlib pin is \texttt{<commit>}
(see \texttt{formal/lake-manifest.json}).

\subsection*{Headline statements (Lean source)}

The main result, as it appears in
\texttt{formal/<DisplayName>/Main.lean}, is:

\begin{lstlisting}[language=Lean]
theorem ramsey_3_3 :
    R(3, 3) = 6 := by
  …
\end{lstlisting}

\subsection*{Axiom witness}

For each verified theorem, \texttt{\#print axioms} reports:

\begin{tabular}{lll}
\toprule
Theorem & File & Axioms \\
\midrule
\texttt{ramsey\_3\_3\_lower\_bound}
  & \texttt{formal/<DisplayName>/LowerBound.lean}
  & \texttt{propext, Classical.choice, Quot.sound} \\
\texttt{ramsey\_3\_3\_upper\_bound}
  & \texttt{formal/<DisplayName>/UpperBound.lean}
  & \texttt{propext, Classical.choice, Quot.sound} \\
\texttt{ramsey\_3\_3}
  & \texttt{formal/<DisplayName>/Main.lean}
  & \texttt{propext, Classical.choice, Quot.sound} \\
\bottomrule
\end{tabular}

\subsection*{Reproducing the verification}

\begin{enumerate}
\item Clone the repository at the tagged commit.
\item Run \texttt{(cd formal \&\& lake exe cache get \&\& lake build)}.
\item Inspect the axiom report with \texttt{\#print axioms} on
each theorem name listed above.
\end{enumerate}
```

The `lstlisting` package needs to be loaded in the preamble; if
it isn't, add `\usepackage{listings}` and a Lean-style
configuration. If your manuscript already uses a different
verbatim mechanism (`verbatim`, `minted`), match the existing
convention rather than introducing a new one.

For each `[verified: ...]`-tagged claim, **read the actual `.lean`
file and quote the *real* theorem statement** — do not
paraphrase. Run the Lean file through `lake env lean
<file.lean>` (or just `lake build`) once to confirm the
statement is current; out-of-date Lean snippets in a published
paper are worse than no snippet.

## References / bibliography

If the bibliography section is empty or has unresolved citations,
dispatch `librarian` with: "Resolve all `\cite{...}` keys in
`manuscript/proof.tex` — produce a complete `\bibitem` block (or
`.bib` entries) with arXiv IDs / DOIs / publication venue for
every citation." Then integrate.

## Banned text sweep

Final grep, before rebuilding:

```sh
grep -nE '\\section\{(Initial attack vectors|Roadmap|Plan|Revision history|Status|Current focus|Verified results|Sketches)\}|Critic review|\[verified: formal/' manuscript/proof.tex
```

Any hit indicates leftover scaffolding. Address each one before
the final commit.

# Critic adversarial pass on the polished draft

Dispatch `critic` with: "Read `manuscript/proof.tex` in its
current (polished) form. Adversarially review the *paper*, not
the Lean. Catch any statement that overclaims relative to the
Lean theorem behind it, any proof that smuggles in a hypothesis
not stated in the theorem, any abstract claim not actually
delivered in the body, any unresolved citation, any banned scaffolding
phrase. Output verdict PASS / REVISION REQUIRED / FAIL with a
findings/review-polish-<date>.md note."

If `REVISION REQUIRED`: address each finding before committing.

If `FAIL`: do not commit; produce a `findings/decision-polish-fail-<date>.md`
explaining what's blocking and suggesting whether the user should
re-run `/solve` to verify more material first.

# Build PDF + commit

```sh
(cd manuscript && tectonic -X compile proof.tex)
ls -la manuscript/proof.pdf
git add manuscript/proof.tex manuscript/proof.pdf findings/polish-*.md findings/review-polish-*.md findings/INDEX.md
git commit -m "polish: final manuscript pass for <DisplayName>

Audit findings recorded in findings/polish-audit-<date>.md.
Critic review: <PASS/REVISION applied>.
Manuscript style now matches CLAUDE.md § Manuscript style:
- Abstract expanded to a real summary
- Introduction restructured (problem / result / strategy / formalisation)
- Theorems carry the footnote pattern linking each to its Lean file
- Formal verification appendix added with verbatim Lean snippets
  and the axiom table
- Banned scaffolding (section bins, project-log phrases) removed
- References resolved (arXiv IDs / DOIs)

Built manuscript/proof.pdf with tectonic." && git push
```

Update `findings/INDEX.md` with the new `polish-audit-*.md` and
`review-polish-*.md` entries.

# Report back

End-of-skill output to the user (2–4 sentences): "Manuscript polished
for `<DisplayName>`. \<N\> theorems carry the formal-verification
footnote; the appendix lists \<M\> Lean files; critic verdict
\<PASS / X revisions applied\>. PDF rebuilt at `manuscript/proof.pdf`."

# What `/polish` does *not* do

- It does **not** open new attack vectors. If the audit finds gaps
  that would need new Lean work, it flags them and stops — opening
  vectors is `/vector add`'s job.
- It does **not** modify any `.lean` file. The verified theorems
  are the contract; polish reads them but does not edit them.
- It does **not** run `/solve` recursively. If unverified material
  exists, partial-polish is the right mode; the user re-runs
  `/solve` to verify, then re-runs `/polish`.
- It does **not** rewrite the manuscript from scratch. It iterates
  the existing one. The author voice and structure are preserved
  where they exist; polish fills gaps, fixes scaffolding, and
  adds the formal-verification appendix.

# Anti-patterns

- **Paraphrasing the Lean statement** in the appendix snippet
  instead of quoting it verbatim. The whole point of the snippet
  is reader-verifiable correspondence with the formal source.
- **Inventing citations.** Every `\cite{key}` must resolve to an
  actual paper (arXiv ID, DOI, or full publication metadata). If
  `librarian` can't find a real citation for a claim, weaken the
  claim or footnote it as "folklore".
- **Promoting a `[sketch]` to a verified-style proof** without an
  actual Lean theorem behind it. `polish` does not change tags;
  if a block is `[sketch]`, the polished version is still a
  sketch (clearly labelled in partial-polish mode), not a faked
  proof block.
- **Removing the manuscript's verification tags from the LaTeX
  comments.** The `% [verified: …]` / `% [sketch]` comments above
  each theorem are the machine-readable status; they stay even
  in the polished manuscript. They are invisible in the PDF and
  are how future sessions (and any future `polish` re-run) know
  the state.
