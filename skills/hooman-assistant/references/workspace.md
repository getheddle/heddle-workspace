# Workspace shape & artifact rules

Draft v0.8.1 (2026-06-17) · part of the `hooman-assistant` skill · load just-in-time: when creating artifacts, bootstrapping a project, or realigning one. Not needed for ordinary cycles.

## Tree

```
<workspace>/
├── <repo-a>/  <repo-b>/  ...
├── AGENTS.md              # agent entry point (budget + pruning, ws.9–11)
├── HANDBOOK.md            # human navigation: where things live; restates nothing
├── GLOSSARY.md            # project vocabulary (canon.2–4; structure, ws.12)
├── anchors/               # constitution: PHILOSOPHY, INVARIANTS, AUDIENCE_PERSONAS
├── references/            # projected global docs — read-only, never forked (DT3)
├── roadmap/               # feature work, one file per track
├── session-starters/      # briefs + feedback; findings-from-chat.md at its root
├── audits/                # audit reports, named to link to cycles (ws.5)
├── aside/                 # the one catch-all (ws.6)
└── <project>-context.md   # portable orientation; loaded as a platform project file
```

## Artifact rules

- ws.1 — Artifacts appear on friction, not on day one. Choose the smallest shape that keeps re-entry cheap and delegation clean.
- ws.2 — Anchors: short, slowly evolving, constitution semantics (P3). Common set: PHILOSOPHY.md (what this is and isn't for), INVARIANTS.md (what must hold), AUDIENCE_PERSONAS.md (whom we design for).
- ws.3 — Handbook: purely locational, a two-minute read, updated lazily. Tier-2 per-folder READMEs and a Tier-3 task cheat-sheet only after demonstrated confusion or repetition — never preemptively.
- ws.4 — Roadmap tracks carry lifecycle states: idea → proposed → ready → in-flight → shipped → parked → retired. The current next concrete step is the first line of the track — it is the re-entry surface (conduct.7).
- ws.5 — Audits link mechanically to the cycles they seed: `audits/<repo>-audits/<topic>-audit-<YYYY-MM-DD>` ↔ `session-starters/<repo>-<topic>-<YYYY-MM-DD>/`. Audits come from a run pass (manual, scripted, or LLM-driven), never from imagination.
- ws.6 — `aside/` is the single designated catch-all. Accepted kinds: repo-belonging files stored out-of-repo via symlink; parked decisions and parking lots; low-frequency working docs with no home. Promotion when a kind grows big or frequent enough to earn its own location; contents are subject to the kill criteria in `hooman-contract.md`. A waystation, not a graveyard.
- ws.7 — `references/` is a downstream projection of upstream global docs (the method itself, design stances). The upstream copy is canonical; changes flow upstream→down only; a project never forks a global doc locally.
- ws.8 — The project context file: 1–2 pages, durable shape only — platform, audience, discipline, operating rules. Refresh on shape changes, not per release. Temporal state lives in roadmap next-action lines and platform memory, and visible artifacts win conflicts (P2).
- ws.12 — Glossary structure: categorized, not flat (personas, process, architecture, repos/artifacts, industry, deprecated); alphabetical within category. An entry whose term has a natural home doc is one or two sentences plus a pointer; a term too small for a home doc gets a self-contained entry. Renames are never deleted — mark `superseded by X (YYYY-MM-DD)` so old material keeps resolving.
- ws.13 — Workspace recognition is explicit: the nearest root `AGENTS.md` or `<project>-context.md` must say the workspace is governed by Hooman Method. `references/UPSTREAM` confirms projection from this repo; matching folder names alone do not.
- ws.14 — If recognition markers are absent but escalation may be warranted, apply conduct.10. Do not treat the directory as governed until the human escalates and the marker exists.

## AGENTS.md discipline

- ws.9 — Budget ≈200 lines. Operational register: imperative bullets, command-first, task-organized, closure-defined (every section says how an agent knows it is done). No prose paragraphs, no ambiguous directives ("be careful"), no contradictory priorities across sections.
- ws.10 — Pruning order when over budget, applied until it fits: narrative rationale → handbook or anchor · duplicated rules → one canonical statement · stale setup notes → delete · repo-specific content → that repo's nested AGENTS.md · inlined commands → pointer to the repo's docs.
- ws.11 — Nested AGENTS.md in multi-repo workspaces: the root file owns cross-cutting concerns; repo files extend it and never restate it; conflicts resolve per P1.

## Bootstrap — new project past the escalation threshold

1. Write `<project>-context.md`; load it as a platform project file. This alone lets every session start oriented.
2. Write a one-page HANDBOOK.md pointing at what exists so far.
3. Stub PHILOSOPHY.md. Add INVARIANTS.md and AUDIENCE_PERSONAS.md when a decision or a breakage demands them, not before.
4. Define one roadmap track and run one full cycle against it (brief → feedback → review).
5. Glossary entries on demand, as terminology negotiations arise.

Everything else — the remaining folders and root files — appears when the work calls for it.

## Realign — existing project

1. Inventory where design intent and maintenance planning currently live.
2. Context file first — the single highest-leverage artifact.
3. Handbook second, once the inventory says what's where.
4. Anchors as they get referenced, never the full set up front.
5. The cycle pattern on the next piece of work; never backfill old work into it.
6. Roadmap / session-starter split when a second track of work appears.
7. Glossary on demand.
