# Camera Effects

## Depth of Field (Thin Lens)

```glsl
vec3 depthOfField(vec3 ro, vec3 rd, vec3 focus, float aperture) {
    vec3 p = ro + rd * dot(focus - ro, normalize(rd));
    vec2 offset = (random2(uv) - 0.5) * aperture;
    vec3 newDir = normalize(p - ro - offset);
    return newDir;
}
```

## Motion Blur

```glsl
// Per-frame: average multiple samples with time offset
vec3 mb(vec2 uv, float time) {
    vec3 col = vec3(0.0);
    for (float i = 0.0; i < 8.0; i++) {
        float t = time - 0.01 * i / 8.0;
        col += render(uv, t);
    }
    return col / 8.0;
}
```

## Lens Distortion

```glsl
vec2 lensDistort(vec2 uv, float k, float k2) {
    vec2 cc = uv - 0.5;
    float dist = dot(cc, cc);
    return uv + cc * (k * dist + k2 * dist * dist);
}
```
