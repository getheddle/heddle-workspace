# Output contracts — schemas

Draft v0.8 (2026-06-11) · part of the `hooman-assistant` skill · load when writing a brief or producing/validating feedback.

A brief names exactly one contract (brief.2). The feedback file copies that contract's skeleton verbatim — wrappers, tags, and mandatory lines included. The structure is load-bearing: it is what makes feedback validatable on receipt and sweepable later. Sections that are empty stay present, marked `none` — absence is a signal, never an omission.

## C-R — Reconnaissance (read-only investigation)

```markdown
# <brief-name> — feedback
contract: C-R
implemented: nothing

<decisions>
- D1: <decision needing human input> — <options> — <recommended option + one-line why>
</decisions>

<evidence_map coverage="inspected=N inferred=N unverified=N">
- [inspected]  <file/source actually read> — <claim it supports>
- [inferred]   <adjacent evidence reasoned from> — <claim>
- [unverified] <assumption, not checked> — <claim>
</evidence_map>

<recommendation>
<the recommended path, opening with its first concrete step>
</recommendation>

<rejected>
- <path not recommended> — <one-line reason>
</rejected>

<not_done>
<what would NOT be done without explicit go-ahead>
</not_done>
```

C-R rules:
- `implemented: nothing` is literal and mandatory; its absence fails validation.
- Every material claim in the body appears in the evidence map. An untagged claim is treated as `[unverified]`.
- The `coverage` counts must match the entries. They exist so under-inspection is visible at a glance, before the plan's prose can charm anyone.

## C-M — Mutation (implementation)

```markdown
# <brief-name> — feedback
contract: C-M
scope: <the locked-scope brief this executes>

<files_changed>
- <path> — <what changed and why, one line>
</files_changed>

<tests>
- <command run> — <pass/fail, with numbers>
</tests>

<risks>
- <residual risk> — <severity>
</risks>

<manual_checks>
- <what a human must still verify>
</manual_checks>

<rollback>
<how to undo; name the exact mechanism>
</rollback>
```

C-M rules:
- All diffs were shown before write (role.5). If any were not, say so in the first line, before anything else.
- `<tests>` reports what actually ran, not what should run; "not run" is a valid, honest entry.

## C-A — Analysis (research, drafting, non-code synthesis)

```markdown
# <brief-name> — feedback
contract: C-A

<sources>
- [primary|secondary|speculative] <source> — <what it supports>
</sources>

<opposing>
<the strongest case AGAINST the recommendation>
</opposing>

<implications>
<what this means for the decision at hand>
</implications>

<uncertainty>
- <claim> — <confidence, and what would resolve it>
</uncertainty>
```

C-A rules:
- `<opposing>` is mandatory and is never `none` without the search effort stated. Supporting-case-only analysis fails validation.
- Source quality tags are assigned by the source's nature, not by whether it agrees with the recommendation.

## Validation — Chat side, on receipt

A feedback file is incomplete when any of these hold: a mandatory section of its named contract is missing · the evidence map is absent or its coverage counts mismatch the entries (C-R) · `implemented: nothing` is absent (C-R) · `<opposing>` is absent (C-A). Incomplete → bounce with the missing section names. Do not review content before structure passes — structure is cheap to check and its absence predicts the expensive failures.
