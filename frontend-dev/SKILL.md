---
github_url: https://github.com/MiniMax-AI/skills
github_hash: f87b423670b193a0b52a10526338f596f673a8b8
name: frontend-dev
description: |
  Full-stack frontend development combining premium UI design, cinematic animations,
  AI-generated media assets, persuasive copywriting, and visual art. Builds complete,
  visually striking web pages with real media, advanced motion, and compelling copy.
  Use when: building landing pages, marketing sites, product pages, dashboards,
  generating media assets (image/video/audio/music), writing conversion copy,
  creating generative art, or implementing cinematic scroll animations.
license: MIT
metadata:
  version: "1.1.0"
  category: frontend
  sources:
    - Framer Motion documentation
    - GSAP / GreenSock documentation
    - Three.js documentation
    - Tailwind CSS documentation
    - React / Next.js documentation
    - AIDA Framework (Elmo Lewis)
    - p5.js documentation
---

# Frontend Studio

Build complete, production-ready frontend pages by orchestrating 5 specialized capabilities: design engineering, motion systems, AI-generated assets, persuasive copy, and generative art.

## Invocation

```
/frontend-dev <request>
```

The user provides their request as natural language (e.g. "build a landing page for a music streaming app").

## Skill Structure

```
frontend-dev/
├── SKILL.md                      # Core skill (this file)
├── scripts/                      # Asset generation scripts
│   ├── minimax_tts.py            # Text-to-speech
│   ├── minimax_music.py          # Music generation
│   ├── minimax_video.py          # Video generation (async)
│   └── minimax_image.py          # Image generation
├── references/                   # Detailed guides (read as needed)
│   ├── minimax-cli-reference.md  # CLI flags quick reference
│   ├── asset-prompt-guide.md     # Asset prompt engineering rules
│   ├── minimax-tts-guide.md      # TTS usage & voices
│   ├── minimax-music-guide.md    # Music prompts & lyrics format
│   ├── minimax-video-guide.md    # Camera commands & models
│   ├── minimax-image-guide.md    # Ratios & batch generation
│   ├── minimax-voice-catalog.md  # All voice IDs
│   ├── motion-recipes.md         # Animation code snippets
│   ├── env-setup.md              # Environment setup
│   └── troubleshooting.md        # Common issues
├── templates/                    # Visual art templates
│   ├── viewer.html               # p5.js interactive art base
│   └── generator_template.js     # p5.js code reference
└── canvas-fonts/                 # Static art fonts (TTF + licenses)
```

## Project Structure

### Assets (Universal)

All frameworks use the same asset organization:

```
assets/
├── images/
│   ├── hero-landing-1710xxx.webp
│   ├── icon-feature-01.webp
│   └── bg-pattern.svg
├── videos/
│   ├── hero-bg-1710xxx.mp4
│   └── demo-preview.mp4
└── audio/
    ├── bgm-ambient-1710xxx.mp3
    └── tts-intro-1710xxx.mp3
```

**Asset naming:** `{type}-{descriptor}-{timestamp}.{ext}`

### By Framework

| Framework | Asset Location | Component Location |
|-----------|---------------|-------------------|
| **Pure HTML** | `./assets/` | N/A (inline or `./js/`) |
| **React/Next.js** | `public/assets/` | `src/components/` |
| **Vue/Nuxt** | `public/assets/` | `src/components/` |
| **Svelte/SvelteKit** | `static/assets/` | `src/lib/components/` |
| **Astro** | `public/assets/` | `src/components/` |

### Pure HTML

```
project/
├── index.html
├── assets/
│   ├── images/
│   ├── videos/
│   └── audio/
├── css/
│   └── styles.css
└── js/
    └── main.js           # Animations (GSAP/vanilla)
```

### React / Next.js

```
project/
├── public/assets/        # Static assets
├── src/
│   ├── components/
│   │   ├── ui/           # Button, Card, Input
│   │   ├── sections/     # Hero, Features, CTA
│   │   └── motion/       # RevealSection, StaggerGrid
│   ├── lib/
│   ├── styles/
│   └── app/              # Pages
└── package.json
```

### Vue / Nuxt

