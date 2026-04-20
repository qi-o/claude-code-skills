# Workflow Deep-Dive

Six-step design artifact workflow with gates, common mistakes, and concrete
examples for each step.

---

## Step 1 — Understand

**Goal:** Know exactly what you're building before touching code.

### What to do

1. **Classify the output format** using this selector:

   | Signal in request | Format |
   |------------------|--------|
   | "slide deck", "presentation", "pitch" | `deck_stage.js` web component |
   | "animation", "motion", "video-style" | `animations.jsx` (Stage/Sprite/Easing) |
   | "compare options", "show variations side by side" | `design_canvas.jsx` |
   | "prototype", "app mockup", "interactions", "flows" | Hi-fi prototype + Tweaks |
   | "color", "typography", "layout exploration" of one element | `design_canvas.jsx` |

2. **Determine if `questions_v2` is needed:**

   | Request type | Action |
   |-------------|--------|
   | Vague / open-ended ("make a deck about X") | Use `questions_v2`, 10+ questions |
   | Full spec given (audience, length, content source) | Skip, start immediately |
   | Small tweak or follow-up | Skip, execute directly |
   | Screenshot → prototype (behavior obvious from image) | Skip or ask 1–2 targeted questions |
   | New product prototype from scratch | Use `questions_v2`, ask many questions |

3. **Confirm design context exists** — always check if the user has:
   - A UI kit or design system
   - A codebase to import
   - Brand assets (logo, colors, fonts)
   - Reference screenshots or Figma links

   If none exist, say so in a question (not just text output) and request context.
   **Mocking a full product from scratch is a last resort and will lead to poor design.**

### Gates (must pass before Step 2)
- [ ] Output format chosen
- [ ] Decision made on questions_v2 (use or skip, with rationale)
- [ ] Design context confirmed or explicitly acknowledged as missing

### Common mistakes
- Starting to code before confirming the output format
- Skipping `questions_v2` for genuinely ambiguous requests
- Assuming the user has no design context without asking

---

## Step 2 — Explore Context

**Goal:** Read all relevant design files before writing a single component.

### What to do

1. **Read design system files in this order:**
   - Color tokens: `theme.ts`, `colors.ts`, `tokens.css`, `_variables.scss`
   - Component files matching what the user mentioned
   - Global stylesheets and layout scaffolds

2. **Lift exact values** — do not paraphrase or approximate:
   - Hex codes: copy verbatim
   - Spacing scale: copy every step
   - Font stacks: copy the full stack including fallbacks
   - Border radii: copy the token name and value

3. **For GitHub repos:** Use the full chain:
   `list files → import files → read imported files`.
   Do not build from training-data memory of what an app "roughly looks like."

4. **When no design system is provided:**
   - Invoke the **Frontend design** skill for aesthetic direction
   - Do not invent colors from scratch — see `design-tokens.md`

Gates: token files read, exact values extracted (no approximations), only referenced files copied.

Mistakes: skipping global tokens, approximating colors, bulk-copying entire design system folders.

---

## Step 3 — Plan

Before writing code, write a comment block stating the design system in play:

```html
<!-- DESIGN SYSTEM: Tokens: ./tokens.css | Font: Geist 400/600 |
     Accent: #6366F1 → dim 15% → glow 40% | Radius: 12px | Grid: 12-col 24px gap
     Components: Sidebar, TopBar, StatCard | Variations: by-the-book / bold / editorial -->
```

For decks: commit to layout patterns (section header / title+body / full-bleed) and max 2 bg colors.
For prototypes: decide Tweaks surface (what params, defaults, panel vs. inline handles) before building.
List 3+ variations across dimensions (safe/conventional, color-forward, editorial/type-dominant).
Create a todo list for multi-part work.

Gates: system comment written, 3+ variations defined, Tweaks surface planned, todo list created.
- [ ] Todo list created for 3+ component tasks

### Common mistakes
- Skipping the system comment block (leads to inconsistent decisions mid-build)
- Planning only 1 variation
- Not deciding on background colors for decks before building slides

---

## Step 4 — Build

**Goal:** Implement the design with discipline.

### What to do

