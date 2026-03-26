# Shadow Techniques

## Hard Shadow

```glsl
float hardShadow(vec3 ro, vec3 rd, float mint, float maxt) {
    for(float t = mint; t < maxt;) {
        float h = map(ro + rd * t);
        if(h < 0.001) return 0.0;
        t += h;
    }
    return 1.0;
}
```

## Soft Shadow (Penumbra)

```glsl
float softShadow(vec3 ro, vec3 rd, float mint, float maxt, float k) {
    float res = 1.0;
    float ph = 1e20;
    for(float t = mint; t < maxt;) {
        float h = map(ro + rd * t);
        if(h < 0.001) return 0.0;
        float y = h*h / (2.0 * ph);
        float d = sqrt(h*h - y*y);
        res = min(res, k * d / max(0.0, t - y));
        ph = h;
        t += h;
    }
    return clamp(res, 0.0, 1.0);
}
```

## Cascade Shadows

```glsl
// PCF-style cascade
float cascadeShadow(vec3 p, vec3 n, float bias) {
    vec3 lightDir = normalize(vec3(0.5, 0.7, -0.3));
    float shadow = 0.0;
    float t = bias;
    for(int i = 0; i < 4; i++) {
        shadow += softShadow(p + n * 0.01, lightDir, 0.02, 10.0, 8.0);
        // blur offset would go here
    }
    return shadow / 4.0;
}
```
