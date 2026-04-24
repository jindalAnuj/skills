---
name: think-like-a-human
description: >-
  Structured goal decomposition skill that thinks like a domain expert before
  any execution. Use when the user wants to learn a new skill, build something
  outside their expertise, or asks "how do I start", "I want to learn X",
  "I want to build X", "how do I get into X", or any broad goal that lacks
  a clear execution path. Breaks the goal into a phased roadmap, maps knowledge
  gaps, and hands the human clear decision points — without burning tokens on
  premature execution.
---

# Think Like a Human

## Purpose

Prevent AI from hallucinating a path forward on broad goals. Instead of diving
in, apply the structured thinking a senior human practitioner would use:
clarify → decompose → surface gaps → build roadmap → hand off.

**Output is always a plan, never execution.** The human decides what happens next.

---

## Phase 1 — Clarify Intent

Before anything else, ask **2–3 targeted questions** to narrow the goal.
Do not skip this phase, even if the goal seems clear.

Ask these dimensions (pick the most relevant 2–3):

| Dimension | Example question |
|---|---|
| Current level | "What's your background with X — complete beginner, some exposure, or familiar with adjacent skills?" |
| End deliverable | "What does success look like — a portfolio piece, a live product, a working prototype, a certification?" |
| Timeline / constraint | "Is there a deadline or is this open-ended learning?" |
| Purpose | "Is this for a career change, a side project, personal interest, or a client?" |
| Resources | "Do you have a budget for tools/courses, or are you looking for free paths?" |

Present these as a short conversational list, not a wall of text. Wait for
answers before proceeding to Phase 2.

---

## Phase 2 — Decompose Like an Expert

Reason about the domain the way a **senior practitioner** would outline it —
not a generic AI overview. Ask yourself:

> "If a skilled professional in this domain were mentoring a beginner,
> what would they say are the real stages? What do most beginners skip
> that causes them to fail? What is the non-obvious order of operations?"

Structure the decomposition as **named stages**, each with:
- What it covers
- Why it comes before the next stage
- A concrete signal that this stage is complete ("you know this stage is done when…")

Example format:

```
Stage 1 — [Name]
  What: ...
  Why first: ...
  Done when: ...

Stage 2 — [Name]
  ...
```

Aim for 4–7 stages. More than 7 is usually artificial splitting.

---

## Phase 3 — Knowledge Gap Map

After decomposing the domain, explicitly surface what **this specific user**
likely does not know yet. Categorise gaps into four buckets:

| Bucket | What belongs here |
|---|---|
| **Foundational knowledge** | Concepts the user must understand before any tool makes sense |
| **Tooling & ecosystem** | Software, platforms, libraries, services — and which ones actually matter |
| **Process & workflow** | The how-to: the sequence of steps a practitioner follows day-to-day |
| **Unknown unknowns** | Things beginners don't know they don't know (jargon, hidden complexity, common traps) |

Format this as a concise bullet list per bucket. This map becomes the
input for choosing what sub-skills to create or what to research next.

---

## Phase 4 — Phased Roadmap

Produce a numbered roadmap that maps the stages from Phase 2 onto a
realistic timeline, with:

- **Phase number and name**
- **Goal**: one sentence on what the phase achieves
- **Key activities**: 3–5 concrete things to do
- **Estimated effort**: rough time range (e.g., "1–2 weeks part-time")
- **Resources / sub-skill suggestion**: a recommended resource type or
  the name of a sub-skill that could be created for this phase
- **Exit criteria**: how the human knows the phase is complete

Format:

```
Phase N — [Name]
  Goal: ...
  Activities:
    - ...
  Effort: ...
  Resources: ...
  Exit: ...
```

Keep the roadmap honest. If a phase is genuinely hard, say so.
Do not pad with filler phases.

---

## Phase 5 — Decision Handoff

End **every** think-like-a-human session by presenting the human with
exactly **3 choices**. Do not proceed past this point without a choice.

Standard choices:

```
What would you like to do next?

A) Deep-dive a specific phase — I'll break it down in detail
B) Create a sub-skill for one of the phases — I'll draft the SKILL.md
C) Start executing a phase now — I'll guide you step by step through it
```

Adapt the labels to the actual roadmap (e.g. name the phase). If the
human's answer leads to sub-skill creation, follow the `create-skill`
skill to draft it.

**Do not execute anything until the human has made a choice.**

---

## Anti-patterns to avoid

- Jumping to tools or code before Phase 1 is complete
- Giving a generic "here are 10 steps" list without expert reasoning
- Treating all goals as equally well-defined (always clarify first)
- Skipping the gap map because the roadmap "covers it"
- Offering more than 3 choices at the handoff (causes decision paralysis)

---

## Additional resources

- For worked examples (VFX, game dev, marketing), see [examples.md](examples.md)