```
project/
├── public/assets/
├── src/                  # or root for Nuxt
│   ├── components/
│   │   ├── ui/
│   │   ├── sections/
│   │   └── motion/
│   ├── composables/      # Shared logic
│   ├── pages/
│   └── assets/           # Processed assets (optional)
└── package.json
```

### Astro

```
project/
├── public/assets/
├── src/
│   ├── components/       # .astro, .tsx, .vue, .svelte
│   ├── layouts/
│   ├── pages/
│   └── styles/
└── package.json
```

**Component naming:** PascalCase (`HeroSection.tsx`, `HeroSection.vue`, `HeroSection.astro`)

---

## Compliance

**All rules in this skill are mandatory. Violating any rule is a blocking error — fix before proceeding or delivering.**

---

## Workflow
### Phase 1: Design Architecture
1. Analyze the request — determine page type and context
2. Set design dials based on page type
3. Plan layout sections and identify asset needs

### Phase 2: Motion Architecture
1. Select animation tools per section (see Tool Selection Matrix)
2. Plan motion sequences following performance guardrails

### Phase 3: Asset Generation
Generate all image/video/audio assets using `scripts/`. NEVER use placeholder URLs (unsplash, picsum, placeholder.com, via.placeholder, placehold.co, etc.) or external URLs.

1. Parse asset requirements (type, style, spec, usage)
2. Craft optimized prompts, show to user, confirm before generating
3. Execute via scripts, save to project — do NOT proceed to Phase 5 until all assets are saved locally

### Phase 4: Copywriting & Content
Follow copywriting frameworks (AIDA, PAS, FAB) to craft all text content. Do NOT use "Lorem ipsum" — write real copy.

### Phase 5: Build UI
Scaffold the project and build each section following Design and Motion rules. Integrate generated assets and copy. All `<img>`, `<video>`, `<source>`, and CSS `background-image` MUST reference local assets from Phase 3.

### Phase 6: Quality Gates
Run final checklist (see Quality Gates section).

---

# 1. Design Engineering

## 1.1 Baseline Configuration

| Dial | Default | Range |
|------|---------|-------|
| DESIGN_VARIANCE | 8 | 1=Symmetry, 10=Asymmetric |
| MOTION_INTENSITY | 6 | 1=Static, 10=Cinematic |
| VISUAL_DENSITY | 4 | 1=Airy, 10=Packed |

Adapt dynamically based on user requests.

## 1.2 Architecture Conventions
- **DEPENDENCY VERIFICATION:** Check `package.json` before importing any library. Output install command if missing.
- **Framework:** React/Next.js. Default to Server Components. Interactive components must be isolated `"use client"` leaf components.
- **Styling:** Tailwind CSS. Check version in `package.json` — NEVER mix v3/v4 syntax.
- **ANTI-EMOJI POLICY:** NEVER use emojis anywhere. Use Phosphor or Radix icons only.
- **Viewport:** Use `min-h-[100dvh]` not `h-screen`. Use CSS Grid not flex percentage math.
- **Layout:** `max-w-[1400px] mx-auto` or `max-w-7xl`.

## 1.3 Design Rules

> **For detailed design patterns and anti-slop techniques, see [references/motion-recipes.md](references/motion-recipes.md)**

| Rule | Directive |
|------|-----------|
| Typography | Headlines: `text-4xl md:text-6xl tracking-tighter`. Body: `text-base leading-relaxed max-w-[65ch]`. **NEVER** use Inter — use Geist/Outfit/Satoshi. |
| Color | Max 1 accent, saturation < 80%. **NEVER** use AI purple/blue. |
| Layout | **NEVER** use centered heroes when VARIANCE > 4. Force split-screen or asymmetric. |
| Cards | **NEVER** use generic cards when DENSITY > 7. Use `border-t`, `divide-y`, or spacing. |
| States | **ALWAYS** implement: Loading (skeleton), Empty, Error, Tactile feedback (`scale-[0.98]`). |
| Forms | Label above input. Error below. `gap-2` for input blocks. |

## 1.4-1.8 Design Patterns

**Anti-Slop Techniques:** Liquid Glass, Magnetic Buttons, Perpetual Motion, Layout Transitions, Stagger

**Forbidden Patterns:** Neon glows, pure black, oversaturated accents, gradient text, Inter font, oversized H1s, Serif on dashboards, 3-column equal cards, default shadcn/ui

