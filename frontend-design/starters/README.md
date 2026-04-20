# Starter Components

Copy-paste-ready scaffolds for design artifacts. Drop them in, slot your design content in, done.

## Which starter for which use case

| File | Use case |
|------|----------|
| `deck_stage.js` | Any slide presentation / deck |
| `design_canvas.jsx` | Showing 2+ design options side-by-side |
| `animations.jsx` | Animated video / motion design with a timeline |
| `device_frames/ios_frame.jsx` | iPhone 15 Pro bezel mockup |
| `device_frames/android_frame.jsx` | Pixel-style Android bezel mockup |
| `device_frames/macos_window.jsx` | macOS window chrome mockup |
| `device_frames/browser_window.jsx` | Browser chrome mockup |

---

## React + Babel CDN tags

Copy these exactly — pinned versions with integrity hashes.

```html
<script src="https://unpkg.com/react@18.3.1/umd/react.development.js" integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L" crossorigin="anonymous"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js" integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm" crossorigin="anonymous"></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js" integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y" crossorigin="anonymous"></script>
```

---

## How to load each starter

### `deck_stage.js` — plain `<script src>`

```html
<script src="deck_stage.js"></script>

<deck-stage>
  <section style="background:#0a0a0b; color:#fff; display:flex; align-items:center; justify-content:center;">
    <h1>Slide 1</h1>
  </section>
  <section style="background:#f5f0eb; display:flex; align-items:center; justify-content:center;">
    <h1>Slide 2</h1>
  </section>
</deck-stage>
```

Speaker notes (optional, parsed automatically):

```html
<script type="application/json" id="speaker-notes">
["Notes for slide 1.", "Notes for slide 2."]
</script>
```

### JSX starters — `<script type="text/babel" src>`

Load React + Babel first, then any JSX starters, then your own code:

```html
<!-- 1. React + Babel -->
<script src="https://unpkg.com/react@18.3.1/umd/react.development.js" ...></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js" ...></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js" ...></script>

<!-- 2. Starter (exports components to window) -->
<script type="text/babel" src="design_canvas.jsx"></script>

<!-- 3. Your design code (DesignCanvas and CanvasCell are now on window) -->
<script type="text/babel">
  ReactDOM.createRoot(document.getElementById('root')).render(
    <DesignCanvas>
      <CanvasCell label="Option A"><div>Design A</div></CanvasCell>
      <CanvasCell label="Option B"><div>Design B</div></CanvasCell>
    </DesignCanvas>
  );
</script>
```

---

## Cross-file window-export pattern

Every JSX starter exports its components to `window` at the bottom:

```js
Object.assign(window, { DesignCanvas, CanvasCell });
```

This makes them available to any subsequent `<script type="text/babel">` block.
Do NOT use `type="module"` — it breaks Babel's global scope sharing.
Each style object uses a unique name (e.g. `iosFrameStyles`, `androidFrameStyles`) to prevent collisions when multiple starters are loaded together.

---

## Quick component reference

| Component | Key props |
|-----------|-----------|
| `<deck-stage>` | children: `<section>` elements |
| `<DesignCanvas>` | `style?` |
| `<CanvasCell>` | `label`, `style?` |
| `<Stage>` | `totalDuration`, `autoPlay?`, `loop?`, `baseWidth?`, `baseHeight?`, `showControls?` |
| `<Sprite>` | `start` (seconds), `end` (seconds) |
| `<IOSFrame>` | `darkMode?` |
| `<AndroidFrame>` | `darkMode?` |
| `<MacOSWindow>` | `title?`, `darkMode?`, `width?`, `height?` |
| `<BrowserWindow>` | `url?`, `title?`, `darkMode?`, `width?`, `height?` |
