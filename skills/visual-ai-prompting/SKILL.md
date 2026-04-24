---
name: visual-ai-prompting
description: >-
  Craft high-quality prompts for AI image generators (Midjourney, Stable Diffusion, Flux, DALL-E),
  cinematic stills, video generation (Sora, Runway Gen-4, Kling, Veo 3, Pika), and VFX shots.
  Use when the user asks how to write prompts for images, videos, cinematic shots, VFX effects,
  lighting, camera angles, or visual AI tools. Also use when reviewing or improving existing prompts.
---

# Visual AI Prompting

## Mental Model

You are not *describing a picture* — you are **directing a scene**. A film director controls four things:
1. **What** is in the frame (subject, props, set)
2. **How** the camera sees it (angle, lens, movement)
3. **How it is lit** (source, direction, intensity, color)
4. **What feeling** it creates (mood, era, style reference)

Your prompt gives all four instructions to a virtual DP (Director of Photography). Specific, technical prompts produce cinematic results. Vague prompts produce generic ones.

---

## Universal Prompt Formula

### Images
```
[Subject + Action] + [Setting & Time] + [Lighting] + [Camera Angle + Lens + DOF] + [Color Grade] + [Technical Params]
```

### Video
```
[Scene & Environment] + [Subject + Active Motion] + [Camera Movement] + [Duration] + [Lighting] + [Style]
```

> **Key difference**: Images describe a moment. Videos describe *change over time*.  
> Always specify motion at 3 levels: **environment**, **subject**, and **camera**.

---

## Shot Types (Framing)

| Shot | What It Shows | Use For |
|---|---|---|
| Extreme Wide (EWS) | Vast env, tiny subject | Scale, isolation |
| Wide (WS) | Full subject + environment | Context, world-building |
| Medium (MS) | Waist up | Action, conversation |
| Medium Close-Up (MCU) | Chest up | Emotional connection |
| Close-Up (CU) | Face | Emotion, detail |
| Extreme Close-Up (ECU) | Eyes / hands / object | Intensity, obsession |
| Over-the-Shoulder (OTS) | One character toward another | Dialogue, confrontation |
| Low Angle | Camera below subject | Power, heroism |
| High Angle | Camera above subject | Vulnerability, smallness |
| Bird's Eye / Aerial | Directly overhead | Scale, surveillance |
| Dutch Tilt | Tilted frame | Tension, unease |

---

## Camera Movements (Video)

| Movement | Effect |
|---|---|
| Static shot | Stillness, contemplation |
| Dolly in / out | Intimacy / isolation |
| Pan left / right | Follow action, reveal space |
| Tracking shot | Energy, presence alongside subject |
| Crane shot | Epic vertical reveal |
| Drone shot | Scale, grandeur |
| Handheld | Urgency, documentary realism |
| Steadicam | Fluid elegance |
| Whip pan | Rapid cut energy |
| Rack focus | Shift narrative attention |
| Slow push in | Psychological dread, vertigo |

---

## Lighting Quick Reference

**Techniques:**
- `chiaroscuro` — dramatic light/dark contrast, single hard source
- `Rembrandt lighting` — triangle of light on shadowed cheek
- `butterfly lighting` — overhead front, Hollywood glamour
- `rim lighting` / `edge light` — glowing edge separating subject from background
- `split lighting` — half face illuminated, half in shadow
- `volumetric lighting` / `god rays` — visible light through fog/dust/smoke
- `silhouette` — subject fully backlit, no fill light

**Natural Sources:**
- `golden hour` — warm directional, 1hr before sunset
- `blue hour` — cool twilight
- `overcast soft light` — even, flattering, no harsh shadows
- `harsh overhead noon sun` — gritty, raw

**Color Temperature:**
- 2700–3200K → warm / amber / tungsten
- 5600K → neutral daylight
- 7000K+ → cool / blue / twilight

---

## Lens & Technical Specs

| Focal Length | Effect |
|---|---|
| 14–24mm | Ultra-wide, exaggerated depth |
| 35mm | Natural, human-eye feel |
| 50mm | Neutral, no distortion |
| 85mm | Classic portrait, subject isolation |
| 135mm+ | Heavy compression, shallow DOF |