**Creative Arsenal:** Navigation (Dock, Magnetic, Gooey), Layout (Bento, Masonry, Split-screen), Cards (Parallax tilt, Glassmorphism), Scroll (Sticky stack, Horizontal hijack), Gallery (Dome, Coverflow), Text (Kinetic marquee, Scramble), Micro (Particle explosion, Ripple)

**Bento Paradigm:** Background `#f9fafb`, cards pure white, `rounded-[2.5rem]`, Geist/Satoshi typography, spring physics animation

**Brand Override:** Dark `#141413`, Light `#faf9f5`, Accents: Orange `#d97757`, Blue `#6a9bcc`, Green `#788c5d`, Fonts: Poppins/Lora

---

# 2. Motion Engine

## 2.1 Tool Selection Matrix

| Need | Tool |
|------|------|
| UI enter/exit/layout | **Framer Motion** — `AnimatePresence`, `layoutId`, springs |
| Scroll storytelling (pin, scrub) | **GSAP + ScrollTrigger** — frame-accurate control |
| Looping icons | **Lottie** — lazy-load (~50KB) |
| 3D/WebGL | **Three.js / R3F** — isolated `<Canvas>`, own `"use client"` boundary |
| Hover/focus states | **CSS only** — zero JS cost |
| Native scroll-driven | **CSS** — `animation-timeline: scroll()` |

**Conflict Rules [MANDATORY]:**
- NEVER mix GSAP + Framer Motion in same component
- R3F MUST live in isolated Canvas wrapper
- ALWAYS lazy-load Lottie, GSAP, Three.js

## 2.2 Intensity Scale

| Level | Techniques |
|-------|------------|
| 1-2 Subtle | CSS transitions only, 150-300ms |
| 3-4 Smooth | CSS keyframes + Framer animate, stagger ≤3 items |
| 5-6 Fluid | `whileInView`, magnetic hover, parallax tilt |
| 7-8 Cinematic | GSAP ScrollTrigger, pinned sections, horizontal hijack |
| 9-10 Immersive | Full scroll sequences, Three.js particles, WebGL shaders |

## 2.3-2.7 Motion Details

> **For animation recipes, performance rules, and accessibility, see [references/motion-recipes.md](references/motion-recipes.md)**

**Animation Recipes Summary:**
- Scroll Reveal, Stagger Grid, Pinned Timeline (GSAP), Tilt Card, Magnetic Button, Text Scramble, SVG Path Draw, Horizontal Scroll, Particle Background, Layout Morph

**Performance:** GPU-only properties (`transform`, `opacity`, `filter`, `clip-path`). NEVER animate `width`, `height`, `top`, `left`, `margin`, `padding`.

**Mobile:** Respect `prefers-reduced-motion`, disable parallax/3D on `pointer: coarse`, cap particles (desktop 800, tablet 300, mobile 100).

**Springs:** Snappy (300/30), Smooth (150/20), Bouncy (100/10), Heavy (60/20)

**Dependencies:** `framer-motion` (top level), `gsap`, `lottie-react`, `three`, `@react-three/fiber`, `@react-three/drei` (lazy-load)

---

# 3. Asset Generation

## 3.1 Scripts

| Type | Script | Pattern |
|------|--------|---------|
| TTS | `scripts/minimax_tts.py` | Sync |
| Music | `scripts/minimax_music.py` | Sync |
| Video | `scripts/minimax_video.py` | Async (create → poll → download) |
| Image | `scripts/minimax_image.py` | Sync |

Env: `MINIMAX_API_KEY` (required).

## 3.2 Workflow
1. **Parse:** type, quantity, style, spec, usage
2. **Craft prompt:** Be specific (composition, lighting, style). **NEVER** include text in image prompts.
3. **Execute:** Show prompt to user, **MUST confirm before generating**, then run script
4. **Save:** `<project>/public/assets/{images,videos,audio}/` as `{type}-{descriptor}-{timestamp}.{ext}` — **MUST save locally**
5. **Post-process:** Images → WebP, Videos → ffmpeg compress, Audio → normalize
6. **Deliver:** File path + code snippet + CSS suggestion

## 3.3 Preset Shortcuts

