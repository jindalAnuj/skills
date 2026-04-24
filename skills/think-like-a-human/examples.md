# Think Like a Human — Worked Examples

Three complete walkthroughs showing how the 5-phase process plays out for
different goal types.

---

## Example 1 — Learning VFX / AI Video Generation

**User goal:** "I want to learn VFX and AI video generation."

---

### Phase 1 — Clarify

Questions asked:

1. "Are you coming from a design/video editing background, or is this completely new territory?"
2. "What's the end deliverable — short films, YouTube content, client work, or just personal learning?"
3. "Are you focused on AI-generated video (Sora, Runway, Kling) or traditional VFX compositing (After Effects, Nuke)?"

User answers: Complete beginner. Wants to create cinematic short clips. Interested in AI tools primarily.

---

### Phase 2 — Expert Decomposition

```
Stage 1 — Visual literacy
  What: Understanding composition, color, lighting, and camera language
  Why first: AI tools amplify whatever taste you bring in. Without visual
             literacy, outputs look random even with great prompts.
  Done when: You can look at a reference frame and name what makes it work.

Stage 2 — Prompt engineering for visuals
  What: Writing prompts that reliably produce the shot you intend
  Why first: All AI video tools are prompt-driven. This is the core skill.
  Done when: You can reproduce a specific visual style 3 times in a row.

Stage 3 — Tool ecosystem
  What: Learning Runway Gen-4, Kling, Sora (text-to-video); ControlNet /
        IP-Adapter for image-to-video; Topaz for upscaling
  Why first: Now that you can describe what you want, you need the right
             tool for each use case.
  Done when: You know which tool to reach for given a brief.

Stage 4 — Shot assembly and editing
  What: Cutting AI-generated clips into a coherent sequence in DaVinci
        Resolve or Premiere; handling inconsistency between shots
  Why first: Individual great shots don't make a film. Assembly is where
             most beginners get stuck.
  Done when: You can produce a 30-second sequence that feels intentional.

Stage 5 — Sound design and music
  What: Adding audio that matches the visual tone (ElevenLabs, Suno,
        royalty-free libraries)
  Why first: 50% of cinematic impact is sound. Silence kills otherwise
             strong visual work.
  Done when: A finished clip with synced audio that you'd share publicly.
```

---

### Phase 3 — Knowledge Gap Map

**Foundational knowledge**
- Color theory basics (hue, saturation, value, contrast)
- Shot types and camera language (wide, medium, close-up, Dutch angle)
- What makes motion cinematic vs. amateur

**Tooling & ecosystem**
- Runway Gen-4, Kling 2.0, Sora, Pika — differences and strengths
- DaVinci Resolve (free, industry standard for color grading)
- Topaz Video AI for upscaling/frame interpolation
- ElevenLabs for voiceover, Suno/Udio for music

**Process & workflow**
- Reference gathering before prompting (mood boards)
- Iterating on a seed image before generating video
- How to handle inconsistent faces/characters across shots
- Export settings for social vs. film delivery

**Unknown unknowns**
- AI video has a 4–10 second limit per clip — long sequences require many shots stitched together
- "Prompt drift" across shots makes characters inconsistent; techniques exist to fix this
- Generation costs real money at volume; budgeting matters
- Style guides and LoRAs can lock a visual look across generations

---

### Phase 4 — Phased Roadmap

