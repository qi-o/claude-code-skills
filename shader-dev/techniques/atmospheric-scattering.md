# Atmospheric Scattering

## Rayleigh/Mie Scattering

```glsl
vec3 rayleigh(float cosTheta) {
    return 3.0 / (16.0 * 3.14159) * (1.0 + cosTheta * cosTheta);
}
float mie(float cosTheta, float g) {
    float g2 = g * g;
    return (1.0 - g2) / (4.0 * 3.14159 * pow(1.0 + g2 - 2.0 * g * cosTheta, 1.5));
}
vec3 atmosphere(vec3 rd, vec3 sunDir) {
    float cosTheta = dot(rd, sunDir);
    return rayleigh(cosTheta) * vec3(0.05, 0.15, 0.4) +
           mie(cosTheta, 0.8) * vec3(0.5);
}
```

## God Rays (Crepuscular)

```glsl
float godRays(vec2 uv, vec2 lightPos, int samples) {
    float rays = 0.0;
    vec2 delta = (uv - lightPos) / float(samples);
    float t = 0.0;
    for(int i = 0; i < samples; i++) {
        t += length(delta);
        rays += texture2D(uOccluder, uv - delta * float(i)).r;
    }
    return rays / float(samples);
}
```