**Key lens terms:** `anamorphic lens flare`, `creamy bokeh orbs`, `shallow depth of field`, `f/1.4 aperture`, `chromatic aberration`, `lens flare`

**Film stocks:** `shot on ARRI Alexa Mini`, `Kodak Vision3 500T`, `16mm film grain`, `Fujifilm Velvia`

**Aspect ratios:** `16:9` (standard), `2.39:1` (anamorphic cinema), `9:16` (mobile/reels), `4:5` (portrait)

---

## Color Grades

| Grade | Look | Prompt |
|---|---|---|
| Orange & Teal | Warm skin + cool BG | `"teal and orange color grade"` |
| Desaturated gritty | Muted, gray | `"desaturated with crushed blacks"` |
| Neon Noir | Saturated neons + deep shadows | `"neon pink and electric blue on wet pavement"` |
| Warm vintage | Faded 70s | `"warm amber tones, lifted shadows, film-scanned"` |
| Bleach bypass | Silver-grey, high contrast | `"bleach bypass treatment"` |
| High key | Bright, white, airy | `"high key lighting, white background, soft shadows"` |

---

## Director Style References

| Director | Prompt Keywords |
|---|---|
| Christopher Nolan | `"desaturated blue-gray, IMAX, practical lighting"` |
| Denis Villeneuve | `"vast architectural frame, cool epic, wide shot"` |
| Wong Kar-wai | `"slow shutter motion blur, warm reds and greens, dreamy"` |
| Wes Anderson | `"perfectly centered symmetry, pastel palette"` |
| David Fincher | `"dark green tint, high contrast, hyper-detailed"` |
| Stanley Kubrick | `"one-point perspective, 14mm, perfectly symmetrical, cold"` |
| Ridley Scott | `"god rays, atmospheric haze, high detail cinematic"` |
| Terrence Malick | `"handheld golden hour, natural light, ethereal"` |

---

## VFX Prompting Essentials

**Fire:** describe temperature (color), intensity (size), environment interaction + `"volumetric smoke"`, `"embers scattering"`

**Explosion:** specify scale, debris behavior, light cast + `"slow-motion"`, `"shockwave pulse"`, `"heat distortion"`

**Water:** specify volume, motion, lighting reflections + `"fluid dynamics"`, `"caustic light patterns"`

**Magic/Energy:** `"arc lightning"`, `"glowing energy tendrils"`, `"particle tendrils reaching outward"`, `"swirling vortex"`

**Weather:**
- Rain → `"rain streaks"` + `"wet pavement reflections"` + neon for cyberpunk
- Snow → `"snowflakes accumulating on surfaces"`, `"blizzard swirling"`, `"pale sun"`
- Fog → `"low-lying mist"`, `"volumetric fog tendrils"`, `"shafts of light cutting through"`

---

## Platform Notes

| Platform | Strengths | Key Param |
|---|---|---|
| Midjourney V6 | Best image quality | `--ar`, `--style raw`, `--no`, `--sref` |
| Stable Diffusion / Flux | Full control, LoRA support | Negative prompt, CFG scale |
| Sora | Narrative coherence | Descriptive + emotional |
| Runway Gen-4 | Commercial precision | Motion brush, camera controls |
| Kling 2.0 | Long clips (120s), faces | Detail-focused |
| Veo 3 / 3.1 | Physics, weather, VFX | Technical + physics-aware |

---

## Common Mistakes

| Mistake | Fix |
|---|---|
| `"beautiful cinematic 8K"` | Use specific techniques: `"anamorphic, god rays, shallow DOF"` |
| No camera movement in video | Always add: `"slow dolly in"`, `"tracking shot"`, `"static"` |
| No lighting spec | Add source, direction, color temp every time |
| Contradictory elements | `"daylight + neon lit"` needs reconciliation or a clear choice |
| Passive verbs in video | Use active present tense: `"walks"`, `"turns"`, `"crashes"` |

---

## Supporting Files

- Full lighting, color, lens, director, VFX, weather details → [reference.md](reference.md)
- 5 copy-paste prompt templates → [examples.md](examples.md)
- Complete term definitions → [glossary.md](glossary.md)
