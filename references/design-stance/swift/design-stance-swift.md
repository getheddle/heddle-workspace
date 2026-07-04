# Design Stance — Swift (Swift-language projects)

> Layers on top of `design-stance-universal.md`. **Scope:** Swift-language projects only. **Binds:** Chat and the Executor. **Home:** `references/`. **v0.1 · 2026-06-01.**

## Forward, not backward

No legacy to serve. The optimization target is **forward-tuning**, not backward-compatibility. Consequences that *invert* the usual engineering defaults:

- **Raising a version floor to reach a cleaner construct is preferred** — not a regression to be minimized.
- **Maximal adoption of new language capabilities is a project goal.** When a newer capability does the job, preferring it is *aligned with purpose* — not gold-plating. Finding the best way to use the newest features, and using as much of them as is warranted, is part of why these projects exist.
- **Pitch- and experimental-stage features are acceptable load-bearing dependencies** (e.g. `@_lifetime`, `Disconnected<T>`, SE-0532), accepting churn. Stability is re-evaluated at **release** time, not before — a feature being underscored or in-review is not, by itself, a reason to avoid it.

## The governor

"Use the newest" is governed by the universal **certainty process**. A newer capability earns adoption when investigation shows it is **better for the case at hand**, not merely more recent. Newest-for-its-own-sake is the over-engineering failure wearing Swift clothing — the same adjudication applies.

## Working together on Swift

Context: returning to Swift after years away, leapfrogging to current idiom with LLM help. Therefore:

- I default to **current idiom** and do not relitigate the old ways.
- I surface modern constructs **proactively**, even when an older one you would remember would still compile.
- I flag **"this changed since you were last in Swift"** / "this is newer than the prior mental model" without being asked.
- If I show an older-style construct, it is a **deliberate, named choice** — not an oversight.

## Version & feature honesty

(Generalizes the per-project epistemic standard to all Swift work.)

- Every claim about Swift behavior **names the toolchain context** — 5.10 / 6.0 / 6.1 / 6.2 / trunk differ meaningfully.
- Feature claims **cite the SE proposal number and current status** (accepted / implemented / in review / returned).
- For anything **post-5.x, verify rather than recall** — training-data recall is likely stale.
- **Flag experimental features** (behind `-enable-experimental-feature`) explicitly as such.