| Shortcut | Spec |
|----------|------|
| `hero` | 16:9, cinematic, text-safe |
| `thumb` | 1:1, centered subject |
| `icon` | 1:1, flat, clean background |
| `avatar` | 1:1, portrait, circular crop ready |
| `banner` | 21:9, OG/social |
| `bg-video` | 768P, 6s, `[Static shot]` |
| `video-hd` | 1080P, 6s |
| `bgm` | 30s, no vocals, loopable |
| `tts` | MiniMax HD, MP3 |

## 3.4 Reference

- `references/minimax-cli-reference.md` — CLI flags
- `references/asset-prompt-guide.md` — Prompt rules
- `references/minimax-voice-catalog.md` — Voice IDs
- `references/minimax-tts-guide.md` — TTS usage
- `references/minimax-music-guide.md` — Music generation (prompts, lyrics, structure tags)
- `references/minimax-video-guide.md` — Camera commands
- `references/minimax-image-guide.md` — Ratios, batch

---

# 4. Copywriting

> **For detailed copywriting frameworks and examples, see existing references**

**Core Job:** Grab attention → Create desire → Remove friction → Prompt action

**Frameworks:**
- **AIDA** (landing pages): Attention → Interest → Desire → Action
- **PAS** (pain-driven): Problem → Agitate → Solution
- **FAB** (product): Feature → Advantage → Benefit

**Headline Formulas:** Promise, Question, How-To, Number, Negative, Curiosity, Transformation

**CTAs:** [Action Verb] + [What They Get] + [Urgency/Ease]. Place above fold, after value, multiple on long pages.

**Emotional Triggers:** FOMO, Fear of loss, Status, Ease, Frustration, Hope

**Objection Handling:** Too expensive → ROI, Won't work → Social proof, No time → Quick setup, What if fails → Guarantee

**Proof Types:** Testimonials, Case studies, Data/metrics, Social proof, Certifications

---

# 5. Visual Art

**Philosophy-first workflow. Two output modes:**

| Mode | Output | When |
|------|--------|------|
| Static | PDF/PNG | Posters, print, design assets |
| Interactive | HTML (p5.js) | Generative art, explorable variations |

**Workflow:**
1. **Philosophy Creation**: Name movement (1-2 words). Articulate philosophy covering space, form, color, scale, rhythm, hierarchy (static) or computation, emergence, noise, parametric variation (interactive)
2. **Conceptual Seed**: Subtle, niche reference — sophisticated, not literal
3. **Creation**:
   - Static: Single page, highly visual, repeating patterns, perfect shapes, sparse typography, proper margins. Output `.pdf`/`.png` + philosophy `.md`
   - Interactive: Read `templates/viewer.html`, keep fixed sections (header, sidebar, seed controls), replace variable sections (algorithm, parameters), seeded randomness. Output single HTML
4. **Refinement**: Refine, don't add. Make it crisp. Polish into masterpiece

---

# Quality Gates
**Design:**
- [ ] Mobile layout collapse (`w-full`, `px-4`) for high-variance designs
- [ ] `min-h-[100dvh]` not `h-screen`
- [ ] Empty, loading, error states provided
- [ ] Cards omitted where spacing suffices

**Motion:**
- [ ] Correct tool per selection matrix
- [ ] No GSAP + Framer mixed in same component
- [ ] All `useEffect` have cleanup returns
- [ ] `prefers-reduced-motion` respected
- [ ] Perpetual animations in `React.memo` leaf components
- [ ] Only GPU properties animated
- [ ] Heavy libraries lazy-loaded

**General:**
- [ ] Dependencies verified in `package.json`
- [ ] **No placeholder URLs** — grep the output for `unsplash`, `picsum`, `placeholder`, `placehold`, `via.placeholder`, `lorem.space`, `dummyimage`. If ANY found, STOP and replace with generated assets before delivering.
- [ ] **All media assets exist as local files** in the project's assets directory
- [ ] Asset prompts confirmed with user before generation

---

*React and Next.js are trademarks of Meta Platforms, Inc. and Vercel, Inc., respectively. Vue.js is a trademark of Evan You. Tailwind CSS is a trademark of Tailwind Labs Inc. Svelte and SvelteKit are trademarks of their respective owners. GSAP/GreenSock is a trademark of GreenSock Inc. Three.js, Framer Motion, Lottie, Astro, and all other product names are trademarks of their respective owners.*
