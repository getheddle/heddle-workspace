# Swift Conventions — Coding Guidelines Index

> Global / upstream doc, projected into each workspace via `references/` (a downstream copy — never forked; the upstream repo is canonical). Sibling to `design-stance-swift.md`, which it cites for the *why* (forward-feature orientation). A lean index: it points at rules, it does not restate them.
>
> **v0.1 · 2026-06-02 · draft** — seeded from observed friction; categories accrete as friction appears, not by anticipation.

## How to use

Before writing code, identify the **task-type** below and read the linked rules. Each row carries a **when-enforced** tag that says which pass owns it:

- **coding-time** — shapes the code; carry these in the implementation brief's *Read first*. Non-retrofittable.
- **doc-pass** — enforced in the separate documentation pass, not inline (keeps the coding pass lean).
- **tool** — a mechanical pass: run the formatter / linter.

*Forward-path discipline (all rows): when a current-idiom tool or API snags, surface it as a decision point — don't silently fall back to its legacy equivalent. This is the universal stance's "never silently default," applied to tooling.*

## Taxonomy

| Task-type | Enforced | Rules live in |
|---|---|---|
| Tests | coding-time | Swift Testing only, never XCTest. Availability gating → **note A**. |
| Types & buffers ("currency types") | coding-time | Prefer `FoundationEssentials` / `[UInt8]` / `Span` over `Foundation` / `Data` → **note B**. Project carrier & alignment: the project's `DECISIONS.md`. |
| Imports | coding-time | Canonical baseline → **note B**. Foundation-free core where Embedded-clean is required: the project's `INVARIANTS.md`. |
| Generics | coding-time | Prefer constraints over existentials; reach for `any P` only deliberately. A hard "never `any P`" is a project invariant where it applies. |
| Naming & API design | coding-time + doc-pass | Swift API Design Guidelines — <https://www.swift.org/documentation/api-design-guidelines/>. |
| Doc comments | doc-pass | DocC markup + articulation rules → **note C**. |
| Formatting | tool | `swift format` against a committed `.swift-format` (Apple's formatter, bundled in the Swift 6 toolchain). |
| Lint | tool | SwiftLint — *deliberately* (third-party; its rules don't port off-platform). Not a default. |
| Section markers | coding-time | `// MARK:` / `// TODO:` / `// FIXME:` (Xcode-recognized). |

*Not yet populated (accrete on friction): concurrency, error handling, logging, …*

## Notes

**A — Swift Testing × availability.** `@Test` can't carry `@available`; gate availability with a runtime `guard #available` inside the test body. (Setup, not a convention: `swift test` needs a Swift.org toolchain, not Command Line Tools — keep that in the project's `AGENTS.md`/README, since it's environment-dependent and goes stale.)

**B — Currency types & imports.** In portable code prefer `FoundationEssentials` over `Foundation`, and `[UInt8]` / `Span` over `Data`; choose the integer width and signedness the data actually needs. Where Embedded-clean is required, the core imports no Foundation at all — that hard line is the project's `INVARIANTS.md`, not this doc.

**C — Doc-comment articulation** (enforced in the documentation pass). Follow DocC markup (`///`, `- Parameters:`, `- Returns:`, `- Throws:`). Don't explain the obvious; name the standard pattern or algorithm used; state the rationale for non-obvious choices. Reconstruct intent from the code rather than restating it — and flag rationale you genuinely can't infer rather than inventing it (uninferable rationale lives in the project's `DECISIONS.md`).

---
*When this outgrows an inline index, it becomes a Skill: this file as the `SKILL.md` router, each note a small bundled detail doc loaded on demand. v0.1 inlines the few notes deliberately — accrete, don't proliferate.*
