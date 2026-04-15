---
name: frontend-design
description: >
  Create distinctive, production-grade frontend interfaces with high design quality. Triggers (English): build web components, create website, landing page, dashboard, React component, web UI, styling, beautify, frontend design, web design. Triggers (Chinese): 前端开发, 网页设计, 制作网页, 创建网站, 做界面, 前端UI, React组件, 样式美化, Web开发, 做前端。
  Use when the user asks to build web components, pages, artifacts, posters, or applications. Generates creative, polished code and UI design that avoids generic AI aesthetics.
license: Complete terms in LICENSE.txt
github_url: https://github.com/anthropics/skills
github_hash: 0f7c287eaf0d4fa511cb871bb55e2a7862251fbb
version: 0.0.1
secondary_sources:
  - name: react-best-practices
    url: https://github.com/vercel-labs/agent-skills
    hash: 47863b24f8e22966bfcf8470debc7ba8c2c3b99c
---

This skill guides creation of distinctive, production-grade frontend interfaces that avoid generic "AI slop" aesthetics. Implement real working code with exceptional attention to aesthetic details and creative choices.

The user provides frontend requirements: a component, page, application, or interface to build. They may include context about the purpose, audience, or technical constraints.

## Design Thinking

Before coding, understand the context and commit to a BOLD aesthetic direction:
- **Purpose**: What problem does this interface solve? Who uses it?
- **Tone**: Pick an extreme: brutally minimal, maximalist chaos, retro-futuristic, organic/natural, luxury/refined, playful/toy-like, editorial/magazine, brutalist/raw, art deco/geometric, soft/pastel, industrial/utilitarian, etc. There are so many flavors to choose from. Use these for inspiration but design one that is true to the aesthetic direction.
- **Constraints**: Technical requirements (framework, performance, accessibility).
- **Differentiation**: What makes this UNFORGETTABLE? What's the one thing someone will remember?

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work - the key is intentionality, not intensity.

Then implement working code (HTML/CSS/JS, React, Vue, etc.) that is:
- Production-grade and functional
- Visually striking and memorable
- Cohesive with a clear aesthetic point-of-view
- Meticulously refined in every detail


## DESIGN.md System

DESIGN.md is a standardized format for capturing complete visual design systems in markdown — directly consumable by AI agents. It complements CLAUDE.md (code behavior) and AGENTS.md (build behavior) with the visual/aesthetic layer.

### Reading DESIGN.md

When a project contains a `DESIGN.md` in its root:
1. **Read it first** — DESIGN.md overrides all default aesthetic choices below
2. **Extract design tokens** — colors, typography, spacing, elevation from the spec
3. **Follow component patterns** — buttons, cards, inputs must match the spec's states and styles
4. **Respect Do's and Don'ts** — the spec's guardrails take precedence over this skill's defaults
5. **Use Agent Prompt Guide** — Section 9 of DESIGN.md contains ready-to-use color references

### Generating DESIGN.md

When no DESIGN.md exists and the user wants a design system, generate one following the 9-section schema:

| # | Section | What to Define |
|---|---------|---------------|
| 1 | **Visual Theme & Atmosphere** | Mood descriptor, design density, overall philosophy (e.g., "void-black canvas, emerald accent, terminal-native") |
| 2 | **Color Palette & Roles** | Semantic name + hex + functional role for each color. Include: primary, secondary, accent, background, surface, text, muted, border, error, success, warning |
| 3 | **Typography Rules** | Font families (display + body), full size hierarchy table (h1-h6, body, caption, overline), line-height, letter-spacing, font-weight |
| 4 | **Component Stylings** | Buttons (primary/secondary/ghost + hover/active/disabled states), cards, inputs, navigation, badges, tooltips with exact CSS values |
| 5 | **Layout Principles** | Spacing scale (4px base or 8px base), grid system, max-width, whitespace philosophy, container padding |
| 6 | **Depth & Elevation** | Shadow system (sm/md/lg/xl), surface hierarchy (background → surface → elevated → overlay), border treatments |
| 7 | **Do's and Don'ts** | Design guardrails: what to always do, what to never do, specific anti-patterns for this brand |
| 8 | **Responsive Behavior** | Breakpoints table, touch target minimums (44px), collapsing strategy (stack/hide/drawer), mobile-specific overrides |
| 9 | **Agent Prompt Guide** | Quick color reference block for copy-paste, ready-to-use Tailwind/CSS variable declarations, example prompts |

