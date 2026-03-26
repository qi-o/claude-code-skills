# Post-Processing

## Tone Mapping

```glsl
// ACES Filmic
vec3 aces(vec3 x) {
    float a = 2.51, b = 0.03, c = 2.43, d = 0.59, e = 0.14;
    return clamp((x*(a*x+b))/(x*(c*x+d)+e), 0.0, 1.0);
}

// Reinhard
vec3 reinhard(vec3 x) { return x / (1.0 + x); }
```

## Bloom

```glsl
// Separable Gaussian blur for bloom extraction
vec3 blur9(sampler2D tex, vec2 uv, vec2 resolution, float radius) {
    vec3 col = vec3(0.0);
    float total = 0.0;
    for(float x = -4.0; x <= 4.0; x += 1.0) {
        float w = exp(-0.5 * x * x / (radius * radius));
        col += texture(tex, uv + vec2(x, 0.0) / resolution).rgb * w;
        col += texture(tex, uv + vec2(0.0, x) / resolution).rgb * w;
        total += 2.0 * w;
    }
    return col / total;
}
```

## Vignette

```glsl
float vignette(vec2 uv, float strength, float amount) {
    return 1.0 - amount * length(uv - 0.5) * strength;
}
```

## Chromatic Aberration

```glsl
vec3 chromaticAberration(sampler2D tex, vec2 uv, float amount) {
    vec2 dir = uv - 0.5;
    float r = texture(tex, uv + dir * amount).r;
    float g = texture(tex, uv).g;
    float b = texture(tex, uv - dir * amount).b;
    return vec3(r, g, b);
}
```

## Glitch Effect

```glsl
vec3 glitch(vec2 uv, sampler2D tex, float time) {
    float t = floor(time * 10.0);
    vec2 uv_glitch = uv + vec2(hash(t) * 0.05, 0.0);
    return texture(tex, uv_glitch).rgb;
}
```