Structural rules:
- Split files > 1000 lines into multiple JSX files; import into a main file at the end
- Persist playback position via `localStorage` for slides and video content
- Put `[data-screen-label]` on every slide/screen (1-indexed: "01 Title", "02 Agenda")
- Add `text-wrap: pretty` to all prose text
- Use CSS Grid as the primary layout tool

React/Babel rules (see `react-babel-guide.md` for full details):
- Pinned CDN versions with integrity hashes — always
- No `type="module"` on Babel scripts
- Style objects named per component — never `const styles = {}`
- Cross-file components exported via `Object.assign(window, {...})`

Content discipline:
- Never pad with filler text or dummy stats
- Never add sections the user didn't ask for — ask first
- Placeholder > bad attempt at real imagery (geometric shape + label)
- Only add emoji if the brand uses them

For multiple variants:
- Expose via Tweaks panel, not separate HTML files
- One `EDITMODE-BEGIN/END` block per root file

Device mockups:
- Use `ios_frame.jsx`, `android_frame.jsx`, etc. — do not hand-draw bezels
- Never add a "title" screen to prototypes — center within viewport

### Gates
- [ ] File under 1000 lines OR properly split + imported
- [ ] localStorage persistence for slides/video
- [ ] All slides have 1-indexed `data-screen-label`
- [ ] No `const styles = {}` anywhere
- [ ] No `scrollIntoView()` anywhere
- [ ] No filler content
- [ ] Tweaks listener registered BEFORE `__edit_mode_available` is posted

### Common mistakes
- Writing `const styles = {}` when importing multiple components
- Building multiple HTML files for variants (use Tweaks instead)
- Adding a hero/title screen to a prototype
- Using `scrollIntoView()` for any scroll behavior

---

## Step 5 — Verify

**Goal:** Confirm the artifact loads and runs without errors.

### Claude Code adaptation

The original workflow uses `done` (opens file, returns console errors) and
`fork_verifier_agent` (spawns a background subagent to check layout + JS).

In Claude Code, replicate this pattern:

**Step 5a — Open and check:**
1. Open the HTML file in a browser or the Claude Code preview pane.
2. Check the browser console (F12 → Console tab).
3. Gate: **zero errors** before proceeding.

**Step 5b — Fix errors:**
If errors appear:
- Read the error message fully before changing anything
- Fix the root cause (not a try/catch wrapper)
- Reload; verify the error is gone
- Repeat until the console is clean

**Step 5c — Dispatch verifier:**
Once console is clean, dispatch a `verifier` agent:
```
Task: "Check layout, JS behavior, and console errors for [filename].
Specifically verify: [list any areas you're uncertain about]."
```

Do not consider the artifact done until the verifier reports clean.

**Directed checks** (mid-task, not end-of-turn):
If you need to check something specific ("does the animation timing look right?"),
dispatch `verifier` with a focused task string. You do not need to wait for a
full pass — just the specific check.

### Gates
- [ ] Console is zero-error
- [ ] Verifier agent dispatched and returned clean
- [ ] All slides/screens render without layout breakage
- [ ] Tweaks panel appears and functions (if implemented)
- [ ] localStorage persistence verified (refresh → same slide/state)

### Common mistakes
- Declaring done without opening the browser
- Fixing errors with try/catch instead of fixing the root cause
- Not dispatching the verifier agent
- Checking only the happy path (not refreshing, not testing keyboard nav)

---

## Step 6 — Summarize

2–4 lines max. Caveats (placeholders to replace) + concrete next steps only.
Do not recap what was built. Do not add generic encouragement.

Example: "Hero image is a placeholder — drop in your actual screenshot. Next: request
speaker notes, PDF export via Ctrl+P, or Tweaks panel for color/font customization."

## questions_v2 Rules

Full template: `../SKILL.md` § questions_v2 Checklist.

- Lead with `design_context` then `variation_count` — most critical first
- `text-options` must always include "Explore a few options", "Decide for me", "Other"
- Sliders: be generous with ranges — users go further than expected
- Minimum 10 questions + at least 4 task-specific ones
- One round only — never plan a follow-up questioning round
- Ask only what you cannot discover by reading project files
