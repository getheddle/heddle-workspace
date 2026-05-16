# Changelog

All notable changes to the Heddle Agent Toolkit are documented here.
The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the
project adheres to [Semantic Versioning](https://semver.org/).

Changes to anchors, skills, or subagents in this repo are
**behavioural changes for agent consumers** of the toolkit and must
be recorded here. Documentation-only changes (typo fixes, README
clarifications) and CI/tooling adjustments are exempt. See `AGENTS.md`
"How this toolkit conflicts with a repo file" for guidance on
cross-repo coherence; see this `CHANGELOG.md` itself for the entry-
format model.

## [Unreleased]

### Changed

- `anchors/PHILOSOPHY.md` §3 broadened from "Zero-config UX is the
  headline" to "Progressive disclosure with sensible, inspectable
  defaults" — the principle now spans UI, API, and architecture
  rather than just first-run UX, and explicitly names *inspectability*
  as the load-bearing second half (every default the system picks
  must be visible somewhere the user can read; no magic).
- `anchors/PHILOSOPHY.md` Anti-patterns list adds the
  inspectability-failure anti-pattern ("hide the decision in code and
  document it in the docstring") and re-frames the zero-config
  anti-pattern in the new vocabulary.

### Added

- `skills/heddle-orient/SKILL.md` "rules to keep in mind" list grew
  from three to four items; progressive disclosure is now a top-level
  orientation rule alongside upstream-source-of-truth, statelessness,
  and solo/SMB orientation.
- `skills/heddle-new-worker/SKILL.md` adds an explicit step on
  scaffolding sensible, inspectable defaults in the worker YAML —
  every optional field should have a default the user can read,
  preferably with a one-line comment explaining *why* that default.

## [0.1.0] — 2026-05-15

Initial release.

### Added

- **Anchor docs** (`anchors/`):
  - `ECOSYSTEM.md` — repo map and ownership table for the `getheddle/*` family.
  - `PHILOSOPHY.md` — design opinions (solo/SMB orientation,
    privacy by default, local-first, typed contracts everywhere) and
    anti-patterns.
  - `INVARIANTS.md` — pointer to `heddle/docs/DESIGN_INVARIANTS.md` plus
    seven cross-repo invariants (C1–C7) governing the seam between
    repos: schema source of truth, byte-identical subject names,
    statelessness across languages, processor-not-LLM SDK scope,
    transport abstraction, language parity, and
    warp-design-proposes-only.
  - `CONTRACT_MAP.md` — wire-protocol schemas, NATS subjects, queue
    groups, and the workflow for evolving the contract across repos.
- **Skills** (`skills/<name>/SKILL.md`):
  - `/heddle-orient` — fast cross-repo orientation at session start.
  - `/heddle-invariants` — mid-session refresher on non-negotiable rules.
  - `/heddle-new-worker` — scaffold a worker that respects contracts.
  - `/heddle-contract-sync` — verify and update schema sync between
    `heddle` and `heddle-sdk`.
  - `/heddle-preflight` — repo-aware pre-commit verification.
  - `/warp-adr` — write or format an ADR for `warp-design`.
- **Subagents** (`agents/<name>.md`):
  - `heddle-architect` — read-only design consultant; returns
    implementation plans, not code.
  - `heddle-invariant-guard` — reviews diffs for violations of the
    eight framework red lines plus contrib→core import direction.
  - `heddle-contract-reviewer` — cross-repo wire-protocol coherence
    review (Python ↔ JSON Schema ↔ .NET ↔ Swift).
- **`install.sh`** — symlinks `skills/` and `agents/` into a target
  repo's `.claude/` using relative paths so both checkouts can move
  together. Idempotent; leaves repo-local skill/agent files alone.
- **`audits/`** — historical fresh-eyes documentation audits captured
  during the initial buildout (heddle, heddle-sdk, warp-design).

[Unreleased]: https://github.com/getheddle/heddle-agent-toolkit/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/getheddle/heddle-agent-toolkit/releases/tag/v0.1.0
