# Voronoi / Cellular Noise

## Classic Voronoi

```glsl
vec2 hash2(vec2 p) { return fract(sin(vec2(dot(p,vec2(127.1,311.7)), dot(p,vec2(269.5,183.3))))*43758.5453); }
float voronoi(vec2 p) {
    vec2 i = floor(p), f = fract(p);
    float minDist = 1e10;
    for(int y = -1; y <= 1; y++)
        for(int x = -1; x <= 1; x++) {
            vec2 neighbor = vec2(x, y);
            vec2 point = hash2(i + neighbor);
            point = 0.5 + 0.5 * sin(6.28 * point); // animate
            vec2 diff = neighbor + point - f;
            minDist = min(minDist, length(diff));
        }
    return minDist;
}
```

## Worley Noise (Voronoi F1)

```glsl
float worley(vec2 p) { return voronoi(p); }
```

## Cracked Earth Effect

```glsl
float cracks(vec2 p) {
    float v = voronoi(p * 3.0);
    return smoothstep(0.0, 0.05, v - 0.02);
}
```
