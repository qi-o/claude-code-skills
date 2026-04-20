# Anti-AI-Slop Rules

Five rules extracted from the Claude Artifacts design system prompt (lines 305–311).
The list is "including but not limited to" — treat these as exemplars of a broader
principle: **every visual element must serve a purpose, not fill space or signal effort**.

---

## The 5 Rules

### Rule 1 — No Aggressive Gradient Backgrounds

**Banned:** `background: linear-gradient(135deg, #667eea, #764ba2)` directly on a
container or page surface.

**Why it's slop:** Multi-color surface gradients are the single most recognizable
AI-generation signature. They dominate content hierarchy and make all outputs look
like the same template.

**Correct approach — glow layers, not surface color:**

```css
/* BAD — gradient as surface */
.card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* GOOD — gradient as atmosphere, detached from surface */
.hero-glow::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(ellipse, rgba(99,102,241,0.25) 0%,
              rgba(99,102,241,0.06) 40%, transparent 70%);
  filter: blur(40px);
  pointer-events: none;
}

/* Actual card surface uses near-transparent solid */
.card {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
}
```

**Allowed uses of gradient:**
- `::before` / `::after` pseudo-elements as a blur-filtered glow layer
- `background-clip: text` for text decoration
- Decorative top-border lines: `linear-gradient(90deg, transparent, var(--accent), transparent)`

---

### Rule 2 — No Emoji as Icons

**Banned:** Using 🎨 ✨ 🚀 📊 as functional icons in UI.

**Why it's slop:** Emoji rendering varies across platforms and fonts. More critically,
emoji-as-icon is the fastest path to making a design look AI-generated and generic.

**Exception:** Only if the existing brand/design system already uses emoji as part of
its established visual language.

**Correct approach — SVG line icons or text placeholders:**

```html
<!-- BAD -->
<span class="icon">🚀</span>

<!-- GOOD — 24×24 stroke-based SVG icon -->
<svg width="24" height="24" viewBox="0 0 24 24"
     fill="none" stroke="currentColor"
     stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
  <polyline points="7 10 12 15 17 10"/>
  <line x1="12" y1="15" x2="12" y2="3"/>
</svg>

<!-- GOOD — initials / letter placeholder when no real icon -->
<div class="avatar">L</div>
```

---

### Rule 3 — No Rounded Cards with Left-Border Accent

**Banned:** The combination of `border-radius` + `border-left: Npx solid <color>`.

**Why it's slop:** This three-element combo (rounded corners + colored left border +
gradient fill inside) is the most recognizable AI card pattern. The combination — not
any single element — is the problem.

**Correct approach — uniform border, no directional accent:**

```css
/* BAD — the AI slop trifecta */
.card {
  border-radius: 12px;
  border-left: 4px solid #6366F1;
  background: linear-gradient(135deg, ...);
}

/* GOOD — uniform border, transparent surface */
.card {
  border-radius: var(--radius);   /* 16px is fine — radius alone is not the problem */
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);  /* uniform, all sides */
  padding: 36px;
}

/* GOOD alternative — glassmorphism */
.card {
  border-radius: 12px;
  background: rgba(17, 17, 17, 0.6);
  backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.06);
}
```

---

### Rule 4 — No SVG-Drawn Illustrations

**Banned:** Using SVG to hand-draw decorative images, product mockups, people,
scenes, or any illustration meant to represent real-world objects.

**Why it's slop:** SVG illustrations look cheap, and asking Claude to draw complex
scenes in SVG produces low-fidelity, obviously-AI results.

**Exception:** Functional line icons (stroke-based, 24×24, semantic meaning) are fine.

**Correct approach — placeholders and real assets:**

```html
<!-- BAD — SVG illustration attempting to look like UI -->
<svg><!-- 200 lines of hand-drawn fake UI --></svg>

<!-- GOOD — semantic code placeholder (landing page "product preview" area) -->
<div class="code-preview">
  <pre><code>const result = await api.query({
  model: "claude-opus",
  prompt: userInput,
});</code></pre>
</div>

<!-- GOOD — geometric placeholder with label -->
<div class="img-placeholder" aria-label="Product screenshot">
  <span>Product screenshot</span>
</div>
```

Ask the user for real assets: "I've used a placeholder here — drop in your actual
screenshot when ready."

---

### Rule 5 — No Overused Font Families

**Banned fonts:**
- `Inter`
- `Roboto`
- `Arial`
- `Fraunces`
- System fonts as primary (`system-ui`, `-apple-system` alone)

**Why it's slop:** Inter especially has become the default AI-output font. It signals
"I didn't think about typography."

**Preferred:** `Geist` (Vercel) — modern geometric, low AI-saturation, excellent
readability. Load from Google Fonts or CDN.

```css
/* BAD */
body { font-family: 'Inter', sans-serif; }

/* GOOD */
@import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700&display=swap');
body { font-family: 'Geist', sans-serif; }

/* Acceptable fallback chain */
body { font-family: 'Geist', 'SF Pro Display', sans-serif; }
```

For CJK content: `'Geist', 'Noto Sans SC', sans-serif` is an acceptable combination.

---

## Additional Avoid List

Beyond the 5 core rules, these patterns also produce AI-slop output:

| Pattern | Problem | Fix |
|---------|---------|-----|
| `scrollIntoView()` | Breaks web app scroll behavior | Use `element.scrollTop`, `scrollTo()` |
| Unpinned React versions (`react@18`) | CDN resolves to different version over time | Pin exact: `react@18.3.1` |
| `const styles = {}` global style objects | Collides when multiple components loaded | Name by component: `const cardStyles = {}` |
| Filler stats / data ("10K+ users", "99.9% uptime") | Data slop — meaningless without context | Remove or ask user for real numbers |
| Title screen on prototypes | Wastes user's first impression | Start directly at the real UI |
| Speaker notes without being asked | Clutters the output | Only add when user explicitly requests |
| Multiple HTML files for variants | Hard to compare | Use Tweaks panel to toggle variants |
| Bulk-copying design system assets | Wastes project space | Copy only files actually referenced |