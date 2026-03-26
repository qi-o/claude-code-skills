# Color Palette Generation

## Inigo Quilez Cosine Palette

```glsl
vec3 palette(float t, vec3 a, vec3 b, vec3 c, vec3 d) {
    return a + b * cos(6.28318 * (c * t + d));
}

// Usage:
vec3 col = palette(v, vec3(0.5), vec3(0.5), vec3(1.0), vec3(0.0, 0.33, 0.67));
```

## Common Palettes

| Palette | a | b | c | d |
|---------|---|---|---|---|
| Rainbow | (0.5,0.5,0.5) | (0.5,0.5,0.5) | (1,1,1) | (0,0.33,0.67) |
| Sunset | (0.5,0.5,0.5) | (0.5,0.5,0.5) | (1,1,1) | (0,0.1,0.2) |
| Inferno | (0.5,0.5,0.5) | (0.5,0.5,0.5) | (1,1,1) | (0,0.14,0.68) |
| Viridis | (0.5,0.5,0.5) | (0.5,0.5,0.5) | (1,1,1) | (0.13,0.56,0.82) |

## HSL to RGB

```glsl
vec3 hsl2rgb(vec3 hsl) {
    vec3 rgb = clamp(abs(mod(hsl.x*6.0+vec3(0,4,2),6.0)-3.0)-1.0, 0.0, 1.0);
    return hsl.z + hsl.y * (rgb-0.5)*(1.0-abs(2.0*hsl.z-1.0));
}
```

## Oklab (Perceptual)

```glsl
// For more perceptually uniform color mapping
vec3 oklab_mix(vec3 a, vec3 b, float t) {
    // Convert to oklab, interpolate, convert back
}
```
