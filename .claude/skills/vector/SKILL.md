---
name: vector
description: Manage attack vectors for this formalia clone — add a new vector, retire a stuck one, or pivot the strategic posture by retiring several and seeding replacements. Interactive (uses AskUserQuestion). The user-driven complement to /solve's autonomous vector reasoning. Run between autonomous sessions when the strategic landscape shifts. Do not call from /solve.
---

You are the **vector** skill for an active `formalia` clone. Your job
is to manage the live attack-vector roster — the high-level strategic
posture of the project. `/solve` works *within* the current vectors;
`/vector` adjusts *which* vectors are live.

Three modes:
- **add** — seed a new vector mid-project.
- **retire** — close a stuck or superseded vector.
- **pivot** — retire several at once, write a strategic-rationale
  document, and seed replacements.

This skill **is** interactive (uses `AskUserQuestion`). Do **not**
call it from `/solve`.

# Pre-flight

Run in parallel:

```sh
grep -L "FORMALIA_TEMPLATE" manuscript/proof.tex     # template marker should be ABSENT
gh auth status 2>&1 | head -3                     # active account = ikaric
git remote -v                                     # remote sanity
git pull --rebase origin main                     # ensure up-to-date
```

If `FORMALIA_TEMPLATE` marker is **present**: this clone has not been
initialized. Refuse to run; tell the user to run `/target` first.

If the active gh account is not `ikaric`: `gh auth switch -u ikaric
&& gh auth setup-git`.

# Mode selection

First `AskUserQuestion`: pick the operation.

```
Question: "Which vector operation?"
Header: "Operation"
Options:
  - label: "Add a new vector"
    description: "Seed a fresh attack vector with name + statement + optional dependency."
  - label: "Retire a vector"
    description: "Close a stuck vector with a reason; moves to Retired list."
  - label: "Pivot strategy"
    description: "Retire several at once, write a rationale, seed replacements."
```

Branch on the answer.

# add branch

Ask a follow-up `AskUserQuestion` (free-text fields):

1. **Vector name** (3–6 words). Free-text.
2. **Vector statement** (one paragraph). Free-text.
3. **Dependency** (optional). Free-text — names another vector or
   sub-lemma this one builds on.

## Compute V<N>

Find the highest existing `vector-V<N>` label:

```sh
gh label list --limit 200 \
  | awk '/^vector-V[0-9]+/{gsub(/vector-V/,"",$1); print $1}' \
  | sort -n | tail -1
```

Increment by 1. Create the new label if it doesn't exist:

```sh
gh label create "vector-V<N+1>" --color FBCA04 --description "Attack vector V<N+1>"
```

## Open the per-vector issue

```sh
gh issue create \
  --title "V<N>: <vector name>" \
  --label "open,vector,vector-V<N>" \
  --body "<vector statement>

Dependency: <if any>.

Seeded by /vector on <YYYY-MM-DD>."
```

Record the issue number returned by `gh issue create`.

## Update the ROADMAP

Read the ROADMAP issue body. Add a new checkbox under the `## Attack
vectors` section:

```markdown
- [ ] #<issue-N> V<N>: <vector name>
```

`gh issue edit $ROADMAP --body "$(updated body)"`. Recompute the
`## Progress: N/M closed` line.

## Commit + push

```
vector: add V<N> — <vector name>

Issue #<N>; see ROADMAP issue for placement.
```

Push.

## Report

Output 2–3 sentences: the vector name, the new issue URL, the
ROADMAP URL.

# retire branch

List open `vector`-labelled issues:

```sh
gh issue list --label vector --state open --json number,title --limit 50
```

Ask `AskUserQuestion`:

1. **Which vector to retire?** Single-select; each option is one of
   the listed issues (`label: "V<N>: <name>"`, `description:
   "Issue #<N>"`).
2. **Reason for retirement** (free-text). Used to choose the
   secondary label.

## Heuristic label choice

If the reason text contains any of `blocked`, `impossible`, `dead
end`, `doesn't work`, `barrier`, `parity`, `dead-end`, label as
`deadend`. Otherwise label as `deprioritized`.

## Close the issue

```sh
gh issue close <N> --comment "Retired by /vector on <YYYY-MM-DD>.

Reason: <user-supplied reason>.

Retirement category: deadend | deprioritized."

gh issue edit <N> --remove-label open --add-label "<deadend|deprioritized>"
```

## Update the ROADMAP

