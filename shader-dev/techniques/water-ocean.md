# Water & Ocean Rendering

## Gerstner Waves

```glsl
vec3 gerstnerWave(vec3 pos, vec2 dir, float steepness, float wavelength, float time) {
    float k = 2.0 * 3.14159 / wavelength;
    float c = sqrt(9.8 / k);
    vec2 d = normalize(dir);
    float f = k * (dot(d, pos.xz) - c * time);
    float a = steepness / k;
    return vec3(d.x * (a * cos(f)), a * sin(f), d.y * (a * cos(f)));
}
```

## FFT Ocean (Simplified)

```glsl
// Heightfield from spectrum
float oceanHeight(vec2 p, float time) {
    float h = 0.0;
    for(int i = 0; i < 8; i++) {
        float fi = float(i);
        float k = pow(2.0, fi * 0.25) * 0.5;
        float ph = noise(p * k + time * sqrt(9.8 * k)) * 6.28;
        h += sin(dot(p, vec2(cos(ph), sin(ph))) * k) / k;
    }
    return h;
}
```

## Caustics

```glsl
float caustics(vec2 p, float time) {
    float c = 0.0;
    for(int i = 0; i < 3; i++) {
        vec2 tp = p + noise(p + time * 0.1) * 0.1;
        c += pow(0.5 + 0.5 * sin(length(tp) * 10.0 - time), 3.0);
    }
    return c / 3.0;
}
```
