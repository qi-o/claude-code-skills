# Multi-Pass / Buffer Setup

## Ping-Pong FBO

```javascript
// WebGL2: two framebuffers for state persistence
const fbA = gl.createFramebuffer();
const fbB = gl.createFramebuffer();
const texA = createDoubleFBO(fbA, w, h);
const texB = createDoubleFBO(fbB, w, h);
// Each frame: read from texA, write to texB, swap
```

## State Persistence

```glsl
// Buffer A: position
// Buffer B: velocity
// In buffer A shader:
vec4 getPos(ivec2 px) { return texelFetch(uPosA, px, 0); }
vec4 getVel(ivec2 px) { return texelFetch(uVelB, px, 0); }
// Write updated position based on velocity
```

## Common Patterns

```glsl
// Neighbor sampling
vec4 get(vec2 offset) { return texelFetch(uBuffer, ivec2(gl_FragCoord.xy) + ivec2(offset), 0); }

// Accumulation
vec4 accum = vec4(0.0);
for(int i = 0; i < 4; i++) {
    accum += texelFetch(uBuffer, ivec2(gl_FragCoord.xy) + offsets[i], 0);
}
```
