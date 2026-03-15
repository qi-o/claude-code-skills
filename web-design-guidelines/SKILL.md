---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance. Use when asked to "review my UI", "check accessibility", "audit design", "review UX", "check my site against best practices", "检查可访问性", "审查界面", "UI审查", "检查组件的可访问性", "审查一下这个页面", "a11y check", "accessibility audit". Do NOT use for general code review unrelated to UI/UX (use code-reviewer instead).
github_url: https://github.com/vercel-labs/agent-skills
github_hash: 5847a7c7e79bab3e400cf47800b83449d7aea2d4
version: 1.2.0
created_at: 2026-01-27
platform: github
source: https://github.com/vercel-labs/agent-skills/tree/main/skills/web-design-guidelines
stars: 17000
language: JavaScript
author: vercel
tags: [ui, ux, accessibility, a11y, web, design, review, audit]
license: MIT
metadata:
  category: code-quality
---

# Web Design Guidelines

Review UI code for Vercel Web Interface Guidelines compliance. This skill provides 100+ actionable rules across 16 categories for building production-ready web interfaces.

## How It Works

1. Fetch the latest guidelines from the source URL before each review
2. Read the specified files (or prompt user for files/pattern)
3. Check against all rules in the fetched guidelines
4. Output findings in terse `file:line` format

**Guidelines Source:**
```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

## Usage

**Triggers:**
- "review my UI"
- "check accessibility"
- "audit design"
- "review UX"
- "check my site against best practices"
- "妫€鏌ヨ繖涓粍浠剁殑鍙闂€?
- "瀹℃煡涓€涓嬭繖涓〉闈?

**With file pattern:**
```
Review src/components/*.tsx for web design guidelines
```

## Rule Categories (100+ Rules)

### 1. Accessibility (13 rules)
- Icon-only buttons require `aria-label`
- Form controls need `<label>` or `aria-label`
- Interactive elements need keyboard handlers (`onKeyDown`/`onKeyUp`)
- Use `<button>` for actions, `<a>`/`<Link>` for navigation (not `<div onClick>`)
- Images need `alt` attribute (or `alt=""` for decorative)
- Decorative icons need `aria-hidden="true"`
- Async updates need `aria-live="polite"` for toasts/validation
- Prefer semantic HTML before ARIA attributes
- Hierarchical headings `<h1>`鈥揱<h6>` with skip link for main content
- `scroll-margin-top` on heading anchors

### 2. Focus States (4 rules)
- Visible focus indicators: `focus-visible:ring-*` or equivalent
- Never remove outlines without replacement
- Use `:focus-visible` over `:focus` to avoid click focus rings
- Group focus with `:focus-within` for compound controls

### 3. Forms (12 rules)
- Inputs need `autocomplete` and meaningful `name`
- Correct input `type` (`email`, `tel`, `url`, `number`) and `inputmode`
- Never block paste functionality
- Clickable labels via `htmlFor` or wrapping
- Disable spellcheck on emails/codes/usernames
- Checkboxes/radios share single hit target with label
- Submit button enabled until request starts; show spinner during request
- Inline errors next to fields; focus first error on submit
- Placeholders end with `鈥 showing example patterns
- `autocomplete="off"` on non-auth fields
- Warn before navigation with unsaved changes

### 4. Animation (6 rules)
- Honor `prefers-reduced-motion` media query
- Animate only `transform`/`opacity` (compositor-friendly)
- Never `transition: all`鈥攍ist properties explicitly
- Set correct `transform-origin`
- SVG transforms on `<g>` wrapper with `transform-box: fill-box`
- Animations must be interruptible

### 5. Typography (6 rules)
- Use `鈥 not `...`
- Curly quotes `"` `"` not straight `"`
- Non-breaking spaces: `10&nbsp;MB`, `鈱?nbsp;K`
- Loading states end with `鈥: `"Loading鈥?`
- `font-variant-numeric: tabular-nums` for number columns
- `text-wrap: balance` or `text-pretty` on headings

### 6. Content Handling (4 rules)
- Text containers handle overflow: `truncate`, `line-clamp-*`, `break-words`
- Flex children need `min-w-0` for text truncation
- Handle empty states gracefully
- Anticipate short, average, and very long user inputs

### 7. Images (3 rules)
- Explicit `width` and `height` to prevent CLS
- Below-fold: `loading="lazy"`
- Above-fold critical: `priority` or `fetchpriority="high"`

### 8. Performance (7 rules)
- Virtualize large lists (>50 items)
- No layout reads in render (`getBoundingClientRect`, etc.)
- Batch DOM reads/writes
- Prefer uncontrolled inputs
- `<link rel="preconnect">` for CDN/asset domains
- Critical fonts: `<link rel="preload" as="font">` with `font-display: swap`

### 9. Navigation & State (4 rules)
- URL reflects state via query params
- Links use `<a>`/`<Link>` for Cmd/Ctrl+click support
- Deep-link stateful UI
- Destructive actions need confirmation or undo

### 10. Touch & Interaction (5 rules)
- `touch-action: manipulation` prevents double-tap delay
- Set `-webkit-tap-highlight-color` intentionally
- `overscroll-behavior: contain` in modals/drawers
- Disable text selection during drag
- `autoFocus` sparingly鈥攄esktop only, avoid mobile

### 11. Safe Areas & Layout (3 rules)
- Full-bleed layouts need `env(safe-area-inset-*)`
- Avoid unwanted scrollbars with `overflow-x-hidden`
- Flex/grid over JS measurement

### 12. Dark Mode & Theming (3 rules)
- `color-scheme: dark` on `<html>` for dark themes
- `<meta name="theme-color">` matches background
- Native `<select>`: explicit colors for Windows dark mode

### 13. Locale & i18n (3 rules)
- Use `Intl.DateTimeFormat` not hardcoded formats
- Use `Intl.NumberFormat` for numbers/currency
- Detect language via `Accept-Language`/`navigator.languages`

### 14. Hydration Safety (3 rules)
- Inputs with `value` need `onChange` (or use `defaultValue`)
- Guard date/time rendering against hydration mismatch
- `suppressHydrationWarning` only where necessary

### 15. Hover & Interactive States (2 rules)
- Buttons/links need `hover:` state (visual feedback)
- Interactive states increase contrast: hover/active/focus more prominent than rest

### 16. Content & Copy (7 rules)
- Active voice preferred
- Title Case for headings/buttons
- Numerals for counts
- Specific button labels
- Error messages include fixes
- Second person voice
- `&` over "and" where space-constrained

## Anti-patterns to Flag

These patterns should be flagged during review:

| Anti-pattern | Issue |
|--------------|-------|
| `user-scalable=no` | Disabling zoom hurts accessibility |
| Blocking paste | Frustrates users, breaks password managers |
| `transition: all` | Performance issue, animate specific properties |
| `outline-none` without replacement | Removes focus visibility |
| `<div onClick>` for navigation | Breaks Cmd/Ctrl+click, accessibility |
| Images without dimensions | Causes layout shift (CLS) |
| Large arrays without virtualization | Performance issue |
| Form inputs without labels | Accessibility violation |
| Icon buttons without `aria-label` | Screen readers can't identify |
| Hardcoded date/number formats | i18n issue |
| Unjustified `autoFocus` | Problematic on mobile |

## Output Format

Findings are output in terse format:

```
src/components/Button.tsx:42 - Icon button missing aria-label
src/components/Form.tsx:15 - Input missing associated label
src/components/Modal.tsx:8 - Missing overscroll-behavior: contain
```

## Resources

- [Web Interface Guidelines Source](https://github.com/vercel-labs/web-interface-guidelines)
- [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills)
