# Volumetric Rendering

## Volume Ray Marching

```glsl
vec4 volMarch(vec3 ro, vec3 rd, float maxDist) {
    vec4 col = vec4(0.0);
    float t = 0.0;
    for(int i = 0; i < 64; i++) {
        vec3 p = ro + rd * t;
        float density = volumeDensity(p); // your density field
        if(density > 0.01) {
            vec4 c = volumeColor(p, density);
            c.a *= 0.1; // absorption
            c.rgb *= c.a;
            col += c * (1.0 - col.a);
        }
        t += maxDist / 64.0;
        if(col.a > 0.95) break;
    }
    return col;
}
```

## Cloud Rendering

```glsl
float cloudDensity(vec3 p) {
    float h = smoothstep(0.0, 1.5, p.y) * smoothstep(5.0, 1.5, p.y);
    return h * fbm(p.xz * 0.3 + vec2(0.0, p.y * 0.1));
}
```
