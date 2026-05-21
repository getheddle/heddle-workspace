# AGENTIC-DEV: Development under bounded vigilance with AI assistance

**Status:** Active. PHILOSOPHY-weight / advisory. **NOT an invariant.** The principle stated here is a load-bearing bet about how design value is measured at solo + AI scale; it remains itself walk-back-able at bounded cost. This anchor is the principle's **canonical home** (adopted 2026-05-20); project roadmaps reference it, they do not re-host it.

**Audience.** Agents and humans contributing to heddle and downstream projects. Read at the start of any session that touches design choices about structure, naming, regularity of code shape. **Not** for feature-scope or capability decisions.

**Origin.** Articulated 2026-05-20 across multiple project-Claude + `heddle-architect` + advisor sessions, while working through the `wire-envelope-base-specialization` redesign (in the originating project's roadmap). The principle was *the reason* a particular design override (full reach in `WireEnvelope` despite the IP-header-analogy collapse) was lockable; surfacing the principle was inseparable from making that call. That redesign is the worked example to refer to when applying the principle. The principle is *itself* a clean-slate move: it identifies a category of design pressure (irregularities compounding at solo + AI scale) that conventional software-development wisdom hasn't yet calibrated for, and adopts a discipline tuned to today's conditions rather than yesterday's.

---

## The principle

> Under bounded vigilance and while breakage is cheap, default to the *reversible* error (refactor now) over the *irreversible* one (foreclosure into forced, compounding redundancy). Trigger on foreclosure risk — demonstrated by **N ≥ 2 present redundant call sites**, not projected drift — not taste. Instrument the rule so applying it doesn't itself require the vigilance it's compensating for. The default *inverts* when "free to break" expires — and it expires the moment a durable consumer **beyond your one-session reach** depends on the shape: an external adopter you can't reach in one session; a persistent event log **with real stored instances** you can't migrate in one session; or an SDK schema **vendored to a consumer you don't control**. A consumer you *do* control and can rewrite in one session — an owner-controlled SDK, an empty or simulation-only log — does **not** trigger inversion; that carve-out is part of the rule, not an exception to it.

This supersedes earlier phrasings ("design as if onboarding the next agent"; "if I'd design it differently today, fix it now") that fired on taste and stated no limits.

---

## Foundation — why this is a bet, and why it's sound

### Rules-over-discretion under bounded vigilance

A perfectly sharp operator would refactor *if/when needed* and catch every foreclosure window with pure discretion, paying no standing burden. The owner does not trust himself — *or* an LLM session — to be that sharp every time. So adopt a standing default that doesn't depend on being sharp every time.

Same logic as checklists, defaults, fiscal rules: trade some agility for failure-mode predictability when attention is the scarce resource. This reframes earlier review rounds that graded the principle on *structural justification*: the real justification is **policy design under unreliable attention**.

### Reversible-vs-irreversible precommitment

Under "free to break," acting-now converts an *irreversible* error (miss the foreclosure window → permanent forced redundancy) into a *reversible* one (over-unify on false-DRY → split back at bounded cost). Since vigilance can't reliably avoid *both*, precommit to the reversible failure mode.

### Compounding is *structural*, not cognitive

This is the load-bearing clarification. The compounding the principle guards against is **structural-redundancy / foreclosure**, not "the per-session adult-learner read-cost." Specifically:

- Once foreclosed, "duplicate X in a second place for historical reasons" becomes a forced rule.
- That rule **multiplies** across all future work touching the concept.
- New dependencies and contribs form *on* the split, **self-propagating** the irregularity.
- It is **irreversible** at solo + AI scale: cleaning up later requires migrating all the new dependents too.

**Anchoring/documentation bounds only the *cognitive* re-learning tax — it cannot touch the structural redundancy tax.** Writing "we duplicate X for history" into an anchor *codifies* the redundancy, it doesn't cure it. This is why Leg (a) below is the load-bearing one, not the read-cost leg.

---

## Domain of validity — where the principle does NOT apply

### Durable-consumer inversion (the hard stop)

The default **inverts** to conservatism when "free to break" expires. It expires the moment a durable consumer **beyond your one-session reach** depends on the shape:

- An external adopter you can't reach in one session.
- A persistent event log **with real stored instances** you can't migrate in one session. (An empty or simulation-only log does not count.)
- An SDK schema **vendored to a consumer you don't control**. (A sha256-pinned `manifest.json` entry / regenerated `.NET`/Swift code that *you* own and can re-vendor in one session does not count — re-vendoring is the one-session refactor.)

The qualifier is the rule, not an exception: durability alone doesn't trigger inversion — durability **beyond your one-session reach** does. Once crossed, both failure modes are expensive — refactor cost is no longer bounded by one session, and reversal requires data migration or coordinated updates to consumers you can't rewrite yourself. The reversible-error advantage disappears; the principle stops favoring action and favors deliberation.

### Scope discipline

The principle governs **design shape** (irregularities, naming, structure). It does NOT govern:

- Feature scope or capability additions ("I'd add this if I were designing today" is a license to *grow*, not redesign).
- Cosmetic preferences absent foreclosure risk.
- Aesthetic uniformity for its own sake.

### Cost ceiling

The principle's discount on refactor cost applies inside the **one-session reviewer-verifiable** boundary. A multi-session migration is back in ordinary break-cost territory; the discount doesn't apply. AI authoring is cheap; AI-assisted human verification is the actual constraint.

### Audience boundary

The principle presumes the no-external-uncontrolled-consumers regime. Once heddle has downstream consumers it can't reach in one session, the unbounded-tax side of the bet shrinks, and the principle weakens regardless of whether a specific durable-consumer trigger has fired.

---

## Guardrails (the conditions that make adoption disciplined)

### Guardrail 1 — Written justification on every clean-slate change

**The load-bearing instrumentation.** Every change citing the clean-slate principle MUST attach a CHANGELOG-tagged justification naming:

(i) The **irregularity** being eliminated.
(ii) Which of *today's* design parameters wouldn't reproduce it.
(iii) An assertion the change is **reviewer-verifiable in one session** — not just agent-authorable.

The justification is the queryable evidence that turns a self-licensing rule into auditable practice. Without it the principle becomes "I think we should refactor" with extra steps. The CHANGELOG tag (`clean-slate`) is what makes the audit pipeline mechanical.

### Guardrail 2 — Foreclosure risk = N ≥ 2 present redundant call sites

The trigger is *foreclosure*, not *taste*. Demonstrated by **N ≥ 2 present redundant call sites** for the structure in question — not projected accretion, not "we'll regret this later."

Projected drift with zero present duplicates is taste rebranded with urgency. This guardrail turns the trigger into a grep.

### Guardrail 3 — Durable-consumer-beyond-reach = the hard stop

When a durable consumer **beyond your one-session reach** depends on the shape — an external adopter, a log with real stored instances, or an SDK schema vendored to a consumer you don't control — the default **inverts** to conservatism. The reversibility logic that makes the principle sound no longer holds. Do not cite the principle to justify changes past this line. (Durability you *do* control and can rewrite in one session — an owner-controlled SDK, an empty/simulation-only log — has not crossed the line.)

### Guardrail 4 — Philosophy weight, never invariant weight

The principle lives at PHILOSOPHY / advisory weight in this doc, **not** as an invariant. As philosophy it stays itself walk-back-able (drop it later at bounded cost). As an invariant, dropping it would be a breaking governance change — the exact failure mode the principle exists to avoid in code, smuggled into doctrine.

---

## Hypothesis legs — honest verdict

### Leg (a) — Structural-redundancy / foreclosure compounding (load-bearing)

Multiplicative, self-propagating, irreversible. **NOT bounded by anchoring.** This is the actual load-bearing reason — the first review round under-modeled it as "read-cost."

### Leg (b) — "Bounded by AI capability" (half-true)

*Authoring* cost shrinks with AI. *Total* cost is bounded by **reviewer-verifiable scope** (a human bottleneck), which doesn't shrink at the same rate. Valid only inside the one-session verification boundary. Don't claim the principle "scales with AI."

### Leg (c) — Adult-learner cognitive re-payment (solid but bounded)

The per-session "this looks weird because of [historical reason X]" tax is real, but **bounded by anchoring**: a documented irregularity is a one-time read for any session that loads the doc. Real, not the strongest leg.

---

## The regress — named honestly

The principle exists to compensate for unreliable vigilance, but it can only **relocate** residual vigilance, not eliminate it — to the **real-vs-apparent-redundancy** judgment. That judgment is *harder* for a cold LLM session than "should I refactor this?" — deciding whether two structures are "one concept" often requires understanding things like CAS, replay, dedup, or three ordering authorities. Exactly the cold-start knowledge the principle exists to route around.

**Honest read:** the principle is a vigilance *reduction* only if you (i) concentrate scarce sharpness on the relocated judgment, AND (ii) use the durable-consumer guardrail to backstop misjudgment. Without the guardrail, the relocation is a downgrade.

---

## How to apply

1. **Spot the candidate.** Two structures that look like "one concept implemented twice" with **present** (not projected) redundancy.
2. **Verify N ≥ 2 redundant call sites.** Grep, not vibe.
3. **Check durable-consumer status.** Is any shape in question persisted, vendored, or external-consumer-dependent? If yes, **STOP** — inversion fired; default to conservatism.
4. **Judge real-vs-apparent redundancy.** This is where the residual vigilance lives. Apparent redundancy (two things that *look* similar but mean different things) does NOT trigger; real redundancy (two things that *are* the same concept) does.
5. **Write the Guardrail-1 justification BEFORE the refactor**, naming irregularity, today's-parameter mismatch, and one-session verifiability.
6. **Tag the CHANGELOG entry** with `clean-slate` for queryability.
7. **Verify the refactor in one session.** If it splits across multiple, the cost-ceiling guardrail fired — re-scope or split the change.

---

## Tripwires — going wrong (grep-able)

Run these checks across maintenance cycles. Any one firing is a signal the principle is being misapplied:

1. Same area clean-slated **twice within ~2 maintenance cycles** (audit ↔ cycle topic strings).
2. An invariant **added-then-re-edited within ~2 cycles** (`git log -p heddle/docs/DESIGN_INVARIANTS.md`).
3. A "shape" PR whose **test diff carries non-rename behavior changes** (regularity work shouldn't change behavior).
4. **Contract-boundary SDK regens / paired PRs above baseline** (`heddle-sdk/schemas/manifest.json` history).
5. CHANGELOG `Changed` + `Removed` entries **outrunning `Added`** entries.
6. An **audit topic recurring across cycles** citing regularity.

---

## Success metric — paying off (also grep-able)

A measurable **decline over cycles in prefatory "this looks weird because of historical reason X"** framing in session-starters, audits, and subagent prompts. That caveat *is* the per-session adult-learner tax; if it doesn't drop, the principle isn't earning its cost — independent of whether a tripwire fires.

---

## Interactions with existing philosophy and invariants

- **Reinforces `PHILOSOPHY.md §3` (progressive disclosure).** One regular envelope family, fewer "tasks use one shape, events use another" exceptions for new sessions to absorb.
- **Tensions with `DESIGN_INVARIANTS.md #14`.** The principle's first invariant-layer act is to *soften* a red line (admitting `InMemoryBus` as a runtime). The downstream write-on-shutdown work is the test of whether that softening was disciplined or the principle's first erosion; gate it on a Guardrail-1 written justification.
- **Sits *under* `PHILOSOPHY.md §1` (SMB-first).** Never cite the principle to justify hyperscaler-shaped uniformity at the cost of the lightweight end of the audience span.
- **Keeps the typed-contract net (`PHILOSOPHY.md §6`).** The composition mechanism's opaque `payload: dict` is fine *if* the two-step validation stays genuinely two-step. The principle does not license relaxing typing.

---

## Worked example

The `wire-envelope-base-specialization` redesign (in the originating project's roadmap: the v4 design doc + the v2/v3/v4 feedback files) is the first explicit application:

- **The candidate:** two parallel envelope families (`TaskMessage`/`TaskResult` and `EventEnvelope`/`CommandMessage`/`RejectionEnvelope`) carrying message envelope concerns redundantly.
- **The N ≥ 2 check:** more than 24 construction sites distributed across both families.
- **The durable-consumer check:** the events-side shapes are *durable* (persisted to JetStream, vendored to `heddle-sdk` with sha256-pinned schemas) — but by Guardrail 3's qualifier, durability alone isn't the trigger; durability **beyond one-session reach** is. Here the log is empty/simulation-only (no real installed base, contrib.events pre-freeze) and the SDK is owner-controlled and re-vendorable in one session. So the trigger has **not** fired — it names the *future* boundary, once a real event log accrues or a consumer leaves the owner's control.
- **The judgment:** the redundancy is real-not-apparent (one concept: "message with identity, timestamps, origin, payload-slot"), and the owner accepts the large refactor scope at this stage of the project's life.
- **The justification:** structural-redundancy elimination before the durable-consumer trigger fires — buying out the foreclosure window while it remains open.

This is the worked example to refer to when the principle's application to a future decision is unclear. Four reviewer rounds (v2-feedback, v3-feedback-round-1, v3-feedback-round-2 on the principle itself, owner's §0 rescope) document the sharpening process from a loose initial statement to the §1 form above.

---

## Provenance

- Articulated and sharpened: 2026-05-20, across project-Claude + `heddle-architect` + advisor sessions.
- Round 1 review of the inline principle: SOUND-WITH-LIMITS verdict; identified that the principle was carrying Decision 1 alone with no structural backup.
- Round 2 review of the sharpened principle: durable-consumer counter decisive (reversibility leg fails for durable shapes); broadened inversion trigger to include the event log; N ≥ 2 sites foreclosure test added.
- Owner's §0 rescope: the breakage window is currently still open across the whole stack; the "free to break already expired" finding correctly names the *future* trigger.
- Verified in code at articulation time: `core/messages.py` (`TaskMessage`), `contrib/events/envelopes.py` (`EventEnvelope`, persisted+replayed), `heddle-sdk/schemas/manifest.json` (schemas sha256-pinned), `DESIGN_INVARIANTS.md` (#14, #22).
- This doc adopted as the principle's durable home: 2026-05-20, alongside the wire-envelope v4 design and its implementation plan.
