# Design Stance — Universal (all projects)

> Companion to the working method (`hooman-contract.md` + `hooman-assistant`). **Scope:** every project, any language or domain. **Binds:** both Chat and the Executor. **Home:** `references/`. **v0.2 · 2026-06-04.**
>
> This governs *what to build and when*. Language- and domain-specific stances layer on top (e.g. `design-stance-swift.md`).

## The balance

Two failure modes, **equally** to be avoided:

- **Under-engineering / tunnel vision** — pretending domain knowledge doesn't exist; deferring a structure the domain already determines; writing throwaway code when the shape is already knowable from the project's positioning and domain.
- **Over-engineering** — building on speculation; abstracting for "we might want it"; cathedrals on day one.

Throwaway code is a **cost to weigh, not a virtue.** Sometimes it is worth paying — a disposable probe that unblocks a gate. It is never to be *manufactured* when the domain already tells us the shape we will need.

## The certainty process (the spine)

We are rarely certain beforehand. Certainty is reached by a **process**, not assumed:

1. **A candidate emerges.** A structure suggests itself — from the domain / specification, from a standout newer attempt at the same domain (reference implementations), or from our own verified probes.
2. **Investigate / debate.** A candidate does **not** authorize building. It authorizes *running it down*: examine the domain evidence, see how the strongest existing attempts solved it, debate until the threshold is met — or isn't.
3. **Threshold.** **Design-and-name now** if *both*: (i) the domain/spec determines its existence and rough shape *independently of our implementation choices*, **and** (ii) a credible reference or our own verified probes already exhibit it. **Defer** only if the shape depends on a tradeoff we can evaluate solely by writing concrete code.
4. **When deferring, name it.** Record the candidate *and the specific reason it is deferred*, and what would change the answer — so it is a parked decision, not a forgotten one.

**The root error:** silent-defer and silent-build are the *same* mistake — an **un-adjudicated candidate**. The discipline is to *adjudicate*, never to default in either direction.

## The environment is a candidate, not a constraint

The installed toolchain — compilers, formatters, linters, CLIs, package and toolchain managers, the OS utilities a project leans on — is a **candidate surface**, subject to the same certainty process as any structural choice, not a fixed given to be accommodated. The common reflex (accept what is installed and build within it) is a reasonable adaptation to the *typical* case, where a separate authority owns the toolchain and "install something cleaner" is outside the operator's hands. That reflex **misfires when the operator controls the environment and is there to modernize.**

Separate two duties:

- **Surfacing is unconditional.** Never treat the installed environment as self-justifying. When a newer or cleaner tool or version would be better *for the case at hand*, name it — as a decision point, with its tradeoff — the same way Chat surfaces a structural candidate.
- **Adoption follows control.** Where the operator owns the environment, a surfaced improvement is adoptable; where a separate authority owns it, the improvement is surfaced as information, not pretended away. Surfacing does not depend on being able to act; the duty is to make the better option *visible*.

The governor is the certainty process, exactly as for language constructs: **better for the case, not newest-for-its-own-sake** — reflexive toolchain churn is the over-engineering failure in a different costume. Two costs pull the other way and must be weighed: a continuously shifting environment fights **re-entry** (returning to a toolchain that moved under you) and **fluency** (learning needs a stable surface). So modernize in **deliberate, discrete moves** — adopt, record the decision where re-entry will find it, let it settle — not continuously. Surface always; adopt deliberately.

A claim that a newer version or tool exists must be **verified current, not recalled** — releases and versions are precisely where stale knowledge misleads. (For a language toolchain, this is the language stance's version-honesty rule, applied to the environment.)

## Scouting — who watches for candidates

- **Chat** surfaces emerging candidates *as a design forms*, names them, and brings them to adjudication. Chat challenges any design that under-uses what is available, or that defers something domain-certain — at the moment it forms, not in hindsight.
- **The Executor** includes, in every reconnaissance (R1) output, a section naming **structural and environment candidates it noticed and whether each meets the threshold** — structures the domain implies, *and* tooling improvements observed while working (a newer or cleaner toolchain, formatter, build or package tool), per *The environment is a candidate, not a constraint*. An R1 that touches the environment **evaluates** what is installed, rather than merely accepting it. The Executor is an active scout, not only an implementer of settled decisions.

## When a candidate is adjudicated

The outcome — *design-and-name* or *defer-with-reason* — is recorded where a cold re-entry will find it (decisions log, parking lot, or the roadmap track), phrased so the reasoning survives without the conversation that produced it.

## Why this exists

Unstated principles cannot be checked. Past misalignment traced to principles **held but never written down** — a design choice or two that should have been named earlier slipped through, because neither party could check a design against a rule that lived only in someone's head. This document makes the rules checkable by both parties.