### Brand Mood Vocabulary

Use evocative compound descriptors to capture design identity in minimal tokens:

**By archetype:**
- **Luxury/Premium**: "cinema-black canvas, monochrome austerity, monumental display type"
- **Technical/Developer**: "terminal-first, monochrome simplicity, code-forward"
- **Editorial/Content**: "paper-white broadsheet density, custom serif, ink-blue links"
- **Playful/Friendly**: "playful gradients, friendly aesthetic, rounded surfaces"
- **Fintech/Trust**: "clean blue identity, trust-focused, institutional feel"
- **Cinematic/Media**: "dark cinematic UI, media-rich layout, waveform aesthetics"
- **Minimal/Precise**: "black and white precision, radical subtraction, systematic typography"
- **Bold/Energetic**: "bold dark interface, neon accents, high-contrast surfaces"

### Preview HTML Generation

After generating a DESIGN.md, also generate a `preview.html` visual catalog containing:
- Color swatches (all palette colors with hex labels)
- Typography scale (all heading levels + body + caption rendered)
- Button states (primary/secondary/ghost x default/hover/active/disabled)
- Card examples (basic, with image, interactive)
- Input states (default, focus, error, disabled)
- Spacing scale visualization
- Shadow/elevation examples

Generate both light and dark variants (`preview.html` + `preview-dark.html`) when the design system includes dark mode.

## Frontend Aesthetics Guidelines

Focus on:
- **Typography**: Choose fonts that are beautiful, unique, and interesting. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics; unexpected, characterful font choices. Pair a distinctive display font with a refined body font.
- **Color & Theme**: Commit to a cohesive aesthetic. Use CSS variables for consistency. Dominant colors with sharp accents outperform timid, evenly-distributed palettes.
- **Motion**: Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on high-impact moments: one well-orchestrated page load with staggered reveals (animation-delay) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.
- **Spatial Composition**: Unexpected layouts. Asymmetry. Overlap. Diagonal flow. Grid-breaking elements. Generous negative space OR controlled density.
- **Backgrounds & Visual Details**: Create atmosphere and depth rather than defaulting to solid colors. Add contextual effects and textures that match the overall aesthetic. Apply creative forms like gradient meshes, noise textures, geometric patterns, layered transparencies, dramatic shadows, decorative borders, custom cursors, and grain overlays.

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Interpret creatively and make unexpected choices that feel genuinely designed for the context. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices (Space Grotesk, for example) across generations.

**IMPORTANT**: Match implementation complexity to the aesthetic vision. Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

Remember: Claude is capable of extraordinary creative work. Don't hold back, show what can truly be created when thinking outside the box and committing fully to a distinctive vision.

## 用户确认检查点

以下操作前**必须暂停并询问用户确认**：

| 检查点 | 触发条件 | 确认内容 |
|--------|---------|---------|
| 覆盖现有文件 | 生成的代码将写入已有项目文件 | 展示将被修改的文件列表，确认覆盖范围 |
| 设计方向选择 | 存在多个合理的美学方向时 | 展示 2-3 个设计方向的核心特征，请用户选择 |
| 第三方依赖引入 | 代码需要安装新的 npm 包或外部资源 | 列出依赖名称和用途，确认用户同意引入 |

## 错误处理与回退

| 错误场景 | 检测信号 | 回退策略 |
|---------|---------|---------|
| 框架/技术栈不匹配 | 用户指定了 React/Vue 但生成了纯 HTML | 重新确认技术栈要求，按指定框架重写 |
| 生成的样式与 DESIGN.md 冲突 | 项目存在 DESIGN.md 但输出未遵循 | 重新读取 DESIGN.md 提取设计 token，按规范调整 |
| 响应式布局失效 | 组件在移动端显示异常 | 检查断点设置和 media query，补充移动端适配 |
| 字体/资源加载失败 | CDN 字体或外部资源不可用 | 替换为系统字体或本地资源，确保界面可用性 |

**原则**：不要静默失败——报错时同时提供修复建议。
