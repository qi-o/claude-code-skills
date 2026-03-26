# Procedural Noise

## Value Noise

```glsl
float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float valueNoise(vec2 p) {
    vec2 i = floor(p), f = fract(p);
    float a = hash(i);
    float b = hash(i + vec2(1.0, 0.0));
    float c = hash(i + vec2(0.0, 1.0));
    float d = hash(i + vec2(1.0, 1.0));
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(a, b, u.x) + (c - a) * u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
}
```

## Perlin Noise

```glsl
vec2 grad(vec2 p) {
    float h = hash(p);
    return h < 0.25 ? vec2(1,1) :
           h < 0.50 ? vec2(-1,1) :
           h < 0.75 ? vec2(1,-1) : vec2(-1,-1);
}
float perlin(vec2 p) {
    vec2 i = floor(p), f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(mix(dot(grad(i), f), dot(grad(i+vec2(1,0)), f-vec2(1,0)), u.x),
               mix(dot(grad(i+vec2(0,1)), f-vec2(0,1)), dot(grad(i+vec2(1,1)), f-vec2(1,1)), u.x), u.y);
}
```

## FBM

```glsl
float fbm(vec2 p) {
    float v = 0.0, a = 0.5;
    for(int i = 0; i < 6; i++) { v += a * noise(p); p *= 2.0; a *= 0.5; }
    return v;
}
float fbm(vec3 p) {
    float v = 0.0, a = 0.5;
    for(int i = 0; i < 6; i++) { v += a * perlin(p.xy); p.xz *= 2.0; a *= 0.5; }
    return v;
}
```

## Worley Noise

```glsl
float worley(vec2 p) {
    vec2 i = floor(p);
    float minDist = 1e10;
    for(int y = -1; y <= 1; y++)
        for(int x = -1; x <= 1; x++) {
            vec2 cell = i + vec2(x, y);
            vec2 point = cell + hash2(cell);
            minDist = min(minDist, length(p - point));
        }
    return minDist;
}
```