Read the ROADMAP body. **Move** the matching `- [x] #<N> V<N>:
<name>` line from `## Attack vectors` to `## Retired vectors`,
appending the reason in parentheses:

```markdown
## Retired vectors

- [x] #<N> V<N>: <name> — <one-line reason> (retired YYYY-MM-DD)
```

(The checkbox is `[x]` because the issue is closed; GitHub auto-ticks
it via the tracked-in feature, but writing `[x]` explicitly avoids
drift if the auto-tick lags.) Recompute `## Progress`.

`gh issue edit $ROADMAP --body "$(updated body)"`.

## Commit + push

```
vector: retire V<N>

<one-line reason>. Issue #<N> closed.
```

Push.

## Report

Output 2–3 sentences.

# pivot branch

The strategic-pivot ceremony. Retires several vectors at once, names
the strategic rationale, and seeds replacements.

## Multi-select retire

List open vectors as before. Ask `AskUserQuestion` with
`multiSelect: true`:

1. **Which vectors to retire?** Multi-select from the open list.
2. **Strategic rationale** (one paragraph). Free-text. *Why* the
   pivot is happening (what changed about the landscape).

## Bulk close

For each selected vector issue:
- `gh issue close <N> --comment "Retired by /vector pivot on
  <YYYY-MM-DD>. See findings/pivot-<YYYY-MM-DD>.md for full
  rationale."`
- `gh issue edit <N> --remove-label open --add-label deprioritized`

(Pivot retirements default to `deprioritized` rather than `deadend`,
because the strategic rationale is the load-bearing context — not a
specific obstacle hit.)

## Add replacements (up to 3, prompted iteratively)

Loop up to 3 times. Each iteration:

1. Ask `AskUserQuestion`:
   - **Replacement vector name** (3–6 words). Free-text.
   - **Replacement statement** (one paragraph). Free-text.
   - **Add another?** Single-select: "Yes, add another" / "No, done".
2. Auto-increment V<N> per the add branch.
3. Open the new vector issue with labels `open + vector +
   vector-V<N>`. Body footer:
   `Seeded by /vector pivot on <YYYY-MM-DD>; see
   findings/pivot-<YYYY-MM-DD>.md for context.`
4. If user said "No, done", break.

## Write `findings/pivot-<YYYY-MM-DD>.md`

```markdown
# Strategic pivot — <YYYY-MM-DD>

## Rationale

<user-supplied rationale paragraph>

## Retired

- V<N1>: <name> (issue #<N1>)
- V<N2>: <name> (issue #<N2>)
- ...

## Replaced with

- V<M1>: <name> (issue #<M1>) — <one-line gist>
- V<M2>: <name> (issue #<M2>) — <one-line gist>
- ...

## Carried over

(vectors not touched by this pivot — list by V<N> for reference)
```

Append a one-line entry to `findings/INDEX.md`:

```markdown
- `pivot-<YYYY-MM-DD>.md` — strategic pivot: <one-line rationale gist>
```

## Update the ROADMAP

Rewrite the body in one pass:
- **Move** retired vectors from `## Attack vectors` to `## Retired
  vectors`, appending the retirement reason.
- **Append** replacements to `## Attack vectors`.
- Recompute `## Progress: N/M closed`.

`gh issue edit $ROADMAP --body "$(rewritten body)"`.

## Commit + push

A single commit captures the whole pivot:

```
pivot: <one-line strategic rationale summary>

Retired V<N1>, V<N2>, ...
Added V<M1>, V<M2>, ...
See findings/pivot-<YYYY-MM-DD>.md.
```

Push.

## Report

Output 3–4 sentences:
- The rationale gist.
- How many retired vs added.
- ROADMAP URL + findings file path.

# Cross-cutting

## Always

- `git pull --rebase origin main` before any edits.
- Push after every commit so the user can see the result on GitHub
  immediately.
- The repo-local git config (`Ilhan Karić <ilhan.karic@gmail.com>`,
  set by `make init`) is correct; do not change it.
- Never include `Co-Authored-By: Claude` trailers, `Generated with
  Claude Code` footers, or any mention of the agent runtime in commit
  messages.

## Sub-agents

`/vector` does not dispatch sub-agents. It is a thin orchestration
skill — read user input, update issues + ROADMAP + findings, commit,
push, report. Sub-agent work belongs to `/solve`.

## Output to user

End with a 2–4-sentence report containing the new/closed issue URLs
and (for `pivot`) the findings file path. Then stop.
