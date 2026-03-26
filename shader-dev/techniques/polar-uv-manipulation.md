# Polar UV Manipulation

## Cartesian to Polar

```glsl
vec2 toPolar(vec2 uv) {
    return vec2(length(uv), atan(uv.y, uv.x));
}
```

## Kaleidoscope

```glsl
vec2 kaleidoscope(vec2 uv, float segments) {
    vec2 p = toPolar(uv - 0.5);
    p.y = mod(p.y, 6.28 / segments);
    return p.x * vec2(cos(p.y), sin(p.y)) + 0.5;
}
```

## Spiral Mapping

```glsl
vec2 spiral(vec2 uv, float turns) {
    vec2 p = toPolar(uv - 0.5);
    p.y += p.x * turns * 6.28;
    return p.x * vec2(cos(p.y), sin(p.y)) + 0.5;
}
```
