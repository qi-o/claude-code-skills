# 2D Procedural Patterns

## Brick Pattern

```glsl
vec2 brick(vec2 uv, float rows, float cols) {
    uv.x *= cols / rows;
    vec2 id = floor(uv);
    uv.x += 0.5 * mod(id.y, 2.0); // offset alternate rows
    vec2 f = fract(uv);
    float mortar = min(min(f.x, 1.0 - f.x), min(f.y, 1.0 - f.y));
    float brick = step(0.05, mortar);
    return vec2(brick, mortar);
}
```

## Hexagon Grid

```glsl
float hexagon(vec2 p) {
    p.x *= 0.57735 * 2.0;
    p.y += mod(floor(p.x), 2.0) * 0.5;
    p = abs(fract(p) - 0.5);
    return abs(max(p.x * 1.5 + p.y, p.y * 2.0) - 1.0);
}
```

## Truchet Tiles

```glsl
float truchet(vec2 uv) {
    vec2 id = floor(uv);
    vec2 f = fract(uv);
    float r = hash(id) > 0.5 ? f.x : 1.0 - f.x; // flip
    float d = abs(r - f.y);
    return step(d, 0.05); // tile edge
}
```