```
Phase 1 — Visual Foundation
  Goal: Develop enough visual literacy to judge and describe what you want
  Activities:
    - Study 20 reference shots from films you admire, name what works
    - Complete a free color theory crash course (Canva, YouTube)
    - Build a reference mood board for your first project
  Effort: 1 week, 1–2 hours/day
  Resources: YouTube "Film Riot", Canva Design School, Pinterest for refs
  Exit: Can describe a target frame in words a stranger could reconstruct

Phase 2 — Prompt Craft
  Goal: Write prompts that produce predictable visual results
  Activities:
    - Study the visual-ai-prompting skill (already available in this repo)
    - Generate 50 test images/videos, iterate on each until the output
      matches your intent
    - Build a personal prompt library of working patterns
  Effort: 1–2 weeks
  Resources: visual-ai-prompting skill, Runway/Kling free tiers
  Exit: 3 prompts that reliably reproduce a specific style

Phase 3 — Tool Mastery
  Goal: Know which tool to use for which brief
  Activities:
    - Try Runway Gen-4, Kling 2.0, and Pika on the same brief
    - Learn Topaz for upscaling a low-res clip
    - Document your tool comparison in a personal cheat-sheet
  Effort: 1–2 weeks
  Resources: Official docs, r/aivideo, community Discord servers
  Exit: Personal tool selection guide completed

Phase 4 — Assembly
  Goal: Produce a 30-second cinematic sequence
  Activities:
    - Learn DaVinci Resolve basics (cut page, color page)
    - Stitch 5–8 AI clips into a coherent sequence
    - Add a basic color grade
  Effort: 2 weeks
  Resources: DaVinci Resolve free, YouTube "Casey Faris"
  Exit: 30-second clip ready to share

Phase 5 — Audio & Polish
  Goal: Complete a shareable short with full audio
  Activities:
    - Add music via Suno or a royalty-free library
    - Add optional voiceover via ElevenLabs
    - Export and share for feedback
  Effort: 1 week
  Resources: Suno.com, ElevenLabs free tier
  Exit: Shared publicly and received at least 3 pieces of feedback
```

---

### Phase 5 — Decision Handoff

```
What would you like to do next?

A) Deep-dive Phase 1 (Visual Foundation) — I'll give you a structured
   daily plan for the first week
B) Create a sub-skill for VFX prompt engineering — I'll draft a
   SKILL.md extending the visual-ai-prompting skill
C) Start Phase 2 (Prompt Craft) now — I'll guide you through your
   first 10 test generations
```

---

## Example 2 — Building a Game (Non-Developer)

**User goal:** "I want to build a game. I have an idea but I'm not a developer."

---

### Phase 1 — Clarify

Questions asked:

1. "What type of game — 2D platformer, RPG, puzzle, mobile casual, narrative?"
2. "Is the goal to ship a real product, build a portfolio piece, or learn game dev as a skill?"
3. "Have you used any game engines before (Unity, Godot, GameMaker) or is this truly from zero?"

User answers: 2D pixel RPG. Wants to ship on itch.io. Never touched a game engine.

---

### Phase 2 — Expert Decomposition

```
Stage 1 — Game design fundamentals
  What: Core loop, player motivation, progression systems, scope control
  Why first: Most first games fail because the scope is uncontrolled.
             Design on paper before touching any tool.
  Done when: One-page game design document (GDD) written.

Stage 2 — Engine basics (Godot)
  What: Scene system, nodes, signals, GDScript basics
  Why first: Godot is free, beginner-friendly, and ideal for 2D.
             Understanding the engine's mental model unlocks everything else.
  Done when: A character moves on screen, collects an item, and a score
             increments.

Stage 3 — Art pipeline
  What: Creating or sourcing pixel art assets, animation basics,
        tilesets, UI sprites
  Why first: Art takes longer than beginners expect. Starting early
             prevents a blank-screen crisis mid-development.
  Done when: Main character and one tileset are complete and in-engine.

Stage 4 — Core systems
  What: Combat, inventory, dialogue, save system — only what the GDD specifies
  Why first: Build only what's in scope. Every extra system doubles timeline.
  Done when: The core loop is playable end-to-end.

Stage 5 — Polish and ship
  What: Sound effects, music, playtesting, bug fixing, itch.io page
  Why first: Shipping something small beats perfecting something unfinished.
  Done when: Live on itch.io and shared with 10 people.
```

---

### Phase 3 — Knowledge Gap Map

**Foundational knowledge**
- What a core loop is and why it matters
- Scope creep — why games never ship and how to prevent it
- Basic programming concepts (variables, conditionals, functions) — GDScript is gentle but not zero

