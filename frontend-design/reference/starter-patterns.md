# Starter Patterns

Index of ready-made scaffold components for HTML artifacts.
Each entry covers: use case, contract, and copy-paste instructions.

Actual starter source files live in `../starters/` (relative to this `reference/` directory).
This file describes the usage contract so you can slot your design into the scaffold
correctly.

---

## When to Use Starters

Always prefer a starter over hand-rolling for:
- Slide decks (deck_stage.js handles scaling, nav, persistence, PDF)
- Device mockups (ios_frame, android_frame, macos_window, browser_window)
- Multi-option design comparisons (design_canvas.jsx)
- Timeline animations (animations.jsx)

Do not hand-roll these — the starters provide contracts the host environment
depends on (postMessage events, data attributes, localStorage keys).

---

## Starter Index

### `starters/deck_stage.js` — Slide Decks

**Use case:** Any slide presentation — conference talks, design reviews, product
decks, pitches.

**What it provides:**
- Fixed 1920×1080 canvas with JS `transform: scale()` letterboxing to any viewport
- Keyboard navigation: `ArrowLeft` / `ArrowRight` / `Space`
- Touch/tap navigation
- Slide-count overlay (`{current}/{total}`)
- `localStorage` persistence of current slide position
- Print-to-PDF (one page per slide)
- Auto-tags every slide with `data-screen-label` and `data-om-validate`
- Posts `{ slideIndexChanged: N }` to parent for speaker-notes sync

**Usage contract:**

```html
<!-- 1. Load the starter (plain JS, not Babel) -->
<script src="starters/deck_stage.js"></script>

<!-- 2. Wrap slides in <deck-stage> -->
<deck-stage>
  <!-- Each <section> is one slide -->
  <section data-screen-label="01 Title">
    <h1>Your Title</h1>
  </section>

  <section data-screen-label="02 Agenda">
    <h2>Agenda</h2>
    <ul>
      <li>Point one</li>
      <li>Point two</li>
    </ul>
  </section>
</deck-stage>

<!-- 3. Speaker notes (optional — only if user asks) -->
<script type="application/json" id="speaker-notes">
["Notes for slide 1", "Notes for slide 2"]
</script>
```

**Critical rules:**
- Slide labels are **1-indexed**: "01 Title", "02 Agenda", not "00 Title".
- When user says "slide 5", they mean the 5th slide (label "05"), not array index [4].
- Nav controls must live **outside** the scaled element so they stay usable on small screens.
- Do NOT add speaker notes unless the user explicitly asks.
- `window.postMessage({ slideIndexChanged: N })` is called by the component automatically.

**localStorage key:** `deck_stage_index` (auto-managed by component).

---

### `starters/design_canvas.jsx` — Multi-Option Side-by-Side

**Use case:** Presenting 2 or more static design options in a labeled grid for
comparison. Use when exploring color, type, layout, or component variants
that should be seen together.

**What it provides:**
- Responsive grid of labeled cells
- Each cell gets a visible label ("Option A", "Option B", or custom)
- Consistent padding and border between cells
- Print-friendly layout

**Usage contract:**

```jsx
// Load with Babel (JSX)
// <script type="text/babel" src="starters/design_canvas.jsx"></script>

function MyDesigns() {
  return (
    <DesignCanvas columns={3} label="Color Exploration">
      <DesignCanvas.Cell label="Minimal Dark">
        {/* Your first design variant here */}
        <Card theme="dark-minimal" />
      </DesignCanvas.Cell>

      <DesignCanvas.Cell label="Bold Accent">
        <Card theme="bold-accent" />
      </DesignCanvas.Cell>

      <DesignCanvas.Cell label="Light + Warm">
        <Card theme="light-warm" />
      </DesignCanvas.Cell>
    </DesignCanvas>
  );
}
```

**When to use vs. Tweaks:**
- `design_canvas` → options meant to be compared side-by-side simultaneously
- Tweaks → options meant to be toggled on/off in a single prototype view

---

### `starters/animations.jsx` — Timeline Animation Engine

**Use case:** Video-style motion design, animated explainers, product demos.

**Provides:** `<Stage duration>` (auto-scales, scrubber, play/pause), `<Sprite start end>` (timeline element), `useTime()`, `useSprite()`, `Easing`, `interpolate(progress, from, to)`.

```jsx
function MyAnimation() {
  return (
    <Stage duration={5000}>
      <Sprite start={0} end={0.2}>
        {({ progress }) => (
          <h1 style={{ opacity: Easing.easeOut(progress),
                       transform: `translateY(${interpolate(progress,40,0)}px)` }}>
            Hello
          </h1>
        )}
      </Sprite>
    </Stage>
  );
}
```

Rules: center within viewport, no title screen, no Popmotion unless Stage/Sprite genuinely can't cover the use case.

---

### `starters/device_frames/` — Device Chrome

**Use case:** Wrapping prototypes in realistic device bezels. Do not hand-draw these.

| File | Component | Provides |
|------|-----------|----------|
| `ios_frame.jsx` | `<IOSFrame>` | iPhone 15 Pro bezel, dynamic island, status bar, home indicator |
| `android_frame.jsx` | `<AndroidFrame>` | Material device shape, status bar, gesture/button nav |
| `macos_window.jsx` | `<MacOSWindow title width height>` | Traffic light buttons, title bar, window shadow |
| `browser_window.jsx` | `<BrowserWindow url width height>` | Tab bar, address bar, browser controls |

```jsx
// All device frames — load as Babel script, wrap your content as children
<IOSFrame><AppScreen /></IOSFrame>
<MacOSWindow title="My App" width={900} height={600}><AppContent /></MacOSWindow>
```

---

## Starter Selection Guide

| What you're building | Use |
|---------------------|-----|
| Any slide presentation | `deck_stage.js` |
| 2+ options to compare visually | `design_canvas.jsx` |
| Animated / motion design | `animations.jsx` |
| Mobile app mockup | `ios_frame.jsx` or `android_frame.jsx` |
| Desktop app mockup | `macos_window.jsx` |
| Website / web app mockup | `browser_window.jsx` |
| No above — hi-fi prototype | Start from `react-babel-guide.md` template |

---

## Loading Starters

Copy the file from `starters/<name>` into your project. Extension is required — `deck_stage` fails, `deck_stage.js` works.

- `.js` files → `<script src="starters/deck_stage.js"></script>`
- `.jsx` files → `<script type="text/babel" src="starters/design_canvas.jsx"></script>`
- Device frames → `<script type="text/babel" src="starters/device_frames/ios_frame.jsx"></script>`
