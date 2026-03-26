# Texture Sampling

## Bicubic Interpolation

```glsl
vec2 m = mod(uv * resolution - 0.5, 1.0);
vec2 f = m * m * (3.0 - 2.0 * m); // smoothstep
// Then bilinear sample with f as offset
```

## Mipmap Selection

```glsl
// Explicit LOD
float lod = 2.0;
vec4 c = textureLod(uTex, uv, lod);

// Anisotropic
vec4 anisotropicSample(sampler2D tex, vec2 uv, vec2 duvdx, vec2 duvdy) {
    float rx = length(duvdx) * textureSize(uTex, 0).x;
    float ry = length(duvdy) * textureSize(uTex, 0).y;
    float r = max(rx, ry);
    return textureGrad(uTex, uv, duvdx, duvdy);
}
```

## Procedural Texture

```glsl
// Checkered pattern
float checker(vec2 uv) {
    vec2 q = floor(uv);
    return mod(q.x + q.y, 2.0);
}
```
