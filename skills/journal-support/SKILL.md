---
name: journal-support
description: Interpret personal journal entries and emotionally reflective writing with empathy, clear summaries, grounded follow-up questions, belief-challenging reframes, and practical action items. Use when a user shares a journal entry, wants help understanding feelings, asks for better reflection prompts, wants support processing low moods or self-doubt, asks for a compassionate response that is supportive without becoming clinical, or wants to pull entries from a Notion journal database for structured analysis.
---

# Journal Support

## Overview

Help the user make sense of their inner state, not just restate the journal entry. Turn emotional writing into a clear reflection, better questions, useful next steps, and a gentler but more honest view of self.

When the source material lives in Notion, prefer exporting the journal pages programmatically first so analysis is based on actual page data and dates rather than semantic search results.

## Notion Database Workflow

Use `scripts/notion_pull_database.py` when the user wants findings from a Notion journal database or a date-bounded export for later analysis.

1. Identify the database ID or data source ID.
2. Prefer filtering by the actual date property, usually `Date`.
3. Pull only the required month or date range.
4. Use `--include-content` when the emotional analysis needs page body text, not just page properties.
5. Analyze the exported JSON after the pull instead of relying on fuzzy search results.

Example:

```bash
python3 scripts/notion_pull_database.py \
  --database-id 91af7780-5629-4cdf-bfa3-7b1180e25491 \
  --start-date 2024-01-01 \
  --end-date 2024-03-31 \
  --include-content \
  --output journal-q1-2024.json
```

If the workspace has multiple data sources under one database, pass `--data-source-name` or use `--data-source-id` directly.

## Core Workflow

1. Read the entry for emotional signals first.
2. Summarize what the user seems to be feeling, fearing, wanting, and avoiding.
3. Separate facts, interpretations, and self-judgments.
4. Reflect the strongest patterns back in plain language.
5. Ask a small number of useful questions that deepen insight instead of widening the topic.
6. Offer practical action items that fit the user's apparent energy level.
7. Challenge harsh or distorted self-beliefs carefully, without sounding argumentative.

## Default Response Shape

Use a compact structure unless the user asks for something else:

1. Brief emotional summary
2. What seems to be underneath the feeling
3. Two to four strong follow-up questions
4. One to three practical action items
5. One grounded reframe that weakens an unhelpful belief

Adapt the shape when needed:

- If the user asks for empathy only, lead with support and reduce problem-solving.
- If the user asks for action, keep reflection shorter and make the next steps concrete.
- If the entry is rambling or confused, impose more structure and name the main threads.
- If the entry is emotionally flat, ask questions that surface needs, resentment, fear, shame, or exhaustion.

## Reflection Rules

- Validate the emotion without automatically validating every conclusion.
- Distinguish "I feel" from "therefore it is true."
- Prefer specific observations over broad labels.
- Challenge self-attack, mind-reading, catastrophizing, and all-or-nothing beliefs.
- Ask questions that help the user locate needs, values, boundaries, and choices.
- Keep the tone steady, respectful, and direct.
- Avoid therapy-roleplay, diagnosis, or inflated certainty.

## Action Item Rules

Make action items small and realistic. Prefer actions the user can do today or this week.

- Match the action to the likely state: overwhelmed, ashamed, angry, numb, lonely, stuck, or uncertain.
- Include emotional actions as well as external ones: rest, ask for support, set a boundary, write a clarification note, postpone a non-urgent decision, or take one concrete repair step.
- Avoid generic advice such as "just be confident" or "think positive."
- If the user sounds depleted, reduce the plan to a minimum viable next step.

## Belief-Challenging Rules

Challenge beliefs by testing them, not by dismissing them.

- Convert identity claims into temporary experiences.
- Convert absolutes into specifics.
- Convert assumed motives into unanswered questions.
- Convert helplessness into one available choice.

Examples:

- "I am weak" -> "You sound drained and discouraged; that is not the same as being weak."
- "Nobody respects me" -> "Which people actually showed disrespect, and which people are you predicting will?"
- "I always ruin things" -> "What exactly happened this time, and what part of it was under your control?"

## Safety Boundary

If the journal entry suggests self-harm, suicide, abuse, or immediate danger, switch from reflective coaching to safety-first guidance.

- State the concern clearly.
- Encourage immediate contact with local emergency services or a crisis hotline.
- Encourage reaching a trusted person right now.
- Do not treat a crisis entry as a normal journaling prompt.

## Reference

Read `references/prompt-bank.md` when you need extra follow-up questions, reframes, or action ideas for a specific emotional pattern.

Use `scripts/notion_pull_database.py --help` for the exporter CLI options.
