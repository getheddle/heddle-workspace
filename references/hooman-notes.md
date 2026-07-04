# Hooman — Companion: Rationale, Provenance & References

*The why behind the operating set: why the method exists, the reasoning each prescription leans on, what's distinctive, where it sits in the ecosystem, verified references, the candidate-binding roadmap, and open questions. The operating set itself is `hooman-contract.md` (the principal's self-contract) and the `hooman-assistant` skill (`SKILL.md` + `contracts.md` + `workspace.md`, the assistants' ground rules). Read those to operate; read this when you want the reasoning. Never needed in an agent's working context.*

**Canonical version:** <https://github.com/hooman/hooman-method>.

**Status:** Draft v0.8.1 (2026-06-17). Changelog at the end.

---

## The name

**Hooman** is eponymous — named for its author (GitHub: `hooman`) — because it is, for now, a single-user method, not a universal standard. Naming it after the author is honest about that scope.

The name does double duty. It quietly encodes the method's premise — a *human* in the director's seat, directing AI executors ("Hooman" ≈ "human", and the human-in-the-loop is the whole point). And it sidesteps two collision problems at once: the crowded ecosystem vocabulary (*workflow, skill, agent, constitution* are all taken) and the method's own internal terms (*brief, cycle, offload*). It namespaces the entire toolkit: the `hooman-assistant` skill, the `hooman-method` repo, the founding gist (now a redirect).

**Rejected alternatives** (per the naming gate):

- **homer** — the author's old dial-up-BBS handle. Rejected as the primary name: dominated by Homer Simpson and the Greek poet, and already used by existing dev tools (a self-hosted dashboard; a SIP-capture tool). Kept only as a sentimental nod here.
- **"Chat-First Project Development with LLMs"** — the descriptive working title through v0.4. Retired as the primary name. It still describes the method accurately and could serve as a public descriptive subtitle if the method is ever published for others.

**The doc set** (since v0.8): `hooman-guide.md` is retired. Its self-directed discipline became `hooman-contract.md`; its agent-operational rules became the `hooman-assistant` skill; its rationale lives here. The migration map for that split is a one-time review artifact, not part of the canonical set.

### Role labels: "Code" → "Executor" (v0.6)

The role labels are **Chat** (orchestration) and, as of v0.6, **Executor** (the tool-equipped agent). The executor role was renamed from "Code" because the distinction that actually matters between the two roles is **embodiment** — a tool-equipped agent with filesystem and execution access versus a conversational assistant — *not* subject matter. "Code" implied the work was always software; in practice the same role drafts bills of materials, structures analytical briefs, and runs research. "Executor" names the function across domains. The tool that fills the role is still usually a coding agent (Claude Code); role and tool are distinct.

*Rejected alternatives:* **Synthesizer** (too drafting-specific); **Agent** (overloaded across the ecosystem); **Worker** (vague, says nothing about embodiment). **Chat** is retained — accurate for the orchestration role and not overloaded in this context.

---

## Why this exists

Working on a non-trivial project with an LLM hits a predictable ceiling. A single conversation can't hold the project's full context. Detail work pollutes the conversation's attention budget. Decisions made in one session get re-derived in the next. The LLM serializes all reasoning through one context window, and the output reflects the limits of one model's first-pass thinking.

The conventional response — "use a more capable model" or "use a coding agent" — is partial. But the deeper point, and the one that explains the method's shape, is *who it is for*:

> Hooman is a personal operating method for delegating complex, intermittent work to LLMs without losing the thread. It is built for a single principal whose main job is not this project and whose attention is split across operational, technical, family, civic, and personal domains. The dominant cost in that situation is not bad output — it is **re-entry**: picking a project back up after a long gap and reconstructing what was decided, what was half-done, and what must not be touched. The method separates judgment from execution — the human owns priorities, constraints, and final decisions; Chat holds direction and frames delegation; the Executor investigates, implements, audits, and summarizes; durable artifacts carry context across gaps — and it optimizes for re-entry being cheap, delegation being the default, and scarce attention going to judgment rather than to rediscovering context or shuttling handoffs.

That framing explains choices that otherwise read as overbuilt. The artifact system is not ceremony; it is **externalized working memory** for someone who may touch a project once a month between fabrication deadlines, family obligations, and IT emergencies. The roadmap, anchors, session summaries, glossary, and findings inbox are what make a three-week gap survivable.

Stated as design properties, the method optimizes for: fast re-entry after context gaps; clear delegation boundaries; persistent decision memory; low ceremony during active work; high recoverability when work stalls; protection from agent-generated sprawl; and separation between unrelated efforts. The *scale-to-stakes* rule (contract, *Before invoking*) is the operational expression of that last property — not every effort earns the full apparatus.

---

## The shape the problem forces

*(Absorbed from the retired guide's two-role narrative; the operational residue is skill role.1–7.)*

The response that works is **role separation with mechanical artifacts**: a conversational assistant that holds strategy, a tool-equipped agent that investigates and implements, and artifacts in the project tree that survive across sessions and across handoffs to entirely new agents. The human stays in the seat that can't be delegated — priorities, constraints, final decisions — and pushes reconnaissance, implementation, inventory, and cleanup outward.

**Why reconnaissance and mutation are separate modes, not phases.** The Executor bundles two functions with different safety profiles: read-only investigation and real writes. Reconnaissance is the mode most users underuse — the Executor is a remarkably effective design partner when the brief asks it to think, not to type. Treating the two as one undifferentiated "do the work" role is the most common way unreviewed writes slip through; the method separates them by brief type and, where the tool allows, by enforcement (plan mode for reconnaissance, show-diff for mutation).

**Why output contracts, and why the evidence map is the one to keep.** Scarce attention makes *review cost* the real bottleneck, not execution. Vague delegated output forces the principal to reconstruct context just to judge it — the exact cost the method exists to avoid. So every brief names what "done enough to decide quickly" looks like. The evidence map (*inspected / inferred / unverified*) is the load-bearing field because agents reliably produce plausible plans that under-report what they never actually looked at; the tag forces that distinction into the open. v0.8 closes the map's own honesty gap — the tags travel the same self-report channel as the failure they police — with two mechanisms: coverage counts that make under-inspection visible at a glance, and a spot-check rule (skill review.3) that samples `[inspected]` claims against what was actually read. A false `[inspected]` is at least a falsifiable lie rather than a vague one.

**Why the principal gets guarded twice.** The method routes all judgment to one person and would otherwise never check it — for a solo operator, one's own framing is the unguarded single point of failure. Two guards now exist, deliberately asymmetric. The **direction check** (contract, *Before dispatching*) is self-administered: three questions on the brief's framing, adopted on its own friction trigger. The **contract watch** (skill conduct.8 + the contract's standing triggers) is assistant-administered: the assistant may name a trigger by id when it sees the pattern, once, without arguing. Only the standing triggers are assistant-visible by design; whether the direction check should also become assistant-administered is an open question below, gated on the same friction as everything else.

---

## Why each artifact earns its place

*(Absorbed rationale; the operational rules are skill canon.\*, ws.\*, inbox.1, and the contract's rituals.)*

- **Anchors as constitution.** Briefs cannot quietly override them: a plan that implies changing what an anchor states is a deliberate anchor revision, not a side effect of implementation. Propose-then-commit is the gate, and the friction of committing by hand is the feature — it is what keeps the canonical docs canonical (see *Deferred bindings*).
- **Glossary as a gated artifact.** The hardest moments in a project tend to be naming negotiations, renames, and terms whose meanings have drifted. A disciplined glossary prevents most of them and shortens the rest; the naming gate runs *before* a term is added, and deprecated names are kept, dated, and pointed forward so old material keeps resolving.
- **The findings inbox.** Sessions regularly notice issues in passing — dead links, drifted facts, undocumented behavior. Without somewhere to drop them, findings die when the session ends; with somewhere too heavy, capturing them derails the session. One append-only line each is the equilibrium, and it doubles as the capture-and-return move for the principal's own tangents (contract T1).
- **Roadmap next-action-first, because re-entry is a deciding problem.** After a long gap, the facts being *available* is necessary but not sufficient — a status dump still leaves you to decide what to do next, and for intermittent work the deciding is itself the cost. So the re-entry surface leads with the single next concrete action; you read one line and move. A re-entry surface that opens with a wall of state has lost the point of the method.
- **Session close, and why it needed a trigger.** The close ritual makes discarded context productive — but it is also the discipline most likely to be skipped under exactly the conditions the method is built for (interruption, fatigue). The v0.7 failure map assigned the stale-next-action failure to the very ritual whose lapse causes it. T6 breaks that circle: when a session is being cut off, the next-action line is the one thing that may not die, and it costs thirty seconds.
- **`aside/` — one designated catch-all.** Misfit material otherwise fails in one of two ways: accumulating ad-hoc in whatever folder is nearest, or spawning a new folder per misfit (premature structure). One catch-all with a promotion rule and kill-criteria hygiene is the anti-bureaucracy guardrail made physical — a waystation, not a graveyard. (The `overlays/` → `aside/` rename rationale is recorded in the v0.7.4 changelog entry.)
- **`references/` and the global layer.** The first *second* project forced the recognition that some governing documents are cross-project: the method itself, the design stances, the conventions indexes. They live upstream of any workspace and project *into* each one as a downstream copy that is never forked — one source of truth, many readers. The projection mechanism was deliberately deferred at v0.7.2; it is now the subject of the repo-graduation design track.
- **Visible artifacts over opaque memory.** Platform memory is convenient but often non-auditable and silently mutated — a mismatch with an otherwise inspectable system. Memory is a cache; if a fact matters for re-entry, it lives in a visible artifact, and the artifact wins any conflict. The six-month test keeps the partition stable: durable shape goes to the context file, temporal state to memory, borderline cases lean toward memory until stability is demonstrated.

---

## Why the method is an escalation protocol

The failure the method most has to guard against is not premature invocation; it is **scope gravity** — a large, interesting effort entering the system as fog. Hence the threshold (work informally below it), the scope-intake gate at the moment of escalation (*big is allowed, undefined is not*), and scale-to-stakes as the first operational decision rather than a bootstrap afterthought. Positioning the method as escalation-not-universal-workflow is also what keeps its apparatus from reading as bloat: below the line the apparatus is overhead; above it, its absence is.

The same logic runs backwards as the **anti-bureaucracy guardrail**: every rule, template, convention, and artifact must name the specific friction it solved, and — since v0.7's kill criteria — must keep earning its place to survive. Adoption needs observed friction; survival needs it too.

The named failure mode this guards is **process-as-avoidance**: building or refining the method substituting for doing the work. The method's own history supplies the observed friction — the v0.5–v0.7 stretch shipped eight releases in ten days against roughly two days of real use, a ratio the failure map says to watch — and that episode is what T2 and T8 in the contract now exist to catch, with the contract watch (conduct.8) making the catch assistant-administered rather than purely self-policed.

---

## Doc-audience layering — and the v0.8 split

Project documents serve different audiences, and mixing audiences in one document leads to bloat and to docs nobody fully reads. The method distinguishes agent-specific docs (lean, operational, pointer-heavy), human-leaning docs (narrative, navigational), and hybrids — under one principle: **every persistent context file is a table of contents, not a textbook**, because every line in an auto-loading file claims a slice of every reader's attention budget, every session.

One anti-pattern deserves its rationale spelled out: **"docs AIs read but humans don't."** Files written entirely in agent-pleasing telegraphic style accrete around AI-heavy projects and quietly displace the human-readable doc surface. The resolution is not "no agent docs" — it is that a telegraphic agent doc is acceptable only while the human surface stays alive and primary, and while a human still authors and commits every change to it (propose-then-commit makes the human the write path, so hostility to human readers is a tax collected at every edit).

v0.8 applied this rule to the method's own documents, which had drifted into exactly the hybrid bloat the rule warns about: one guide serving two audiences, 527 lines, over its own budgets, with one drift incident (v0.7.1) already on record. The split's disciplines:

- **Partition, not projection.** Every rule has exactly one canonical home — operational rules in the skill, personal discipline in the contract, rationale here — with pointers and never restatement. Restatement is how two-doc drift happens.
- **Structure points at outputs, not at the rulebook.** Models need unambiguous imperative rules more than they need markup, but they *echo* a given structure very reliably — and structured feedback is validatable on receipt and sweepable later. So the contract skeletons and the evidence map are strict; the rules stay disciplined Markdown; XML islands appear only at boundaries that must never blur (precedence, don't-touch).
- **Budgets are declared per file**, which is what makes the doc linter (now an adopted binding, below) checkable rather than aspirational.
- **Design the agent doc for the weakest model actually used as Chat** — structure's payoff scales inversely with model capability.

---

## Failure map

The happy path is the easy case to document. These are the failures that actually bite, each mapped to the mechanism that catches it — now by rule id. If a failure recurs and *no* mechanism catches it, that is the friction that justifies a new rule.

| Failure | Symptom | Caught by |
|---|---|---|
| Stale Executor context | Plan references code or conventions that have changed | Reconnaissance + evidence map (review.1) |
| Over-confident feedback | Plausible plan, unstated unknowns | Coverage counts + spot-check (review.3); Skeptic/Omission lenses (review.2) |
| Over-scoped plan | Executor proposes more than the brief asked | Scope lens (review.2); locked-scope briefs (brief.3) |
| Hallucinated conventions | Executor invents repo patterns that don't exist | Evidence map (review.1); Invariant lens (review.2) |
| Wrong target, well executed | Clean cycle, wrong question | Direction check (contract, *Before dispatching*) |
| Duplicate artifacts | Second doc or term for an existing concept | Naming gate (canon.3); handbook as locational index (ws.3) |
| Glossary overgrowth | Low-value terms accumulate | Add-trigger (canon.4) |
| Anchor conflict | A plan quietly implies changing an invariant | Precedence P3; Invariant lens (review.2) |
| Silent artifact drift | An agent edits a canonical doc without review | DT1–DT2 + show-diff (role.5) — honestly: the net is human attention on the diff, which is why the scoped-allowlist binding stays queued |
| Premature binding | Tooling encodes a rule before friction proved the need | T5; friction audit |
| Method leakage | Full apparatus applied to a small effort | Scale-to-stakes (contract, *Before invoking*) |
| Re-entry stall | Context present but the session won't start | Next-action-first (conduct.7; ws.4) |
| Process-as-avoidance | Refining the method substitutes for the work | T2/T8; contract watch (conduct.8) |
| Stale next action | The re-entry line points at a done step | T6; ws.4 |
| Memory ⊥ artifacts | Platform memory contradicts the repo | P2 — visible artifacts win |

---

## Session modes

Descriptive of current practice, not prescriptive; whether modes deserve their own brief templates or context-loading recipes remains open — though v0.8 gives the recipes question a concrete substrate (which skill files load per mode: review sessions want `contracts.md`, artifact-creating sessions want `workspace.md`).

| Mode | When | Output |
|---|---|---|
| **Vision / strategy** | Long-arc direction, new bets, positioning | Roadmap entries, anchor updates |
| **Track scoping** | Turning an intent into a defined feature track | `roadmap/<track>.md` |
| **Cycle opening** | Translating a need into an Executor investigation brief | `session-starters/<brief>.md` |
| **Review** | Processing Executor feedback, weighing trade-offs | Decisions committed to roadmap, anchors, or a next-round brief |
| **Architecture decision** | Committing to a design with documented rationale | An ADR or equivalent decision record |
| **Audit triage** | Reading audit findings, deciding what becomes a cycle | A maintenance-cycle scaffold |
| **Realignment** | Restructuring an existing project to fit this methodology | A migration plan, new anchors, retroactive roadmap |

---

## What's distinctive here

Most of this method is novel framing of patterns the LLM-tooling ecosystem has converged on independently. What's genuinely distinctive — worth naming as contributions rather than reinventions:

- **The anti-bureaucracy guardrail**, with **kill criteria**: most methodologies accrete templates; very few require observed friction to adopt a rule *and* to keep it. Scale-to-stakes is its operational complement.
- **The offload test.** "Does this produce content / inventory / details? → Executor. Does it produce direction? → conversational role." Sharper than the implicit splits in most multi-agent frameworks.
- **Output contracts by task type**, including the **evidence map** — and, since v0.8, coverage counts plus a spot-check rule that close the map's own self-report gap. It targets *review cost* directly, the real bottleneck for a time-scarce principal.
- **The direction check** — an adversarial gate pointed at the *director's own framing*, not only the executor's plan. (Prior art in the decision literature: Klein's pre-mortem and the red-team-your-own-framing tradition; within LLM-method space the survey found nothing comparable.)
- **The contract watch** (v0.8) — the principal's self-contract carries machine-citable trigger ids, and the assistant is licensed to name a trigger once when it sees the pattern. The solo principal's discipline gains an enforcement loop that doesn't depend on the principal's own moment-of-failure judgment.
- **The reconnaissance / mutation factoring** of the executor role — two modes with distinct review profiles rather than two phases of one undifferentiated role.
- **Hooman as an escalation protocol**, with a **scope-intake gate** aimed at *scope gravity*: big is allowed, undefined is not.
- **Glossary discipline as a gated artifact**, with naming rules that run before a term is added.
- **The findings inbox** as a standing log for drive-by observations, swept on schedule.
- **Doc-audience layering**, including the *entry-point docs are thin* rule — now applied to the method's own doc set (v0.8).

These are the parts most worth formalizing for reuse outside one project — and they are deliberately kept here, in the companion, so that personalizing the operational set does not erode the generalizable spine.

---

## What this is not

- **Not a tooling spec.** It requires no particular LLM, IDE, or platform.
- **Not a coding methodology.** It governs *how you collaborate with LLMs*, not *how you write code*.
- **Not a project-management methodology.** Compatible with Agile, Shape Up, or whatever cadence you prefer; it governs the *content* and *handoff* of work, not its scheduling.
- **Not a team methodology.** Single-principal by design; multi-human adoption is an explicit non-goal of this version, not an unsolved part of it.
- **Not finished.** An evolving draft, distilled from one project's experience plus an ecosystem survey.

---

## Ecosystem positioning & survey

The method was distilled from one project's practice (Heddle) plus a survey of the May 2026 AI-coding-agent ecosystem, triangulated across several independent LLM research tools. Where it sits: a novel *framing* of patterns the ecosystem converged on independently — the orchestrator/executor split, plan-then-implement, project-root agent files (AGENTS.md), modular capability files (Skills / SKILL.md), MCP, spec-driven tools (Spec-Kit, Kiro), and sub-agent context isolation. The distinctive contributions are listed above. The underlying research reports are kept in the author's archive, not published with the method.

*Source-integrity note:* the survey's distinct inputs were fewer than they appeared — verify source independence before treating any cross-tool "consensus" as strong. Lean on the *Verified references* below.

*On review independence (v0.6, reaffirmed v0.8).* That caution generalizes beyond the survey. Revisions of this method have been shaped by reviews from frontier models, blind and context-aware; their recommendations converge strongly. Treat that convergence the same way: frontier models share training data and house-style priors — they gravitate toward "personalize it, add a taxonomy, automate the loop" — so cross-model review consensus is lower-independence than it looks. Convergence flags changes worth *examining*; each change is kept only where it survives the method's own tests. (v0.8's reviewer applied the rule to itself: the split it endorsed was subtractive, and the maximal-XML lockdown it declined was the house-prior-shaped half.)

---

## Verified references

Ecosystem claims checked against primary sources (**verified as of May 2026**). These are current, public facts that will decay — re-check before relying on them — and they are **positioning, not load-bearing**.

- **AGENTS.md is a Linux-Foundation-stewarded open standard.** *Verified.* The Linux Foundation formed the **Agentic AI Foundation (AAIF)** in December 2025, anchored by founding contributions: **MCP** (Anthropic), **goose** (Block), and **AGENTS.md** (OpenAI). Sources: [Linux Foundation press release](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation), [OpenAI](https://openai.com/index/agentic-ai-foundation/), [agents.md](https://agents.md/).
- **Adoption: 60,000+ open-source projects.** The figure stated by the AAIF / agents.md — consistent across sources, but **self-reported, not independently audited**. Cite it as such.
- **SKILL.md is cross-tool portable.** *Verified, with nuance.* The **Agent Skills** specification ([agentskills.io](https://agentskills.io/specification)) was released by Anthropic as an open standard (December 2025) and is compatible across Claude Code, OpenAI Codex CLI, Gemini CLI, OpenClaw, and OpenAI's Skills tool. Skills adhering to the core format (YAML frontmatter `name` + `description`, markdown body, progressive disclosure) are portable without modification; tool-specific extensions are not guaranteed to carry over.

Also confirmed in passing: **MCP** was likewise contributed to the AAIF; the spec-driven tools **Spec-Kit** (GitHub: *constitution → specify → plan → tasks → implement*) and **Kiro** (AWS: `requirements.md` / `design.md` / `tasks.md`, EARS notation) match the method's escalation shape and its use of anchors as a "constitution."

---

## From methodology to tooling — candidate bindings

Some concepts may eventually earn a **tool binding** — the encoded form that runs a rule automatically rather than by discipline. Each is adopted only when its own trigger fires.

| Concept | Candidate binding | Friction solved | Adoption trigger / status |
|---|---|---|---|
| Session modes | Auto-loadable instruction packs | Mode context re-pasted by hand | Mode context retyped across ≥3 sessions |
| Cycle-brief R1 | Plan mode / read-only constraint | Executor implements during R1 | First unrequested write in R1 |
| Cycle-brief implement | Show-diff hooks, scoped tool allowlists | Unreviewed writes; anchor edits slipping through large diffs | First unreviewed write that should have been caught |
| Sub-agent roles | Configured sub-agent definitions, tight scopes | Ad-hoc dispatch, inconsistent isolation | Sub-agent failure traced to scope — *bound downstream in `heddle-workspace` (reviewer/architect subagents); upstream generalization is part of the repo-design track* |
| Output contracts | Brief templates with the schema built in | Review cost; under-reported unknowns | **Adopted v0.8** — `contracts.md` skeletons + Chat-side validation |
| Doc discipline | Linter: budgets, unique rule ids, skeleton validation | Budget breaches and drift unnoticed | **Adopted v0.8, built v0.8.1** — trigger fired (the guide blew its own budgets); shipped as `tools/check-docs.py` |
| Direction check | Pre-dispatch checklist (skill or brief preamble) | A cycle answers the wrong question | A well-executed cycle aimed at the wrong target |
| Findings inbox | Standing log; eventually a structured-note tool | Drive-by findings lost | Findings lost despite the log |
| Glossary discipline | A gate running the naming rules on add | Rule checks applied inconsistently | Terms landing without rule checks |
| Audit cycles | Scheduled agent runs against narrow-slice auditors | Audits skipped indefinitely | *Bound downstream in `heddle-workspace` (audit-runner → planner → implementer → coordinator); upstream generalization is part of the repo-design track* |
| Chat→Executor dispatch | An MCP server exposing the Executor as a callable tool | Human-as-messenger overhead | **Deferred** — cost-based (see *Closure mechanics*) |

The general principle: a binding that removes *friction* is a candidate; a binding that removes *curation* is a hazard.

---

## Closure mechanics (future)

Today, briefs are produced as files, saved to the workspace manually, and the Executor is pointed at them. An end-state where Chat dispatches Executor briefs directly via an MCP-style tool and reads the feedback inline is a natural evolution — it closes the human-as-messenger loop.

**When to build it.** The earlier trigger was by *count*: a session needing more than two rounds of human transcription. The real variable is **cost per transcription, not count**. For an operator whose every context-switch carries a high cognitive tax, a single shuttle costs more than the count implies, and the threshold is correspondingly lower — *without* discarding the trigger logic and building ahead of friction. Below the threshold the manual loop is fast enough; above it the dispatch tooling starts paying its cost.

---

## Deferred bindings (explicit)

Two bindings remain deliberately *not* built, logged so the decision is explicit rather than quietly forgotten. Both were recommended by reviewers; both were declined on the method's own terms.

- **Chat→Executor MCP dispatch** — the zero-transcription loop. Deferred per the anti-premature-binding rule; the trigger is cost-based (above).
- **Auto-synthesis of canonical artifacts** — an agent extracting decisions at session end and writing them straight into anchors and the glossary. Deferred on a stronger ground than friction: **auto-writing the project's constitution destroys the curation that makes it canonical.** The atrophy problem it would solve is real; the sanctioned answer is **propose-then-commit** — the agent drafts, the human commits in-session — which cuts the compilation cost without surrendering the write path.

---

## Open questions for iteration

- **Session modes.** Descriptive, not prescriptive; whether modes earn templates or context-loading recipes is open. v0.8's file split supplies the substrate if they do.
- **Trust calibration.** Whether useful calibration can stay informal, or inevitably wants a structured record without becoming its own bureaucracy, is unproven.
- **Direction-check efficacy — and administration.** Whether a pre-dispatch self-check reliably catches mis-framing is unproven; adoption stays gated on a well-executed cycle hitting the wrong target. v0.8 surfaced, and declined for now, promoting it to assistant-administered (Chat asking the three questions whenever it drafts an R1 brief): same gate, same friction trigger.
- **Closure of the Chat→Executor loop.** Deliberately deferred; see above.
- **Multi-project user.** The within-project memory/context split is operational via the six-month test. What legitimately belongs in account-scoped user memory rather than per-project context remains worth a dedicated audit as the multi-project case grows. The parallel *governing-documents* axis is now in motion: the global layer projects via `references/`, and the projection mechanism is the subject of the repo-graduation design track.
- **Upstream/downstream seam with `heddle-workspace`.** The Heddle toolkit already field-runs several of the method's patterns as tooling (adapter symlinks into agent discovery directories, an umbrella-repo workspace lifecycle, the audit→cycle pipeline as a four-agent chain). What of that is method-generic and extracts upstream, versus Heddle-specific and stays — and whether the upstream repo ships tooling at all or stays docs-plus-skill pointing at a reference implementation — is the central question of the repo-design track.
- **Anti-bureaucracy in practice.** The friction audit's first real run effectively happened as the v0.8 split (this doc set was the artifact set under audit). Open: the cadence, and the first run against a downstream *project* workspace.
- **~~Team adoption.~~** *Out of scope (v0.6)* — an explicit non-goal.
- **~~Role labels.~~** *Resolved (v0.6).*
- **~~Verification of ecosystem claims.~~** *Resolved* — see *Verified references*.

---

## Changelog

- **v0.8.1 (2026-06-17)** — Escalation watch, workspace-recognition rules, the doc linter shipped, and a README orientation pass. Added the **escalation watch** (skill `conduct.10`): when the session plus memory clearly meet the contract's escalation threshold, suggest escalation once and ask for the three scope-intake answers — the human escalates, the assistant only flags — and widened the contract's assistant-reading scope from *Standing triggers* alone to also cover *Before invoking* and *At escalation*, for `conduct.8` / `conduct.10`. Added **workspace-recognition rules** `ws.13`/`ws.14`: a directory is governed only once a root `AGENTS.md` or `<project>-context.md` says so explicitly (`references/UPSTREAM` confirms projection; matching folder names alone do not), and absent the marker the assistant flags via `conduct.10` rather than assuming governance — the same rule mirrored into the README's downstream-projection section. **Shipped the doc linter** `tools/check-docs.py` (line budgets, unique rule ids, contract-skeleton validation) — the binding whose trigger fired at v0.8 with its build queued to the first cycle. Fixed a stale `hooman-guide.md` reference in `design-stance-universal.md` (→ `hooman-contract.md` + the `hooman-assistant` skill). **README orientation pass:** rewrote the repository opening for a human reader before the repo inventory — named the method as a personal operating method for LLM-assisted work that pauses for weeks, explained the re-entry problem, introduced the Human / Chat / Executor split, and clarified that Hooman is an escalation protocol rather than a process for every task; added a short "Who this is for" section; made the downstream projection instructions easier to scan.
- **v0.8 (2026-06-11)** — Split the operating guide by audience, per the method's own doc-audience layering rule: `hooman-contract.md` (the principal's self-contract — escalation threshold, scope intake, direction check, kill criteria, and standing triggers T1–T8 as WHEN→THEN pairs) and the `hooman` skill (assistant ground rules in Agent Skills format: `SKILL.md` core on a 120-line budget · `contracts.md` output schemas · `workspace.md` just-in-time artifact rules). `hooman-guide.md` retired. Partition rule: every rule has one canonical home; pointers, never restatement. Structure was pointed at outputs rather than the rulebook — contract skeletons with mandatory sections, evidence-map coverage counts, a Chat-side validate-then-bounce rule — with XML islands confined to precedence, don't-touch, and contract wrappers. New mechanisms: the **contract watch** (conduct.8; assistant cites trigger ids), the **evidence-map spot-check** (review.3; closes the self-report gap), **T6** (non-circular catch for stale next-actions), and per-file budgets. This companion absorbed the rationale stripped from the guide (role/contract reasoning, artifact rationale, escalation framing, layering — including the v0.8 split's own story), repointed all guide references, rewired the failure map to rule ids, and recorded two bindings as adopted (output contracts; doc linter — trigger fired) and two as bound-downstream in `heddle-workspace` pending the repo-design track. Prompted by observed friction: the guide had outgrown its own attention-budget rules while serving two audiences at once; the assistant-side set was reader-tested against the split's target before commit.
- **v0.7.4 (2026-06-04)** — Renamed `overlays/` → `aside/` and broadened it from repo-belonging symlink-storage into a deliberate **catch-all**: workspace-scoped material that has no better home *and* isn't big or frequent enough to earn its own location yet. Three accepted kinds — (a) repo-belonging files stored out-of-repo via symlink (the original role, retained); (b) parked decisions / parking lots; (c) low-frequency working docs — with a **promotion rule** and a **hygiene rule** (subject to the kill criteria / friction audit). Prompted by observed friction: the narrow `overlays/` definition left no home for parked/misc working docs, so they accumulated in it off-label. **Renamed, not just redefined,** because `overlays` actively mis-signals a catch-all; *rejected `unfiled` and `misc`* — both lean toward "disposable junk" and mis-describe the durable symlink occupants.
- **v0.7.3 (2026-06-04)** — Added Post-implementation passes to the cycle-brief protocol: retrofittable concerns factor out of the implementation pass into dedicated mechanical and semantic passes; the semantic pass doubles as a lightweight correctness review and reconstructs intent skeptically. Prompted by observed friction: a separate doc-review pass that both improved maintainability and found bugs.
- **v0.7.2 (2026-06-02)** — Added **Global references**: cross-project governing documents live upstream and project into each workspace via `references/` as a downstream copy that is never forked. Prompted by observed friction: the first *second* project (Cap'n-Proto-for-Swift) needed the method and stance docs shared across workspaces. The projection *mechanism* deferred to its own pass.
- **v0.7.1 (2026-06-01)** — Consistency fix: Chat *maintains a working representation of* the project's direction but the human *owns* it. A proposed v0.8 package was **considered and mostly declined** — most of it codified *anticipated* friction on a method with ~2 days of real use, against the anti-bureaucracy rule.
- **v0.7 (2026-05-29)** — Framed the method as an **escalation protocol** with a two-of-five entry threshold; added the **scope-intake gate**, **kill criteria**, a **visible-artifacts-over-opaque-memory** rule, and three failure-mode rows including **process-as-avoidance**. Centered the **evidence map**. Prompted by a second external review whose additions were mostly declined; a compress-and-clarify pass.
- **v0.6 (2026-05-29)** — Reframed the optimization target around a single principal with **re-entry** as the dominant cost. Renamed **Code → Executor**; split **reconnaissance / mutation**. Added **output contracts** with the **evidence map**, the **direction check**, **trust calibration**, a **failure-modes** map, a **Re-entry** section, an AGENTS.md **pruning order**, a tightened glossary add-trigger, **propose-then-commit**, and the **review-independence** note. Demoted team adoption to a non-goal.
- **v0.5 (2026-05-29)** — Named the method **Hooman**; split the single document into companion + operating guide. Added *The name*, *Ecosystem positioning & survey*, and *Verified references*.
- **v0.4 (2026-05-26)** — "Table of contents, not textbook"; six-month test; degrees-of-freedom across cycle rounds; adversarial gate; sub-agent interface; nested AGENTS.md; *Session close*; anchors as constitution; friction audit.
- **earlier** — see the gist's revision history.

---

*Companion to the operating set (`hooman-contract.md` + the `hooman-assistant` skill). Distilled from the Heddle project's practice plus a May 2026 ecosystem survey. An evolving draft — refine in place.*
