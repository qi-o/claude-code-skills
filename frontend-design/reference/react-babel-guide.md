# React + Babel Inline JSX Guide

Rules for writing React prototypes with inline JSX in HTML artifacts.
All rules are non-negotiable — violations cause silent runtime breakage.

---

## Pinned CDN Versions (Mandatory)

Always use these exact script tags. Never use unpinned versions (`react@18`) or omit
integrity attributes. Unpinned CDN references resolve to different versions over time
and break reproducibility.

```html
<script src="https://unpkg.com/react@18.3.1/umd/react.development.js"
        integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L"
        crossorigin="anonymous"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js"
        integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm"
        crossorigin="anonymous"></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js"
        integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y"
        crossorigin="anonymous"></script>
```

Load order: React → ReactDOM → Babel → your component files → your main script.

---

## No `type="module"` on Babel Scripts

Babel-transpiled scripts must NOT use `type="module"`:

```html
<!-- BAD — breaks Babel transpilation -->
<script type="module" src="components.jsx"></script>

<!-- GOOD -->
<script type="text/babel" src="components.jsx"></script>

<!-- GOOD — inline JSX -->
<script type="text/babel">
  function App() { return <div>Hello</div>; }
  ReactDOM.createRoot(document.getElementById('root')).render(<App />);
</script>
```

---

## Style Object Naming (Critical)

Each `<script type="text/babel">` gets its own transpiled scope — but style objects
assigned to generic names **collide** when multiple component files are loaded.

**Rule: NEVER write `const styles = {}`.**
Always name style objects after the component they belong to.

```js
// BAD — will be overwritten if any other component also uses `styles`
const styles = {
  container: { padding: '24px' },
};

// GOOD — component-specific name
const cardStyles = {
  container: { padding: '24px' },
  header: { fontSize: '18px', fontWeight: 600 },
};

const terminalStyles = {
  container: { background: '#0a0a0a', fontFamily: 'monospace' },
  line: { color: '#22c55e' },
};
```

Alternatives to named style objects:
- Inline styles directly in JSX: `style={{ padding: '24px' }}`
- CSS classes via `:root` tokens in a `<style>` tag

---

## Cross-File Component Sharing

Each `<script type="text/babel">` has isolated scope after transpilation.
To share components between files, export them to `window` at the end of the
file that defines them.

```js
// components.jsx — define and export to window
function Terminal({ children }) {
  return <div className="terminal">{children}</div>;
}

function Line({ children, color = '#22c55e' }) {
  return <div style={{ color }}>{children}</div>;
}

// Export all shared components at the end of the file
Object.assign(window, {
  Terminal,
  Line,
  // ... every component other scripts need
});
```

```js
// main.jsx — consume from window (no import statement needed)
function App() {
  const { Terminal, Line } = window;
  return (
    <Terminal>
      <Line>$ npm run dev</Line>
    </Terminal>
  );
}
```

The `Object.assign(window, {...})` pattern makes components globally available to
all subsequent `<script type="text/babel">` blocks.

---

## Minimal Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Design Artifact</title>
  <script src="https://unpkg.com/react@18.3.1/umd/react.development.js"
          integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L"
          crossorigin="anonymous"></script>
  <script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js"
          integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm"
          crossorigin="anonymous"></script>
  <script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js"
          integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y"
          crossorigin="anonymous"></script>
  <style>
    :root { --bg:#050505; --fg:#f0f0f0; --accent:#6366F1;
            --border:rgba(255,255,255,0.08); --radius:12px;
            --font:'Geist',sans-serif; }
    *{box-sizing:border-box;margin:0;padding:0}
    body{background:var(--bg);color:var(--fg);font-family:var(--font);
         min-height:100vh;display:flex;align-items:center;justify-content:center}
  </style>
</head>
<body>
  <div id="root"></div>
  <script>
    /* Exactly one EDITMODE block per root file — valid JSON inside */
    const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{"primaryColor":"#6366F1","fontSize":16,"dark":true}/*EDITMODE-END*/;
  </script>
  <!-- <script type="text/babel" src="components.jsx"></script> -->
  <script type="text/babel">
    const { useState } = React;

    /* Name style objects after their component — NEVER `const styles = {}` */
    const appStyles = {
      card: { background:'rgba(255,255,255,0.04)', border:'1px solid var(--border)',
              borderRadius:'12px', padding:'36px', maxWidth:'480px' },
    };

    function App() {
      return <div style={appStyles.card}><h1>Replace me</h1></div>;
    }

    /* Register listener BEFORE posting __edit_mode_available */
    window.addEventListener('message', (e) => {
      if (e.data?.type === '__activate_edit_mode') { /* show panel */ }
      if (e.data?.type === '__deactivate_edit_mode') { /* hide panel */ }
    });
    window.parent.postMessage({ type: '__edit_mode_available' }, '*');

    ReactDOM.createRoot(document.getElementById('root')).render(<App />);
  </script>
</body>
</html>
```

## Quick Rules Checklist

- [ ] React + ReactDOM + Babel pinned with integrity hashes (versions above, exact)
- [ ] No `type="module"` on Babel script tags
- [ ] Style objects named per component — never `const styles = {}`
- [ ] Cross-file components exported via `Object.assign(window, {...})`
- [ ] Exactly one `EDITMODE-BEGIN/END` block per root HTML file
- [ ] Tweaks listener registered BEFORE `__edit_mode_available` is posted
- [ ] `localStorage` used for slide/video position persistence
- [ ] No `scrollIntoView()` anywhere

**Animations:** use `animations.jsx` starter for timeline motion. Popmotion
(`popmotion@11.0.5`) only if starter genuinely can't cover the use case.
CSS transitions + React state are sufficient for interactive prototypes.
