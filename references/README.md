# hooman-method

This is a personal operating method for using LLMs on work that matters, pauses for weeks, and cannot safely live only in chat history.

The **Hooman method** is built for a single principal whose attention is split across projects, operational responsibilities, family, civic work, and long gaps between sessions. Its main problem is re-entry: when I come back to a project, I need to know what was decided, what is next, what must not be touched, and what can be delegated without losing judgment.

The method separates three roles:

- **Human** — owns priorities, constraints, and final decisions.
- **Chat** — frames the work, watches the long arc, drafts briefs, and reviews output with the human.
- **Executor** — investigates or mutates files under a narrow brief, with persistent artifacts as the source of truth.

It is not meant to turn every task into a process. It is an escalation protocol: below the threshold, work informally; above it, create just enough durable structure that the work survives interruption, delegation, and review.

This repository is the **global tier**: the versioned, taggable home for the method's operating documents and assistant skill. Downstream consumers project from a pinned tag; they never fork these docs.

## Who this is for

This may look unusually formal because the circumstances are unusually shaped: one person, many unrelated obligations, intermittent project attention, high context-switch cost, and increasing delegation to AI tools. Some parts are broadly recognizable to anyone doing serious LLM-assisted work; the full apparatus is intentionally personal and should be scaled down unless the same pressures are present.

## The three-tier model

- **Global** *(this repo)* — the method itself: the principal's self-contract, the assistant ground-rules skill, design stances, and coding-convention indexes.
- **Family commons** — a shared layer for a family of related workspaces. Reference implementation: `heddle-workspace`; second field sample: `dev-commons`.
- **Workspace** — an individual project: a `references/` projection of the global docs (a downstream copy, never forked) plus its own anchors, briefs, and findings.

## Contents

- `hooman-contract.md` — the principal's contract with themselves (assistants read narrow sections only for contract/escalation watch).
- `hooman-notes.md` — companion: rationale, provenance, references. Never needed to operate.
- `skills/hooman-assistant/` — the assistant ground rules as an Agent Skill: `SKILL.md` (core) plus `references/contracts.md` (output schemas) and `references/workspace.md` (artifact rules).
- `design-stance/` — design stances; `universal/` applies everywhere, with per-language overlays alongside (`swift/`).
- `coding-conventions/` — coding-guideline indexes, per language (`swift/`).
- `tools/check-docs.py` — local doc-discipline check: budgets, unique rule ids, and contract skeletons.

## Using it downstream (projection v0)

Consumers copy the docs they need, pinned to a release tag, and record the source in a `references/UPSTREAM` marker:

- source repo
- pinned tag
- refresh date
- refresh instruction

Refresh means re-copying at a newer tag. No submodules, no symlinks; the copy rides the consuming repo's own git. The assistant skill installs by copying `skills/hooman-assistant/` into the consumer's skill-discovery directory.

A workspace is governed only after a root `AGENTS.md` or `<project>-context.md` says so explicitly. `references/UPSTREAM` confirms the projection, but folder shape alone is not a marker.

## Checks

Run `python3 tools/check-docs.py` before tagging a doc-set release.

## Versioning & license

Doc-set releases are tagged; latest is `v0.8.1`, and `v0.8.0` was the first repository release, with provenance running back to v0.4 in history. Docs are licensed **CC BY 4.0** (see `LICENSE`). Graduated from the method's founding gist, which remains in place as a redirect.
