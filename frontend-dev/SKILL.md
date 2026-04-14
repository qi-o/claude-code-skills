---
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
  version: "1.0.0"
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
### Phase 0: Design System Discovery
1. Check for `DESIGN.md` in project root — if present, it overrides all default design dials
2. Extract design tokens from DESIGN.md sections:
   - Section 2 (Color Palette) → CSS custom properties / Tailwind theme extension
   - Section 3 (Typography) → Font imports + Tailwind font config
   - Section 4 (Components) → Component styling baseline
   - Section 5 (Layout) → Spacing scale + grid config
   - Section 6 (Depth) → Shadow tokens
3. Generate `tailwind.config` theme extension from extracted tokens
4. If no DESIGN.md exists, proceed with default design dials below

### Phase 1: Design Architecture
1. Analyze the request — determine page type and context. If DESIGN.md was found in Phase 0, all design decisions derive from it.
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

Adapt dynamically based on user requests. When DESIGN.md is present, derive dial values from its Visual Theme & Atmosphere section.

## 1.2 Architecture Conventions
- **DEPENDENCY VERIFICATION:** Check `package.json` before importing any library. Output install command if missing.
- **Framework:** React/Next.js. Default to Server Components. Interactive components must be isolated `"use client"` leaf components.
- **Styling:** Tailwind CSS. Check version in `package.json` — NEVER mix v3/v4 syntax.
- **ANTI-EMOJI POLICY:** NEVER use emojis anywhere. Use Phosphor or Radix icons only.
- **Viewport:** Use `min-h-[100dvh]` not `h-screen`. Use CSS Grid not flex percentage math.
- **Layout:** `max-w-[1400px] mx-auto` or `max-w-7xl`.

## 1.3 Design Rules
| Rule | Directive |
|------|-----------|
| Typography | Headlines: `text-4xl md:text-6xl tracking-tighter`. Body: `text-base leading-relaxed max-w-[65ch]`. **NEVER** use Inter — use Geist/Outfit/Satoshi. **NEVER** use Serif on dashboards. |
| Color | Max 1 accent, saturation < 80%. **NEVER** use AI purple/blue. Stick to one palette. |
| Layout | **NEVER** use centered heroes when VARIANCE > 4. Force split-screen or asymmetric layouts. |
| Cards | **NEVER** use generic cards when DENSITY > 7. Use `border-t`, `divide-y`, or spacing. |
| States | **ALWAYS** implement: Loading (skeleton), Empty, Error, Tactile feedback (`scale-[0.98]`). |
| Forms | Label above input. Error below. `gap-2` for input blocks. |

## 1.4 Anti-Slop Techniques

- **Liquid Glass:** `backdrop-blur` + `border-white/10` + `shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]`
- **Magnetic Buttons:** Use `useMotionValue`/`useTransform` — never `useState` for continuous animations
- **Perpetual Motion:** When INTENSITY > 5, add infinite micro-animations (Pulse, Float, Shimmer)
- **Layout Transitions:** Use Framer `layout` and `layoutId` props
- **Stagger:** Use `staggerChildren` or CSS `animation-delay: calc(var(--index) * 100ms)`

