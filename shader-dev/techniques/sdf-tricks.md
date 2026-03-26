# SDF Tricks

## Optimization

```glsl
// Bounding volume
float map(vec3 p) {
    if (!inBoundingBox(p)) return OUTSIDE;
    // expensive SDF computation
}

// Binary search refinement
float refine(float d, vec3 p, vec3 rd) {
    float t = abs(d);
    for(int i = 0; i < 3; i++) {
        t += sdScene(p + rd * t) * 0.5;
    }
    return t;
}
```

## Hollowing

```glsl
float opHollow(float d, float r) { return abs(d) - r; }
```

## Layered Edges

```glsl
// Extrude with beveled edge
float opExtrudeBevel(float d2d, float pz, float h, float r) {
    float d = max(d2d, abs(pz) - h);
    vec2 w = vec2(d, abs(pz) - h - r);
    return min(max(w.x, w.y), 0.0) + length(max(w, 0.0)) - r;
}
```