**Tooling & ecosystem**
- Godot 4 (engine), Aseprite (pixel art), BFXR/sfxr (sound effects), itch.io (distribution)
- Git for version control (even solo — saves games from catastrophic loss)

**Process & workflow**
- Vertical slice first: one complete level before building more
- Playtesting early, not at the end
- Asset packs (itch.io free assets) to unblock when art is a bottleneck

**Unknown unknowns**
- "Programmer art" is fine for prototyping — don't block on perfect assets
- Godot's scene/node model is fundamentally different from thinking in files
- Audio is 30–40% of perceived polish; many beginners skip it
- The itch.io page design affects downloads as much as the game itself

---

### Phase 4 — Phased Roadmap

```
Phase 1 — Design on Paper
  Goal: One-page GDD with a locked, shippable scope
  Activities:
    - Define core loop in one sentence
    - List features: must-have vs. cut if time runs out
    - Sketch 3 screens by hand
  Effort: 3–5 days
  Resources: "The GDD Template" (free), watch 1 GDC talk on scope
  Exit: GDD signed off, scope frozen

Phase 2 — Engine Foundations
  Goal: Move a character, collect an item, display score
  Activities:
    - Complete Godot official beginner tutorial
    - Implement the mechanic from your GDD (not the tutorial's mechanic)
  Effort: 2 weeks
  Resources: Godot docs, GDQuest YouTube
  Exit: Your mechanic works in a blank scene

Phase 3 — Art & Assets
  Goal: Main character + one environment tileset in-engine
  Activities:
    - Learn Aseprite basics (4-hour YouTube course)
    - Draw or source main character + idle/walk/attack frames
    - Build one tileset
  Effort: 2–3 weeks
  Resources: Aseprite ($20), itch.io free asset packs as reference
  Exit: Character walks on a tiled floor in Godot

Phase 4 — Core Loop Playable
  Goal: Full core loop working end-to-end
  Activities:
    - Implement all must-have features from GDD
    - First playtest with someone other than yourself
    - Cut anything not in the must-have list
  Effort: 3–4 weeks
  Resources: Godot docs, r/godot for stuck moments
  Exit: Playtest feedback collected, loop is fun

Phase 5 — Ship
  Goal: Live on itch.io
  Activities:
    - Add SFX and music (BFXR + free music)
    - Fix top 5 playtest bugs
    - Build itch.io page with screenshots and a GIF
    - Export and publish
  Effort: 1 week
  Resources: itch.io upload guide
  Exit: URL shared with 10 people
```

---

## Example 3 — Learning Marketing (Non-Marketer)

**User goal:** "I want to learn marketing. I have a product but no idea how to market it."

---

### Phase 1 — Clarify

Questions asked:

1. "What's the product and who is the target customer? (B2B or B2C, niche or broad)"
2. "Do you have any existing audience, email list, or social following — even small?"
3. "What's the primary goal — first paying customers, growing an audience, or brand awareness?"

User answers: B2C app, target is indie creators, no audience. Goal: first 100 paying customers.

---

### Phase 2 — Expert Decomposition

```
Stage 1 — Customer clarity
  What: Defining exactly who the customer is, what pain they have,
        and what they already try to solve it with
  Why first: Every marketing tactic fails if you don't know who you're
             talking to. Messaging before clarity is noise.
  Done when: A one-paragraph "customer profile" that 3 real people
             in the target agree describes them.

Stage 2 — Message-market fit
  What: Crafting the core message: what the product does, for whom,
        and why it beats the alternative — in one sentence
  Why first: Until the message is sharp, no channel will work well.
             Ads, content, cold email — all need a sharp hook.
  Done when: A headline that gets a "yes, that's my problem" reaction
             from 5 target customers.

Stage 3 — Channel selection
  What: Choosing 1–2 channels where the target customer already spends
        time (not all channels — one or two done well)
  Why first: Spreading across 6 channels at zero budget is the #1
             mistake beginners make.
  Done when: Two channels selected with a written rationale.

Stage 4 — Content and distribution engine
  What: Building a repeatable system to publish content or outreach
        on the chosen channels consistently
  Why first: One-off posts don't compound. A system does.
  Done when: 30-day content calendar exists and first 10 posts are live.

Stage 5 — Conversion and retention
  What: Landing page copy, onboarding, email sequences — turning
        visitors into paying customers and keeping them
  Why first: Traffic without conversion is vanity. Fix the funnel
             before scaling the top.
  Done when: Conversion rate measured on 100 visitors.
```