## 1.5 Forbidden Patterns
| Category | Banned |
|----------|--------|
| Visual | Neon glows, pure black (#000), oversaturated accents, gradient text on headers, custom cursors |
| Typography | Inter font, oversized H1s, Serif on dashboards |
| Layout | 3-column equal card rows, floating elements with awkward gaps |
| Components | Default shadcn/ui without customization |

## 1.6 Creative Arsenal

| Category | Patterns |
|----------|----------|
| Navigation | Dock magnification, Magnetic button, Gooey menu, Dynamic island, Radial menu, Speed dial, Mega menu |
| Layout | Bento grid, Masonry, Chroma grid, Split-screen scroll, Curtain reveal |
| Cards | Parallax tilt, Spotlight border, Glassmorphism, Holographic foil, Swipe stack, Morphing modal |
| Scroll | Sticky stack, Horizontal hijack, Locomotive sequence, Zoom parallax, Progress path, Liquid swipe |
| Gallery | Dome gallery, Coverflow, Drag-to-pan, Accordion slider, Hover trail, Glitch effect |
| Text | Kinetic marquee, Text mask reveal, Scramble effect, Circular path, Gradient stroke, Kinetic grid |
| Micro | Particle explosion, Pull-to-refresh, Skeleton shimmer, Directional hover, Ripple click, SVG draw, Mesh gradient, Lens blur |

## 1.7 Bento Paradigm

- **Palette:** Background `#f9fafb`, cards pure white with `border-slate-200/50`
- **Surfaces:** `rounded-[2.5rem]`, diffusion shadow
- **Typography:** Geist/Satoshi, `tracking-tight` headers
- **Labels:** Outside and below cards
- **Animation:** Spring physics (`stiffness: 100, damping: 20`), infinite loops, `React.memo` isolation

**5-Card Archetypes:**
1. Intelligent List — auto-sorting with `layoutId`
2. Command Input — typewriter + blinking cursor
3. Live Status — breathing indicators
4. Wide Data Stream — infinite horizontal carousel
5. Contextual UI — staggered highlight + float-in toolbar

## 1.8 Brand Override

When brand styling is active:
- Dark: `#141413`, Light: `#faf9f5`, Mid: `#b0aea5`, Subtle: `#e8e6dc`
- Accents: Orange `#d97757`, Blue `#6a9bcc`, Green `#788c5d`
- Fonts: Poppins (headings), Lora (body)

**DESIGN.md Override:** When a project-level `DESIGN.md` exists, it supersedes the hardcoded brand values above. Extract colors, fonts, and spacing from the DESIGN.md sections 2-6 and generate Tailwind config accordingly. The DESIGN.md is the single source of truth for the project's visual identity.

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

## 2.3 Animation Recipes

See `references/motion-recipes.md` for full code. Summary:

| Recipe | Tool | Use For |
|--------|------|---------|
| Scroll Reveal | Framer | Fade+slide on viewport entry |
| Stagger Grid | Framer | Sequential list animations |
| Pinned Timeline | GSAP | Horizontal scroll with pinning |
| Tilt Card | Framer | Mouse-tracking 3D perspective |
| Magnetic Button | Framer | Cursor-attracted buttons |
| Text Scramble | Vanilla | Matrix-style decode effect |
| SVG Path Draw | CSS | Scroll-linked path animation |
| Horizontal Scroll | GSAP | Vertical-to-horizontal hijack |
| Particle Background | R3F | Decorative WebGL particles |
| Layout Morph | Framer | Card-to-modal expansion |

## 2.4 Performance Rules
**GPU-only properties (ONLY animate these):** `transform`, `opacity`, `filter`, `clip-path`

**NEVER animate:** `width`, `height`, `top`, `left`, `margin`, `padding`, `font-size` — if you need these effects, use `transform: scale()` or `clip-path` instead.

**Isolation:**
- Perpetual animations MUST be in `React.memo` leaf components
- `will-change: transform` ONLY during animation
- `contain: layout style paint` on heavy containers

**Mobile:**
- ALWAYS respect `prefers-reduced-motion`
- ALWAYS disable parallax/3D on `pointer: coarse`
- Cap particles: desktop 800, tablet 300, mobile 100
- Disable GSAP pin on mobile < 768px

**Cleanup:** Every `useEffect` with GSAP/observers MUST `return () => ctx.revert()`

## 2.5 Springs & Easings

| Feel | Framer Config |
|------|---------------|
| Snappy | `stiffness: 300, damping: 30` |
| Smooth | `stiffness: 150, damping: 20` |
| Bouncy | `stiffness: 100, damping: 10` |
| Heavy | `stiffness: 60, damping: 20` |

| CSS Easing | Value |
|------------|-------|
| Smooth decel | `cubic-bezier(0.16, 1, 0.3, 1)` |
| Smooth accel | `cubic-bezier(0.7, 0, 0.84, 0)` |
| Elastic | `cubic-bezier(0.34, 1.56, 0.64, 1)` |

## 2.6 Accessibility
- ALWAYS wrap motion in `prefers-reduced-motion` check
- NEVER flash content > 3 times/second (seizure risk)
- ALWAYS provide visible focus rings (use `outline` not `box-shadow`)
- ALWAYS add `aria-live="polite"` for dynamically revealed content
- ALWAYS include pause button for auto-playing animations

## 2.7 Dependencies

```bash
npm install framer-motion           # UI (keep at top level)
npm install gsap                    # Scroll (lazy-load)
npm install lottie-react            # Icons (lazy-load)
npm install three @react-three/fiber @react-three/drei  # 3D (lazy-load)
```

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

## 4.1 Core Job

1. Grab attention → 2. Create desire → 3. Remove friction → 4. Prompt action

## 4.2 Frameworks

**AIDA** (landing pages, emails):
```
ATTENTION:  Bold headline (promise or pain)
INTEREST:   Elaborate problem ("yes, that's me")
DESIRE:     Show transformation
ACTION:     Clear CTA
```

**PAS** (pain-driven products):
```
PROBLEM:    State clearly
AGITATE:    Make urgent
SOLUTION:   Your product
```

**FAB** (product differentiation):
```
FEATURE:    What it does
ADVANTAGE:  Why it matters
BENEFIT:    What customer gains
```

## 4.3 Headlines

| Formula | Example |
|---------|---------|
| Promise | "Double open rates in 30 days" |
| Question | "Still wasting 10 hours/week?" |
| How-To | "How to automate your pipeline" |
| Number | "7 mistakes killing conversions" |
| Negative | "Stop losing leads" |
| Curiosity | "The one change that tripled bookings" |
| Transformation | "From 50 to 500 leads" |

Be specific. Lead with outcome, not method.

## 4.4 CTAs

**Bad:** Submit, Click here, Learn more

**Good:** "Start my free trial", "Get the template now", "Book my strategy call"

**Formula:** [Action Verb] + [What They Get] + [Urgency/Ease]

Place: above fold, after value, multiple on long pages.

## 4.5 Emotional Triggers

| Trigger | Example |
|---------|---------|
| FOMO | "Only 3 spots left" |
| Fear of loss | "Every day without this, you're losing $X" |
| Status | "Join 10,000+ top agencies" |
| Ease | "Set it up once. Forget forever." |
| Frustration | "Tired of tools that deliver nothing?" |
| Hope | "Yes, you CAN hit $10K MRR" |

## 4.6 Objection Handling

| Objection | Response |
|-----------|----------|
| Too expensive | Show ROI: "Pays for itself in 2 weeks" |
| Won't work for me | Social proof from similar customer |
| No time | "Setup takes 10 minutes" |
| What if it fails | "30-day money-back guarantee" |
| Need to think | Urgency/scarcity |

Place in FAQ, testimonials, near CTA.

## 4.7 Proof Types

Testimonials (with name/title), Case studies, Data/metrics, Social proof, Certifications

---

# 5. Visual Art

Philosophy-first workflow. Two output modes.

## 5.1 Output Modes

| Mode | Output | When |
|------|--------|------|
| Static | PDF/PNG | Posters, print, design assets |
| Interactive | HTML (p5.js) | Generative art, explorable variations |

## 5.2 Workflow

### Step 1: Philosophy Creation
Name the movement (1-2 words). Articulate philosophy (4-6 paragraphs) covering:
- Static: space, form, color, scale, rhythm, hierarchy
- Interactive: computation, emergence, noise, parametric variation

### Step 2: Conceptual Seed
Identify subtle, niche reference — sophisticated, not literal. Jazz musician quoting another song.

### Step 3: Creation

**Static Mode:**
- Single page, highly visual, design-forward
- Repeating patterns, perfect shapes
- Sparse typography from `canvas-fonts/`
- Nothing overlaps, proper margins
- Output: `.pdf` or `.png` + philosophy `.md`

**Interactive Mode:**
1. Read `templates/viewer.html` first
2. Keep FIXED sections (header, sidebar, seed controls)
3. Replace VARIABLE sections (algorithm, parameters)
4. Seeded randomness: `randomSeed(seed); noiseSeed(seed);`
5. Output: single self-contained HTML

### Step 4: Refinement
Refine, don't add. Make it crisp. Polish into masterpiece.

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

## 用户确认检查点

以下操作前**必须暂停并询问用户确认**：

| 检查点 | 触发条件 | 确认内容 |
|--------|---------|---------|
| 资产生成 | Phase 3 前调用 MiniMax 生成图片/视频/音频 | 确认生成内容和数量，消耗 API 配额且不可撤销 |
| DESIGN.md 覆盖 | Phase 0 检测到已有 DESIGN.md | 确认是追加更新还是完全覆盖现有设计 |
| 技术栈选择 | 用户未指定框架/CSS方案/动画库时 | 确认技术选型，后续切换成本高 |
| 重量级动效资源 | MOTION_INTENSITY >= 7 的动效需求 | 提示性能影响和移动端兼容性，确认是否降级 |

## 错误处理与回退

| 错误场景 | 检测信号 | 回退策略 |
|---------|---------|---------|
| MiniMax API 失败 | 资产生成脚本返回非零退出码 | 跳过该资产继续构建，用占位符标记，最后统一重试 |
| 依赖安装失败 | npm install 报错 | 检查 Node 版本兼容性，尝试删除 node_modules 重新安装 |
| GSAP 与 Framer Motion 冲突 | 两者同时引入导致动画异常 | 移除 GSAP 依赖，统一使用 Framer Motion 实现所有动效 |
| Tailwind v3/v4 语法不匹配 | 构建报错 class 无效 | 检测项目 Tailwind 版本，v4 使用 CSS-first 配置而非 tailwind.config.js |
