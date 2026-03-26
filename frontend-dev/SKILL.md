---
name: frontend-dev
description: Frontend UI development with premium animations (Framer Motion, GSAP) and MiniMax API integration (TTS, image, video). AIDA copywriting framework for landing pages. Trigger when building React/Next.js UIs with advanced animations or MiniMax media generation.
type: skill
github_url: https://github.com/MiniMax-AI/skills
github_hash: b4c7c3fcd4d8c1f6e2a3d7b9c5e1f4a8d2b7c3e9
version: 1.0.0
---

# Frontend Development with MiniMax

React/Next.js UI development with cinematic animations and MiniMax multi-modal integration.

## UI + Animation Development (No MiniMax API needed)

When building UI without MiniMax generation:

### Framer Motion Spring Presets

```javascript
const springs = {
    snappy: { stiffness: 300, damping: 30 },
    smooth: { stiffness: 150, damping: 20 },
    bouncy: { stiffness: 100, damping: 10 },
    heavy: { stiffness: 60, damping: 20 },
};
```

### 10 Animation Recipes

| Recipe | Tool | Key Code |
|--------|------|----------|
| Scroll Reveal | Framer | `<motion.div initial={{opacity:0,y:50}} whileInView={{opacity:1,y:0}}>` |
| Stagger Grid | Framer | `staggerChildren: 0.1` on parent |
| Pinned Timeline | GSAP | `ScrollTrigger.pin()`, horizontal scroll |
| Tilt Card | Framer | `onMove={{i,d}} rotateX:${d*5} rotateY:${d*5}` |
| Magnetic Button | Framer | `whileHover={{scale:1.1}}` on icon |
| Text Scramble | Vanilla | `chars.reduce((a,c)=>a+CHARS[Math.random()|0],'')` |
| SVG Path Draw | CSS | `stroke-dashoffset` animation |
| Horizontal Scroll | GSAP | `gsap.to(container, {x: -totalWidth})` |
| Particle Background | R3F | Three.js points with noise |
| Layout Morph | Framer | `<AnimatePresence>` for card→modal |

### NEVER
- Mix GSAP + Framer Motion in the same component
- Put R3F (React Three Fiber) in same component tree — use isolated Canvas wrapper
- Use GSAP context improperly — always `gsap.context(() => {}, ref)` cleanup
- Skip `prefers-reduced-motion` media query check

## MiniMax API Integration

### TTS in React Component

```typescript
// Call the TTS script from frontend
import { exec } from 'child_process';
import path from 'path';

async function generateTTS(text: string, outputPath: string) {
    const scriptPath = path.join(process.cwd(), 'scripts', 'minimax_tts.py');
    return new Promise((resolve, reject) => {
        exec(`python "${scriptPath}" "${text}" -o "${outputPath}"`, (err, stdout, stderr) => {
            if (err) reject(err);
            else resolve(stdout);
        });
    });
}
```

### Image Generation in Next.js API Route

```typescript
// app/api/generate-image/route.ts
import { spawn } from 'child_process';
import path from 'path';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
    const { prompt, ratio } = await req.json();
    const script = path.join(process.cwd(), 'scripts', 'minimax_image.py');
    const output = `/tmp/${Date.now()}.png`;

    return new Promise((resolve) => {
        const p = spawn('python', [script, '--prompt', prompt, '-o', output, '--ratio', ratio || '1:1']);
        let stdout = '', stderr = '';
        p.stdout.on('data', d => stdout += d);
        p.stderr.on('data', d => stderr += d);
        p.on('close', () => {
            if (p.exitCode !== 0) resolve(NextResponse.json({ error: stderr }, { status: 500 }));
            else resolve(NextResponse.json({ output }));
        });
    });
}
```

## AIDA Copywriting Framework

For landing pages and persuasive UI text:

### AIDA Structure

```
ATTENTION: Bold headline (promise or pain point)
INTEREST: Elaborate the problem ("yes, that's me")
DESIRE: Show transformation (before/after)
ACTION: Clear CTA
```

### Headline Formulas

| Type | Formula |
|------|---------|
| Promise | "Get [specific outcome]" |
| Question | "Tired of [problem]?" |
| How-To | "How to [achieve goal] in [timeframe]" |
| Negative | "Stop [common mistake]" |
| Transformation | "From [before] to [after]" |

### CTA Formulas

`[Action Verb] + [What They Get] + [Urgency/Ease]`

**Good**: "Start my free trial", "Get the template now", "Book my strategy call"
**Bad**: "Submit", "Click here", "Learn more"

## Performance Rules

- Only GPU properties: `transform`, `opacity`, `filter`, `clip-path`
- Always lazy-load: Lottie, GSAP, Three.js
- Use `will-change` sparingly (remove after animation)
- Keep Framer Motion variants stable (memoize outside component)

## Tech Stack Defaults

- React 18 + Next.js 14 App Router
- Tailwind CSS for styling
- Framer Motion for animations
- MiniMax scripts in `scripts/` directory (not in components)