---

### Phase 3 — Knowledge Gap Map

**Foundational knowledge**
- Jobs-to-be-done framework (why people buy)
- The difference between awareness, consideration, and conversion
- What "positioning" means and why it matters before any tactic

**Tooling & ecosystem**
- Beehiiv or ConvertKit (email list — the one asset you own)
- Buffer or Typefully (social scheduling)
- Carrd or Framer (fast landing pages)
- Hotjar or Microsoft Clarity (free session recording to see where people drop off)

**Process & workflow**
- How to run a customer interview (5 questions that reveal real pain)
- How to write copy using the PAS formula (Problem–Agitate–Solution)
- How to measure what's working: CAC, conversion rate, email open rate

**Unknown unknowns**
- "Build it and they will come" is the biggest myth in product marketing
- Distribution > product quality for the first 1,000 customers
- Paid ads require a proven message first — burning budget on untested copy is common
- Community-led growth (indie hacker forums, Reddit, Discord) often outperforms paid for early-stage B2C
- An email list of 500 engaged subscribers beats 50,000 social followers for conversions

---

### Phase 4 — Phased Roadmap

```
Phase 1 — Customer Clarity
  Goal: A sharp customer profile validated by real people
  Activities:
    - Conduct 5 customer interviews (30 min each)
    - Write a one-paragraph customer profile
    - Identify the #1 pain your product solves
  Effort: 1 week
  Resources: "The Mom Test" (book, ~3 hours), Calendly for scheduling
  Exit: Profile reviewed and agreed by 3 people in the target segment

Phase 2 — Message Craft
  Goal: One headline sentence that gets "yes, that's me" reactions
  Activities:
    - Write 10 headline variants using PAS formula
    - Test top 3 in conversations or a small survey
    - Finalize landing page headline and subheadline
  Effort: 1 week
  Resources: Copywriting basics (CopyHackers free articles), Carrd
  Exit: Landing page live with the winning message

Phase 3 — Channel Selection
  Goal: Two channels chosen with rationale and 30-day plan
  Activities:
    - Research where indie creators already hang out online
    - Join 3 communities and observe before posting
    - Choose 2 channels: one owned (email), one borrowed (Reddit/Twitter/Discord)
  Effort: 3–5 days
  Resources: SparkToro for audience research (free tier)
  Exit: Channel strategy doc written, accounts set up

Phase 4 — Content Engine
  Goal: 30-day content calendar executed, first 10 pieces live
  Activities:
    - Create content calendar for chosen channels
    - Publish 10 posts / pieces of value-first content
    - Engage in 3 community threads per week (not promotional)
  Effort: 3–4 weeks (ongoing)
  Resources: Typefully, Buffer free tier
  Exit: 10 pieces live, first organic traffic measured

Phase 5 — Conversion Funnel
  Goal: Measure and improve conversion from visitor to paying customer
  Activities:
    - Install Clarity or Hotjar on landing page
    - Set up a 3-email welcome sequence for new sign-ups
    - Run 100 visitors through the funnel and record conversion rate
  Effort: 1 week setup + ongoing measurement
  Resources: Beehiiv (email), Microsoft Clarity (free)
  Exit: Baseline conversion rate established, first 10 paying customers
```

---

### Phase 5 — Decision Handoff

```
What would you like to do next?

A) Deep-dive Phase 1 (Customer Interviews) — I'll give you the exact
   5 questions to ask and how to find people to interview
B) Create a sub-skill for copywriting / message crafting — I'll draft
   a SKILL.md so AI can help you write PAS-formula copy consistently
C) Start Phase 2 (Message Craft) now — I'll workshop your headline
   variants with you right here
```
