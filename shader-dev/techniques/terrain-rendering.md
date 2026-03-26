# Terrain Rendering

## FBM Terrain

```glsl
float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float noise(vec2 p) {
    vec2 i = floor(p), f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(mix(hash(i), hash(i + vec2(1,0)), u.x),
               mix(hash(i + vec2(0,1)), hash(i + vec2(1,1)), u.x), u.y);
}
float fbm(vec2 p) {
    float v = 0.0, a = 0.5;
    for(int i = 0; i < 6; i++) { v += a * noise(p); p *= 2.0; a *= 0.5; }
    return v;
}
float terrain(vec2 p) { return fbm(p * 0.1) * 4.0 - 1.0; }
```

## Heightfield Ray Marching

```glsl
float rayMarchTerrain(vec3 ro, vec3 rd) {
    float t = 0.0;
    for(int i = 0; i < 64; i++) {
        vec3 p = ro + rd * t;
        float h = p.y - terrain(p.xz);
        if(abs(h) < 0.001 * t) return t;
        if(t > 100.0) break;
        t += h * 0.5;
    }
    return -1.0;
}
```

## Erosion Simulation

```glsl
// Thermal erosion approximation
float erode(float h, vec2 p, float rate) {
    float dh = fbm(p + 0.1) - fbm(p - 0.1);
    return h - rate * max(0.0, dh);
}
```
