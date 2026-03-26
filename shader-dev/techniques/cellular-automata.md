# Cellular Automata

## Game of Life

```glsl
int countNeighbors(ivec2 px) {
    int n = 0;
    for(int dy = -1; dy <= 1; dy++)
        for(int dx = -1; dx <= 1; dx++)
            if(dx != 0 || dy != 0)
                n += texelFetch(uState, px + ivec2(dx, dy), 0).r > 0.5 ? 1 : 0;
    return n;
}
float gol(vec2 uv, float time) {
    ivec2 px = ivec2(uv * uResolution);
    int n = countNeighbors(px);
    float current = texelFetch(uState, px, 0).r > 0.5 ? 1.0 : 0.0;
    if(current == 1.0) return (n == 2 || n == 3) ? 1.0 : 0.0;
    else return n == 3 ? 1.0 : 0.0;
}
```

## Reaction-Diffusion

```glsl
// Gray-Scott model
vec2 reactDiffuse(vec2 uv, float time) {
    vec2 u = texture2D(uTex, uv).xy;
    float a = u.x, b = u.y;
    vec2 lap = laplacian(uv);
    float da = 1.0 * lap.x - a * b * b + 0.1 * (1.0 - a);
    float db = 0.5 * lap.y + a * b * b - 0.15 * b;
    return vec2(da, db) * 0.00016 + u;
}

vec2 laplacian(vec2 uv) {
    vec2 c = texture2D(uTex, uv).xy;
    vec2 n = texture2D(uTex, uv + vec2(0, 1) / uResolution).xy;
    vec2 s = texture2D(uTex, uv - vec2(0, 1) / uResolution).xy;
    vec2 e = texture2D(uTex, uv + vec2(1, 0) / uResolution).xy;
    vec2 w = texture2D(uTex, uv - vec2(1, 0) / uResolution).xy;
    return (n + s + e + w - 4.0 * c);
}
```
