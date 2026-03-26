# Domain Repetition

## Infinite Repetition

```glsl
vec3 opRep(vec3 p, vec3 c) { return mod(p + 0.5 * c, c) - 0.5 * c; }
float repSphere(vec3 p, float r, vec3 cell) {
    vec3 q = opRep(p, cell);
    return sdSphere(q, r);
}
```

## Limited Repetition

```glsl
vec3 opRepLim(vec3 p, vec3 c, vec3 lim) {
    return p - c * clamp(round(p / c), -lim, lim);
}
```

## Folding

```glsl
// Mirror fold
vec3 opFold(vec3 p, vec3 n) { return p - 2.0 * n * min(0.0, dot(p, n)); }
// Box fold
vec3 opBoxFold(vec3 p, vec3 lim) { return clamp(p, -lim, lim) * 2.0 - p; }
// Sierpinski fold
vec3 opSierpinskiFold(vec3 p) {
    p.xy = abs(p.xy);
    if(p.x < p.y) p.xy = p.yx;
    p.xz = abs(p.xz);
    if(p.x < p.z) p.xz = p.zx;
    return p;
}
```
