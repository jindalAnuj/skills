# Visual AI Prompting — Templates & Examples

## Template 1: Cinematic Portrait

```
[GENDER/AGE/ETHNICITY] [EXPRESSION] [PHYSICAL DETAIL],
[SETTING] at [TIME OF DAY],
[LIGHTING TYPE] from [DIRECTION],
[SHOT TYPE], [FOCAL LENGTH] lens, [APERTURE] aperture,
[COLOR GRADE], [FILM STOCK],
cinematic, --ar 4:5 --style raw
```

**Example:**
```
A 40-year-old Japanese man with tired but determined eyes and a faint scar on his jaw,
standing in a rain-soaked train station at 3am,
harsh fluorescent overhead light from directly above creating deep under-eye shadows,
medium close-up, 85mm lens, f/1.8 aperture,
cool blue desaturated grade, Kodak Vision3 film grain,
cinematic --ar 4:5 --style raw
```

---

## Template 2: Epic Landscape / Establishing Shot

```
[LOCATION DESCRIPTION], [TIME + WEATHER],
[ATMOSPHERIC EFFECTS],
[CAMERA POSITION + ANGLE],
[SUBJECT placement if any],
[COLOR PALETTE], [FILM REFERENCE],
wide shot, cinematic, --ar 21:9
```

**Example:**
```
A crumbling gothic cathedral on a remote cliff overlooking a stormy ocean, golden hour with approaching storm,
god rays breaking through dark clouds, waves crashing against the cliff base,
drone shot from far behind and slightly above, tilting down toward the cathedral,
single hooded figure standing in the entrance archway,
warm gold against cold grey-blue storm, Ridley Scott cinematic,
wide shot, cinematic --ar 21:9
```

---

## Template 3: Action / VFX Shot

```
[ACTION SUBJECT] [PERFORMING ACTION] in [ENVIRONMENT],
[VFX ELEMENTS] with [PHYSICAL BEHAVIOR],
[CAMERA ANGLE + MOVEMENT],
[LIGHTING from VFX source],
slow-motion, [FPS if relevant], cinematic VFX quality
```

**Example:**
```
A superhero landing hard on a city rooftop at night,
massive shockwave pulse rippling outward from impact point, cracking concrete,
low angle dutch tilt looking up at figure, camera shake on impact,
chest armor glowing blue illuminating dust cloud from below,
slow-motion 120fps, cinematic VFX quality, Zack Snyder style
```

---

## Template 4: Video Scene (5 Layers)

```
SCENE:    [Environment, time, weather]
SUBJECT:  [Who + what they are doing + HOW they move]
CAMERA:   [Position, movement, framing change over duration]
DURATION: [X seconds, pacing notes]
STYLE:    [Film reference, color grade, quality]
```

**Example:**
```
SCENE:    Rain-soaked Tokyo alley at midnight, neon signs reflecting in puddles
SUBJECT:  A woman in a red coat walks slowly away from camera, heels clicking on pavement
CAMERA:   Steadicam following shot at medium distance, slowly drifting to her left side over 10 seconds
DURATION: 10 seconds, real-time pacing, no slow motion
STYLE:    Wong Kar-wai cinematic, warm reds, shallow depth of field, 35mm film grain
```

---

## Template 5: VFX / Particle / Weather Effect

```
[EFFECT TYPE] [SCALE] in [ENVIRONMENT],
[PHYSICAL BEHAVIOR: spread, direction, color, opacity],
[HOW IT INTERACTS with subjects / environment],
[CAMERA ANGLE], [SPEED: real-time / slow-mo],
cinematic VFX, [style reference]
```

**Example — Blizzard:**
```
Howling blizzard engulfing a mountain village at dusk,
horizontal snow streaks driven by violent gusts, accumulating on rooftops and fences,
snowflakes reacting to subject's movement and breath plumes,
wide static shot from slightly above, real-time,
cinematic VFX, cold desaturated blue-white palette, The Revenant aesthetic
```

**Example — Explosion:**
```
Controlled demolition explosion of a skyscraper at golden hour,
debris cloud expanding outward in slow motion, dust ring rolling along the ground,
glass shards catching the warm light mid-air,
drone wide shot pulling back as explosion fills the frame,
slow-motion 240fps, cinematic VFX, warm orange and black smoke
```

---

## Improving Weak Prompts

| Weak Prompt | Why It Fails | Improved Version |
|---|---|---|
| `"A beautiful sunset photo"` | No subject, angle, or lighting spec | `"Lone fisherman silhouetted against a fiery orange sunset over a calm lake, low angle wide shot, warm rim light from behind, anamorphic lens, teal and orange grade"` |
| `"Epic battle scene"` | No scale, no camera position, no light source | `"Two medieval armies clashing on a fog-covered hillside at dawn, aerial crane shot pulling back from a single knight mid-swing, god rays through morning fog, desaturated cool grade"` |
| `"Cyberpunk city"` | Generic, no subject anchor | `"A neon-lit street vendor under a flickering holographic sign in rain-soaked Neo-Tokyo at 2am, medium close-up, handheld, pink and blue neon reflections on wet cobblestones, shallow DOF"` |
| `"8K ultra realistic portrait"` | Overused quality-filler terms ignored by models | `"Shot on ARRI Alexa Mini, 85mm, f/1.8, Rembrandt lighting, natural color grade, Kodak Vision3 grain"` |

---

## Common Mistakes

| Mistake | Problem | Fix |
|---|---|---|
| `"stunning cinematic 8K"` | Ignored quality filler | Use specific techniques: `"anamorphic, god rays, f/1.4 bokeh"` |
| No camera movement in video | Static clip | Add: `"slow dolly in"`, `"tracking shot"`, `"static shot"` |
| No subject motion in video | Subject freezes | Active present tense: `"walks slowly"`, `"turns her head"`, `"crashes through"` |
| No lighting spec | Flat, uninteresting light | Always specify source + direction + color temp |
| Contradictory elements | `"bright daylight + neon lit"` confuses model | Pick one or explicitly explain: `"late dusk with both fading daylight and neon store signs"` |
| No mood/emotion | Technically correct but soulless | Add director reference or emotional descriptor: `"melancholic"`, `"tense"`, `"serene"` |
| Too many options | Confuses model | Give one clear direction; use `--no` for exclusions |

---

## Learning Path

**Week 1 — Foundations**
- Learn universal formula (SKILL.md)
- Practice shot type vocabulary — generate 10 portrait prompts using Template 1

**Week 2 — Light & Color**
- Study all lighting techniques (reference.md)
- Recreate the look of 3 films you love using director references

**Week 3 — Camera Mastery**
- Practice every camera movement with a video tool
- Apply focal length + aperture + film stock systematically

**Week 4 — VFX & Video**
- Generate 5 particle effects using Template 5
- Write 5-layer video prompts using Template 4
- Experiment with every weather type

**Ongoing**
- Build a personal prompt library — tag what works
- Study film stills from favorite movies and reverse-engineer the prompt
- Follow creators on X/YouTube who publish prompt breakdowns
