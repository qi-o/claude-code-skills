# Ambient Occlusion

## SDF-Based AO

```glsl
float calcAO(vec3 p, vec3 n) {
    float occ = 0.0;
    float sca = 1.0;
    for(int i = 0; i < 5; i++) {
        float h = 0.01 + 0.12 * float(i);
        float d = map(p + h * n);
        occ += (h - d) * sca;
        sca *= 0.7;
    }
    return clamp(1.0 - 3.0 * occ, 0.0, 1.0);
}
```

## Screen-Space AO (SSAO)

```glsl
// Requires depth buffer + normal buffer
float ssao(vec3 p, vec3 n, sampler2D depthTex, vec2 uv) {
    float radius = 0.5;
    float occlusion = 0.0;
    for(int i = 0; i < 16; i++) {
        vec2 offset = noise2(uv + float(i) * 43.2) * radius;
        float depth = texture(depthTex, uv + offset).r;
        occlusion += step(depth, p.z - 0.01);
    }
    return 1.0 - occlusion / 16.0;
}
```
