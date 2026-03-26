# Anti-Aliasing

## SSAA (Super Sample AA)

Render at higher resolution, scale down. Most expensive, highest quality.

## MSAA (Multi Sample AA)

Built into WebGL2: `gl.drawArraysInstanced` with MSAA config.

## Post-Process AA (FXAA)

```glsl
float fxaa(vec2 uv, sampler2D tex) {
    vec2 texel = 1.0 / vec2(textureSize(tex, 0));
    // Luma at center
    float lumaCenter = luma(texture(tex, uv));
    float lumaDown = luma(texture(tex, uv + vec2(0,-1) * texel));
    float lumaUp = luma(texture(tex, uv + vec2(0,1) * texel));
    float lumaLeft = luma(texture(tex, uv + vec2(-1,0) * texel));
    float lumaRight = luma(texture(tex, uv + vec2(1,0) * texel));
    // ... (simplified - full implementation uses more samples)
}
```

## TAA (Temporal AA)

```glsl
// Use previous frame data
vec4 prev = texture(uPrevFrame, uv);
// Reproject based on camera velocity
```
