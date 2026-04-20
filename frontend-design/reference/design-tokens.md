# Design Tokens

Token philosophy, color strategy, scale requirements, and typography rules
extracted from the Claude Artifacts design system.

---

## Core Philosophy

CSS custom properties are the **only** sanctioned way to define color, spacing, and
typography in HTML artifacts. Never hard-code hex values in component styles —
always reference a token. This enables Tweaks-driven runtime theming and keeps
the design system maintainable.

**Three laws:**
1. Colors live in `:root` as custom properties.
2. Components consume tokens, never raw values.
3. oklch is for extension only — not the starting point.

---

## Color Priority Chain

```
Brand color / design system color
        ↓ (first choice — always)
Use existing tokens as-is

        ↓ (when palette is too restrictive)
Extend with oklch() — keep hue consistent, vary L and C

        ↓ (never do this)
Invent colors from scratch
```

**Practical decision rule:**
- Have a brand `#` value? Use it. Derive transparency variants from it.
- Need a shade lighter/darker? Convert to oklch, shift L channel, convert back.
- Tempted to pick a "nice color"? Don't. Harmonize with what exists.

---

## oklch Color Space

oklch(L C H) — Lightness, Chroma, Hue.

**Why oklch over HSL:**
HSL's lightness is perceptually non-uniform — blue at L=50% looks much darker than
yellow at L=50%. oklch's L channel maps directly to perceived brightness, so a 10-unit
L shift feels the same regardless of hue.

**Typical use cases:**

```css
/* Extend a brand color into a full shade scale */
:root {
  --accent-base: #6366F1;
  /* oklch equivalent: oklch(0.48 0.16 277) */

  /* Lighter variant: raise L */
  --accent-light: oklch(0.65 0.14 277);

  /* Dimmed variant: lower C (desaturate) */
  --accent-muted-bg: oklch(0.48 0.04 277 / 0.15);

  /* Complementary: rotate H by 180° */
  --accent-complement: oklch(0.55 0.12 97);
}
```

**Workflow for extending an existing color:**
1. Paste hex into an oklch converter (oklch.com or CSS Color 4 tools).
2. Note the H (hue) value. Lock it.
3. Vary L (0.2 → 0.9) for shade scale.
4. Vary C (0.04 → 0.20) for saturation scale.
5. Rotate H ±30°/60° for analogous/complementary harmonics.

---

## Example `:root` Token Block

This is the minimal token set for a dark-theme artifact. Adapt to brand colors.

```css
:root {
  /* ── Backgrounds ── */
  --bg:           #050505;       /* deepest — page bg */
  --bg-2:         #0a0a0a;       /* secondary surface */
  --bg-elevated:  #111111;       /* cards, modals */
  --bg-card:      rgba(17, 17, 17, 0.6); /* glass cards */
  --bg-hover:     rgba(255, 255, 255, 0.04);

  /* ── Borders ── */
  --border:       rgba(255, 255, 255, 0.08); /* standard */
  --border-inner: rgba(255, 255, 255, 0.03); /* subtle dividers */

  /* ── Text ── */
  --text:         #f0f0f0;       /* primary */
  --text-2:       #888888;       /* secondary / captions */
  --text-3:       #555555;       /* tertiary / disabled */

  /* ── Accent ── */
  --accent:       #6366F1;       /* primary action color */
  --accent-hover: #818cf8;       /* interactive hover state */
  --accent-dim:   rgba(99, 102, 241, 0.15); /* muted backgrounds */
  --accent-glow:  rgba(99, 102, 241, 0.40); /* glow effects */

  /* ── Status ── */
  --success:      #22c55e;
  --success-bg:   rgba(34, 197, 94, 0.15);
  --warning:      #f59e0b;
  --warning-bg:   rgba(245, 158, 11, 0.15);
  --danger:       #ef4444;
  --danger-bg:    rgba(239, 68, 68, 0.15);
  --info:         #3b82f6;
  --info-bg:      rgba(59, 130, 246, 0.15);

  /* ── Spacing / Radius ── */
  --radius-sm:    8px;
  --radius:       12px;
  --radius-lg:    16px;
  --radius-xl:    20px;

  /* ── Blur ── */
  --blur-glass:   24px;

  /* ── Animation ── */
  --ease-reveal:  cubic-bezier(0.16, 1, 0.3, 1);  /* spring-like entrance */
  --ease-out:     cubic-bezier(0.0, 0.0, 0.2, 1);
  --duration-fast: 150ms;
  --duration:     300ms;
  --duration-slow: 600ms;
}
```

---

## Token Naming Conventions

| Style | Example | Use for |
|-------|---------|---------|
| Semantic > visual | `--text-secondary` not `--gray-500` | Everything — semantic names survive theme changes |
| Layer suffix | `--bg-card`, `--bg-elevated` | Background hierarchy |
| State suffix | `--accent-hover`, `--accent-dim` | Interactive and opacity variants |
| Status prefix | `--success`, `--danger` | Feedback colors |

**Never name tokens by their raw value:** `--blue-6366f1` tells the consumer nothing
useful and breaks the moment you change the color.

---

## Transparency Strategy (Dark Themes)

Use white-transparency, not fixed gray. Composites naturally over glass/blur layers.

| Layer | Value | Use |
|-------|-------|-----|
| Structural borders | `rgba(255,255,255,0.06)` | Sidebar, nav |
| Content dividers | `rgba(255,255,255,0.03)` | Card internals |
| Hover backgrounds | `rgba(255,255,255,0.04)` | Rows, nav items |
| Glass card bg | `rgba(17,17,17,0.60)` | Floating panels + blur |
| Secondary button | `rgba(255,255,255,0.08)` | Ghost buttons |
| Focus border | `rgba(255,255,255,0.14)` | Input focus ring |

## Accent Derivation

Single accent + transparency — never add a second hue.

```css
--accent:       #6366F1;         /* base — buttons, active */
--accent-hover: #818cf8;         /* hover — +1 shade lighter */
--accent-dim:   rgba(99,102,241,0.15); /* badge backgrounds */
--accent-glow:  rgba(99,102,241,0.40); /* glow effects */
```

## Scale Requirements

| Context | Minimum |
|---------|---------|
| Slide decks (1920×1080) | **24px** text (32–48px headlines) |
| Mobile hit targets | **44px** |
| Print documents | **12pt** |

Slides: use `deck_stage.js` for JS `transform: scale()` letterboxing — never hand-roll.

## Typography, Easing & Slide Backgrounds

**Artifact fallback font (only when project/brand has no specified font):** `'Geist', sans-serif`. CJK fallback: add `'Noto Sans SC'`. Always `text-wrap: pretty`.
**Banned fallback fonts:** Inter, Roboto, Arial, system-ui as sole font.
**Not banned when intentional:** Any font explicitly chosen by the project DESIGN.md or by the user (including Fraunces, Space Grotesk, Playfair, etc.). This section only constrains the *unspecified default*. The guidance in `reference/typography.md` on distinctive font pairing takes precedence over this fallback.

Easing: `--ease-reveal: cubic-bezier(0.16,1,0.3,1)` (spring/reveals) · `--ease-out: cubic-bezier(0,0,0.2,1)`.

**Slide decks:** max 2 bg colors, named by slot (`--bg-01`, `--bg-02`). Pair with `--text-on-dark` / `--text-on-light` for contrast. Apply via `.slide--dark` / `.slide--light` classes.
```
